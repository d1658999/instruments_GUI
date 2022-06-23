tech = ['FR1']
bw_fr1 = [10]
bw_lte = [5]
ue_power = [1]

chan = "LMH"

bands_fr1 = [28]
bands_lte = [28]
bands_wcdma = []
bands_hsupa = []
bands_hsdpa = []
bands_gsm = None

tx = True
rx = False
rx_sweep = False
tx_level_sweep = False
tx_freq_sweep = False

instrument = "Cmw100"
band_segment = "A"
band_segment_fr1 = "B"

port_tx_lte = 4
port_tx_fr1 = 1
asw_path = 0
srs_path = 0
sync_path = 0

tx_paths = ['TX1']
rx_paths = []

scripts = ['GENERAL']
type_fr1 = ['CP']
mcs_lte = ['QPSK']
mcs_fr1 = ['QPSK']
rb_ftm_lte = ['PRB', 'FRB']
rb_ftm_fr1 = ['INNER_FULL']
