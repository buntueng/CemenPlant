import pathlib
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import sqlite3
from sqlite3 import Error
from datetime import datetime

software_path = os.path.dirname(os.path.realpath(__file__))
database_path = software_path +"/database/main_db.db"

class ReportWindowApp:
    def __init__(self, master=None):
        # build ui
        self.reportWindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame1 = ttk.Frame(self.reportWindow)
        self.select_date_label = ttk.Label(self.frame1)
        self.select_date_label.configure(text='เลือกวันที่ต้่องการแสดงผล')
        self.select_date_label.grid(column='0', columnspan='3', padx='10', row='0', sticky='ew')
        self.start_date_label = ttk.Label(self.frame1)
        self.start_date_label.configure(text='วันที่เริ่ม')
        self.start_date_label.grid(column='0', padx='10', row='1', sticky='ew')
        self.stop_date_label = ttk.Label(self.frame1)
        self.stop_date_label.configure(text='ถึงวันที่')
        self.stop_date_label.grid(column='2', row='1', sticky='ew')
        #=========================================================
        self.start_date_dateEntry = DateEntry(master = self.frame1, width=15, background='darkblue', foreground='white', borderwidth=2, justify='center',date_pattern='dd/MM/yyyy')
        self.start_date_dateEntry.grid(column='1',row='1')
        self.end_date_dateEntry = DateEntry(master = self.frame1, width=15, background='darkblue', foreground='white', borderwidth=2, justify='center',date_pattern='dd/MM/yyyy')
        self.end_date_dateEntry.grid(column='3',row='1')
        #=========================================================
        self.show_report_button = ttk.Button(self.frame1)
        self.show_report_button.configure(text='แสดงผล', width='10')
        self.show_report_button.grid(column='6', padx='10 0', row='1', rowspan='2',ipady=10,sticky='ew')
        self.show_report_button.configure(command=self.show_report_button_pressed)
        self.result_label = ttk.Label(self.frame1)
        self.result_label.configure(text='แสดงค่าทั้งหมด')
        self.result_label.grid(column='0', padx='10', row='2', sticky='ew')
        self.totsl_record_entry = ttk.Entry(self.frame1)
        self.total_record_number_int = tk.IntVar(value='')
        self.totsl_record_entry.configure(justify='center', state='readonly', textvariable=self.total_record_number_int, width='5')
        self.totsl_record_entry.grid(column='1', row='2', sticky='ew',pady=10)
        self.order_label = ttk.Label(self.frame1)
        self.order_label.configure(text='รายการ')
        self.order_label.grid(column='2', row='2', sticky='ew')
        columns = ('order_number', 'customer_name', 'date', 'amount','agg_name','target','measure','error')
        self.result_treeview = ttk.Treeview(self.frame1,columns=columns, show='headings',height=30)
        self.add_treeview_header()
        self.result_treeview.grid(column='0', columnspan='9', padx='10', row='3', sticky='ew',pady=10)
        self.yaxis_scrollbar = ttk.Scrollbar(self.frame1,command=self.result_treeview.yview)
        self.result_treeview.configure(yscrollcommand=self.yaxis_scrollbar.set)
        self.yaxis_scrollbar.configure(orient='vertical')
        self.yaxis_scrollbar.grid(column='9', padx='0 5', row='3', sticky='nse')
        self.export_button = ttk.Button(self.frame1)
        self.export_button.configure(text='ส่งค่าออก', width='10')
        self.export_button.grid(column='7', padx='10', row='1', rowspan='2', sticky='ew',ipady=10)
        self.export_button.configure(command=self.export_button_pressed)
        self.print_button = ttk.Button(self.frame1)
        self.print_button.configure(text='ปริ้น', width='10')
        self.print_button.grid(column='8', row='1', rowspan='2', sticky='ew',ipady=10)
        self.print_button.configure(command=self.print_button_pressed)
        self.frame1.configure(height='768', width='1024')
        self.frame1.pack(side='top')
        self.reportWindow.configure(height='768', width='1024')
        self.reportWindow.resizable(False, False)
        self.reportWindow.title('คอนกรีตผสม ห้างหุ้นส่วนจำกัด ปาน-ปริญ คอนกรีต')

        # Main widget
        self.mainwindow = self.reportWindow
    
    def add_treeview_header(self):
        self.result_treeview.heading('order_number', text='ลำดับ')
        self.result_treeview.heading('customer_name', text='ชื่อลูกค้า')
        self.result_treeview.heading('date', text='วันที่ เวลา')
        self.result_treeview.heading('amount', text='จำนวน')
        self.result_treeview.heading('agg_name', text='ส่วนผสม')
        self.result_treeview.heading('target', text='ค่าที่กำหนด')
        self.result_treeview.heading('measure', text='ชั่งจริง')
        self.result_treeview.heading('error', text='ความผิดพลาด')

        self.result_treeview.column("# 1",anchor=tk.CENTER, stretch=tk.NO, width=50)
        self.result_treeview.column("# 2",anchor=tk.CENTER, stretch=tk.NO, width=150)    
        self.result_treeview.column("# 3",anchor=tk.CENTER, stretch=tk.NO, width=150)
        self.result_treeview.column("# 4",anchor=tk.CENTER, stretch=tk.NO, width=60)
        self.result_treeview.column("# 5",anchor=tk.W, stretch=tk.NO, width=150)
        self.result_treeview.column("# 6",anchor=tk.CENTER, stretch=tk.NO, width=120)        # target
        self.result_treeview.column("# 7",anchor=tk.CENTER, stretch=tk.NO, width=120)
        self.result_treeview.column("# 8",anchor=tk.CENTER, stretch=tk.NO, width=120)

    def run(self):
        self.mainwindow.mainloop()

    def show_report_button_pressed(self):
        for i in self.result_treeview.get_children():
            self.result_treeview.delete(i)
        start_date_str = self.start_date_dateEntry.get_date().strftime("%Y-%m-%d 00:00:00")
        stop_date_str = self.end_date_dateEntry.get_date().strftime("%Y-%m-%d 23:59:59")
        db_connector = sqlite3.connect(database_path)
        db_cursor = db_connector.cursor()
        sql_query = "SELECT * FROM recording_table WHERE Record_time >= '" + start_date_str + "' AND Record_time <= '" + stop_date_str + "';"
        db_cursor.execute(sql_query)
        response_list = db_cursor.fetchall()
        db_connector.close()
        self.total_record_number_int.set(len(response_list))
        display_list = []
        for present_data in response_list:
            error1 = (int(present_data[14]) - int(present_data[6]))/int(present_data[6])*100
            error1_float = float("{:.2f}".format(error1))
            first_row = (present_data[0],present_data[2],present_data[1],present_data[4],"หิน 1",present_data[6],present_data[14],error1_float)
            display_list.append(first_row)

            error2 = (int(present_data[16]) - int(present_data[8]))/int(present_data[8])*100
            error2_float = float("{:.2f}".format(error2))
            second_row = ("","","","","หิน 2",present_data[8],present_data[16],error2_float)
            display_list.append(second_row)

            error3 = (int(present_data[15]) - int(present_data[7]))/int(present_data[7])*100
            error3_float = float("{:.2f}".format(error3))
            third_row = ("","","","","ทราย",present_data[7],present_data[15],error3_float)
            display_list.append(third_row)

            error4 = (int(present_data[17]) - int(present_data[9]))/int(present_data[9])*100
            error4_float = float("{:.2f}".format(error4))
            fourth_row = ("","","","","ปูนซีเมนต์",present_data[9],present_data[17],error4_float)
            display_list.append(fourth_row)

            error5 = (int(present_data[18]) - int(present_data[10]))/int(present_data[10])*100
            error5_float = float("{:.2f}".format(error5))
            fifth_row = ("","","","","เถ้าลอย",present_data[10],present_data[18],error5_float)
            display_list.append(fifth_row)

            error6 = (int(present_data[19]) - int(present_data[11]))/int(present_data[11])*100
            error6_float = float("{:.2f}".format(error6))
            sixth_row = ("","","","","น้ำ",present_data[11],present_data[19],error6_float)
            display_list.append(sixth_row)

            error7 = (float(present_data[20]) - float(present_data[12]))/float(present_data[12])*100
            error7_float = float("{:.2f}".format(error7))
            target_float = float("{:.1f}".format(present_data[12]))
            weight_float = float("{:.1f}".format(present_data[20]))
            seventh_row = ("","","","","น้ำยาเคมี 1",target_float,weight_float,error7_float)
            display_list.append(seventh_row)

            error8 = (float(present_data[21]) - float(present_data[13]))/float(present_data[13])*100
            error8_float = float("{:.2f}".format(error8))
            target_float = float("{:.1f}".format(present_data[13]))
            weight_float = float("{:.1f}".format(present_data[21]))
            eigth_row = ("","","","","น้ำยาเคมี 2",target_float,weight_float,error8_float)
            display_list.append(eigth_row)
        
        for display_item in display_list:
            self.result_treeview.insert('', tk.END, values=display_item)
        

    def export_button_pressed(self):
        pass

    def print_button_pressed(self):
        pass


if __name__ == '__main__':
    app = ReportWindowApp()
    app.run()


