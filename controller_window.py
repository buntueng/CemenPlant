import os
import tkinter as tk
from tkinter import  DISABLED, StringVar, font
from share_library import center_screen, default_window_size,read_concrete_formula_from_db,record_booking_data,read_booking_queue,remove_booking_queue,process_booking_queue
from share_library import get_processing_queue,relife_booking_queue,fail_booking_queue,read_concrete_formula
from share_library import complete_booking_queue,save_complete_queue
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

software_path = os.path.dirname(os.path.realpath(__file__))
run_home_window = 'python ' + software_path + '/home_window.py'

running = False

# ===========================
dummy_weight = 11

# ==== global variable =======
state_interval = 0
main_state = 0
in_loop = True
quad_cubic_load = False
first_loop = True
button_cancel_pressed = False
comport = '/dev/ttyS0'
#comport = 'COM3'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
# ============== processing state =================================
def main_controller():
    global main_state
    global in_loop
    global quad_cubic_load
    global first_loop
    global button_cancel_pressed
    try:
        if not running:
            print(main_state)
        if main_state == 0:
            button_cancel_pressed = False
            main_state = 1
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # load target weight of each aggs
        elif main_state == 1:
            current_batch_amount = float(concrete_order_string.get()) - float(mixed_finished_string.get())
            if  current_batch_amount >= 1:
                amount_string.set("1")
                # ======== load target aggs =======
                rock1_target_weight_string.set(str(int(one_cubic_rock1)))
                sand_target_weight_string.set(str(int(one_cubic_sand)))
                rock2_target_weight_string.set(str(int(one_cubic_rock2)))
                flyash_target_weight_string.set(str(int(one_cubic_flyash)))
                cemen_target_weight_string.set(str(int(one_cubic_cemen)))
                water_target_weight_string.set(str(int(one_cubic_water)))
                chem1_target_weight_string.set(str(one_cubic_chem1))
                chem2_target_weight_string.set(str(one_cubic_chem2))
            else:
                one_digit_display = "{:.2f}".format(current_batch_amount)
                amount_string.set(one_digit_display)
                rock1_target_weight_string.set(str(int(one_cubic_rock1*current_batch_amount)))
                sand_target_weight_string.set(str(int(one_cubic_sand*current_batch_amount)))
                rock2_target_weight_string.set(str(int(one_cubic_rock2*current_batch_amount)))
                flyash_target_weight_string.set(str(int(one_cubic_flyash*current_batch_amount)))
                cemen_target_weight_string.set(str(int(one_cubic_cemen*current_batch_amount)))
                water_target_weight_string.set(str(int(one_cubic_water*current_batch_amount)))
                one_digit_display = "{:.1f}".format(one_cubic_chem1*current_batch_amount)
                chem1_target_weight_string.set(one_digit_display)
                one_digit_display = "{:.1f}".format(one_cubic_chem2*current_batch_amount)
                chem2_target_weight_string.set(one_digit_display)
            # ==== check loads =========
            if current_batch_amount >= 0.75:
                quad_cubic_load = False
            else:
                quad_cubic_load = True
            main_state = 2
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # initialize PLC1
        elif main_state == 2:                                                 # reset most coils except mixer (M6)
            if running:
                modbus_result = client.write_coil(address=6,value=1,unit=0x01)  # this coil will reset itself in 0.1 seconds
                if modbus_result.function_code < 0x80:
                    main_state = 3
            else:
                add_status("init PLC1")
                main_state = 3      ## test to state 602
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        elif main_state == 3:                                               # if first loop stop mixer else go next state
            if running:
                if first_loop == True:
                    modbus_result = client.write_coil(address=10,value=0,unit=0x01)
                    if modbus_result.function_code < 0x80:
                        main_state = 4
                else:
                    main_state = 4
            else:
                #add_status("first loop -- stop mixer")
                main_state = 4
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        # initial PLC2
        elif main_state == 4:                                               # reset all coils in PLC2
            if running:
                modbus_result = client.write_coil(address=15,value=1,unit=0x02)
                if modbus_result.function_code < 0x80:
                    main_state = 5
            else:
                add_status("init PLC2")
                main_state = 5
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        # === tempolary state =====
        elif main_state == 5:
            main_state = 6
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
            #add_status("tempolary state")

        # set rock1 weights to PLC1
        elif main_state == 6:
            rock1_weight_int = int((float(rock1_target_weight_string.get())+65)/2)
            if running:
                modbus_result = client.write_register(address=0,value=rock1_weight_int,unit=0x01)
                if modbus_result.function_code < 0x80:
                    main_state = 7
            else:
                main_state = 7
                message = "set rock1 " + str(rock1_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        
        # set rock2 weights to PLC1 (rock1 + rock2)
        elif main_state == 7:
            r1 = float(rock1_target_weight_string.get())
            r2 = float(rock2_target_weight_string.get())
            rock2_weight_int = int(((r1+r2)+65)/2)
            if running:
                modbus_result = client.write_register(address=2,value=rock2_weight_int,unit=0x01)
                if modbus_result.function_code < 0x80:
                    main_state = 8
            else:
                main_state = 8
                message = "set rock2 " + str(rock2_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        
        # set sand weights to PLC1 (rock1 + rock2 + sand)
        elif main_state == 8:
            s1 = float(sand_target_weight_string.get())
            r1 = float(rock1_target_weight_string.get())
            r2 = float(rock2_target_weight_string.get())
            sand_weight_int = int(((s1+r1+r2)+65)/2)
            if running:
                modbus_result = client.write_register(address=1,value=sand_weight_int,unit=0x01)
                if modbus_result.function_code < 0x80:
                    main_state = 9
            else:
                main_state = 9
                message = "set sand " + str(sand_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        # set process to open rock1 gate
        elif main_state == 9:
            if running:
                modbus_result = client.write_coil(address=7,value=quad_cubic_load,unit=0x01)
                if modbus_result.function_code < 0x80:
                    main_state = 10
            else:
                main_state = 10
                message = "set process to open rock1"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        # ======== start weighting rock1 ===========
        elif main_state == 10:
            rock1_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=0,value=1,unit=0x01)
                if modbus_result.function_code < 0x80:
                    main_state = 11
            else:
                main_state = 11
                message = "start weighing rock1"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        # ========= set flyash weight ==============
        elif main_state == 11:
            flyash_float = float(flyash_target_weight_string.get())*1.02
            flyash_weight_int = 0
            current_amount = float(amount_string.get())
            if current_amount <= 0.5:
                if flyash_float <= 11:
                    flyash_weight_int = int((flyash_float))
                else:
                    flyash_weight_int = int(((flyash_float)-7)/1.05)
            else:
                if flyash_float <= 11:
                    flyash_weight_int = int((flyash_float)*1.3)
                else:
                    flyash_weight_int = int((flyash_float)*1.35)
            
            # if flyash_float <= 15:
            #     #flyash_weight_int = int((flyash_float)/1.05)
            #     flyash_weight_int = int((flyash_float))
            # else:
            #     #flyash_weight_int = int((flyash_float-11)/1.05)
            #     flyash_weight_int = int((flyash_float-11))
            # ======== running process =======
            if running:
                modbus_result = client.write_register(address=0,value=flyash_weight_int,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 12
            else:
                main_state = 12
                message = "set flyash weight " + str(flyash_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========= set cemen weight (flyash+cemen) =====
        elif main_state == 12:
            f1 = float(flyash_target_weight_string.get())
            c1 = float(cemen_target_weight_string.get())
            #cemen_weight_int = int(((f1+c1)-11)/1.05)
            # ============ set condition 0.5 and 1 cubic
            cemen_weight_int = 0
            current_amount = float(amount_string.get())
            if current_amount <= 0.5:
                cemen_weight_int = int((f1+c1)/1.01)
            else:
                cemen_weight_int = int((f1+c1)/1.03)
            
            if running:
                modbus_result = client.write_register(address=1,value=cemen_weight_int,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 13
            else:
                main_state = 13
                message = "set cemen " + str(cemen_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======== set water weight =============
        elif main_state == 13:
            water_weight_int = int((float(water_target_weight_string.get())+0.5))
            if running:
                modbus_result = client.write_register(address=5,value=water_weight_int,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 14
            else:
                main_state = 14
                message = "set water " + str(water_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======= set chem1 weight =============
        elif main_state == 14:
            chem1_weight_int = int(float(chem1_target_weight_string.get())*200)
            if running:
                modbus_result = client.write_register(address=10,value=chem1_weight_int,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 15
            else:
                main_state = 15
                message = "set chem1 " + str(chem1_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======= set chem2 weight (chem1+chem2) =============
        elif main_state == 15:
            c1 = float(chem1_target_weight_string.get())
            c2 = float(chem2_target_weight_string.get())
            chem2_weight_int = int((c1+c2)*200)
            if running:
                modbus_result = client.write_register(address=11,value=chem2_weight_int,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 16
            else:
                main_state = 16
                message = "set chem2 " + str(chem2_weight_int) + " kg"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ====== start weighting chem1 =========
        elif main_state == 16:
            chem1_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=10,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 17
            else:
                main_state = 17
                message = "start weighing chem1"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======= start weighting  flyash =====
        elif main_state == 17:
            flyash_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=0,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 18
            else:
                main_state = 18
                message = "start weighing flyash"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======= start weighting water =======
        elif main_state == 18:
            water_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=7,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 19
            else:
                main_state = 19
                message = "start weighing water"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======== check rock1 ================
        elif main_state == 19:
            if running:
                modbus_result = client.read_coils(address=1,count=1,unit=1)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 20
                    rock1_display_label.configure(bg='white')
            else:
                rock1_display_label.configure(bg='white')
                main_state = 20
                message = "check rock1"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========= read rock1 weight =========
        elif main_state == 20:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=5)
                if modbus_result.function_code < 0x80:
                    rock1_weight = int(modbus_result.registers[0])
                    rock1_weight_string.set(str(rock1_weight))
                    agg_total_weight_string.set(str(rock1_weight))
                    # ===== update total weight ======
                    previous_weight = int(float(total_rock1_weight_string.get()))
                    update_weight = previous_weight + int(rock1_weight_string.get())
                    total_rock1_weight_string.set(str(update_weight))
                    main_state = 21
            else:
                agg_total_weight_string.set("11")
                rock1_weight_string.set(str(dummy_weight))
                #========= update total weight ======
                previous_weight = int(float(total_rock1_weight_string.get()))
                update_weight = previous_weight + int(rock1_weight_string.get())
                total_rock1_weight_string.set(str(update_weight))
                main_state = 21
                message = "read rock1 weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)

        # ======= start rock2 =================
        elif main_state == 21:
            rock2_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=2,value=1,unit=1)
                if modbus_result.function_code < 0x80:
                    main_state = 22
            else:
                main_state = 22
                message = "start weighing rock2"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======== check chem1 =================
        elif main_state == 22:
            if running:
                modbus_result = client.read_coils(address=11,count=1,unit=2)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 23
                    chem1_display_label.configure(bg='white')
            else:
                chem1_display_label.configure(bg='white')
                main_state = 23
                message = "check chem1"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========= read chem1 ================
        elif main_state == 23:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=8)
                if modbus_result.function_code < 0x80:
                    chem1_weight_float = int(modbus_result.registers[0])/10
                    one_digit_floating = "{:.1f}".format(chem1_weight_float)
                    chem1_weight_string.set(one_digit_floating)
                    # =========== upate total chem1 ================
                    previous_weight = float(total_chem1_weight_string.get())
                    update_weight = previous_weight + float(chem1_weight_string.get())
                    one_digit = "{:.1f}".format(update_weight)
                    total_chem1_weight_string.set(one_digit)
                    main_state = 24
            else:
                chem1_weight_string.set(str(dummy_weight))
                # =========== upate total chem1 ================
                previous_weight = float(total_chem1_weight_string.get())
                update_weight = previous_weight + float(chem1_weight_string.get())
                one_digit = "{:.1f}".format(update_weight)
                total_chem1_weight_string.set(one_digit)
                main_state = 24
                message = "read chem1"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ======== start chem2 ================
        elif main_state == 24:
            chem2_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=12,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 25
            else:
                main_state = 25
                message = "start chem2"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ============== check water ================
        elif main_state == 25:
            if running:
                modbus_result = client.read_coils(address=8,count=1,unit=2)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 26
                    water_display_label.configure(bg='white')
            else:
                water_display_label.configure(bg='white')
                main_state = 26
                message = "check water"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 1500
                main_window.after(state_delay,main_controller)
        # ============= show water ===================
        elif main_state == 26:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=7)
                if modbus_result.function_code < 0x80:
                    water_weight = int(float(modbus_result.registers[0]))
                    water_weight_string.set(str(water_weight))
                    # =========== update total weight ===========
                    previous_weight = int(total_water_weight_string.get())
                    update_weight = previous_weight + int(water_weight_string.get())
                    total_water_weight_string.set(str(update_weight))
                    main_state = 300
            else:
                water_weight_string.set(str(dummy_weight))
                # =========== update total weight ===========
                previous_weight = int(total_water_weight_string.get())
                update_weight = previous_weight + int(water_weight_string.get())
                total_water_weight_string.set(str(update_weight))
                main_state = 300
                message = "read water weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ====================================================== start mixer =============================
        elif main_state == 300:                                               # if first loop start mixer
            mixer_display_label.configure(bg='green')
            if first_loop == True:
                if running:
                    modbus_result = client.write_coil(address=10,value=1,unit=0x01)
                    if modbus_result.function_code < 0x80:
                        first_loop = False
                        main_state = 301
                else:
                    main_state = 301
                    message = "run first loop"
                    add_status(message)
            else:
                main_state = 301
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========= dummy state =====
        elif main_state == 301:
            message = "dummy state"
            add_status(message)
            main_state = 302
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== check flyash ============
        elif main_state == 302:
            if running:
                modbus_result = client.read_coils(address=1,count=1,unit=2)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 303
                    flyash_display_label.configure(bg='white')
            else:
                flyash_display_label.configure(bg='white')
                main_state = 303
                message = "check flyash"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # =========== read flyash weight ======
        elif main_state == 303:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=6)
                if modbus_result.function_code < 0x80:
                    flyash_weight = int(modbus_result.registers[0])
                    flyash_weight_string.set(str(flyash_weight))
                    # =========== update total weight ===========
                    previous_weight = int(total_flyash_weight_string.get())
                    update_weight = previous_weight + int(flyash_weight_string.get())
                    total_flyash_weight_string.set(str(update_weight))
                    main_state = 304
            else:
                flyash_weight_string.set(str(dummy_weight))
                # =========== update total weight ===========
                previous_weight = int(total_flyash_weight_string.get())
                update_weight = previous_weight + int(flyash_weight_string.get())
                total_flyash_weight_string.set(str(update_weight))
                main_state = 304
                message = "read flyash weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== start weighting cemen ======
        elif main_state == 304:
            cemen_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=5,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 305
            else:
                main_state = 305
                message = "start weighing cemen"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # =========== check rock2 ======
        elif main_state == 305:
            if running:
                modbus_result = client.read_coils(address=3,count=1,unit=1)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 306
                    rock2_display_label.configure(bg='white')
            else:
                rock2_display_label.configure(bg='white')
                main_state = 306
                message = "check rock2 state"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== read rock2 weight ===========
        elif main_state == 306:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=5)
                if modbus_result.function_code < 0x80:
                    rock1_plus_rock2_weight = int(modbus_result.registers[0])
                    rock2_weight = rock1_plus_rock2_weight - int(rock1_weight_string.get())
                    rock2_weight_string.set(str(rock2_weight))
                    agg_total_weight_string.set(str(rock1_plus_rock2_weight))
                    # =========== update total weight ===========
                    previous_weight = int(total_rock2_weight_string.get())
                    update_weight = previous_weight + int(rock2_weight_string.get())
                    total_rock2_weight_string.set(str(update_weight))
                    main_state = 307
            else:
                rock2_weight_string.set(str(dummy_weight))
                # =========== update total weight ===========
                previous_weight = int(total_rock2_weight_string.get())
                update_weight = previous_weight + int(rock2_weight_string.get())
                total_rock2_weight_string.set(str(update_weight))
                agg_total_weight_string.set(str(22))
                rock1_weight_string.set(dummy_weight)
                main_state = 307
                message = "read rock2 weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== start weighting sand ========
        elif main_state == 307:
            sand_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=4,value=1,unit=1)
                if modbus_result.function_code < 0x80:
                    main_state = 308
            else:
                main_state = 308
                message = "start weighing sand"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 2000
                main_window.after(state_delay,main_controller)
        # ========== check cemen ================
        elif main_state == 308:
            if running:
                modbus_result = client.read_coils(address=6,count=1,unit=0x02)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 309
                    cemen_display_label.configure(bg='white')
            else:
                cemen_display_label.configure(bg='white')
                main_state = 309
                message = "check cemen state"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 1000
                main_window.after(state_delay,main_controller)
        # ====== read cemen weight ==============
        elif main_state == 309:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=6)
                if modbus_result.function_code < 0x80:
                    flyash_plus_cemen_weight = int(modbus_result.registers[0])
                    cemen_weight = flyash_plus_cemen_weight - int(flyash_weight_string.get())
                    cemen_weight_string.set(str(cemen_weight))
                    # =========== update total weight ===========
                    previous_weight = int(total_cemen_weight_string.get())
                    update_weight = previous_weight + int(cemen_weight_string.get())
                    total_cemen_weight_string.set(str(update_weight))
                    main_state = 310
            else:
                cemen_weight_string.set(str(dummy_weight))
                # =========== update total weight ===========
                previous_weight = int(total_cemen_weight_string.get())
                update_weight = previous_weight + int(cemen_weight_string.get())
                total_cemen_weight_string.set(str(update_weight))
                main_state = 310
                message = "read cemen weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== check chem2 ===============
        elif main_state == 310:
            if running:
                modbus_result = client.read_coils(address=13,count=1,unit=2)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 311
            else:
                main_state = 311
                message = "check chem2"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== read chem 2 ================
        elif main_state == 311:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=8)
                if modbus_result.function_code < 0x80:
                    chem1_chem2_weight_float = int(modbus_result.registers[0])/10
                    chem2_weight_float = chem1_chem2_weight_float - float(chem1_weight_string.get())
                    one_digit_floating = "{:.1f}".format(chem2_weight_float)
                    chem2_weight_string.set(one_digit_floating)
                    chem2_display_label.configure(bg='white')
                    # =========== upate total chem1 ================
                    previous_weight = float(total_chem2_weight_string.get())
                    update_weight = previous_weight + float(chem2_weight_string.get())
                    one_digit = "{:.1f}".format(update_weight)
                    total_chem2_weight_string.set(one_digit)
                    main_state = 312
            else:
                chem2_weight_string.set(str(dummy_weight))
                chem2_display_label.configure(bg='white')
                previous_weight = float(total_chem2_weight_string.get())
                update_weight = previous_weight + float(chem2_weight_string.get())
                one_digit = "{:.1f}".format(update_weight)
                total_chem2_weight_string.set(one_digit)
                main_state = 312
                message = "read chem2 weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========== check sand ================
        elif main_state == 312:
            if running:
                modbus_result = client.read_coils(address=5,count=1,unit=1)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 313
                    sand_display_label.configure(bg='white')
            else:
                sand_display_label.configure(bg='white')
                main_state = 313
                message = "check sand weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ========= read sand weight ============
        elif main_state == 313:
            if running:
                modbus_result = client.read_holding_registers(address=1,count=1,unit=5)
                if modbus_result.function_code < 0x80:
                    rock1_plus_rock2_plus_sand_weight = int(modbus_result.registers[0])
                    sand_weight = rock1_plus_rock2_plus_sand_weight - int(rock1_weight_string.get()) - int(rock2_weight_string.get())
                    sand_weight_string.set(str(sand_weight))
                    agg_total_weight_string.set(str(rock1_plus_rock2_plus_sand_weight))
                    # =========== update total weight ===========
                    previous_weight = int(total_sand_weight_string.get())
                    update_weight = previous_weight + int(sand_weight_string.get())
                    total_sand_weight_string.set(str(update_weight))
                    main_state = 314
            else:
                sand_weight_string.set(str(dummy_weight))
            # =========== update total weight ===========
                previous_weight = int(total_sand_weight_string.get())
                update_weight = previous_weight + int(sand_weight_string.get())
                total_sand_weight_string.set(str(update_weight))
                agg_total_weight_string.set("33")
                main_state = 314
                message = "read sand weight"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # =============== start mixed all aggregates here ========
        elif main_state == 314:
            conveyor_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=11,value=1,unit=1)
                if modbus_result.function_code < 0x80:
                    main_state = 315
            else:
                main_state = 315
                message = "start mixing aggs"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 15000
                main_window.after(state_delay,main_controller)
        # ============= pump chem to mixer ========================
        elif main_state == 315:
            chem1_display_label.configure(bg='yellow')
            chem2_display_label.configure(bg='yellow')
            if running:
                modbus_result = client.write_coil(address=14,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 316
            else:
                main_state = 316
                message = "pump chemical to mixer"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # =============== check status aggs to mixer ==============
        elif main_state == 316:
            if running:
                modbus_result = client.read_coils(address=12,count=1,unit=1)
                if (modbus_result.function_code < 0x80) and (modbus_result.bits[0] == True):
                    main_state = 317
                    chem1_display_label.configure(bg='white')
                    chem2_display_label.configure(bg='white')
                    conveyor_label.configure(bg='white')
            else:
                chem1_display_label.configure(bg='white')
                chem2_display_label.configure(bg='white')
                conveyor_label.configure(bg='white')
                main_state = 317
                message = "check agg status"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ================= dummy state >> wait mixer ==============
        elif main_state == 317:
            # message = "dummy state"
            # add_status(message)
            main_state = 318
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # ================= open mixer gate all process take 8 seconds =========================
        elif main_state == 318:
            mixer_valve_display_label.configure(bg='green')
            if running:
                modbus_result = client.write_coil(address=20,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 319            # state 319
            else:
                main_state = 319                # state 319
                message = "open mixer gate"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 1000
                main_window.after(state_delay,main_controller)
        # ==============================================
        elif main_state == 319:     # wait 3 seconds
            main_state = 320
            if in_loop:
                state_delay = state_interval + 3000
                main_window.after(state_delay,main_controller)
        elif main_state == 320:
            if running:
                modbus_result = client.write_coil(address=20,value=0,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 321
            else:
                message = "dummy state"
                add_status(message)
                main_state = 321
            if in_loop:
                state_delay = state_interval + 3000
                main_window.after(state_delay,main_controller)

        elif main_state == 321:
            if running:
                modbus_result = client.write_coil(address=20,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 322
                    #mixer_valve_display_label.configure(bg='white')
            else:
                message = "dummy state"
                add_status(message)
                main_state = 322
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        
        # ============ wait open mixer gate finished
        elif main_state == 322:
            if running:
                modbus_result = client.read_coils(address=20,count=1,unit=2)
                if modbus_result.function_code < 0x80 and modbus_result.bits[0] == False:
                    main_state = 323
                    #mixer_valve_display_label.configure(bg='white')
            else:
                message = "dummy state"
                add_status(message)
                main_state = 323
            if in_loop:
                state_delay = state_interval + 1000
                main_window.after(state_delay,main_controller)
        # ========== reopen gate 6 seconds ===================
        elif main_state == 323:
            if running:
                modbus_result = client.write_coil(address=20,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 324
            else:
                main_state = 324
                message = "reopen mixer gate"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 6000
                main_window.after(state_delay,main_controller)
        # ================ close mixer gate ===================
        elif main_state == 324:
            mixer_valve_display_label.configure(bg='white')
            if running:
                modbus_result = client.write_coil(address=20,value=0,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 600
            else:
                main_state = 600
                message = "close mixer gate"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)  
        # ========= update amount finished and check is process complete >> if not go to state 1  else go to next state ================= 
        elif main_state == 600:
            mixed_amount = float(amount_string.get())
            mixed_finish = float(mixed_finished_string.get())+ mixed_amount
            one_digit_floating = "{:.2f}".format(mixed_finish)
            mixed_finished_string.set(one_digit_floating)
            amount_string.set("0")
            total_order_amount = float(concrete_order_string.get())
            clear_previous_weight_display()
            if total_order_amount > mixed_finish:
                main_state = 1    # return to previous state
            else:
                main_state = 601    # mixed finished
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
        # =========== finished state ============
        elif main_state == 601:
            if running:
                # ===== stop mixer ===== 
                modbus_result = client.write_coil(address=10,value=0,unit=1)
                if modbus_result.function_code < 0x80:
                    main_state = 602
                    mixer_display_label.configure(bg='white')
            else:
                mixer_display_label.configure(bg='white')
                main_state = 602
                message = "finish state"
                add_status(message)
            if in_loop:
                state_delay = state_interval + 500
                main_window.after(state_delay,main_controller)
            
        elif main_state == 602:
            stop_process_button.config(state='disabled')
            start_process_button.configure(state='normal')
            add_status("End process")
            #======= add this queue to database ==========
            data_list=[]
            data_list.append(booking_ID)
            data_list.append(customer_name_string.get())
            data_list.append(keep_sample)
            data_list.append(float(concrete_order_string.get()))
            agg1_target = int(one_cubic_rock1*float(concrete_order_string.get()))
            data_list.append(agg1_target)      # agg1_target
            agg2_target = int(one_cubic_sand*float(concrete_order_string.get()))
            data_list.append(agg2_target)      # agg2_target
            agg3_target = int(one_cubic_rock2*float(concrete_order_string.get()))
            data_list.append(agg3_target)      # agg3_target
            cemen_target = int(one_cubic_cemen*float(concrete_order_string.get()))
            data_list.append(cemen_target)      # cemen_target
            flyash_target = int(one_cubic_flyash*float(concrete_order_string.get()))
            data_list.append(flyash_target)      # flyash_target
            water_target = int(one_cubic_water*float(concrete_order_string.get()))
            data_list.append(water_target)      # water_target
            chem1_target = float(one_cubic_chem1*float(concrete_order_string.get()))
            data_list.append(chem1_target)      # chem1_target
            chem2_target = float(one_cubic_chem2*float(concrete_order_string.get()))
            data_list.append(chem2_target)      # chem2_target
            #======== save measured data ======
            agg1_measure = int(total_rock1_weight_string.get())
            data_list.append(agg1_measure)      # agg1
            agg2_measure = int(total_sand_weight_string.get())
            data_list.append(agg2_measure)      # agg2
            agg3_measure = int(total_rock2_weight_string.get())
            data_list.append(agg3_measure)      # agg3
            cemen_measure = int(total_cemen_weight_string.get())
            data_list.append(cemen_measure)      # cemen
            flyash_measure = int(total_flyash_weight_string.get())
            data_list.append(flyash_measure)      # flyash
            water_measure = int(total_water_weight_string.get())
            data_list.append(water_measure)      # water
            chem1_measure = float(total_chem1_weight_string.get())
            data_list.append(chem1_measure)      # chem1
            chem2_measure = float(total_chem2_weight_string.get())
            data_list.append(chem2_measure)      # chem2
            data_list.append(formula_name_string.get())
            data_list.append(float(concrete_order_string.get()))
            save_complete_queue(data_list)
            #======= update queue status =================
            complete_booking_queue(booking_ID)
            start_process_button.configure(state=tk.DISABLED)
            go_home_button.configure(state=tk.NORMAL)


        # this state run after the stop button pressed
        # clear all coils in PLC1 and PLC2 after that exit loop
        elif main_state == 1000:            # reset PLC1
            if running:
                modbus_result = client.write_coil(address=6,value=1,unit=1)
                if modbus_result.function_code < 0x80:
                    main_state = 1001
            else:
                main_state = 1001
                add_status("run state 1000")
            state_delay = state_interval + 500
            main_window.after(state_delay,main_controller)
        elif main_state == 1001:            # reset PLC2
            if running:
                modbus_result = client.write_coil(address=15,value=1,unit=2)
                if modbus_result.function_code < 0x80:
                    main_state = 1002
            else:
                main_state = 1002
                add_status("run state 1001")
            state_delay = state_interval + 500
            main_window.after(state_delay,main_controller)
        elif main_state == 1002:            # turn off mixer
            if running:
                modbus_result = client.write_coil(address=10,value=0,unit=1)
                if modbus_result.function_code < 0x80:
                    main_state = 1003
            else:
                main_state = 1003
                add_status("run state 1002")
            state_delay = state_interval + 500
            main_window.after(state_delay,main_controller)
        # === dummy state ======
        elif main_state == 1003:
            main_state = 1004
            state_delay = state_interval + 500
            main_window.after(state_delay,main_controller)
        elif main_state == 1004:
            pass
    except Exception:
        message = "มีข้อผิดพลาด state = " + str(main_state) + str(Exception)
        add_status(message)
        state_delay = state_interval + 500
        main_window.after(state_delay,main_controller)
# =================================================================
def clear_total_weight_display():
    mixed_finished_string.set('0.0')
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
    #main_window.after(100,main_controller)
    start_process_button.config(state=tk.DISABLED)
    stop_process_button.config(state=tk.NORMAL)
    go_home_button.config(state=tk.DISABLED)

    clear_total_weight_display()
    clear_previous_weight_display()
    add_status("เริ่มผสมคอนกรีต")
    main_controller()

# =================================================================
def stop_process_button_pressed():
    global in_loop
    global main_state
    global button_cancel_pressed

    button_cancel_pressed = True
    add_status("หยุดการผสมคอนกรีต")
    fail_booking_queue(booking_ID)
    main_state = 1000
    in_loop = False
    start_process_button.config(state=tk.NORMAL)
    stop_process_button.config(state=tk.DISABLED)
    go_home_button.config(state=tk.NORMAL)
# ============= sub functions =====================================
def go_home():
    if int(booking_ID)>0:
        if main_state == 0:
            relife_booking_queue(booking_ID)
        elif main_state >= 1000:
            fail_booking_queue(booking_ID)
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
concrete_order_string = StringVar()
formula_name_string = StringVar()

customer_name_label = tk.Label(master=top_left_frame,text='ชื่อลูกค้า',font=main_font)
customer_name_entry = tk.Entry(master=top_left_frame,width=35,font=main_font,state=DISABLED,textvariable=customer_name_string)
telephone_number_label = tk.Label(master=top_left_frame,text="เบอร์โทร",font=main_font)
telephone_number_entry = tk.Entry(master=top_left_frame,width=35,font=main_font,state=DISABLED,textvariable=customer_number_string)
formula_name_label = tk.Label(master=top_left_frame,text='สูตรปูน',font=main_font)
formula_name_entry = tk.Entry(master=top_left_frame,width=35,font=main_font,state=DISABLED,textvariable=formula_name_string)

concrete_amount_label = tk.Label(master=top_left_frame,text="จำนวน",font=main_font)
concrete_amount_entry = tk.Entry(master=top_left_frame,state=DISABLED,font=main_font,width=15,textvariable=concrete_order_string)
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
amount_label = tk.Label(master=right_frame,text='กำลังผสม',font=main_font)
amount_entry = tk.Entry(master=right_frame,width=7,font=main_font,justify=tk.CENTER,state=DISABLED,textvariable=amount_string)
mixed_finish_label = tk.Label(master=right_frame,text='โหลดแล้ว',font=main_font)
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

## [Booking_ID,Customer_Name,Phone,Amount,Formula_ID,Formula_Name,Keep_Sample]
current_booking = get_processing_queue()
booking_ID = '0'
keep_sample = 0

one_cubic_rock1 = 0
one_cubic_rock2 = 0
one_cubic_sand = 0
one_cubic_cemen = 0
one_cubic_flyash = 0
one_cubic_water = 0
one_cubic_chem1 = 0
one_cubic_chem2 = 0

if len(current_booking) > 0:
    customer_name_string.set(current_booking[1])
    customer_number_string.set(current_booking[2])
    concrete_order_string.set(str(current_booking[3]))
    #amount_string.set(str(current_booking[3]))
    amount_string.set("0")
    formula_name_string.set(current_booking[6])
    booking_ID = current_booking[0]         # this object is a string class
    mixed_finished_string.set('0.0')
    keep_sample = current_booking[5]

    resp = read_concrete_formula(int(current_booking[4]))
    one_cubic_rock1 = resp[2]           # int
    one_cubic_rock2 = resp[4]           # int
    one_cubic_sand = resp[3]            # int
    one_cubic_cemen = resp[5]           # int
    one_cubic_flyash = resp[6]          # int
    one_cubic_water = resp[7]           # int
    one_cubic_chem1 = resp[8]           # float
    one_cubic_chem2 = resp[9]           # float

if concrete_order_string.get() == "":
    start_process_button.configure(state=tk.DISABLED)

main_window.mainloop()