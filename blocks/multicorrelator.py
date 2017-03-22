# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Multicorrelator
# Generated: Wed Mar 22 00:25:16 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from correlator_kernel import correlator_kernel  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from multicorr_state_machine_v1 import multicorr_state_machine_v1  # grc-generated hier_block
from three_tap_controlled_delay import three_tap_controlled_delay  # grc-generated hier_block


class multicorrelator(gr.hier_block2):

    def __init__(self, frequency=1000, int_mult=1, poll_rate=1, samp_rate=32000):
        gr.hier_block2.__init__(
            self, "Multicorrelator",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
            gr.io_signaturev(2, 2, [gr.sizeof_float*3, gr.sizeof_int*3]),
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
        self.three_tap_controlled_delay_0 = three_tap_controlled_delay(
            init_delay=0,
            name='delay',
        )
        self.multicorr_state_machine_v1_0 = multicorr_state_machine_v1(
            dly_cont_name='delay',
            max_delay=samp_rate / frequency,
        )
        self.correlator_kernel_prompt = correlator_kernel(
            int_period=(samp_rate / frequency) * int_mult,
        )
        self.correlator_kernel_late = correlator_kernel(
            int_period=(samp_rate / frequency) * int_mult,
        )
        self.correlator_kernel_early = correlator_kernel(
            int_period=(samp_rate / frequency) * int_mult,
        )
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_float*1, 3)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, 3)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(poll_rate, 3)
        self.blocks_divide_xx_0 = blocks.divide_ff(3)
        self.blocks_complex_to_real_0_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, poll_rate)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.multicorr_state_machine_v1_0, 'delay_cmd'), (self.three_tap_controlled_delay_0, 'command'))    
        self.msg_connect((self, 'command'), (self.multicorr_state_machine_v1_0, 'sm_cmd'))    
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_streams_to_vector_0, 0))    
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_streams_to_vector_0, 2))    
        self.connect((self.blocks_complex_to_real_0_1, 0), (self.blocks_streams_to_vector_0, 1))    
        self.connect((self.blocks_divide_xx_0, 0), (self.multicorr_state_machine_v1_0, 0))    
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_divide_xx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_divide_xx_0, 1))    
        self.connect((self.blocks_streams_to_vector_0, 0), (self.blocks_integrate_xx_0, 0))    
        self.connect((self.blocks_streams_to_vector_0, 0), (self, 0))    
        self.connect((self.correlator_kernel_early, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.correlator_kernel_late, 0), (self.blocks_complex_to_real_0_0, 0))    
        self.connect((self.correlator_kernel_prompt, 0), (self.blocks_complex_to_real_0_1, 0))    
        self.connect((self.multicorr_state_machine_v1_0, 0), (self, 1))    
        self.connect((self, 0), (self.correlator_kernel_early, 0))    
        self.connect((self, 0), (self.correlator_kernel_late, 0))    
        self.connect((self, 0), (self.correlator_kernel_prompt, 0))    
        self.connect((self, 1), (self.three_tap_controlled_delay_0, 0))    
        self.connect((self.three_tap_controlled_delay_0, 0), (self.correlator_kernel_early, 1))    
        self.connect((self.three_tap_controlled_delay_0, 2), (self.correlator_kernel_late, 1))    
        self.connect((self.three_tap_controlled_delay_0, 1), (self.correlator_kernel_prompt, 1))    

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.multicorr_state_machine_v1_0.set_max_delay(self.samp_rate / self.frequency)
        self.correlator_kernel_prompt.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.correlator_kernel_late.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.correlator_kernel_early.set_int_period((self.samp_rate / self.frequency) * self.int_mult)

    def get_int_mult(self):
        return self.int_mult

    def set_int_mult(self, int_mult):
        self.int_mult = int_mult
        self.correlator_kernel_prompt.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.correlator_kernel_late.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.correlator_kernel_early.set_int_period((self.samp_rate / self.frequency) * self.int_mult)

    def get_poll_rate(self):
        return self.poll_rate

    def set_poll_rate(self, poll_rate):
        self.poll_rate = poll_rate
        self.analog_const_source_x_0.set_offset(self.poll_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.multicorr_state_machine_v1_0.set_max_delay(self.samp_rate / self.frequency)
        self.correlator_kernel_prompt.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.correlator_kernel_late.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
        self.correlator_kernel_early.set_int_period((self.samp_rate / self.frequency) * self.int_mult)
