#
# Copyright 2008,2009,2010 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from __future__ import division

##################################################
# Imports
##################################################
from gnuradio import gr, blks2
from gnuradio.wxgui import common
from gnuradio.wxgui.pubsub import pubsub
from gnuradio.wxgui.constants import *
import math
from logpwrspectrum import *
import specest_window

##################################################
# FFT sink block (wrapper for old wxgui)
##################################################
class _spectrum_sink_base(gr.hier_block2, common.wxgui_hb):
	"""
	An spectrum block with real/complex inputs and a gui window.
	"""

	def __init__(
		self,
		parent,
		baseband_freq=0,
		ref_scale=2.0,
		y_per_div=10,
		y_divs=8,
		ref_level=50,
		sample_rate=1,
		pspectrum_len=512,
		specest_rate=specest_window.DEFAULT_FRAME_RATE,
		average=False,
		avg_alpha=None,
		title='',
		size=specest_window.DEFAULT_WIN_SIZE,
		peak_hold=False,
        use_persistence=False,
        persist_alpha=None,
        n = 1,
        m = 150,
        nsamples = 256,
        estimator = 'esprit',
		**kwargs #do not end with a comma
	):
		#ensure avg alpha
		if avg_alpha is None: avg_alpha = 2.0/specest_rate
                #ensure analog alpha
                if persist_alpha is None: 
                  actual_specest_rate=float(sample_rate/pspectrum_len)/float(max(1,int(float((sample_rate/pspectrum_len)/specest_rate))))
                  #print "requested_specest_rate ",specest_rate
                  #print "actual_specest_rate    ",actual_specest_rate
                  analog_cutoff_freq=0.5 # Hertz
                  #calculate alpha from wanted cutoff freq
                  persist_alpha = 1.0 - math.exp(-2.0*math.pi*analog_cutoff_freq/actual_specest_rate)
                  
		#init
		gr.hier_block2.__init__(
			self,
			"spectrum_sink",
			gr.io_signature(1, 1, self._item_size),
			gr.io_signature(0, 0, 0),
		)
		#blocks
		fft = self._specest_chain(
			sample_rate=sample_rate,
			pspectrum_len=pspectrum_len,
			frame_rate=specest_rate,
			ref_scale=ref_scale,
			avg_alpha=avg_alpha,
			average=average,
            n = n,
            m = m,
            nsamples = nsamples,
            estimator = estimator
		)
		msgq = gr.msg_queue(2)
		sink = gr.message_sink(gr.sizeof_float*pspectrum_len, msgq, True)

		#controller
		self.controller = pubsub()
		self.controller.subscribe(AVERAGE_KEY, fft.set_average)
		self.controller.publish(AVERAGE_KEY, fft.average)
		self.controller.subscribe(AVG_ALPHA_KEY, fft.set_avg_alpha)
		self.controller.publish(AVG_ALPHA_KEY, fft.avg_alpha)
		self.controller.subscribe(SAMPLE_RATE_KEY, fft.set_sample_rate)
		self.controller.publish(SAMPLE_RATE_KEY, fft.sample_rate)
		#start input watcher
		common.input_watcher(msgq, self.controller, MSG_KEY)
		#create window
		self.win = specest_window.specest_window(
			parent=parent,
			controller=self.controller,
			size=size,
			title=title,
			real=self._real,
			spectrum_len=pspectrum_len,
			baseband_freq=baseband_freq,
			sample_rate_key=SAMPLE_RATE_KEY,
			y_per_div=y_per_div,
			y_divs=y_divs,
			ref_level=ref_level,
			average_key=AVERAGE_KEY,
			avg_alpha_key=AVG_ALPHA_KEY,
			peak_hold=peak_hold,
			msg_key=MSG_KEY,
            use_persistence=use_persistence,
            persist_alpha=persist_alpha,
		)
		common.register_access_methods(self, self.win)
		setattr(self.win, 'set_baseband_freq', getattr(self, 'set_baseband_freq')) #BACKWARDS
		setattr(self.win, 'set_peak_hold', getattr(self, 'set_peak_hold')) #BACKWARDS
		#connect
		self.wxgui_connect(self, fft, sink)

class spectrum_sink_f(_spectrum_sink_base):
	_specest_chain = logpwrspectrum_f
	_item_size = gr.sizeof_float
	_real = True

class spectrum_sink_c(_spectrum_sink_base):
	_specest_chain = logpwrspectrum_c
	_item_size = gr.sizeof_gr_complex
	_real = False

# ----------------------------------------------------------------
# Standalone test app
# ----------------------------------------------------------------

import wx
from gnuradio.wxgui import stdgui2

class test_app_block (stdgui2.std_top_block):
    def __init__(self, frame, panel, vbox, argv):
        stdgui2.std_top_block.__init__ (self, frame, panel, vbox, argv)

        pspectrum_len = 1024

        # build our flow graph
        input_rate = 2e6

        #Generate some noise
        noise = gr.noise_source_c(gr.GR_GAUSSIAN, 1.0/10)

        # Generate a complex sinusoid
        #source = gr.file_source(gr.sizeof_gr_complex, 'foobar2.dat', repeat=True)

        src1 = gr.sig_source_c (input_rate, gr.GR_SIN_WAVE, -500e3, 1)
        src2 = gr.sig_source_c (input_rate, gr.GR_SIN_WAVE, 500e3, 1)
        src3 = gr.sig_source_c (input_rate, gr.GR_SIN_WAVE, -250e3, 2)

        # We add these throttle blocks so that this demo doesn't
        # suck down all the CPU available.  Normally you wouldn't use these.
        thr1 = gr.throttle(gr.sizeof_gr_complex, input_rate)

        sink1 = spectrum_sink_c (panel, title="Spectrum Sink", pspectrum_len=pspectrum_len,
                            sample_rate=input_rate, baseband_freq=0,
                            ref_level=0, y_per_div=20, y_divs=10, m = 70, n = 3, nsamples = 1024)
        vbox.Add (sink1.win, 1, wx.EXPAND)

        combine1=gr.add_cc()
        self.connect(src1,(combine1,0))
        self.connect(src2,(combine1,1))
        self.connect(src3,(combine1,2))
        self.connect(noise, (combine1,3))
        self.connect(combine1,thr1, sink1)
        
def main ():
    app = stdgui2.stdapp (test_app_block, "ESPRIT Sink Test App")
    app.MainLoop ()

if __name__ == '__main__':
    main ()
