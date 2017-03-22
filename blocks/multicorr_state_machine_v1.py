# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Block
# Title: Multicorrelator State Machine (v1)
# Description: State machine for multicorrelation.
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes

import numpy as np
import pmt

class multicorr_state_machine_v1(gr.sync_block):
    """
    Multicorrelator State Machine (v1) - Controls delay of reference signal to maximize
                                         correlation
    """

    def __init__(self, dly_cont_name='', max_delay=0):
        gr.sync_block.__init__(
            self,
            "Multicorrelator State Machine (v1)",
            in_sig=[(np.float32, 3)],
            out_sig=[(np.int32, 3)]
        )

        self.message_port_register_in(pmt.intern("sm_cmd"))
        self.in_port = pmt.intern("sm_cmd")
        self.set_msg_handler(self.in_port, self.reset)
        self.message_port_register_out(pmt.intern("delay_cmd"))
        self.out_port = pmt.intern("delay_cmd")

        self.dly_cont_name = pmt.intern(dly_cont_name)
        self.max_delay = max_delay

        self.state = 'INIT'
        self.curr_delays = [-1 % self.max_delay, 0, 1 % self.max_delay]
        self.best_delay = 0

        self.values = [0 for i in xrange(self.max_delay)]

        self.send_cmd(self.curr_delays[0],
                      self.curr_delays[1],
                      self.curr_delays[2])

    def work(self, input_items, output_items):
        if self.state == 'INIT':
            if self.curr_delays[1] < self.max_delay:
                rounded = np.around(input_items[0][0], decimals=1)
                self.values[self.curr_delays[0]] = rounded[0]
                self.values[self.curr_delays[1]] = rounded[1]
                self.values[self.curr_delays[2]] = rounded[2]

                self.curr_delays[0] = (self.curr_delays[0] + 3) % self.max_delay
                self.curr_delays[1] = (self.curr_delays[1] + 3)
                self.curr_delays[2] = (self.curr_delays[2] + 3) % self.max_delay

                self.send_cmd(self.curr_delays[0],
                              self.curr_delays[1],
                              self.curr_delays[2])
            else:
                self.state = 'RUN'
        elif self.state == 'RUN':
            max_val = max(self.values)
            self.best_delay = self.values.index(max_val)
            self.send_cmd((self.best_delay - 1) % self.max_delay,
                          self.best_delay,
                          (self.best_delay + 1) % self.max_delay)

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

    def send_cmd(self, early, prompt, late):
        new_delays = pmt.make_u32vector(3, 0)
        
        pmt.u32vector_set(new_delays, 0, early)
        pmt.u32vector_set(new_delays, 1, prompt)
        pmt.u32vector_set(new_delays, 2, late)
        cmd = pmt.cons(self.dly_cont_name, new_delays)

        self.message_port_pub(self.out_port, cmd)

    def reset(self, msg):
        if pmt.is_symbol(msg) and pmt.eqv(msg, pmt.intern('RESET')):
            self.state = 'INIT'
            self.curr_delays = [-1 % self.max_delay, 0, 1 % self.max_delay]
            self.values = [0 for i in xrange(self.max_delay)]
            self.send_cmd(self.curr_delays[0],
                          self.curr_delays[1],
                          self.curr_delays[2])
