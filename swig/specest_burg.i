GR_SWIG_BLOCK_MAGIC(specest,burg);

specest_burg_sptr
specest_make_burg(unsigned blocklen, unsigned int fft_len, unsigned int order, bool fftshift=false, int decimation=1)
	throw(std::invalid_argument);

class specest_burg : public gr_hier_block2
{
 private:
	specest_burg(unsigned blocklen, unsigned int fft_len, unsigned int order, bool fftshift, int decimation);
};

