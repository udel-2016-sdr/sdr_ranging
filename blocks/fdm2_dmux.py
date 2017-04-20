# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: FDM (2 Slot) Demux
# Generated: Thu Apr 20 19:41:00 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes


class fdm2_dmux(gr.hier_block2):

    def __init__(self, ch_width=1000, samp_rate=32000):
        gr.hier_block2.__init__(
            self, "FDM (2 Slot) Demux",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.ch_width = ch_width
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0 = firdes.low_pass(1.0, samp_rate, ch_width, ch_width / 100, firdes.WIN_HAMMING, 6.76)
          
        
        self.variable_band_pass_filter_taps_0 = variable_band_pass_filter_taps_0 = firdes.band_pass(1.0, samp_rate, ch_width, ch_width * 2, ch_width / 100, firdes.WIN_HAMMING, 6.76)
          

        ##################################################
        # Blocks
        ##################################################
        self.fft_filter_xxx_2 = filter.fft_filter_ccf(1, (variable_band_pass_filter_taps_0), 1)
        self.fft_filter_xxx_2.declare_sample_delay(0)
        self.fft_filter_xxx_1 = filter.fft_filter_ccf(1, (variable_low_pass_filter_taps_0), 1)
        self.fft_filter_xxx_1.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccf(1, (variable_low_pass_filter_taps_0), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, len(variable_low_pass_filter_taps_0) + 1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -ch_width, 0.5, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_delay_0, 0), (self, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.fft_filter_xxx_1, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.fft_filter_xxx_1, 0), (self, 1))    
        self.connect((self.fft_filter_xxx_2, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self, 0), (self.fft_filter_xxx_2, 0))    

    def get_ch_width(self):
        return self.ch_width

    def set_ch_width(self, ch_width):
        self.ch_width = ch_width
        self.analog_sig_source_x_0.set_frequency(-self.ch_width)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_variable_low_pass_filter_taps_0(self):
        return self.variable_low_pass_filter_taps_0

    def set_variable_low_pass_filter_taps_0(self, variable_low_pass_filter_taps_0):
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0
        self.fft_filter_xxx_1.set_taps((self.variable_low_pass_filter_taps_0))
        self.fft_filter_xxx_0.set_taps((self.variable_low_pass_filter_taps_0))
        self.blocks_delay_0.set_dly(len(self.variable_low_pass_filter_taps_0) + 1)

    def get_variable_band_pass_filter_taps_0(self):
        return self.variable_band_pass_filter_taps_0

    def set_variable_band_pass_filter_taps_0(self, variable_band_pass_filter_taps_0):
        self.variable_band_pass_filter_taps_0 = variable_band_pass_filter_taps_0
        self.fft_filter_xxx_2.set_taps((self.variable_band_pass_filter_taps_0))
