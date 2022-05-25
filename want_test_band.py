lte_bands = [2,3,4,25,66]       # 1,2,3,4,7,25,66,38,39,40,41,5,8,12,13,14,17,18,19,20,28,71,42,48
wcdma_bands = [1,2,4]
gsm_bands = []
hsupa_bands = [4]
hsdpa_bands = []


lte_bandwidths = [1.4,3,5,10,15,20]     # 1.4,3,5,10,15,20

tech = ['HSUPA']  # LTE | WCDMA | GSM | HSUPA | HSDPA
channel = 'H'

fdd_tdd_cross_test = 0     #this is only for 8821,  0: only measure one of FDD or TDD; 1: measure both FDD and TDD

tx_max_pwr_sensitivity = [1, 0]  # 1: Txmax power, 0: -10dBm

def main():
    """
        test
    """
    print(wcdma_bands == [])

if __name__ == "__main__":
    main()
