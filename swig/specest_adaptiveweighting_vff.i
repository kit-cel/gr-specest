GR_SWIG_BLOCK_MAGIC(specest,adaptiveweighting_vff);

specest_adaptiveweighting_vff_sptr specest_make_adaptiveweighting_vff (size_t vlen, const std::vector<float> k);

class specest_adaptiveweighting_vff : public gr_sync_block
{
private:
  specest_adaptiveweighting_vff (size_t vlen,const std::vector<float> k);
};
