GR_SWIG_BLOCK_MAGIC(specest,arfcov_vcc)

specest_arfcov_vcc_sptr
specest_make_arfcov_vcc (unsigned block_len, unsigned order, int normalise = -1);

class specest_arfcov_vcc : public gr_sync_block
{
 protected:
	specest_arfcov_vcc (unsigned block_len, unsigned order, int normalise);
};

