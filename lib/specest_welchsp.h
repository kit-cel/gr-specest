/* -*- c++ -*- */
/*
 * Copyright 2011 Communications Engineering Lab, KIT
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

#ifndef INCLUDED_SPECEST_WELCHSP_H
#define INCLUDED_SPECEST_WELCHSP_H

#include <gr_hier_block2.h>
#include <gr_fft_vcc.h>
#include <gr_complex_to_xxx.h>
#include <gr_firdes.h>
#include <gr_single_pole_iir_filter_ff.h>
#include <gr_multiply_const_vff.h>
#include <specest_stream_to_vector_overlap.h>

class specest_welchsp;
typedef boost::shared_ptr<specest_welchsp> specest_welchsp_sptr;

/*
 * \brief Create a Welch spectrum estimator with user defined window
 */
specest_welchsp_sptr
specest_make_welchsp(unsigned fft_len, int overlap, double alpha,
					 bool fft_shift, const std::vector<float> &window);

/*
 * \brief Create a Welch spectrum estimator using internal window functions.
 */
specest_welchsp_sptr
specest_make_welchsp(unsigned fft_len, int overlap = -1, double alpha = .1, bool fft_shift = false,
		int window_type = (int) gr_firdes::WIN_HAMMING, double beta = 6.76);
// Declaring int instead of win_type makes it compatible with Python

/**
 * \brief Estimate spectral density Sxx(w) using a modified Welch's method.
 *
 * This estimator almost works exactly like specest_welch, but the moving average
 * is replaced by a single-pole IIR filter. This copies what's happening in
 * uhd_fft.py
 *
 * \ingroup specest
 */
class specest_welchsp : public gr_hier_block2
{
 private:
	friend specest_welchsp_sptr
		specest_make_welchsp(unsigned fft_len, int overlap, double alpha, bool fft_shift,
				const std::vector<float> &window);
	friend specest_welchsp_sptr
		specest_make_welchsp(unsigned fft_len, int overlap, double alpha, bool fft_shift,
				int window_type, double beta);

	specest_welchsp(unsigned fft_len, int overlap, double alpha, bool fft_shift, const std::vector<float> &window);

	unsigned d_fft_len;

	specest_stream_to_vector_overlap_sptr d_stream_to_vector;
	gr_fft_vcc_sptr d_fft;
	gr_complex_to_mag_squared_sptr  d_mag_square;
	gr_single_pole_iir_filter_ff_sptr d_moving_average;
	gr_multiply_const_vff_sptr d_normalise;

 public:
        ~specest_welchsp();

	/**
	 * \brief Set the window applied before FFT. Must have same length as FFT length.
	 */
	bool set_window(const std::vector<float> &window) { return d_fft->set_window(window); };

	/**
	 * \brief Sets the window to the default (a Hamming window).
	 */
	bool set_hamming() { return set_window(gr_firdes::window(gr_firdes::WIN_HAMMING, d_fft_len, 0)); };
};

#endif /* INCLUDED_SPECEST_WELCHSP_H */

