GR_SWIG_BLOCK_MAGIC(specest,esprit);

specest_esprit_sptr specest_make_esprit (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);

class specest_esprit : public gr_hier_block2
{
 public:
  unsigned int decimation();
	void set_decimation(unsigned int n);
 private:
	specest_esprit (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);
};
