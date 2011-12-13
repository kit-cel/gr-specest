GR_SWIG_BLOCK_MAGIC(specest,cyclo_fam);

specest_cyclo_fam_sptr
specest_make_cyclo_fam (int Np, int P, int decimation_factor)
        throw(std::invalid_argument);

class specest_cyclo_fam : public gr_hier_block2
{
 public:
 const std::vector<std::vector<float> > &get_estimate();
 
 int get_Np();
 int get_N();
 int get_P();
 int get_L(); 
 
 private:
	specest_cyclo_fam (int Np, int P, int decimation_factor);

};
