tech = ['FR1']
bw_fr1 = [10]
bw_lte = [20]
ue_power = [1, 0]

chan = "LMH"

bands_fr1 = [3]
bands_lte = [3]
bands_wcdma = []
bands_hsupa = []
bands_hsdpa = []
bands_gsm = None
bands_endc = ['3_78']

tx = True
rx = False
rx_sweep = False
tx_level_sweep = False
tx_freq_sweep = False

instrument = "Cmw100"
band_segment = "A"
band_segment_fr1 = "A"

port_tx = 1
port_tx_lte = 1
port_tx_fr1 = 4
sa_nas = 0
asw_path = 0
srs_path = 0
srs_path_enable = True
sync_path = "Main"


tx_paths = ['TX1']
rx_paths = [2]

scripts = ['GENERAL']
type_fr1 = ['DFTS']
mcs_lte = ['QPSK', 'Q16', 'Q64', 'Q256']
mcs_fr1 = ['QPSK']
rb_ftm_lte = ['PRB', 'FRB']
rb_ftm_fr1 = ['INNER_FULL']
