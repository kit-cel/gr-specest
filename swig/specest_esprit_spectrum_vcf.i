GR_SWIG_BLOCK_MAGIC(specest,esprit_spectrum_vcf);

specest_esprit_spectrum_vcf_sptr specest_make_esprit_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len);

class specest_esprit_spectrum_vcf : public gr_sync_block
{
 private:
	specest_esprit_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len);
};
