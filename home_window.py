import os
import tkinter as tk
from tkinter import  font,ttk,messagebox
from tkcalendar import DateEntry
from share_library import center_screen, default_window_size,read_concrete_formula_from_db,record_booking_data,read_booking_queue,remove_booking_queue,process_booking_queue
import datetime

# ===========================================================================
software_path = os.path.dirname(os.path.realpath(__file__))
controller_path = software_path + '/controller_window.py'

run_formula_window = 'python ' + software_path + '/formula_window.py'
run_report_window = 'python ' + software_path + '/report_window.py'
run_controller_window = 'python '+ software_path + '/controller_window.py'

# ============ subprogram ===================================================
concrete_names = []
def open_report_window():
    main_window.destroy()
    os.system(run_report_window)

def open_formula_window():
    main_window.destroy()
    os.system(run_formula_window)

def open_controller_window():
    main_window.destroy()
    os.system(run_controller_window)

def open_formula_window():
    main_window.destroy()
    os.system(run_formula_window)

def process_queue():
    check_select_item = waiting_queue_report.focus()
    if len(check_select_item) > 0:
        booking_id = waiting_queue_report.item(check_select_item)['values'][0]
        process_booking_queue(booking_id)
        update_booking_queue_view
        main_window.after(1000,open_controller_window())
    else:
        messagebox.showinfo(title="เกิดข้อผิดพลาด",message="โปรดเลือกคิวที่ต้องการผลิต")
        
def remove_queue():
    check_select_item = waiting_queue_report.focus()
    if len(check_select_item) > 0:
        booking_id = waiting_queue_report.item(check_select_item)['values'][0]           # got int
        remove_booking_queue(booking_id)
        main_window.after(100,update_booking_queue_view)
    else:
        messagebox.showinfo(title="เกิดข้อผิดพลาด",message="โปรดเลือกคิวที่ต้องการยกเลิก")

def update_booking_queue_view():
    for item in waiting_queue_report.get_children():
        waiting_queue_report.delete(item)
    booking_list = read_booking_queue()
    for booking_info in booking_list:
        waiting_queue_report.insert("",'end',values=booking_info)
    
def record_booking():
    # when customer information was recorded, Booking_Status = 0.
    if customer_name_entry.get() != "" and booking_hour.get() != "" and booking_minute.get() != "" and order_quantity.get() != "":
        data_list = []
        current_date = booking_calendar.get_date()
        current_datetime = datetime.datetime.combine(current_date, datetime.time(int(booking_hour.get()), int(booking_minute.get())))
        data_list.append(current_datetime)
        data_list.append(customer_name_entry.get())                                                 # customer name
        data_list.append(customer_address_entry.get())                                              # customer Address
        data_list.append(customer_phone_number_entry.get())                                         # Phone
        if keep_sample_spinbox.get() == 'เก็บ':                                                      # keep sample - {0 - not keep, 1 - keep}
            data_list.append('1')
        else:
            data_list.append('0')
        data_list.append(order_quantity.get())                                                      # Amount
        data_list.append(concrete_names.index(booking_concrete_spinbox.get())+1)                    # formula ID
        data_list.append(customer_note_entry.get())                                                 # commment
        data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7]
        record_booking_data(data_list)
        clear_all_input()
        main_window.after(100,update_booking_queue_view())
    else:
        message = 'โปรดตรวจสอบข้อมูลดังนี้\n'
        if customer_name_entry.get() == "":
            message = message + "* ชื่อลูกค้า\n"
        if booking_hour.get() == "" or booking_minute.get() == "":
            message = message + "* เวลาจอง\n"
        if order_quantity.get() == "":
            message = message + "* ปริมาณปูนที่ต้องการจอง"
        messagebox.showinfo('เกิดข้อผิดพลาด', message)

def clear_all_input():
    customer_name_entry.delete(0, 'end')
    customer_address_entry.delete(0, 'end')
    customer_phone_number_entry.delete(0, 'end')
    customer_note_entry.delete(0, 'end')
    booking_hour.delete(0, 'end')
    booking_hour.insert(0,"08")
    booking_minute.delete(0, 'end')
    booking_minute.insert(0,"00")
    order_quantity.delete(0, 'end')

def delete_last_quantity():
    if len(order_quantity.get()) > 0:
            order_quantity.delete(len(order_quantity.get())-1, tk.END)

def check_order_quantity_input(ev):
    key_val = ev.char
    if not (key_val <= '9' and key_val >= '0' or key_val == '.'):
        main_window.after(10,delete_last_quantity)


