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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gnuradio import analog
import specest_swig as specest
import numpy


class test_specest_cyclo_fam (gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block ()

    def tearDown(self):
        self.tb = None

    def test_001 (self):
        src_data = (1, 1, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1)
        expected_data = (   0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 1.384, 0.794, 1.384, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.794, 1.384, 2.411, 1.384, 0.794, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.794, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                            0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000  )
        Np = 4
        P = 4
        L = 2
        src = blocks.vector_source_c(src_data, False)
        cyclo_fam = specest.cyclo_fam(Np, P, L)
        sink = blocks.vector_sink_f(2*Np)
        self.tb.connect(src, cyclo_fam, sink)
        self.tb.run()
        estimated_data =  sink.data()[-2*P*L*(2*Np):]
        self.assertFloatTuplesAlmostEqual(expected_data,estimated_data,3)


    def test_002 (self):
        """ Stream some data through the block to see it all works. """
        Np = 128
        P = 512
        L = 4
        src = analog.noise_source_c(analog.GR_GAUSSIAN, 1)
        head = blocks.head(gr.sizeof_gr_complex, P * L)
        cyclo_fam = specest.cyclo_fam (Np,P,L)
        dst = blocks.vector_sink_f(2*Np)
        self.tb.connect(src, head, cyclo_fam, dst)
        try:
            self.tb.run()
        except:
            self.fail("Something's wrong -- an exception was thrown during runtime.")


    def test_exception1_003 (self):
        """ Make sure an exception is thrown when an invalid FFT-Size (Np) is chosen. """
        self.assertRaises(RuntimeError, specest.cyclo_fam, 17, 128, 2)
        self.assertRaises(RuntimeError, specest.cyclo_fam, 128, 16, 2)

    def test_exception2_004 (self):
        """ Make sure an exception is thrown when an invalid FFT-Size (P) is chosen. """
        self.assertRaises(RuntimeError, specest.cyclo_fam, 16, 129, 2)

    def test_exception3_005 (self):
        """ Make sure an exception is thrown when an invalid decimation factor is chosen. """
        self.assertRaises(RuntimeError, specest.cyclo_fam, 16, 128, 3)

    def test_exception4_006 (self):
        """ Make sure an exception is thrown when an invalid overlap factor is chosen. """
        self.assertRaises(RuntimeError, specest.cyclo_fam, 100.0, 2.0, 1.0 , 0.74)
        self.assertRaises(RuntimeError, specest.cyclo_fam, 101.0, 2.0, 1.0 , 1.1)

    def test_get_functions_007 (self):

        Np = 128
        P = 512
        L = 4
        N = P*L
        cyclo_fam  = specest.cyclo_fam(Np,P,L)
        self.assertEqual(cyclo_fam.get_Np(),Np)
        self.assertEqual(cyclo_fam.get_N(),N)
        self.assertEqual(cyclo_fam.get_L(),L)
        self.assertEqual(cyclo_fam.get_P(),P)


    def test_008 (self):

        fs = 133
        df = 2.3
        da = 1.4
        q  = 0.9
        cyclo_fam  = specest.cyclo_fam(fs, df, da, q)
        self.assertEqual(cyclo_fam.get_sample_frequency(),fs)
        #self.assertLessEqual(cyclo_fam.get_frequency_resolution(),df)
        #self.assertLessEqual(cyclo_fam.get_cycle_frequency_resolution(),da)

if __name__ == '__main__':
    gr_unittest.main ()

