#!/usr/bin/env python
"""
A GUI front-end for the estimators in the GNU Radio Spectral Estimation Toolbox.
"""

import sys
import time
import numpy
import pylab
from PyQt4 import QtGui, QtCore
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt
from gnuradio import gr, uhd, filter, blocks
import specest

try:
    from specest_window import Ui_MainWindow
except ImportError:
    print "Error: could not find specest_window.py:"
    print "\t\"Please run: pyuic4 specest_window.ui -o specest_window.py\""
    sys.exit(1)

### Global definitions #######################################################
FFT_SIZE_INDEX = {16: 0, 32: 1, 64: 2, 128: 3, 256: 4, 512: 5, 1024: 6,
                  2048: 7, 4096: 8, 8192: 9, 16384:10,
                  32768:11, 65536:12}

WINDOW_INDEX = {'Hann': 0, 'Hamming': 1, 'Kaiser': 2, 'Blackman': 3,
                'Blackman-Harris': 4, 'Rectangular': 5}
WIN_TYPE_IDX = {'Hann': filter.firdes.WIN_HANN,
                'Hamming': filter.firdes.WIN_HAMMING,
                'Kaiser': filter.firdes.WIN_KAISER,
                'Blackman': filter.firdes.WIN_BLACKMAN,
                'Blackman-Harris': filter.firdes.WIN_BLACKMAN_hARRIS,
                'Rectangular': filter.firdes.WIN_RECTANGULAR}
ESTIM_TAB_NAMES = {'Welch': 0, 'Welch (SP)': 1, 'Burg': 2, 'fcov': 3, 'fmcov': 4, 'MTM': 5, 'Music': 6, 'Esprit': 7}
### Estimator Definitions ####################################################
class EstimatorBase(object):
    """ Derive any estimator bindings from this class. """
    def __init__(self):
        self.fg = None
        self.gui = None
        self.block = None

    def connect_fg(self, fg):
        " Don't call this yourself! "
        self.fg = fg

    def connect_gui(self, gui):
        " Don't call this yourself! "
        self.gui = gui
        self.setup_gui(gui.gui)
        self.connect_control_signals(gui)

    def setup_gui(self, gui):
        " Overload this to set the values in the fields of the GUI. "
        pass

    def connect_control_signals(self, gui):
        " Overload this to connect Qt control signals to setters. "
        pass

    def setup_block(self, fg):
        """Overload this to configure the actual estimator block.
        Must return a tuple (input block size, output block size)
        """
        pass


class EstimatorWelch(EstimatorBase):
    """ Bindings for the Welch spectral estimator. """
    def __init__(self):
        EstimatorBase.__init__(self)
        self.mov_avg_len = 8
        self.overlap = -1
        self.window = "Hamming"
        self.window_option = 0.00
        self.fft_size = 512

    def setup_gui(self, gui):
        gui.welch_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])
        gui.welch_mov_avg.setValue(self.mov_avg_len)
        gui.welch_overlap.setValue(self.overlap)
        gui.welch_window.setCurrentIndex(WINDOW_INDEX[self.window])
        gui.welch_window_option.setValue(self.window_option)

    def connect_control_signals(self, gui):
        gui.connect(gui.gui.welch_mov_avg, QtCore.SIGNAL("editingFinished()"),
                    self._set_ma_len)
        gui.connect(gui.gui.welch_overlap, QtCore.SIGNAL("valueChanged()"),
                    self._set_overlap)
        gui.connect(gui.gui.welch_window, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_window)
        gui.connect(gui.gui.welch_window_option, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_window_option)
        gui.connect(gui.gui.welch_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)

    def _set_ma_len(self):
        self.mov_avg_len = self.gui.gui.welch_mov_avg.text().toLong()[0]
        self.fg.set_body()

    def _set_overlap(self):
        self.overlap = self.gui.gui.welch_overlap.text().toLong()[0]
        self.fg.set_body()

    def _set_window(self):
        self.window = str(self.gui.gui.welch_window.currentText())
        self.fg.set_body()

    def _set_window_option(self):
        self.window_option = self.gui.gui.welch_window_option.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        try:
            window = WIN_TYPE_IDX[self.window]
        except KeyError:
            print "Unkown window-type set for Welch!"
        self.block = specest.welch(self.fft_size, self.overlap,
                                   self.mov_avg_len, shift_fft,
                                   window, self.window_option)
        return (self.fft_size, self.fft_size)


