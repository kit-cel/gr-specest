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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gnuradio import analog
import specest_swig as specest
import numpy

test_sig = (1.4310-0.3066j, 2.3536-0.9656j, 2.6211-1.6518j, 2.3034-1.3116j, 2.0013+0.6699j, 0.3519+3.8874j, -3.3812+7.4823j, -7.6895+9.6972j,
        -8.9602+7.0478j, -5.9128-2.8789j, 0.8732-15.3469j, 7.4119-22.9530j, 9.7694-18.9880j, 6.9671-2.9939j, 1.0988+18.9369j, -3.6737+34.4581j,
        -4.1556+32.2055j, -1.4540+10.7854j, 1.2396-18.8327j, 0.6621-39.4158j, -3.8499-38.6139j, -7.8648-17.2044j, -6.4302+12.6777j, 1.3515+33.5593j,
        11.5656+33.6270j, 17.4025+15.4283j, 13.7454-8.5046j, 1.9575-24.1417j, -10.8231-23.7297j, -16.7723-10.5482j, -13.0526+5.8286j, -3.1100+15.3772j,
        7.4885+14.8894j, 12.2439+8.1645j, 9.0544+1.0704j, -0.2944-3.4651j, -9.0227-6.4728j, -10.4626-9.5586j, -3.6472-12.2162j, 6.0801-11.5650j,
        9.4981-4.0649j, 3.4508+9.0515j, -8.7140+21.8845j, -19.2602+25.4466j, -19.5270+15.3183j, -7.4965-5.3381j, 10.9481-25.6783j, 25.2469-32.7227j,
        26.7339-21.0964j, 13.0857+2.9365j, -8.5498+26.8052j, -25.7815+37.7338j, -27.9848+29.0029j, -13.4110+5.1540j, 9.7372-21.1807j, 27.4513-35.5135j,
        28.8425-29.4464j, 13.9589-8.0639j, -9.0257+16.0057j, -27.2919+30.6175j, -31.4544+29.3729j, -19.9534+15.5743j, 1.1527-2.3653j, 21.5482-17.0954j,
        30.4895-25.5414j, 23.2192-26.2681j, 4.1280-17.8631j, -16.2913-0.9747j, -27.0466+19.5638j, -22.8010+34.1825j, -7.5832+33.8352j, 9.1074+14.8073j,
        17.0148-15.9612j, 14.0197-42.8637j, 4.5944-49.1105j, -4.8554-28.2850j, -9.6085+9.2433j, -9.7944+42.5767j, -7.5682+52.1452j, -4.9781+31.9000j,
        -0.4770-5.5890j, 7.4238-37.8724j, 14.3288-46.5004j, 14.9138-27.7316j, 5.7220+5.4319j, -10.0506+32.6572j, -23.0979+39.3120j, -23.5330+24.9450j,
        -9.0988+1.0376j, 13.6646-17.0466j, 30.9490-21.1233j, 31.1980-13.6821j, 13.3288-2.2684j, -12.5264+5.2112j, -30.5561+6.2367j, -29.8474+4.6307j,
        -12.0690+5.0478j, 9.6322+9.0180j, 22.9237+12.9184j, 21.7015+10.6222j, 9.3396-1.1856j, -4.5837-17.4015j, -11.7555-28.2480j, -10.8916-24.4600j,
        -6.3945-4.3929j, -3.1969+22.3499j, -1.4541+40.2538j, 0.6530+38.3435j, 5.3226+16.4807j, 11.5192-14.2581j, 14.4291-37.1521j, 8.7124-39.6230j,
        -5.4829-21.8040j, -20.7514+5.0873j, -27.6453+27.1782j, -19.7068+34.3613j, 0.3606+25.3493j, 21.8368+5.7509j, 32.3954-14.6036j, 24.7448-26.2847j,
        2.2742-26.0359j, -21.9784-15.5346j, -34.9064-0.0581j, -28.7074+13.5670j, -4.9444+20.4800j, 24.1003+17.6968j, 41.2230+5.3632j, 35.6707-11.6508j,
        9.1771-25.2628j, -22.1425-28.2930j, -38.8634-18.9320j, -30.9584-0.5203j, -5.2262+17.8408j, 21.0994+27.2149j, 31.5234+23.8132j, 21.1365+9.8556j,
        -1.3592-7.7348j, -20.8647-21.1297j, -26.1002-25.7534j, -15.8284-20.2408j, 0.4495-5.9854j, 12.0044+13.0175j, 13.4550+28.5235j, 7.7107+30.8056j,
        1.6444+16.5423j, 0.1200-7.7917j, 1.0469-29.3147j, -1.0480-36.6136j, -8.3996-23.8981j, -16.4504+1.2872j, -16.3570+24.1858j, -3.9963+31.3402j,
        16.2982+19.4015j, 32.3522-2.6508j, 32.5456-20.3333j, 13.5961-24.0058j, -16.1576-13.1983j, -40.9904+3.9745j, -45.4703+16.8080j, -24.1876+18.1106j,
        12.4462+9.4298j, 43.3584-1.5839j, 49.8775-6.0027j, 27.0704-1.4925j, -12.1249+6.6573j, -44.4599+9.6387j, -50.7506+1.9153j, -27.9143-12.6605j,
        9.9861-23.3596j, 40.4215-20.4657j, 47.6341-2.4568j, 29.9793+20.5212j, 0.5586+32.6560j, -24.1526+24.0527j, -32.8887-1.4276j, -25.1566-27.6119j,
        -8.3047-37.8054j, 8.3969-24.9353j, 16.9110+3.3284j, 14.9537+30.3347j, 5.7759+39.6700j, -3.6369+25.6956j, -6.9529-3.6387j, -4.0552-31.6993j,
        0.8876-41.8909j, 3.1992-28.4243j, 0.3688+0.7622j, -4.7904+27.9128j, -7.4925+38.7789j, -3.3352+29.0599j, 6.2686+6.5573j, 15.7156-15.6791j,
        17.2700-27.1011j, 7.9230-24.0290j, -8.0701-10.3345j, -22.5922+4.8138j, -27.2434+12.8615j, -17.4211+11.1623j, 3.1873+3.1250j, 22.9731-4.1846j,
        29.7741-6.0138j, 19.3835-2.9361j, -2.6326-0.1426j, -22.6581-0.7461j, -29.0448-3.4409j, -17.4560-4.3857j, 4.0325-0.1217j, 21.6524+7.3171j,
        23.8460+12.4985j, 9.6375+10.5970j, -10.9514+1.4037j, -23.4015-10.6162j, -18.6629-17.8529j, -0.0989-15.2613j, 18.6009-4.2023j, 24.4013+8.1370j,
        14.0274+15.2079j, -4.7243+13.3267j, -18.5261+4.1913j, -18.1706-7.2293j, -5.7607-14.8260j, 9.0800-16.8572j, 15.4527-13.8653j, 9.1331-7.7126j,
        -4.1298-0.2090j, -13.8054+7.4431j, -12.5094+13.4579j, -0.9024+16.7357j, 13.0998+14.4587j, 19.0230+4.8008j, 11.9921-10.9766j, -3.9570-26.0289j,
        -18.0829-31.5947j, -20.2843-21.5776j, -9.1063+2.5010j, 8.0221+29.6231j, 20.1530+43.6857j, 19.7075+33.1382j, 8.5339+2.3426j, -5.9032-29.8051j,
        -15.6607-43.5495j, -17.5384-31.7484j, -11.6454-2.1032j, -0.8069+26.7304j, 10.0212+37.4636j, 16.6764+25.9419j, 16.5986+0.7517j, 9.8190-23.4467j,
        -1.0703-33.0681j, -11.4211-23.6324j, -16.6591-2.0755j, -12.4093+18.5888j, -0.9193+27.8319j, 9.7836+23.0118j, 12.1677+8.3128j, 4.5613-7.4870j)