def delete_last_hour():
    if len(booking_hour.get()) > 0:
        booking_hour.delete(len(booking_hour.get())-1, tk.END)

def check_hour_input(ev):
    key_val = ev.char
    if not (key_val <= '9' and key_val >= '0'):
        main_window.after(10,delete_last_hour)

def delete_last_minute():
    if len(booking_minute.get()) > 0:
        booking_minute.delete(len(booking_minute.get())-1, tk.END)

def check_minute_input(ev):
    key_val = ev.char
    if not (key_val <= '9' and key_val >= '0'):
        main_window.after(10,delete_last_minute)
    
# =========== main program =================
main_window = tk.Tk()
main_window.geometry(default_window_size())
main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
main_window.title("คอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต")

top_frame = tk.Frame(master=main_window,highlightbackground="snow4", highlightthickness=2)
middle_frame = tk.Frame(master=main_window)
bottom_frame = tk.Frame(master=main_window,highlightbackground="snow4", highlightthickness=2)

top_frame.grid(row=0,column=0,sticky='w',padx=10)
middle_frame.grid(row=1,column=0,padx=10,pady=(10,0))
bottom_frame.grid(row=2,column=0,padx=10,pady=(10,0))

booking_label = tk.Label(master=top_frame,text='บันทึกรายการสั่งจอง',font=main_font)
booking_label.grid(row=0,column=0,columnspan=5,padx=10,pady=(10,0),sticky='w')

customer_name_label = tk.Label(top_frame,text='ชื่อลูกค้า',font=main_font)
customer_name_label.grid(row=1,column=0,sticky='e')
customer_name_entry = tk.Entry(top_frame,width=30,font=main_font)
customer_name_entry.grid(row = 1,column=1,sticky='w',padx=10,pady=(0,10))

customer_phone_number_label = tk.Label(top_frame,text='เบอร์โทร',font=main_font)
customer_phone_number_label.grid(row=2,column=0,sticky='e')
customer_phone_number_entry = tk.Entry(master = top_frame,width=30,font=main_font)
customer_phone_number_entry.grid(row=2,column=1,sticky='w',padx=10,pady=10)

customer_address_label = tk.Label(master=top_frame,text='ที่อยู่',font=main_font)
customer_address_label.grid(row=3,column=0,sticky='e',padx=10,pady=10)
customer_address_entry = tk.Entry(master=top_frame, width=30,font=main_font)
customer_address_entry.grid(row=3,column=1,sticky='w',padx=10,pady=10)

customer_note_label = tk.Label(top_frame,text='หมายเหตุ',font=main_font)
customer_note_label.grid(row=4,column=0,sticky='e',padx=10,pady=10)
customer_note_entry = tk.Entry(top_frame,width=68,font=main_font)
customer_note_entry.grid(row=4,column=1,padx=10,pady=10,sticky='w',columnspan=4)

booking_calendar_label = tk.Label(master=top_frame,text='วันจอง',font=main_font)
booking_calendar_label.grid(row=1,column=2,padx=(100,0),pady=10,sticky='w')

booking_calendar = DateEntry(master=top_frame, width=15, background='darkblue', foreground='white', borderwidth=2,font=main_font, justify='center',date_pattern='dd/MM/yyyy')
booking_calendar.grid(row=1,column=3,padx=10,pady=10)

booking_time_label = tk.Label(master=top_frame,text='เวลาจอง',font=main_font)
booking_time_label.grid(row=1,column=4,sticky='e',padx=(20,0))

booking_hour = tk.Entry(master=top_frame,width=6,font=main_font,justify='center')
booking_hour.insert(0,'08')
booking_hour.bind('<Key>',check_hour_input)
booking_hour.grid(row=1,column=5,sticky='w',padx=(20,0))
tk.Label(master=top_frame,text=":",font=main_font,width=2,justify='center').grid(row=1,column=6,sticky='w')
booking_minute = tk.Entry(master=top_frame,width=6,font=main_font,justify='center')
booking_minute.insert(0,'00')
booking_minute.bind('<Key>',check_minute_input)
booking_minute.grid(row=1,column=7,sticky='w')

booking_concrte_type_label = tk.Label(master=top_frame,text='ชนิดของปูน',font=main_font)
booking_concrte_type_label.grid(row=2,column=2,sticky='e')
# ======= read concrete fuomula here =========
concrete_type = tk.StringVar()
concrete_formula_list = read_concrete_formula_from_db()
concrete_names = []
for name in concrete_formula_list:
    concrete_names.append(name[1])
