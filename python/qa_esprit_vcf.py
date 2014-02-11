#!/usr/bin/env python
#
# Copyright 2010-2013 Communications Engineering Lab, KIT
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

from gnuradio import gr, gr_unittest, eng_notation
from gnuradio import blocks
import specest_swig as specest
import numpy
import signal_generator as siggen

class qa_esprit_vcf (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test__001_t (self):
        """
        Generate a signal with n_sinusoids sinusoids
        and a SNR of SNR.
        Another Check to see if it's working at all.
        """
        n_sinusoids = 2
        nsamples = 2048
        samp_rate = 32000
        SNR = 10 # in dB
        decimals = 3
        self.siggen = siggen.signal_generator(n_sinusoids = n_sinusoids,
                                              SNR = SNR, samp_rate = samp_rate,
                                              nsamples = nsamples)
        self.stream = blocks.stream_to_vector(gr.sizeof_gr_complex, nsamples)
        self.esprit = specest.esprit_vcf(n=n_sinusoids, m=100, nsamples = nsamples)
        self.sink = blocks.vector_sink_f(vlen=n_sinusoids)
        self.tb.connect(self.siggen, self.stream, self.esprit, self.sink)
        for i in range(100):
            self.tb.run()
            for (g,e) in  zip(sorted(list(self.sink.data())), self.siggen.omegas()):
                self.assertAlmostEqual(g,e, decimals)

    def test__002_t (self):
        """
        Generate a signal with SNR as given below.
        Calculate the RMSE.
        """
        nsamples = 1024
        n_trials = 100
        samp_rate = 32000
        SNR = 20 # in dB
        self.siggen = siggen.signal_generator(n_sinusoids = 1,
                                              SNR = SNR, samp_rate = samp_rate,
                                              nsamples = nsamples * n_trials)

        self.stream = blocks.stream_to_vector(gr.sizeof_gr_complex, nsamples)
        self.esprit = specest.esprit_vcf(n=1, m=64, nsamples = nsamples)
        self.sink = blocks.vector_sink_f(vlen=1)
        # wire it up ...
        self.tb.connect(self.siggen, self.stream, self.esprit, self.sink)
        self.tb.run()
        MSE = 0.0
        omega = self.siggen.omegas()[0]
        for i in range(n_trials):
            MSE += (omega - self.sink.data()[i])**2.0
        print '\n' + 70*'-'
        print 'Testing specest_esprit_vcf ...'
        print 'Ran %u trials to estimate the frequency' % n_trials
        print 'Used %u samples to estimate the frequency' % nsamples
        print 'Sampling rate %s' % eng_notation.num_to_str(samp_rate)
        print 'SNR of %u dB' % SNR
        print 'Root mean square error %g' % numpy.sqrt(MSE/n_trials)
        print 'Cramer-Rao Bound %g' % numpy.sqrt(6/10**(SNR/10.0)/nsamples**3)
        print 70*'-'

if __name__ == '__main__':
    gr_unittest.main ()

