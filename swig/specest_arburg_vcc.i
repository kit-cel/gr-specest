GR_SWIG_BLOCK_MAGIC(specest,arburg_vcc)

specest_arburg_vcc_sptr
specest_make_arburg_vcc (unsigned block_len, unsigned order, int normalise = -1);

class specest_arburg_vcc : public gr_sync_block
{
 protected:
	specest_arburg_vcc (unsigned block_len, unsigned order, int normalise);
};

