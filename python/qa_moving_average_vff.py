#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010,2013 Communications Engineering Lab, KIT
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

class qa_moving_average_vff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        vlen = 8
        N = 2
        in_data = (1,) * vlen + (2,) * vlen
        expected_data = (.5,) * vlen + (1.5,) * vlen
        src = blocks.vector_source_f(in_data, False, vlen)
        avg = specest.moving_average_vff(N, vlen, 1.0/N)
        sink = blocks.vector_sink_f(vlen)
        self.tb.connect(src, avg, sink)
        self.tb.run ()
        self.assertEqual(expected_data, sink.data())

if __name__ == '__main__':
    gr_unittest.run(qa_moving_average_vff, "qa_moving_average_vff.xml")
