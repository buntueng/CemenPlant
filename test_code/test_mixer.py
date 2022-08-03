from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

comport = '/dev/ttyS0'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
time.sleep(3)
main_state = 0
while True:
    print("in loop")
    if main_state == 0:
        modbus_result = client.write_coil(address=10,value=1,unit=0x01)
        if modbus_result.function_code < 0x80:
            main_state = 1

    elif main_state == 1:
        print("ff")
        time.sleep(15)
        print("kk")
        main_state = 2

    elif main_state == 2:
        modbus_result = client.write_coil(address=10,value=0,unit=0x01)
        if modbus_result.function_code < 0x80:
            main_state = 3
        time.sleep(2)

    elif main_state == 3:
        time.sleep(2)
        break
    time.sleep(1)

print("exit loop")