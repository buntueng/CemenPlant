import os
import tkinter as tk
from tkinter import  DISABLED, StringVar, font
from share_library import center_screen, default_window_size,read_concrete_formula_from_db,record_booking_data,read_booking_queue,remove_booking_queue,process_booking_queue
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

software_path = os.path.dirname(os.path.realpath(__file__))
run_home_window = 'python ' + software_path + '/home_window.py'


# ==== global variable =======
main_state = 0
in_loop = True
# comport = '/dev/ttyS0'
comport = 'COM3'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
# ============== processing state =================================
def main_controller():
    global main_state
    global in_loop
    try:
        # initialize PLC1
        if main_state == 0:                                                 # reset most coils except mixer (M6) 
            add_status("main state = 0")                                    # this coil will reset itself in 0.1 seconds
            modbus_result = client.write_coil(address=6,value=1,unit=0x01)
            if modbus_result.function_code < 0x80:
                main_state = 1        
            if in_loop:
                main_window.after(1000,main_controller)

        elif main_state == 1:                                               # stop mixer
            add_status("main state = 1")
            modbus_result = client.write_coil(address=10,value=0,unit=0x01)
            if modbus_result.function_code < 0x80:
                main_state = 2
            if in_loop:
                main_window.after(1000,main_controller)

        # initial PLC2
        elif main_state == 2:                                               # reset all coils in PLC2
            add_status("main state = 2")
            modbus_result = client.write_coil(address=15,value=1,unit=0x02)
            if modbus_result.function_code < 0x80:
                main_state = 3

        # set agg weights to PLC1
        elif main_state == 3:
            add_status("main state = 3")
            if in_loop:
                main_window.after(1000,main_controller)


        # this state run after the stop button pressed
        # clear all coils in PLC1 and PLC2 after that exit loop
        elif main_state == 1000:    
            main_state = 1001
            main_window.after(500,main_controller)
        elif main_state == 1001:
            main_state = 1002
            main_window.after(500,main_controller)
        elif main_state == 1002:
            main_state = 1003
            main_window.after(500,main_controller)
        elif main_state == 1003:
            main_state = 1004
            main_window.after(500,main_controller)
        elif main_state == 1004:
            pass
    except Exception:
        message = "มีข้อผิดพลาด state = " + str(main_state)
        add_status(message)
        main_window.after(500,main_controller)
# =================================================================
def clear_total_weight_display():
    mixed_finished_string.set('0')
    total_rock1_weight_string.set('0')
    total_sand_weight_string.set('0')
    total_rock2_weight_string.set('0')
    total_water_weight_string.set('0')
    total_chem1_weight_string.set('0')
    total_chem2_weight_string.set('0')
    total_flyash_weight_string.set('0')
    total_cemen_weight_string.set('0')

def clear_previous_weight_display():
    rock1_weight_string.set('0')
    sand_weight_string.set('0')
    rock2_weight_string.set('0')
    agg_total_weight_string.set('0')       # sum of (sand + rcok1 + rock2)
    cemen_weight_string.set('0')
    flyash_weight_string.set('0')
    water_weight_string.set('0')
    chem1_weight_string.set('0')
    chem2_weight_string.set('0')

# =================================================================
def start_process_button_pressed():
    global in_loop
    global main_state

    in_loop = True
    main_state = 0
    main_window.after(100,main_controller)
    start_process_button.config(state=tk.DISABLED)
    stop_process_button.config(state=tk.NORMAL)
    go_home_button.config(state=tk.DISABLED)

    clear_total_weight_display()
    clear_previous_weight_display()
    add_status("เริ่มผสมคอนกรีต")

# =================================================================
def stop_process_button_pressed():
    global in_loop
    global main_state
    add_status("หยุดการผสมคอนกรีต")
    main_state = 1000
    in_loop = False
    start_process_button.config(state=tk.NORMAL)
    stop_process_button.config(state=tk.DISABLED)
    go_home_button.config(state=tk.NORMAL)
# ============= sub functions =====================================
def go_home():
    main_window.destroy()
    os.system(run_home_window)

