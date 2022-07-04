tech = ['FR1']
bw_fr1 = [25, 40, 50, 60, 80, 100]
bw_lte = [1.4, 3, 5, 10, 15, 20]
ue_power = [1, 0]

chan = "M"

bands_fr1 = [48, 77, 78]
bands_lte = [42, 48]
bands_wcdma = []
bands_hsupa = []
bands_hsdpa = []
bands_gsm = None
bands_endc = ['3_78']

tx = False
rx = True
rx_sweep = False
tx_level_sweep = False
tx_freq_sweep = False

instrument = "Cmw100"
band_segment = "A"
band_segment_fr1 = "A"

port_tx = 4
port_tx_lte = 1
port_tx_fr1 = 4
sa_nas = 0
asw_path = 0
srs_path = 0
srs_path_enable = False
sync_path = "Main"


tx_paths = ['TX1']
rx_paths = [2]

scripts = ['GENERAL']
type_fr1 = ['DFTS', 'CP']
mcs_lte = ['QPSK', 'Q16', 'Q64', 'Q256']
mcs_fr1 = ['BPSK', 'QPSK', 'Q16', 'Q64', 'Q256']
rb_ftm_lte = ['PRB', 'FRB']
rb_ftm_fr1 = ['INNER_FULL', 'OUTER_FULL', 'INNER_1RB_LEFT', 'INNER_1RB_RIGHT', 'EDGE_1RB_LEFT', 'EDGE_1RB_RIGHT', 'EDGE_FULL_LEFT', 'EDGE_FULL_RIGHT']
