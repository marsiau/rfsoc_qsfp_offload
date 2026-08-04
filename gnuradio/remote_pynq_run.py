from pynq import PL
from functools import partial
from rfsoc_qsfp_offload.overlay import Overlay

PL.reset()

olf = "/home/msphd/Projects/qsfp-radio/ms-qsfp-remote/rfsoc_qsfp_offload/bitstream/qsfp_remote.xsa"
ol = Overlay(olf, ignore_version=True)

ol.cmac.mmio.write(0x107C, 0x3) # RSFEC_CONFIG_ENABLE
ol.cmac.mmio.write(0x1000, 0x7) # RSFEC_CONFIG_INDICATION_CORRECTION
ol.cmac.start()
board_ip = '192.168.4.99'
ol.netlayer.set_ip_address(board_ip, debug=True)
client_ip = '192.168.4.1'
ol.netlayer.sockets[0] = (client_ip, 60133, 60133, True)
ol.netlayer.populate_socket_table()

ol.source_select(1) # 0 - DMA | 1 - RF-ADC

ADC_TILE = 2       # ADC Tile 226
ADC_BLOCK = 0       # ADC Block 0
ADC_SAMPLE_FREQUENCY = 4915.2  # MSps
ADC_PLL_FREQUENCY    = 491.52   # MHz
ADC_FC = -800 # Centering around middle of sample rate

ol.initialise_adc(tile=ADC_TILE,
                  block=ADC_BLOCK,
                  pll_freq=ADC_PLL_FREQUENCY,
                  fs=ADC_SAMPLE_FREQUENCY,
                  fc=ADC_FC)

DAC_TILE = 0       # DAC Tile 228
DAC_BLOCK = 0       # DAC Block 0
DAC_SAMPLE_FREQUENCY = 4915.2  # MSps
DAC_PLL_FREQUENCY = 491.52   # MHz
DAC_FC = 0.0

ol.initialise_dac(tile=DAC_TILE,
                  block=DAC_BLOCK,
                  pll_freq=DAC_PLL_FREQUENCY,
                  fs=DAC_SAMPLE_FREQUENCY,
                  fc=DAC_FC)

ol.packet_generator.packetsize = 128 # 128 * 64 bytes = 8192 bytes to be sent
ol.packet_generator.enable()



set_fc = partial(ol.set_fc, ADC_TILE, ADC_BLOCK)
set_fc.__name__="set_fc"
set_decimation = partial(ol.set_decimation, ADC_TILE, ADC_BLOCK)
set_decimation.__name__="set_decimation"

#server = ServerThread(set_fc, set_decimation)
#server.start()
