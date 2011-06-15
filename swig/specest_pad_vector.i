GR_SWIG_BLOCK_MAGIC(specest,pad_vector)

specest_pad_vector_sptr specest_make_pad_vector (size_t item_size, unsigned vlen_in, unsigned vlen_out);

class specest_pad_vector : public gr_sync_block
{
	specest_pad_vector (size_t item_size, unsigned vlen_in, unsigned vlen_out);
};

