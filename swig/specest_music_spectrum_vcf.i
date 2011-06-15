GR_SWIG_BLOCK_MAGIC(specest,music_spectrum_vcf);

specest_music_spectrum_vcf_sptr specest_make_music_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len);

class specest_music_spectrum_vcf : public gr_sync_block
{
 private:
	specest_music_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len);
};
