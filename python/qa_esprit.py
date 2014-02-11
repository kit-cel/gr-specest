#!/usr/bin/env python
#
# Copyright 2011-2013 Free Software Foundation, Inc.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import specest_swig as specest
import signal_generator as siggen

class qa_esprit (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        """
        Simple test to see if decimation is working at all.
        """
        input_len = 2048
        nsamples = 1024
        decimation = 2
        pspectrum_len = 512
        n = 1
        m = 64
        self.siggen = siggen.signal_generator(n_sinusoids = n,
                                              SNR = 20, samp_rate = 32e3,
                                              nsamples = input_len)
        self.esprit = specest.esprit(n, m, nsamples, pspectrum_len, decimation)
        self.sink = blocks.vector_sink_f(vlen=pspectrum_len)
        self.tb.connect(self.siggen, self.esprit, self.sink)
        self.tb.run ()
        self.assertEqual(len(self.sink.data()), input_len / nsamples / decimation * pspectrum_len)

    def test_002_t (self):
        """
        Simple test to see if the decimation setters and getters work at all.
        """
        input_len = 1024
        nsamples = 256
        decimation = 1
        pspectrum_len = 512
        n = 1
        m = 64
        self.siggen = siggen.signal_generator(n_sinusoids = n,
                                              SNR = 20, samp_rate = 32e3,
                                              nsamples = input_len)
        self.esprit = specest.esprit(n, m, nsamples, pspectrum_len, decimation)
        self.assertEqual(self.esprit.decimation(), 1)
        self.esprit.set_decimation(2)
        self.assertEqual(self.esprit.decimation(), 2)
        self.sink = blocks.vector_sink_f(vlen=pspectrum_len)
        self.tb.connect(self.siggen, self.esprit, self.sink)
        self.tb.run ()
        self.assertEqual(len(self.sink.data()), input_len / nsamples / 2 * pspectrum_len)


if __name__ == '__main__':
    gr_unittest.main ()

