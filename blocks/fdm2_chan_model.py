# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: FDM (2 Slot) Channel Model
# Generated: Tue Apr 25 15:43:23 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from fdm2_dmux import fdm2_dmux  # grc-generated hier_block
from fdm2_mux import fdm2_mux  # grc-generated hier_block
from gnuradio import channels
from gnuradio import gr
from gnuradio.filter import firdes


class fdm2_chan_model(gr.hier_block2):

    def __init__(self, ch_width=1000, freq_offset=0, noise_volt=0, samp_rate=32000, seed=0):
        gr.hier_block2.__init__(
            self, "FDM (2 Slot) Channel Model",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.ch_width = ch_width
        self.freq_offset = freq_offset
        self.noise_volt = noise_volt
        self.samp_rate = samp_rate
        self.seed = seed

        ##################################################
        # Blocks
        ##################################################
        self.fdm2_mux_0 = fdm2_mux(
            ch_width=ch_width,
            samp_rate=samp_rate,
        )
        self.fdm2_dmux_0 = fdm2_dmux(
            ch_width=ch_width,
            samp_rate=samp_rate,
        )
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=noise_volt,
        	frequency_offset=freq_offset,
        	epsilon=1.0,
        	taps=(1.0, ),
        	noise_seed=seed,
        	block_tags=False
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.channels_channel_model_0, 0), (self.fdm2_dmux_0, 0))    
        self.connect((self.fdm2_dmux_0, 0), (self, 0))    
        self.connect((self.fdm2_dmux_0, 1), (self, 1))    
        self.connect((self.fdm2_mux_0, 0), (self.channels_channel_model_0, 0))    
        self.connect((self, 0), (self.fdm2_mux_0, 0))    
        self.connect((self, 1), (self.fdm2_mux_0, 1))    

    def get_ch_width(self):
        return self.ch_width

    def set_ch_width(self, ch_width):
        self.ch_width = ch_width
        self.fdm2_mux_0.set_ch_width(self.ch_width)
        self.fdm2_dmux_0.set_ch_width(self.ch_width)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset)

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0.set_noise_voltage(self.noise_volt)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.fdm2_mux_0.set_samp_rate(self.samp_rate)
        self.fdm2_dmux_0.set_samp_rate(self.samp_rate)

    def get_seed(self):
        return self.seed

    def set_seed(self, seed):
        self.seed = seed
