import serial
import time
import serial.tools.list_ports
import logging
from logging.config import fileConfig
from thermal_disable import thd

fileConfig('logging.ini')
logger = logging.getLogger()


class Flymode:
    def __init__(self, comport):
        self.begin(comport)
    def begin(self, comport):
        self.ser = serial.Serial()
        self.ser.baudrate = 230400
        self.ser.port = comport
        self.off = 'AT+CFUN=0\r'
        self.on = 'AT+CFUN=1\r'
    def com_open(self):
        self.ser.open()

    def com_close(self):
        self.ser.close()

    def fly_on(self):
        self.ser.write(self.off.encode())
        logger.info('flymode is on, 0')

    def fly_off(self):
        self.ser.write(self.on.encode())
        logger.info('flymode is off, 1')

def get_comport_wanted():
    comports = serial.tools.list_ports.comports()
    comport_waned = None
    for comport in comports:
        # print(comport.description)
        # print(type(comport.description))
        if 'Modem' in comport.description:
            comport_waned = comport.name
            logger.info(f'Modem comport is: {comport_waned}')
    return comport_waned

def main():

    port = get_comport_wanted()

    s = Flymode(port)
    s.com_open()
    s.fly_on()
    time.sleep(1)
    s.fly_off()

if __name__ == '__main__':
    main()


