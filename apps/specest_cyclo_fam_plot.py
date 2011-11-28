#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
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
Plots the magnitude of the spectral correlation density
(cyclic spectrum) of a file estimated with FAM.

"""

import numpy
import time
from optparse import OptionParser

import gobject
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pylab as plt
from gnuradio import gr

import specest
from gnuradio.eng_option import eng_option

class FAMProcessor(gr.top_block):
    """ Simple flow graph: run file through FAM.
        Plotting is done in animate()! """
    def __init__(self, Np=32, P=128, L=2,
                 filename=None, sample_type='complex', verbose=True):
        gr.top_block.__init__(self)
        if filename is None:
            src = gr.noise_source_c(gr.GR_GAUSSIAN, 1)
            if verbose:
                print "Using Gaussian noise source."
        else:
            if sample_type == 'complex':
                src = gr.file_source(gr.sizeof_gr_complex, filename, True)
            else:
                fsrc = gr.file_source(gr.sizeof_float, filename, True)
                src = gr.float_to_complex()
                self.connect(fsrc, src)
            if verbose:
                print "Reading data from %s" % filename
        if verbose:
            print "FAM configuration:"
            print "N'   = %d" % Np
            print "P    = %d" % P
            print "L    = %d" % L
            #print "Δf   = %f" % asfd
        sink = gr.null_sink(gr.sizeof_float * 2 * Np)
        self.cyclo_fam = specest.cyclo_fam(Np, P, L)
        self.connect(src, self.cyclo_fam, sink)

def animate(fam_block, image, cbar):
    """ Read the data from the running block and shove it onto
    the Matplotlib widget.
    """
    while(True):
        raw = fam_block.get_estimate()
        data = numpy.array(raw)
        image.set_data(data)
        image.changed()
        cbar.set_clim(vmax=data.max())
        cbar.draw_all()
        plt.draw()
        yield True

def parse_options():
    """ Options parser. """
    usage = "%prog: [options] filename"
    parser = OptionParser(option_class=eng_option, usage=usage)
    parser.add_option("-s", "--sample-type", type="choice",
                      choices=("float", "complex"),
                      help="Set input type to float or complex.", default="complex")
    parser.add_option("-N", "--Np", type="int", default=32,
            help="N' (not N!)")
    parser.add_option("-P", type="int", default=128,
            help="P")
    parser.add_option("-L", default=2,
            help="L")
    (options, args) = parser.parse_args ()
    if len(args) != 1:
        return (options, None)
    return (options, args[0])

def main():
    """ Setup plot widget and run. """
    (options, filename) = parse_options()
    mytb = FAMProcessor(filename=filename,
                        Np=options.Np, P=options.P, L=options.L,
                        sample_type=options.sample_type)
    # Start Flowgraph in background, then give it some time to fire up
    mytb.start()
    time.sleep(3)
    # Calc First Image to Show, setup axis
    raw = mytb.cyclo_fam.get_estimate()
    data = numpy.array(raw)
    image = plt.imshow(data,
                        interpolation='nearest',
                        animated=True,
                        extent=(-0.5, 0.5-1.0/options.Np, -1.0, 1.0-1.0/(options.P*options.L)))
    cbar = plt.colorbar(image)
    plt.xlabel('frequency / fs')
    plt.ylabel('cycle frequency / fs')
    plt.axis('normal')
    plt.title('Magnitude of estimated cyclic spectrum with FAM')

    # optional:
    # pylab.axhline(linewidth=1, color='w')
    # pylab.axvline(linewidth=1, color='w')
    gobject.idle_add(lambda iter=animate(mytb.cyclo_fam, image, cbar): iter.next())
    plt.show()

if __name__ == "__main__":
    main()

