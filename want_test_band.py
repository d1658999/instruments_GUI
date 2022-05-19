lte_bands = [42,48]       # 1,2,3,4,7,25,66,38,39,40,41,5,8,12,13,14,17,18,19,20,28,71,42,48
wcdma_bands = [1,2,4]
gsm_bands = []


lte_bandwidths = [10]     # 1.4,3,5,10,15,20

tech = ['LTE']  # LTE | WCDMA | GSM
channel = 'LMH'

fdd_tdd_cross_test = 0

tx_max_pwr_sensitivity = [1,0]  # 1: Txmax power, 0: -10dBm

def main():
    """
        test
    """
    print(wcdma_bands == [])

if __name__ == "__main__":
    main()
