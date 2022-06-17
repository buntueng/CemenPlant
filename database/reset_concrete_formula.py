import sqlite3
from sqlite3 import Error
import os

database_path = os.path.dirname(os.path.realpath(__file__))
db_file = database_path+"/main_db.db"
db_connector = False

def add_concrete_formula(formula_id,description,agg1_weight,agg2_weight,agg3_weight,cemen_weight,flyash_weight,water_weight,chemical1_weight,chemical2_weight):
    try:
        db_connector = sqlite3.connect(db_file)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'SELECT Formula_ID FROM concrete_formula_table WHERE Formula_ID = ?'
        db_cursor.execute(sql_query,(formula_id,))
        rows = db_cursor.fetchall()
        if len(rows) <= 0:
            # ====== add new formula ==============
            db_cursor.execute('INSERT INTO concrete_formula_table(Formula_ID,Description,Agg1,Agg2,Agg3,Cemen,Flyash,Water,Chemical1,Chemical2) VALUES(?,?,?,?,?,?,?,?,?,?)',(formula_id,description,agg1_weight,agg2_weight,agg3_weight,cemen_weight,flyash_weight,water_weight,chemical1_weight,chemical2_weight))
            db_connector.commit()
            print('new formula was added')
        else:
            print("This formula is exist")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()

def remove_concrete_formula(formula_id):
    try:
        db_connector = sqlite3.connect(db_file)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'DELETE FROM concrete_formula_table WHERE Formula_ID = ?'
        db_cursor.execute(sql_query,(formula_id,))
        db_connector.commit()
        print("Remove complete")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()

def clear_all_formula():
    try:
        db_connector = sqlite3.connect(db_file)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'DELETE FROM concrete_formula_table'
        db_cursor.execute(sql_query)
        db_connector.commit()
        print("Clean complete")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()
#========= main script ========

clear_all_formula()
add_concrete_formula(1,"สูตร 1",100,200,200,200,200,100,1,1.1)
add_concrete_formula(2,"สูตร 2",200,200,200,200,200,100,1,1.2)
add_concrete_formula(3,"สูตร 3",300,200,200,200,200,100,1,1.3)
add_concrete_formula(4,"สูตร 4",400,200,200,200,200,100,1,1.4)
add_concrete_formula(5,"สูตร 5",500,200,200,200,200,100,1,1.5)
add_concrete_formula(6,"สูตร 6",600,200,200,200,200,100,1,1.6)
add_concrete_formula(7,"สูตร 7",700,200,200,200,200,100,1,1.7)
add_concrete_formula(8,"สูตร 8",800,200,200,200,200,100,1,1.8)
add_concrete_formula(9,"สูตร 8",800,200,200,200,200,100,1,1.8)
add_concrete_formula(10,"สูตร 8",800,200,200,200,200,100,1,1.8)
add_concrete_formula(11,"สูตร 8",800,200,200,200,200,100,1,1.8)

