#!/usr/bin/env python

from gnuradio import gr, blks2
import specest
from gnuradio import uhd
from PyQt4 import QtGui, QtCore
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt
import sys
import numpy
import pylab
import os
import time

try:
    from specest_window import Ui_MainWindow
except ImportError:
    print "Error: could not find specest_window.py:"
    print "\t\"Please run: pyuic4 specest_window.ui -o specest_window.py\""
    sys.exit(1)

class dialog_box(QtGui.QMainWindow):
    def __init__(self, fg, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        self.fg = fg
	self.first_run = 0

        # Set up plot
        self.gui.plot.setTitle("Spectrum Estimate")
        self.gui.plot.setAxisTitle(Qwt.QwtPlot.xBottom, "Frequency (MHz)")
	self.gui.plot.setAxisTitle(Qwt.QwtPlot.yLeft, "Spectral Power Density (dB)")
        #Grid
        grid = Qwt.QwtPlotGrid()
	pen = Qt.QPen(Qt.Qt.DotLine)
	pen.setColor(Qt.Qt.black)
	pen.setWidth(0)
	grid.setPen(pen)
	grid.attach(self.gui.plot)
        #Curve
	pen_curve = Qt.QPen(Qt.Qt.SolidLine)
	pen_curve.setColor(Qt.Qt.blue)
	pen_curve.setWidth(1)
	self.curve = Qwt.QwtPlotCurve("Power Density")
        self.curve.attach(self.gui.plot)
	self.curve.setPen(pen_curve)

        # Set data in UI
	# General Settings
	self.set_input_selector(self.fg.input_selector())
	self.set_input_tab(self.fg.input_selector())
	self.set_method_selector(self.fg.method_selector())
	self.set_method_tab(self.fg.method_selector())
	self.set_center_f(self.fg.center_frequency())
	self.set_scale(self.fg.get_scale())
        # File Input Settings
        self.set_file_rec_samp_rate(self.fg.file_rec_samp_rate())
        self.set_file_file_to_open(self.fg.file_file_to_open())
        self.set_file_samp_type(self.fg.file_samp_type())
	# UHD Input Settings
	self.set_uhd_samp_type(self.fg.uhd_samp_type())
	self.set_uhd_board_num(self.fg.uhd_board_num())
	self.set_uhd_samp_rate(self.fg.uhd_samp_rate())
	self.set_uhd_gain(self.fg.uhd_gain())
	self.set_uhd_ant(self.fg.uhd_ant())
	self.set_uhd_subdev_spec(self.fg.uhd_subdev_spec())
        # Welch Settings
        self.set_welch_mov_avg_len(self.fg.welch_mov_avg_len())
        self.set_welch_overlap(self.fg.welch_overlap())
	self.set_welch_window(self.fg.welch_window())
	self.set_welch_window_option(self.fg.welch_window_option())
	self.set_welch_fft_size(self.fg.welch_fft_size())
	# Burg Settings
	self.set_burg_order(self.fg.burg_order())
	self.set_burg_fft_size(self.fg.burg_fft_size())
	self.set_burg_block_len(self.fg.burg_block_len())
	# fcov Settings
	self.set_fcov_order(self.fg.fcov_order())
	self.set_fcov_fft_size(self.fg.fcov_fft_size())
	self.set_fcov_block_len(self.fg.fcov_block_len())
	# fmcov Settings
	self.set_fmcov_order(self.fg.fmcov_order())
	self.set_fmcov_fft_size(self.fg.fmcov_fft_size())
	self.set_fmcov_block_len(self.fg.fmcov_block_len())
	# MTM Settings
	self.set_mtm_tbp(self.fg.mtm_tbp())
	self.set_mtm_num_tap(self.fg.mtm_num_tap())
	self.set_mtm_weight_method(self.fg.mtm_weight_method())
	self.set_mtm_dpss_len(self.fg.mtm_dpss_len())
	# Music Settings
	self.set_music_cor_size(self.fg.music_cor_size())
	self.set_music_sin_cnt(self.fg.music_sin_cnt())
	self.set_music_fft_size(self.fg.music_fft_size())
	# Esprit Settings
	self.set_esprit_cor_size(self.fg.esprit_cor_size())
	self.set_esprit_sin_cnt(self.fg.esprit_sin_cnt())
	self.set_esprit_fft_size(self.fg.esprit_fft_size())
	###########################################################
	##                Add new estimator here!         1/8    ##
	###########################################################

	# Connect control signals
        self.connect(self.gui.pause_button, QtCore.SIGNAL("clicked()"),
		                     self.pauseFg)
        self.connect(self.gui.run_button, QtCore.SIGNAL("clicked()"),
		                     self.runFg)
        self.connect(self.gui.close_button, QtCore.SIGNAL("clicked()"),
		                     self.stopFg)
	# Connect general signals
        self.connect(self.gui.input_selector, QtCore.SIGNAL("currentIndexChanged(int)"),
		                     self.input_selector_text)
        self.connect(self.gui.tabWidget_2, QtCore.SIGNAL("currentChanged(int)"),
		                     self.input_tab_text)
        self.connect(self.gui.method_selector, QtCore.SIGNAL("currentIndexChanged(int)"),
		                     self.method_selector_text)
        self.connect(self.gui.tabWidget, QtCore.SIGNAL("currentChanged(int)"),
		                     self.method_tab_text)
        self.connect(self.gui.center_f, QtCore.SIGNAL("valueChanged(double)"),
		                     self.center_f_text)
        self.connect(self.gui.scale, QtCore.SIGNAL("currentIndexChanged(int)"),
		                     self.scale_text)
        # File Input Signals	
        self.connect(self.gui.file_rec_samp_rate, QtCore.SIGNAL("editingFinished()"),
                     self.file_rec_samp_rate_text)
        self.connect(self.gui.file_file_to_open, QtCore.SIGNAL("editingFinished()"),
                     self.file_file_to_open_text)
        self.connect(self.gui.file_samp_type, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.file_samp_type_text)
        # UHD Input Signals
        self.connect(self.gui.uhd_samp_type, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.uhd_samp_type_text)
        self.connect(self.gui.uhd_gain, QtCore.SIGNAL("editingFinished()"),
                     self.uhd_gain_text)
        self.connect(self.gui.uhd_samp_rate, QtCore.SIGNAL("editingFinished()"),
                     self.uhd_samp_rate_text)
        self.connect(self.gui.uhd_board_num, QtCore.SIGNAL("editingFinished()"),
                     self.uhd_board_num_text)
        self.connect(self.gui.uhd_ant, QtCore.SIGNAL("editingFinished()"),
                     self.uhd_ant_text)
        self.connect(self.gui.uhd_subdev_spec, QtCore.SIGNAL("editingFinished()"),
                     self.uhd_subdev_spec_text)
        # Welch Signals
	self.connect(self.gui.welch_mov_avg, QtCore.SIGNAL("editingFinished()"),
                     self.welch_mov_avg_len_text)
        self.connect(self.gui.welch_overlap, QtCore.SIGNAL("valueChanged()"),
                     self.welch_overlap_text)
        self.connect(self.gui.welch_window, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.welch_window_text)
        self.connect(self.gui.welch_window_option, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.welch_window_option_text)
        self.connect(self.gui.welch_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.welch_fft_size_text)
	# Burg Signals
        self.connect(self.gui.burg_order, QtCore.SIGNAL("editingFinished()"),
                     self.burg_order_text)
        self.connect(self.gui.burg_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.burg_fft_size_text)
        self.connect(self.gui.burg_block_len, QtCore.SIGNAL("editingFinished()"),
                     self.burg_block_len_text)
	# fcov Signals
        self.connect(self.gui.fcov_order, QtCore.SIGNAL("editingFinished()"),
                     self.fcov_order_text)
        self.connect(self.gui.fcov_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.fcov_fft_size_text)
        self.connect(self.gui.fcov_block_len, QtCore.SIGNAL("editingFinished()"),
                     self.fcov_block_len_text)
	# fmcov Signals
        self.connect(self.gui.fmcov_order, QtCore.SIGNAL("editingFinished()"),
                     self.fmcov_order_text)
        self.connect(self.gui.fmcov_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.fmcov_fft_size_text)
        self.connect(self.gui.fmcov_block_len, QtCore.SIGNAL("editingFinished()"),
                     self.fmcov_block_len_text)
	# MTM Signals
        self.connect(self.gui.mtm_tbp, QtCore.SIGNAL("editingFinished()"),
                     self.mtm_tbp_text)
        self.connect(self.gui.mtm_num_tap, QtCore.SIGNAL("editingFinished()"),
                     self.mtm_num_tap_text)
        self.connect(self.gui.mtm_weight_method, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.mtm_weight_method_text)
        self.connect(self.gui.mtm_dpss_len, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.mtm_dpss_len_text)
	# Music Signals
        self.connect(self.gui.music_cor_size, QtCore.SIGNAL("editingFinished()"),
                     self.music_cor_size_text)
        self.connect(self.gui.music_sin_cnt, QtCore.SIGNAL("editingFinished()"),
                     self.music_sin_cnt_text)
        self.connect(self.gui.music_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.music_fft_size_text)
	# Esprit Signals
        self.connect(self.gui.esprit_cor_size, QtCore.SIGNAL("editingFinished()"),
                     self.esprit_cor_size_text)
        self.connect(self.gui.esprit_sin_cnt, QtCore.SIGNAL("editingFinished()"),
                     self.esprit_sin_cnt_text)
        self.connect(self.gui.esprit_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.esprit_fft_size_text)
	###########################################################
	##                Add new estimator here!         2/8    ##
	###########################################################

        self.__initTracking()
        self.__initZooming()

    # Plot data
    def plot_data(self, data_x, data_y, rescale_at_sample_num):
        self.x = data_x
	self.y = data_y
	self.curve.setData(self.x, self.y)
	if(self.first_run == (rescale_at_sample_num + 1)):
	    scale_div = self.gui.plot.axisScaleDiv(Qwt.QwtPlot.yLeft)
	    self.gui.plot.setAxisScaleDiv(Qwt.QwtPlot.yLeft, scale_div)
	    self.zoomer.setZoomBase()
	    self.first_run = self.first_run + 1
        elif(self.first_run == 0):
	    self.gui.plot.setAxisAutoScale(Qwt.QwtPlot.yLeft)
	    self.gui.plot.setAxisScale(Qwt.QwtPlot.xBottom, self.x.item(1), self.x.item(data_x.size -1))
	    self.first_run = 1
        elif(self.first_run == rescale_at_sample_num):
	    self.gui.plot.setAxisAutoScale(Qwt.QwtPlot.yLeft)
	    self.gui.plot.setAxisScale(Qwt.QwtPlot.xBottom, self.x.item(1), self.x.item(data_x.size -1))
	    self.first_run = self.first_run + 1
        elif(self.first_run > 0 and self.first_run < rescale_at_sample_num):
	    self.first_run = self.first_run + 1
	self.gui.plot.replot()

    # Pause/Run Flowgraoh
    def pauseFg(self):
        if(self.gui.pause_button.text() == "Pause"):
            self.fg.stop()
            self.fg.wait()
            self.gui.pause_button.setText("Unpause")
        else:
            self.fg.start()
            self.gui.pause_button.setText("Pause")

    def runFg(self):
	self.fg.start()

    def stopFg(self):
	self.fg.sink.watcher.quit()
	self.fg.stop()

    # Functions to manipulate parameters in GUI
    def set_input_selector(self, src_type):
	if(src_type == "File"):
            self.gui.input_selector.setCurrentIndex(0)
        elif(src_type == "UHD"):
            self.gui.input_selector.setCurrentIndex(1)
	else:
	    pass

    def set_input_tab(self, src_type):
	if(src_type == "File"):
            self.gui.tabWidget_2.setCurrentIndex(0)
        elif(src_type == "UHD"):
            self.gui.tabWidget_2.setCurrentIndex(1)
	else:
	    pass

    def set_method_selector(self, method):
	if(method == "Welch"):
            self.gui.method_selector.setCurrentIndex(0)
        elif(method == "Burg"):
            self.gui.method_selector.setCurrentIndex(1)
        elif(method == "fcov"):
            self.gui.method_selector.setCurrentIndex(2)
        elif(method == "fmcov"):
            self.gui.method_selector.setCurrentIndex(3)
        elif(method == "MTM"):
            self.gui.method_selector.setCurrentIndex(4)
        elif(method == "Music"):
            self.gui.method_selector.setCurrentIndex(5)
        elif(method == "Esprit"):
            self.gui.method_selector.setCurrentIndex(6)
	else:
	    pass

    def set_method_tab(self, method):
	if(method == "Welch"):
            self.gui.tabWidget.setCurrentIndex(0)
        elif(method == "Burg"):
            self.gui.tabWidget.setCurrentIndex(1)
        elif(method == "fcov"):
            self.gui.tabWidget.setCurrentIndex(2)
        elif(method == "fmcov"):
            self.gui.tabWidget.setCurrentIndex(3)
        elif(method == "MTM"):
            self.gui.tabWidget.setCurrentIndex(4)
        elif(method == "Music"):
            self.gui.tabWidget.setCurrentIndex(5)
        elif(method == "Esprit"):
            self.gui.tabWidget.setCurrentIndex(6)
	else:
	    pass

    def set_center_f(self, center_f):
        self.gui.center_f.setValue(center_f)

    def set_scale(self, scale):
	if(scale == "Logarithmic"):
            self.gui.scale.setCurrentIndex(0)
        elif(scale == "Linear"):
            self.gui.scale.setCurrentIndex(1)
	else:
	    pass

    def set_file_rec_samp_rate(self, samp_rate):
        self.gui.file_rec_samp_rate.setText(QtCore.QString("%1").arg(samp_rate))

    def set_file_file_to_open(self, file_to_open):
        self.gui.file_file_to_open.setText(QtCore.QString("%1").arg(file_to_open))

    def set_file_samp_type(self, samp_type):
	if(samp_type == gr.sizeof_gr_complex):
            self.gui.file_samp_type.setCurrentIndex(0)
        elif(samp_type == gr.sizeof_float):
            self.gui.file_samp_type.setCurrentIndex(1)
	else:
	    print "Wrong sample-type set!"

    def set_uhd_samp_type(self, samp_type):
	if(samp_type == gr.sizeof_gr_complex):
            self.gui.uhd_samp_type.setCurrentIndex(0)
        elif(samp_type == gr.sizeof_float):
            self.gui.uhd_samp_type.setCurrentIndex(1)
	else:
	    print "Wrong sample-type set!"

    def set_uhd_gain(self, gain):
        self.gui.uhd_gain.setValue(gain)

    def set_uhd_board_num(self, board_num):
        self.gui.uhd_board_num.setValue(board_num)

    def set_uhd_samp_rate(self, samp_rate):
        self.gui.uhd_samp_rate.setValue(samp_rate)

    def set_uhd_ant(self, ant):
        self.gui.uhd_ant.setText(QtCore.QString("%1").arg(ant))

    def set_uhd_subdev_spec(self, subdev_spec):
        self.gui.uhd_subdev_spec.setText(QtCore.QString("%1").arg(subdev_spec))

    def set_welch_mov_avg_len(self, mov_avg):
        self.gui.welch_mov_avg.setValue(mov_avg)

    def set_welch_overlap(self, overlap):
        self.gui.welch_overlap.setValue(overlap)

    def set_welch_window(self, window):
	if(window == "Hann"):
            self.gui.welch_window.setCurrentIndex(0)
        elif(window == "Hamming"):
            self.gui.welch_window.setCurrentIndex(1)
        elif(window == "Kaiser"):
            self.gui.welch_window.setCurrentIndex(2)
        elif(window == "Blackman"):
            self.gui.welch_window.setCurrentIndex(3)
        elif(window == "Blackman-Harris"):
            self.gui.welch_window.setCurrentIndex(4)
        elif(window == "Rectangular"):
            self.gui.welch_window.setCurrentIndex(5)
	else:
	    pass

    def set_welch_window_option(self, window_option):
        self.gui.welch_window_option.setValue(window_option)

    def set_welch_fft_size(self, fft_size):
	if(fft_size == 16):
            self.gui.welch_fft_size.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.welch_fft_size.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.welch_fft_size.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.welch_fft_size.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.welch_fft_size.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.welch_fft_size.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.welch_fft_size.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.welch_fft_size.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.welch_fft_size.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.welch_fft_size.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.welch_fft_size.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.welch_fft_size.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.welch_fft_size.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    def set_burg_order(self, order):
        self.gui.burg_order.setValue(order)

    def set_burg_block_len(self, block_len):
        self.gui.burg_block_len.setValue(block_len)

    def set_burg_fft_size(self, fft_size):
	if(fft_size == 16):
            self.gui.burg_fft_size.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.burg_fft_size.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.burg_fft_size.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.burg_fft_size.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.burg_fft_size.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.burg_fft_size.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.burg_fft_size.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.burg_fft_size.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.burg_fft_size.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.burg_fft_size.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.burg_fft_size.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.burg_fft_size.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.burg_fft_size.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    def set_fcov_order(self, order):
        self.gui.fcov_order.setValue(order)

    def set_fcov_block_len(self, block_len):
        self.gui.fcov_block_len.setValue(block_len)

    def set_fcov_fft_size(self, fft_size):
	if(fft_size == 16):
            self.gui.fcov_fft_size.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.fcov_fft_size.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.fcov_fft_size.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.fcov_fft_size.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.fcov_fft_size.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.fcov_fft_size.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.fcov_fft_size.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.fcov_fft_size.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.fcov_fft_size.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.fcov_fft_size.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.fcov_fft_size.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.fcov_fft_size.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.fcov_fft_size.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    def set_fmcov_order(self, order):
        self.gui.fmcov_order.setValue(order)

    def set_fmcov_block_len(self, block_len):
        self.gui.fmcov_block_len.setValue(block_len)

    def set_fmcov_fft_size(self, fft_size):
	if(fft_size == 16):
            self.gui.fmcov_fft_size.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.fmcov_fft_size.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.fmcov_fft_size.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.fmcov_fft_size.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.fmcov_fft_size.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.fmcov_fft_size.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.fmcov_fft_size.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.fmcov_fft_size.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.fmcov_fft_size.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.fmcov_fft_size.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.fmcov_fft_size.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.fmcov_fft_size.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.fmcov_fft_size.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    def set_mtm_tbp(self, tbp):
        self.gui.mtm_tbp.setValue(tbp)

    def set_mtm_num_tap(self, num_tap):
        self.gui.mtm_num_tap.setValue(num_tap)

    def set_mtm_dpss_len(self, dpss_len):
        self.gui.mtm_dpss_len.setValue(dpss_len)

    def set_mtm_dpss_len(self, fft_size):
	if(fft_size == 16):
            self.gui.mtm_dpss_len.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.mtm_dpss_len.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.mtm_dpss_len.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.mtm_dpss_len.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.mtm_dpss_len.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.mtm_dpss_len.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.mtm_dpss_len.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.mtm_dpss_len.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.mtm_dpss_len.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.mtm_dpss_len.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.mtm_dpss_len.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.mtm_dpss_len.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.mtm_dpss_len.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    def set_mtm_weight_method(self, method):
	if(method == "unity"):
            self.gui.mtm_weight_method.setCurrentIndex(0)
        elif(method == "eigenvalues"):
            self.gui.mtm_weight_method.setCurrentIndex(1)
        elif(method == "adaptive"):
            self.gui.mtm_weight_method.setCurrentIndex(2)
	else:
	    pass

    def set_music_cor_size(self, cor_size):
        self.gui.music_cor_size.setValue(cor_size)

    def set_music_sin_cnt(self, sin_cnt):
        self.gui.music_sin_cnt.setValue(sin_cnt)

    def set_music_fft_size(self, fft_size):
	if(fft_size == 16):
            self.gui.music_fft_size.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.music_fft_size.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.music_fft_size.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.music_fft_size.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.music_fft_size.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.music_fft_size.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.music_fft_size.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.music_fft_size.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.music_fft_size.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.music_fft_size.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.music_fft_size.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.music_fft_size.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.music_fft_size.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    def set_esprit_cor_size(self, cor_size):
        self.gui.esprit_cor_size.setValue(cor_size)

    def set_esprit_sin_cnt(self, sin_cnt):
        self.gui.esprit_sin_cnt.setValue(sin_cnt)

    def set_esprit_fft_size(self, fft_size):
	if(fft_size == 16):
            self.gui.esprit_fft_size.setCurrentIndex(0)
	elif(fft_size == 32):
            self.gui.esprit_fft_size.setCurrentIndex(1)
	elif(fft_size == 64):
            self.gui.esprit_fft_size.setCurrentIndex(2)
	elif(fft_size == 128):
            self.gui.esprit_fft_size.setCurrentIndex(3)
	elif(fft_size == 256):
            self.gui.esprit_fft_size.setCurrentIndex(4)
	elif(fft_size == 512):
            self.gui.esprit_fft_size.setCurrentIndex(5)
	elif(fft_size == 1024):
            self.gui.esprit_fft_size.setCurrentIndex(6)
	elif(fft_size == 2048):
            self.gui.esprit_fft_size.setCurrentIndex(7)
	elif(fft_size == 4096):
            self.gui.esprit_fft_size.setCurrentIndex(8)
	elif(fft_size == 8192):
            self.gui.esprit_fft_size.setCurrentIndex(9)
	elif(fft_size == 16384):
            self.gui.esprit_fft_size.setCurrentIndex(10)
	elif(fft_size == 32768):
            self.gui.esprit_fft_size.setCurrentIndex(11)
	elif(fft_size == 65536):
            self.gui.esprit_fft_size.setCurrentIndex(12)
	else:
	    print "Invalid FFT-Size!"

    ###########################################################
    ##                Add new estimator here!         3/8    ##
    ###########################################################

    # Functions to change parameters in flowgraph
    def input_selector_text(self):
        try:
            src_type = str(self.gui.input_selector.currentText())
            self.fg.set_src_type(src_type)
	    self.set_input_tab(src_type)
        except RuntimeError:
            pass

    def input_tab_text(self, tab):
        ### Add code to execute, when input-tab changes!
	input_tab = tab

    def method_selector_text(self):
        try:
            method = str(self.gui.method_selector.currentText())
            self.fg.set_method(method)
	    self.set_method_tab(method)
        except RuntimeError:
            pass

    def method_tab_text(self, tab):
        ### Add code to execute, when method-tab changes!
	method_tab = tab

    def center_f_text(self):
        try:
            center_f = self.gui.center_f.value()
            self.fg.set_center_f(center_f)
        except RuntimeError:
            pass

    def scale_text(self):
        try:
            scale = str(self.gui.scale.currentText())
            self.fg.set_scale(scale)
        except RuntimeError:
            pass

    def file_rec_samp_rate_text(self):
        try:
            rec_samp_rate = self.gui.file_rec_samp_rate.text().toLong()[0]
            self.fg.set_file_rec_samp_rate(rec_samp_rate)
        except RuntimeError:
            pass

    def file_file_to_open_text(self):
        try:
            file_to_open = str(self.gui.file_file_to_open.text())
            self.fg.set_file_to_open(file_to_open)
        except RuntimeError:
            pass

    def file_samp_type_text(self):
        try:
            samp_type = str(self.gui.file_samp_type.currentText())
            self.fg.set_file_samp_type(samp_type)
        except RuntimeError:
            pass

    def uhd_samp_type_text(self):
        try:
            samp_type = str(self.gui.uhd_samp_type.currentText())
            self.fg.set_uhd_samp_type(samp_type)
        except RuntimeError:
            pass

    def uhd_gain_text(self):
        try:
            gain = self.gui.uhd_gain.text().toLong()[0]
            self.fg.set_uhd_gain(gain)
        except RuntimeError:
            pass

    def uhd_board_num_text(self):
        try:
            board_num = self.gui.uhd_board_num.text().toLong()[0]
            self.fg.set_uhd_board_num(board_num)
        except RuntimeError:
            pass

    def uhd_samp_rate_text(self):
        try:
            samp_rate = self.gui.uhd_samp_rate.text().toLong()[0]
            self.fg.set_uhd_samp_rate(samp_rate)
        except RuntimeError:
            pass

    def uhd_ant_text(self):
        try:
            ant = str(self.gui.uhd_ant.text())
            self.fg.set_uhd_ant(ant)
        except RuntimeError:
            pass

    def uhd_subdev_spec_text(self):
        try:
            subdev_spec = str(self.gui.uhd_subdev_spec.text())
            self.fg.set_uhd_subdev_spec(subdev_spec)
        except RuntimeError:
            pass

    def welch_mov_avg_len_text(self):
        try:
            mal = self.gui.welch_mov_avg.text().toLong()[0]
            self.fg.set_welch_mov_avg_len(mal)
        except RuntimeError:
            pass

    def welch_overlap_text(self):
        try:
            ol = self.gui.welch_overlap.text().toLong()[0]
            self.fg.set_welch_overlap(ol)
        except RuntimeError:
            pass

    def welch_window_text(self):
        try:
            window = str(self.gui.welch_window.currentText())
            self.fg.set_welch_window(window)
        except RuntimeError:
            pass

    def welch_window_option_text(self):
        try:
            window_option = self.gui.welch_window_option.text().toLong()[0]
            self.fg.set_welch_window_option(window_option)
        except RuntimeError:
            pass

    def welch_fft_size_text(self):
        try:
            fft_size = self.gui.welch_fft_size.currentText().toLong()[0]
            self.fg.set_welch_fft_size(fft_size)
        except RuntimeError:
            pass

    def burg_order_text(self):
        try:
            order = self.gui.burg_order.text().toLong()[0]
            self.fg.set_burg_order(order)
        except RuntimeError:
            pass

    def burg_block_len_text(self):
        try:
            block_len = self.gui.burg_block_len.text().toLong()[0]
            self.fg.set_burg_block_len(block_len)
        except RuntimeError:
            pass

    def burg_fft_size_text(self):
        try:
            fft_size = self.gui.burg_fft_size.currentText().toLong()[0]
            self.fg.set_burg_fft_size(fft_size)
        except RuntimeError:
            pass

    def fcov_order_text(self):
        try:
            order = self.gui.fcov_order.text().toLong()[0]
            self.fg.set_fcov_order(order)
        except RuntimeError:
            pass

    def fcov_block_len_text(self):
        try:
            block_len = self.gui.fcov_block_len.text().toLong()[0]
            self.fg.set_fcov_block_len(block_len)
        except RuntimeError:
            pass

    def fcov_fft_size_text(self):
        try:
            fft_size = self.gui.fcov_fft_size.currentText().toLong()[0]
            self.fg.set_fcov_fft_size(fft_size)
        except RuntimeError:
            pass

    def fmcov_order_text(self):
        try:
            order = self.gui.fmcov_order.text().toLong()[0]
            self.fg.set_fmcov_order(order)
        except RuntimeError:
            pass

    def fmcov_block_len_text(self):
        try:
            block_len = self.gui.fmcov_block_len.text().toLong()[0]
            self.fg.set_fmcov_block_len(block_len)
        except RuntimeError:
            pass

    def fmcov_fft_size_text(self):
        try:
            fft_size = self.gui.fmcov_fft_size.currentText().toLong()[0]
            self.fg.set_fmcov_fft_size(fft_size)
        except RuntimeError:
            pass

    def mtm_tbp_text(self):
        try:
            tbp = self.gui.mtm_tbp.text().toDouble()[0]
            self.fg.set_mtm_tbp(tbp)
        except RuntimeError:
            pass

    def mtm_num_tap_text(self):
        try:
            num_tap = self.gui.mtm_num_tap.text().toLong()[0]
            self.fg.set_mtm_num_tap(num_tap)
        except RuntimeError:
            pass

    def mtm_weight_method_text(self):
        try:
            method = str(self.gui.mtm_weight_method.currentText())
            self.fg.set_mtm_weight_method(method)
        except RuntimeError:
            pass

    def mtm_dpss_len_text(self):
        try:
            dpss_len = self.gui.mtm_dpss_len.text().toLong()[0]
            self.fg.set_mtm_dpss_len(dpss_len)
        except RuntimeError:
            pass

    def mtm_dpss_len_text(self):
        try:
            fft_size = self.gui.mtm_dpss_len.currentText().toLong()[0]
            self.fg.set_mtm_dpss_len(fft_size)
        except RuntimeError:
            pass

    def music_cor_size_text(self):
        try:
            cor_size = self.gui.music_cor_size.text().toLong()[0]
            self.fg.set_music_cor_size(cor_size)
        except RuntimeError:
            pass

    def music_sin_cnt_text(self):
        try:
            sin_cnt = self.gui.music_sin_cnt.text().toLong()[0]
            self.fg.set_music_sin_cnt(sin_cnt)
        except RuntimeError:
            pass

    def music_fft_size_text(self):
        try:
            fft_size = self.gui.music_fft_size.currentText().toLong()[0]
            self.fg.set_music_fft_size(fft_size)
        except RuntimeError:
            pass

    def esprit_cor_size_text(self):
        try:
            cor_size = self.gui.esprit_cor_size.text().toLong()[0]
            self.fg.set_esprit_cor_size(cor_size)
        except RuntimeError:
            pass

    def esprit_sin_cnt_text(self):
        try:
            sin_cnt = self.gui.esprit_sin_cnt.text().toLong()[0]
            self.fg.set_esprit_sin_cnt(sin_cnt)
        except RuntimeError:
            pass

    def esprit_fft_size_text(self):
        try:
            fft_size = self.gui.esprit_fft_size.currentText().toLong()[0]
            self.fg.set_esprit_fft_size(fft_size)
        except RuntimeError:
            pass

    ###########################################################
    ##                Add new estimator here!         4/8    ##
    ###########################################################

    # Functions needed for zooming
    def __initTracking(self):
        self.connect(Spy(self.gui.plot.canvas()),
                     Qt.SIGNAL("MouseMove"),
                     self.showCoordinates) 

    def showCoordinates(self, position):
        self.statusBar().showMessage(
            'f = %.6g MHz | P = %.6g (dB)'
            % (self.gui.plot.invTransform(Qwt.QwtPlot.xBottom, position.x()),
               self.gui.plot.invTransform(Qwt.QwtPlot.yLeft, position.y())))
    
    def __initZooming(self):
        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.ActiveOnly,
                                        self.gui.plot.canvas())
        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.black))
	self.zoomer.initMousePattern(0)
       
