import pyodbc
import win32com.client # need to get pypiwin32 (pip install pypiwin32)
import time

est=0 #variable to check if a connection to SQL server has been established

while est==0: #loop until connection exists
	cn = pyodbc.connect(driver = '{SQL Server Native Client 11.0}', server = server_name, database = db_name, Trusted_Connection='yes', autocommit = True) 
	if cn is None:
		est=0
		time.sleep(300) #wait 5 minutes if db unavailable, try again
	else:
		est=1

cr = cn.cursor()
cr.execute("exec procedure")
fn = daily sales template pathname
xl = win32com.client.DispatchEx("Excel.Application")
wb = xl.workbooks.open(fn)
xl.Visible=True

#setting background refresh to false so that everything is updated before macros are run
for c in wb.Connections:
	c.OLEDBConnection.BackgroundQuery=False
	c.Refresh()
	c.OLEDBConnection.BackgroundQuery=True

xl.Run('ValuesCopy')
xl.Run('daily_sales_file!SendMail')
wb.Close(False)
xl.Quit()
