#!/usr/bin/python3
import pathlib
import tkinter.ttk as ttk
import pygubu
import datetime
import logging
from logging.config import fileConfig
import threading

import ui_init

fileConfig('logging.ini')
logger = logging.getLogger()

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "main.ui"


class MainApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("toplevel2", master)

        self.instrument = None
        self.tx = None
        self.rx = None
        self.rx_sweep = None
        self.chan_L = None
        self.chan_M = None
        self.chan_H = None
        self.tech_LTE = None
        self.tech_WCDMA = None
        self.tech_GSM = None
        self.tech_HSUPA = None
        self.tech_HSDPA = None
        self.B5 = None
        self.B8 = None
        self.B12 = None
        self.B13 = None
        self.B14 = None
        self.B17 = None
        self.B18 = None
        self.B19 = None
        self.B20 = None
        self.B26 = None
        self.B28 = None
        self.B29 = None
        self.B32 = None
        self.B71 = None
        self.LB_all = None
        self.B21 = None
        self.B1 = None
        self.B2 = None
        self.B3 = None
        self.B4 = None
        self.B7 = None
        self.B30 = None
        self.B25 = None
        self.B66 = None
        self.B39 = None
        self.B40 = None
        self.B38 = None
        self.B41 = None
        self.MHB_all = None
        self.B42 = None
        self.B48 = None
        self.UHB_all = None
        self.W1 = None
        self.W2 = None
        self.WCDMA_all = None
        self.W4 = None
        self.W5 = None
        self.W8 = None
        self.W6 = None
        self.W19 = None
        self.GSM850 = None
        self.GSM900 = None
        self.GSM_all = None
        self.GSM1800 = None
        self.GSM1900 = None
        self.U1 = None
        self.U2 = None
        self.HSUPA_all = None
        self.U4 = None
        self.U5 = None
        self.U8 = None
        self.U6 = None
        self.U19 = None
        self.D1 = None
        self.D2 = None
        self.HSDPA_all = None
        self.D4 = None
        self.D5 = None
        self.D8 = None
        self.D6 = None
        self.D19 = None
        self.bw1p4 = None
        self.bw3 = None
        self.bw5 = None
        self.bw10 = None
        self.bw15 = None
        self.bw20 = None
        self.TxMax = None
        self.TxLow = None
        builder.import_variables(
            self,
            [
                "instrument",
                "tx",
                "rx",
                "rx_sweep",
                "chan_L",
                "chan_M",
                "chan_H",
                "tech_LTE",
                "tech_WCDMA",
                "tech_GSM",
                "tech_HSUPA",
                "tech_HSDPA",
                "B5",
                "B8",
                "B12",
                "B13",
                "B14",
                "B17",
                "B18",
                "B19",
                "B20",
                "B26",
                "B28",
                "B29",
                "B32",
                "B71",
                "LB_all",
                "B21",
                "B1",
                "B2",
                "B3",
                "B4",
                "B7",
                "B30",
                "B25",
                "B66",
                "B39",
                "B40",
                "B38",
                "B41",
                "MHB_all",
                "B42",
                "B48",
                "UHB_all",
                "W1",
                "W2",
                "WCDMA_all",
                "W4",
                "W5",
                "W8",
                "W6",
                "W19",
                "GSM850",
                "GSM900",
                "GSM_all",
                "GSM1800",
                "GSM1900",
                "U1",
                "U2",
                "HSUPA_all",
                "U4",
                "U5",
                "U8",
                "U6",
                "U19",
                "D1",
                "D2",
                "HSDPA_all",
                "D4",
                "D5",
                "D8",
                "D6",
                "D19",
                "bw1p4",
                "bw3",
                "bw5",
                "bw10",
                "bw15",
                "bw20",
                "TxMax",
                "TxLow",

            ],
        )

        builder.connect_callbacks(self)
        # self.init_select()
        self.import_ui_setting()

    def run(self):
        self.mainwindow.mainloop()

    def import_ui_setting(self):
        """
        skip bands_gsm

        """
        logger.info('Import the last setting')
        self.instrument.set(ui_init.instrument)
        self.off_all_reset_tech()
        self.off_all_reset_bw()
        self.off_all_reset_ue_power()
        self.off_all_reset_ch()
        self.tx.set(ui_init.tx)
        self.rx.set(ui_init.rx)
        self.rx_sweep.set(ui_init.rx_sweep)
        self.off_all_reset_GSM()
        self.off_all_reset_HSDPA()
        self.off_all_reset_HSUPA()
        self.off_all_reset_WCDMA()
        self.off_all_reset_LB()
        self.off_all_reset_MHB()
        self.off_all_reset_UHB()

        for band_lte in ui_init.bands_lte:
            if band_lte == 1:
                self.B1.set(band_lte)
            elif band_lte == 2:
                self.B2.set(band_lte)
            elif band_lte == 3:
                self.B3.set(band_lte)
            elif band_lte == 4:
                self.B4.set(band_lte)
            elif band_lte == 5:
                self.B5.set(band_lte)
            elif band_lte == 7:
                self.B7.set(band_lte)
            elif band_lte == 8:
                self.B8.set(band_lte)
            elif band_lte == 12:
                self.B12.set(band_lte)
            elif band_lte == 13:
                self.B13.set(band_lte)
            elif band_lte == 14:
                self.B14.set(band_lte)
            elif band_lte == 17:
                self.B17.set(band_lte)
            elif band_lte == 18:
                self.B18.set(band_lte)
            elif band_lte == 19:
                self.B19.set(band_lte)
            elif band_lte == 20:
                self.B20.set(band_lte)
            elif band_lte == 21:
                self.B21.set(band_lte)
            elif band_lte == 25:
                self.B25.set(band_lte)
            elif band_lte == 26:
                self.B26.set(band_lte)
            elif band_lte == 28:
                self.B28.set(band_lte)
            elif band_lte == 29:
                self.B29.set(band_lte)
            elif band_lte == 30:
                self.B30.set(band_lte)
            elif band_lte == 32:
                self.B32.set(band_lte)
            elif band_lte == 38:
                self.B38.set(band_lte)
            elif band_lte == 39:
                self.B39.set(band_lte)
            elif band_lte == 40:
                self.B40.set(band_lte)
            elif band_lte == 41:
                self.B41.set(band_lte)
            elif band_lte == 42:
                self.B42.set(band_lte)
            elif band_lte == 48:
                self.B48.set(band_lte)
            elif band_lte == 66:
                self.B66.set(band_lte)
            elif band_lte == 71:
                self.B71.set(band_lte)

        for band_wcdma in ui_init.bands_wcdma:
            if band_wcdma == 1:
                self.W1.set(band_wcdma)
            elif band_wcdma == 2:
                self.W2.set(band_wcdma)
            elif band_wcdma == 4:
                self.W4.set(band_wcdma)
            elif band_wcdma == 5:
                self.W5.set(band_wcdma)
            elif band_wcdma == 8:
                self.W8.set(band_wcdma)
            elif band_wcdma == 6:
                self.W6.set(band_wcdma)
            elif band_wcdma == 19:
                self.W19.set(band_wcdma)

        for band_hsupa in ui_init.bands_hsupa:
            if band_hsupa == 1:
                self.U1.set(band_hsupa)
            elif band_hsupa == 2:
                self.U2.set(band_hsupa)
            elif band_hsupa == 4:
                self.U4.set(band_hsupa)
            elif band_hsupa == 5:
                self.U5.set(band_hsupa)
            elif band_hsupa == 8:
                self.U8.set(band_hsupa)
            elif band_hsupa == 6:
                self.U6.set(band_hsupa)
            elif band_hsupa == 19:
                self.U19.set(band_hsupa)

        for band_hsdpa in ui_init.bands_hsdpa:
            if band_hsdpa == 1:
                self.D1.set(band_hsdpa)
            elif band_hsdpa == 2:
                self.D2.set(band_hsdpa)
            elif band_hsdpa == 4:
                self.D4.set(band_hsdpa)
            elif band_hsdpa == 5:
                self.D5.set(band_hsdpa)
            elif band_hsdpa == 8:
                self.D8.set(band_hsdpa)
            elif band_hsdpa == 6:
                self.D6.set(band_hsdpa)
            elif band_hsdpa == 19:
                self.D19.set(band_hsdpa)

        # skip
        # for band_gsm in ui_init.bands_gsm:
        #     if band_gsm == 850:
        #         self.GSM850.set(band_gsm)
        #     elif band_gsm == 900:
        #         self.GSM900.set(band_gsm)
        #     elif band_gsm == 1800:
        #         self.GSM1800.set(band_gsm)
        #     elif band_gsm == 1900:
        #         self.GSM1900.set(band_gsm)

        for tech in ui_init.tech:
            if tech == 'LTE':
                self.tech_LTE.set(True)
            elif tech == 'WCDMA':
                self.tech_WCDMA.set(True)
            elif tech == 'HSUPA':
                self.tech_HSUPA.set(True)
            elif tech == 'HSDPA':
                self.tech_HSDPA.set(True)
            # elif tech == 'GSM':
            #     self.tech_GSM.set(True)

        for bw in ui_init.bw:
            if bw == 1.4:
                self.bw1p4.set(True)
            elif bw == 3:
                self.bw3.set(True)
            elif bw == 5:
                self.bw5.set(True)
            elif bw == 10:
                self.bw10.set(True)
            elif bw == 15:
                self.bw15.set(True)
            elif bw == 20:
                self.bw20.set(True)

        for ue_pwr in ui_init.ue_power:
            if ue_pwr == 1:
                self.TxMax.set(True)
            elif ue_pwr == 0:
                self.TxLow.set(True)

        for ch in ui_init.chan:
            if ch == 'L':
                self.chan_L.set(True)
            elif ch == 'M':
                self.chan_M.set(True)
            elif ch == 'H':
                self.chan_H.set(True)

    def export_ui_setting(self):
        logger.info('Export ui setting')
        tech = self.wanted_tech()
        bw = self.wanted_bw()
        ue_power = self.wanted_ue_pwr()
        bands_lte = self.wanted_band_LTE()
        bands_wcdma = self.wanted_band_WCDMA()
        bands_hsupa = self.wanted_band_HSUPA()
        bands_hsdpa = self.wanted_band_HSDPA()
        bands_gsm = self.wanted_band_GSM()
        instrument = self.instrument.get()
        chan = self.wanted_chan()
        tx, rx, rx_sweep = self.wanted_tx_rx_sweep()

        new_data = []
        with open('ui_init.py', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'bands_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_lte) +'\n'
                    logger.debug('replace band LTE')
                    line = '='.join(temp_list)

                elif 'bands_wcdma' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_wcdma) +'\n'
                    logger.debug('replace band WCDMA')
                    line = '='.join(temp_list)

                elif 'bands_hsupa' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_hsupa) +'\n'
                    logger.debug('replace band HSUPA')
                    line = '='.join(temp_list)

                elif 'bands_hsdpa' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_hsdpa) +'\n'
                    logger.debug('replace band HSDPA')
                    line = '='.join(temp_list)

                elif 'bands_gsm' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_gsm) +'\n'
                    logger.debug('replace band GSM')
                    line = '='.join(temp_list)

                elif 'tech' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tech) +'\n'
                    logger.debug('replace tech setting')
                    line = '='.join(temp_list)

                elif 'bw' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bw) +'\n'
                    logger.debug('replace bw setting')
                    line = '='.join(temp_list)

                elif 'ue_power' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(ue_power) +'\n'
                    logger.debug('replace ue power setting')
                    line = '='.join(temp_list)

                elif 'instrument' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(instrument) + '"' +'\n'
                    logger.debug('replace instrument setting')
                    line = '='.join(temp_list)

                elif 'tx' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tx) +'\n'
                    logger.debug('replace tx setting')
                    line = '='.join(temp_list)

                elif 'rx ' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rx) +'\n'
                    logger.debug('replace rx setting')
                    line = '='.join(temp_list)

                elif 'rx_sweep' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rx_sweep) +'\n'
                    logger.debug('replace rx_sweep setting')
                    line = '='.join(temp_list)

                elif 'chan' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(chan) + '"' +'\n'
                    logger.debug('replace chan setting')
                    line = '='.join(temp_list)

                new_data.append(line)

        with open('ui_init.py', 'w') as f:
            f.writelines(new_data)

    def off_all_reset_GSM(self):
        self.GSM_all.set(False)
        self.GSM_all_state()

    def off_all_reset_HSDPA(self):
        self.HSDPA_all.set(False)
        self.HSDPA_all_state()

    def off_all_reset_HSUPA(self):
        self.HSUPA_all.set(False)
        self.HSUPA_all_state()

    def off_all_reset_WCDMA(self):
        self.WCDMA_all.set(False)
        self.WCDMA_all_state()

    def off_all_reset_LB(self):
        self.LB_all.set(False)
        self.LB_all_state()

    def off_all_reset_MHB(self):
        self.MHB_all.set(False)
        self.MHB_all_state()

    def off_all_reset_UHB(self):
        self.UHB_all.set(False)
        self.UHB_all_state()

    def thermal_dis(self):
        from thermal_disable import thd
        thd()

    def init_select(self):
        self.instrument.set('Anritsu8820')
        self.bw10.set(True)
        self.tech_LTE.set(True)
        self.tx.set(True)
        self.wanted_tx_rx_sweep()
        self.chan_L.set(True)
        self.chan_M.set(True)
        self.chan_H.set(True)

        logger.info(f'default instrument: {self.instrument.get()}')

    def wanted_band_LTE(self):
        self.band_lte = []

        if self.B1.get() == 1:
            logger.debug(self.B1.get())
            self.band_lte.append(self.B1.get())
        if self.B2.get() == 2:
            logger.debug(self.B2.get())
            self.band_lte.append(self.B2.get())
        if self.B3.get() == 3:
            logger.debug(self.B3.get())
            self.band_lte.append(self.B3.get())
        if self.B4.get() == 4:
            logger.debug(self.B4.get())
            self.band_lte.append(self.B4.get())
        if self.B7.get() == 7:
            logger.debug(self.B7.get())
            self.band_lte.append(self.B7.get())
        if self.B25.get() == 25:
            logger.debug(self.B25.get())
            self.band_lte.append(self.B25.get())
        if self.B66.get() == 66:
            logger.debug(self.B66.get())
            self.band_lte.append(self.B66.get())
        if self.B30.get() == 30:
            logger.debug(self.B30.get())
            self.band_lte.append(self.B30.get())
        if self.B39.get() == 39:
            logger.debug(self.B39.get())
            self.band_lte.append(self.B39.get())
        if self.B40.get() == 40:
            logger.debug(self.B40.get())
            self.band_lte.append(self.B40.get())
        if self.B38.get() == 38:
            logger.debug(self.B38.get())
            self.band_lte.append(self.B38.get())
        if self.B41.get() == 41:
            logger.debug(self.B41.get())
            self.band_lte.append(self.B41.get())
        if self.B5.get() == 5:
            logger.debug(self.B5.get())
            self.band_lte.append(self.B5.get())
        if self.B8.get() == 8:
            logger.debug(self.B8.get())
            self.band_lte.append(self.B8.get())
        if self.B12.get() == 12:
            logger.debug(self.B12.get())
            self.band_lte.append(self.B12.get())
        if self.B13.get() == 13:
            logger.debug(self.B13.get())
            self.band_lte.append(self.B13.get())
        if self.B14.get() == 14:
            logger.debug(self.B14.get())
            self.band_lte.append(self.B14.get())
        if self.B17.get() == 17:
            logger.debug(self.B17.get())
            self.band_lte.append(self.B17.get())
        if self.B18.get() == 18:
            logger.debug(self.B18.get())
            self.band_lte.append(self.B18.get())
        if self.B19.get() == 19:
            logger.debug(self.B19.get())
            self.band_lte.append(self.B19.get())
        if self.B20.get() == 20:
            logger.debug(self.B20.get())
            self.band_lte.append(self.B20.get())
        if self.B21.get() == 21:
            logger.debug(self.B21.get())
            self.band_lte.append(self.B21.get())
        if self.B26.get() == 26:
            logger.debug(self.B26.get())
            self.band_lte.append(self.B26.get())
        if self.B28.get() == 28:
            logger.debug(self.B28.get())
            self.band_lte.append(self.B28.get())
        if self.B29.get() == 29:
            logger.debug(self.B29.get())
            self.band_lte.append(self.B29.get())
        if self.B32.get() == 32:
            logger.debug(self.B32.get())
            self.band_lte.append(self.B32.get())
        if self.B71.get() == 71:
            logger.debug(self.B71.get())
            self.band_lte.append(self.B71.get())
        if self.B42.get() == 42:
            logger.debug(self.B42.get())
            self.band_lte.append(self.B42.get())
        if self.B48.get() == 48:
            logger.debug(self.B48.get())
            self.band_lte.append(self.B48.get())

        if self.band_lte == []:
            logger.debug('Nothing to select for LTE')

        logger.info(f'select LTE band: {self.band_lte}')
        return self.band_lte


    def wanted_band_WCDMA(self):
        self.band_wcdma = []

        if self.W1.get() == 1:
            logger.debug(self.W1.get())
            self.band_wcdma.append(self.W1.get())
        if self.W2.get() == 2:
            logger.debug(self.W2.get())
            self.band_wcdma.append(self.W2.get())
        if self.W4.get() == 4:
            logger.debug(self.W4.get())
            self.band_wcdma.append(self.W4.get())
        if self.W5.get() == 5:
            logger.debug(self.W5.get())
            self.band_wcdma.append(self.W5.get())
        if self.W8.get() == 8:
            logger.debug(self.W8.get())
            self.band_wcdma.append(self.W8.get())
        if self.W6.get() == 6:
            logger.debug(self.W6.get())
            self.band_wcdma.append(self.W6.get())
        if self.W19.get() == 19:
            logger.debug(self.W19.get())
            self.band_wcdma.append(self.W19.get())
        if self.band_wcdma == []:
            logger.debug('Nothing to select for WCDMA')

        logger.info(f'select WCDMA band: {self.band_wcdma}')
        return self.band_wcdma

    def wanted_band_HSUPA(self):
        self.band_hsupa = []

        if self.U1.get() == 1:
            logger.debug(self.U1.get())
            self.band_hsupa.append(self.U1.get())
        if self.U2.get() == 2:
            logger.debug(self.U2.get())
            self.band_hsupa.append(self.U2.get())
        if self.U4.get() == 4:
            logger.debug(self.U4.get())
            self.band_hsupa.append(self.U4.get())
        if self.U5.get() == 5:
            logger.debug(self.U5.get())
            self.band_hsupa.append(self.U5.get())
        if self.U8.get() == 8:
            logger.debug(self.U8.get())
            self.band_hsupa.append(self.U8.get())
        if self.U6.get() == 6:
            logger.debug(self.U6.get())
            self.band_hsupa.append(self.U6.get())
        if self.U19.get() == 19:
            logger.debug(self.U19.get())
            self.band_hsupa.append(self.U19.get())
        if self.band_hsupa == []:
            logger.debug('Nothing to select for WCDMA')

        logger.info(f'select HSUPA band: {self.band_hsupa}')
        return self.band_hsupa

    def wanted_band_HSDPA(self):
        self.band_hsdpa = []

        if self.D1.get() == 1:
            logger.debug(self.D1.get())
            self.band_hsdpa.append(self.D1.get())
        if self.D2.get() == 2:
            logger.debug(self.D2.get())
            self.band_hsdpa.append(self.D2.get())
        if self.D4.get() == 4:
            logger.debug(self.D4.get())
            self.band_hsdpa.append(self.D4.get())
        if self.D5.get() == 5:
            logger.debug(self.D5.get())
            self.band_hsdpa.append(self.D5.get())
        if self.D8.get() == 8:
            logger.debug(self.D8.get())
            self.band_hsdpa.append(self.D8.get())
        if self.D6.get() == 6:
            logger.debug(self.D6.get())
            self.band_hsdpa.append(self.D6.get())
        if self.D19.get() == 19:
            logger.debug(self.D19.get())
            self.band_hsdpa.append(self.D19.get())
        if self.band_hsdpa == []:
            logger.debug('Nothing to select for HSDPA')

        logger.info(f'select HSUPA band: {self.band_hsdpa}')
        return self.band_hsdpa

    def wanted_band_GSM(self):
        pass

    def inst_select(self):
        logger.info(self.instrument.get())
        # return self.instrument.get()

    def wanted_tx_rx_sweep(self):
        self.wanted_test = {}
        self.wanted_test.setdefault('tx', False)
        self.wanted_test.setdefault('rx', False)
        self.wanted_test.setdefault('rx_sweep', False)

        if self.tx.get():
            logger.debug(self.tx.get())
            self.wanted_test['tx'] = self.tx.get()

        if self.rx.get():
            logger.debug(self.rx.get())
            self.wanted_test['rx'] = self.rx.get()

        if self.rx_sweep.get():
            logger.debug(self.rx_sweep.get())
            self.wanted_test['rx_sweep'] = self.rx_sweep.get()

        if self.wanted_test == {}:
            logger.debug('Nothing to select for test items')

        logger.info(self.wanted_test)
        return self.tx.get(), self.rx.get(), self.rx_sweep.get()

    def wanted_ue_pwr(self):
        self.ue_power = []

        if self.TxMax.get():
            logger.debug('TxMax for sensitivity')
            self.ue_power.append(1)

        if self.TxLow.get():
            logger.debug('-10dBm for sensitivity')
            self.ue_power.append(0)

        logger.info(f'select UE Power when sensitivity: {self.ue_power}')
        return self.ue_power

    def wanted_chan(self):
        self.chan = ''

        if self.chan_L.get():
            logger.debug('L chan')
            self.chan += 'L'

        if self.chan_M.get():
            logger.debug('M chan')
            self.chan += 'M'

        if self.chan_H.get():
            logger.debug('H chan')
            self.chan += 'H'

        if self.chan == '':
            logger.debug('Nothing to select for chan')

        logger.info(f'select channel: {self.chan}')
        return self.chan

    def wanted_bw(self):
        self.bw = []

        if self.bw1p4.get():
            logger.debug('Bw_1.4')
            self.bw.append(1.4)

        if self.bw3.get():
            logger.debug('Bw_3')
            self.bw.append(3)

        if self.bw5.get():
            logger.debug('Bw_5')
            self.bw.append(5)

        if self.bw10.get():
            logger.debug('Bw_10')
            self.bw.append(10)

        if self.bw15.get():
            logger.debug('Bw_15')
            self.bw.append(15)

        if self.bw15.get():
            logger.debug('Bw_20')
            self.bw.append(20)

        if self.bw == []:
            logger.debug('Nothing to select for Bw')

        logger.info(f'select BW: {self.bw}')
        return self.bw

    def wanted_tech(self):
        self.tech = []

        if self.tech_LTE.get():
            logger.debug(self.tech_LTE.get())
            self.tech.append('LTE')

        if self.tech_WCDMA.get():
            logger.debug(self.tech_WCDMA.get())
            self.tech.append('WCDMA')

        if self.tech_HSUPA.get():
            logger.debug(self.tech_HSUPA.get())
            self.tech.append('HSUPA')

        if self.tech_HSDPA.get():
            logger.debug(self.tech_HSDPA.get())
            self.tech.append('HSDPA')

        if self.tech_GSM.get():
            logger.debug(self.tech_GSM.get())
            self.tech.append('GSM')

        if self.tech == []:
            logger.debug('Nothing to select for tech')

        logger.info(f'select tech: {self.tech}')
        return self.tech

    def off_all_reset_bw(self):
        self.bw1p4.set(False)
        self.bw3.set(False)
        self.bw5.set(False)
        self.bw10.set(False)
        self.bw20.set(False)

    def off_all_reset_tech(self):
        self.tech_LTE.set(False)
        self.tech_WCDMA.set(False)
        self.tech_HSDPA.set(False)
        self.tech_HSUPA.set(False)
        self.tech_GSM.set(False)

    def off_all_reset_ue_power(self):
        self.TxMax.set(False)
        self.TxLow.set(False)


    def off_all_reset_ch(self):
        self.chan_L.set(False)
        self.chan_M.set(False)
        self.chan_H.set(False)

    def off_all_none_LB(self, event=None):
        self.LB_all.set(False)

    def LB_all_state(self):
        logger.debug(self.LB_all.get())
        if self.LB_all.get():
            logger.debug("LB band all is checked")
            self.B5.set(5)
            self.B8.set(8)
            self.B12.set(12)
            self.B13.set(13)
            self.B14.set(14)
            self.B17.set(17)
            self.B18.set(18)
            self.B19.set(19)
            self.B20.set(20)
            self.B21.set(21)
            self.B26.set(26)
            self.B28.set(28)
            self.B29.set(29)
            self.B32.set(32)
            self.B71.set(71)

        else:
            logger.debug("LB band all is unchecked")
            self.B5.set(0)
            self.B8.set(0)
            self.B12.set(0)
            self.B13.set(0)
            self.B14.set(0)
            self.B17.set(0)
            self.B18.set(0)
            self.B19.set(0)
            self.B20.set(0)
            self.B21.set(0)
            self.B26.set(0)
            self.B28.set(0)
            self.B29.set(0)
            self.B32.set(0)
            self.B71.set(0)

        self.wanted_band_LTE()

    def off_all_none_MHB(self, event=None):
        self.MHB_all.set(False)

    def MHB_all_state(self):
        if self.MHB_all.get():
            logger.debug("MHB band all is checked")
            self.B1.set(1)
            self.B2.set(2)
            self.B25.set(25)
            self.B3.set(3)
            self.B4.set(4)
            self.B66.set(66)
            self.B7.set(7)
            self.B30.set(30)
            self.B39.set(39)
            self.B40.set(40)
            self.B38.set(38)
            self.B41.set(41)

        else:
            logger.debug("MHB band all is unchecked")
            self.B1.set(0)
            self.B2.set(0)
            self.B25.set(0)
            self.B3.set(0)
            self.B4.set(0)
            self.B66.set(0)
            self.B7.set(0)
            self.B30.set(0)
            self.B39.set(0)
            self.B40.set(0)
            self.B38.set(0)
            self.B41.set(0)

        self.wanted_band_LTE()

    def off_all_none_UHB(self, event=None):
        self.UHB_all.set(False)


    def UHB_all_state(self):
        if self.UHB_all.get():
            logger.debug("UHB band all is checked")
            self.B48.set(48)
            self.B42.set(42)

        else:
            logger.debug("UHB band all is unchecked")
            self.B48.set(0)
            self.B42.set(0)

        self.wanted_band_LTE()

    def off_all_none_WCDMA(self, event=None):
        self.WCDMA_all.set(False)


    def off_all_none_HSUPA(self, event=None):
        self.HSUPA_all.set(False)

    def off_all_none_HSDPA(self, event=None):
        self.HSDPA_all.set(False)

    def WCDMA_all_state(self):
        if self.WCDMA_all.get():
            logger.debug("now is true")
            self.W1.set(1)
            self.W2.set(2)
            self.W4.set(4)
            self.W5.set(5)
            self.W8.set(8)
            self.W6.set(6)
            self.W19.set(19)

        else:
            logger.debug("now is false")
            self.W1.set(0)
            self.W2.set(0)
            self.W4.set(0)
            self.W5.set(0)
            self.W8.set(0)
            self.W6.set(0)
            self.W19.set(0)

        self.wanted_band_WCDMA()

    def off_all_none_GSM(self, event=None):
        self.GSM_all.set(False)

    def GSM_all_state(self):
        if self.GSM_all.get():
            logger.debug("now is true")
            self.GSM850.set(850)
            self.GSM900.set(900)
            self.GSM1800.set(1800)
            self.GSM1900.set(1900)

        else:
            logger.debug("now is false")
            self.GSM850.set(0)
            self.GSM900.set(0)
            self.GSM1800.set(0)
            self.GSM1900.set(0)

    def HSUPA_all_state(self):
        if self.HSUPA_all.get():
            logger.debug("now is true")
            self.U1.set(1)
            self.U2.set(2)
            self.U4.set(4)
            self.U5.set(5)
            self.U8.set(8)
            self.U6.set(6)
            self.U19.set(19)

        else:
            logger.debug("now is false")
            self.U1.set(0)
            self.U2.set(0)
            self.U4.set(0)
            self.U5.set(0)
            self.U8.set(0)
            self.U6.set(0)
            self.U19.set(0)

        self.wanted_band_HSUPA()

    def HSDPA_all_state(self):
        if self.HSDPA_all.get():
            logger.debug("now is true")
            self.D1.set(1)
            self.D2.set(2)
            self.D4.set(4)
            self.D5.set(5)
            self.D8.set(8)
            self.D6.set(6)
            self.D19.set(19)

        else:
            logger.debug("now is false")
            self.D1.set(0)
            self.D2.set(0)
            self.D4.set(0)
            self.D5.set(0)
            self.D8.set(0)
            self.D6.set(0)
            self.D19.set(0)

        self.wanted_band_HSDPA()

    def rx_auto_check_ue_pwr(self, event=None):
        self.TxMax.set(True)
        self.TxLow.set(True)
        self.rx_sweep.set(False)
        self.wanted_ue_pwr()

    def sweep_auto_check_ue_pwr(self, event=None):
        self.TxMax.set(True)
        self.TxLow.set(False)
        self.rx.set(False)
        self.wanted_ue_pwr()

    def measure(self):
        start = datetime.datetime.now()
        self.export_ui_setting()

        if self.instrument.get() == 'Anritsu8820':
            from anritsu8820 import Anritsu8820
            import want_test_band as wt

            wt.tech = self.wanted_tech()
            wt.lte_bands = self.wanted_band_LTE()
            wt.wcdma_bands = self.wanted_band_WCDMA()
            wt.gsm_bands = self.wanted_band_GSM()
            wt.hsupa_bands = self.wanted_band_HSUPA()
            wt.hsdpa_bands = self.wanted_band_HSDPA()
            wt.lte_bandwidths = self.wanted_bw()
            wt.channel = self.wanted_chan()
            wt.tx_max_pwr_sensitivity = self.wanted_ue_pwr()

            anritsu = Anritsu8820()

            if self.wanted_test['tx']:
                anritsu.run_tx()

            if self.wanted_test['rx']:
                anritsu.run_rx()

            if self.wanted_test['rx_sweep']:
                anritsu.run_rx_sweep_ch()

        elif self.instrument.get() == 'Anritsu8821':
            from anritsu8820 import Anritsu8821
            import want_test_band as wt

            wt.tech = self.wanted_tech()
            wt.lte_bands = self.wanted_band_LTE()
            wt.lte_bandwidths = self.wanted_bw()
            wt.channel = self.wanted_chan()
            wt.tx_max_pwr_sensitivity = self.wanted_ue_pwr()

            anritsu = Anritsu8821()

            if self.wanted_test['tx']:
                anritsu.run_tx()

            if self.wanted_test['rx']:
                anritsu.run_rx()

            if self.wanted_test['rx_sweep']:
                anritsu.run_rx_sweep_ch()

        elif self.instrument.get() == 'Agilent8960':
            pass

        stop = datetime.datetime.now()

        logger.info(f'Timer: {stop - start}')


if __name__ == "__main__":
    app = MainApp()
    app.run()