def clear_status():
    status_text.config(state=tk.NORMAL)
    status_text.delete("1.0",tk.END)
    status_text.config(state=tk.DISABLED)
    
def add_status(message):
    message = message + "\n"
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END,message)
    status_text.config(state=tk.DISABLED)
    message = ""

# ==================== set color to items ===================================
def reset_items_color():
    rock1_display_label.configure(bg="#FFFFFF")
    sand_display_label.configure(bg="#FFFFFF")
    rock2_display_label.configure(bg="#FFFFFF")
    conveyor_label.configure(bg="#FFFFFF")
    cemen_display_label.configure(bg="#FFFFFF")
    flyash_display_label.configure(bg="#FFFFFF")
    water_display_label.configure(bg="#FFFFFF")
    chem1_display_label.configure(bg="#FFFFFF")
    chem2_display_label.configure(bg="#FFFFFF")
    mixer_display_label.configure(bg="#FFFFFF")
    mixer_valve_display_label.configure(bg="#FFFFFF")

def rock1_active():
    rock1_display_label.configure(bg="green")
def sand_active():
    sand_display_label.configure(bg="green")
def rock2_active():
    rock2_display_label.configure(bg="green")
def conveyor_active():
    conveyor_label.configure(bg="green")
def mixer_active():
    mixer_display_label.configure(bg="green")
def mixer_valve_active():
    mixer_valve_display_label.configure(bg="green")
def water_active():
    water_display_label.configure(bg="green")
def flyash_active():
    flyash_display_label.configure(bg="green")
def cemen_active():
    cemen_display_label.configure(bg="green")
def chem1_active():
    chem1_display_label.configure(bg="green")
def chem2_active():
    chem2_display_label.configure(bg="green")
# =================================================================
main_window = tk.Tk()
main_window.geometry(default_window_size())
main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
main_window.title("คอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต")

main_frame = tk.Frame(master = main_window)
top_left_frame = tk.Frame(master = main_frame)
left_frame = tk.Frame(master = main_frame)
right_frame = tk.Frame(master = main_frame)
bottom_frame = tk.Frame(master = main_frame)

main_frame.grid(row=0,column=0)
top_left_frame.grid(row=0,column=0,padx=(10,10),pady=5,sticky='nw')
left_frame.grid(row=1,column=0,padx=(10,10),pady=(5,30))
right_frame.grid(row=0,column=1,padx =(30,0),pady=10,sticky='nw',rowspan=2)
bottom_frame.grid(row=2,column=0,columnspan=2,padx=10,pady=(20,10),sticky='w')
center_screen(main_window)
# ========== top left frame UI ============
customer_name_string = StringVar()
customer_number_string = StringVar()
formula_name_string = StringVar()

customer_name_label = tk.Label(master=top_left_frame,text='ชื่อลูกค้า',font=main_font)
customer_name_entry = tk.Entry(master=top_left_frame,width=35,font=main_font,state=DISABLED,textvariable=customer_name_string)
telephone_number_label = tk.Label(master=top_left_frame,text="เบอร์โทร",font=main_font)
telephone_number_entry = tk.Entry(master=top_left_frame,width=35,font=main_font,state=DISABLED,textvariable=customer_number_string)
formula_name_label = tk.Label(master=top_left_frame,text='สูตรปูน',font=main_font)
formula_name_entry = tk.Entry(master=top_left_frame,width=35,font=main_font,state=DISABLED,textvariable=formula_name_string)

concrete_amount_label = tk.Label(master=top_left_frame,text="จำนวน",font=main_font)
concrete_amount_entry = tk.Entry(master=top_left_frame,state=DISABLED,font=main_font,width=15)
concrete_unit_label = tk.Label(master=top_left_frame,text="คิวบิค",font=main_font)

customer_name_label.grid(row=0,column=0,padx=10)
customer_name_entry.grid(row=0,column=1,sticky=tk.W,pady=10)

telephone_number_label.grid(row=0,column=2,padx=10)
telephone_number_entry.grid(row=0,column=3,columnspan=3)


formula_name_label.grid(row=1,column=0)
formula_name_entry.grid(row=1,column=1,sticky=tk.W)

