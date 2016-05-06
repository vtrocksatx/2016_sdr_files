#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Scram Sock
# Generated: Wed Apr  6 13:30:07 2016
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import time
import vtgs


class tx_scram_sock(gr.top_block):

    def __init__(self, addr="127.0.0.1", alpha=0.5, bb_gain=0.65, port="4000", samps_per_symb=4, tx_correct=0, tx_freq=2402e6, tx_gain=20, samp_rate=100e3, tx_offset=50e3):
        gr.top_block.__init__(self, "Tx Scram Sock")

        ##################################################
        # Parameters
        ##################################################
        self.addr = addr
        self.alpha = alpha
        self.bb_gain = bb_gain
        self.port = port
        self.samps_per_symb = samps_per_symb
        self.tx_correct = tx_correct
        self.tx_freq = tx_freq
        self.tx_gain = tx_gain
        self.samp_rate = samp_rate
        self.tx_offset = tx_offset

        ##################################################
        # Blocks
        ##################################################
        self.vtgs_mult_scrambler_0 = vtgs.mult_scrambler(17, 0x3FFFF)
        self.vtgs_ao40_encoder_0 = vtgs.ao40_encoder(False, 449838109)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_time_source("gpsdo", 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(tx_freq+tx_correct, tx_offset), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.digital_map_bb_0 = digital.map_bb((1,0))
        self.digital_dxpsk_mod_0 = digital.dbpsk_mod(
        	samples_per_symbol=samps_per_symb,
        	excess_bw=alpha,
        	mod_code="gray",
        	verbose=False,
        	log=False)
        	
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (384,5232,384))
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_SERVER", addr, port, 10000, False)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((bb_gain, ))
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 1, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.vtgs_ao40_encoder_0, 'in'))    
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_mux_0, 0))    
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_mux_0, 2))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_dxpsk_mod_0, 0))    
        self.connect((self.blocks_stream_mux_0, 0), (self.digital_map_bb_0, 0))    
        self.connect((self.digital_dxpsk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.digital_map_bb_0, 0), (self.vtgs_mult_scrambler_0, 0))    
        self.connect((self.vtgs_ao40_encoder_0, 0), (self.blocks_stream_mux_0, 1))    
        self.connect((self.vtgs_mult_scrambler_0, 0), (self.blocks_pack_k_bits_bb_0, 0))    

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.blocks_multiply_const_vxx_0.set_k((self.bb_gain, ))

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

    def get_tx_correct(self):
        return self.tx_correct

    def set_tx_correct(self, tx_correct):
        self.tx_correct = tx_correct
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
        	

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--addr", dest="addr", type="string", default="127.0.0.1",
        help="Set addr [default=%default]")
    parser.add_option(
        "", "--alpha", dest="alpha", type="eng_float", default=eng_notation.num_to_str(0.5),
        help="Set alpha [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(0.65),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default="4000",
        help="Set port [default=%default]")
    parser.add_option(
        "", "--samps-per-symb", dest="samps_per_symb", type="eng_float", default=eng_notation.num_to_str(4),
        help="Set samps_per_symb [default=%default]")
    parser.add_option(
        "", "--tx-correct", dest="tx_correct", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_correct [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(2402e6),
        help="Set tx_freq [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set tx_gain [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(100e3),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "", "--tx-offset", dest="tx_offset", type="eng_float", default=eng_notation.num_to_str(50e3),
        help="Set tx_offset [default=%default]")
    return parser


def main(top_block_cls=tx_scram_sock, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(addr=options.addr, alpha=options.alpha, bb_gain=options.bb_gain, port=options.port, samps_per_symb=options.samps_per_symb, tx_correct=options.tx_correct, tx_freq=options.tx_freq, tx_gain=options.tx_gain, samp_rate=options.samp_rate, tx_offset=options.tx_offset)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
