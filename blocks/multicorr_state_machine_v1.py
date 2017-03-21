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
    Correlator State Machine (v1) - Controls delay of reference signal to maximize
                               correlation
    """

    def __init__(self, early_dly_cont_name='', prompt_dly_cont_name='', late_dly_cont_name='', max_delay=0):
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

        self.early_dly_cont_name = pmt.intern(early_dly_cont_name)
        self.prompt_dly_cont_name = pmt.intern(prompt_dly_cont_name)
        self.late_dly_cont_name = pmt.intern(late_dly_cont_name)
        self.max_delay = max_delay

        self.state = 'INIT'
        self.curr_delay = 0
        self.best_delay = 0

        self.send_cmd((self.curr_delay - 1) % self.max_delay,
                      self.curr_delay % self.max_delay,
                      (self.curr_delay + 1) % self.max_delay)

    def get_early_dly_cont_name(self):
        return self.early_dly_cont_name

    def set_early_dly_cont_name(self, early_dly_cont_name):
        self.early_dly_cont_name = pmt.intern(early_dly_cont_name)

    def get_prompt_dly_cont_name(self):
        return self.prompt_dly_cont_name

    def set_prompt_dly_cont_name(self, prompt_dly_cont_name):
        self.prompt_dly_cont_name = pmt.intern(prompt_dly_cont_name)

    def get_late_dly_cont_name(self):
        return self.late_dly_cont_name

    def set_late_dly_cont_name(self, late_dly_cont_name):
        self.late_dly_cont_name = pmt.intern(late_dly_cont_name)

    def get_max_delay(self):
        return self.max_delay

    def set_max_delay(self, max_delay):
        self.max_delay = max_delay

    def send_cmd(self, early, prompt, late):
        early = pmt.from_long(early)
        prompt = pmt.from_long(prompt)
        late = pmt.from_long(late)

        cmd = pmt.make_dict()
        cmd = pmt.dict_add(cmd, self.early_dly_cont_name, early)
        cmd = pmt.dict_add(cmd, self.prompt_dly_cont_name, prompt)
        cmd = pmt.dict_add(cmd, self.late_dly_cont_name, late)

        self.message_port_pub(self.out_port, cmd)

    def reset(self, msg):
        pass
