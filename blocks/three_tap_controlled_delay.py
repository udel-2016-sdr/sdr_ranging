# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: 3Tap Controlled Delay
# Description: Message controlled three tap variable delay block.
# Generated: Sat Mar 18 23:43:01 2017
##################################################

from gnuradio import blocks
from gnuradio import gr
from msg_redirector import msg_redirector
import pmt


class three_tap_controlled_delay(gr.hier_block2):

    def __init__(self, init_delay=0, name=''):
        gr.hier_block2.__init__(
            self, "3Tap Controlled Delay",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(3, 3, gr.sizeof_gr_complex*1),
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
        self.blocks_delay_1 = blocks.delay(gr.sizeof_gr_complex*1, init_delay)
        self.blocks_delay_2 = blocks.delay(gr.sizeof_gr_complex*1, init_delay)
        self.blocks_msg_redirector_0 = msg_redirector(port="command", callback=self.interpret)
        self.msg_connect(self, "command", self.blocks_msg_redirector_0, "command")

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.blocks_delay_0, 0))
        self.connect((self, 0), (self.blocks_delay_1, 0))
        self.connect((self, 0), (self.blocks_delay_2, 0))

        self.connect((self.blocks_delay_0, 0), (self, 0))
        self.connect((self.blocks_delay_1, 0), (self, 1))
        self.connect((self.blocks_delay_2, 0), (self, 2))

    def get_init_delay(self):
        return self.init_delay

    def set_init_delay(self, init_delay):
        self.init_delay = init_delay
        self.blocks_delay_0.set_dly(self.init_delay)
        self.blocks_delay_1.set_dly(self.init_delay)
        self.blocks_delay_2.set_dly(self.init_delay)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = pmt.intern(name)

    def interpret(self, msg):
        if pmt.is_dict(msg):
            delays = None
            try:
                delays = pmt.dict_ref(msg, self.name, None)
            except:
                pass

            try:
                if pmt.eqv(self.name, pmt.car(msg)):
                    delays = pmt.cdr(msg)
            except:
                pass

            if delays is not None and pmt.is_u32vector(delays):
                delay0 = pmt.u32vector_ref(delays, 0)
                delay1 = pmt.u32vector_ref(delays, 1)
                delay2 = pmt.u32vector_ref(delays, 2)

                self.blocks_delay_0.set_dly(delay0)
                self.blocks_delay_1.set_dly(delay1)
                self.blocks_delay_2.set_dly(delay2)
