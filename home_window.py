import os
import tkinter as tk
from tkinter import  font
from pyparsing import col
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from share_library import center_screen, default_window_size
import panel as pn
import datetime

pn.extension()


software_path = os.path.dirname(os.path.realpath(__file__))
controller_path = software_path + '\\controller_window.py'


# =========== main program =================
main_window = tk.Tk()
main_window.geometry(default_window_size())
main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
main_window.title("คอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต")


top_frame = tk.Frame(master=main_window)
bottom_frame = tk.Frame(master=main_window)
upper_right_frame = tk.Frame(master=main_window)
lower_right_frame = tk.Frame(master=main_window)


top_frame.grid(row=0,column=0,sticky='w')
bottom_frame.grid(row=1,column=0,padx=10,pady=(10,0))
upper_right_frame.grid(row=0,column=1,sticky='w')
lower_right_frame.grid(row=1,column=1,padx=(50,0),sticky='w')

booking_label = tk.Label(master=top_frame,text='บันทึกรายการสั่งซื้อคอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต',font=main_font)
booking_label.grid(row=0,column=0,columnspan=5,padx=10,pady=(10,0),sticky='w')

customer_name_label = tk.Label(top_frame,text='ชื่อลูกค้า',font=main_font)
customer_name_label.grid(row=1,column=0,sticky='e')
customer_name_entry = tk.Entry(top_frame,width=30,font=main_font)
customer_name_entry.grid(row = 1,column=1,sticky='w',padx=10,pady=(0,10))

customer_phone_number_label = tk.Label(top_frame,text='เบอร์โทรศัพท์',font=main_font)
customer_phone_number_label.grid(row=2,column=0,sticky='e')
customer_phone_number_entry = tk.Entry(master = top_frame,width=30,font=main_font)
customer_phone_number_entry.grid(row=2,column=1,sticky='w',padx=10,pady=10)

customer_address_label = tk.Label(master=top_frame,text='ที่อยู่',font=main_font)
customer_address_label.grid(row=3,column=0,sticky='e',padx=10,pady=10)
customer_address_entry = tk.Entry(master=top_frame, width=30,font=main_font)
customer_address_entry.grid(row=3,column=1,sticky='w',padx=10,pady=10)

customer_note_label = tk.Label(top_frame,text='หมายเหตุ',font=main_font)
customer_note_label.grid(row=4,column=0,sticky='ne',padx=10,pady=10)
customer_note_text = tk.Text(top_frame,width=30,font=main_font,height=3)
customer_note_text.grid(row=4,column=1,padx=10,pady=10,sticky='w')

booking_calendar_label = tk.Label(master=top_frame,text='วันจอง',font=main_font)
booking_calendar_label.grid(row=1,column=2,padx=(100,0),pady=10,sticky='w')

booking_calendar = DateEntry(master=top_frame, width=15, background='darkblue', foreground='white', borderwidth=2,font=main_font, justify='center',date_pattern='dd/MM/yyyy')
booking_calendar.grid(row=1,column=3,columnspan=4,padx=10,pady=10)

booking_time_label = tk.Label(master=top_frame,text='เวลาจอง',font=main_font)
booking_time_label.grid(row=2,column=2,sticky='e')

booking_hour = tk.Entry(master=top_frame,width=2,font=main_font)
booking_hour.grid(row=2,column=4,sticky='w')
tk.Label(master=top_frame,text=":",font=main_font).grid(row=2,column=5)
booking_minute = tk.Entry(master=top_frame,width=2,font=main_font)
booking_minute.grid(row=2,column=6)

booking_concrte_type_label = tk.Label(master=top_frame,text='ชนิดของปูน',font=main_font)
booking_concrte_type_label.grid(row=3,column=2,sticky='e')
# ======= read concrete fuomula here =========
concrete_formula = []
booking_concrete_spinbox = tk.Spinbox(master=top_frame,width=15,font=main_font)
booking_concrete_spinbox.config(values=concrete_formula)
booking_concrete_spinbox.grid(row=3,column=3,columnspan=4,sticky='w',padx=10,pady=10)

    # order_quantity_label = tk.Label(master=reg_center_frame,text='จำนวน',font=main_font)
    # order_quantity_label.grid(row=3,column=0,sticky='e')   
    # order_quantity = tk.Entry(master=reg_center_frame,width=7,font=main_font)
    # order_quantity.bind('<Key>',check_order_quantity_data_type)
    # order_quantity.grid(row=3,column=1,padx=10,pady=10,sticky='w')

    # order_quantity_amount_label = tk.Label(master=reg_center_frame,text='คิวบิคเมตร',font=main_font)
    # order_quantity_amount_label.grid(row=3,column=2,columnspan=3,sticky='w')
        
    # mortar_status_label = tk.Label(master=reg_center_frame,text='เก็บลูกปูน',font=main_font)
    # mortar_status_label.grid(row=4,column=0,pady=10,sticky='e')
    # mortar_status_value = ['เก็บ','ไม่เก็บ']
    # mortar_status = tk.Spinbox(master=reg_center_frame,values=mortar_status_value,font=main_font,width=6)
    # mortar_status.grid(row=4,column=1,sticky='w',padx=10,pady=10)

    # save_order_button = tk.Button(master=reg_right_frame,text='บันทึกรายการสั่งซื้อ',font=main_font,width=25,height=3,command=save_order_in_reg_tab)
    # save_order_button.grid(row=0,column=0)

    # save_order_button = tk.Button(master=reg_right_frame,text='โหลดชื่อสูตรปูน',font=main_font,width=25,height=2,command=reload_formula)
    # save_order_button.grid(row=1,column=0,pady=20)
    
center_screen(main_window)
main_window.mainloop()
