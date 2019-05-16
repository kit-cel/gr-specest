#!/usr/bin/env python
#
# Copyright 2011-2013 Communications Engineering Lab, KIT
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

import numpy
from gnuradio import gr, gr_unittest
from gnuradio import blocks
import specest_swig as specest
import signal_generator as siggen

class qa_esprit_spectrum_vcf (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test__001_t (self):
        n_sinusoids = 5
        nsamples = 2048
        samp_rate = 32000
        SNR = 20 # in dB
        pspectrum_len = 512
        decimals = 4
        self.siggen = siggen.signal_generator(n_sinusoids = n_sinusoids,
                                              SNR = SNR, samp_rate = samp_rate,
                                              nsamples = nsamples)

        self.stream = blocks.stream_to_vector(gr.sizeof_gr_complex, nsamples)
        self.esprit = specest.esprit_spectrum_vcf(n=n_sinusoids, m=100, nsamples = nsamples, pspectrum_len = pspectrum_len)
        self.sink = blocks.vector_sink_f(vlen=pspectrum_len)
        # wire it up ...
        self.tb.connect(self.siggen, self.stream, self.esprit, self.sink)
        x = numpy.arange(start=-0.5, stop=0.5, step=1.0/float(pspectrum_len))
        self.tb.run()

if __name__ == '__main__':
    gr_unittest.main ()