concrete_amount_label.grid(row=1,column=2)
concrete_amount_entry.grid(row=1,column=3,sticky=tk.W)
concrete_unit_label.grid(row=1,column=4,sticky=tk.W)

# ========== left frame UI ================
rock1_weight_string = StringVar()
sand_weight_string = StringVar()
rock2_weight_string = StringVar()
agg_total_weight_string = StringVar()       # sum of (sand + rcok1 + rock2)
cemen_weight_string = StringVar()
flyash_weight_string = StringVar()
water_weight_string = StringVar()
chem1_weight_string = StringVar()
chem2_weight_string = StringVar()


rock1_weight_entry = tk.Entry(master=left_frame,width=7,state=tk.DISABLED,justify=tk.CENTER,textvariable=rock1_weight_string)
rock1_display_label = tk.Label(master=left_frame,text="หิน1",width=6,height=2,borderwidth=2, relief="solid",font=main_font)
sand_weight_entry = tk.Entry(master=left_frame,width=7,state=tk.DISABLED,justify=tk.CENTER,textvariable=sand_weight_string)
sand_display_label = tk.Label(master=left_frame,text="ทราย",width=6,height=2,borderwidth=2, relief="solid",font=main_font)
rock2_weight_entry = tk.Entry(master=left_frame,width=7,state=tk.DISABLED,justify=tk.CENTER,textvariable=rock2_weight_string)
rock2_display_label = tk.Label(master=left_frame,text="หิน2",width=6,height=2,borderwidth=2, relief="solid",font=main_font)
conveyor_label = tk.Label(master=left_frame,text="สายพานลำเลียง",width=32,height=1,borderwidth=2, relief="solid")
empty_label = tk.Label(master=left_frame,text="",width=9)

agg_total_weight_label = tk.Label(master=left_frame,text="น้ำหนักรวม",width=10,height=2)
agg_total_weight_entry = tk.Entry(master=left_frame,width=7,state=tk.DISABLED,justify=tk.CENTER,textvariable=agg_total_weight_string)

cemen_weight_entry = tk.Entry(master=left_frame,width=9,state=tk.DISABLED,justify=tk.CENTER,textvariable=cemen_weight_string)
cemen_display_label = tk.Label(master=left_frame,text="ซีเมนต์",width=7,height=2,borderwidth=2, relief="solid",font=main_font)
flyash_weight_entry = tk.Entry(master=left_frame,width=9,state=tk.DISABLED,justify=tk.CENTER,textvariable=flyash_weight_string)
flyash_display_label = tk.Label(master=left_frame,text="เถ้าลอย",width=7,height=2,borderwidth=2, relief="solid",font=main_font)
water_weight_entry = tk.Entry(master=left_frame,width=9,state=tk.DISABLED,justify=tk.CENTER,textvariable=water_weight_string)
water_display_label = tk.Label(master=left_frame,text="น้ำ",width=7,height=2,borderwidth=2, relief="solid",font=main_font)
chem1_weight_entry = tk.Entry(master=left_frame,width=9,state=tk.DISABLED,justify=tk.CENTER,textvariable=chem1_weight_string)
chem1_display_label = tk.Label(master=left_frame,text="น้ำยา1",width=7,height=2,borderwidth=2, relief="solid",font=main_font)
chem2_weight_entry = tk.Entry(master=left_frame,width=9,state=tk.DISABLED,justify=tk.CENTER,textvariable=chem2_weight_string)
chem2_display_label = tk.Label(master=left_frame,text="น้ำยา2",width=7,height=2,borderwidth=2, relief="solid",font=main_font)

mixer_display_label = tk.Label(master=left_frame,text="เครื่องผสมคอนกรีต",width=48,height=3,borderwidth=2, relief="solid",font=main_font)
mixer_valve_display_label = tk.Label(master=left_frame,text="วาล์วปล่อยปูน",width=30,height=1,borderwidth=2, relief="solid")

