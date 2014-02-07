#!/usr/bin/env python
#
# Copyright 2011 Communications Engineering Lab, KIT
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from __future__ import division

##################################################
# Imports
##################################################
from gnuradio import gr
from gnuradio.wxgui import common
from gnuradio.wxgui.pubsub import pubsub
from gnuradio.wxgui.constants import *
import math
import wx
from gnuradio import uhd
from gnuradio.wxgui import stdgui2

from optparse import OptionParser
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option

#from spectrum_sink_gl import spectrum_sink_c
from specest import spectrum_sink_c

class test_app_block (stdgui2.std_top_block):
    def __init__(self, frame, panel, vbox, argv):
        stdgui2.std_top_block.__init__ (self, frame, panel, vbox, argv)

        parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
        parser.add_option("-r", "--sample-rate", type="eng_float", default=1e6,
                           help="set samplerate to RATE [default=%default]")
        parser.add_option("-f", "--freq", type="eng_float", default=1.8e9,
                           help="set center frequency to RATE [default=%default]")

        parser.add_option("-d", "--soft-decimate", type="eng_float", default=1,
                           help="decimate the given samplingrate further by a factor of [default=%default]")


        (options,values) = parser.parse_args()

        pspectrum_len = 1024
        nsamples = 512

        # build our flow graph
        input_rate = options.sample_rate
        soft_decimation = int(options.soft_decimate)
        center_freq = options.freq

        source = uhd.single_usrp_source(device_addr='type=usrp2',io_type=uhd.io_type_t.COMPLEX_FLOAT32, num_channels=1)
        source.set_samp_rate(input_rate)
        source.set_gain(45,0)
        source.set_center_freq(center_freq,0)

        item_size = gr.sizeof_gr_complex

        dec  = gr.keep_one_in_n(item_size, soft_decimation)

        sink1 = spectrum_sink_c (panel, title="ESPRIT Spectrum", pspectrum_len=pspectrum_len,
                            sample_rate=input_rate / soft_decimation, baseband_freq=0,
                            ref_level=0, y_per_div=20, y_divs=10, m = 128, n = 6, nsamples = nsamples,
                            estimator='esprit')

        vbox.Add (sink1.win, 1, wx.EXPAND)
        #sink2 = spectrum_sink_c (panel, title="MUSIC Spectrum", pspectrum_len=pspectrum_len,
                            #sample_rate=input_rate / soft_decimation, baseband_freq=0,
                            #ref_level=0, y_per_div=20, y_divs=10, m = 64, n = 2, nsamples = nsamples,
                            #estimator='music')

        scale = gr.multiply_const_cc(30.0e3)
        #vbox.Add (sink2.win, 1, wx.EXPAND)
        self.connect(source,scale,sink1)
        #self.connect(scale,sink2)

def main ():
    app = stdgui2.stdapp (test_app_block, "ESPRIT Sink Test App")
    app.MainLoop ()

if __name__ == '__main__':
    main ()
