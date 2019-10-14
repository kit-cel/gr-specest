#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :
#
# Copyright 2011,2013 Communications Engineering Lab, KIT
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
Provides functionality to run the FAM on-line with Matplotlib output.
"""

import time
import numpy
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pylab as plt
from gnuradio import gr
from gnuradio import analog
from gnuradio import blocks
import specest

class FAMProcessor(gr.top_block):
    """ Simple flow graph: run file through FAM.
        Plotting is done in animate()! """
    def __init__(self, Np=32, P=128, L=2,
                 filename=None, sample_type='complex', verbose=True):
        gr.top_block.__init__(self)
        if filename is None:
            src = analog.noise_source_c(analog.GR_GAUSSIAN, 1)
            if verbose:
                print("Using Gaussian noise source.")
        else:
            if sample_type == 'complex':
                src = blocks.file_source(gr.sizeof_gr_complex, filename, True)
            else:
                fsrc = blocks.file_source(gr.sizeof_float, filename, True)
                src = blocks.float_to_complex()
                self.connect(fsrc, src)
            if verbose:
                print(("Reading data from %s" % filename))
        if verbose:
            print("FAM configuration:")
            print(("N'   = %d" % Np))
            print(("P    = %d" % P))
            print(("L    = %d" % L))
            #print "Δf   = %f" % asfd
        sink = blocks.null_sink(gr.sizeof_float * 2 * Np)
        self.cyclo_fam = specest.cyclo_fam(Np, P, L)
        self.connect(src, self.cyclo_fam, sink)

def animate(fam_block, image, cbar):
    """ Read the data from the running block and shove it onto
    the Matplotlib widget.
    """
    while True:
        raw = fam_block.get_estimate()
        data = numpy.array(raw)
        image.set_data(data)
        image.changed()
        cbar.set_clim(vmax=data.max())
        cbar.draw_all()
        plt.draw()
        yield True

def setup_fam_matplotlib(Np, P, L, filename, sample_type, verbose,
                         animate_func=animate):
    """Setup the FAM flow graph and Matplotlib and start it.  """
    mytb = FAMProcessor(filename=filename,
                        Np=Np, P=P, L=L,
                        sample_type=sample_type,
                        verbose=verbose)
    # Start Flowgraph in background, then give it some time to fire up
    mytb.start()
    time.sleep(3)
    # Calc First Image to Show, setup axis
    raw = mytb.cyclo_fam.get_estimate()
    data = numpy.array(raw)
    image = plt.imshow(data,
                       interpolation='nearest',
                       animated=True,
                       extent=(-0.5, 0.5-1.0/Np, -1.0, 1.0-1.0/(P*L)))
    cbar = plt.colorbar(image)
    plt.xlabel('frequency / fs')
    plt.ylabel('cycle frequency / fs')
    plt.axis('normal')
    plt.title('Magnitude of estimated cyclic spectrum with FAM')

    # optional:
    # pylab.axhline(linewidth=1, color='w')
    # pylab.axvline(linewidth=1, color='w')
    GObject.idle_add(lambda iter=animate_func(mytb.cyclo_fam, image, cbar): next(iter))
    plt.show()
