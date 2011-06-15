GR_SWIG_BLOCK_MAGIC(specest,music_vcf);

specest_music_vcf_sptr specest_make_music_vcf (unsigned int n, unsigned int m, unsigned int nsamples);

class specest_music_vcf : public gr_sync_block
{
 private:
	specest_music_vcf (unsigned int n, unsigned int m, unsigned int nsamples);
};
