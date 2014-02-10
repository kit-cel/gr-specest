#!/usr/bin/env python
#
# Copyright 2010-2013 Communications Engineering Lab, KIT, Germany
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

test_sig = (
 1.349839031+2.011167288j,
-2.117270231+0.817693591j,
-1.786421657-1.291698933j,
 1.162236333-1.482598066j,
 1.641072035+0.372950256j,
 0.072213709+1.828492761j,
-1.564284801+0.824533045j,
-1.080565453-1.869776845j,
 0.927129090-1.743406534j,
 1.891979456+0.972347319j,
-0.105391249+1.602209687j,
-1.618367076+0.637513280j,
-0.945704579-1.079569221j,
 1.135566235-1.692269921j,
 1.855816245+0.986030221j,
-1.032083511+1.414613724j,
-1.571600199+0.089229003j,
-0.243143231-1.444692016j,
 0.838980973-0.985756695j,
 1.516003132+0.928058863j,
 0.257979959+1.170676708j,
-2.057927608+0.343388647j,
-0.578682184-1.441192508j,
 1.584011555-1.011150956j,
 0.614114344+1.508176208j,
-0.710567117+1.130144477j,
-1.100205779-0.584209621j,
 0.150702029-1.217450142j,
 0.748856127-0.804411888j,
 0.795235813+1.114466429j,
-0.071512341+1.017092347j,
-1.732939839-0.283070654j,
 0.404945314-0.781708360j,
 1.293794155-0.352723092j,
-0.119905084+0.905150294j,
-0.522588372+0.437393665j,
-0.974838495-0.670074046j,
 0.275279552-0.509659231j,
 0.854210198-0.008278057j,
 0.289598197+0.506233990j,
-0.283553183+0.250371397j,
-0.359602571-0.135261074j,
 0.102775671-0.466086507j,
-0.009722650+0.030377999j,
 0.185930878+0.808869600j,
-0.243692726-0.200126961j,
-0.270986766-0.460243553j,
 0.399368525+0.249096692j,
-0.250714004-0.362990230j,
 0.419116348-0.389185309j,
-0.050458215+0.702862442j,
-0.395043731+0.140808776j,
 0.746575892-0.126762003j,
-0.559076190+0.523169816j,
-0.344389260-0.913451135j,
 0.733228028-0.006237417j,
-0.480273813+0.509469569j,
 0.033316225+0.087501869j,
-0.321229130-0.254548967j,
-0.063007891-0.499800682j,
 1.239739418-0.013479125j,
 0.083303742+0.673984587j,
-0.762731433+0.408971250j,
-0.895898521-0.364855707j)
test_sig_coeffs = (1.0000, 0.4828-0.4248j, 0.7171-0.3047j, 0.2411-0.1540j, 0.4463+0.0523j)
test_sig_var = (0.1482,)

class test_specest_fmcov(gr_unittest.TestCase):
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_noiseprocess (self):
        """  Calculate coefficients of known signal and compare w/ precalculated results.
        We run the test twice to make sure no residual stuff affects calculation. """
        src = blocks.vector_source_c(test_sig * 2, False, len(test_sig))
        fmcov = specest.arfmcov_vcc(len(test_sig), len(test_sig_coeffs) - 1)
        dst_coeffs = blocks.vector_sink_c(len(test_sig_coeffs))
        dst_var = blocks.vector_sink_f()
        self.tb.connect(src, fmcov, dst_coeffs)
        self.tb.connect((fmcov, 1), dst_var)
        self.tb.run()
        result_coeffs = tuple(dst_coeffs.data())
        result_var = dst_var.data()
        self.assertFloatTuplesAlmostEqual(result_coeffs, test_sig_coeffs * 2, 3)
        self.assertFloatTuplesAlmostEqual(result_var, test_sig_var * 2, 4)

    def test_002_stream (self):
        """ Monkey test """
        block_len = 256
        fft_len = 128
        order = 6
        n_blocks = 100
        src = analog.noise_source_c(analog.GR_GAUSSIAN, 1)
        head = blocks.head(gr.sizeof_gr_complex, n_blocks * block_len)
        fmcov = specest.fmcov(block_len, fft_len, order)
        dst = blocks.vector_sink_f(fft_len)
        self.tb.connect(src, head, fmcov, dst)
        try:
            self.tb.run()
        except:
            self.fail("Something's wrong -- an exception was thrown during runtime.")


if __name__ == '__main__':
    gr_unittest.main ()

