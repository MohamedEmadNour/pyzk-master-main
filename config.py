import urllib.parse
from connectionstring import conn_str

class Config:
    JWT_SECRET_KEY = 'ffc632ce-0053-4bab-8077-93a4d14caaad'
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
