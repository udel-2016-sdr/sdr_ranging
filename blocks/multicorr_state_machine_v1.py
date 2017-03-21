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

        self.message_port_register_in("sm_cmd")
        self.in_port = pmt.intern("sm_cmd")
        self.set_msg_handler(self.in_port, self.reset)
        self.message_port_register_out("delay_cmd")
        self.out_port = pmt.intern("delay_cmd")

        self.dly_cont_name = pmt.intern(dly_cont_name)
        self.max_delay = max_delay

        self.state = 'INIT'
        self.curr_delay = 0
        self.best_delay = 0

        self.send_cmd((self.curr_delay - 1) % self.max_delay,
                      self.curr_delay % self.max_delay,
                      (self.curr_delay + 1) % self.max_delay)

    def get_dly_cont_name(self):
        return self.dly_cont_name

    def set_dly_cont_name(self, dly_cont_name):
        self.dly_cont_name = pmt.intern(dly_cont_name)

    def get_max_delay(self):
        return self.max_delay

    def set_max_delay(self, max_delay):
        self.max_delay = max_delay

    def send_cmd(self, early, prompt, late):
        new_delays = pmt.make_u32vector(3, np.uint32(0))
        
        pmt.u32vector_set(new_delays, 0, np.uint32(early))
        pmt.u32vector_set(new_delays, 1, np.uint32(prompt))
        pmt.u32vector_set(new_delays, 2, np.uint32(late))
        cmd = pmt.cons(self.dly_cont_name, new_delays)

        self.message_port_pub(self.out_port, cmd)

    def reset(self, msg):
        pass
