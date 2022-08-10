#!/usr/bin/python3
import pathlib
import tkinter
import tkinter.ttk as ttk
import pygubu
import datetime
import logging
from logging.config import fileConfig
import threading
import signal
import os

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
        self.button_run = builder.get_object("button_run", master)
        self.checkbox_hsupa = builder.get_object("checkbutton_WCDMA", master)
        self.checkbox_hsdpa = builder.get_object("checkbutton_HSUPA", master)
        self.checkbox_wcdma = builder.get_object("checkbutton_HSDPA", master)
        self.style = ttk.Style(self.mainwindow)
        self.style.theme_use('xpnative')

        self.instrument = None
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
        self.band_segment = None
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
        self.tech_LTE = None
        self.tech_WCDMA = None
        self.tech_GSM = None
        self.tech_HSUPA = None
        self.tech_HSDPA = None
        self.bw1p4 = None
        self.bw3 = None
        self.bw5 = None
        self.bw10 = None
        self.bw15 = None
        self.bw20 = None
        self.TxMax = None
        self.TxLow = None
        self.tech_FR1 = None
        self.qpsk_lte = None
        self.q16_lte = None
        self.q64_lte = None
        self.q256_lte = None
        self.prb_lte = None
        self.frb_lte = None
        self.tx = None
        self.rx = None
        self.rx_sweep = None
        self.chan_L = None
        self.chan_M = None
        self.chan_H = None
        self.tx_level_sweep = None
        self.tx_freq_sweep = None
        self.N5 = None
        self.N8 = None
        self.N12 = None
        self.N13 = None
        self.N14 = None
        self.N18 = None
        self.N20 = None
        self.N26 = None
        self.N28 = None
        self.N29 = None
        self.N32 = None
        self.N71 = None
        self.LB_all_fr1 = None
        self.band_segment_fr1 = None
        self.N24 = None
        self.N1 = None
        self.N2 = None
        self.N3 = None
        self.N7 = None
        self.N30 = None
        self.N25 = None
        self.N66 = None
        # self.N39 = None
        self.N40 = None
        self.N38 = None
        self.N41 = None
        self.MHB_all_fr1 = None
        self.N34 = None
        self.N77 = None
        self.N78 = None
        self.UHB_all_fr1 = None
        self.N48 = None
        self.N79 = None
        self.bw5_fr1 = None
        self.bw10_fr1 = None
        self.bw15_fr1 = None
        self.bw20_fr1 = None
        self.bw25_fr1 = None
        self.bw30_fr1 = None
        self.bw40_fr1 = None
        self.bw50_fr1 = None
        self.bw60_fr1 = None
        self.bw80_fr1 = None
        self.bw90_fr1 = None
        self.bw100_fr1 = None
        self.bw70_fr1 = None
        self.qpsk_fr1 = None
        self.q16_fr1 = None
        self.q64_fr1 = None
        self.q256_fr1 = None
        self.dfts = None
        self.cp = None
        self.bpsk_fr1 = None
        self.inner_full_fr1 = None
        self.outer_full_fr1 = None
        self.inner_1rb_left_fr1 = None
        self.inner_1rb_right_fr1 = None
        self.edge_1rb_left_fr1 = None
        self.edge_1rb_right_fr1 = None
        self.edge_full_left_fr1 = None
        self.edge_full_right_fr1 = None
        self.sa_nsa = None
        self.scs15 = None
        self.scs30 = None
        self.scs60 = None
        self.general = None
        self.fcc = None
        self.ce = None
        self.endc = None
        self.tx_port_lte = None
        self.tx_port_fr1 = None
        self.tx1 = None
        self.tx2 = None
        self.sync_path = None
        self.ulmimo = None
        self.rx0 = None
        self.rx1 = None
        self.rx2 = None
        self.rx3 = None
        self.rx0_rx1 = None
        self.rx2_rx3 = None
        self.rx_all_path = None
        self.asw_path = None
        self.srs_path = None
        self.B3_N78 = None
        self.B2_N77 = None
        self.B66_N77 = None
        self.B66_N2 = None
        self.B66_N5 = None
        self.B12_N78 = None
        self.B5_N78 = None
        self.B28_N78 = None
        self.B5_N77 = None
        self.B13_N5 = None
        builder.import_variables(
            self,
            [
                "instrument",
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
                "band_segment",
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
                "tech_LTE",
                "tech_WCDMA",
                "tech_GSM",
                "tech_HSUPA",
                "tech_HSDPA",
                "bw1p4",
                "bw3",
                "bw5",
                "bw10",
                "bw15",
                "bw20",
                "TxMax",
                "TxLow",
                "tech_FR1",
                "qpsk_lte",
                "q16_lte",
                "q64_lte",
                "q256_lte",
                "prb_lte",
                "frb_lte",
                "tx",
                "rx",
                "rx_sweep",
                "chan_L",
                "chan_M",
                "chan_H",
                "tx_level_sweep",
                "tx_freq_sweep",
                "N5",
                "N8",
                "N12",
                "N13",
                "N14",
                "N18",
                "N20",
                "N26",
                "N28",
                "N29",
                "N32",
                "N71",
                "LB_all_fr1",
                "band_segment_fr1",
                "N24",
                "N1",
                "N2",
                "N3",
                "N7",
                "N30",
                "N25",
                "N66",
                # "N39",
                "N40",
                "N38",
                "N41",
                "MHB_all_fr1",
                "N34",
                "N77",
                "N78",
                "UHB_all_fr1",
                "N48",
                "N79",
                "bw5_fr1",
                "bw10_fr1",
                "bw15_fr1",
                "bw20_fr1",
                "bw25_fr1",
                "bw30_fr1",
                "bw40_fr1",
                "bw50_fr1",
                "bw60_fr1",
                "bw80_fr1",
                "bw90_fr1",
                "bw100_fr1",
                "bw70_fr1",
                "qpsk_fr1",
                "q16_fr1",
                "q64_fr1",
                "q256_fr1",
                "dfts",
                "cp",
                "bpsk_fr1",
                "inner_full_fr1",
                "outer_full_fr1",
                "inner_1rb_left_fr1",
                "inner_1rb_right_fr1",
                "edge_1rb_left_fr1",
                "edge_1rb_right_fr1",
                "edge_full_left_fr1",
                "edge_full_right_fr1",
                "sa_nsa",
                "scs15",
                "scs30",
                "scs60",
                "general",
                "fcc",
                "ce",
                "endc",
                "tx_port_lte",
                "tx_port_fr1",
                "tx1",
                "tx2",
                "sync_path",
                "ulmimo",
                "rx0",
                "rx1",
                "rx2",
                "rx3",
                "rx0_rx1",
                "rx2_rx3",
                "rx_all_path",
                "asw_path",
                "srs_path",
                "B3_N78",
                "B2_N77",
                "B66_N77",
                "B66_N2",
                "B66_N5",
                "B12_N78",
                "B5_N78",
                "B28_N78",
                "B5_N77",
                "B13_N5",
            ],
        )

        builder.connect_callbacks(self)
        # self.init_select()
        self.import_ui_setting()
        self.inst_to_tech()

    def run(self):
        self.mainwindow.mainloop()

    def t_stop(self):
        t = threading.Thread(target=self.stop)
        t.start()

    def stop(self):
        print('Crtrl C')
        os.kill(signal.CTRL_C_EVENT, 0)

    def t_measure(self):
        t = threading.Thread(target=self.measure, daemon=True)
        t.start()

    def import_ui_setting(self):
        """
        skip bands_gsm

        """
        logger.info('Import the last setting')
        # non list-like
        self.instrument.set(ui_init.instrument)
        self.band_segment.set(ui_init.band_segment)
        self.band_segment_fr1.set(ui_init.band_segment_fr1)
        self.tx.set(ui_init.tx)
        self.rx.set(ui_init.rx)
        self.rx_sweep.set(ui_init.rx_sweep)
        self.tx_level_sweep.set(ui_init.tx_level_sweep)
        self.tx_freq_sweep.set(ui_init.tx_freq_sweep)
        self.tx_port_lte.set(ui_init.port_tx_lte)
        self.tx_port_fr1.set(ui_init.port_tx_fr1)
        self.asw_path.set(ui_init.asw_path)
        self.srs_path.set(ui_init.srs_path)
        self.sync_path.set(ui_init.sync_path)


        #reet all the check button
        self.off_all_reset_tech()
        self.off_all_reset_bw()
        self.off_all_reset_ue_power()
        self.off_all_reset_ch()
        self.off_all_reset_GSM()
        self.off_all_reset_HSDPA()
        self.off_all_reset_HSUPA()
        self.off_all_reset_WCDMA()
        self.off_all_reset_LB()
        self.off_all_reset_MHB()
        self.off_all_reset_UHB()

        # list-like
        for band_endc in ui_init.bands_endc:
            if band_endc == '3_78':
                self.B3_N78.set(True)
            elif band_endc == '2_77':
                self.B2_N77.set(True)
            elif band_endc == '66_77':
                self.B66_N77.set(True)
            elif band_endc == '66_2':
                self.B66_N2.set(True)
            elif band_endc == '66_5':
                self.B66_N5.set(True)
            elif band_endc == '12_78':
                self.B12_N78.set(True)
            elif band_endc == '5_78':
                self.B5_N78.set(True)
            elif band_endc == '28_78':
                self.B28_N78.set(True)
            elif band_endc == '5_77':
                self.B5_N77.set(True)
            elif band_endc == '13_5':
                self.B13_N5.set(True)

        for band_fr1 in ui_init.bands_fr1:
            if band_fr1 == 1:
                self.N1.set(band_fr1)
            elif band_fr1 == 2:
                self.N2.set(band_fr1)
            elif band_fr1 == 3:
                self.N3.set(band_fr1)
            # elif band_fr1 == 4:
            #     self.N4.set(band_fr1)
            elif band_fr1 == 5:
                self.N5.set(band_fr1)
            elif band_fr1 == 7:
                self.N7.set(band_fr1)
            elif band_fr1 == 8:
                self.N8.set(band_fr1)
            elif band_fr1 == 12:
                self.N12.set(band_fr1)
            elif band_fr1 == 13:
                self.N13.set(band_fr1)
            elif band_fr1 == 14:
                self.N14.set(band_fr1)
            elif band_fr1 == 17:
                self.N17.set(band_fr1)
            elif band_fr1 == 18:
                self.N18.set(band_fr1)
            elif band_fr1 == 19:
                self.N19.set(band_fr1)
            elif band_fr1 == 20:
                self.N20.set(band_fr1)
            elif band_fr1 == 21:
                self.N21.set(band_fr1)
            elif band_fr1 == 24:
                self.N24.set(band_fr1)
            elif band_fr1 == 25:
                self.N25.set(band_fr1)
            elif band_fr1 == 26:
                self.N26.set(band_fr1)
            elif band_fr1 == 28:
                self.N28.set(band_fr1)
            elif band_fr1 == 29:
                self.N29.set(band_fr1)
            elif band_fr1 == 30:
                self.N30.set(band_fr1)
            elif band_fr1 == 32:
                self.N32.set(band_fr1)
            elif band_fr1 == 34:
                self.N34.set(band_fr1)
            elif band_fr1 == 38:
                self.N38.set(band_fr1)
            # elif band_fr1 == 39:
                # self.N39.set(band_fr1)
            elif band_fr1 == 40:
                self.N40.set(band_fr1)
            elif band_fr1 == 41:
                self.N41.set(band_fr1)
            elif band_fr1 == 42:
                self.N48.set(band_fr1)
            elif band_fr1 == 66:
                self.N66.set(band_fr1)
            elif band_fr1 == 71:
                self.N71.set(band_fr1)
            elif band_fr1 == 77:
                self.N77.set(band_fr1)
            elif band_fr1 == 78:
                self.N78.set(band_fr1)
            elif band_fr1 == 79:
                self.N79.set(band_fr1)

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
            elif tech == 'FR1':
                self.tech_FR1.set(True)
            # elif tech == 'GSM':
            #     self.tech_GSM.set(True)

        for bw in ui_init.bw_lte:
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

        for bw in ui_init.bw_fr1:
            if bw == 5:
                self.bw5_fr1.set(True)
            elif bw == 10:
                self.bw10_fr1.set(True)
            elif bw == 15:
                self.bw15_fr1.set(True)
            elif bw == 20:
                self.bw20_fr1.set(True)
            elif bw == 25:
                self.bw25_fr1.set(True)
            elif bw == 30:
                self.bw30_fr1.set(True)
            elif bw == 40:
                self.bw40_fr1.set(True)
            elif bw == 50:
                self.bw50_fr1.set(True)
            elif bw == 60:
                self.bw60_fr1.set(True)
            elif bw == 70:
                self.bw70_fr1.set(True)
            elif bw == 80:
                self.bw80_fr1.set(True)
            elif bw == 90:
                self.bw90_fr1.set(True)
            elif bw == 100:
                self.bw100_fr1.set(True)

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

        for script in ui_init.scripts:
            if script == 'GENERAL':
                self.general.set(True)
            elif script == 'FCC':
                self.fcc.set(True)
            elif script == 'CE':
                self.ce.set(True)
            elif script == 'ENDC':
                self.endc.set(True)

        for type in ui_init.type_fr1:
            if type == 'DFTS':
                self.dfts.set(True)
            elif type == 'CP':
                self.cp.set(True)

        for rb_ftm in ui_init.rb_ftm_lte:
            if rb_ftm == 'PRB':
                self.prb_lte.set(True)
            elif rb_ftm == 'FRB':
                self.frb_lte.set(True)

        for rb_ftm in ui_init.rb_ftm_fr1:
            if rb_ftm == 'INNER_FULL':
                self.inner_full_fr1.set(True)
            elif rb_ftm == 'OUTER_FULL':
                self.outer_full_fr1.set(True)
            elif rb_ftm == 'EDGE_1RB_LEFT':
                self.edge_1rb_left_fr1.set(True)
            elif rb_ftm == 'EDGE_1RB_RIGHT':
                self.edge_1rb_right_fr1.set(True)
            elif rb_ftm == 'EDGE_FULL_LEFT':
                self.edge_full_left_fr1.set(True)
            elif rb_ftm == 'EDGE_FULL_RIGHT':
                self.edge_full_right_fr1.set(True)
            elif rb_ftm == 'INNER_1RB_LEFT':
                self.inner_1rb_left_fr1.set(True)
            elif rb_ftm == 'INNER_1RB_RIGHT':
                self.inner_1rb_right_fr1.set(True)

            for mcs in ui_init.mcs_lte:
                if mcs == 'QPSK':
                    self.qpsk_lte.set(True)
                elif mcs == 'Q16':
                    self.q16_lte.set(True)
                elif mcs == 'Q64':
                    self.q64_lte.set(True)
                elif mcs == 'Q256':
                    self.q256_lte.set(True)

            for mcs in ui_init.mcs_fr1:
                if mcs == 'QPSK':
                    self.qpsk_fr1.set(True)
                elif mcs == 'Q16':
                    self.q16_fr1.set(True)
                elif mcs == 'Q64':
                    self.q64_fr1.set(True)
                elif mcs == 'Q256':
                    self.q256_fr1.set(True)
                elif mcs == 'BPSK':
                    self.bpsk_fr1.set(True)

        for tx_path in ui_init.tx_paths:
            if tx_path == 'TX1':
                self.tx1.set(True)
            elif tx_path == 'TX2':
                self.tx2.set(True)
            elif tx_path == 'MIMO':
                self.ulmimo.set(True)

        for rx_path in ui_init.rx_paths:
            if rx_path == 2:
                self.rx0.set(True)
            elif rx_path == 1:
                self.rx1.set(True)
            elif rx_path == 4:
                self.rx2.set(True)
            elif rx_path == 8:
                self.rx3.set(True)
            elif rx_path == 3:
                self.rx0_rx1.set(True)
            elif rx_path == 12:
                self.rx2_rx3.set(True)
            elif rx_path == 15:
                self.rx_all_path.set(True)

        for mcs in ui_init.mcs_lte:
            if mcs == 'QPSK':
                self.qpsk_lte.set(True)
            elif mcs == 'Q16':
                self.q16_lte.set(True)
            elif mcs == 'Q64':
                self.q64_lte.set(True)
            elif mcs == 'Q256':
                self.q256_lte.set(True)

        for mcs in ui_init.mcs_fr1:
            if mcs == 'QPSK':
                self.qpsk_fr1.set(True)
            elif mcs == 'Q16':
                self.q16_fr1.set(True)
            elif mcs == 'Q64':
                self.q64_fr1.set(True)
            elif mcs == 'Q256':
                self.q256_fr1.set(True)

    def export_ui_setting(self):
        logger.info('Export ui setting')
        # thses are list like
        tech = self.wanted_tech()
        bw_lte = self.wanted_bw()
        bw_fr1 = self.wanted_bw_fr1()
        ue_power = self.wanted_ue_pwr()
        bands_fr1 = self.wanted_band_FR1()
        bands_lte = self.wanted_band_LTE()
        bands_wcdma = self.wanted_band_WCDMA()
        bands_hsupa = self.wanted_band_HSUPA()
        bands_hsdpa = self.wanted_band_HSDPA()
        bands_gsm = self.wanted_band_GSM()
        bands_endc = self.wanted_band_ENDC()
        scripts = self.wanted_scripts()
        type_fr1 = self.wanted_type()
        mcs_lte = self.wanted_mcs_lte()
        mcs_fr1 = self.wanted_mcs_fr1()
        rb_ftm_lte = self.wanted_ftm_rb_lte()
        rb_ftm_fr1 = self.wanted_ftm_rb_fr1()
        tx_paths = self.wanted_tx_path()
        rx_paths = self.wanted_rx_path()



        # these are not list-like
        instrument = self.instrument.get()
        port_tx_lte = self.tx_port_lte.get()
        port_tx_fr1 = self.tx_port_fr1.get()
        asw_path = self.asw_path.get()
        srs_path = self.srs_path.get()
        sync_path = self.sync_path.get()
        band_segment = self.band_segment.get()
        band_segment_fr1 = self.band_segment_fr1.get()
        chan = self.wanted_chan()
        tx, rx, rx_sweep, tx_level_sweep, tx_freq_sweep = self.wanted_tx_rx_sweep()

        new_data = []
        with open('ui_init.py', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'bands_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_lte) + '\n'
                    logger.debug('replace band LTE')
                    line = '='.join(temp_list)

                elif 'bands_wcdma' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_wcdma) + '\n'
                    logger.debug('replace band WCDMA')
                    line = '='.join(temp_list)

                elif 'bands_hsupa' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_hsupa) + '\n'
                    logger.debug('replace band HSUPA')
                    line = '='.join(temp_list)

                elif 'bands_hsdpa' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_hsdpa) + '\n'
                    logger.debug('replace band HSDPA')
                    line = '='.join(temp_list)

                elif 'bands_gsm' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_gsm) + '\n'
                    logger.debug('replace band GSM')
                    line = '='.join(temp_list)

                elif 'bands_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_fr1) + '\n'
                    logger.debug('replace band FR1')
                    line = '='.join(temp_list)

                elif 'bands_endc' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bands_endc) + '\n'
                    logger.debug('replace band ENDC')
                    line = '='.join(temp_list)

                elif 'scripts' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(scripts) + '\n'
                    logger.debug('replace band Scripts')
                    line = '='.join(temp_list)

                elif 'type_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(type_fr1) + '\n'
                    logger.debug('replace band Type')
                    line = '='.join(temp_list)

                elif 'mcs_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(mcs_lte) + '\n'
                    logger.debug('replace band MCS for LTE')
                    line = '='.join(temp_list)

                elif 'mcs_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(mcs_fr1) + '\n'
                    logger.debug('replace band MCS for FR1')
                    line = '='.join(temp_list)

                elif 'rb_ftm_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rb_ftm_lte) + '\n'
                    logger.debug('replace band RB_FTM for LTE')
                    line = '='.join(temp_list)

                elif 'rb_ftm_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rb_ftm_fr1) + '\n'
                    logger.debug('replace band RB_FTM for FR1')
                    line = '='.join(temp_list)

                elif 'tx_paths' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tx_paths) + '\n'
                    logger.debug('replace tx_paths')
                    line = '='.join(temp_list)

                elif 'rx_paths' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rx_paths) + '\n'
                    logger.debug('replace rx_paths')
                    line = '='.join(temp_list)

                elif 'tech' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tech) + '\n'
                    logger.debug('replace tech setting')
                    line = '='.join(temp_list)

                elif 'bw_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bw_lte) + '\n'
                    logger.debug('replace bw setting for LTE')
                    line = '='.join(temp_list)

                elif 'bw_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(bw_fr1) + '\n'
                    logger.debug('replace bw setting for FR1')
                    line = '='.join(temp_list)

                elif 'ue_power' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(ue_power) + '\n'
                    logger.debug('replace ue power setting')
                    line = '='.join(temp_list)

                elif 'instrument' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(instrument) + '"' + '\n'
                    logger.debug('replace instrument setting')
                    line = '='.join(temp_list)

                elif 'tx_port_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(tx_port_lte) + '"' + '\n'
                    logger.debug('replace tx_port_lte setting')
                    line = '='.join(temp_list)

                elif 'tx_port_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(tx_port_fr1) + '"' + '\n'
                    logger.debug('replace tx_port_fr1 setting')
                    line = '='.join(temp_list)

                elif 'sync_path' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(sync_path) + '\n'
                    logger.debug('replace sync_path setting')
                    line = '='.join(temp_list)

                elif 'asw_path' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(asw_path) + '\n'
                    logger.debug('replace asw_path setting')
                    line = '='.join(temp_list)

                elif 'srs_path' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(srs_path) + '\n'
                    logger.debug('replace srs_path setting')
                    line = '='.join(temp_list)

                elif 'band_segment ' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(band_segment) + '"' + '\n'
                    logger.debug('replace band segment setting for LTE')
                    line = '='.join(temp_list)

                elif 'band_segment_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] =' ' + '"' + str(band_segment_fr1) + '"' + '\n'
                    logger.debug('replace band segment setting for FR1')
                    line = '='.join(temp_list)

                elif 'port_tx_lte' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(port_tx_lte) + '\n'
                    logger.debug('replace port_tx_lte for LTE')
                    line = '='.join(temp_list)

                elif 'port_tx_fr1' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(port_tx_fr1) + '\n'
                    logger.debug('replace port_tx_frq for FR1')
                    line = '='.join(temp_list)

                elif 'tx ' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tx) + '\n'
                    logger.debug('replace tx setting')
                    line = '='.join(temp_list)

                elif 'tx_level_sweep' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tx_level_sweep) + '\n'
                    logger.debug('replace tx level sweep setting')
                    line = '='.join(temp_list)

                elif 'tx_freq_sweep' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(tx_freq_sweep) + '\n'
                    logger.debug('replace tx freq sweep setting')
                    line = '='.join(temp_list)

                elif 'rx ' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rx) + '\n'
                    logger.debug('replace rx setting')
                    line = '='.join(temp_list)

                elif 'rx_sweep' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + str(rx_sweep) + '\n'
                    logger.debug('replace rx_sweep setting')
                    line = '='.join(temp_list)

                elif 'chan' in line:
                    temp_list = line.split('=')
                    temp_list[1] = ' ' + '"' + str(chan) + '"' + '\n'
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
        self.LB_all_fr1.set(False)
        self.LB_all_state()
        self.LB_all_state_fr1()

    def off_all_reset_MHB(self):
        self.MHB_all.set(False)
        self.MHB_all_fr1.set(False)
        self.MHB_all_state()
        self.MHB_all_state_fr1()

    def off_all_reset_UHB(self):
        self.UHB_all.set(False)
        self.UHB_all_fr1.set(False)
        self.UHB_all_state()
        self.UHB_all_state_fr1()

    def thermal_dis(self):
        from adb_control import thermal_charger_disable
        thermal_charger_disable()

    def init_select(self):
        self.instrument.set('Anritsu8820')
        self.bw10.set(True)
        self.tech_LTE.set(True)
        self.tx.set(True)
        self.wanted_tx_rx_sweep()
        self.chan_L.set(True)
        self.chan_M.set(True)
        self.chan_H.set(True)
        self.sa_nsa.set(0)


        logger.info(f'default instrument: {self.instrument.get()}')

    def wanted_band_ENDC(self):
        self.band_endc = []

        if self.B3_N78.get():
            logger.debug(self.B3_N78.get())
            self.band_endc.append('3_78')
        if self.B2_N77.get():
            logger.debug(self.B2_N77.get())
            self.band_endc.append('2_77')
        if self.B66_N77.get():
            logger.debug(self.B66_N77.get())
            self.band_endc.append('66_77')
        if self.B66_N2.get():
            logger.debug(self.B66_N2.get())
            self.band_endc.append('66_2')
        if self.B66_N5.get():
            logger.debug(self.B66_N5.get())
            self.band_endc.append('66_5')
        if self.B12_N78.get():
            logger.debug(self.B12_N78.get())
            self.band_endc.append('12_78')
        if self.B5_N78.get():
            logger.debug(self.B5_N78.get())
            self.band_endc.append('5_78')
        if self.B28_N78.get():
            logger.debug(self.B28_N78.get())
            self.band_endc.append('28_78')
        if self.B5_N77.get():
            logger.debug(self.B5_N77.get())
            self.band_endc.append('5_77')
        if self.B13_N5.get():
            logger.debug(self.B13_N5.get())
            self.band_endc.append('13_5')

        if self.band_endc == []:
            logger.debug('Nothing to select for ENDC')

        logger.info(f'select ENDC band: {self.band_endc}')
        return self.band_endc

    def wanted_band_FR1(self):
        self.band_fr1 = []

        if self.N1.get() == 1:
            logger.debug(self.N1.get())
            self.band_fr1.append(self.N1.get())
        if self.N2.get() == 2:
            logger.debug(self.N2.get())
            self.band_fr1.append(self.N2.get())
        if self.N3.get() == 3:
            logger.debug(self.N3.get())
            self.band_fr1.append(self.N3.get())
        # if self.N4.get() == 4:
        #     logger.debug(self.N4.get())
        #     self.band_fr1.append(self.N4.get())
        if self.N7.get() == 7:
            logger.debug(self.N7.get())
            self.band_fr1.append(self.N7.get())
        if self.N25.get() == 25:
            logger.debug(self.N25.get())
            self.band_fr1.append(self.N25.get())
        if self.N66.get() == 66:
            logger.debug(self.N66.get())
            self.band_fr1.append(self.N66.get())
        if self.N30.get() == 30:
            logger.debug(self.N30.get())
            self.band_fr1.append(self.N30.get())
        # if self.N39.get() == 39:
        #     logger.debug(self.N39.get())
        #     self.band_fr1.append(self.N39.get())
        if self.N40.get() == 40:
            logger.debug(self.N40.get())
            self.band_fr1.append(self.N40.get())
        if self.N38.get() == 38:
            logger.debug(self.N38.get())
            self.band_fr1.append(self.N38.get())
        if self.N41.get() == 41:
            logger.debug(self.N41.get())
            self.band_fr1.append(self.N41.get())
        if self.N34.get() == 34:
            logger.debug(self.N34.get())
            self.band_fr1.append(self.N34.get())
        if self.N5.get() == 5:
            logger.debug(self.N5.get())
            self.band_fr1.append(self.N5.get())
        if self.N8.get() == 8:
            logger.debug(self.N8.get())
            self.band_fr1.append(self.N8.get())
        if self.N12.get() == 12:
            logger.debug(self.N12.get())
            self.band_fr1.append(self.N12.get())
        if self.N13.get() == 13:
            logger.debug(self.N13.get())
            self.band_fr1.append(self.N13.get())
        if self.N14.get() == 14:
            logger.debug(self.N14.get())
            self.band_fr1.append(self.N14.get())
        if self.N18.get() == 18:
            logger.debug(self.N18.get())
            self.band_fr1.append(self.N18.get())
        if self.N20.get() == 20:
            logger.debug(self.N20.get())
            self.band_fr1.append(self.N20.get())
        if self.N24.get() == 24:
            logger.debug(self.N24.get())
            self.band_fr1.append(self.N24.get())
        if self.N26.get() == 26:
            logger.debug(self.N26.get())
            self.band_fr1.append(self.N26.get())
        if self.N28.get() == 28:
            logger.debug(self.N28.get())
            self.band_fr1.append(self.N28.get())
        if self.N29.get() == 29:
            logger.debug(self.N29.get())
            self.band_fr1.append(self.N29.get())
        if self.N32.get() == 32:
            logger.debug(self.N32.get())
            self.band_fr1.append(self.N32.get())
        if self.N71.get() == 71:
            logger.debug(self.N71.get())
            self.band_fr1.append(self.N71.get())
        if self.N48.get() == 48:
            logger.debug(self.N48.get())
            self.band_fr1.append(self.N48.get())
        if self.N77.get() == 77:
            logger.debug(self.N77.get())
            self.band_fr1.append(self.N77.get())
        if self.N78.get() == 78:
            logger.debug(self.N78.get())
            self.band_fr1.append(self.N78.get())
        if self.N79.get() == 79:
            logger.debug(self.N79.get())
            self.band_fr1.append(self.N79.get())

        if self.band_fr1 == []:
            logger.debug('Nothing to select for FR1')

        logger.info(f'select FR1 band: {self.band_fr1}')
        return self.band_fr1

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

    def inst_to_tech(self):
        if self.instrument.get() == 'Cmw100':
            self.checkbox_hsupa['state'] = tkinter.DISABLED
            self.checkbox_hsdpa['state'] = tkinter.DISABLED
            self.checkbox_wcdma['state'] = tkinter.DISABLED
        else:
            self.checkbox_hsupa['state'] = tkinter.NORMAL
            self.checkbox_hsdpa['state'] = tkinter.NORMAL
            self.checkbox_wcdma['state'] = tkinter.NORMAL

    def inst_select(self):
        logger.info(self.instrument.get())
        # return self.instrument.get()
        if self.instrument.get() == 'Cmw100':
            self.checkbox_hsupa['state'] = tkinter.DISABLED
            self.checkbox_hsdpa['state'] = tkinter.DISABLED
            self.checkbox_wcdma['state'] = tkinter.DISABLED
        else:
            self.checkbox_hsupa['state'] = tkinter.NORMAL
            self.checkbox_hsdpa['state'] = tkinter.NORMAL
            self.checkbox_wcdma['state'] = tkinter.NORMAL

    def segment_select(self):
        logger.info(f'segment: {self.band_segment.get()}')

    def segment_select_fr1(self):
        logger.info(f'segment: {self.band_segment_fr1.get()}')

    def wanted_tx_rx_sweep(self):
        self.wanted_test = {}
        self.wanted_test.setdefault('tx', False)
        self.wanted_test.setdefault('rx', False)
        self.wanted_test.setdefault('rx_sweep', False)
        self.wanted_test.setdefault('tx_level_sweep', False)
        self.wanted_test.setdefault('tx_freq_sweep', False)

        if self.tx.get():
            logger.debug(self.tx.get())
            self.wanted_test['tx'] = self.tx.get()

        if self.tx_level_sweep.get():
            logger.debug(self.tx_level_sweep.get())
            self.wanted_test['tx_level_sweep'] = self.tx_level_sweep.get()

        if self.tx_freq_sweep.get():
            logger.debug(self.tx_freq_sweep.get())
            self.wanted_test['tx_freq_sweep'] = self.tx_freq_sweep.get()

        if self.rx.get():
            logger.debug(self.rx.get())
            self.wanted_test['rx'] = self.rx.get()

        if self.rx_sweep.get():
            logger.debug(self.rx_sweep.get())
            self.wanted_test['rx_sweep'] = self.rx_sweep.get()

        if self.wanted_test == {}:
            logger.debug('Nothing to select for test items')

        logger.info(self.wanted_test)
        return self.tx.get(), self.rx.get(), self.rx_sweep.get(), self.tx_level_sweep.get(), self.tx_freq_sweep.get()

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

        if self.bw20.get():
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

        if self.tech_FR1.get():
            logger.debug(self.tech_FR1.get())
            self.tech.append('FR1')

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
        self.bw5_fr1.set(False)
        self.bw10_fr1.set(False)
        self.bw15_fr1.set(False)
        self.bw20_fr1.set(False)
        self.bw25_fr1.set(False)
        self.bw30_fr1.set(False)
        self.bw40_fr1.set(False)
        self.bw50_fr1.set(False)
        self.bw60_fr1.set(False)
        self.bw70_fr1.set(False)
        self.bw80_fr1.set(False)
        self.bw90_fr1.set(False)
        self.bw100_fr1.set(False)

    def off_all_reset_tech(self):
        self.tech_LTE.set(False)
        self.tech_WCDMA.set(False)
        self.tech_HSDPA.set(False)
        self.tech_HSUPA.set(False)
        self.tech_GSM.set(False)
        self.tech_FR1.set(False)

    def off_all_reset_ue_power(self):
        self.TxMax.set(False)
        self.TxLow.set(False)

    def off_all_reset_ch(self):
        self.chan_L.set(False)
        self.chan_M.set(False)
        self.chan_H.set(False)

    # def off_all_none_LB(self, event=None):
    #     self.LB_all.set(False)

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

    def LB_all_state_fr1(self):
        logger.debug(self.LB_all_fr1.get())
        if self.LB_all_fr1.get():
            logger.debug("LB band all is checked for FR1")
            self.N5.set(5)
            self.N8.set(8)
            self.N12.set(12)
            self.N13.set(13)
            self.N14.set(14)
            # self.N18.set(18)
            self.N20.set(20)
            self.N24.set(24)
            self.N26.set(26)
            self.N28.set(28)
            self.N29.set(29)
            self.N32.set(32)
            self.N71.set(71)

        else:
            logger.debug("LB band all is unchecked for FR1")
            self.N5.set(0)
            self.N8.set(0)
            self.N12.set(0)
            self.N13.set(0)
            self.N14.set(0)
            self.N18.set(0)
            self.N20.set(0)
            self.N24.set(0)
            self.N26.set(0)
            self.N28.set(0)
            self.N29.set(0)
            self.N32.set(0)
            self.N71.set(0)

        self.wanted_band_FR1()


    # def off_all_none_MHB(self, event=None):
    #     self.MHB_all.set(False)

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

    def MHB_all_state_fr1(self):
        logger.debug(self.MHB_all_fr1.get())
        if self.MHB_all_fr1.get():
            logger.debug("MHB band all is checked for FR1")
            self.N1.set(1)
            self.N2.set(2)
            self.N25.set(25)
            self.N3.set(3)
            # self.N4.set(4)
            self.N66.set(66)
            self.N7.set(7)
            self.N30.set(30)
            # self.N39.set(39)
            self.N40.set(40)
            self.N38.set(38)
            self.N41.set(41)
            self.N34.set(34)

        else:
            logger.debug("MHB band all is unchecked for FR1")
            self.N1.set(0)
            self.N2.set(0)
            self.N25.set(0)
            self.N3.set(0)
            # self.N4.set(0)
            self.N66.set(0)
            self.N7.set(0)
            self.N30.set(0)
            # self.N39.set(0)
            self.N40.set(0)
            self.N38.set(0)
            self.N41.set(0)
            self.N34.set(0)

        self.wanted_band_FR1()

    # def off_all_none_UHB(self, event=None):
    #     self.UHB_all.set(False)

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

    def UHB_all_state_fr1(self):
        logger.debug(self.UHB_all_fr1.get())
        if self.UHB_all_fr1.get():
            logger.debug("UHB band all is checked for FR1")
            self.N48.set(48)
            self.N77.set(77)
            self.N78.set(78)
            self.N79.set(79)

        else:
            logger.debug("UHB band all is unchecked for FR1")
            self.N48.set(0)
            self.N77.set(0)
            self.N78.set(0)
            self.N79.set(0)

        self.wanted_band_FR1()


    # def off_all_none_WCDMA(self, event=None):
    #     self.WCDMA_all.set(False)
    #
    # def off_all_none_HSUPA(self, event=None):
    #     self.HSUPA_all.set(False)
    #
    # def off_all_none_HSDPA(self, event=None):
    #     self.HSDPA_all.set(False)

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

    # def off_all_none_GSM(self, event=None):
    #     self.GSM_all.set(False)

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

    def wanted_bw_fr1(self):
        self.bw_fr1 = []

        if self.bw5_fr1.get():
            logger.debug('Bw_5')
            self.bw_fr1.append(5)

        if self.bw10_fr1.get():
            logger.debug('Bw_10')
            self.bw_fr1.append(10)

        if self.bw15_fr1.get():
            logger.debug('Bw_15')
            self.bw_fr1.append(15)

        if self.bw20_fr1.get():
            logger.debug('Bw_20')
            self.bw_fr1.append(20)

        if self.bw25_fr1.get():
            logger.debug('Bw_25')
            self.bw_fr1.append(25)

        if self.bw30_fr1.get():
            logger.debug('Bw_30')
            self.bw_fr1.append(30)

        if self.bw40_fr1.get():
            logger.debug('Bw_40')
            self.bw_fr1.append(40)

        if self.bw50_fr1.get():
            logger.debug('Bw_50')
            self.bw_fr1.append(50)

        if self.bw60_fr1.get():
            logger.debug('Bw_60')
            self.bw_fr1.append(60)

        if self.bw70_fr1.get():
            logger.debug('Bw_70')
            self.bw_fr1.append(70)

        if self.bw80_fr1.get():
            logger.debug('Bw_80')
            self.bw_fr1.append(80)

        if self.bw90_fr1.get():
            logger.debug('Bw_90')
            self.bw_fr1.append(90)

        if self.bw100_fr1.get():
            logger.debug('Bw_100')
            self.bw_fr1.append(100)

        if self.bw_fr1 == []:
            logger.debug('Nothing to select for Bw')

        logger.info(f'fr1 select BW: {self.bw_fr1}')
        return self.bw_fr1

    def wanted_mcs_fr1(self):
        self.mcs_fr1 = []
        if self.bpsk_fr1.get():
            logger.debug('BPSK')
            self.mcs_fr1.append('BPSK')

        if self.qpsk_fr1.get():
            logger.debug('QPSK')
            self.mcs_fr1.append('QPSK')

        if self.q16_fr1.get():
            logger.debug('Q16')
            self.mcs_fr1.append('Q16')

        if self.q64_fr1.get():
            logger.debug('Q64')
            self.mcs_fr1.append('Q64')

        if self.q256_fr1.get():
            logger.debug('Q256')
            self.mcs_fr1.append('Q256')

        if self.mcs_fr1 == []:
            logger.debug('Nothing to select for mcs_fr1')

        logger.info(f'FR1 select MCS: {self.mcs_fr1}')
        return self.mcs_fr1

    def wanted_mcs_lte(self):
        self.mcs_lte = []
        if self.qpsk_lte.get():
            logger.debug('QPSK')
            self.mcs_lte.append('QPSK')

        if self.q16_lte.get():
            logger.debug('Q16')
            self.mcs_lte.append('Q16')

        if self.q64_lte.get():
            logger.debug('Q64')
            self.mcs_lte.append('Q64')

        if self.q256_lte.get():
            logger.debug('Q256')
            self.mcs_lte.append('Q256')

        if self.mcs_lte == []:
            logger.debug('Nothing to select for mcs_lte')

        logger.info(f'LTE select MCS: {self.mcs_lte}')
        return self.mcs_lte

    def wanted_type(self):
        self.type = []
        if self.dfts.get():
            logger.debug('DFTS')
            self.type.append('DFTS')

        if self.cp.get():
            logger.debug('CP')
            self.type.append('CP')

        if self.type == []:
            logger.debug('Nothing to select for type')

        logger.info(f'type select: {self.type}')
        return self.type

    def fr1_mode_select(self):
        if self.sa_nsa.get() == 0:
            logger.info('selct mode: SA')
        elif self.sa_nsa.get() == 1:
            logger.info('selct mode: NSA')
        # return self.instrument.get()

    def wanted_scs(self):
        pass

    def wanted_scripts(self):
        self.script = []
        if self.general.get():
            logger.debug('GENERAL')
            self.script.append('GENERAL')

        if self.fcc.get():
            logger.debug('FCC')
            self.script.append('FCC')

        if self.ce.get():
            logger.debug('CE')
            self.script.append('CE')

        if self.endc.get():
            logger.debug('ENDC')
            self.script.append('ENDC')

        if self.script == []:
            logger.debug('Nothing to select for script')

        logger.info(f'Script to select : {self.script}')
        return self.script

    def select_tx_port_lte(self):
        logger.info(self.tx_port_lte.get())
        # return self.tx_port_lte.get()

    def select_tx_port_fr1(self):
        logger.info(self.tx_port_fr1.get())
        # return self.tx_port_fr1.get()

    def wanted_tx_path(self):
        self.tx_path = []
        if self.tx1.get():
            logger.debug('TX1')
            self.tx_path.append('TX1')

        if self.tx2.get():
            logger.debug('TX2')
            self.tx_path.append('TX2')

        if self.ulmimo.get():
            logger.debug('MIMO')
            self.tx_path.append('MIMO')

        if self.tx_path == []:
            logger.debug('Nothing to select for tx path')

        logger.info(f'script select BW: {self.tx_path}')
        return self.tx_path

    def wanted_rx_path(self):
        self.rx_path = []
        self.rx_path_show = []
        if self.rx0.get():
            logger.debug('RX0')
            self.rx_path_show.append('RX0')
            self.rx_path.append(2)

        if self.rx1.get():
            logger.debug('RX1')
            self.rx_path_show.append('RX1')
            self.rx_path.append(1)

        if self.rx2.get():
            logger.debug('RX2')
            self.rx_path_show.append('RX2')
            self.rx_path.append(4)

        if self.rx3.get():
            logger.debug('RX3')
            self.rx_path_show.append('RX3')
            self.rx_path.append(8)

        if self.rx0_rx1.get():
            logger.debug('RX0+RX1')
            self.rx_path_show.append('RX0+RX1')
            self.rx_path.append(3)

        if self.rx2_rx3.get():
            logger.debug('RX2+RX3')
            self.rx_path_show.append('RX2+RX3')
            self.rx_path.append(12)

        if self.rx_all_path.get():
            logger.debug('all path')
            self.rx_path_show.append('ALL PATH')
            self.rx_path.append(15)

        if self.rx_path == []:
            logger.debug('Nothing to select for rx path')


        logger.info(f'RX path select: {self.rx_path_show}')
        logger.debug(f'RX path select: {self.rx_path}')

        return self.rx_path

    def select_asw_path(self):
        logger.info(f'select AS path {self.asw_path.get()}')

    def select_sync_path(self):
        logger.info(f'select syn(CA) path {self.sync_path.get()}')

    def select_srs_path(self):
        logger.info(f'select SRS path {self.srs_path.get()}')

    def wanted_ftm_rb_lte(self):
        self.ftm_rb_lte = []
        if self.prb_lte.get():
            logger.debug('PRB')
            self.ftm_rb_lte.append('PRB')

        if self.frb_lte.get():
            logger.debug('FRB')
            self.ftm_rb_lte.append('FRB')

        if self.ftm_rb_lte == []:
            logger.debug('Nothing to select on RB setting for LTE')

        logger.info(f'RB setting for LTE to select: {self.ftm_rb_lte}')
        return self.ftm_rb_lte

    def wanted_ftm_rb_fr1(self):
        self.ftm_rb_fr1 = []
        if self.inner_full_fr1.get():
            logger.debug('INNER_FULL')
            self.ftm_rb_fr1.append('INNER_FULL')

        if self.outer_full_fr1.get():
            logger.debug('OUTER_FULL')
            self.ftm_rb_fr1.append('OUTER_FULL')

        if self.inner_1rb_left_fr1.get():
            logger.debug('INNER_1RB_LEFT')
            self.ftm_rb_fr1.append('INNER_1RB_LEFT')

        if self.inner_1rb_right_fr1.get():
            logger.debug('INNER_1RB_RIGHT')
            self.ftm_rb_fr1.append('INNER_1RB_RIGHT')

        if self.edge_1rb_left_fr1.get():
            logger.debug('EDGE_1RB_LEFT')
            self.ftm_rb_fr1.append('EDGE_1RB_LEFT')

        if self.edge_1rb_right_fr1.get():
            logger.debug('EDGE_1RB_RIGHT')
            self.ftm_rb_fr1.append('EDGE_1RB_RIGHT')

        if self.edge_full_left_fr1.get():
            logger.debug('EDGE_FULL_LEFT')
            self.ftm_rb_fr1.append('EDGE_FULL_LEFT')

        if self.edge_full_right_fr1.get():
            logger.debug('EDGE_FULL_RIGHT')
            self.ftm_rb_fr1.append('EDGE_FULL_RIGHT')

        if self.ftm_rb_fr1 == []:
            logger.debug('Nothing to select on RB setting for FR1')

        logger.info(f'RB setting for FR1 to select: {self.ftm_rb_fr1}')
        return self.ftm_rb_fr1

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

    def test_pipeline(self, inst_class):
        inst = inst_class()
        if inst.__class__.__name__ == 'Cmw100':
            if self.wanted_test['tx']:
                inst.run_tx()

            if self.wanted_test['rx']:
                inst.run_rx()

            if self.wanted_test['tx_level_sweep']:
                inst.run_tx_level_sweep()

            if self.wanted_test['tx_freq_sweep']:
                inst.run_tx_freq_sweep()

        elif inst.__class__.__name__ == 'Anritsu8820':
            if self.wanted_test['tx']:
                inst.run_tx()

            if self.wanted_test['rx']:
                inst.run_rx()

            if self.wanted_test['rx_sweep']:
                inst.run_rx_sweep_ch()

        elif inst.__class__.__name__ == 'Anritsu8821':
            if self.wanted_test['tx']:
                inst.run_tx()

            if self.wanted_test['rx']:
                inst.run_rx()

            if self.wanted_test['rx_sweep']:
                inst.run_rx_sweep_ch()


    def measure(self):
        import want_test_band as wt
        self.button_run['state'] = tkinter.DISABLED
        start = datetime.datetime.now()
        self.export_ui_setting()
        # list-like
        wt.tech = self.wanted_tech()
        wt.endc_bands = self.wanted_band_ENDC()
        wt.fr1_bands = self.wanted_band_FR1()
        wt.lte_bands = self.wanted_band_LTE()
        wt.wcdma_bands = self.wanted_band_WCDMA()
        wt.gsm_bands = self.wanted_band_GSM()
        wt.hsupa_bands = self.wanted_band_HSUPA()
        wt.hsdpa_bands = self.wanted_band_HSDPA()
        wt.lte_bandwidths = self.wanted_bw()
        wt.fr1_bandwidths = self.wanted_bw_fr1()
        wt.channel = self.wanted_chan()
        wt.tx_max_pwr_sensitivity = self.wanted_ue_pwr()
        wt.rb_ftm_lte = self.wanted_ftm_rb_lte()
        wt.rb_ftm_fr1 = self.wanted_ftm_rb_fr1()
        wt.tx_paths = self.wanted_tx_path()
        wt.rx_paths = self.wanted_rx_path()
        wt.mcs_lte = self.wanted_mcs_lte()
        wt.mcs_fr1 = self.wanted_mcs_fr1()
        wt.type_fr1 = self.wanted_type()
        wt.scripts = self.wanted_scripts()
        # non list-lke
        wt.port_tx_lte = self.tx_port_lte.get()
        wt.port_tx_fr1 = self.tx_port_fr1.get()
        wt.band_segment = self.band_segment.get()
        wt.band_segment_fr1 = self.band_segment_fr1.get()
        wt.asw_path = self.asw_path.get()
        wt.srs_path = self.srs_path.get()
        wt.sync_path = self.sync_path.get()
        wt.sa_nas = self.sa_nsa.get()

        if self.instrument.get() == 'Anritsu8820':
            from anritsu8820 import Anritsu8820
            # import want_test_band as wt
            #
            # wt.tech = self.wanted_tech()
            # wt.fr1_bands =self.wanted_band_FR1()
            # wt.lte_bands = self.wanted_band_LTE()
            # wt.wcdma_bands = self.wanted_band_WCDMA()
            # wt.gsm_bands = self.wanted_band_GSM()
            # wt.hsupa_bands = self.wanted_band_HSUPA()
            # wt.hsdpa_bands = self.wanted_band_HSDPA()
            # wt.lte_bandwidths = self.wanted_bw()
            # wt.channel = self.wanted_chan()
            # wt.tx_max_pwr_sensitivity = self.wanted_ue_pwr()
            # wt.band_segmment = self.band_segment.get()
            # wt.band_segment_fr1 = self.band_segment_fr1.get()
            self.test_pipeline(Anritsu8820)
            # anritsu = Anritsu8820()
            #
            # if self.wanted_test['tx']:
            #     anritsu.run_tx()
            #
            # if self.wanted_test['rx']:
            #     anritsu.run_rx()
            #
            # if self.wanted_test['rx_sweep']:
            #     anritsu.run_rx_sweep_ch()

        elif self.instrument.get() == 'Anritsu8821':
            from anritsu8820 import Anritsu8821
            # import want_test_band as wt
            #
            # wt.tech = self.wanted_tech()
            # wt.lte_bands = self.wanted_band_LTE()
            # wt.lte_bandwidths = self.wanted_bw()
            # wt.channel = self.wanted_chan()
            # wt.tx_max_pwr_sensitivity = self.wanted_ue_pwr()
            # wt.band_segmment = self.band_segment.get()
            self.test_pipeline(Anritsu8821)
            # anritsu = Anritsu8821()
            #
            # if self.wanted_test['tx']:
            #     anritsu.run_tx()
            #
            # if self.wanted_test['rx']:
            #     anritsu.run_rx()
            #
            # if self.wanted_test['rx_sweep']:
            #     anritsu.run_rx_sweep_ch()

        elif self.instrument.get() == 'Agilent8960':
            pass

        elif self.instrument.get() == 'Cmw100':
            from cmw100 import Cmw100
            self.test_pipeline(Cmw100)


        stop = datetime.datetime.now()

        logger.info(f'Timer: {stop - start}')
        self.button_run['state'] = tkinter.NORMAL


if __name__ == "__main__":
    app = MainApp()
    app.run()
