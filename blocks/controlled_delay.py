# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Controlled Delay
# Description: Message controlled variable delay block.
# Generated: Sat Mar 18 23:43:01 2017
##################################################

from gnuradio import blocks
from gnuradio import gr
from msg_redirector import msg_redirector
import pmt


class controlled_delay(gr.hier_block2):

    def __init__(self, init_delay=0, name=''):
        gr.hier_block2.__init__(
            self, "Controlled Delay",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        self.message_port_register_hier_in("command")

        ##################################################
        # Parameters
        ##################################################
        self.init_delay = init_delay
        self.name = pmt.intern(name)

        ##################################################
        # Blocks
        ##################################################
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, init_delay)
        self.blocks_msg_redirector_0 = msg_redirector(port="command", callback=self.interpret)
        self.msg_connect(self, "command", self.blocks_msg_redirector_0, "command")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self, 0))    
        self.connect((self, 0), (self.blocks_delay_0, 0))    

    def get_init_delay(self):
        return self.init_delay

    def set_init_delay(self, init_delay):
        self.init_delay = init_delay
        self.blocks_delay_0.set_dly(self.init_delay)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = pmt.intern(name)

    def interpret(self, msg):
        if pmt.is_dict(msg):
            delay = None
            try:
                delay = pmt.dict_ref(msg, self.name, None)
            except:
                pass

            try:
                if pmt.eqv(self.name, pmt.car(msg)):
                    delay = pmt.cdr(msg)
            except:
                pass

            if delay is not None:
                delay = pmt.to_long(delay)
                self.blocks_delay_0.set_dly(delay)
