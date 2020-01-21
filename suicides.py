import pandas as pd
from tabulate import tabulate
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
from hdx.location.country import Country
import math

#getting a country and region table
allCountryData = Country.countriesdata(use_live=False)
detailCountryData = allCountryData['countries']
countryRegion = pd.DataFrame(columns=['country', 'region'])

for country in detailCountryData:
    countryRegion = countryRegion.append({'country':detailCountryData[country]['#country+name+preferred'],
                                          'region': detailCountryData[country]['#region+main+name+preferred']},
                                         ignore_index=True)

#reading data and correcting column names
data = pd.read_csv(r'./suicides.csv')
data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population', 'suicides_per_100k', 'country_year',
            'HDI_year', 'gdp_year', 'gdp_per_capita', 'generation']
# print(tabulate(data.head(20), headers='keys', tablefmt='github'))

#making sorting by age easier and dropping rows with NaN
data['age'] = data['age'].map({ '5-14 years' : '1. 5-14 years' , '15-24 years' : '2. 15-24 years',
                               '25-34 years' : '3. 25-34 years', '35-54 years' : '4. 35-54 years',
                               '55-74 years' : '5. 55-74 years', '75+ years'   : '6. 75+ years'})
data.dropna()

# Dropping rows that don't have all the age brackets
def age_clean(d):
    incData = d.groupby(['year', 'country', 'sex'], as_index = False).agg('age').count()
    incData = incData[incData['age'] == 6]
    return incData

# Feature engineering
def ratio(df, source, target, lod = 'country'):
    if lod=='region':
        perc_df = df.groupby(['year', 'region', 'age', 'sex']).agg(source).sum().rename(target)
    else:
        perc_df = df.groupby(['year', 'country', 'age', 'sex']).agg(source).sum().rename(target)
    perc_df = perc_df / perc_df.groupby(level=[0, 1]).transform("sum")
    return perc_df

# Running age clean and correcting type for population and gdp per year
data = data.merge(age_clean(data)[['year', 'country', 'sex']], on=['year', 'country', 'sex'])
data['gdp_year'] = data['gdp_year'].str.replace(',','').astype({'gdp_year': np.int64})
data['population'] = data['population'].astype({'population': np.int64})

#adding region column and creating decade
data = data.merge(countryRegion, on='country', how='left')
# data['year'] = math.floor((data['year'] % 100) / 10.0)
data['decade'] = data['year'] - data['year'] % 10
print(data.head())

# creating age and suicide ratios
data = data.merge(ratio(data, 'population', 'ageRatio'), on = ['year','country','age', 'sex'])
data = data.merge(ratio(data, 'suicides_no', 'suicideRatio'), on = ['year','country','age', 'sex'])

# Removing all rows with 100% rate and rerunning age clean
data = data.drop(data[data['suicideRatio']==1].index)
data = data.merge(age_clean(data)[['year', 'country', 'sex']], on=['year', 'country', 'sex'])

# creating level of detail views
data_country = data.groupby(['country', 'region', 'year', 'gdp_year', 'age', 'sex', 'decade'], as_index=False).agg({'suicides_no': 'sum', 'population': 'sum', 'suicideRatio':'sum', 'ageRatio':'sum'})
data_region = data_country.groupby(['region', 'year', 'age', 'sex', 'decade'], as_index=False).agg({'suicides_no': 'sum', 'population': 'sum', 'gdp_year': 'sum'})
data_age = data.groupby(['region', 'country', 'age', 'gdp_year', 'decade'], as_index=False).agg({'suicides_no':'sum', 'population':'sum'})

# feature engineering
data_country['gdp_pc'] = data_country['gdp_year'] / data_country['population']
data_region['suicides_per100k'] = data_region['suicides_no']/(data_region['population']/100000)
data_region = data_region.merge(ratio(data_region, 'population', 'ageRatio', 'region'), on = ['year','region','age', 'sex'])
data_region = data_region.merge(ratio(data_region, 'suicides_no', 'suicideRatio', 'region'), on = ['year','region','age', 'sex'])

# visualizing
sb.set()
pal = ['red', 'blue', 'green', 'black']
# sb.relplot(x='year', y='suicides_per100k', data=data_region, kind='line', hue='region', ci=None )
sb.relplot(x='ageRatio', y='suicideRatio', data = data.sort_values(by = ['region', 'country', 'year', 'age']),
           kind='scatter', style='region', ci=None, row='sex', col='age', hue ='decade', palette=pal )
sb.relplot(x='ageRatio', y='suicideRatio', data = data_region.sort_values(by = ['region', 'year', 'age']),
           kind='scatter', style='region', ci=None, row='sex', col='age', hue ='decade', palette=pal)
plt.show()


