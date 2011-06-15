GR_SWIG_BLOCK_MAGIC(specest,arfmcov_vcc)

specest_arfmcov_vcc_sptr
specest_make_arfmcov_vcc (unsigned block_len, unsigned order, int normalise = -1)
	throw(std::invalid_argument);

class specest_arfmcov_vcc : public gr_sync_block
{
 protected:
	specest_arfmcov_vcc (unsigned block_len, unsigned order, int normalise);
};

