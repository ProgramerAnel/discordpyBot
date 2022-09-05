import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

class DBSQL:
    def __init__(self):
        self.driver = '{ODBC Driver 18 for SQL Server}'
        #self.driver = '{SQL Server}'
        self.server = os.getenv('SQL_SERVER')
        self.db = os.getenv('SQL_DATABASE')
        self.user = os.getenv('SQL_USER')
        self.password = os.getenv('SQL_PASSWORD')
      
    def execute(self, query, *params):
        pyodbc.connect(f'DRIVER={self.driver};' + f'SERVER={self.server};DATABSE={self.db};UID={self.user};PWD={self.password};TrustServerCertificate=yes;').cursor().execute(query, params).commit()
        
    def execute_and_fetch(self, query, *params):
        conn = pyodbc.connect(f'DRIVER={self.driver};' + f'SERVER={self.server};DATABSE={self.db};UID={self.user};PWD={self.password};TrustServerCertificate=yes;')
        result = conn.cursor().execute(query, params).fetchall()
        conn.commit()
        return result

    def fetch_one_field(self, field_name):
        conn = pyodbc.connect(f'DRIVER={self.driver};' + f'SERVER={self.server};DATABSE={self.db};UID={self.user};PWD={self.password};TrustServerCertificate=yes;')
        result = conn.cursor().execute('select attribute_value from sellduct.dbo.setup where attribute =?', field_name).fetchall()
        conn.commit() 
        for row in result:
            return row.attribute_value

    def fetch_one_value_by_query(self, query):
        conn = pyodbc.connect(f'DRIVER={self.driver};' + f'SERVER={self.server};DATABSE={self.db};UID={self.user};PWD={self.password};TrustServerCertificate=yes;')
        result = conn.cursor().execute(query).fetchall()
        conn.commit() 
        for row in result:
            return row.attribute_value