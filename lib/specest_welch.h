/* -*- c++ -*- */
/*
 * Copyright 2009 Institut fuer Nachrichtentechnik / Uni Karlsruhe
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_SPECEST_WELCH_H
#define INCLUDED_SPECEST_WELCH_H

#include <gr_hier_block2.h>
#include <gr_fft_vcc.h>
#include <gr_complex_to_xxx.h>
#include <gr_firdes.h>
#include <specest_stream_to_vector_overlap.h>
#include <specest_moving_average_vff.h>

class specest_welch;
typedef boost::shared_ptr<specest_welch> specest_welch_sptr;

/*
 * \brief Create a Welch spectrum estimator with user defined window
 */
specest_welch_sptr
specest_make_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window);

/*
 * \brief Create a Welch spectrum estimator using internal window functions.
 */
specest_welch_sptr
specest_make_welch(unsigned fft_len, int overlap = -1, int ma_len = 8, bool fft_shift = false,
		int window_type = (int) gr_firdes::WIN_HAMMING, double beta = 6.76);
// Declaring int instead of win_type makes it compatible with Python

/**
 * \brief Estimate spectral density Sxx(w) using Welch's method.
 *
 * The estimator works on complex input signals. If \p overlap is left unspecified or -1, a
 * 50% overlap is calculated. The standard window is a Hamming window, but can be changed to
 * be anything else. The output is vector containing the moving average of the last \p ma_len
 * overlapping, windowed periodograms signal segments. The first element is Sxx(0), then goes
 * up to Sxx(pi) and wraps around to Sxx(-pi) - unless \p fft_shift is set to True, in which
 * case the DC carrier is shifted to the middle. The sum over one output vector multiplied by
 * 2 * pi / \p fft_len is the estimated power in the last \p ma_len blocks.
 *
 * \ingroup specest
 */
class specest_welch : public gr_hier_block2
{
 private:
	friend specest_welch_sptr
		specest_make_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift,
				const std::vector<float> &window);
	friend specest_welch_sptr
		specest_make_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift,
				int window_type, double beta);

	specest_welch(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window);

	unsigned d_fft_len;

	specest_stream_to_vector_overlap_sptr d_stream_to_vector;
	gr_fft_vcc_sptr d_fft;
	gr_complex_to_mag_squared_sptr  d_mag_square;
	specest_moving_average_vff_sptr d_moving_average;

 public:
        ~specest_welch();

	/**
	 * \brief Set the window applied before FFT. Must have same length as FFT length.
	 */
	bool set_window(const std::vector<float> &window) { return d_fft->set_window(window); };

	/**
	 * \brief Sets the window to the default (a Hamming window).
	 */
	bool set_hamming() { return set_window(gr_firdes::window(gr_firdes::WIN_HAMMING, d_fft_len, 0)); };
};

#endif /* INCLUDED_SPECEST_WELCH_H */

