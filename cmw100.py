import serial
import time
import datetime
import serial.tools.list_ports
import logging
import pyvisa
from logging.config import fileConfig
import openpyxl
from openpyxl.chart import LineChart, Reference, ScatterChart
import pathlib
import scripts
from varname import nameof

import common_parameters_ftm as cm_pmt_ftm
import want_test_band as wt
from loss_table import loss_table

fileConfig('logging.ini')
logger = logging.getLogger()

class CMW100:
    def __init__(self):
        self.begin()
        self.get_resource()

    def begin(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 230400
        self.ser.timeout = 0.15
        self.ser.port = self.get_comport_wanted()
        self.com_open()


    def com_open(self):
        try:
            self.ser.open()
            logger.info('open modem comport')
        except:
            logger.info('check the comport is locked or drop comport')

    def com_close(self):
        self.ser.close()

    def get_resource(self):
        self.cmw100 = pyvisa.ResourceManager().open_resource('TCPIP0::127.0.0.1::INSTR')
        self.cmw100.timeout = 5000
        logger.info('Connect to CMW100')
        logger.info('TCPIP0::127.0.0.1::INSTR')

    def preset_instrument_lte(self):
        logger.info('----------Preset CMW100----------')
        self.command_cmw100_write('CONFigure:FDCorrection:DEACtivate RFAC')
        self.command_cmw100_write('CONFigure:BASE:FDCorrection:CTABle:DELete:ALL')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('*RST')
        self.command_cmw100_query('*OPC?')

    @staticmethod
    def get_comport_wanted():
        comports = serial.tools.list_ports.comports()
        comport_waned = None
        for comport in comports:
            if 'Modem' in comport.description:
                comport_waned = comport.name
                logger.info(f'Modem comport is: {comport_waned}')
        return comport_waned

    def get_loss(self, freq):
        want_loss = None
        for f in loss_table.keys():
            if freq > f*1000:
                want_loss = loss_table[f]
            elif f*1000 > freq:
                break
        return want_loss

    def set_test_mode_lte(self, band_lte):
        logger.info('----------Set Test Mode----------')
        self.command(f'AT+LRFFINALSTART=1,{band_lte}')
        self.command(f'AT+LMODETEST')


    def set_test_end_lte(self):
        logger.info('----------Set End----------')
        self.command(f'AT+LRFFINALFINISH')

    def sig_gen_lte(self, band_lte, rx_freq_lte, bw_lte, rx_loss, rx_level=-70):
        logger.info('----------Sig Gen----------')
        self.command_cmw100_query('SYSTem:BASE:OPTion:VERSion?  "CMW_NRSub6G_Meas"')
        self.command_cmw100_write('ROUT:GPRF:GEN:SCEN:SAL R118, TX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:LIST OFF')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:EATT {rx_loss}')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:BBM ARB')
        self.command_cmw100_query('*OPC?')
        if band_lte in [34, 38, 39, 40, 41, 42, 48]:
            self.command_cmw100_write(f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_Channel_CC0_RxAnt0_RF_Verification_10M_SIMO_01.wv'")
        else:
            self.command_cmw100_write(f"SOUR:GPRF:GEN1:ARB:FILE 'C:\CMW100_WV\SMU_NodeB_Ant0_FRC_10MHz.wv'")
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_query('SOUR:GPRF:GEN1:ARB:FILE?')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:FREQ {rx_freq_lte}KHz')
        self.command_cmw100_write(f'SOUR:GPRF:GEN1:RFS:LEV {rx_level}.000000')
        self.command_cmw100_query('SOUR:GPRF:GEN1:STAT?')
        self.command_cmw100_write('SOUR:GPRF:GEN1:STAT ON')
        self.command_cmw100_query('*OPC?')

    def sync_lte(self, rx_freq_lte, sync_path=0, sync_mode=0):
        logger.info('---------Sync----------')
        self.command(f'AT+LSYNC={sync_path},{sync_mode},{rx_freq_lte}',delay=1.2)

    def tx_set_lte(self, tx_path, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level):
        """
        :param tx_path: TX1: 0 (main path)| TX2: 1 (sub path)
        :param bw_lte: 1.4: 0 | 3: 1 | 5: 2 | 10: 3 | 15: 4 | 20: 5
        :param tx_freq_lte:
        :param rb_num:
        :param rb_start:
        :param mcs: "QPSK": 0 | "Q16": 11 | "Q64": 25 | "Q256": 27
        :param pwr:
        :return:
        """
        logger.info('---------Tx Set----------')
        tx_path_dict = {
            'TX1': 0,
            'TX2': 1,
        }

        bw_dict = {
            1.4: 0,
            3: 1,
            5: 2,
            10: 3,
            15: 4,
            20: 5,
        }

        mcs_dict = {
            'QPSK': 0,
            'Q16': 11,
            'Q64': 25,
            'Q256': 27,
        }

        self.command(f'AT+LTXSENDREQ={tx_path_dict[tx_path]},{bw_dict[bw_lte]},{tx_freq_lte},{rb_num},{rb_start},{mcs_dict[mcs]},2,1,{tx_level}')
        logger.info(f'TX_PATH: {tx_path}, BW: {bw_lte}, TX_FREQ: {tx_freq_lte}, RB_SIZE: {rb_num}, RB_OFFSET: {rb_start}, MCS: {mcs}, TX_LEVEL: {tx_level}')

    def antenna_switch(self, on_off=0):  # AS ON: 1, AS OFF: 0
        logger.info('---------Antenna Switch----------')
        self.command(f'AT+LTXASTUNESET={on_off}')
        if on_off == 0:
            logger.info('Antenna Switch OFF')
        elif on_off == 1:
            logger.info('Antenna Switch ON')

    def antenna_switch_v2(self, tech, ant_path=0):
        """
        this is to place on the first to activate
        AT+ANTSWSEL=P0,P1	//Set Tx DPDT switch
        P0: RAT (0=GSM, 1=WCDMA, 2=LTE, 4=CDMA, 6=NR)
        P1: ANT path (0=default, 1=switched, 4=dynamic mode),
        P1 (P0=NR): ANT Path (0=Tx-Ant1, 1=Tx-Ant2, 2=Tx-Ant3, 3=Tx-Ant4, 4=dynamic switch mode)
        :param tech:
        :param ant_path:
        :return:
        """
        tech_dict = {
            'GSM': 0,
            'WCDMA': 1,
            'LTE': 2,
            'NR': 6,
        }

        self.command(f'AT+ANTSWSEL={tech_dict[tech]},{ant_path}')
        logger.info(f'RAT: {tech}, ANT_PATH: {ant_path}')


    def tx_measure(self, band_lte, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_loss):
        logger.info('---------Tx Measure----------')

        mode = 'TDD' if band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
        self.command_cmw100_write(f'CONF:LTE:MEAS:DMODe {mode}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:BAND OB{band_lte}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:FREQ {tx_freq_lte}KHz')
        self.command_cmw100_query('*OPC?')
        rb = f'0{bw_lte*10}' if bw_lte < 10 else f'{bw_lte*10}'
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CBAN B{rb}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOD:MSCH {mcs}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:NRB {rb_num}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:ORB {rb_start}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CPR NORM')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:PLC 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:DSSP 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO OFF')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOEX ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN100 ON,0MHz,1MHz,-18,K030')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN100 ON,1MHz,2.5MHz,-10,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN100 ON,2.5MHz,2.8MHz,-10,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN100 ON,2.8MHz,5MHz,-10,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN100 ON,5MHz,6MHz,-13,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN100 ON,6MHz,10MHz,-13,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN100 ON,10MHz,15MHz,-25,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN100 OFF,15MHz,15MHz,-25,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN100 OFF,15MHz,15MHz,-25,M1')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {tx_level+5}.00')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R11, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:ACLR 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:SEM 5')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
        self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:SCEN:ACT SAL')
        self.command_cmw100_query('SYST:ERR:ALL?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{rf_port}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{rf_port}, RX1')
        self.command_cmw100_query('*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {tx_loss}')
        self.command_cmw100_query('*OPC?')
        time.sleep(0.2)
        mod_results = self.command_cmw100_query('READ:LTE:MEAS:MEV:MOD:AVER?')  # P3 is EVM, P15 is Ferr, P14 is IQ Offset
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, IQ_OFFSET: {mod_results[2]:.2f}')
        self.command_cmw100_write(f'INIT:LTE:MEAS:MEV')
        self.command_cmw100_query('*OPC?')
        f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
        while f_state != 'RDY':
            time.sleep(0.2)
            f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
        aclr_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:ACLR:AVER?')
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr)*-1 if eval(aclr) > 30 else eval(aclr) for aclr in aclr_results]  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2
        logger.info(f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        iem_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:IEM:MARG?')
        iem_results = iem_results.split(',')
        logger.info(f'InBandEmissions Margin: {eval(iem_results[2]):.2f}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        esfl_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:ESFL:EXTR?')
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]),2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]),2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
        time.sleep(0.2)
        # logger.info(f'ESFL results: {esfl_results}')
        sem_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:MARG?')
        logger.info(f'SEM_MARG results: {sem_results}')
        sem_avg_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:AVER?')
        sem_avg_results = sem_avg_results.split(',')
        logger.info(f'OBW: {eval(sem_avg_results[2])/1000000:.3f} MHz, Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
        # logger.info(f'SEM_AVER results: {sem_avg_results}')
        self.command_cmw100_write(f'STOP:LTE:MEAS:MEV')
        self.command_cmw100_query('*OPC?')

        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def tx_power_relative_test_export_excel(self, data, band_lte, bw_lte, tx_freq_level_lte):
        """
        data is dict like:
        tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET]
        """
        logger.info('----------save to excel----------')
        filename = None
        if self.script == 'GENERAL':
            if tx_freq_level_lte >= 100:
                filename = f'relative power_{bw_lte}MHZ_LTE.xlsx'
            elif tx_freq_level_lte <= 100:
                filename = f'TxP_ACLR_EVM_{bw_lte}MHZ_LTE.xlsx'


            if pathlib.Path(filename).exists() is False:
                logger.info('----------file does not exist----------')
                wb = openpyxl.Workbook()
                wb.remove(wb['Sheet'])
                # to create sheet
                for mcs in ['QPSK', 'Q16', 'Q64', 'Q256']:  # some cmw10 might not have licesnse of Q256
                    wb.create_sheet(f'Raw_Data_{mcs}_PRB')
                    wb.create_sheet(f'Raw_Data_{mcs}_FRB')

                for sheetname in wb.sheetnames:
                    ws = wb[sheetname]
                    ws['A1'] = 'Band'
                    ws['B1'] = 'Tx_Freq'
                    ws['C1'] = 'Tx_level'
                    ws['D1'] = 'Measured_Power'
                    ws['E1'] = 'E_-1'
                    ws['F1'] = 'E_+1'
                    ws['G1'] = 'U_-1'
                    ws['H1'] = 'U_+1'
                    ws['I1'] = 'U_-2'
                    ws['J1'] = 'U_+2'
                    ws['K1'] = 'EVM'
                    ws['L1'] = 'Freq_Err'
                    ws['M1'] = 'IQ_OFFSET'
                    ws['N1'] = 'RB_num'
                    ws['O1'] = 'RB_start'
                    ws['P1'] = 'MCS'

                wb.save(filename)
                wb.close()

            logger.info('----------file exist----------')
            wb = openpyxl.load_workbook(filename)
            if self.rb_state == 'PRB':
                ws = wb[f'Raw_Data_{self.mcs}_{self.rb_state}']
            else:
                ws = wb[f'Raw_Data_{self.mcs}_{self.rb_state}']

            max_row = ws.max_row
            row = max_row + 1
            if tx_freq_level_lte >= 100:
                for tx_level, measured_data in data.items():
                    ws.cell(row, 1).value = band_lte
                    ws.cell(row, 2).value = tx_freq_level_lte  # this tx_freq_lte
                    ws.cell(row, 3).value = tx_level
                    ws.cell(row, 4).value = measured_data[3]
                    ws.cell(row, 5).value = measured_data[2]
                    ws.cell(row, 6).value = measured_data[4]
                    ws.cell(row, 7).value = measured_data[1]
                    ws.cell(row, 8).value = measured_data[5]
                    ws.cell(row, 9).value = measured_data[0]
                    ws.cell(row, 10).value = measured_data[6]
                    ws.cell(row, 11).value = measured_data[7]
                    ws.cell(row, 12).value = measured_data[8]
                    ws.cell(row, 13).value = measured_data[9]
                    ws.cell(row, 14).value = self.rb_num
                    ws.cell(row, 15).value = self.rb_start
                    ws.cell(row, 16).value = self.mcs

                    row += 1

            elif tx_freq_level_lte <= 100:
                for tx_freq_lte, measured_data in data.items():
                    ws.cell(row, 1).value = band_lte
                    ws.cell(row, 2).value = tx_freq_lte
                    ws.cell(row, 3).value = tx_freq_level_lte  # this tx_level
                    ws.cell(row, 4).value = measured_data[3]
                    ws.cell(row, 5).value = measured_data[2]
                    ws.cell(row, 6).value = measured_data[4]
                    ws.cell(row, 7).value = measured_data[1]
                    ws.cell(row, 8).value = measured_data[5]
                    ws.cell(row, 9).value = measured_data[0]
                    ws.cell(row, 10).value = measured_data[6]
                    ws.cell(row, 11).value = measured_data[7]
                    ws.cell(row, 12).value = measured_data[8]
                    ws.cell(row, 13).value = measured_data[9]
                    ws.cell(row, 14).value = self.rb_num
                    ws.cell(row, 15).value = self.rb_start
                    ws.cell(row, 16).value = self.mcs

                    row += 1

            wb.save(filename)
            wb.close()

            return filename



    def tx_power_relative_test_initial(self, band_lte, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_loss):
        logger.info('----------Relatvie test initial----------')
        mode = 'TDD' if band_lte in [38, 39, 40, 41, 42, 48] else 'FDD'
        self.command_cmw100_write(f'CONF:LTE:MEAS:DMODe {mode}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:BAND OB{band_lte}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:FREQ {tx_freq_lte}KHz')
        self.command_cmw100_query(f'*OPC?')
        rb = f'0{bw_lte * 10}' if bw_lte < 10 else f'{bw_lte * 10}'
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CBAN B{rb}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOD:MSCH {mcs}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:NRB {rb_num}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:ORB {rb_start}')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:CPR NORM')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:PLC 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:DSSP 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO OFF')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MOEX ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM1:CBAN100 ON,0MHz,1MHz,-18,K030')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM2:CBAN100 ON,1MHz,2.5MHz,-10,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM3:CBAN100 ON,2.5MHz,2.8MHz,-10,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM4:CBAN100 ON,2.8MHz,5MHz,-10,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM5:CBAN100 ON,5MHz,6MHz,-13,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM6:CBAN100 ON,6MHz,10MHz,-13,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM7:CBAN100 ON,10MHz,15MHz,-25,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM8:CBAN100 OFF,15MHz,15MHz,-25,M1')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:LIM:SEM:LIM9:CBAN100 OFF,15MHz,15MHz,-25,M1')
        self.command_cmw100_query(f'SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONFigure:LTE:MEAS:MEValuation:MSLot ALL')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {tx_level+5}')
        self.command_cmw100_write(f'ROUT:LTE:MEAS:SCEN:SAL R1{rf_port}, RX1')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:MOD 5')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:ACLR 5')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:SCO:SPEC:SEM 5')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f"TRIG:LTE:MEAS:MEV:SOUR 'GPRF Gen1: Restart Marker'")
        self.command_cmw100_write(f'TRIG:LTE:MEAS:MEV:THR -20.0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:REP SING')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:RES:ALL ON, ON, ON, ON, ON, ON, ON, ON, ON, ON')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:MEV:MSUB 2, 10, 0')
        self.command_cmw100_write(f'CONF:LTE:MEAS:SCEN:ACT SAL')
        self.command_cmw100_query(f'SYST:ERR:ALL?')
        self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:EATT {tx_loss}')
        self.command_cmw100_query(f'*OPC?')
        self.command_cmw100_write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{rf_port}, RX1')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:SCO 2')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:REP SING')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:LIST OFF')
        self.command_cmw100_write(f"TRIGger:GPRF:MEAS:POWer:SOURce 'Free Run'")
        self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:TRIG:SLOP REDG')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:SLEN 5.0e-3')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:POW:MLEN 8.0e-4')
        self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3')
        self.command_cmw100_write(f'TRIG:GPRF:MEAS:POW:MODE ONCE')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:UMAR 10.000000')
        self.command_cmw100_write(f'CONF:GPRF:MEAS:RFS:ENP 29.00')

    def tx_power_aclr_evm_lmh_pipeline_lte(self):
        for tech in wt.tech:
            if tech == 'LTE' and wt.lte_bands != []:
                for tx_path in wt.tx_path:
                    for bw in wt.lte_bandwidths:
                        try:
                            for band in wt.lte_bands:
                                if bw in cm_pmt_ftm.bandwidths_selected(band):
                                    self.tx_power_aclr_evm_lmh_lte(band, bw, wt.tx_level, wt.port_lte, wt.channel, tx_path, plot=False)
                                else:
                                    logger.info(f'B{band} does not have BW {bw}MHZ')
                            self.txp_aclr_evm_plot(self.filename)
                        except AttributeError:
                            logger.info(f'there is no data to plot because the band does not have this BW ')

    def tx_power_relative_test_freq_pipeline_lte(self):
        for tech in wt.tech:
            if tech == 'LTE' and wt.lte_bands != []:
                for tx_path in wt.tx_path:
                    for bw in wt.lte_bandwidths:
                        try:
                            for band in wt.lte_bands:
                                if bw in cm_pmt_ftm.bandwidths_selected(band):
                                    # default setting is FRB and GENERAL
                                    self.script = 'GENERAL'  # force set self.script = 'GENERAL'
                                    self.rb_state = 'PRB'  # force set self.script = 'PRB'
                                    self.mcs = 'QPSK'  # force set self.mcs = 'QPSK'
                                    rb_num, rb_start = scripts.GENERAL_LTE[bw][0]  # 0: PRB, # 1: FRB
                                    self.rb_num = rb_num
                                    self.rb_start = rb_start
                                    self.tx_power_relative_test_freq_progress(band, bw, self.rb_num, self.rb_start, self.mcs, 26, wt.port_lte, tx_path, plot=False)
                                else:
                                    logger.info(f'B{band} does not have BW {bw}MHZ')
                            self.txp_aclr_evm_plot(self.filename)
                        except AttributeError:
                            logger.info(f'there is no data to plot because the band does not have this BW ')


    def tx_power_aclr_evm_lmh_lte(self, band_lte, bw_lte, tx_level, rf_port, freq_select, tx_path='TX1', plot=True):
        """
        order: tx_path > bw > band > mcs > rb > chan
        :param band_lte:
        :param bw_lte:
        :param tx_level:
        :param rf_port:
        :param freq_select: 'LMH'
        :param tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', band_lte, bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        # tx_freq_lte_mch = cm_pmt_ftm.transfer_freq_rx2tx_lte(band_lte, rx_freq_list[1])  # M_tx_freq
        rx_loss = self.get_loss(rx_freq_list[1])
        tx_loss = self.get_loss(cm_pmt_ftm.transfer_freq_rx2tx_lte(band_lte, rx_freq_list[1]))
        logger.info('----------Test LMH progress---------')
        self.preset_instrument_lte()
        self.set_test_end_lte()
        self.antenna_switch_v2('LTE')
        self.set_test_mode_lte(band_lte)
        self.sig_gen_lte(band_lte, rx_freq_list[1], bw_lte, rx_loss)
        self.sync_lte(rx_freq_list[1])

        freq_list = []
        for freq in freq_select:
            if freq == 'L':
                freq_list.append(cm_pmt_ftm.transfer_freq_rx2tx_lte(band_lte, rx_freq_list[0]))
            elif freq == 'M':
                freq_list.append(cm_pmt_ftm.transfer_freq_rx2tx_lte(band_lte, rx_freq_list[1]))
            elif freq == 'H':
                freq_list.append(cm_pmt_ftm.transfer_freq_rx2tx_lte(band_lte, rx_freq_list[2]))

        for mcs in wt.mcs:
            self.mcs = mcs
            for script in wt.scripts:
                if script == 'GENERAL':
                    self.script = 'GENERAL'
                    for num, rb_set in enumerate(scripts.GENERAL_LTE[bw_lte]):
                        rb_num, rb_start = rb_set
                        self.rb_num = rb_num
                        self.rb_start = rb_start
                        self.rb_state = 'PRB' if num == 0 else 'FRB'
                        data_freq = {}
                        for tx_freq_lte in freq_list:
                            self.tx_set_lte(tx_path, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level)
                            aclr_mod_results = self.tx_measure(band_lte, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_loss)
                            logger.debug(aclr_mod_results)
                            data_freq[tx_freq_lte] = aclr_mod_results
                        logger.debug(data_freq)
                        # ready to export to excel
                        self.filename = self.tx_power_relative_test_export_excel(data_freq, band_lte, bw_lte, tx_level)

        self.set_test_end_lte()
        if plot == True:
            self.txp_aclr_evm_plot(self.filename)
        else:
            pass


    def tx_power_relative_test_freq_progress(self, band_lte, bw_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_path='TX1', plot=True):
        """
        :param band_lte:
        :param bw_lte:
        :param tx_freq_lte:
        :param rb_num:
        :param rb_start:
        :param mcs:
        :param tx_level:
        :param rf_port:
        :param freq_range_list: [freq_level_1, freq_level_2, freq_step]
        :param tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        logger.info('----------Relatvie test freq progress ---------')
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', band_lte, bw_lte)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(band_lte, rx_freq) for rx_freq in rx_freq_list]
        rx_loss = self.get_loss(rx_freq_list[1])
        tx_loss = self.get_loss(cm_pmt_ftm.transfer_freq_tx2rx_lte(band_lte, rx_freq_list[1]))
        self.preset_instrument_lte()
        self.set_test_end_lte()
        self.antenna_switch_v2('LTE')
        self.set_test_end_lte()
        self.set_test_mode_lte(band_lte)
        self.sig_gen_lte(band_lte, rx_freq_list[1], bw_lte, rx_loss)
        self.sync_lte(rx_freq_list[1])

        # freq_range_list = [tx_freq_list[0], tx_freq_list[2], int((tx_freq_list[2] - tx_freq_list[0])/10)]
        freq_range_list = [tx_freq_list[0], tx_freq_list[2], 1000]
        step = freq_range_list[2]

        data = {}
        for tx_freq_lte in range(freq_range_list[0], freq_range_list[1] + step, step):
            self.tx_set_lte(tx_path, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level)
            aclr_mod_results = self.tx_measure(band_lte, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_loss)

            logger.debug(aclr_mod_results)
            data[tx_freq_lte] = aclr_mod_results

        self.set_test_end_lte()
        logger.debug(data)

        self.filename = self.tx_power_relative_test_export_excel(data, band_lte, bw_lte, tx_level)
        if plot == True:
            self.txp_aclr_evm_plot(self.filename)
        else:
            pass


    def tx_power_relative_test_progress(self, band_lte, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_range_list, tx_path='TX1'):
        """
        :param band_lte:
        :param bw_lte:
        :param tx_freq_lte:
        :param rb_num:
        :param rb_start:
        :param mcs:
        :param pwr:
        :param rf_port:
        :param loss:
        :param tx_range_list: [tx_level_1, tx_level_2]
        :param tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """

        tx_loss = self.get_loss(tx_freq_lte)
        rx_loss = self.get_loss(cm_pmt_ftm.transfer_freq_tx2rx_lte(band_lte, rx_freq_lte))
        self.preset_instrument_lte()
        self.set_test_end_lte()
        self.antenna_switch_v2('LTE')
        self.set_test_mode_lte(band_lte)
        self.sig_gen_lte(band_lte, cm_pmt_ftm.transfer_freq_tx2rx_lte(band_lte, tx_freq_lte), bw_lte, rx_loss)
        self.sync_lte(cm_pmt_ftm.transfer_freq_tx2rx_lte(band_lte, tx_freq_lte))
        self.tx_set_lte(tx_path, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level)

        self.tx_power_relative_test_initial(band_lte, bw_lte, tx_freq_lte, rb_num, rb_start, mcs, tx_level, rf_port, tx_loss)
        logger.info('----------Relatvie test progress---------')
        logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

        step = -1 if tx_range_list[0] > tx_range_list[1] else 1

        data = {}
        for tx_level in range(tx_range_list[0], tx_range_list[1]+step, step):
            logger.info(f'========Now Tx level = {tx_level} dBm========')
            self.command(f'AT+LTXPWRLVLSET={tx_level}')
            self.command(f'AT+LTXCHNSDREQ')
            self.command_cmw100_write('CONF:LTE:MEAS:RFS:UMAR 15.000000')
            self.command_cmw100_write(f'CONF:LTE:MEAS:RFS:ENP {tx_level + 5}.00')
            mod_results = self.command_cmw100_query(f'READ:LTE:MEAS:MEV:MOD:AVER?')
            mod_results = mod_results.split(',')
            mod_results = [mod_results[3], mod_results[15], mod_results[14]]
            mod_results = [eval(m) for m in mod_results]
            logger.info(f'mod_results = {mod_results}')
            self.command_cmw100_write('INIT:LTE:MEAS:MEV')
            self.command_cmw100_query('*OPC?')
            f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
            while f_state != 'RDY':
                time.sleep(0.2)
                f_state = self.command_cmw100_query('FETC:LTE:MEAS:MEV:STAT?')
            aclr_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:ACLR:AVER?')
            aclr_results = aclr_results.split(',')[1:]
            aclr_results = [eval(aclr) * -1 if eval(aclr) > 30 else eval(aclr) for aclr in
                            aclr_results]  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2
            logger.info(
                f'Power: {aclr_results[3]:.2f}, E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
            iem_results = self.command_cmw100_query('FETC:LTE:MEAS:MEV:IEM:MARG?')
            iem_results = iem_results.split(',')
            logger.info(f'InBandEmissions Margin: {eval(iem_results[2]):.2f}dB')
            # logger.info(f'IEM_MARG results: {iem_results}')
            esfl_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:ESFL:EXTR?')
            esfl_results = esfl_results.split(',')
            logger.info(
                f'Equalize Spectrum Flatness: Ripple1:{eval(esfl_results[2]):.2f} dBpp, Ripple2:{esfl_results[3]} dBpp')
            time.sleep(0.2)
            # logger.info(f'ESFL results: {esfl_results}')
            sem_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:MARG?')
            logger.info(f'SEM_MARG results: {sem_results}')
            sem_avg_results = self.command_cmw100_query(f'FETC:LTE:MEAS:MEV:SEM:AVER?')
            sem_avg_results = sem_avg_results.split(',')
            logger.info(
                f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
            # logger.info(f'SEM_AVER results: {sem_avg_results}')
            self.command_cmw100_write(f'STOP:LTE:MEAS:MEV')
            self.command_cmw100_query('*OPC?')

            logger.debug(aclr_results + mod_results)
            data[tx_level] = aclr_results + mod_results

        self.set_test_end_lte()
        logger.debug(data)

        filename = self.tx_power_relative_test_export_excel(data, band_lte, bw_lte, tx_freq_lte)

    def txp_aclr_evm_plot(self, filename):
        logger.info('----------Plot Chart---------')
        wb = openpyxl.load_workbook(filename)
        if self.script == 'GENERAL':
            for ws_name in wb.sheetnames:
                ws = wb[ws_name]

                if ws._charts != []:  # if there is charts, delete it
                    ws._charts.clear()


                logger.info('----------Power---------')
                chart = LineChart()
                chart.title = 'Power'
                chart.y_axis.title = 'Power(dBm)'
                chart.x_axis.title = 'Band'
                chart.x_axis.tickLblPos = 'low'

                chart.height = 20
                chart.width = 32

                y_data = Reference(ws, min_col=4, min_row=1, max_col=4, max_row=ws.max_row)
                x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                chart.add_data(y_data, titles_from_data=True)
                chart.set_categories(x_data)

                chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                chart.series[0].marker.size = 10


                ws.add_chart(chart, "R1")


                logger.info('----------ACLR---------')
                chart = LineChart()
                chart.title = 'ACLR'
                chart.y_axis.title = 'ACLR(dB)'
                chart.x_axis.title = 'Band'
                chart.x_axis.tickLblPos = 'low'
                chart.y_axis.scaling.min = -60
                chart.y_axis.scaling.max = -20

                chart.height = 20
                chart.width = 32

                y_data = Reference(ws, min_col=5, min_row=1, max_col=10, max_row=ws.max_row)
                x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                chart.add_data(y_data, titles_from_data=True)
                chart.set_categories(x_data)

                chart.series[0].marker.symbol = 'triangle'  # for EUTRA_-1
                chart.series[0].marker.size = 10
                chart.series[1].marker.symbol = 'circle'  # for EUTRA_+1
                chart.series[1].marker.size = 10
                chart.series[2].graphicalProperties.line.width = 50000  # for UTRA_-1
                chart.series[3].graphicalProperties.line.width = 50000  # for UTRA_+1
                chart.series[4].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_-2
                chart.series[5].graphicalProperties.line.dashStyle = 'dash'  # for UTRA_+2

                ws.add_chart(chart, "R39")

                logger.info('----------EVM---------')
                chart = LineChart()
                chart.title = 'EVM'
                chart.y_axis.title = 'EVM(%)'
                chart.x_axis.title = 'Band'
                chart.x_axis.tickLblPos = 'low'

                chart.height = 20
                chart.width = 32

                y_data = Reference(ws, min_col=11, min_row=1, max_col=11, max_row=ws.max_row)
                x_data = Reference(ws, min_col=1, min_row=2, max_col=2, max_row=ws.max_row)
                chart.add_data(y_data, titles_from_data=True)
                chart.set_categories(x_data)

                chart.series[0].marker.symbol = 'circle'  # for EUTRA_+1
                chart.series[0].marker.size = 10

                ws.add_chart(chart, "R77")

            wb.save(filename)
            wb.close()


    def command_cmw100_query(self, tcpip_command):
        tcpip_response = self.cmw100.query(tcpip_command).strip()
        logger.info(f'TCPIP::<<{tcpip_command}')
        logger.info(f'TCPIP::>>{tcpip_response}')
        return tcpip_response

    def command_cmw100_write(self, tcpip_command):
        self.cmw100.write(tcpip_command)
        logger.info(f'TCPIP::<<{tcpip_command}')


    def command(self, command='at', delay=0.1):
        logger.info(f'MTM: <<{command}')
        command = command + '\r'
        self.ser.write(command.encode())
        time.sleep(delay)
        response = self.ser.readlines()
        for res in response:
            r = res.decode().split()
            if len(r) > 1:  # with more than one response
                for rr in r:
                    logger.info(f'MTM: >>{rr}')
            else:
                if r == []:  # sometimes there is not \r\n in the middle response
                    continue
                else:  # only one response
                    logger.info(f'MTM: >>{r[0]}')

        # logger.info('OK is not at the end, so repeat again')
        # while 'OK' not in response:
        #     time.sleep(0.1)
        #     response = self.ser.readlines()
        #     for res in response:
        #         r = res.decode().split()
        #         if len(r) > 1:  # with more than one response
        #             for rr in r:
        #                 logger.info(f'MTM: >>{rr}')
        #         else:
        #             if r == []:  # sometimes there is not \r\n in the middle response
        #                 continue
        #             else:  # only one response
        #                 logger.info(f'MTM: >>{r[0]}')


def main():
    start = datetime.datetime.now()
    cmw100 = CMW100()

    # cmw100.antenna_switch_v2('LTE')
    # cmw100.set_test_end_lte()
    # cmw100.set_test_mode_lte(1)
    # cmw100.sig_gen_lte(band_lte, rx_freq_lte, bw_lte, loss)
    # cmw100.sync_lte(rx_freq_lte)
    # cmw100.tx_set_lte('TX1', 10, tx_freq_lte, 50, 0, 'QPSK', 24)
    # cmw100.tx_measure(band_lte, bw, tx_freq_lte, 50, 0, 'QPSK', 24, 1, 0.8)
    # cmw100.preset_instrument_lte()
    # cmw100.tx_power_relative_test_progress(band_lte, bw_lte, tx_freq_lte, 50, 0, 'QPSK', 25, rf_port, loss, [0, 25])

    # cmw100.tx_power_relative_test_freq_progress(band_lte, bw_lte, tx_freq_lte[1], 50, 0, 'QPSK', 25, rf_port, loss, [tx_freq_lte[0], tx_freq_lte[2], int((tx_freq_lte[2] - tx_freq_lte[0])/2)])
    # cmw100.tx_power_aclr_evm_lmh_lte(band_lte, bw_lte, 50, 0, 'QPSK', 25, rf_port, 0.8, 'LMH',)
    # cmw100.tx_power_aclr_evm_lmh_pipeline_lte()
    cmw100.tx_power_relative_test_freq_pipeline_lte()
    stop = datetime.datetime.now()

    logger.info(f'Timer: {stop - start}')


if __name__ == '__main__':
    main()