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

# Plots the magnituce of the spectral correlation density (cyclic spectrum) of a file 
# estimated with FAM

import numpy
import ctypes

import gtk, gobject
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pylab as plt
from gnuradio import gr
import specest
import time


# 

# Parameters of Estimation
Np = 32
P = 128
L = 2


class top(gr.top_block):

    def __init__(self):

        gr.top_block.__init__(self)
        # Settings   
        # TODO: Parsing Filename
        self.src  = src = gr.noise_source_f(gr.GR_GAUSSIAN, 1)
        #self.src = gr.file_source(gr.sizeof_float,"/path/to/file.bin",True)	

        self.ftc = gr.float_to_complex(1)
        self.sink = gr.null_sink(gr.sizeof_float*2*Np)
        self.cyclo_fam = specest.cyclo_fam(Np,P,L)
       	  
        self.connect(self.src,self.ftc,self.cyclo_fam,self.sink)
        
def animate():
        while(True):
            raw = mytb.cyclo_fam.get_estimate()
            data = numpy.array(raw)
                       
            image.set_data(data)
            image.changed()
            cbar.set_clim(vmax=data.max())

            cbar.draw_all()

            plt.draw()
            yield True        

# Go:
        
# Start Top Block
mytb = top()

# Start Flowgraph
mytb.start()

time.sleep(3)


# Calc First Image to Show
raw = mytb.cyclo_fam.get_estimate()
data = numpy.array(raw)

image = plt.imshow(data,interpolation='nearest',animated=True,extent= (-0.5, 0.5-1.0/Np, -1.0, 1.0-1.0/(P*L)))
                
cbar = plt.colorbar(image)
plt.xlabel('frequency /fs')
plt.ylabel('cycle frequency /fs')
plt.axis('normal')
plt.title('Magnitude of estimated cyclic spectrum with FAM')

# optional:
# pylab.axhline(linewidth=1, color='w')
# pylab.axvline(linewidth=1, color='w')
           
gobject.idle_add(lambda iter=animate(): iter.next())

plt.show()
