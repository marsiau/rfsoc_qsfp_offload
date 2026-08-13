__author__ = "David Northcote, Josh Goldsmith, Marius Siauciulis"

from pynq import Overlay
import os
import time
import xrfdc
import xrfclk
from . import networkLayer
from . import signal_generator
from . import fifo_control
from . import packet_generator

# "SAMPLE_FREQUENCY" : (DecimationFactor, XRFDC_FAB_CLK_DIVx)
fs2div = {
    '4915200000.0': (1,0),
    '2457600000.0': (2,2),
    '1228800000.0': (4,3),
    '614400000.0':  (8,4),
    '307200000.0':  (16,5)
}


def _resolve_bitfile_name(bitfile_name):
    """Resolve user inputs onto a downloadable bitstream.

    PYNQ can parse `.xsa` files directly, but the XSA exported for this
    design contains inconsistent AXIS metadata for `netlayer_switch`.
    Prefer the packaged `.bit`/`.hwh` pair whenever an XSA or HWH path is
    supplied.
    """
    if bitfile_name is None:
        this_dir = os.path.dirname(__file__)
        return os.path.join(this_dir, 'bitstream', 'rfsoc_offload.bit')

    bitfile_name = os.path.abspath(os.path.expanduser(bitfile_name))
    if not os.path.isfile(bitfile_name):
        raise ValueError("Bitstream does not exist.")

    ext = os.path.splitext(bitfile_name)[1].lower()
    if ext not in ('.xsa', '.hwh'):
        return bitfile_name

    same_stem_bit = os.path.splitext(bitfile_name)[0] + '.bit'
    if os.path.isfile(same_stem_bit):
        return same_stem_bit

    sibling_bits = sorted(
        os.path.join(os.path.dirname(bitfile_name), name)
        for name in os.listdir(os.path.dirname(bitfile_name))
        if name.endswith('.bit')
    )
    if len(sibling_bits) == 1:
        return sibling_bits[0]

    raise ValueError(
        "This overlay must be loaded from a .bit file. "
        "The packaged XSA metadata is not parseable by PYNQ for this design."
    )

class Overlay (Overlay):
    """Class for the RFSoC offload overlay
    """
    
    def __init__(self, bitfile_name=None, **kwargs):
        """Initialise the overlay and drivers.
        """
        bitfile_name = _resolve_bitfile_name(bitfile_name)

        # Initialise Overlay class
        print(f"Initing with {bitfile_name}")
        super().__init__(bitfile_name, **kwargs)
        self.init_rf_clks()
        
    def init_rf_clks(self, lmk_freq=245.76, lmx_freq=491.52):
        """Initialise the LMX and LMK clocks for RF-DC operation.
        """
        print(f"xrfclk.set_ref_clks(lmk_freq={lmk_freq}, lmx_freq={lmx_freq})")
        xrfclk.set_ref_clks(lmk_freq=lmk_freq, lmx_freq=lmx_freq)
        
    def initialise_adc(self, tile, block, pll_freq=491.52, fs=4915.2, fc=0.0):
        """Initialise an ADC tile and block in bypass mode.
        """
        self.rfdc.adc_tiles[tile].DynamicPLLConfig(1, pll_freq, fs)
        self.rfdc.adc_tiles[tile].blocks[block].NyquistZone = 1
        self.rfdc.adc_tiles[tile].blocks[block].MixerSettings = {
            'CoarseMixFreq':  xrfdc.COARSE_MIX_BYPASS,
            'EventSource':    xrfdc.EVNT_SRC_TILE,
            'FineMixerScale': xrfdc.MIXER_SCALE_1P0,
            'Freq':           fc,
            'MixerMode':      xrfdc.MIXER_MODE_R2C,
            'MixerType':      xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset':    0.0
        }
        self.rfdc.adc_tiles[tile].blocks[block].UpdateEvent(xrfdc.EVENT_MIXER)
        self.rfdc.adc_tiles[tile].SetupFIFO(True)
        
    def initialise_dac(self, tile, block, pll_freq=491.52, fs=2457.60, fc=0.0):
        """Initialise a DAC tile and block in bypass mode.
        """
        self.rfdc.dac_tiles[tile].DynamicPLLConfig(1, pll_freq, fs)
        self.rfdc.dac_tiles[tile].blocks[block].NyquistZone = 1
        self.rfdc.dac_tiles[tile].blocks[block].MixerSettings['EventSource'] = xrfdc.EVNT_SRC_IMMEDIATE
        self.rfdc.dac_tiles[tile].SetupFIFO(True)

    def set_decimation(self, tile, block, sample_rate):
        """ Set the sampling rate by changing decimation factor and FabClkDiv.
        """
        decimation_factor, fab_clk_div = fs2div[str(sample_rate)]
        self.packet_generator.disable()
        self.rfdc.adc_tiles[tile].ShutDown()
        self.rfdc.adc_tiles[tile].FabClkOutDiv = fab_clk_div
        self.rfdc.adc_tiles[tile].blocks[block].DecimationFactor = decimation_factor
        self.rfdc.adc_tiles[tile].StartUp()
        self.packet_generator.enable()
        return sample_rate

    def set_fc(self, tile, block, fc):
        """ Change the center frequency.
        """
        if fc <= 4915200:
            self.rfdc.adc_tiles[tile].blocks[block].MixerSettings['Freq'] = -fc
            self.rfdc.adc_tiles[tile].blocks[block].NyquistZone = 1
        else:
            self.rfdc.adc_tiles[tile].blocks[block].MixerSettings['Freq'] = fc
            self.rfdc.adc_tiles[tile].blocks[block].NyquistZone = 2
        self.rfdc.adc_tiles[tile].blocks[block].UpdateEvent(xrfdc.EVENT_MIXER)
        return fc

    def source_select(self, source):
        # 0 = DMA
        # 1 = RF-ADC
        self.netlayer_switch.write(0x40, source)
        self.netlayer_switch.write(0x00, 0x02)
