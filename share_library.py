import sqlite3
from sqlite3 import Error
import os

window_size = '1024x768'

software_path = os.path.dirname(os.path.realpath(__file__))
database_path = software_path +"\\database\\main_db.db"



def default_window_size():
    return window_size

def center_screen(top_level_window):
    top_level_window.update_idletasks()
    width = top_level_window.winfo_width()
    frm_width = top_level_window.winfo_rootx() - top_level_window.winfo_x()
    win_width = width + 2 * frm_width
    height = top_level_window.winfo_height()
    titlebar_height = top_level_window.winfo_rooty() - top_level_window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = top_level_window.winfo_screenwidth() // 2 - win_width // 2
    y = top_level_window.winfo_screenheight() // 2 - win_height // 2
    top_level_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    top_level_window.deiconify()

def read_concrete_formula_from_db():
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'SELECT * FROM concrete_formula_table'
    db_cursor.execute(sql_query)
    rows = db_cursor.fetchall()
    return rows

def update_concrete_formula(formula_id,description,agg1_weight,agg2_weight,agg3_weight,cemen_weight,flyash_weight,water_weight,chemical1_weight,chemical2_weight):
    try:
        db_connector = sqlite3.connect(database_path)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'SELECT Formula_ID FROM concrete_formula_table WHERE Formula_ID = ?'
        db_cursor.execute(sql_query,(formula_id,))
        rows = db_cursor.fetchall()
        if len(rows) <= 0:
            # ====== add new formula ==============
            db_cursor.execute('INSERT INTO concrete_formula_table(Formula_ID,Description,Agg1,Agg2,Agg3,Cemen,Flyash,Water,Chemical1,Chemical2) VALUES(?,?,?,?,?,?,?,?,?,?)',(formula_id,description,agg1_weight,agg2_weight,agg3_weight,cemen_weight,flyash_weight,water_weight,chemical1_weight,chemical2_weight))
            db_connector.commit()
        #    print('new formula was added')
        #else:
        #    print("This formula is exist")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()


def clear_all_formula():
    try:
        db_connector = sqlite3.connect(database_path)
        db_cursor = db_connector.cursor()
        # ==== check existing user =====
        sql_query = 'DELETE FROM concrete_formula_table'
        db_cursor.execute(sql_query)
        db_connector.commit()
        #print("Clean complete")

    except Error as e:
        print(e)
    finally:
        if db_connector:
            db_connector.close()