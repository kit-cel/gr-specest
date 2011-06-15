GR_SWIG_BLOCK_MAGIC(specest,esprit_vcf);

specest_esprit_vcf_sptr specest_make_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples);

class specest_esprit_vcf : public gr_sync_block
{
 private:
	specest_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples);
};
