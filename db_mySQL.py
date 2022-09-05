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
        connection = mysql.connector.connect(host=os.getenv('MYSQL_SERVER'),
                                            database=os.getenv('MYSQL_DATABASE'),
                                            user=os.getenv('MYSQL_USERNAME'),
                                            password=os.getenv('MYSQL_PASSWORD'))
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("insert into Requests(SKU,Completed, Date_Completed)values('" + str(SKU) + "',0, NOW())")
            connection.commit()
    except Error as e:
        print('REMOTE_REQUESTS: ',"Error while connecting to MySQL", e)
        return False
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print('REMOTE_REQUESTS: ',"MySQL record added ")
            return True
 
 
