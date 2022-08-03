from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

comport = '/dev/ttyS0'
client = ModbusClient(method='rtu',port=comport,stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
time.sleep(3)
main_state = 0
for i in range(0,10):
    modbus_result = client.read_holding_registers(address=1,count=1,unit=6)
    if modbus_result.function_code < 0x80:
        print(modbus_result.registers[0])

print("exit loop")