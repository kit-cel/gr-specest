#!/usr/bin/env python
#
# Copyright 2011 Communications Engineering Lab, KIT
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
"""
Demonstrates a decision algorithm for QPSK and BPSK Signals based on the
spectral correlation density (cyclic spectrum). This is merely a small
demonstrator and should not be used for life-or-death type modulation
classification.
"""

import numpy
from specest import fam_matplotlib
import matplotlib.pylab as plt

def animate_bpsk_qpsk_detect(Np, P, L, fam_block, image, cbar):
    """ Alternative animate function: after reading an estimate,
    perform a simple check to see if the input was BPSK or QPSK.
    """
    while(True):
        raw = fam_block.get_estimate()
        data = numpy.array(raw)
        """ The actual decision code:
        Should work for unknown center frequencies,
        as long the max values are not at f=0, alpha=0"""
        f_max     = numpy.max(data[P*L, :])  # Max value on f-Axis
        alpha_max = numpy.max(data[:, Np])   # Max value on alpha-Axis
        tolerance = 0.8                      # Depends on the reliability of estimate
        if  alpha_max < tolerance*f_max:
            plt.title('QPSK')
        else:
            plt.title('BPSK')
        image.set_data(data)
        image.changed()
        cbar.set_clim(vmax=data.max())
        cbar.draw_all()
        plt.draw()
        yield True

def main():
    """ Setup plot widget and run. """
    Np = 32
    P  = 128
    L  = Np/8
    filename = 'bpsk_qpsk.bin'
    animate_func = lambda fam_block, image, cbar: animate_bpsk_qpsk_detect(Np, P, L, fam_block, image, cbar)
    fam_matplotlib.setup_fam_matplotlib(filename=filename, sample_type="float",
                                        Np=Np, P=P, L=L,
                                        verbose=False,
                                        animate_func=animate_func)

if __name__ == "__main__":
    main()

