GR_SWIG_BLOCK_MAGIC(specest,stream_to_vector_overlap)

specest_stream_to_vector_overlap_sptr 
specest_make_stream_to_vector_overlap (size_t itemsize, size_t nitems_per_block, unsigned overlap)
        throw (std::invalid_argument);

class specest_stream_to_vector_overlap : public gr_sync_decimator
{
 protected:
  specest_stream_to_vector_overlap (size_t itemsize, size_t nitems_per_block, unsigned overlap);

 public:
  unsigned overlap();
};

