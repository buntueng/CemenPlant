import pathlib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import  font
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

class DebugLoadcellApp:
    def __init__(self, master=None):
        #================= pymodbus obj =========================
        comport = '/dev/ttyS0'
        self.client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
        self.connection = self.client.connect()
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.mainFrame = ttk.Frame(self.toplevel1)

        main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
        display_font = font.Font(family='TH Niramit AS',size=30,weight="bold")

        self.read_button = tk.Button(self.mainFrame)
        self.read_button.configure(text='เริ่มอ่านค่า', width='20',height=2,font=main_font)
        self.read_button.grid(column='2', row='0',pady=10)
        self.read_button.configure(command=self.read_button_pressed)
        self.label1 = ttk.Label(self.mainFrame)
        self.label1.configure(text='ค่า Chem ใน PLC',font=main_font)
        self.label1.grid(column='0', padx='10 0', row='0')
        self.show_entry = ttk.Entry(self.mainFrame)
        self.plc_value_string = tk.StringVar(value='')
        self.show_entry.configure(state='disabled', textvariable=self.plc_value_string, width='10',font=display_font)
        self.show_entry.grid(column='1', padx='10', row='0',pady=10)
        self.stop_button = tk.Button(self.mainFrame)
        self.stop_button.configure(text='หยุดอ่าน', width='20',height=2,font=main_font)
        self.stop_button.configure(state='disabled')
        self.stop_button.grid(column='3', padx='10', pady='10', row='0')
        self.stop_button.configure(command=self.stop_button_pressed)
        self.mainFrame.configure(height='200', width='200')
        self.mainFrame.grid(column='0', row='0')
        self.toplevel1.configure(height='200', width='200')
        self.toplevel1.resizable(False, False)
        self.toplevel1.title('อ่านโหลดเซลล์ยุ้ง')
        self.center_screen(self.toplevel1)

        # Main widget
        self.mainwindow = self.toplevel1

        # ====== usefull variable ==========
        self.run_main_state_flag = False
    
    def run(self):
        self.mainwindow.mainloop()

    def read_button_pressed(self):
        self.main_state = 0
        self.run_main_state_flag = True
        self.run_main_state()
        self.read_button.configure(state='disabled')
        self.stop_button.configure(state='normal')


    def run_main_state(self):
        if self.run_main_state_flag:
            if self.main_state == 0:
                modbus_result = self.client.write_register(address=10,value=230,unit=2)
                if modbus_result.function_code < 0x80:
                    self.main_state = 1
            elif self.main_state == 1:
                modbus_result = self.client.write_coil(address=10,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    self.main_state = 2
            elif self.main_state == 2:   # show weight
                modbus_result = self.client.read_holding_registers(address=12,count=1,unit=2)
                if modbus_result.function_code < 0x80:
                    current_weight = int(modbus_result.registers[0])
                    self.plc_value_string.set(str(current_weight))

            #=========== stop button pressed ===========
            elif self.main_state == 100:
                modbus_result = self.client.write_coil(address=10,value=0,unit=2)
                if modbus_result.function_code < 0x80:
                    self.main_state = 101
            elif self.main_state == 101:
                self.run_main_state_flag = False
            self.mainwindow.after(500,self.run_main_state)
        else:
            print("stop running")


    def stop_button_pressed(self):
        self.main_state = 100
        self.read_button.configure(state='normal')
        self.stop_button.configure(state='disabled')

    def center_screen(self,top_level_window):
        top_level_window.update_idletasks()
        width = top_level_window.winfo_width()
        frm_width = top_level_window.winfo_rootx() - top_level_window.winfo_x()
        win_width = width + 2 * frm_width
        height = top_level_window.winfo_height()
        titlebar_height = top_level_window.winfo_rooty() - top_level_window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = top_level_window.winfo_screenwidth() // 2 - win_width // 2
        y = top_level_window.winfo_screenheight() // 2 - win_height // 2
        top_level_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        top_level_window.deiconify()


if __name__ == '__main__':
    app = DebugLoadcellApp()
    app.run()


