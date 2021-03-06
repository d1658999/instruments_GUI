lte_bands = [2]       # 1,2,3,4,7,25,66,38,39,40,41,5,8,12,13,14,17,18,19,20,28,71,42,48
wcdma_bands = [1]
gsm_bands = []
hsupa_bands = [1]
hsdpa_bands = [1]
fr1_bands = [77, 78]
endc_bands = ["3_78"]  # "3_78", "2_77","66_77"
band_segment = 'A'  # 'A' | 'B' for B28A ,B28B
band_segment_fr1 = 'B'

lte_bandwidths = [10]     # 1.4, 3, 5, 10, 15, 20
fr1_bandwidths = [10]  # 10, 15, 20, 25, 30 , 40, 50, 60, 80, 90, 100, 70

tech = ['FR1']   # 'LTE' | 'WCDMA' | 'GSM' | 'HSUPA' | 'HSDPA' | 'FR1'
channel = 'LMH'  # 'LMH'

fdd_tdd_cross_test = 0     # this is only for 8821,  0: only measure one of FDD or TDD; 1: measure both FDD and TDD

tx_max_pwr_sensitivity = [1, 0]  # 1: Txmax power, 0: -10dBm

tx_level = 26
tx_level_endc_lte = 26
tx_level_endc_fr1 = 0
sa_nsa = 0
duty_cycle = 100  # 100 for NR TDD PC3, 50: for NR TDD PC2

port_tx = 1
port_tx_lte = 1  # 1 ~ 8 default is  1
# port_rx_lte = 1  # 1 ~ 8 default is  1
port_tx_fr1 = 4  # 1 ~ 8 default is  1
# port_rx_fr1 = 1  # 1 ~ 8 default is  1

asw_path = 0
srs_path = 0
srs_path_enable = False
sync_path = 'Main'  # 'Main', 'CA#1', 'CA#2', 'CA#3'
tx_paths = ['TX1']   # 'TX1' | 'TX2' | 'MIMO
rx_paths = [15]  #  0: default(free run) | 1: DRX_ONLY | 2: PRX ONLY | 3: PRX+DRX | 4: 4RX_PRX(RX2) ONLY | 8: 4RX_DRX(RX3) ONLY | 12: 4RX_PRX(RX2) + 4RX_DRX(RX3) | 15: ALL PATH

scripts = ['GENERAL']  # 'GENERAL' | 'FCC' | 'CE' | 'FACTORY'

type_fr1 = ['DFTS']  # 'DFTS' | 'CP'
mcs_lte = ['QPSK']   # 'QPSK' | 'Q16' | 'Q64' | 'Q256'
mcs_fr1 = ['QPSK', 'Q16', 'Q64', 'Q256']   # 'BPSK' | 'QPSK' | 'Q16' | 'Q64' | 'Q256'
rb_ftm_lte = ['FRB']  # 'PRB' | 'FRB'
rb_ftm_fr1 = ['OUTER_FULL']  #  'INNER_FULL' | 'OUTER_FULL' | 'INNER_1RB_LEFT' | 'INNER_1RB_RIGHT' | 'EDGE_1RB_LEFT' | 'EDGE_1RB_RIGHT' | 'EDGE_FULL_LEFT' | 'EDGE_FULL_RIGHT'
scs = [1]  # 0: 15KHz | 1: 30KHz | 2: 60KHz

tx_level_range_list = [-20, 26]  # tx_level_1, tx_level_2





def main():
    """
        test
    """
    print(wcdma_bands == [])

if __name__ == "__main__":
    main()
