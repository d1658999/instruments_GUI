# bandwidth index
def bandwidths_selected(band):
    bandwidths = {
        'B1': [5, 10 , 15, 20],
        'B2': [1.4, 3, 5, 10 , 15, 20],
        'B3': [1.4, 3, 5, 10 , 15, 20],
        'B4': [1.4, 3, 5, 10 , 15, 20],
        'B5': [1.4, 3, 5, 10],
        'B7': [5, 10 , 15, 20],
        'B8': [1.4, 3, 5, 10],
        'B12': [1.4, 3, 5, 10],
        'B13': [5, 10],
        'B14': [5, 10],
        'B17': [5, 10],
        'B18': [5, 10, 15],
        'B19': [5, 10, 15],
        'B20': [5, 10 , 15, 20],
        'B21': [5, 10, 15],
        'B25': [1.4, 3, 5, 10 , 15, 20],
        'B26': [1.4, 3, 5, 10 , 15],
        'B28': [3, 5, 10, 15, 20],
        'B29': [3, 5, 10],
        'B30': [5, 10],
        'B32': [5, 10, 15, 20],
        'B38': [5, 10, 15, 20],
        'B39': [5, 10, 15, 20],
        'B40': [5, 10, 15, 20],
        'B41': [5, 10, 15, 20],
        'B42': [5, 10, 15, 20],
        'B46': [10, 20],
        'B48': [5, 10, 15, 20],
        'B66': [1.4, 3, 5, 10 , 15, 20],
        'B70': [5, 10, 15, 20],
        'B71': [5, 10, 15, 20],
        'B75': [5, 10, 15, 20],
    }

    return bandwidths[f'B{band}']

# DL Freq
def dl_freq_selected(standard, band, bw=5):
    band_dl_freq_lte = {
        'B1': [2110 + bw / 2, 2140, 2170 - bw / 2],
        'B2': [1930 + bw / 2, 1960, 1990 - bw / 2],
        'B3': [1805 + bw / 2, 1842.5, 1880 - bw / 2],
        'B4': [2110 + bw / 2, 2132.5, 2155 - bw / 2],
        'B5': [869 + bw / 2, 881.5, 894 - bw / 2],
        'B7': [2620 + bw / 2, 2655, 2690 - bw / 2],
        'B8': [925 + bw / 2, 942.5, 960 - bw / 2],
        'B12': [729 + bw / 2, 727.5, 746 - bw / 2],
        'B13': [746 + bw / 2, 751, 756 - bw / 2],
        'B14': [758 + bw / 2, 762, 768 - bw / 2],
        'B17': [734 + bw / 2, 740, 746 - bw / 2],
        'B18': [860 + bw / 2, 867.5, 875 - bw / 2],
        'B19': [875 + bw / 2, 882.5, 890 - bw / 2],
        'B20': [791 + bw / 2, 806, 821 - bw / 2],
        'B21': [1495.9 + bw / 2, 1503.5, 1510.9 - bw / 2],
        'B25': [1930 + bw / 2, 1962.5, 1995 - bw / 2],
        'B26': [859 + bw / 2, 876.5, 894 - bw / 2],
        'B28': [758 + bw / 2, 780.5, 803 - bw / 2],
        'B29': [717 + bw / 2, 722.5, 728 - bw / 2],
        'B30': [2350 + bw / 2, 2355, 2360 - bw / 2],
        'B32': [1452 + bw / 2, 1474, 1496 - bw / 2],
        'B38': [2570 + bw / 2, 2595, 2620 - bw / 2],
        'B39': [1880 + bw / 2, 1900, 1920 - bw / 2],
        'B40': [2300 + bw / 2, 2350, 2400- bw / 2],
        'B41': [2496 + bw / 2, 2593, 2690 - bw / 2],
        'B42': [3400 + bw / 2, 3500, 3600 - bw / 2],
        'B46': [5150 + bw / 2, 5537.5, 5925 - bw / 2],
        'B48': [3550 + bw / 2, 3625, 3700 - bw / 2],
        'B66': [2110 + bw / 2, 2155, 2200 - bw / 2],
        'B71': [617 + bw / 2, 634.5, 652 - bw / 2],
        'B75': [1432 + bw / 2, 1474.5, 1517 - bw / 2],

    }

    band_dl_freq_wcdma = {
        'B1': [2110, 2140, 2170],
        'B2': [1930, 1960, 1990],
        'B4': [2110, 2132.5, 2155],
        'B5': [860, 881.5, 894],
        'B8': [925, 942.5, 960],
        'B6': [875, 880, 885],
        'B9': [1845, 1862.4, 1879.8],
        'B19': [875, 882.5, 890],

    }

    if standard == 'LTE':
        return [int(freq * 1000) for freq in band_dl_freq_lte[f'B{band}']]
    elif standard == 'WCDMA':
        return [int(freq * 1000) for freq in band_dl_freq_wcdma[f'B{band}']]
    elif 'GSM':
        pass

