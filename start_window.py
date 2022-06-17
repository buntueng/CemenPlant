import tkinter as tk
from tkinter import messagebox
import os
import sqlite3
from share_library import center_screen

software_path = os.path.dirname(os.path.realpath(__file__))
main_window_path = software_path + '/main_window.py'
database_path = software_path +"/database/main_db.db"
run_home_window = 'python ' + software_path + '/home_window.py'


def check_user():
    user_name = username_entry.get()
    password = password_entry.get()

    db_connector = sqlite3.connect(database_path)
    db_cursor = db_connector.cursor()
    sql_query = 'SELECT * FROM user_table WHERE User_Name ="' + user_name + '" AND Password = "' + password +'"'
    db_cursor.execute(sql_query)
    rows = db_cursor.fetchall()
    if len(rows) == 1:
        main_window.destroy()
        os.system(run_home_window)
    else:
        messagebox.showerror(title="เกิดข้อผิดพลาด", message="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")


def press_enter(event):
    check_user()


# main program
main_window = tk.Tk()
main_window.wm_title("กรุณาใส่ชื่อและรหัสผ่านเพื่อเข้าใช้งาน")
main_window.geometry('510x160')

main_frame = tk.Frame(master=main_window)
username_label = tk.Label(master=main_frame,text="User")
password_label = tk.Label(master=main_frame,text="Password")
username_entry = tk.Entry(master=main_frame,width=30)
password_entry = tk.Entry(master=main_frame,width=30,show="*")
login_button = tk.Button(master=main_frame,text="Login",width=12,height=4,command=check_user)

main_frame.grid(row=0,column=0)
username_label.grid(row=0,column=0,padx=20,pady=(20,5),sticky=tk.W)
password_label.grid(row=1,column=0,padx=20,pady=5,sticky=tk.W)
username_entry.grid(row=0,column=1,pady=(20,5))
password_entry.grid(row=1,column=1)
login_button.grid(row=0,column=2,rowspan=2,padx=(20,10),pady=(20,10))

main_window.bind('<Return>', press_enter)
center_screen(main_window)
main_window.mainloop()