class Spy(Qt.QObject):
    
    def __init__(self, parent):
        Qt.QObject.__init__(self, parent)
        parent.setMouseTracking(True)
        parent.installEventFilter(self)

    def eventFilter(self, _, event):
        if event.type() == Qt.QEvent.MouseMove:
            self.emit(Qt.SIGNAL("MouseMove"), event.pos())
        return False

class _queue_watcher_thread(QtCore.QThread):
    def __init__(self, msgq, d_len, d_type_numpy, samp_rate, center_f):
	QtCore.QThread.__init__(self)
	self.msgq = msgq
        self.keep_running = True
	self.d_type_numpy = d_type_numpy
	self.d_len = d_len
	self.samp_rate = samp_rate
	self.center_f = center_f
	self.start()
        self.x_values = (pylab.array(range(-(self.d_len / 2), (self.d_len / 2)))) * self.samp_rate / 2 / round(self.d_len/2) / 1e6 + self.center_f

    def run(self):
        while self.keep_running:
	    msg = self.msgq.delete_head()
	    samples = numpy.fromstring(msg.to_string(), self.d_type_numpy)[:self.d_len]
	    self.emit(Qt.SIGNAL("new_plot_data(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.x_values, samples, 13)

    def set_samp_rate(self, samp_rate):
	self.samp_rate = samp_rate
        self.x_values = (pylab.array(range(-(self.d_len / 2), (self.d_len / 2)))) * self.samp_rate / 2 / round(self.d_len/2) / 1e6 + self.center_f

    def set_center_f(self, center_f):
	self.center_f = center_f
        self.x_values = (pylab.array(range(-(self.d_len / 2), (self.d_len / 2)))) * self.samp_rate / 2 / round(self.d_len/2) / 1e6 + self.center_f

class plot_sink(gr.hier_block2):
    def __init__(self, d_type, d_len, qt_box, d_type_numpy, samp_rate, center_f):
	gr.hier_block2.__init__(self, "plot_sink",
		    gr.io_signature(1, 1, d_type * d_len),
		    gr.io_signature(0, 0, 0))

	self.msgq = gr.msg_queue(1)
        self.snk = gr.message_sink(d_type * d_len, self.msgq, True)
	self.connect(self, self.snk)

        self.watcher = _queue_watcher_thread(self.msgq, d_len, d_type_numpy, samp_rate, center_f)

	qt_box.connect(self.watcher, Qt.SIGNAL("new_plot_data(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), qt_box.plot_data)

class head(gr.hier_block2):
    def __init__(self, fg, src_type, file_samp_type, file_to_open, file_rec_samp_rate, uhd_samp_rate, uhd_gain, center_f, uhd_subdev_spec):
	gr.hier_block2.__init__(self, "head",
		    gr.io_signature(0, 0, 0),
		    gr.io_signature(1, 1, gr.sizeof_gr_complex))

        if(src_type == "File"):
	    try:
                self.head_src = gr.file_source(file_samp_type, file_to_open, True)
		fg.set_samp_rate(file_rec_samp_rate)
		fg.uhd_src_active = False
		fg.cpu_watcher.quit()
		if(file_samp_type == gr.sizeof_float):
		    self.head_bottom = gr.float_to_complex()
		    self.connect((self.head_src, 0), (self.head_bottom, 0))
		    self.connect((self.head_bottom, 0), (self, 0))
		else:
		    self.connect((self.head_src, 0), (self, 0))
	    except RuntimeError:
		print "Could not initialize file-source!"
		self.head_src = None
	elif(src_type == "UHD"):
	    try:
	        self.head_src = uhd.single_usrp_source(device_addr='', io_type=uhd.io_type_t.COMPLEX_FLOAT32, num_channels=1)
	        self.head_src.set_samp_rate(fg.d_uhd_samp_rate)
	        self.head_src.set_gain(fg.d_uhd_gain, 0)
	        self.head_src.set_center_freq(fg.center_f*1e6 ,0)
		self.head_src.set_subdev_spec(fg.d_uhd_subdev_spec)
		fg.set_samp_rate(fg.d_uhd_samp_rate)
		fg.uhd_src_active = True
		fg.cpu_watcher.start()
		if(fg.d_uhd_samp_type == gr.sizeof_float):
		    self.head_bottom = gr.float_to_complex()
		    self.connect((self.head_src, 0), (self.head_bottom, 0))
		    self.connect((self.head_bottom, 0), (self, 0))
		else:
		    self.connect((self.head_src, 0), (self, 0))
	    except RuntimeError:
		print "Could not initialize UHD source!"
		self.head_src = None
        else:
            print "Unknown type of source!"

class _cpu_usage_watcher_thread(QtCore.QThread):
    def __init__(self, fg):
	QtCore.QThread.__init__(self)
	self.fg = fg
	self.keep_running = 1
	self.measurement_interval = 0.5

    def get_cpu_load(self):
	stats = file("/proc/stat", "r")
	stats.readline()
	cpu_load = None
	while stats.read(3) == "cpu":
		if cpu_load != None:
			cpu_load.extend(stats.readline().split(" ")[1:5])
		else:
			cpu_load = stats.readline().split(" ")[1:5]
	stats.close()
	for i in range(len(cpu_load)):
		cpu_load[i] = int(cpu_load[i])
	return cpu_load

    def run(self):
	while self.keep_running:
		load_old = self.get_cpu_load()
		num_cpus = len(load_old) / 4
		time.sleep(self.measurement_interval)
		load = self.get_cpu_load()
		cpu_idle_min = 1
		for i in range(len(load)):
			load[i] -= load_old[i]
		for i in range(num_cpus):
			cpu_idle = float(load[(i * 4 - 1)]) / sum(load[(i * 4):((i + 1) * 4)])
			if cpu_idle < 0.1 and self.fg.uhd_src_active == True:
				self.fg.set_decimation(self.fg.decimation + 1)
			if cpu_idle_min > cpu_idle:
				cpu_idle_min = cpu_idle
			if cpu_idle_min > 0.7 and self.fg.decimation > 1:
				self.fg.set_decimation(self.fg.decimation - 1)

class decimator(gr.hier_block2):
    def __init__(self, block_len, n, uhd_src_active, file_rec_samp_rate):
	gr.hier_block2.__init__(self, "decimator",
		    gr.io_signature(1, 1, gr.sizeof_gr_complex),
		    gr.io_signature(1, 1, gr.sizeof_gr_complex))

	if(uhd_src_active == True):
            self.stv = gr.stream_to_vector(gr.sizeof_gr_complex, block_len)
	    self.decim = gr.keep_one_in_n(block_len * gr.sizeof_gr_complex, n)
	    self. vts = gr.vector_to_stream(gr.sizeof_gr_complex, block_len)

	    self.connect(self, self.stv)
	    self.connect(self.stv, self.decim)
	    self.connect(self.decim, self.vts)
	    self.connect(self.vts, self)

	else:
	    self.throttle = gr.throttle(gr.sizeof_gr_complex, file_rec_samp_rate)
	    self.connect(self, self.throttle)
	    self.connect(self.throttle, self)

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.qapp = QtGui.QApplication(sys.argv)

        # Set Parameters
	self.shift_fft = True
	self.decimation = 1
	self.decimation_step = 50
	self.center_f = 102
	self.estimator = "Welch"
	self.src_type = "File"
	self.scale = "Logarithmic"
	# File Source Parameters
	self.d_file_rec_samp_rate = 32e3
	self.d_file_file_to_open = "4cos.dat"
	self.d_file_samp_type = gr.sizeof_gr_complex
	# UHD Source Parameters
	self.d_uhd_samp_type = gr.sizeof_gr_complex
	self.d_uhd_gain = 30
	self.d_uhd_ant = "Rx"
	self.d_uhd_subdev_spec = "B:0"
	self.d_uhd_board_num = 0
	self.d_uhd_samp_rate = 0.5e6
	# Welch Parameters
	self.d_welch_mov_avg_len = 8
	self.d_welch_overlap = -1
	self.d_welch_window = "Hamming"
	self.d_welch_window_option = 0.00
	self.d_welch_fft_size = 512
	# Burg Parameters
	self.d_burg_order = 4
	self.d_burg_block_len = 128
	self.d_burg_fft_size = 512
	self.d_burg_decim = 1
	# fcov Parameters
	self.d_fcov_order = 4
	self.d_fcov_block_len = 128
	self.d_fcov_decim = 1
	self.d_fcov_fft_size = 512
	# fmcov Parameters
	self.d_fmcov_order = 4
	self.d_fmcov_block_len = 128
	self.d_fmcov_decim = 1
	self.d_fmcov_fft_size = 512
	# MTM Parameters
	self.d_mtm_tbp = 3.0
	self.d_mtm_num_tap = 2
	self.d_mtm_weight_method = "adaptive"
	self.d_mtm_dpss_len = 512
	# Music Parameters
	self.d_music_cor_size = 32
	self.d_music_sin_cnt = 4
	self.d_music_fft_size = 512
	# Esprit Parameters
	self.d_esprit_cor_size = 32
	self.d_esprit_sin_cnt = 4
	self.d_esprit_fft_size = 512
        ###########################################################
	##                Add new estimator here!         5/8    ##
        ###########################################################

        self.main_box = dialog_box(self)

        self.samp_rate = 0
	self.fft_size = 512
	self.est_input_block_len = 512
	self.uhd_src_active = False
        self.head = None
	self.decimator = None
        self.body = None
	self.foot = None
	self.cpu_watcher = _cpu_usage_watcher_thread(self)
	self.set_head()
	self.set_decimator()
	self.set_body()
	self.set_decimator()
        self.main_box.show()

    def set_head(self):
	self.lock()
	if(self.head != None):
	    self.disconnect((self.head, 0), (self.decimator, 0))

        self.head = head(self, self.src_type, self.d_file_samp_type, self.d_file_file_to_open, self.d_file_rec_samp_rate, self.d_uhd_samp_rate, self.d_uhd_gain, self.center_f, self.d_uhd_subdev_spec)

        if(self.decimator != None and self.head != None):
	    self.connect((self.head, 0), (self.decimator, 0))
	self.main_box.first_run = 0
	self.unlock()

    def set_decimator(self):
	self.lock()
	if(self.decimator != None):
	    self.disconnect((self.head, 0), (self.decimator, 0))
	    self.disconnect((self.decimator, 0), (self.body, 0))

        self.decimator = None
        self.decimator = decimator(self.est_input_block_len, self.decimation * self.decimation_step, self.uhd_src_active, self.d_file_rec_samp_rate)

	self.connect((self.head, 0), (self.decimator, 0))
        if(self.body != None):
	    self.connect((self.decimator, 0), (self.body, 0))
	self.unlock()

    def set_body(self):
	self.lock()
	if(self.body != None and self.decimator != None and self.foot != None):
	    self.sink.watcher.quit()
	    self.disconnect((self.decimator, 0), (self.body, 0))
	    self.disconnect((self.body, 0), (self.foot, 0))
	    self.disconnect((self.foot, 0), (self.sink, 0))
	elif(self.body != None and self.decimator != None and self.foot == None):
	    self.sink.watcher.quit()
	    self.disconnect((self.decimator, 0), (self.body, 0))
	    self.disconnect((self.body, 0), (self.sink, 0))
	if(self.estimator == "Welch"):
	    if(self.d_welch_window == "Hann"):
		self.window = gr.firdes.WIN_HANN
	    elif(self.d_welch_window == "Hamming"):
		self.window = gr.firdes.WIN_HAMMING
	    elif(self.d_welch_window == "Kaiser"):
		self.window = gr.firdes.WIN_KAISER
	    elif(self.d_welch_window == "Blackman"):
		self.window = gr.firdes.WIN_BLACKMAN
	    elif(self.d_welch_window == "Blackman-Harris"):
		self.window = gr.firdes.WIN_BLACKMAN_hARRIS
	    elif(self.d_welch_window == "Rectangular"):
		self.window = gr.firdes.WIN_RECTANGULAR
	    else:
		print "Unkown window-type set for Welch!"
	    try:
	        self.body = specest.welch(self.d_welch_fft_size, self.d_welch_overlap, self.d_welch_mov_avg_len, self.shift_fft , self.window, self.d_welch_window_option)
		self.fft_size = self.d_welch_fft_size
		self.est_input_block_len = self.d_welch_fft_size
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
	elif(self.estimator == "Burg"):
	    try:
	        self.body = specest.burg(self.d_burg_block_len, self.d_burg_fft_size, self.d_burg_order, self.shift_fft, self.d_burg_decim)
		self.fft_size = self.d_burg_fft_size
		self.est_input_block_len = self.d_burg_block_len
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
	elif(self.estimator == "fcov"):
	    try:
                self.body = specest.fcov(self.d_fcov_block_len, self.d_fcov_fft_size, self.d_fcov_order, self.shift_fft, self.d_fcov_decim)
		self.fft_size = self.d_fcov_fft_size
		self.est_input_block_len = self.d_fcov_block_len
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
	elif(self.estimator == "fmcov"):
	    try:
	        self.body = specest.fmcov(self.d_fmcov_block_len, self.d_fmcov_fft_size, self.d_fmcov_order, self.shift_fft, self.d_fmcov_decim)
		self.fft_size = self.d_fmcov_fft_size
		self.est_input_block_len = self.d_fmcov_block_len
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
	elif(self.estimator == "MTM"):
	    try:
	        self.body = specest.mtm(self.d_mtm_dpss_len, self.d_mtm_tbp, self.d_mtm_num_tap, self.d_mtm_weight_method, self.shift_fft)
		self.fft_size = self.d_mtm_dpss_len
		self.est_input_block_len = self.d_mtm_dpss_len
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
	elif(self.estimator == "Music"):
	    try:
	        self.body = specest.music(self.d_music_sin_cnt, self.d_music_cor_size, self.d_music_fft_size, self.d_music_fft_size, 1)
		self.fft_size = self.d_music_fft_size
		self.est_input_block_len = self.d_music_fft_size
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
	elif(self.estimator == "Esprit"):
	    try:
	        self.body = specest.esprit(self.d_esprit_sin_cnt, self.d_esprit_cor_size, self.d_esprit_fft_size, self.d_esprit_fft_size, 1)
		self.fft_size = self.d_esprit_fft_size
		self.est_input_block_len = self.d_esprit_fft_size
	    except RuntimeError:
		print "Could not initialize Estimator (wrong settings?) !"
        ###########################################################
        ##                Add new estimator here!         6/8    ##
        ###########################################################
	else:
	    print "Unknown Estimator!"

	self.decimation = 1
        self.sink = plot_sink(gr.sizeof_float, self.fft_size, self.main_box, numpy.float32, self.samp_rate, self.center_f)

        if(self.scale == "Logarithmic"):
	    try:
	        self.foot = gr.nlog10_ff(10, self.fft_size)
	    except RuntimeError:
	        print "Wrong sink-data!"
	    self.connect((self.foot, 0), (self.sink,  0))
	elif(self.scale == "Linear"):
	    try:
	        self.foot = None
	    except RuntimeError:
	        print "Wrong sink-data!"
	else:
	    print "Wrong scale-settings!"


	if(self.body != None and self.decimator != None):	    
	    self.connect((self.decimator, 0), (self.body, 0))
	    if(self.scale == "Logarithmic"):
	        self.connect((self.body, 0), (self.foot, 0))
	    elif(self.scale == "Linear"):
		self.connect((self.body, 0), (self.sink, 0))
	    else:
		print "Wrong scale-settings!"
	    self.main_box.first_run = 0
	self.unlock()

        # Functions returning system parameters (for GUI)
    def input_selector(self):
	return self.src_type

    def method_selector(self):
	return self.estimator

    def center_frequency(self):
	return self.center_f

    def get_scale(self):
	return self.scale

    def file_rec_samp_rate(self):
	return self.d_file_rec_samp_rate

    def file_file_to_open(self):
	return self.d_file_file_to_open

    def file_samp_type(self):
	return self.d_file_samp_type

    def uhd_samp_type(self):
	return self.d_uhd_samp_type

    def uhd_gain(self):
	return self.d_uhd_gain

    def uhd_board_num(self):
	return self.d_uhd_board_num

    def uhd_samp_rate(self):
	return self.d_uhd_samp_rate

    def uhd_ant(self):
	return self.d_uhd_ant

    def uhd_subdev_spec(self):
	return self.d_uhd_subdev_spec

    def welch_mov_avg_len(self):
	return self.d_welch_mov_avg_len

    def welch_overlap(self):
	return self.d_welch_overlap

    def welch_window(self):
	return self.d_welch_window

    def welch_window_option(self):
	return self.d_welch_window_option

    def welch_fft_size(self):
	return self.d_welch_fft_size

    def burg_order(self):
	return self.d_burg_order

    def burg_block_len(self):
	return self.d_burg_block_len

    def burg_fft_size(self):
	return self.d_burg_fft_size

    def fcov_order(self):
	return self.d_fcov_order

    def fcov_block_len(self):
	return self.d_fcov_block_len

    def fcov_fft_size(self):
	return self.d_fcov_fft_size

    def fmcov_order(self):
	return self.d_fmcov_order

    def fmcov_block_len(self):
	return self.d_fmcov_block_len

    def fmcov_fft_size(self):
	return self.d_fmcov_fft_size

    def mtm_tbp(self):
	return self.d_mtm_tbp

    def mtm_num_tap(self):
	return self.d_mtm_num_tap

    def mtm_weight_method(self):
	return self.d_mtm_weight_method

    def mtm_dpss_len(self):
	return self.d_mtm_dpss_len

    def music_cor_size(self):
	return self.d_music_cor_size

    def music_sin_cnt(self):
	return self.d_music_sin_cnt

    def music_fft_size(self):
	return self.d_music_fft_size

    def esprit_cor_size(self):
	return self.d_esprit_cor_size

    def esprit_sin_cnt(self):
	return self.d_esprit_sin_cnt

    def esprit_fft_size(self):
	return self.d_esprit_fft_size

    ###########################################################
    ##                Add new estimator here!         7/8    ##
    ###########################################################

        # Functions to set system parameters (from GUI)
    def set_src_type(self, src_type):
	self.src_type = src_type
	self.set_head()
	self.sink.watcher.set_samp_rate(self.samp_rate)
	self.set_head()
	self.set_decimator()

    def set_method(self, method):
	self.estimator = method
	self.set_body()
	self.set_decimator()

    def set_decimation(self, decimation):
	self.decimation = decimation
	self.set_decimator()

    def set_samp_rate(self, samp_rate):
	self.samp_rate = samp_rate

    def set_center_f(self, center_f):
	self.center_f = center_f
	self.sink.watcher.set_center_f(self.center_f)
	self.set_head()

    def set_scale(self, scale):
	self.scale = scale
	self.set_body()

    def set_file_rec_samp_rate(self, rec_samp_rate):
	self.d_file_rec_samp_rate = rec_samp_rate
	self.set_head()
	self.sink.watcher.set_samp_rate(self.samp_rate)

    def set_file_to_open(self, file_to_open):
	self.d_file_file_to_open = file_to_open
	self.set_head()

    def set_file_samp_type(self, samp_type):
	if(samp_type == "complex"):
		self.d_file_samp_type = gr.sizeof_gr_complex
	else:
		self.d_file_samp_type = gr.sizeof_float
	self.set_head()

    def set_uhd_samp_type(self, samp_type):
	if(samp_type == "complex"):
		self.d_uhd_samp_type = gr.sizeof_gr_complex
	else:
		self.d_uhd_samp_type = gr.sizeof_float
	self.set_head()

    def set_uhd_gain(self, gain):
	self.d_uhd_gain = gain
	self.set_head()
	self.set_head()

    def set_uhd_board_num(self, board_num):
	self.d_uhd_board_num = board_num
	self.set_head()
	self.set_head()

    def set_uhd_samp_rate(self, samp_rate):
	self.d_uhd_samp_rate = samp_rate
	self.set_head()
	self.sink.watcher.set_samp_rate(self.samp_rate)
	self.set_head()

    def set_uhd_ant(self, ant):
	self.d_uhd_ant = ant
	self.set_head()
	self.set_head()

    def set_uhd_subdev_spec(self, subdev_spec):
	self.d_uhd_subdev_spec = subdev_spec
	self.set_head()
	self.set_head()

    def set_welch_mov_avg_len(self, mov_avg_len):
	self.d_welch_mov_avg_len = mov_avg_len
	self.set_body()

    def set_welch_overlap(self, overlap):
	self.d_welch_overlap = overlap
	self.set_body()

    def set_welch_window(self, window):
	self.d_welch_window = window
	self.set_body()

    def set_welch_window_option(self, window_option):
	self.d_welch_window_option = window_option
	self.set_body()

    def set_welch_fft_size(self, fft_size):
	self.d_welch_fft_size = fft_size
	self.set_body()
	self.set_decimator()

    def set_burg_order(self, order):
	self.d_burg_order = order
	self.set_body()

    def set_burg_block_len(self, block_len):
	self.d_burg_block_len = block_len
	self.set_body()
	self.set_decimator()

    def set_burg_fft_size(self, fft_size):
	self.d_burg_fft_size = fft_size
	self.set_body()
	self.set_decimator()

    def set_fcov_order(self, order):
	self.d_fcov_order = order
	self.set_body()

    def set_fcov_block_len(self, block_len):
	self.d_fcov_block_len = block_len
	self.set_body()
	self.set_decimator()

    def set_fcov_fft_size(self, fft_size):
	self.d_fcov_fft_size = fft_size
	self.set_body()
	self.set_decimator()

    def set_fmcov_order(self, order):
	self.d_fmcov_order = order
	self.set_body()

    def set_fmcov_block_len(self, block_len):
	self.d_fmcov_block_len = block_len
	self.set_body()
	self.set_decimator()

    def set_fmcov_fft_size(self, fft_size):
	self.d_fmcov_fft_size = fft_size
	self.set_body()
	self.set_decimator()

    def set_mtm_tbp(self, tbp):
	self.d_mtm_tbp = tbp
	self.set_body()

    def set_mtm_num_tap(self, num_tap):
	self.d_mtm_num_tap = num_tap
	self.set_body()

    def set_mtm_weight_method(self, weight_method):
	self.d_mtm_weight_method = weight_method
	self.set_body()

    def set_mtm_dpss_len(self, dpss_len):
	self.d_mtm_dpss_len = dpss_len
	self.set_body()
	self.set_decimator()

    def set_music_cor_size(self, cor_size):
	self.d_music_cor_size = cor_size
	self.set_body()

    def set_music_sin_cnt(self, sin_cnt):
	self.d_music_sin_cnt = sin_cnt
	self.set_body()

    def set_music_fft_size(self, fft_size):
	self.d_music_fft_size = fft_size
	self.set_body()
	self.set_decimator()

    def set_esprit_cor_size(self, cor_size):
	self.d_esprit_cor_size = cor_size
	self.set_body()

    def set_esprit_sin_cnt(self, sin_cnt):
	self.d_esprit_sin_cnt = sin_cnt
	self.set_body()

    def set_esprit_fft_size(self, fft_size):
	self.d_esprit_fft_size = fft_size
	self.set_body()
	self.set_decimator()

    ###########################################################
    ##                Add new estimator here!         8/8    ##
    ###########################################################

if __name__ == "__main__":
    tb = my_top_block();
    tb.qapp.exec_()
    tb.sink.watcher.quit()
    tb.stop()