def transfer_freq_rx2tx_lte(band_lte, freq):
    if band_lte not in [38, 39, 40, 41, 42, 48]:
        spacing_lte = {
            1: -190000,
            2: -80000,
            3: -95000,
            4: -400000,
            5: -45000,
            7: -120000,
            8: -45000,
            12: -30000,
            13: 31000,
            14: 30000,
            17: -30000,
            18: -45000,
            19: -45000,
            20: 41000,
            21: -48000,
            25: -80000,
            26: -45000,
            28: -55000,
            30: -45000,
            66: -400000,
            71: 46000,

        }

        return freq + spacing_lte[band_lte]
    else:
        return freq

def transfer_freq_tx2rx_lte(band_lte, freq):
    if band_lte not in [38, 39, 40, 41, 42, 48]:
        spacing_lte = {
            1: 190000,
            2: 80000,
            3: 95000,
            4: 400000,
            5: 45000,
            7: 120000,
            8: 45000,
            12: 30000,
            13: -31000,
            14: -30000,
            17: 30000,
            18: 45000,
            19: 45000,
            20: -41000,
            21: 48000,
            25: 80000,
            26: 45000,
            28: 55000,
            30: 45000,
            66: 400000,
            71: -46000,

        }

        return freq + spacing_lte[band_lte]
    else:
        return freq

def special_uplink_config_sensitivity(band, bw):
    if (int(band) in [2,3,25]) and int(bw) == 15:
        return 50, 25
    elif (int(band) in [2,3,25]) and int(bw) == 20:
        return 50, 50
    elif int(band) in [5,8,18,19,21,26,28,30]  and int(bw) == 10:
        return 25, 25
    elif int(band) == 7 and int(bw) == 20:
        return 75, 25
    elif int(band) == 7 and int(bw) == 20:
        return 75, 25
    elif int(band) in [12,17] and int(bw) == 5:
        return 20, 5
    elif int(band) == 12 and int(bw) == 10:
        return 20, 30
    elif int(band) == 13 and (int(bw) in [5,10]):
        return 20, 0
    elif int(band) == 14 and (int(bw) in [5,10]):
        return 15, 0
    elif int(band) == 17 and int(bw) == 10:
        return 20, 30
    elif (int(band) == 18 in [18,19,21,26,28]) and int(bw) == 15:
        return 25, 50
    elif int(band) == 20 and int(bw) == 10:
        return 20, 0
    elif int(band) == 20 and int(bw) == 15:
        return 20, 11
    elif int(band) == 20 and int(bw) == 20:
        return 20, 16
    elif int(band) == 28 and int(bw) == 20:
        return 25, 75
    else:
        if int(bw) == 1.4:
            return 6, 0
        else:
            return int(bw) * 5, 0





def main():
    """
    this main() function is used for testing some function
    """

    if CHAN_LIST:
        print(CHAN_LIST)
    else:
        print('others')


if __name__ == "__main__" :
    main()
