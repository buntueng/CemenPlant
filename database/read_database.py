import sqlite3
from sqlite3 import Error
import os

database_path = os.path.dirname(os.path.realpath(__file__))
db_file = database_path+"/main_db.db"
db_connector = False

def read_booking():
    cmd = "SELECT * FROM booking_table"
    event_list = read_table_execute(cmd)
    for event_data in event_list:
        print(event_data)


def read_event_log():
    cmd = "SELECT * FROM event_log_table"
    event_list = read_table_execute(cmd)
    for event_data in event_list:
        print(event_data)

def read_user_table():
    cmd = "SELECT * FROM user_table"
    user_list = read_table_execute(cmd)
    for username in user_list:
        print(username)

def read_concrete_formula():
    cmd = "SELECT * FROM concrete_formula_table"
    concrete_formula_list = read_table_execute(cmd)
    for formula in concrete_formula_list:
        print(formula)

def read_table_execute(cmd):
    db_connector = sqlite3.connect(db_file)
    db_cursor = db_connector.cursor()
    db_cursor.execute(cmd)
    response_list = db_cursor.fetchall()
    db_connector.close()
    return response_list

def delete_table_execute(cmd):
    db_connector = sqlite3.connect(db_file)
    db_cursor = db_connector.cursor()
    db_cursor.execute(cmd)
    db_connector.commit()
    db_connector.close()

def delete_all_in_booking_table():
    cmd = "DELETE FROM booking_table"
    delete_table_execute(cmd)



# read_event_log()
# read_user_table()
# read_concrete_formula()
# delete_all_in_booking_table()
read_booking()