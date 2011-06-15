GR_SWIG_BLOCK_MAGIC(specest,moving_average_vff);

specest_moving_average_vff_sptr specest_make_moving_average_vff (int length, int vlen, float scale, int max_iter=4096);

class specest_moving_average_vff : public gr_sync_block
{
private:
  specest_moving_average_vff ();
};

