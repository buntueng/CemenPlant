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


main_frame = tk.Frame(main_window)
top_frame = tk.Frame(main_frame)
left_frame = tk.Frame(main_frame)
right_frame = tk.Frame(main_frame)
bottom_frame = tk.Frame(main_frame)

top_frame.grid(row=0,column=0,columnspan=2,padx=50,sticky='w')
left_frame.grid(row=1,column=0,padx=(10,10),pady=5)
right_frame.grid(row=1,column=1,padx =(30,0),pady=10,sticky='ne')
bottom_frame.grid(row=2,column=0,columnspan=2,padx=(0,0),sticky='w')
center_screen(main_window)
main_window.mainloop()