class EstimatorWelchSP(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.alpha = 0.1
        self.overlap = 0
        self.window = "Hamming"
        self.window_option = 0.00
        self.fft_size = 512

    def setup_gui(self, gui):
        gui.welchsp_alpha.setValue(self.alpha)
        gui.welchsp_overlap.setValue(self.overlap)
        gui.welchsp_window.setCurrentIndex(WINDOW_INDEX[self.window])
        gui.welchsp_window_option.setValue(self.window_option)
        gui.welchsp_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.welchsp_alpha, QtCore.SIGNAL("editingFinished()"),
                    self._set_alpha)
        gui.connect(gui.gui.welchsp_overlap, QtCore.SIGNAL("valueChanged()"),
                    self._set_overlap)
        gui.connect(gui.gui.welchsp_window, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_window)
        gui.connect(gui.gui.welchsp_window_option, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_window_option)
        gui.connect(gui.gui.welchsp_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)

    def _set_alpha(self):
        self.alpha = self.gui.gui.welchsp_alpha.text().toDouble()[0]
        self.fg.set_body()

    def _set_overlap(self):
        self.overlap = self.gui.gui.welchsp_overlap.text().toLong()[0]
        self.fg.set_body()

    def _set_window(self):
        self.window = str(self.gui.gui.welchsp_window.currentText())
        self.fg.set_body()

    def _set_window_option(self):
        self.window_option = self.gui.gui.welchsp_window_option.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()


    def setup_block(self, shift_fft):
        try:
            window = WIN_TYPE_IDX[self.window]
        except KeyError:
            print "Unknown window-type set for Welch!"
        self.block = specest.welchsp(self.fft_size, self.overlap,
                                   self.alpha, shift_fft,
                                   window, self.window_option)
        return (self.fft_size, self.fft_size)

