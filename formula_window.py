import os
from re import M
import tkinter as tk
from tkinter import  font

from share_library import center_screen, default_window_size,read_concrete_formula_from_db,update_concrete_formula,clear_all_formula

software_path = os.path.dirname(os.path.realpath(__file__))
controller_path = software_path + '/controller_window.py'
run_home_window = 'python ' + software_path + '/home_window.py'

def open_home_window():
    main_window.destroy()
    os.system(run_home_window)

def update_formula_to_db():
    entry_values = [widget.get() for widget in widget_list]        # get list of string value of entry widget
    copy_list = entry_values.copy()
    for index in [90,81,72,63,54,45,36,27,18,9,0]:
        copy_list.pop(index)
  
    float_checker = True
    for index in [87,86,79,78,71,70,63,62,55,54,47,46,39,38,31,30,23,22,15,14,7,6] :
        if float(copy_list[index]):
            copy_list.pop(index)
        else:
            float_checker = False

    digit_checker = True
    for entry_value in copy_list:
        if not entry_value.isdigit():
            digit_checker = False
    if(float_checker== True and digit_checker==True):
        clear_all_formula()
        update_concrete_formula(1,entry_values[0],entry_values[1],entry_values[2],entry_values[3],entry_values[4],entry_values[5],entry_values[6],entry_values[7],entry_values[8])
        update_concrete_formula(2,entry_values[9],entry_values[10],entry_values[11],entry_values[12],entry_values[13],entry_values[14],entry_values[15],entry_values[16],entry_values[17])
        update_concrete_formula(3,entry_values[18],entry_values[19],entry_values[20],entry_values[21],entry_values[22],entry_values[23],entry_values[24],entry_values[25],entry_values[26])
        update_concrete_formula(4,entry_values[27],entry_values[28],entry_values[29],entry_values[30],entry_values[31],entry_values[32],entry_values[33],entry_values[34],entry_values[35])
        update_concrete_formula(5,entry_values[36],entry_values[37],entry_values[38],entry_values[39],entry_values[40],entry_values[41],entry_values[42],entry_values[43],entry_values[44])
        update_concrete_formula(6,entry_values[45],entry_values[46],entry_values[47],entry_values[48],entry_values[49],entry_values[50],entry_values[51],entry_values[52],entry_values[53])
        update_concrete_formula(7,entry_values[54],entry_values[55],entry_values[56],entry_values[57],entry_values[58],entry_values[59],entry_values[60],entry_values[61],entry_values[62])
        update_concrete_formula(8,entry_values[63],entry_values[64],entry_values[65],entry_values[66],entry_values[67],entry_values[68],entry_values[69],entry_values[70],entry_values[71])
        update_concrete_formula(9,entry_values[72],entry_values[73],entry_values[74],entry_values[75],entry_values[76],entry_values[77],entry_values[78],entry_values[79],entry_values[80])
        update_concrete_formula(10,entry_values[81],entry_values[82],entry_values[83],entry_values[84],entry_values[85],entry_values[86],entry_values[87],entry_values[88],entry_values[89])
        update_concrete_formula(11,entry_values[90],entry_values[91],entry_values[92],entry_values[93],entry_values[94],entry_values[95],entry_values[96],entry_values[97],entry_values[98])
        status_text.insert(tk.END,"อัพเดตสูตรคอนกรีตแล้ว กำลังกลับโปรแกรมหลัก\n")
        status_text.see("end")
        main_window.after(2000,open_home_window)
    else:
        status_text.insert(tk.END,"โปรดเช็คค่าที่กำหนดว่าถูกต้องหรือไม่\n")
        status_text.see("end")

# =========== main program =================
main_window = tk.Tk()
main_window.geometry(default_window_size())
center_screen(main_window)
main_font = font.Font(family='TH Niramit AS',size=16,weight="bold")
main_window.title("กำหนดค่าสูตรผสมคอนกรีต")

top_frame = tk.Frame(master=main_window)
bottom_frame = tk.Frame(master=main_window)
top_frame.grid(row=0,column=0,padx=10,pady=5)
bottom_frame.grid(row=1,column=0,padx=10,pady=5)

header_setup_list = ['ลำดับ','ชื่อสูตร','หินเบอร์ 1','ทราย','หินเบอร์ 2','ซีเมนต์','เถ้าลอย','น้ำ','น้ำยาเคมี 1','น้ำยาเคมี 2']
for h_index in range(0,len(header_setup_list)):
    tk.Label(top_frame,text=header_setup_list[h_index],font=main_font).grid(row=1,column=h_index,padx=5,pady=5)


concrete_formula_list = read_concrete_formula_from_db()
number_of_formula = len(concrete_formula_list)
number_of_substrate = len(concrete_formula_list[0])
widget_list =[]
for index,current_formula in enumerate(concrete_formula_list):
    tk.Label(master=top_frame,text=str(current_formula[0]),font=main_font).grid(row=index+2,column=0,padx=10,pady=10)
    # >>> substrate list <<<
    widget_list.append(tk.Entry(master=top_frame,width=30,justify='left',font=main_font))          # formula name
    widget_list[-1].insert(0,current_formula[1])
    widget_list[-1].grid(row=index+2,column=1,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # agg1
    widget_list[-1].insert(0,str(current_formula[2]))
    widget_list[-1].grid(row=index+2,column=2,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # agg2
    widget_list[-1].insert(0,str(current_formula[3]))
    widget_list[-1].grid(row=index+2,column=3,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # agg3
    widget_list[-1].insert(0,str(current_formula[4]))
    widget_list[-1].grid(row=index+2,column=4,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # cemen
    widget_list[-1].insert(0,str(current_formula[5]))
    widget_list[-1].grid(row=index+2,column=5,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # flyash
    widget_list[-1].insert(0,str(current_formula[6]))
    widget_list[-1].grid(row=index+2,column=6,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # water
    widget_list[-1].insert(0,str(current_formula[7]))
    widget_list[-1].grid(row=index+2,column=7,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # chemical 1
    widget_list[-1].insert(0,str(current_formula[8]))
    widget_list[-1].grid(row=index+2,column=8,padx=10,pady=3)
    widget_list.append(tk.Entry(master=top_frame,width=5,justify='center',font=main_font))         # chemical 2
    widget_list[-1].insert(0,str(current_formula[9]))
    widget_list[-1].grid(row=index+2,column=9,padx=10,pady=3)


tk.Label(master=bottom_frame,text="สถานะการปรับเปลี่ยนสูตร",font=main_font).grid(row=0,column=0,columnspan=2,sticky=tk.W)

status_text = tk.Text(master=bottom_frame,width=70,height=4,font=main_font)
status_text.grid(row=1,column=0)
update_button = tk.Button(master=bottom_frame,text="ปรับสูตร",command=update_formula_to_db,font=main_font,width=35,height=3)
update_button.grid(row=1,column=1,padx = 20,pady=10,sticky=tk.NSEW)


main_window.mainloop()

