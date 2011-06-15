from gnuradio import gr, gr_unittest
import numpy
import os

class signal_generator(gr.hier_block2):
    """
    This class is meant to be used as a signal generator for
    ESPRIT / MUSICs unittests.

    @param n_sinusoids: Number of complex sinusoids
    @type n_sinusoids: number
    @param SNR: Signal to Noise Ratio in dB. 
                Please note that in this case SNR describes the ratio between 
                the sum of the energies of the sinusoids and the noise.
    @type SNR: float
    @param samp_rate : Sampling Rate for the sources
    @type samp_rate: number
    @param nsamples: Number of samples that will be generated before the block stops
    @type nsamples: number
    """
    def __init__(self, n_sinusoids = 1, SNR = 10, samp_rate = 32e3, nsamples = 2048):
        gr.hier_block2.__init__(self, "ESPRIT/MUSIC signal generator",
                                gr.io_signature(0, 0, gr.sizeof_float),
                                gr.io_signature(1, 1, gr.sizeof_gr_complex))
        sigampl = 10.0**(SNR/10.0) # noise power is 1
        self.srcs = list()

        self.n_sinusoids = n_sinusoids
        self.samp_rate = samp_rate
        # create our signals ...
        for s in range(n_sinusoids):
            self.srcs.append(gr.sig_source_c(samp_rate,
                gr.GR_SIN_WAVE,1000 * s + 2000,
                numpy.sqrt(sigampl/n_sinusoids)))

        seed = ord(os.urandom(1))
        self.noise = gr.noise_source_c(gr.GR_GAUSSIAN, 1, seed)
        self.add = gr.add_cc()
        self.head = gr.head(gr.sizeof_gr_complex, nsamples)
        self.sink = gr.vector_sink_f(vlen=n_sinusoids)
        # wire it up ... 
        for s in range(n_sinusoids):
            self.connect(self.srcs[s], (self.add, s))
        # Additive noise
        self.connect(self.noise, (self.add, n_sinusoids))
        self.connect(self.add, self.head, self)

    def omegas(self):
        """
        Returns a sorted list of the frequencies generated in the range [-pi:pi]
        """
        omegas = list()
        for s in self.srcs:
            omegas.append(s.frequency() / (0.5*self.samp_rate) * numpy.pi)
        return sorted(omegas)