rock1_weight_entry.grid(row=0,column=0,pady=5,padx=5)
rock1_display_label.grid(row=1,column=0)
sand_weight_entry.grid(row=0,column=1,pady=5)
sand_display_label.grid(row=1,column=1)
rock2_weight_entry.grid(row=0,column=2,pady=5)
rock2_display_label.grid(row=1,column=2,padx=5)
empty_label.grid(row=0,column=3)

conveyor_label.grid(row=2,column=0,columnspan=4,sticky=tk.E,pady=10,padx=(5,15))

agg_total_weight_label.grid(row=4,column=0,columnspan=2,sticky=tk.E,padx=10)
agg_total_weight_entry.grid(row=4,column=2)

cemen_weight_entry.grid(row=0,column=4,padx=5)
cemen_display_label.grid(row=1,column=4)
flyash_weight_entry.grid(row=0,column=5,padx=5)
flyash_display_label.grid(row=1,column=5)
water_weight_entry.grid(row=0,column=6,padx=5)
water_display_label.grid(row=1,column=6)
chem1_weight_entry.grid(row=0,column=7,padx=5)
chem1_display_label.grid(row=1,column=7)
chem2_weight_entry.grid(row=0,column=8,padx=5)
chem2_display_label.grid(row=1,column=8)

mixer_display_label.grid(row=2,column=4,padx=5,columnspan=5,rowspan=4,pady =10)
mixer_valve_display_label.grid(row=6,column=5,columnspan=3)
reset_items_color()

# ========== right frame UI ================
amount_string = StringVar()
mixed_finished_string = StringVar()
rock1_target_weight_string = StringVar()
total_rock1_weight_string = StringVar()
sand_target_weight_string = StringVar()
total_sand_weight_string = StringVar()
rock2_target_weight_string = StringVar()
total_rock2_weight_string = StringVar()
water_target_weight_string = StringVar()
total_water_weight_string = StringVar()
chem1_target_weight_string = StringVar()
total_chem1_weight_string = StringVar()
chem2_target_weight_string = StringVar()
total_chem2_weight_string = StringVar()
flyash_target_weight_string = StringVar()
total_flyash_weight_string = StringVar()
cemen_target_weight_string = StringVar()
total_cemen_weight_string = StringVar()

record_label = tk.Label(master=right_frame,text="บันทึกน้ำหนักส่วนผสม",font=main_font)
amount_label = tk.Label(master=right_frame,text='รอผสม',font=main_font)
amount_entry = tk.Entry(master=right_frame,width=7,font=main_font,justify=tk.CENTER,state=DISABLED,textvariable=amount_string)
mixed_finish_label = tk.Label(master=right_frame,text='ผสมแล้ว',font=main_font)
mixed_finish_entry = tk.Entry(master=right_frame,width=7,font=main_font,justify=tk.CENTER,state=DISABLED,textvariable=mixed_finished_string)
cubic_label1 = tk.Label(master=right_frame,text='คิวบิค',font=main_font,justify=tk.LEFT)
cubic_label2 = tk.Label(master=right_frame,text='คิวบิค',font=main_font,justify=tk.LEFT)

target_weight_label = tk.Label(master=right_frame,text='เตรียมโหลด',font=main_font,justify=tk.CENTER)
total_weight_label = tk.Label(master=right_frame,text='น้ำหนักรวม',font=main_font,justify=tk.CENTER)


rock1_label = tk.Label(master=right_frame,text='หินเบอร์ 1',font=main_font)
target_rock1_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,textvariable=rock1_target_weight_string,state=DISABLED)
total_rock1_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,textvariable=total_rock1_weight_string,state=DISABLED)

sand_label = tk.Label(master=right_frame,text='ทราย',font=main_font)
target_sand_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=sand_target_weight_string)
total_sand_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_sand_weight_string)

rock2_label = tk.Label(master=right_frame,text='หินเบอร์ 2',font=main_font)
target_rock2_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=rock2_target_weight_string)
total_rock2_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_rock2_weight_string)

water_label = tk.Label(master=right_frame,text='น้ำ',font=main_font)
target_water_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=water_target_weight_string)
total_water_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_water_weight_string)

