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

# Demonstrates a decision algorithm for QPSK and BPSK Signals based on the 
# spectral correlation density (cyclc spectrum).

import numpy
import ctypes

import sys
import gtk, gobject
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pylab as plt
from gnuradio import gr
import specest
import time

# Parameters of Estimation

Np = 32
P= 128
L = Np/8


class top(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        #Settings
        
        self.src = gr.file_source(gr.sizeof_float,"/path/to/file.bin",True)	
        self.ftc = gr.float_to_complex(1)

        trt = gr.throttle(gr.sizeof_gr_complex,1.2*P*Np)
        self.sink = gr.null_sink(gr.sizeof_float*2*Np)

        self.cyclo_fam = specest.cyclo_fam(Np,P,L)
       	  
        self.connect(self.src,self.ftc,self.cyclo_fam,self.sink)
        
        self.estimate = self.cyclo_fam.get_estimate()

def animate():
        while(True):
            data = numpy.array(raw[0:(2*Np)*(2*P*L+1)])
            data.resize(2*Np-1, 2*P*L)
            data = numpy.transpose(data)
                        
            # the actual decision code
            # should work for unknown center frequencys, as long the max values are not at f=0, alpha=0 

            f_max     = numpy.max(data[P*L,:])      # Max value on f-Axis
	    alpha_max = numpy.max(data[:,Np])           # Max value on alpha-Axis	
            
 	    tolerance = 0.9			    # Depends on the reliableness of estimate

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
            
        
# Start top block
mytb = top()

# Start flowgraph
mytb.start()

# Calc first image to show
raw = ctypes.cast( mytb.estimate.__long__(), ctypes.POINTER( ctypes.c_float) )
data = numpy.array(raw[0:(2*Np-1)*2*P*L])

data.resize(2*Np-1, 2*P*L)
data = numpy.transpose(data)

image = plt.imshow(data,interpolation='nearest',animated=True,extent= (-0.5, 0.5-1.0/Np, -1.0, 1.0-1.0/(P*L)))
          
cbar = plt.colorbar(image)
plt.xlabel('frequency /fs')
plt.ylabel('cycle frequency /fs')
plt.axis('normal')
   
gobject.idle_add(lambda iter=animate(): iter.next())

plt.show()
