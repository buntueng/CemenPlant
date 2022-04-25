import sqlite3
from sqlite3 import Error
import os

database_path = os.path.dirname(os.path.realpath(__file__))
db_file = database_path+"\\main_db.db"
db_connector = False

def add_user(user_name,first_name,last_name,password):
    try:
        db_connector = sqlite3.connect(db_file)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'SELECT User_Name FROM user_table WHERE User_Name = ?'
        db_cursor.execute(sql_query,(user_name,))
        rows = db_cursor.fetchall()
        if len(rows) <= 0:
            # ====== add user ==============
            db_cursor.execute('INSERT INTO user_table(User_Name,First_Name,Last_Name,Password) VALUES(?,?,?,?)',(user_name,first_name,last_name,password))
            db_connector.commit()
            print('new user was added')
        else:
            print("This user is exist")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()

def remove_user(user_name):
    try:
        db_connector = sqlite3.connect(db_file)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'DELETE FROM user_table WHERE User_Name = ?'
        db_cursor.execute(sql_query,(user_name,))
        db_connector.commit()
        print("Remove complete")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()


#========= main script ========
#add_user(user_name="yana",first_name="Buntueng",last_name="Yana",password="0820216694")
add_user(user_name="bt",first_name="Buntueng",last_name="Yana",password="1234")
#remove_user(user_name="bt")