chem1_label = tk.Label(master=right_frame,text='น้ำยา 1',font=main_font)
target_chem1_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=chem1_target_weight_string)
total_chem1_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_chem1_weight_string)

chem2_label = tk.Label(master=right_frame,text='น้ำยา 2',font=main_font)
target_chem2_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=chem2_target_weight_string)
total_chem2_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_chem2_weight_string)

flyash_label = tk.Label(master=right_frame,text='เถ้าลอย',font=main_font)
target_flyash_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=flyash_target_weight_string)
total_flyash_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_flyash_weight_string)

cemen_label = tk.Label(master=right_frame,text='ซีเมนต์',font=main_font)
target_cemen_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=cemen_target_weight_string)
total_cemen_entry = tk.Entry(master=right_frame,width=7,justify=tk.RIGHT,font=main_font,state=DISABLED,textvariable=total_cemen_weight_string)

start_process_button = tk.Button(master=right_frame,text="เริ่มทำงาน",font=main_font,width=25,height=1,command=start_process_button_pressed)
stop_process_button = tk.Button(master=right_frame,text="หยุด",font=main_font,width=25,height=1,command=stop_process_button_pressed)
stop_process_button.config(state=tk.DISABLED)


record_label.grid(row=0,column=0,columnspan=3,pady=5)
amount_label.grid(row=2,column=0,pady = (15,5),padx=5,sticky='e')
amount_entry.grid(row=2,column=1)
mixed_finish_label.grid(row=3,column=0)
mixed_finish_entry.grid(row=3,column=1)

cubic_label1.grid(row=2,column=2,sticky='w')
cubic_label2.grid(row=3,column=2,sticky='w')

target_weight_label.grid(row=4,column=1,pady=(15,5))
total_weight_label.grid(row=4,column=2,pady=(15,5))

rock1_label.grid(row=5,column=0,sticky='e')
target_rock1_entry.grid(row=5,column=1)
total_rock1_entry.grid(row=5,column=2)

sand_label.grid(row=6,column=0,sticky='e')
target_sand_entry.grid(row=6,column=1)
total_sand_entry.grid(row=6,column=2)

rock2_label.grid(row=7,column=0,sticky='e')
target_rock2_entry.grid(row=7,column=1)
total_rock2_entry.grid(row=7,column=2)

water_label.grid(row=8,column=0,sticky='e')
target_water_entry.grid(row=8,column=1)
total_water_entry.grid(row=8,column=2)

chem1_label.grid(row=9,column=0,sticky='e')
target_chem1_entry.grid(row=9,column=1)
total_chem1_entry.grid(row=9,column=2)

chem2_label.grid(row=10,column=0,sticky='e')
target_chem2_entry.grid(row=10,column=1)
total_chem2_entry.grid(row=10,column=2)

flyash_label.grid(row=11,column=0,sticky='e')
target_flyash_entry.grid(row=11,column=1)
total_flyash_entry.grid(row=11,column=2)

cemen_label.grid(row=12,column=0,sticky='e')
target_cemen_entry.grid(row=12,column=1)
total_cemen_entry.grid(row=12,column=2)

start_process_button.grid(row=13,column=0,columnspan=3,pady=(15,10),sticky=tk.E)
stop_process_button.grid(row=14,column=0,columnspan=3,sticky=tk.E)

# ======= bottom frame UI ================
status_string = StringVar()
status_label = tk.Label(master=bottom_frame,text="สถานะการทำงานของระบบ",font=main_font)
status_text = tk.Text(master = bottom_frame,width=100,height=4,font=main_font,state=DISABLED)
clear_status_button = tk.Button(master=bottom_frame,text="ล้างข้อความ",width=23,height=1,font=main_font,command=clear_status)
go_home_button = tk.Button(master=bottom_frame,text="กลับหน้าหลัก",width=23,height=1,font=main_font,command=go_home)

status_label.grid(row=0,column=0,sticky='w')
status_text.grid(row=1,column=0,rowspan=2)
clear_status_button.grid(row=1,column=1,padx=(20,0))
go_home_button.grid(row=2,column=1,padx=(20,0))

main_window.mainloop()