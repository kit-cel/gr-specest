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

from gnuradio import gr, window
import specest_gendpss
import specest_swig

## Estimates PSD using Thomson's multitaper method
# @param[in] N: Length of the FFT
# @param[in] NW: Time Bandwidth Product usually is of value 2, 2.5, 3.0, 3.5, or 4
# @param[in] K: Numbers of Tapers to use. K should be smaller than 2*NW
# @param[in] weighting: Which type of weighting to use for the eigenspectra. Choices can be 'unity','eigenvalues' or adaptive
class mtm(gr.hier_block2):
    """ Estimates PSD using Thomson's multitaper method. """
    def __init__(self, N=512 , NW=3 , K=5, weighting='adaptive', fftshift=False):
        gr.hier_block2.__init__(self, "mtm",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(1, 1, gr.sizeof_float*N))
        self.check_parameters(N, NW, K)

        self.s2v = gr.stream_to_vector(gr.sizeof_gr_complex, N)
        self.connect(self, self.s2v)

        dpss = specest_gendpss.gendpss(N=N, NW=NW, K=K)
        self.mtm = [eigenspectrum(dpss.dpssarray[i], fftshift) for i in xrange(K)]
        if weighting == 'adaptive':
            self.sum = specest_swig.adaptiveweighting_vff(N, dpss.lambdas)
            self.connect_mtm(K)
            self.connect(self.sum, self)
        elif weighting == 'unity':
            self.sum = gr.add_ff(N)
            self.divide = gr.multiply_const_vff([1./K]*N)
            self.connect_mtm(K)
            self.connect(self.sum, self.divide, self)
        elif weighting == 'eigenvalues':
            self.eigvalmulti = []
            self.lambdasum = 0
            for i in xrange(K):
                self.eigvalmulti.append(gr.multiply_const_vff([dpss.lambdas[i]]*N))
                self.lambdasum += dpss.lambdas[i]
            self.divide = gr.multiply_const_vff([1./self.lambdasum]*N)
            self.sum = gr.add_ff(N)
            self.connect_mtm(K)
            self.connect(self.sum, self.divide, self)
        else:
            raise ValueError, 'weighting-type should be: adaptive, unity or eigenvalues'


    def connect_mtm(self, K):
        """ Connects up all the eigenspectrum calculators. """
        for i in xrange(K):
            self.connect(self.s2v, self.mtm[i])
            self.connect(self.mtm[i], (self.sum, i))


    ## Checks the validity of parameters
    # @param[in] N: Length of the FFT
    # @param[in] NW: Time Bandwidth Product
    # @param[in] K: Numbers of Tapers to used
    def check_parameters(self, N, NW, K):
        """ Checks the validity of parameters. """
        if NW < 1: raise ValueError, 'NW must be greater than or equal to 1'
        if K < 2:  raise ValueError, 'K must be greater than or equal to 2'
        if (N % 1): raise TypeError, 'N has to be an integer'
        if N < 1:  raise ValueError, 'N has to be greater than 1'


## Computes the eigenspectra for the multitaper spectrum estimator:
# data ----> multiplication dpss ----> FFT ----> square ----> output eigenspectrum
# @param[in] dpss: the dpss used as a data taper
class eigenspectrum(gr.hier_block2):
    """ Computes the eigenspectra for the multitaper spectrum estimator:
    data --> multiplication dpss --> FFT --> mag-square --> output eigenspectrum """
    def __init__(self, dpss, fftshift=False):
        gr.hier_block2.__init__(self, "eigenspectrum",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*len(dpss)),
                gr.io_signature(1, 1, gr.sizeof_float*len(dpss)))
        self.window = dpss
        self.fft = gr.fft_vcc(len(dpss), True, self.window, fftshift)
        self.c2mag = gr.complex_to_mag_squared(len(dpss))
        self.connect(self, self.fft, self.c2mag, self)

