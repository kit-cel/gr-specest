# vim: set fileencoding=utf-8 :
#
# Copyright 2009,2010,2013 Communications Engineering Lab, KIT
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
Read a file (WAV or DAT) and display a part of the content's power
spectral density using Matplotlib.
"""

import pylab
from gnuradio import gr
from gnuradio import blocks
from gnuradio import filter
import specest

from gnuradio.eng_option import eng_option
from optparse import OptionParser, OptionGroup


def parse_options():
    """ Options parser. """
    usage = "%prog: [options] filename"
    parser = OptionParser(option_class=eng_option, usage=usage)
    parser.add_option("-s", "--sample-type", type="choice", choices=("float", "complex"),
            help="For .dat-files: set input type to float or complex.", default="complex")
    parser.add_option("-v", "--verbose", action="store_true", default=False,
            help="Output some details on the estimator.")
    parser.add_option("-F", "--fft-len", type="int", default=512,
            help="FFT length")
    parser.add_option("-N", "--samples", type="int", default=None,
            help="maximum number of samples to grab from file (Will override settings for Welch)")
    parser.add_option("-S", "--shift-fft", action="store_true", default=False,
            help="shift the DC carrier to the middle.")
    parser.add_option("-l", "--linear", action="store_true", default=False,
            help="Plot output on a linear scale instead of a dB scale.")
    parser.add_option("-M", "--method", type="choice",
            choices=("welch", "welchsp", "burg", "fcov", "fmcov", "mtm", "esprit", "music"),
            help="Choose the spectral estimation method (welch, welchsp, burg, fcov, fmcov, esprit, music or mtm).",
            default="welch")
    ogroup_welch = OptionGroup(parser, 'Welch-specific options (for welch and welchsp)')
    ogroup_welch.add_option("-m", "--ma-length", type="int", default=8,
            help="length of moving average")
    ogroup_welch.add_option("-a", "--alpha", type="int", default=.1,
            help="single-pole moving average coefficient (for welchsp)")
    ogroup_welch.add_option("-o", "--overlap", type="int", default=-1,
            help="number of overlapping samples per segment, leave empty for 50% overlap.")
    ogroup_welch.add_option("-w", "--window-type", type="choice",
            choices=("rect", "hamming","hann", "blackman", "blackmanharris", "kaiser"), default="hamming",
            help="Window type")
    ogroup_welch.add_option("--window-param", type="float", default=6.76,
            help="Window parameter (for Kaiser windows)")
    parser.add_option_group(ogroup_welch)
    ogroup_burg = OptionGroup(parser, 'Parametric estimators specific options')
    ogroup_burg.add_option("-O", "--order", type="int",
            help="Choose the order of the corresponding model (Required!).")
    parser.add_option_group(ogroup_burg)
    ogroup_mtm = OptionGroup(parser, 'MTM-specific options')
    ogroup_mtm.add_option("-W", "--timebandwidthproduct", type="float", default=3,
            help="Time-Bandwidth product, usually of value 2, 2.5, 3.0, 3.5, or 4.")
    ogroup_mtm.add_option("-K", "--n-tapers", type="float", default=5,
            help="Number of tapers to use. Should be smaller than twice the time-bandwidth product.")
    ogroup_mtm.add_option("--weight-method", type="choice", choices=('unity', 'eigenvalues', 'adaptive'),
            help="Weighting method ('unity', 'eigenvalues' or 'adaptive').", default='unity')
    parser.add_option_group(ogroup_mtm)
    ogroup_music_esprit = OptionGroup(parser, 'MUSIC/ESPRIT specific options')
    ogroup_music_esprit.add_option("-C", "--correlation-size", type="int", default=64,
                                   help="Dimension of the correlation matrix to generate")
    parser.add_option_group(ogroup_music_esprit)
    (options, args) = parser.parse_args ()
    if len(args) != 1:
        parser.print_help()
        raise SystemExit, 1
    return (options, args[0])


def sanitize_input(options):
    """ Check the more complicated dependencies etc. """
    if options.samples is None:
        if options.method in ('welch', 'welchsp'):
            if options.overlap == -1:
                options.samples = (options.fft_len / 2 + 1) * options.ma_length
            else:
                options.samples = options.fft_len * options.ma_length - options.overlap * (options.ma_length - 1)
        else:
            options.samples = options.fft_len
    if options.method in ('burg', 'fcov', 'fmcov', 'esprit', 'music') \
            and options.order is None:
        print "Parametric methods require an order parameter."
        raise SystemExit, 1
    if options.method in ('burg', 'fcov', 'fmcov') and options.order < 2:
        print "AR methods require an order parameter greater or equal to 2."
        raise SystemExit, 1
    options.window_type = {
            "rect":           filter.firdes.WIN_RECTANGULAR,
            "hamming":        filter.firdes.WIN_HAMMING,
            "hann":           filter.firdes.WIN_HANN,
            "kaiser":         filter.firdes.WIN_KAISER,
            "blackman":       filter.firdes.WIN_BLACKMAN,
            "blackmanharris": filter.firdes.WIN_BLACKMAN_hARRIS}[options.window_type]
    if options.method in ('music', 'esprit') and options.correlation_size <= options.order:
        print "Correlation Size C must be bigger than the number of assumed sinusoids P"
        raise SystemExit, 1
    options.sample_size = {'complex': gr.sizeof_gr_complex,
                           'real': gr.sizeof_float}[options.sample_type]
    return options


def verbose_output_estimator(options):
    """Print verbose output about the chosen estimator."""
    print 'Estimator information:'
    print '  Estimating from a total of %d samples.' % options.samples
    print '  Output FFT size: %d' % options.fft_len
    print '  Estimator: %s' % options.method,
    if options.method in ('welch', 'welchsp', 'mtm'):
        print '[Non-Parametric]'
    else:
        print '[Parametric]'
        print '  Specified model order: %d' % options.order
    if options.method in ('welch', 'welchsp'):
        print '  Window type: %s' % (
                        'Rectangular', 'Hamming', 'Hann', 'Kaiser',
                        'Blackman', 'Blackman-Harris'
                    )[options.window_type]
        if options.window_type == 'kaiser':
            print '  Window β: %d' % options.window_param
        if options.method == 'welch':
            print '  MA filter length: %d ' % options.ma_length
        else:
            print '  Single Pole Coefficient α: %f' % options.alpha
        print '  Periodogram overlap (samples): %d' % options.overlap
    if options.method in ('esprit', 'music'):
        print '  Autocorrelation matrix size: %d x %d' % \
                (options.correlation_size,options.correlation_size)


class CalcSpecest(gr.top_block):
    """ Flow graph for calculating the spectral estimate. """
    def __init__ (self, options, filename):
        gr.top_block.__init__(self)
        self.options = options
        self.filename = filename
        self.head = blocks.head(gr.sizeof_gr_complex, options.samples)
        self.specest = None # Is defined later
        self.sink = blocks.vector_sink_f(options.fft_len)
        self.ylabelstr = ''
        if options.shift_fft:
            self.x_axis = (pylab.array(range(options.fft_len)) - round(options.fft_len/2)) / round(options.fft_len/2)
        else:
            self.x_axis = (pylab.array(range(options.fft_len))) / round(options.fft_len/2)
        self._setup_head()
        self._setup_specest()
        self._setup_foot()

    def _setup_head(self):
        """ Sets up the input of the flow graph, i.e. determine which kind of file source
        is necessary. """
        if self.filename[-4:].lower() == '.wav':
            if self.options.verbose:
                print 'Reading data from a WAV file.'
            src = blocks.wavfile_source(self.filename, True)
            f2c = blocks.float_to_complex()
            self.connect((src, 0), (f2c, 0))
            if src.channels() == 2:
                self.connect((src, 1), (f2c, 1))
            self.connect(f2c, self.head)
        else:
            if self.options.verbose:
                print 'Reading data from a raw data file.'
            src = blocks.file_source(self.options.sample_size, self.filename, True)
            if self.options.sample_size == gr.sizeof_float:
                f2c = blocks.float_to_complex()
                self.connect(src, f2c, self.head)
                if self.options.verbose:
                    print '  Input data is considered real.'
            else:
                self.connect(src, self.head)
                if self.options.verbose:
                    print '  Input data is considered complex.'

    def _setup_specest(self):
        """Select the chosen estimator and configure it, add it into the flow
        graph.
        """
        options = self.options
        specest_selector = {
            'welch': lambda: specest.welch(options.fft_len, options.overlap,
                                           options.ma_length, options.shift_fft,
                                           options.window_type, options.window_param),
            'welchsp': lambda: specest.welchsp(options.fft_len, options.overlap,
                                               options.alpha, options.shift_fft,
                                               options.window_type, options.window_param),
            'burg': lambda: specest.burg(options.samples, options.fft_len,
                                         options.order, options.shift_fft),
            'fcov': lambda: specest.fcov(options.samples, options.fft_len,
                                         options.order, options.shift_fft),
            'fmcov': lambda: specest.fmcov(options.samples, options.fft_len,
                                           options.order, options.shift_fft),
            'esprit': lambda: specest.esprit(options.order, options.correlation_size,
                                             options.samples, options.fft_len, 1),
            'music': lambda: specest.music(options.order, options.correlation_size,
                                           options.samples, options.fft_len, 1),
            'mtm': lambda: specest.mtm(options.fft_len, options.timebandwidthproduct,
                                       options.n_tapers, options.weight_method,
                                       options.shift_fft)}
        self.specest = specest_selector[options.method]()
        if self.options.verbose:
            verbose_output_estimator(options)

    def _setup_foot(self):
        """ Sets up everything after the spectral estimation. """
        if self.options.linear:
            self.connect(self.head, self.specest, self.sink)
            self.ylabelstr = 'Power Spectrum Density / W/rad'
        else:
            lin2db = blocks.nlog10_ff(10, self.options.fft_len)
            self.connect(self.head, self.specest, lin2db, self.sink)
            self.ylabelstr = 'Power Spectrum Density / dBW/rad'

    def get_data(self):
        """ Returns the spectral estimate data after this block has run. """
        return self.sink.data()[-self.options.fft_len:]


def plot_result(psd_est, x_axis, ylabelstr):
    """ Plot the PSD estimation. """
    pylab.figure()
    pylab.plot(x_axis, psd_est)
    pylab.xlabel('Normalised frequency / pi')
    pylab.ylabel(ylabelstr)
    pylab.grid()
    pylab.show()


def main():
    """ Go, go, go! """
    (options, filename) = parse_options()
    options = sanitize_input(options)
    estimator = CalcSpecest(options, filename)
    estimator.run()
    plot_result(estimator.get_data(), estimator.x_axis, estimator.ylabelstr)


if __name__ == '__main__':
    main()

