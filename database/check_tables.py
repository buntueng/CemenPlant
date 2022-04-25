import sqlite3
from sqlite3 import Error
import os

database_path = os.path.dirname(os.path.realpath(__file__))
db_file = database_path+"\\main_db.db"
db_connector = False


try:
    db_connector = sqlite3.connect(db_file)
    db_cursor = db_connector.cursor()
    #====== check tables =======
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(db_cursor.fetchall())

    
except Error as e:
    print("error")
    print(e)
finally:
    db_connector.commit()
    if db_connector:
        db_connector.close()
