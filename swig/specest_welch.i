GR_SWIG_BLOCK_MAGIC(specest,welch);

specest_welch_sptr
specest_make_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window)
        throw(std::invalid_argument);

specest_welch_sptr
specest_make_welch(unsigned fft_len, int overlap = -1, int ma_len = 8, bool fft_shift = false,
		int window_type = 0, double beta = 6.76) // wintype 0 is Hamming
        throw(std::invalid_argument);

class specest_welch : public gr_hier_block2
{
 private:
	specest_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window);
	specest_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift, int window_type, double beta);

 public:
	bool set_window(const std::vector<float> &window);
	bool set_hamming();
};

