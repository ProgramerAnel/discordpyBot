import mysql.connector
import sys
import decimal
import os
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
import time
from dotenv import load_dotenv 
load_dotenv()
 
def insert_sold_remote_record(SKU):
    try:
        mySqlCon = mysql.connector.connect(host=os.getenv('MYSQL_SERVER'),
                                            database=os.getenv('MYSQL_DATABASE'),
                                            user=os.getenv('MYSQL_USERNAME'),
                                            password=os.getenv('MYSQL_PASSWORD'))
        if mySqlCon.is_connected():
            mySQLCurrsor = mySqlCon.cursor()
            mySQLCurrsor.execute("insert into Requests(SKU,Completed, Date_Completed)values('" + str(SKU) + "',0, NOW())")
            mySqlCon.commit()
    except Error as e:
        print('REMOTE_REQUESTS: ',"Error while connecting to MySQL", e)
        return False
    finally:
        if (mySqlCon.is_connected()):
            mySQLCurrsor.close()
            mySqlCon.close()
            print('REMOTE_REQUESTS: ',"MySQL record added ")
            return True
 
 
