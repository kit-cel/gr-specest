#!/usr/bin/env python
#
# Copyright 2010 Communications Engineering Lab, KIT
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
import numpy
import specest_mtm

class test_specest_mtm(gr_unittest.TestCase):
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001(self):
        """ adaptive weighting:
        - Constant input signal of amplitude 1
        - adaptive weighting
        The given input signal has a known power of 1. Therefore, the integral of the
        PSD estimation result should be pretty close to 1."""
        N = 512
        NW = 3
        K = 5
        weighting = 'adaptive'
        src_data = (1,) * N
        src = gr.vector_source_c(src_data, False)
        self.mtm = specest_mtm.mtm(N=N, NW=NW, K=K, weighting=weighting)
        sink = gr.vector_sink_f(N)

        self.tb.connect(src, self.mtm, sink)
        self.tb.run()

        dst_data = sink.data()
        dst_data = numpy.array(dst_data[-N:])
        power_est = numpy.sum(dst_data) / N
        self.assertAlmostEqual(power_est, 1, 2)

    def test_002(self):
        """ unityweighting:
        - Constant input signal of amplitude 1
        - unity weighting
        The given input signal has a known power of 1. Therefore, the integral of the
        PSD estimation result should be pretty close to 1."""
        N = 512
        NW = 3
        K = 5
        weighting = 'unity'
        src_data = (1,) * N
        src = gr.vector_source_c(src_data, False)
        self.mtm = specest_mtm.mtm(N=N, NW=NW, K=K, weighting=weighting)
        sink = gr.vector_sink_f(N)

        self.tb.connect(src, self.mtm, sink)
        self.tb.run()

        dst_data =  sink.data()
        dst_data = numpy.array(dst_data[-N:])
        power_est = numpy.sum(dst_data) / N
        self.assertAlmostEqual(power_est, 1, 5)

    def test_003(self):
        """ eigenvalue weighting:
        - Constant input signal of amplitude 1
        - eigenvalue weighting
        The given input signal has a known power of 1. Therefore, the integral of the
        PSD estimation result should be pretty close to 1."""
        N = 512
        NW = 3
        K = 5
        weighting = 'eigenvalues'
        src_data = (1,) * N
        src = gr.vector_source_c(src_data, False)
        self.mtm = specest_mtm.mtm(N=N, NW=NW, K=K, weighting=weighting)
        sink = gr.vector_sink_f(N)

        self.tb.connect(src, self.mtm, sink)
        self.tb.run()

        dst_data =  sink.data()
        dst_data = numpy.array(dst_data[-N:])
        power_est = numpy.sum(dst_data) / N
        self.assertAlmostEqual(power_est, 1, 1)

    def test_exception_001(self):
        """ Make sure an exception is thrown when an invalid overlap is chosen. """
        self.assertRaises(ValueError, specest_mtm.mtm, K = -5)


    def test_exception_002(self):
        """ Make sure an exception is thrown when the timebandwidthproduct is smaller than 1. """
        self.assertRaises(ValueError, specest_mtm.mtm, NW = -5)

if __name__ == '__main__':
    gr_unittest.main ()

