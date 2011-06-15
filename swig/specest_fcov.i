GR_SWIG_BLOCK_MAGIC(specest,fcov);

specest_fcov_sptr
specest_make_fcov(unsigned blocklen, unsigned int fft_len, unsigned int order, bool fftshift=false, int decimation=1)
	throw(std::invalid_argument);

class specest_fcov : public gr_hier_block2
{
 private:
	specest_fcov(unsigned blocklen, unsigned int fft_len, unsigned int order, bool fftshift, int decimation);
};

