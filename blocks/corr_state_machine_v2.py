# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Block
# Title: Correlator State Machine
# Description: State machine for correlation.
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes

import numpy as np
import pmt

class corr_state_machine_v2(gr.sync_block):
    """
    Correlator State Machine (v2) - Controls delay of reference signal to maximize
                               correlation
    """

    def __init__(self, dly_cont_name='', max_delay=0):
        gr.sync_block.__init__(
            self,
            "Correlator State Machine (v2)",
            in_sig=[np.float32],
            out_sig=[np.int32]
        )

        self.message_port_register_in(pmt.intern("sm_cmd"))
        self.in_port = pmt.intern("sm_cmd")
        self.set_msg_handler(self.in_port, self.reset)
        self.message_port_register_out(pmt.intern("delay_cmd"))
        self.out_port = pmt.intern("delay_cmd")

        self.dly_cont_name = pmt.intern(dly_cont_name)
        self.max_delay = max_delay

        self.state = 'INIT'
        self.curr_delay = 0
        self.best_delay = 0

        self.values = [0 for i in xrange(self.max_delay)]

        self.send_cmd(self.curr_delay)

    def work(self, input_items, output_items):
        if self.state == 'INIT':
            if self.curr_delay < self.max_delay:
                self.values[self.curr_delay] = np.around(input_items[0], decimals=1)[0]
                self.curr_delay += 1
                self.send_cmd(self.curr_delay)
            else:
                self.state = 'RUN'
        elif self.state == 'RUN':
            max_val = max(self.values)
            best_val = self.values[self.best_delay]
            if max_val >= best_val:
                self.best_delay = self.values.index(max_val)
            self.send_cmd(self.best_delay)

        output_items[0][0] = np.int32(self.best_delay)
        return len(output_items[0])

    def get_dly_cont_name(self):
        return self.dly_cont_name

    def set_dly_cont_name(self, dly_cont_name):
        self.dly_cont_name = pmt.intern(dly_cont_name)

    def get_max_delay(self):
        return self.max_delay

    def set_max_delay(self, max_delay):
        self.max_delay = max_delay

    def send_cmd(self, new_delay):
        new_delay = pmt.from_long(new_delay)

        cmd = pmt.cons(self.dly_cont_name, new_delay)
 
        self.message_port_pub(self.out_port, cmd)

    def reset(self, msg):
        if pmt.is_symbol(msg) and pmt.eqv(msg, pmt.intern('RESET')):
            self.state = 'INIT'
            self.curr_delay = 0
            self.values = [0 for i in xrange(self.max_delay)]
            self.send_cmd(self.curr_delay)
