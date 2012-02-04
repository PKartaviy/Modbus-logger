# -*- coding: utf-8 -*-
"""
@author: Kartaviy Pavel

"""
from minimalmodbus import Instrument 
import time

def blink(instrument):
    secs=1    
    try:    
        instrument.write_register(1102, 65000)
        time.sleep(secs)
        instrument.write_register(1102, 0)
    except:
        instrument.close()
    
def writeData(f, data):
    f.write(str(data[0]))    
    for variable in data[1:]:
        f.write(' ' + str(variable))
    f.write('\n');
    
def main(): 
    # Connect to robot
    port = "COM2"
    slaveNumber = 1
    settings = {"baudrate":9600, "stopbits":1, "parity":"E", "bytesize":8}
    #Register parameters
    #START_REGISTER = 1100
    #NUMBER_OF_REGISTERS = 10
    registers = {'engine_right':1100, 'engine_left':1101, 'light_level':1102, \
    'camera_id':1103, 'noop':1104, 'motor_direction_left':1105, \
    'motor_direction_right':1106}
    
    motka = Instrument(port, slaveNumber, **settings)       
    # test robot
    blink(motka)     

    # open log file
    name = "logs/log_"+time.strftime("%d_%b_%Y_%H_%M_%S") + ".txt"
    logFile = open(name, 'a')
    
    #Read data from device and write it to log file    
    try:    
        while 1:
            data = []        
            for value in registers.values():
                data.append( motka.read_register(value) )    
            writeData(logFile, data)
    except:
        print "Logger is stopped"
    
    logFile.close()
    motka.close()
    
if __name__ == "__main__":
    main()