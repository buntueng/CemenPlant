import sqlite3
from sqlite3 import Error
import os

database_path = os.path.dirname(os.path.realpath(__file__))
db_file = database_path+"\\main_db.db"

db_connector = False
try:
    db_connector = sqlite3.connect(db_file)
    db_cursor = db_connector.cursor()
    # ==== create user table =========================================
    create_user_table = """ CREATE TABLE  IF NOT EXISTS user_table(
            User_Name   VARCHAR(255)    NOT NULL,
            First_Name  CHAR(25)        NOT NULL,
            Last_Name   CHAR(25),
            Password    VARCHAR(16)     NOT NULL      ); """
    db_cursor.execute(create_user_table)
    # ====== create concrete formula table =========================================
    create_concrete_formula_table = """ CREATE TABLE  IF NOT EXISTS concrete_formula_table(
            Formula_ID  INT     NOT NULL,
            Description VARCHAR(256) NOT NULL,
            Agg1        INT     NOT NULL,
            Agg2        INT     NOT NULL,
            Agg3        INT     NOT NULL,
            Cemen       INT     NOT NULL,
            Flyash      INT     NOT NULL,
            Water       INT     NOT NULL,
            Chemical1   FLOAT     NOT NULL,
            Chemical2   FLOAT     NOT NULL            ); """
    db_cursor.execute(create_concrete_formula_table)
    # ====== create event_logg table ===============================================
    create_event_log_table = """ CREATE TABLE  IF NOT EXISTS event_log_table(
            log_time  TIMESTAMP,
            event     VARCHAR(256) NOT NULL           ); """
    db_cursor.execute(create_event_log_table)
    # ======= create booking table ==============================================
    create_booking_table = """ CREATE TABLE  IF NOT EXISTS booking_table(
            Booking_ID              INTEGER PRIMARY KEY AUTOINCREMENT,
            Record_Time             TIMESTAMP,
            Booking_Date_Time       TIMESTAMP,
            Customer_Name           VARCHAR(64)     NOT NULL,
            Address                 VARCHAR(128),
            Phone                   VARCHAR(10),
            Keep_Sample             BOOLEAN,
            Amount                  FLOAT     NOT NULL,
            Formula_ID              INT     NOT NULL,
            Booking_Status          INT     NOT NULL,
            Comment                 VARCHAR(256)            ); """
    db_cursor.execute(create_booking_table)
    print("setup complete")

except Error as e:
    print(e)
finally:
    db_connector.commit()
    if db_connector:
        db_connector.close()

