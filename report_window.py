import os
import tkinter as tk
from tkinter import  font,ttk,messagebox
from tkcalendar import DateEntry
from share_library import center_screen, default_window_size,read_concrete_formula_from_db,record_booking_data,read_booking_queue,remove_booking_queue,process_booking_queue
import datetime

main_window = tk.Tk()
main_window.geometry(default_window_size())
main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
main_window.title("คอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต")
center_screen(main_window)
main_window.mainloop()