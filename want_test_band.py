lte_bands = [48]       # 1,2,3,4,7,25,66,38,39,40,41,5,8,12,13,14,17,18,19,20,28,71,42,48
wcdma_bands = [1]
gsm_bands = []
hsupa_bands = [1]
hsdpa_bands = [1]
fr1_bands = [77]


lte_bandwidths = [10]     # 1.4, 3, 5, 10, 15, 20
fr1_bandwidths = [100]  # 10, 15, 20, 25, 30 , 40, 50, 60, 80, 90, 100, 70

tech = ['FR1']   # 'LTE' | 'WCDMA' | 'GSM' | 'HSUPA' | 'HSDPA' | 'FR1'
channel = 'L'  # 'LMH'

fdd_tdd_cross_test = 0     # this is only for 8821,  0: only measure one of FDD or TDD; 1: measure both FDD and TDD

tx_max_pwr_sensitivity = [1, 0]  # 1: Txmax power, 0: -10dBm

tx_level = 26
sa_nas = 0
tx_level_range_list = [-10, 27]  # tx_level_1, tx_level_2
port_lte = 1  # 1 ~ 8 default is  1
port_fr1 = 1  # 1 ~ 8 default is  1
scripts = ['GENERAL']  # 'GENERAL' | 'FCC' | 'FACTORY'
tx_path = ['TX1']   # 'TX1' | 'TX2'
type_fr1 = ['DFTS']  # 'DFTS' | 'CP'
mcs_lte = ['QPSK']   # 'QPSK' | 'Q16' | 'Q64' | 'Q256'
mcs_fr1 = ['QPSK', 'Q256']   # 'BPSK' | 'QPSK' | 'Q16' | 'Q64' | 'Q256'
rb_ftm_lte = ['PRB']  # 'PRB' | 'FRB'
rb_ftm_fr1 = ['INNER_FULL']  #  'INNER_FULL' | 'OUTER_FULL' | 'INNER_1RB_LEFT' | 'INNER_1RB_RIGHT' | 'EDGE_1RB_LEFT' | 'EDGE_1RB_RIGHT' | 'EDGE_FULL_LEFT' | 'EDGE_FULL_RIGHT'
scs = [1]  # 0: 15KHz | 1: 30KHz | 2: 60KHz




def main():
    """
        test
    """
    print(wcdma_bands == [])

if __name__ == "__main__":
    main()
