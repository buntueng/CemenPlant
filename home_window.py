import os
import tkinter as tk
from tkinter import  font
from share_functions import center_screen

software_path = os.path.dirname(os.path.realpath(__file__))
controller_path = software_path + '\\controller_window.py'


# =========== main program =================
main_window = tk.Tk()
main_window.geometry('1024x768')
main_window.option_add('*Font', 'TH Niramit AS')
main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
main_window.title("คอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต")



top_frame = tk.Frame(master=main_window)
left_frame = tk.Frame(master=main_window)
center_frame = tk.Frame(master=main_window)
right_frame = tk.Frame(master=main_window)
bottom_frame = tk.Frame(master=main_window)

top_frame.grid(row=0,column=0,columnspan=3,sticky='w')
left_frame.grid(row=1,column=0,padx=10,pady=(10,0))
center_frame.grid(row=1,column=1,sticky='w')
right_frame.grid(row=1,column=2,padx=(50,0),sticky='w')
bottom_frame .grid(row=2,column=0,columnspan=3,sticky='w')

    # register_title_label = tk.Label(master=reg_top_frame,text='บันทึกรายการสั่งซื้อคอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต',font=main_font)
    # register_title_label.grid(row=0,column=0,padx=10,pady=(10,0),sticky='w')

    # customer_name_label = tk.Label(reg_left_frame,text='ชื่อลูกค้า',font=main_font)
    # customer_name_label.grid(row=0,column=0,sticky='e')
    # customer_name = tk.Entry(reg_left_frame,width=30,font=main_font)
    # customer_name.grid(row = 0,column=1,sticky='w',padx=10,pady=(0,10))

    # customer_phone_number_label = tk.Label(reg_left_frame,text='หมายเลขโทรศัพท์',font=main_font)
    # customer_phone_number_label.grid(row=1,column=0,sticky='e')
    # customer_phone_number = tk.Entry(reg_left_frame,width=30,font=main_font)
    # customer_phone_number.grid(row=1,column=1,sticky='w',padx=10,pady=10)

    # customer_address_label = tk.Label(master=reg_left_frame,text='ที่อยู่',font=main_font)
    # customer_address_label.grid(row=2,column=0,sticky='e',padx=10,pady=10)
    # customer_address = tk.Entry(master=reg_left_frame, width=30,font=main_font)
    # customer_address.grid(row=2,column=1,sticky='e',padx=10,pady=10)

    # customer_note_label = tk.Label(reg_left_frame,text='หมายเหตุ',font=main_font)
    # customer_note_label.grid(row=3,column=0,sticky='e',padx=10,pady=10)
    # customer_note = tk.Text(reg_left_frame,width=30,font=main_font,height=3)
    # customer_note.grid(row=3,column=1,pady=10,rowspan=3)

    # order_calendar_label = tk.Label(master=reg_center_frame,text='วันนัด',font=main_font)
    # order_calendar_label.grid(row=0,column=0,padx=(100,0),pady=(10,10),sticky='w')

    # present_datetime = datetime.datetime.now()
    # order_calendar = DateEntry(master=reg_center_frame, width=15, year=present_datetime.year, month=present_datetime.month, day=present_datetime.day,background='darkblue', foreground='white', borderwidth=2,font=main_font, justify='center',date_pattern='dd/MM/yyyy')
    # order_calendar.grid(row=0,column=1,columnspan=2,padx=10,pady=10)

    # order_time_label = tk.Label(master=reg_center_frame,text='เวลาจอง',font=main_font)
    # order_time_label.grid(row=1,column=0,sticky='e')
    # order_time_hour = tk.Spinbox(master=reg_center_frame,from_=8,to=18,width=5,font=main_font)
    # order_time_hour.grid(row=1,column=1,sticky='w',padx=10,pady=10)
    # order_time_hour.bind("<Key>", lambda e: "break")

    # order_time_minute = tk.Spinbox(master=reg_center_frame,from_=0,to=50,increment=10,width=5,font=main_font)
    # order_time_minute.grid(row=1,column=2,columnspan=2,sticky='w')
    # order_time_minute.bind("<Key>", lambda e: "break")

    # order_concrte_type_label = tk.Label(master=reg_center_frame,text='เลือกชนิดของปูน',font=main_font)
    # order_concrte_type_label.grid(row=2,column=0,sticky='e')
    # # read concrete fuomula here
    # mixed_formula = read_formula_name()
    # order_concrete_type = tk.Spinbox(master=reg_center_frame,width=25,font=main_font)
    # order_concrete_type.config(values=mixed_formula)
    # order_concrete_type.grid(row=2,column=1,columnspan=4,sticky='w',padx=10,pady=10)

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
