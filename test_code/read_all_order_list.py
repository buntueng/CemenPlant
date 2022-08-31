import sqlite3
import os

software_path = os.path.dirname(os.path.realpath(__file__)).replace('\\test_code','')
database_path = software_path +"/database/main_db.db"
print(database_path)
db_connector = sqlite3.connect(database_path)
db_cursor = db_connector.cursor()
cmd = 'SELECT * FROM booking_table'
db_cursor.execute(cmd)
response_list = db_cursor.fetchall()
db_connector.close()
for the_list in response_list:
    print(the_list)