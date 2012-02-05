# -*- coding: utf-8 -*-
"""
@author: Kartaviy Pavel
A simple modbus logger based on minimalmodbus
"""
from minimalmodbus import Instrument 
import time

def writeData(f, data):
    f.write(str(data[0]))    
    for variable in data[1:]:
        f.write(' ' + str(variable))
    f.write('\n');
    
def main(): 
    # Serial port parameters    
    port = "COM2"
    slaveNumber = 1
    BAUDRATE = 9600
    STOPBITS = 1
    PARITY = "E"
    BYTESIZE = 8
    
    # Register parameters. 
    # registers - list of registers which will be logged. 
    #START_REGISTER = 1100
    #NUMBER_OF_REGISTERS = 10
    registers = {'engine_right':1100, 'engine_left':1101, 'light_level':1102, \
    'camera_id':1103, 'noop':1104, 'motor_direction_left':1105, \
    'motor_direction_right':1106}

    # open log file
    name = "logs/log_"+time.strftime("%d_%b_%Y_%H_%M_%S") + ".txt"
    logFile = open(name, 'a')
    
    # Connect to robot
    motka = Instrument(port, slaveNumber)
    motka.serial.baudrate = BAUDRATE
    motka.serial.stopbits = STOPBITS
    motka.serial.parity = PARITY
    motka.serial.bytesize = BYTESIZE          
    
    #Read data from device and write it to log file    
    print "Logger started. If you want to stop press Cntrl+C "    
    try:    
        while 1:
            data = []        
            for value in registers.values():
                data.append( motka.read_register(value) )    
            writeData(logFile, data)
    except KeyboardInterrupt:
        print "Logger was stopped by keyboard interrupt"
    except:
        logFile.close()
        motka.close()         
        raise
    
    logFile.close()
    motka.close()
    
if __name__ == "__main__":
    main()