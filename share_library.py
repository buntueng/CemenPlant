import sqlite3
from sqlite3 import Error
import os
from datetime import datetime


window_size = '1180x768'

software_path = os.path.dirname(os.path.realpath(__file__))
database_path = software_path +"/database/main_db.db"

def save_complete_queue(data_list):
    now = datetime.now()
    current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    # ==== check existing user =====
    # sql_query = "INSERT INTO recording_table(Record_Time, Booking_ID, Customer_Name, Keep_Sample,Amount,Agg1_Target,Agg2_Target,Agg3_Target,Cemen_Target,Flyash_Target,Water_Target,Chemical1_Target,Chemical2_Target,Agg1_Measure,Agg2_Measure,Agg3_Measure,Cemen_Measure,Flyash_Measure,Water_Measure,Chemical1_Measure,Chemical2_Measure,Description) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    # db_cursor.execute(sql_query,(current_datetime,data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15],data_list[16],data_list[17],data_list[18],data_list[19],data_list[20]))
    #sql_query = "INSERT INTO recording_table(Record_Time) VALUES(?)"
    sql_query = "INSERT INTO recording_table(Booking_ID, Record_Time, Customer_Name,Keep_Sample,Amount,Description,Agg1_Target,Agg2_Target,Agg3_Target,Cemen_Target,Flyash_Target,Water_Target,Chemical1_Target,Chemical2_Target,Agg1_Measure,Agg2_Measure,Agg3_Measure,Cemen_Measure,Flyash_Measure,Water_Measure,Chemical1_Measure,Chemical2_Measure) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    db_cursor.execute(sql_query,(data_list[0],current_datetime,data_list[1],data_list[2],data_list[3],data_list[20],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10],data_list[11],data_list[12],data_list[13],data_list[14],data_list[15],data_list[16],data_list[17],data_list[18],data_list[19]))
    db_connector.commit()
    db_connector.close()

def read_concrete_formula(formula_id):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = "SELECT * FROM concrete_formula_table WHERE Formula_ID = ?"
    db_cursor.execute(sql_query,(formula_id,))
    [response_list] = db_cursor.fetchall()
    db_connector.close()
    return response_list

def complete_booking_queue(booking_id):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'UPDATE booking_table SET Booking_Status = 3 WHERE Booking_ID = ?'
    db_cursor.execute(sql_query,(booking_id,))
    db_connector.commit()
    db_connector.close()

def fail_booking_queue(booking_id):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'UPDATE booking_table SET Booking_Status = 4 WHERE Booking_ID = ?'
    db_cursor.execute(sql_query,(booking_id,))
    db_connector.commit()
    db_connector.close()

def relife_booking_queue(booking_id):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'UPDATE booking_table SET Booking_Status = 0 WHERE Booking_ID = ?'
    db_cursor.execute(sql_query,(booking_id,))
    db_connector.commit()
    db_connector.close()

def process_booking_queue(booking_id):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'UPDATE booking_table SET Booking_Status = 1 WHERE Booking_ID = ?'
    db_cursor.execute(sql_query,(booking_id,))
    db_connector.commit()
    db_connector.close()


def remove_booking_queue(booking_id):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'UPDATE booking_table SET Booking_Status = 2 WHERE Booking_ID = ?'
    db_cursor.execute(sql_query,(booking_id,))
    db_connector.commit()
    db_connector.close()

def read_booking_queue():
    cmd = 'SELECT Booking_ID,Booking_Date_Time,Customer_Name,Phone,Amount FROM booking_table WHERE Booking_Status = "0" ORDER BY Booking_Date_Time DESC'
    queue_list = read_table_execute(cmd)

    return queue_list

def read_table_execute(cmd):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    db_cursor.execute(cmd)
    response_list = db_cursor.fetchall()
    db_connector.close()
    return response_list

def update_table_execute(cmd):
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    db_cursor.execute(cmd)
    db_connector.close()


def record_booking_data(data_list):
    now = datetime.now()
    current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    # ==== check existing user =====
    sql_query = "INSERT INTO booking_table(Record_Time, Booking_Date_Time, Customer_Name, Address,Phone,Keep_Sample,Amount,Formula_ID,Booking_Status,Comment) VALUES(?,?,?,?,?,?,?,?,?,?)"
    db_cursor.execute(sql_query,(current_datetime,data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],0,data_list[7]))
    db_connector.commit()
    db_connector.close()

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
    db_connector.close()
    return rows

def get_processing_queue():
    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'SELECT Booking_ID,Customer_Name,Phone,Amount,Formula_ID,Keep_Sample,Address,Comment FROM booking_table WHERE Booking_Status = "1" ORDER BY Booking_Date_Time ASC LIMIT 1'
    db_cursor.execute(sql_query)
    result = []
    rows = db_cursor.fetchall()
    if len(rows) > 0:
        result = list(rows[0])
        sql_query = 'SELECT Description FROM concrete_formula_table WHERE Formula_ID = ' + str(result[4])
        db_cursor.execute(sql_query)
        [Formula_Name] = db_cursor.fetchall()
        result.append(Formula_Name[0])
    db_connector.close()
        

    # ====== read formula name ============
    return result

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