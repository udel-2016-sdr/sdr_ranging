# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Block
# Title: PRN Sequence Source
# Description: State machine for correlation.
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes

import numpy as np

class prn_seq_source(gr.sync_block):
    """
    PRN Sequence Source -- Generates a PRN sequence from a generator polynomial.
    """

    def __init__(self, poly=[0,1,1]):
        gr.sync_block.__init__(
            self,
            "PRN Sequence Source",
            in_sig=[],
            out_sig=[np.uint8]
        )

        self.poly = poly

        seq_period = 2**len(self.poly) - 1
        seq = []
        state = [0 for i in xrange(len(self.poly) - 1)]
        state.append(1)

        for i in xrange(seq_period):
            seq.append(state[-1])
            bit = sum(map(lambda x,y : x*y, state, poly)) % 2
            state[1:] = state[:-1]
            state[0] = bit
        
        self.seq = np.array(seq, dtype=np.uint8)
        self.pos = 0

        if len(self.seq) < 51200:
            mul = (51200 / len(self.seq)) + 1
            self.seq = np.tile(self.seq, mul)
        
        self.seq_len = len(self.seq)

    def work(self, input_items, output_items):
        buf_len = len(output_items[0])
        if (self.pos + buf_len) > self.seq_len:
            len1 = self.seq_len - self.pos
            len2 = buf_len - len1
            output_items[0][:len1] = self.seq[self.pos:]
            output_items[0][len1:] = self.seq[:len2]
            self.pos = len2
        else:
            output_items[0][:] = self.seq[self.pos:self.pos+buf_len]
            self.pos += buf_len
        return len(output_items[0])

    def get_poly(self):
        return self.poly

    def set_poly(self, poly):
        self.poly = poly
