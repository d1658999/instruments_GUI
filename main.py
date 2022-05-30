#!/usr/bin/python3
import pathlib
import tkinter.ttk as ttk
import pygubu

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
        self.LB_none = None
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
        self.MHB_none = None
        self.B42 = None
        self.B48 = None
        self.UHB_all = None
        self.UHB_none = None
        self.W1 = None
        self.W2 = None
        self.WCDMA_all = None
        self.WCDMA_none = None
        self.W4 = None
        self.W5 = None
        self.W8 = None
        self.W6 = None
        self.W19 = None
        self.chcoding = None
        self.GSM850 = None
        self.GSM900 = None
        self.GSM_all = None
        self.GSM_none = None
        self.GSM1800 = None
        self.GSM1900 = None
        builder.import_variables(
            self,
            [
                "instrument",
                "tx",
                "rx",
                "rx_sweep",
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
                "LB_none",
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
                "MHB_none",
                "B42",
                "B48",
                "UHB_all",
                "UHB_none",
                "W1",
                "W2",
                "WCDMA_all",
                "WCDMA_none",
                "W4",
                "W5",
                "W8",
                "W6",
                "W19",
                "chcoding",
                "GSM850",
                "GSM900",
                "GSM_all",
                "GSM_none",
                "GSM1800",
                "GSM1900",
            ],
        )

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def inst_select(self):
        print(self.instrument.get())

    def measure(self):
        print(self.B5.get())

    def band_select(self):
        print(self.B5.get())

    def off_all_none_LB(self, event=None):
        pass

    def LB_all_checked(self, event=None):
        pass

    def LB_none_checked(self, event=None):
        pass

    def off_all_none_MHB(self, event=None):
        pass

    def MHB_all_checked(self, event=None):
        pass

    def MHB_none_checked(self, event=None):
        pass

    def off_all_none_UHB(self, event=None):
        pass

    def UHB_all_checked(self, event=None):
        pass

    def UHB_none_checked(self, event=None):
        pass

    def off_all_none_WCDMA(self, event=None):
        pass

    def WCDMA_all_checked(self, event=None):
        pass

    def WCDMA_none_checked(self, event=None):
        pass

    def chcoding_select(self):
        pass

    def off_all_none_GSM(self, event=None):
        pass

    def GSM_all_checked(self, event=None):
        pass

    def GSM_none_checked(self, event=None):
        pass


if __name__ == "__main__":
    app = MainApp()
    app.run()
