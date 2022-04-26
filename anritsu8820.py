import pyvisa
import time
import datetime
from decimal import Decimal

from loss_table import loss_table
import common_parameters as cm_pmt
import want_test_band as wt


# rm = pyvisa.ResourceManager()
# for rs in rm.list_resources():
#     if 'GPIB0' in rs:
#         print(rs)
#         inst = rm.open_resource(rs)
# print(inst.query("*IDN?"))

class Anritsu8820:
    def __init__(self, resource_name):
        self.resource_name = resource_name
        try:
            self.build_object()
        except:
            print('Error to connect to instrument')

    def build_object(self):
        print('start to connect')
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.resource_name)
        self.inst.timeout = 5000
        print(self.inst.query('*IDN?'))

    def query_standard(self):
        return self.inst.query("STDSEL?").strip()

    def switch_to_wcdma(self):
        """
            switch to WCDMA mode
            switch ok => return 0
            switch fail => return 1
        """
        s = self.query_standard()  # WCDMA|GSM|LTE
        print("Current Function: " + s)
        if s == 'WCDMA':
            print("Already WCDMA mode")
            return s
        else:
            self.inst.write('STDSEL WCDMA')  # switch to WCDMA
            time.sleep(1)
            if (self.query_standard() == 'WCDMA'):
                print("Switch to WCDMA mode OK")
                return self.query_standard()
            else:
                print("Switch to WCDMA mode fail")
                return 1

    def switch_to_gsm(self):
        """
            switch to GSM mode
            switch ok => return 0
            switch fail => return 1
        """
        s = self.query_standard()  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'GSM':
            print("Already GSM mode")
            return s
        else:
            self.inst.write('STDSEL GSM')  # switch to GSM
            time.sleep(1)
            if (self.query_standard() == "GSM"):
                print("Switch to GSM mode OK")
                return self.query_standard()
            else:
                print("Switch to GSM mode fail")
                return 1

    def switch_to_lte(self):
        """
            switch to LTE mode
            switch ok => return 0
            switch fail => return 1
        """
        s = self.query_standard()  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'LTE':
            print("Already LTE mode")
            return s
        else:
            self.inst.write('STDSEL LTE')  # switch to LTE
            time.sleep(1)
            if (self.query_standard() == 'LTE'):
                print("Switch to LTE mode OK")
                return self.query_standard()
            else:
                print("Switch to LTE mode fail")
                return 1

    def preset(self):
        """
            preset Anritsu 8820C
        """
        print("Preset Anritsu 8820C")
        s = self.query_standard()  # WCDMA|GSM|LTE|CDMA2K
        if s == 'WCDMA':
            self.preset_3gpp()
        else:
            self.inst.write("*RST")  # this command changes measurement count to "single"
        self.inst.write("*CLS")
        self.inst.write("ALLMEASITEMS_OFF")  # Set all measurements to off

    def preset_3gpp(self):
        """
            preest to 3GPP spec (for WCDMA)
        """
        self.inst.write("PRESET_3GPP")

    def preset_extarb(self):
        self.inst.write('PRESET_EXTARB')

    def set_test_parameter_normal(self):
        self.inst.write('TESTPRM NORMAL')
        self.inst.write('ULRMC_64QAM DISABLED')

    def set_init_before_calling(self, standard, dl_ch, bw=5):
        s = standard
        if s == 'LTE':
            self.set_init_before_calling_lte(dl_ch, bw)
        elif s == 'WCDMA':
            self.set_registration_calling_wcdma(dl_ch)
        elif s == 'GSM':
            pass

    def set_init_before_calling_wcdma(self, dl_ch):
        """
            preset before start to calling for WCDMA
        """
        self.preset()
        self.set_band_cal()
        self.set_screen_on()
        self.set_display_remain()
        self.set_test_mode('OFF')
        self.set_integrity('WCDMA', 'ON')
        self.set_imsi()
        self.set_all_measurement_items_off()
        self.set_init_miscs('WCDMA')
        self.set_path_loss('WCDMA')
        self.set_init_level('WCDMA')
        self.set_handover('WCDMA', dl_ch)
        self.inst.query('*OPC?')

    def set_init_before_calling_lte(self, dl_ch, bw):
        """
            preset before start to calling for LTE
        """
        self.preset()
        self.set_band_cal()
        self.set_screen_on()
        self.set_display_remain()
        self.preset_extarb()
        self.set_lvl_status('OFF')
        # if 53 >= band >= 33:
        #     self.set_fdd_tdd_mode('FDD')
        # else:
        #     self.set_fdd_tdd_mode('TDD')
        self.set_test_mode('OFF')
        self.set_integrity('LTE', 'SNOW3G')
        self.set_scenario()
        self.set_pdn_type()
        self.set_mcc_mnc()
        self.set_ant_config()
        self.set_imsi()
        self.set_all_measurement_items_off()
        self.set_init_miscs('LTE')
        self.set_path_loss('LTE')
        self.set_init_level('LTE')
        self.set_handover('LTE', dl_ch, bw)
        self.inst.write('ULRB_POS MIN')
        self.inst.query('*OPC?')

    def set_path_loss(self, standard):
        self.inst.write('DELLOSSTBL')  # delete the unknown loss table first

        loss_title = 'LOSSTBLVAL'
        freq = sorted(loss_table.keys())
        for keys in freq:
            loss = f'{loss_title} {str(keys)}MHZ, {str(loss_table[keys])}, {str(loss_table[keys])}, {str(loss_table[keys])}'
            print(loss)
            self.inst.write(loss)
        s = standard  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'LTE':
            self.inst.write("EXTLOSSW COMMON")
            self.inst.query('*OPC?')
        elif s == 'WCDMA':
            self.inst.write("DLEXTLOSSW COMMON")  # Set DL external loss to COMMON
            self.inst.write("ULEXTLOSSW COMMON")  # Set UL external loss to COMMON
            self.inst.write("AUEXTLOSSW COMMON")  # Set AUX external loss to COMMON
            self.inst.query('*OPC?')
        elif s == "GSM":
            self.inst.write("EXTLOSSW COMMON")
            self.inst.query('*OPC?')

    def set_init_level(self, standard):
        """
            LTE:
                initial input_level=5 and output_level=-60
            WCDMA:
                initial input_level=5 and output_level=-75
        """
        s = standard
        if s == 'LTE':
            self.set_input_level()
            self.set_output_level()
            self.inst.query('*OPC?')
        elif s == 'WCDMA':
            self.set_input_level()
            self.set_output_level(-75)
            self.inst.query('*OPC?')
        elif s == 'GSM':
            pass

    def set_registration_calling(self, standard):
        s = standard
        print("Current Format: " + s)
        if s == 'LTE':
            self.set_registration_calling_lte()
        elif s == 'WCDMA':
            self.set_registration_calling_wcdma()
        elif s == 'GSM':
            pass

    def set_registration_calling_lte(self, times=30):
        """
            ANRITSU_IDLE = 1	        #Idle state
            ANRITSU_REGIST = 3			# Under location registration
            ANRITSU_CONNECTED = 6	    # Under communication or connected
        """
        self.inst.write('CALLTHLD 1')
        self.set_lvl_status('ON')
        self.set_test_mode()
        conn_state = int(self.inst.query("CALLSTAT?").strip())
        while conn_state != cm_pmt.ANRITSU_CONNECTED:
            self.inst.write('CALLRFR')
            while conn_state != cm_pmt.ANRITSU_CONNECTED:
                # if int(conn_state) == cm_pmt.ANRITSU_IDLE:
                print('IDLE')
                time.sleep(1)
                conn_state = int(self.inst.query("CALLSTAT?").strip())
                # elif int(conn_state) == cm_pmt.ANRITSU_REGIST:
                #     conn_state = self.inst.query("CALLSTAT?")
                #     self.inst.query('*OPC?')
                #     print('Registration')
                #     time.sleep(1)
            conn_state = int(self.inst.query("CALLSTAT?").strip())
            self.inst.write('CALLSA')
            self.inst.query('*OPC?')
            print('Connected')
            time.sleep(1)

    def set_registration_calling_wcdma(self, times=30):
        """
            ANRITSU_IDLE = 1	        #Idle state
            ANRITSU_IDLE_REGIST = 2		#Idle( Regist ) Idle state (location registered)
            ANRITSU_LOOP_MODE_1 = 7	    # Under communication or connected
        """
        conn_state = int(self.inst.query("CALLSTAT?").strip())
        while conn_state != cm_pmt.ANRITSU_LOOP_MODE_1:
            while conn_state != cm_pmt.ANRITSU_IDLE_REGIST:
                if conn_state == cm_pmt.ANRITSU_IDLE:
                    print('IDLE')
                    time.sleep(5)
                elif conn_state == cm_pmt.ANRITSU_IDLE_REGIST:
                    print('IDLE(register)')
                    self.inst.query('*OPC?')
                    time.sleep(2)
            conn_state = int(self.inst.query("CALLSTAT?").strip())
            self.inst.write('CALLSA')
            self.inst.query('*OPC?')
            time.sleep(3)

    def set_disconnected(self):
        self.inst.write('CALLSO')
        self.inst.write('CALLPROC OFF')
        self.inst.query('*OPC?')
        print('DISCONNECTED')

    def set_handover(self, standard, dl_ch, bw=5):
        s = standard  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'LTE':
            self.set_bandwidth(bw)
            self.set_downlink_channel(s, dl_ch)
            # ul_ch = self.inst.query('ULCHAN?')
            self.inst.query('*OPC?')
            # if ul_ch != dl_ch:
            #     self.set_fdd_tdd_mode('FDD')
            # elif ul_ch == dl_ch:
            #     self.set_fdd_tdd_mode('TDD')
            # else:
            #     print('comparison between ul_ch and dl_ch seems like error!')
        elif s == ('WCDMA' or 'GSM'):
            self.set_downlink_channel(dl_ch)
            self.inst.query('*OPC?')
        else:
            print('Standard switch @handover function seems like error!')

    def set_fdd_tdd_mode(self, fdd_tdd):
        self.inst.write(f'FRAMETYPE {fdd_tdd}')  # FDD|TDD

    def set_test_mode(self, on_off='ON'):  # this is to set call progress ON
        self.inst.write(f"CALLPROC {on_off}")  # default = ON | OFF for signaling | non-signaling

    def set_imsi(self, imsi=cm_pmt.IMSI):
        self.inst.write(f'IMSI {imsi}')

    # def set_imei(self, IMEI):
    #     self.inst.write(IMEI)

    def set_screen_on(self):
        self.inst.write('SCREEN ON')

    def set_display_remain(self):
        self.inst.write('REMDISP REMAIN')

    def set_lvl_status(self, on_off):
        self.inst.write(f'LVL {on_off}')

    def set_bandwidth(self, bw=5):
        self.inst.write(f'BANDWIDTH {str(bw)}MHZ')

    def set_scenario(self, mode='NORMAL'):
        self.inst.write(f'SCENARIO {mode}')  # default = NORMAL

    def set_pdn_type(self):
        self.inst.write('PDNTYPE AUTO')

    def set_mcc_mnc(self, mcc='001', mnc='01'):
        self.inst.write(f'MCC {mcc}')
        self.inst.write(f'MNC {mnc} ')

    def set_ant_config(self, ant='SINGLE'):
        self.inst.write(f'ANTCONFIG {ant}')  # default =  SINGLE | RX_DIVERSITY | OPEN_LOOP | CLOSED_LOOP_MULTI

    def set_band_cal(self):
        self.inst.query('BANDCAL_TEMP 2.0;*OPC?')

    def set_integrity(self, standard, status):
        s = standard
        if s == 'LTE':
            self.inst.write(f'INTEGRITY {status}')  # SNOW3G | NULL | OFF
        elif s == 'WCDMA':
            self.inst.wrtie(f'INTEGRITY {status}')  # ON | OFF
        elif s == 'GSM':
            pass

    def set_authentication(self):
        self.inst.write('AUTHENT ON')
        self.inst.write('AUTHENT_ALGO XOR')
        self.inst.write('AUTHENT_KEYALL 00112233,44556677,8899AABB,CCDDEEFF')
        self.inst.write('OPC_ALL 00000000,00000000,00000000,00000000')

    def set_init_miscs(self, standard):
        s = standard
        if s == 'LTE':
            self.inst.write('RRCUPDATE PAGING')
            self.inst.write('PT_TRGSRC FRAME')
            self.inst.write('MODIFPERIOD N2')
            self.inst.write('PCYCLE 32')
            self.inst.write('RRCRELEASE OFF')
            self.inst.write('FREQERRRNG NARROW')  # NORMAL | NARROW
            self.inst.write('ROBUSTCON OFF')  # ON | OFF
            self.inst.write('TESTMODE OFF')
            self.inst.write('UECAT CAT3')
            self.inst.write('SIB2_NS NS_01')

        elif s == 'WCDMA':
            self.inst.write('ATTFLAG OFF')
            self.inst.write('MEASREP OFF')
            self.inst.write('DRXCYCLNG 64')
        elif s == 'GSM':
            pass

    def set_input_level(self, input_level=5):
        self.inst.write(f'ILVL {str(input_level)}')

    def set_output_level(self, output_level=-60):
        self.inst.write(f'OLVL {str(output_level)}')

    def set_tpc(self, tpc='ILPC'):
        """
        	set UL target power control mode, default is ILPC(inner loop control)
        """
        self.inst.write(f'TPCPAT {tpc}')  # WCDMA default= ILPC | ALL1 | ALL0 | ALT | UCMD
        # self.inst.write(f'TPCPAT {tpc}')  # LTE default= AUTO | ALL3 |ALL1 | ALL0 | ALLM1| ALT | UCMD

    def set_uplink_channel(self, standard,ul_ch):
        """
            Use this function only in FDD test mode.
            For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == ('LTE' or 'WCDMA'):
            return self.inst.write(f'ULCHAN {str(ul_ch)}')

        elif s == 'GSM':
            pass

    def set_downlink_channel(self, standard, dl_ch):
        """
        	Use this function only in FDD test mode
        	For Anritsu8820C, it could be used in link mode
        """
        s = standard
        if s == ('LTE' or 'WCDMA'):
            return self.inst.write(f'DLCHAN {str(dl_ch)}')
        elif s == 'GSM':
            pass

    def set_init_power(self, count=1):
        self.inst.write('PWR_MEAS ON')  # Set [Power Measurement] to [On]
        self.inst.write(f'PWR_AVG {count}')  # Set [Average Count] to [count] times

    def set_init_aclr(self, standard, count=1):
        s = standard
        if s == 'LTE':
            self.inst.write('ACLR_MEAS ON')  # Set [ACLR Measurement] to [On]
            self.inst.write(f'ACLR_AVG {count}')  # Set [ACLR Count] to [count] times
        elif s == 'WCDMA':
            self.inst.write('ADJ_MEAS ON')  # Set [ACLR Measurement] to [On]
            self.inst.write(f'ADJ_AVG {count}')  # Set [ACLR Count] to [count] times
        elif s =='GSM':
            pass

    def set_init_sem(self, count=1):
        self.inst.write('SEM_MEAS ON')  # Set [SEM Measurement] to [On]
        self.inst.write(f'SEM_AVG {count}')  # Set [SEM Count] to [count] times

    def set_init_obw(self, count=20):
        self.inst.write('OBW_MEAS ON')  # Set [OBW Measurement] to [On]
        self.inst.write(f'OBW_AVG {count}')  # Set [OBW Count] to [count] times

    def set_init_mod(self, standard, count=1):
        """
        this for EVM usage and some other modulation
        Set the average measurement count to 16 times because the average for 16 timeslots is described in the standards
        for 6.5.2.1A PUSCH-EVM with exclusion period
        """
        s = standard
        if s == 'LTE':
            self.inst.write('MOD_MEAS ON')  # Set [MOD Measurement] to [On]
            self.inst.write(f'MOD_AVG {count}')  # Set [MOD Count] to [count] times
        elif s == 'WCDMA':
            self.inst.write('INC_ORGNOFS ON')  # set [EVM include Origin Offset] to [On]
            self.inst.write('MOD_MEAS ON')  # Set [MOD Measurement] to [On]
            self.inst.write(f'MOD_AVG {count}')  # Set [MOD Count] to [count] times
        elif s == 'GSM':
            pass

    def set_init_power_template(self, standard,count=1):
        s = standard
        if s == 'LTE':
            self.inst.write('PWRTEMP ON')  # Set [OBW Measurement] to [On]
            self.inst.write(f'PWRTEMP_AVG {count}')  # Set [OBW Count] to [count] times
        elif s == 'WCDMA':
            self.inst.write('PT_WDR ON')  # Set [OBW Measurement] to [On]
            self.inst.write(f'PT_WDR_AVG {count}')  # Set [OBW Count] to [count] times
        elif s == 'GSM':
            pass

    def set_all_measurement_items_off(self):
        self.inst.write("ALLMEASITEMS_OFF")

    def set_to_measure(self):
        """
            Anritsu8820 use 'SWP' to measure no matter what the test items are
        """
        self.inst.write('SWP')

    def get_validation(self, standard):
        s = standard  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'LTE':
            return self.get_power_aclr_evm_lte()
        elif s == 'WCDMA':
            return self.get_power_aclr_evm_wcdma()
        elif s == 'GSM':
            pass

    def get_power_aclr_evm_lte(self):
        """
            Only measure RB@min
            The format in dictionary is {Q_1: [power, aclr, evm], Q_P: [power, aclr, evm], ...}
            and ACLR format is [EUTRA-1, EUTRA+1, UTRA-1, URTA+1, UTRA-2, URTA+2,]
        """
        want_mods = [
            'TESTPRM TX_MAXPWR_Q_1',
            'TESTPRM TX_MAXPWR_Q_P',
            'TESTPRM TX_MAXPWR_Q_F',
            'TESTPRM TX_MAXPWR_16_P',
            'TESTPRM TX_MAXPWR_16_F',
            'TESTPRM TX_MAXPWR_64_P',
            'TESTPRM TX_MAXPWR_64_F',
        ]

        validation_dict = {}

        self.set_init_power()
        self.set_init_aclr('LTE')
        self.set_init_mod('LTE')
        self.set_input_level(26)
        self.set_tpc('ALL3')
        self.inst.query('*OPC?')

        for mod in want_mods:
            # the four line is for waiting connected before change modulation
            conn_state = int(self.inst.query("CALLSTAT?").strip())
            while conn_state != cm_pmt.ANRITSU_CONNECTED:
                time.sleep(1)
                print('wait 1 second to connect')
                conn_state = int(self.inst.query("CALLSTAT?").strip())

            validation_list = []
            if mod == 'TESTPRM TX_MAXPWR_64_P':
                self.inst.write('TESTPRM TX_MAXPWR_Q_P')
                self.inst.write('ULRMC_64QAM ENABLED')
                self.inst.write('ULIMCS 21')
            elif mod == 'TESTPRM TX_MAXPWR_64_F':
                self.inst.write('TESTPRM TX_MAXPWR_Q_F')
                self.inst.write('ULRMC_64QAM ENABLED')
                self.inst.write('ULIMCS 21')
            else:
                self.inst.write('ULRMC_64QAM DISABLED')
                self.inst.write(mod)

            self.set_to_measure()
            # self.inst.query('MSTAT?')
            # self.inst.query('*OPC?')

            if mod == 'TESTPRM TX_MAXPWR_Q_1':  # mod[18:] -> Q_1
                print(mod)
                validation_list.append(self.get_uplink_power('LTE'))
                validation_dict[mod[18:]] = validation_list
                # self.inst.query('*OPC?')
            else:  # mod[18:] -> Q_P, Q_F, 16_P, 16_F, 64_F
                print(mod)
                validation_list.append(self.get_uplink_power('LTE'))
                validation_list.append(self.get_uplink_aclr('LTE'))
                validation_list.append(self.get_uplink_evm('LTE'))
                validation_dict[mod[18:]] = validation_list
                self.inst.query('*OPC?')
        print(validation_dict)
        return validation_dict

    def get_power_aclr_evm_wcdma(self):
        """
            Only measure RB@min
            The format in dictionary is [power, aclr, evm]
            and ACLR format is [UTRA-1, URTA+1, UTRA-2, URTA+2,]
        """

        self.set_init_power()
        self.set_init_aclr('WCDMA')
        self.set_init_mod('WCDMA')
        self.set_input_level(26)
        self.set_output_level(-106)
        self.set_tpc('ALL1')
        self.inst.query('*OPC?')

        validation_list = []
        self.set_to_measure()

        validation_list.append(self.get_uplink_power('WCDMA'))
        validation_list.append(self.get_uplink_aclr('WCDMA'))
        validation_list.append(self.get_uplink_evm('WCDMA'))
        self.inst.query('*OPC?')
        print(validation_list)
        return validation_list

    def get_uplink_power(self, standard):
        """
            Get UL power
        """
        s = standard  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'LTE':
            power = Decimal(self.inst.query('POWER? AVG'))
            self.inst.query('*OPC?')
            print(f'POWER: {power}')
            return power
        elif s == 'WCDMA':
            power = Decimal(self.inst.query('AVG_POWER?'))
            self.inst.query('*OPC?')
            return power
        elif s == 'GSM':
            pass

    def get_uplink_aclr(self, standard):
        """
            LTE:
                Get LTE ACLR
                return in [LOW5, UP5, LOW10, UP10,] format
        """
        s = standard  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        aclr = []
        if s == 'LTE':
            aclr.append(Decimal(self.inst.query('MODPWR? E_LOW1,AVG')))
            aclr.append(Decimal(self.inst.query('MODPWR? E_UP1,AVG')))
            aclr.append(Decimal(self.inst.query('MODPWR? LOW1,AVG')))
            aclr.append(Decimal(self.inst.query('MODPWR? UP1,AVG')))
            aclr.append(Decimal(self.inst.query('MODPWR? LOW2,AVG')))
            aclr.append(Decimal(self.inst.query('MODPWR? UP2,AVG')))
            self.inst.query('*OPC?')
            print(f'ACLR: {aclr}')
            return aclr
        elif s == 'WCDMA':
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? LOW5')))
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? UP5')))
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? LOW10')))
            aclr.append(Decimal(self.inst.query('AVG_MODPWR? UP10')))
            self.inst.query('*OPC?')
            return aclr
        elif s == 'GSM':
            pass

    def get_uplink_evm(self,standard):
        """
            Get Error Vector Magnitude (EVM) - PUSCH @ max power
        """
        s = standard  # WCDMA|GSM|LTE
        print("Current Format: " + s)
        if s == 'LTE':
            evm = Decimal(self.inst.query('EVM? AVG'))
            self.inst.query('*OPC?')
            print(f'evm: {evm}')
            return evm
        elif s == 'WCDMA':
            evm = Decimal(self.inst.query('AVG_EVM?'))
            self.inst.query('*OPC?')
            return evm
        elif s == 'GSM':
            pass


def get_resource():
    resource_name = None
    rm = pyvisa.ResourceManager()
    for rs in rm.list_resources():
        if 'GPIB0' in rs:
            resource_name = rs
    return resource_name


def run(resource_name):
    anritsu = Anritsu8820(resource_name)
    if wt.lte_bands != []:
        standard = anritsu.switch_to_lte()
        print(standard)
        for bw in wt.lte_bandwidths:
            for band in wt.lte_bands:
                if bw in cm_pmt.bandwidths_selected(band):
                    anritsu.set_test_parameter_normal()
                    for dl_ch in cm_pmt.dl_ch_selected(standard, band, bw):
                        print(f'Start to measure B{band}, bandwidth: {bw} MHz, downlink_chan: {dl_ch}')
                        conn_state = int(anritsu.inst.query("CALLSTAT?").strip())
                        if conn_state != cm_pmt.ANRITSU_CONNECTED:
                            anritsu.set_init_before_calling(standard, dl_ch, bw)
                            anritsu.set_registration_calling(standard)
                        anritsu.set_handover(standard, dl_ch, bw)
                        anritsu.get_validation(standard)
                else:
                    print(f'B{band} do not have BW {bw}MHZ')
    elif wt.wcdma_bands != []:
        standard = anritsu.switch_to_wcdma()
        for band in wt.wcdma_bands:
            for dl_ch in cm_pmt.dl_ch_selected(standard, band):
                print(f'Start to measure B{band}, downlink_chan: {dl_ch}')
                anritsu.set_init_before_calling(standard, dl_ch)
                anritsu.set_registration_calling(standard)
                anritsu.get_validation(standard)
    elif wt.gsm_bands != []:
        pass
    else:
        print(f'there are any bands selected')


def main():
    start = datetime.datetime.now()

    resource_name = get_resource()
    run(resource_name)

    stop = datetime.datetime.now()

    print(f'Timer: {stop - start}')


if __name__ == '__main__':
    main()
