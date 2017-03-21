# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Correlator Kernew
# Description: Performs IQ value correlation between recv and ref.
# Generated: Sun Mar 19 23:37:50 2017
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes


class correlator_kernel(gr.hier_block2):

    def __init__(self, int_period=32):
        gr.hier_block2.__init__(
            self, "Correlator Kernew",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.int_period = int_period

        ##################################################
        # Blocks
        ##################################################
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff(int_period, 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(int_period, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_1, 0))    
        self.connect((self.blocks_complex_to_float_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_float_1, 1), (self.blocks_multiply_xx_1, 1))    
        self.connect((self.blocks_float_to_complex_0, 0), (self, 0))    
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_integrate_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_integrate_xx_0_0, 0))    
        self.connect((self, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self, 1), (self.blocks_complex_to_float_1, 0))    

    def get_int_period(self):
        return self.int_period

    def set_int_period(self, int_period):
        self.int_period = int_period
