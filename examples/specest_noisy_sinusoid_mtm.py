#!/usr/bin/env python

import wx
from optparse import OptionParser
from gnuradio import gr
from gnuradio import analog
from gnuradio import blocks
from gnuradio.wxgui import stdgui2, fftsink2, slider, form
import specest

class app_top_block(stdgui2.std_top_block):
    def __init__(self, frame, panel, vbox, argv):
        stdgui2.std_top_block.__init__(self, frame, panel, vbox, argv)
        self.frame = frame
        self.panel = panel
        parser = OptionParser(usage="%prog: [options]")
        parser.add_option("-N", "--dpsslength", type="int",
                help="Length of the DPSS", default="512")
        parser.add_option("-B", "--timebandwidthproduct", type="float",
                help="Time Bandwidthproduct used to calculate the DPSS", default="3")
        parser.add_option("-K", "--tapers", type="int",
                help="Number of Tapers used to calculate the Spectrum", default="5")
        parser.add_option("-W", "--weighting", type="choice", choices=("unity", "eigenvalues" ,"adaptive" ),
                help="weighting-type to be used (unity, eigenvalues, adaptive) ", default="adaptive")
        (options, args) = parser.parse_args ()
        self.options = options
        #setting up our signal
        self.samplingrate = 48000
        self.source = analog.sig_source_c(self.samplingrate, analog.GR_SIN_WAVE, 3000, 1)
        self.noise = analog.noise_source_c(analog.GR_GAUSSIAN,0.5)
        self.add = blocks.add_cc()
        self.throttle = blocks.throttle(gr.sizeof_gr_complex, self.samplingrate)
        #the actual spectrum estimator
        self.v2s = blocks.vector_to_stream(gr.sizeof_float, self.options.dpsslength)
        self.mtm = specest.mtm(
                N = self.options.dpsslength,
                NW = self.options.timebandwidthproduct,
                K = self.options.tapers,
                weighting = self.options.weighting
        )
        self.scope = specest.spectrum_sink_f(
                panel,
                title='Spectrum with %s weighting, Length %i and %i Tapers' % (
                    self.options.weighting, self.options.dpsslength, self.options.tapers
                ),
                spec_size=self.options.dpsslength,
                sample_rate=self.samplingrate,
                ref_level=80,
                avg_alpha=0.8,
                y_per_div=20
        )
        self.connect(self.source, (self.add, 0) )
        self.connect(self.noise, (self.add, 1) )
        self.connect(self.add, self.throttle, self.mtm)
        self.connect(self.mtm, self.v2s, self.scope)
        self._build_gui(vbox)

    def _set_status_msg(self, msg):
        self.frame.GetStatusBar().SetStatusText(msg, 0)

    def _build_gui(self, vbox):
        def _form_set_freq(kv):
            return self.set_freq(kv['freq'])
        vbox.Add(self.scope.win, 10, wx.EXPAND)
        #self._build_subpanel(vbox)

    def _build_subpanel(self, vbox_arg):
        # build a secondary information panel (sometimes hidden)
        # FIXME figure out how to have this be a subpanel that is always
        # created, but has its visibility controlled by foo.Show(True/False)
        def _form_set_decim(kv):
            return self.set_decim(kv['decim'])
        if not(self.show_debug_info):
            return
        panel = self.panel
        vbox = vbox_arg
        myform = self.myform
        #panel = wx.Panel(self.panel, -1)
        #vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((5,0), 0)
        myform['decim'] = form.int_field(
                parent=panel, sizer=hbox, label="Decim",
                callback=myform.check_input_and_call(_form_set_decim, self._set_status_msg))
        hbox.Add((5,0), 1)
        myform['fs@usb'] = form.static_float_field(
                parent=panel, sizer=hbox, label="Fs@USB")
        hbox.Add((5,0), 1)
        myform['dbname'] = form.static_text_field(
                parent=panel, sizer=hbox)
        hbox.Add((5,0), 1)
        myform['baseband'] = form.static_float_field(
                parent=panel, sizer=hbox, label="Analog BB")
        hbox.Add((5,0), 1)
        myform['ddc'] = form.static_float_field(
                parent=panel, sizer=hbox, label="DDC")
        hbox.Add((5,0), 0)
        vbox.Add(hbox, 0, wx.EXPAND)


if __name__ == '__main__':
    app = stdgui2.stdapp(app_top_block, "GUI GNU Radio Application", nstatus=1)
    app.MainLoop()

