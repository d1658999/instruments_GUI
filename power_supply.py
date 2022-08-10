import pyvisa
import logging
from logging.config import fileConfig
import time
import want_test_band as wt


PSU_LIST = ['E3631A', 'E3642A', ]
fileConfig('logging.ini')
logger = logging.getLogger()


class Psu:
    def __init__(self, psu_enable=False):
        if psu_enable:
            self.build_object()
            self.psu_init()
        else:
            logger.info('----------Disable PSU----------')

    def psu_init(self, voltage=wt.psu_voltage, current=wt.psu_current):
        logger.info('----------Init PSU----------')
        logger.info(self.psu.query("*IDN?").strip())
        self.psu.write('*CLS')
        self.psu.write('INST P6V')
        self.psu.write(f'VOLT {voltage}')
        self.psu.write(f'CURR {current}')

    def get_current(self):
        logger.info('----------Get current value----------')
        current_measure = []
        count = 0
        while count < 5:
            current = eval(self.psu.query('MEAS:CURR?')) * 1000
            logger.debug(current)
            current_measure.append(current)
            count += 1
            # time.sleep(0.1)
        return current_measure

    def current_average(self):
        logger.debug('calculation for currnet average')
        current_list = self.get_current()
        average = round(sum(current_list) / len(current_list), 2)
        logger.info(f'Average current: {average} mA')
        return average

    def build_object(self):
        logger.info('start to connect')
        gpib_want = None
        for gpib in self.get_gpib_psu():  # this is to search GPIB for 8820/8821
            inst = pyvisa.ResourceManager().open_resource(gpib)
            inst = inst.query('*IDN?').strip()
            for psu in PSU_LIST:
                if psu in inst:
                    gpib_want = gpib
                    break

        self.psu = pyvisa.ResourceManager().open_resource(gpib_want)  # to build inst object
        self.psu.timeout = 5000

    @staticmethod
    def get_gpib_psu():
        resources = []
        for resource in pyvisa.ResourceManager().list_resources():
            if 'GPIB' in resource:
                resources.append(resource)
                logger.debug(resource)
        return resources



def main():
        psu = Psu(wt.psu_enable)
        psu.current_average()






if __name__ == '__main__':
    main()