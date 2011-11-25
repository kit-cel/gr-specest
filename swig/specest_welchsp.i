GR_SWIG_BLOCK_MAGIC(specest,welchsp);

specest_welchsp_sptr
specest_make_welchsp(unsigned fft_len, int overlap, double alpha, bool fft_shift, const std::vector<float> &window)
        throw(std::invalid_argument);

specest_welchsp_sptr
specest_make_welchsp(unsigned fft_len, int overlap = -1, double alpha = .1, bool fft_shift = false,
		int window_type = 0, double beta = 6.76) // wintype 0 is Hamming
        throw(std::invalid_argument);

class specest_welchsp : public gr_hier_block2
{
 private:
	specest_welchsp(unsigned fft_len, int overlap, double alpha, const std::vector<float> &window);
	specest_welchsp(unsigned fft_len, int overlap, double alpha, bool fft_shift, int window_type, double beta);

 public:
	bool set_window(const std::vector<float> &window);
	bool set_hamming();
};

