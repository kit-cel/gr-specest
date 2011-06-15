GR_SWIG_BLOCK_MAGIC(specest,fmcov);

specest_fmcov_sptr
specest_make_fmcov(unsigned blocklen, unsigned int fft_len, unsigned int order, bool fftshift=false, int decimation=1)
	throw(std::invalid_argument);

class specest_fmcov : public gr_hier_block2
{
 private:
	specest_fmcov(unsigned blocklen, unsigned int fft_len, unsigned int order, bool fftshift, int decimation);
};

