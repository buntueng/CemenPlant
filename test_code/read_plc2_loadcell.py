from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

comport = '/dev/ttyS0'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
time.sleep(3)
main_state = 0
loop_counter = 0
while True:
    if main_state == 0:
        print("state 0")
        modbus_result = client.write_coil(address=0,value=1,unit=2)
        if modbus_result.function_code < 0x80:
            main_state = 1

    elif main_state == 1:
        print("D0")
        modbus_result = client.read_holding_registers(address=0,count=1,unit=2)
        if modbus_result.function_code < 0x80:
            print(modbus_result.registers[0])
            main_state = 2
    
    elif main_state == 2:
        print("D1")
        modbus_result = client.read_holding_registers(address=1,count=1,unit=2)
        if modbus_result.function_code < 0x80:
            print(modbus_result.registers[0])
            main_state = 3
    
    elif main_state == 3:
        print("D2")
        modbus_result = client.read_holding_registers(address=2,count=1,unit=2)
        if modbus_result.function_code < 0x80:
            print(modbus_result.registers[0])
            loop_counter = loop_counter + 1
            if loop_counter >= 10:
                main_state = 4
            else:
                main_state = 1

    elif main_state == 4:
        print("state 4")
        break
    time.sleep(2)

print("exit loop")