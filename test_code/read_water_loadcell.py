from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

comport = '/dev/ttyS0'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
time.sleep(3)
main_state = 0
while True:
    if main_state == 0:
        print("state 0")
        modbus_result = client.read_holding_registers(address=0,count=1,unit=7)
        if modbus_result.function_code < 0x80:
            print(modbus_result.registers[0])
            main_state = 1

    elif main_state == 1:
        print("state 1")
        modbus_result = client.read_holding_registers(address=0,count=1,unit=7)
        if modbus_result.function_code < 0x80:
            print(type(modbus_result.registers[0]))
            main_state = 2

    elif main_state == 2:
        print("state 2")
        break
    time.sleep(2)

print("exit loop")