booking_concrete_spinbox = tk.Spinbox(master=top_frame,width=15,font=main_font,textvariable=concrete_type)
booking_concrete_spinbox.config(values=concrete_names)
booking_concrete_spinbox.grid(row=2,column=3,columnspan=4,sticky='w',padx=10,pady=10)

tk.Label(master=top_frame,text='จำนวน',font=main_font).grid(row=2,column=4,sticky='e')
order_quantity = tk.Entry(master=top_frame,width=5,font=main_font,justify='center')
order_quantity.grid(row=2,column=5,sticky='e',padx=10)
order_quantity.bind('<Key>',check_order_quantity_input)
tk.Label(master=top_frame,text="คิวบิค",font=main_font).grid(row=2,column=6,columnspan=2)

tk.Label(master=top_frame,text='เก็บลูกปูน',font=main_font).grid(row=3,column=2,sticky='e')
keep_sample_spinbox = tk.Spinbox(master=top_frame,font=main_font,width=6,justify='center')
keep_sample_spinbox.config(values=['ไม่เก็บ','เก็บ'])
keep_sample_spinbox.grid(row=3,column=3,sticky='w',padx=10)

save_order_button = tk.Button(master=top_frame,text='บันทึกข้อมูล',font=main_font,width=20,height=2,command=record_booking)
save_order_button.grid(row=3,column=4,rowspan=2,columnspan=3,padx=(20,10))

clear_order_button = tk.Button(master=top_frame,text='ล้างข้อมูล',font=main_font,width=20,height=2,command=clear_all_input)
clear_order_button.grid(row=3,column=7,rowspan=2,padx=(10,10))


tk.Label(master=bottom_frame,text='รายการสั่งจองในคิว',font=main_font).grid(row=0,column=0,sticky='w',padx=10,pady=(20,10))
waiting_queue_report = ttk.Treeview(master=bottom_frame,columns=('order_number','queue_datetime','customer_name','customer_mobile_phone_no','order_quantity'),padding=[0,0,0,0],selectmode="extended",height=18)
waiting_queue_report.grid(row=1,column=0,padx=(10,20),rowspan=5,pady=(0,10))
waiting_queue_report['show'] = 'headings'
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 10))
waiting_queue_report.heading("order_number", text="ลำดับที่")
waiting_queue_report.column("order_number", minwidth=0, width=50, stretch=tk.NO,anchor=tk.CENTER)
waiting_queue_report.heading("queue_datetime", text="วันเวลาที่จอง")
waiting_queue_report.column("queue_datetime", minwidth=0, width=180, stretch=tk.NO,anchor=tk.CENTER) 
waiting_queue_report.heading("customer_name", text="ชื่อลูกค้า")
waiting_queue_report.column("customer_name", minwidth=0, width=250, stretch=tk.NO,anchor=tk.CENTER)
waiting_queue_report.heading("customer_mobile_phone_no", text="เบอร์โทรศัพท์")
waiting_queue_report.column("customer_mobile_phone_no", minwidth=0, width=180, stretch=tk.NO,anchor=tk.CENTER)
waiting_queue_report.heading("order_quantity", text="ปริมาณ (คิวบิคเมตร)")
waiting_queue_report.column("order_quantity", minwidth=0, width=120, stretch=tk.NO,anchor=tk.CENTER)

remove_queue_button = tk.Button(master=bottom_frame,text='ยกเลิกคิวจอง',width=23,height=2,font=main_font,command=remove_queue)
remove_queue_button.grid(row=1,column=1,padx=10,sticky='n',pady=5)
process_queue_button = tk.Button(master=bottom_frame,text='เลือกคิวทำงาน',width=23,height=2,font=main_font,command=process_queue)
process_queue_button.grid(row=2,column=1,padx=10,sticky='n')
update_formula_button = tk.Button(master=bottom_frame,text='ปรับสูตรปูน',width=23,height=2,font=main_font,command=open_formula_window)
update_formula_button.grid(row=3,column=1,padx=10,sticky='n')
open_report_button = tk.Button(master=bottom_frame,text='แสดงรายงาน',width=23,height=2,font=main_font,command=open_report_window)
open_report_button.grid(row=4,column=1,padx=10,sticky='n')

update_booking_queue_view()

center_screen(main_window)
main_window.mainloop()
