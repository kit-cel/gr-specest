/* -*- c++ -*- */
/* 
 * Copyright 2014 Communications Engineering Lab, KIT
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "welchsp_impl.h"

#include <stdexcept>
#include <cmath>

namespace gr {
  namespace specest {

    inline float
    specest_calculate_norm_factor_impl(int fft_len, const std::vector<float> &window)
    {
      float scale = 1.0 / (fft_len * 2 * M_PI);
      if (window.size() == 0) {
	return scale;
      }

      float window_power = 0;
      for(unsigned i = 0; i < window.size(); i++) {
	window_power += window[i] * window[i];
      }
      window_power /= fft_len;

      return scale / window_power;
    }

    // I'd prefer doing this in the specest constructor, but for some reason throwing
    // exceptions in the constructor ends up in seg faults in the Python domain
    inline void
    specest_check_arguments_impl(unsigned fft_len, int overlap, const std::vector<float> &window)
    {
      if (window.size() != 0 && window.size() != fft_len) {
	throw std::invalid_argument("specest_welchsp: when providing a window, it must have the same length as fft_len.");
      }
      if (overlap < -1) {
	throw std::invalid_argument("specest_welchsp: overlap can not be negative.");
      }
    }

    welchsp::sptr
    welchsp::make(unsigned fft_len, int overlap, double alpha, bool fft_shift, const std::vector<float> &window)
    {
      specest_check_arguments_impl(fft_len, overlap, window);
      return gnuradio::get_initial_sptr
	(new welchsp_impl(fft_len, overlap, alpha, fft_shift, window));
    }

    welchsp::sptr
    welchsp::make(unsigned fft_len, int overlap, double alpha, bool fft_shift, int window_type, double beta)
    {
      std::vector<float> window;
      if (window_type != gr::filter::firdes::WIN_RECTANGULAR) {
	std::vector<float> window = gr::filter::firdes::window((gr::filter::firdes::win_type)window_type, fft_len, beta);
      }
      specest_check_arguments_impl(fft_len, overlap, window);
      return gnuradio::get_initial_sptr
	(new welchsp_impl(fft_len, overlap, alpha, fft_shift, window));
    }

    welchsp_impl::welchsp_impl(unsigned fft_len, int overlap, double alpha, bool fft_shift, const std::vector<float> &window)
      : gr::hier_block2("welchsp",
	  gr::io_signature::make(1, 1, sizeof(gr_complex)),
	  gr::io_signature::make(1, 1, sizeof(float) * fft_len)),
      d_fft_len(fft_len),
      d_stream_to_vector(gr::specest::stream_to_vector_overlap::make(sizeof(gr_complex), fft_len, (overlap == -1) ? fft_len/2 : overlap)),
      d_fft(gr::fft::fft_vcc::make(fft_len, true, window, fft_shift)),
      d_mag_square(gr::blocks::complex_to_mag_squared::make(fft_len)),
      d_moving_average(gr::filter::single_pole_iir_filter_ff::make(alpha, fft_len)),
      d_normalise(gr::blocks::multiply_const_vff::make(std::vector<float>(fft_len, specest_calculate_norm_factor_impl(fft_len, window))))
    {
      connect(self(), 0, d_stream_to_vector, 0);
      connect(d_stream_to_vector, 0, d_fft, 0);
      connect(d_fft, 0, d_mag_square, 0);
      connect(d_mag_square, 0, d_moving_average, 0);
      connect(d_moving_average, 0, d_normalise, 0);
      connect(d_normalise, 0, self(), 0);
    }

    welchsp_impl::~welchsp_impl()
    {
    }

  } /* namespace specest */
} /* namespace gr */