test_sig_coeffs = (1.0000, -2.7733+0.0057j, 3.8177-0.0177j, -2.6493+0.0232j, 0.9132-0.0136j)
test_sig_var = (0.8996131,)


class test_specest_burg(gr_unittest.TestCase):
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_noiseprocess (self):
        """  Calculate coefficients of known signal and compare w/ precalculated results.
        We run the test twice to make sure no residual stuff affects calculation. """
        src = blocks.vector_source_c(test_sig * 2, False, len(test_sig))
        burg = specest.arburg_vcc(len(test_sig), len(test_sig_coeffs) - 1)
        dst_coeffs = blocks.vector_sink_c(len(test_sig_coeffs))
        dst_var = blocks.vector_sink_f()

        self.tb.connect(src, burg, dst_coeffs)
        self.tb.connect((burg, 1), dst_var)
        self.tb.run()

        result_coeffs = tuple(dst_coeffs.data())
        result_var = dst_var.data()

        self.assertFloatTuplesAlmostEqual(result_coeffs, test_sig_coeffs * 2, 4)
        self.assertFloatTuplesAlmostEqual(result_var, test_sig_var * 2, 6)

    def test_002_stream (self):
        """ Stream some data through the block to see it all works. """
        block_len = 256
        fft_len = 128
        order = 6
        n_blocks = 100

        src = analog.noise_source_c(analog.GR_GAUSSIAN, 1)
        head = blocks.head(gr.sizeof_gr_complex, n_blocks * block_len)
        burg = specest.burg(block_len, fft_len, order)
        dst = blocks.vector_sink_f(fft_len)

        self.tb.connect(src, head, burg, dst)
        try:
            self.tb.run()
        except:
            self.fail("Something's wrong -- an exception was thrown during runtime.")

    def test_003_burgoutput (self):
        pass
        # tbw -- the differences between Matlab, Octave and this are quite massive
        #src = blocks.vector_source_c(test_sig, False)
        #burg = specest.burg(len(test_sig), len(test_sig_specest), len(test_sig_coeffs)-1, False)
        #dst = blocks.vector_sink_f(len(test_sig_specest))

        #self.tb.connect(src, burg, dst)
        #self.tb.run()

        #result_specest = tuple(dst.data())

        #self.assertAlmostEqual(numpy.sum(test_sig_specest), numpy.sum(result_specest), 1)


if __name__ == '__main__':
    gr_unittest.main ()
