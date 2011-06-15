GR_SWIG_BLOCK_MAGIC(specest,music);

specest_music_sptr specest_make_music (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);

class specest_music : public gr_hier_block2
{
 public:
  unsigned int decimation();
	void set_decimation(unsigned int n);
 private:
	specest_music (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);
};