class EstimatorBurg(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.order = 4
        self.block_len = 128
        self.fft_size = 512
        self.decim = 1

    def setup_gui(self, gui):
        gui.burg_order.setValue(self.order)
        gui.burg_block_len.setValue(self.block_len)
        gui.burg_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.burg_order, QtCore.SIGNAL("editingFinished()"),
                    self._set_order)
        gui.connect(gui.gui.burg_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)
        gui.connect(gui.gui.burg_block_len, QtCore.SIGNAL("editingFinished()"),
                    self._set_block_len)

    def _set_order(self):
        self.order = self.gui.gui.burg_order.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()

    def _set_block_len(self):
        self.block_len = self.gui.gui.burg_block_len.text().toLong()[0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        self.block = specest.burg(self.block_len, self.fft_size,
                                  self.order, shift_fft, self.decim)
        return (self.block_len, self.fft_size)

class EstimatorFcov(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.order = 4
        self.block_len = 128
        self.decim = 1
        self.fft_size = 512

    def setup_gui(self, gui):
        gui.fcov_order.setValue(self.order)
        gui.fcov_block_len.setValue(self.block_len)
        gui.fcov_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.fcov_order, QtCore.SIGNAL("editingFinished()"),
                    self._set_order)
        gui.connect(gui.gui.fcov_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)
        gui.connect(gui.gui.fcov_block_len, QtCore.SIGNAL("editingFinished()"),
                    self._set_block_len)

    def _set_order(self):
        self.order = self.gui.gui.burg_order.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()

    def _set_block_len(self):
        self.block_len = self.gui.gui.burg_block_len.text().toLong()[0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        self.block = specest.fcov(self.block_len, self.fft_size,
                                  self.order, shift_fft, self.decim)
        return (self.block_len, self.fft_size)


class EstimatorFmcov(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.order = 4
        self.block_len = 128
        self.decim = 1
        self.fft_size = 512

    def setup_gui(self, gui):
        gui.fmcov_order.setValue(self.order)
        gui.fmcov_block_len.setValue(self.block_len)
        gui.fmcov_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.fmcov_order, QtCore.SIGNAL("editingFinished()"),
                    self._set_order)
        gui.connect(gui.gui.fmcov_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)
        gui.connect(gui.gui.fmcov_block_len, QtCore.SIGNAL("editingFinished()"),
                    self._set_block_len)

    def _set_order(self):
        self.order = self.gui.gui.burg_order.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()

    def _set_block_len(self):
        self.block_len = self.gui.gui.burg_block_len.text().toLong()[0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        self.block = specest.fmcov(self.block_len, self.fft_size,
                                   self.order, shift_fft, self.decim)
        return (self.block_len, self.fft_size)


class EstimatorMTM(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.tbp = 3.0
        self.num_tap = 2
        self.weight_method = 'adaptive'
        self.dpss_len = 512

    def setup_gui(self, gui):
        gui.mtm_tbp.setValue(self.tbp)
        gui.mtm_num_tap.setValue(self.num_tap)
        gui.mtm_dpss_len.setCurrentIndex(FFT_SIZE_INDEX[self.dpss_len])
        method_idx = {'unity': 0, 'eigenvalues': 1, 'adaptive': 2}
        gui.mtm_weight_method.setCurrentIndex(method_idx[self.weight_method])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.mtm_tbp, QtCore.SIGNAL("editingFinished()"),
                    self._set_tbp)
        gui.connect(gui.gui.mtm_num_tap, QtCore.SIGNAL("editingFinished()"),
                    self._set_num_tap)
        gui.connect(gui.gui.mtm_weight_method, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_weight_method)
        gui.connect(gui.gui.mtm_dpss_len, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_dpss_len)

    def _set_tbp(self):
        self.tbp = self.gui.gui.mtm_tbp.text().toDouble()[0]
        self.fg.set_body()

    def _set_num_tap(self):
        self.num_tap = self.gui.gui.mtm_num_tap.text().toLong()[0]
        self.fg.set_body()

    def _set_weight_method(self):
        self.weight_method = str(self.gui.gui.mtm_weight_method.currentText())
        self.fg.set_body()

    def _set_dpss_len(self):
        self.dpss_len = self.gui.gui.mtm_dpss_len.text().toLong()[0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        self.block = specest.mtm(self.dpss_len, self.tbp,
                                 self.num_tap, self.weight_method,
                                 shift_fft)
        return (self.dpss_len, self.dpss_len)


class EstimatorMUSIC(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.cor_size = 32
        self.sin_cnt = 4
        self.fft_size = 512

    def setup_gui(self, gui):
        gui.music_cor_size.setValue(self.cor_size)
        gui.music_sin_cnt.setValue(self.sin_cnt)
        gui.music_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.music_cor_size, QtCore.SIGNAL("editingFinished()"),
                    self._set_cor_size)
        gui.connect(gui.gui.music_sin_cnt, QtCore.SIGNAL("editingFinished()"),
                    self._set_sin_cnt)
        gui.connect(gui.gui.music_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)

    def _set_cor_size(self):
        self.cor_size = self.gui.gui.music_cor_size.text().toLong()[0]
        self.fg.set_body()

    def _set_sin_cnt(self):
        self.sin_cnt = self.gui.gui.music_sin_cnt.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        # FIXME 2x fft_size?
        self.block = specest.music(self.sin_cnt, self.cor_size,
                                   self.fft_size, self.fft_size, 1)
        return (self.fft_size, self.fft_size)


class EstimatorESPRIT(EstimatorBase):
    def __init__(self):
        EstimatorBase.__init__(self)
        self.cor_size = 32
        self.sin_cnt = 4
        self.fft_size = 512

    def setup_gui(self, gui):
        gui.esprit_cor_size.setValue(self.cor_size)
        gui.esprit_sin_cnt.setValue(self.sin_cnt)
        gui.esprit_fft_size.setCurrentIndex(FFT_SIZE_INDEX[self.fft_size])

    def connect_control_signals(self, gui):
        """ Connect Qt control signals to setters """
        gui.connect(gui.gui.esprit_cor_size, QtCore.SIGNAL("editingFinished()"),
                    self._set_cor_size)
        gui.connect(gui.gui.esprit_sin_cnt, QtCore.SIGNAL("editingFinished()"),
                    self._set_sin_cnt)
        gui.connect(gui.gui.esprit_fft_size, QtCore.SIGNAL("currentIndexChanged(int)"),
                    self._set_fft_size)

    def _set_cor_size(self):
        self.cor_size = self.gui.gui.esprit_cor_size.text().toLong()[0]
        self.fg.set_body()

    def _set_sin_cnt(self):
        self.sin_cnt = self.gui.gui.esprit_sin_cnt.text().toLong()[0]
        self.fg.set_body()

    def _set_fft_size(self, fft_idx):
        self.fft_size = [k for k, v in FFT_SIZE_INDEX.iteritems() if v == fft_idx][0]
        self.fg.set_body()
        self.fg.set_decimator()

    def setup_block(self, shift_fft):
        # FIXME 2x fft_size?
        self.block = specest.esprit(self.sin_cnt, self.cor_size,
                                    self.fft_size, self.fft_size, 1)
        return (self.fft_size, self.fft_size)

# Define the estimators! (*Trumpets*)
estimators = {'Welch': EstimatorWelch(),
              'Welch (SP)':  EstimatorWelchSP(),
              'Burg':  EstimatorBurg(),
              'fcov':  EstimatorFcov(),
              'fmcov': EstimatorFmcov(),
              'MTM':   EstimatorMTM(),
              'Music': EstimatorMUSIC(),
              'Esprit': EstimatorESPRIT()
            }

### GUI Stuff ################################################################
class SpecEstGUI(QtGui.QMainWindow):
    """ All of this controls the actual GUI. """
    def __init__(self, fg, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        self.fg = fg
        self.first_run = 0

        # Set up plot
        self.gui.plot.setTitle("Spectrum Estimate")
        self.gui.plot.setAxisTitle(Qwt.QwtPlot.xBottom, "Frequency (MHz)")
        self.gui.plot.setAxisTitle(Qwt.QwtPlot.yLeft, "Spectral Power Density (dB)")
        # Grid
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

        # Connect control signals
        self.connect(self.gui.pause_button, QtCore.SIGNAL("clicked()"),
                                 self.pause_flow_graph)
        self.connect(self.gui.run_button, QtCore.SIGNAL("clicked()"),
                                 self.run_flow_graph)
        self.connect(self.gui.close_button, QtCore.SIGNAL("clicked()"),
                                 self.stop_flow_graph)
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
        for estimator_name in estimators:
            estimators[estimator_name].connect_gui(self)
        self.__initTracking()
        self.__initZooming()

    def plot_data(self, data_x, data_y, rescale_at_sample_num):
        """ Update the plot. """
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

    def pause_flow_graph(self):
        """ Pause and unpause the flow graph. """
        if(self.gui.pause_button.text() == "Pause"):
            self.fg.stop()
            self.fg.wait()
            self.gui.pause_button.setText("Unpause")
        else:
            self.fg.start()
            self.gui.pause_button.setText("Pause")

    def run_flow_graph(self):
        """ Init and start the flow graph. """
        self.fg.cpu_watcher = CPUUsageWatcherThread(self)
        self.fg.set_head()
        self.fg.set_decimator()
        self.fg.set_body()
        self.fg.set_decimator()
        self.fg.start()

    def stop_flow_graph(self):
        self.fg.stop()

    # Functions to manipulate parameters in GUI
    def set_input_selector(self, src_type):
        self.gui.input_selector.setCurrentIndex({'File': 0, 'UHD': 1}[src_type])

    def set_input_tab(self, src_type):
        self.gui.tabWidget_2.setCurrentIndex({'File': 0, 'UHD': 1}[src_type])

    def set_method_selector(self, method):
        method_idx = {'Welch': 0, 'Burg': 1, 'fcov': 2, 'fmcov': 3, 'MTM': 4, 'Music': 5, 'Esprit': 6}
        self.gui.method_selector.setCurrentIndex(method_idx[method])

    def set_method_tab(self, method):
        self.gui.tabWidget.setCurrentIndex(ESTIM_TAB_NAMES[method])

    def set_center_f(self, center_f):
        self.gui.center_f.setValue(center_f)

    def set_scale(self, scale):
        self.gui.scale.setCurrentIndex({'Logarithmic': 0, 'Linear': 1}[scale])

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

    # Functions to change parameters in flowgraph
    def input_selector_text(self):
        try:
            src_type = str(self.gui.input_selector.currentText())
            self.fg.set_src_type(src_type)
            self.set_input_tab(src_type)
        except RuntimeError:
            pass

    def input_tab_text(self, tab):
        # FIXME Add code to execute, when input-tab changes!
        pass

    def method_selector_text(self):
        try:
            method = str(self.gui.method_selector.currentText())
            self.fg.set_method(method)
            self.set_method_tab(method)
        except RuntimeError:
            pass

    def method_tab_text(self, tab):
        # FIXME Add code to execute, when method-tab changes!
        pass

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
    """ Event tracking. """
    def __init__(self, parent):
        Qt.QObject.__init__(self, parent)
        parent.setMouseTracking(True)
        parent.installEventFilter(self)

    def eventFilter(self, _, event):
        if event.type() == Qt.QEvent.MouseMove:
            self.emit(Qt.SIGNAL("MouseMove"), event.pos())
        return False

### Threads ##################################################################
class QueueWatcherThread(QtCore.QThread):
    """Watches over the message queue and dumps data into the plot if enough
    new samples have arrived. """
    def __init__(self, msgq, d_len, d_type_numpy, samp_rate, center_f):
        QtCore.QThread.__init__(self)
        self.msgq = msgq
        self.keep_running = True
        self.d_type_numpy = d_type_numpy
        self.d_len = d_len
        self.samp_rate = samp_rate
        self.center_f = center_f
        self.start()
        self.x_values = (pylab.array(range(-(self.d_len / 2), (self.d_len / 2)))) * \
                        self.samp_rate / 2 / round(self.d_len/2) / 1e6 + self.center_f

    def run(self):
        while self.keep_running:
            msg = self.msgq.delete_head()
            samples = numpy.fromstring(msg.to_string(), self.d_type_numpy)[:self.d_len]
            self.emit(Qt.SIGNAL("new_plot_data(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"),
                      self.x_values, samples, 13)

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.x_values = (pylab.array(range(-(self.d_len / 2), (self.d_len / 2)))) * \
                        self.samp_rate / 2 / round(self.d_len/2) / 1e6 + self.center_f

    def set_center_f(self, center_f):
        self.center_f = center_f
        self.x_values = (pylab.array(range(-(self.d_len / 2), (self.d_len / 2)))) * \
                        self.samp_rate / 2 / round(self.d_len/2) / 1e6 + self.center_f

class CPUUsageWatcherThread(QtCore.QThread):
    """ Permanently observe the CPU load. """
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
            if cpu_load is not None:
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

### GNU Radio flow graph and blocks ##########################################
class TopBlock(gr.top_block):
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
        self.d_file_file_to_open = "%s/share/gr-specest/4cos.dat" % gr.prefix()
        self.d_file_samp_type = gr.sizeof_gr_complex
        # UHD Source Parameters
        self.d_uhd_samp_type = gr.sizeof_gr_complex
        self.d_uhd_gain = 30
        self.d_uhd_ant = "Rx"
        self.d_uhd_subdev_spec = "B:0"
        self.d_uhd_board_num = 0
        self.d_uhd_samp_rate = 0.5e6

        self.main_box = SpecEstGUI(self)

        self.samp_rate = 0
        self.fft_size = 512
        self.est_input_block_len = 512
        self.uhd_src_active = False
        self.head = None
        self.decimator = None
        self.body = None
        self.foot = None
        self.sink = None
        self.cpu_watcher = None
        self.main_box.show()

        for estimator_name in estimators:
            estimators[estimator_name].connect_fg(self)
        self.set_head()
        self.set_body()
        self.set_decimator()


    def set_head(self):
        self.lock()
        if(self.head is not None and self.decimator is not None):
            self.disconnect((self.head, 0), (self.decimator, 0))
        self.head = head(self, self.src_type, self.d_file_samp_type,
                         self.d_file_file_to_open, self.d_file_rec_samp_rate,
                         self.d_uhd_samp_rate, self.d_uhd_gain, self.center_f,
                         self.d_uhd_subdev_spec)
        if(self.decimator is not None and self.head is not None):
            self.connect((self.head, 0), (self.decimator, 0))
        self.main_box.first_run = 0
        self.unlock()

    def set_decimator(self):
        self.lock()
        if(self.decimator is not None):
            self.disconnect((self.head, 0), (self.decimator, 0))
            self.disconnect((self.decimator, 0), (self.body, 0))
        self.decimator = None
        self.decimator = decimator(self.est_input_block_len,
                                   self.decimation * self.decimation_step,
                                   self.uhd_src_active, self.d_file_rec_samp_rate)
        self.connect((self.head, 0), (self.decimator, 0))
        if(self.body is not None):
            self.connect((self.decimator, 0), (self.body, 0))
        self.unlock()

    def set_body(self):
        """
        1) Disconnect old stuff, if necessary.
        2) Set up the new block.
        3) Connect everything.
        """
        self.lock()
        if(self.body is not None and self.decimator is not None and self.foot is not None):
            self.sink.watcher.quit()
            self.disconnect((self.decimator, 0), (self.body, 0))
            self.disconnect((self.body, 0), (self.foot, 0))
            self.disconnect((self.foot, 0), (self.sink, 0))
        elif(self.body is not None and self.decimator is not None and self.foot is None):
            self.sink.watcher.quit()
            self.disconnect((self.decimator, 0), (self.body, 0))
            self.disconnect((self.body, 0), (self.sink, 0))

        try:
            (self.est_input_block_len,
             self.fft_size) = estimators[self.estimator].setup_block(self.shift_fft)
        except KeyError:
            print "Unknown estimator selected."
        except RuntimeError:
            print "Could not initialize Estimator (wrong settings?) !"
        self.body = estimators[self.estimator].block

        self.decimation = 1
        self.sink = plot_sink(gr.sizeof_float, self.fft_size, self.main_box,
                              numpy.float32, self.samp_rate, self.center_f)
        if(self.scale == "Logarithmic"):
            try:
                self.foot = blocks.nlog10_ff(10, self.fft_size)
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

        if(self.body is not None and self.decimator is not None):
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

    # Functions to set system parameters (from GUI)
    def set_src_type(self, src_type):
        self.src_type = src_type
        self.set_head()
        if self.sink is not None:
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
        if self.sink is not None:
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
        if self.sink is not None:
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


class head(gr.hier_block2):
    """ Generic source block, depending on whether the user chose UHD or file. """
    def __init__(self, fg, src_type, file_samp_type, file_to_open, file_rec_samp_rate,
                 uhd_samp_rate, uhd_gain, center_f, uhd_subdev_spec):
        gr.hier_block2.__init__(self, "head",
                                gr.io_signature(0, 0, 0),
                                gr.io_signature(1, 1, gr.sizeof_gr_complex))

        if(src_type == "File"):
            try:
                self.head_src = blocks.file_source(file_samp_type, file_to_open, True)
                fg.set_samp_rate(file_rec_samp_rate)
                fg.uhd_src_active = False
                if fg.cpu_watcher is not None:
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
                self.head_src = uhd.single_usrp_source(device_addr='',
                                                       io_type=uhd.io_type_t.COMPLEX_FLOAT32, num_channels=1)
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

class decimator(gr.hier_block2):
    def __init__(self, block_len, n, uhd_src_active, file_rec_samp_rate):
        gr.hier_block2.__init__(self, "decimator",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(1, 1, gr.sizeof_gr_complex))

        if(uhd_src_active == True):
            self.stv = blocks.stream_to_vector(gr.sizeof_gr_complex, block_len)
            self.decim = blocks.keep_one_in_n(block_len * gr.sizeof_gr_complex, n)
            self. vts = blocks.vector_to_stream(gr.sizeof_gr_complex, block_len)

            self.connect(self, self.stv)
            self.connect(self.stv, self.decim)
            self.connect(self.decim, self.vts)
            self.connect(self.vts, self)

        else:
            self.throttle = blocks.throttle(gr.sizeof_gr_complex, file_rec_samp_rate)
            self.connect(self, self.throttle)
            self.connect(self.throttle, self)


class plot_sink(gr.hier_block2):
    def __init__(self, d_type, d_len, qt_box, d_type_numpy, samp_rate, center_f):
        gr.hier_block2.__init__(self, "plot_sink",
                gr.io_signature(1, 1, d_type * d_len),
                gr.io_signature(0, 0, 0))
        self.msgq = gr.msg_queue(1)
        self.snk = blocks.message_sink(d_type * d_len, self.msgq, True)
        self.connect(self, self.snk)
        self.watcher = QueueWatcherThread(self.msgq, d_len, d_type_numpy, samp_rate, center_f)
        qt_box.connect(self.watcher,
                       Qt.SIGNAL("new_plot_data(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"),
                       qt_box.plot_data)

if __name__ == "__main__":
    tb = TopBlock()
    tb.qapp.exec_()
    if tb.sink is not None:
        tb.sink.watcher.quit()
    tb.stop()

