# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Correlator
# Generated: Sun Mar 19 23:51:51 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from controlled_delay import controlled_delay  # grc-generated hier_block
from corr_state_machine_v1 import corr_state_machine_v1  # grc-generated hier_block
from correlator_kernel import correlator_kernel  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes


class correlator(gr.hier_block2):

    def __init__(self, frequency=1000, int_mult=1, poll_rate=1, samp_rate=32000):
        gr.hier_block2.__init__(
            self, "Correlator",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
            gr.io_signaturev(2, 2, [gr.sizeof_float*1, gr.sizeof_int*1]),
        )
        self.message_port_register_hier_in("command")

        ##################################################
        # Parameters
        ##################################################
        self.frequency = frequency
        self.int_mult = int_mult
        self.poll_rate = poll_rate
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.correlator_kernel_0 = correlator_kernel(
            int_period=(samp_rate / frequency) * int_mult,
        )
        self.corr_state_machine_v1_0 = corr_state_machine_v1(
            dly_cont_name='delay',
            max_delay=samp_rate / frequency,
        )
        self.controlled_delay_0 = controlled_delay(
            init_delay=0,
            name='delay',
        )
        self.blocks_integrate_xx_0 = blocks.integrate_ff(poll_rate, 1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, poll_rate)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.corr_state_machine_v1_0, 'delay_cmd'), (self.controlled_delay_0, 'command'))    
        self.msg_connect((self, 'command'), (self.corr_state_machine_v1_0, 'sm_cmd'))    
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_divide_xx_0, 1))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_integrate_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self, 0))    
        self.connect((self.blocks_divide_xx_0, 0), (self.corr_state_machine_v1_0, 0))    
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_divide_xx_0, 0))    
        self.connect((self.controlled_delay_0, 0), (self.correlator_kernel_0, 1))    
        self.connect((self.corr_state_machine_v1_0, 0), (self, 1))    
        self.connect((self.correlator_kernel_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self, 0), (self.correlator_kernel_0, 0))    
        self.connect((self, 1), (self.controlled_delay_0, 0))    

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.correlator_kernel_0.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.corr_state_machine_v1_0.set_max_delay(self.samp_rate / self.frequency)

    def get_int_mult(self):
        return self.int_mult

    def set_int_mult(self, int_mult):
        self.int_mult = int_mult
        self.correlator_kernel_0.set_int_period((self.samp_rate / self.frequency) * self.int_mult)

    def get_poll_rate(self):
        return self.poll_rate

    def set_poll_rate(self, poll_rate):
        self.poll_rate = poll_rate
        self.analog_const_source_x_0.set_offset(self.poll_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.correlator_kernel_0.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.corr_state_machine_v1_0.set_max_delay(self.samp_rate / self.frequency)
