from gnuradio import gr
import pmt

class msg_redirector(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """
    Message Redirector - Redirects message to a callback funtion
    """

    def __init__(self, port='', callback=None):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Messaqe Redirector',   # will show up in GRC
            in_sig=[],
            out_sig=[]
        )

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_in(pmt.intern(port))
        self.callback = callback
        self.set_msg_handler(pmt.intern(port), self.handler)

    def work(self, input_items, output_items):
        return len(output_items[0])

    def handler(self, msg):
        self.callback(msg)
