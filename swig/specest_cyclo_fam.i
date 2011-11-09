GR_SWIG_BLOCK_MAGIC(specest,cyclo_fam);

specest_cyclo_fam_sptr
specest_make_cyclo_fam (int Np, int P, int decimation_factor)
        throw(std::invalid_argument);

class specest_cyclo_fam : public gr_hier_block2
{
 public:
 const float* get_estimate();
 
 private:
	specest_cyclo_fam (int Np, int P, int decimation_factor);

};
