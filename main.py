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

        self.equipment = None
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
        self.GSM850 = None
        self.GSM900 = None
        self.GSM_all = None
        self.GSM_none = None
        self.GSM1800 = None
        self.GSM1900 = None
        builder.import_variables(
            self,
            [
                "equipment",
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

    def select(self):
        pass

    def LB_all_checked(self, event=1):
        self.B5.set(1)
        self.B8.set(1)
        self.B12.set(1)
        self.B13.set(1)
        self.B14.set(1)
        self.B17.set(1)
        self.B18.set(1)
        self.B19.set(1)
        self.B20.set(1)
        self.B21.set(1)
        self.B26.set(1)
        self.B28.set(1)
        self.B29.set(1)
        self.B32.set(1)
        self.B71.set(1)
        self.LB_none.set(0)

    def LB_none_checked(self, event=1):
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
        self.LB_all.set(0)

    def MHB_all_checked(self, event=1):
        self.B1.set(1)
        self.B2.set(1)
        self.B25.set(1)
        self.B3.set(1)
        self.B4.set(1)
        self.B66.set(1)
        self.B7.set(1)
        self.B30.set(1)
        self.B39.set(1)
        self.B40.set(1)
        self.B38.set(1)
        self.B41.set(1)
        self.MHB_none.set(0)

    def MHB_none_checked(self, event=1):
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
        self.MHB_all.set(0)

    def UHB_all_checked(self, event=1):
        self.B42.set(1)
        self.B48.set(1)
        self.UHB_none.set(0)

    def UHB_none_checked(self, event=1):
        self.B42.set(0)
        self.B48.set(0)
        self.UHB_all.set(0)

    def WCDMA_all_checked(self, event=1):
        self.W1.set(1)
        self.W2.set(1)
        self.W4.set(1)
        self.W5.set(1)
        self.W8.set(1)
        self.W6.set(1)
        self.W19.set(1)
        self.WCDMA_none.set(0)

    def WCDMA_none_checked(self, event=1):
        self.W1.set(0)
        self.W2.set(0)
        self.W4.set(0)
        self.W5.set(0)
        self.W8.set(0)
        self.W6.set(0)
        self.W19.set(0)
        self.WCDMA_all.set(0)

    def GSM_all_checked(self, event=1):
        self.GSM850.set(1)
        self.GSM900.set(1)
        self.GSM1800.set(1)
        self.GSM1900.set(1)
        self.GSM_none.set(0)

    def GSM_none_checked(self, event=1):
        self.GSM850.set(0)
        self.GSM900.set(0)
        self.GSM1800.set(0)
        self.GSM1900.set(0)
        self.GSM_all.set(0)




if __name__ == "__main__":
    app = MainApp()
    app.run()
