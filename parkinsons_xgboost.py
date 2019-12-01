#Importing all the libraries
import numpy as np
import pandas as pd
import os, sys
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#importing data and processing
df = pd.read_csv('parkinsons.data')
df = pd.read_csv(r'https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data')
# features = df.loc[:, df.columns!='status'].values[:,1:]
labels = df.loc[:,'status'].values

#scaling for better performance
scaler = MinMaxScaler((-1,1))
x = scaler.fit_transform(features)
y=labels

#setting up training and testing datasets and results
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)

#initiating XGB classifier and fitting to the training dataset
model = XGBClassifier()
model.fit(x_train, y_train)

#producing predicted values and scoring accuracy compared to testing results
y_pred = model.predict(x_test)
print('Model accuracy in % {0: .2f}: '.format(accuracy_score(y_test, y_pred)*100))
