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
import specest_swig as specest
from numpy import *

class test_vectormanip(gr_unittest.TestCase):
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_overlap(self):
        src_data = range(16)
        expected_data = tuple(list((0,) * 4) + range(4) + range(0, 8) + range(4, 12) + range(8, 16))
        vlen = 8

        src = gr.vector_source_i(src_data, False)
        s2v = specest.stream_to_vector_overlap(gr.sizeof_int, vlen, 4)
        dst = gr.vector_sink_i(vlen)

        self.tb.connect(src, s2v, dst)
        self.tb.run()

        dst_data =  dst.data()
        self.assertEqual(expected_data, dst_data)


    def test_002_vectorpad(self):
        vlen = 8
        src_data = (1,) * vlen
        expected_data = (1,) * 8 + (0,) * vlen

        src = gr.vector_source_f(src_data, False, vlen)
        s2v = specest.pad_vector(gr.sizeof_float, vlen, 2*vlen)
        dst = gr.vector_sink_f(2*vlen)

        self.tb.connect(src, s2v, dst)
        self.tb.run()

        dst_data =  dst.data()
        self.assertEqual(expected_data, dst_data)


    def test_003_reciprocal(self):
        vlen = 8
        src_data = (2,) * vlen
        expected_data = (0.5,) * vlen

        src = gr.vector_source_f(src_data, False, vlen)
        recip = specest.reciprocal_ff(vlen)
        dst = gr.vector_sink_f(vlen)

        self.tb.connect(src, recip, dst)
        self.tb.run()

        dst_data =  dst.data()
        self.assertEqual(expected_data, dst_data)


if __name__ == '__main__':
    gr_unittest.main ()


