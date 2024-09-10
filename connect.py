import os
import yfinance as yf
import pyodbc
from dotenv import load_dotenv, dotenv_values 

def connect_to_azure():
    load_dotenv() 
    server = os.getenv('SERVER')
    database = 'mySampleDatabase'
    username = 'azureuser'
    password = os.getenv('PASSWORD')
    driver = '{ODBC Driver 18 for SQL Server}'
    connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    # print(type(connection_string))
    return connection_string

# load_dotenv() 
# server = os.getenv('SERVER')
# database = 'mySampleDatabase'
# username = 'azureuser'
# password = os.getenv('PASSWORD')
# driver = '{ODBC Driver 18 for SQL Server}'

# connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'


# conn = pyodbc.connect(connection_string)