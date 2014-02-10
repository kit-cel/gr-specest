/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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
#include "welch_impl.h"

#include <iostream>

namespace gr {
  namespace specest {
  
	/**
	 * \brief Calculate the correct normalisation factor
	 *
	 * The following is considered:
	 * - FFT length (so Parseval's theorem can be applied)
	 * - The length of the moving average (because the scaling is done after the summation)
	 * - The power of the window function
	 */
	inline float
	specest_calculate_ma_scale_impl(int fft_len, int ma_len, const std::vector<float> &window)
	{

		float scale = 1.0 / (fft_len * ma_len * 2 * M_PI);
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
			throw std::invalid_argument("specest_welch: when providing a window, it must have the same length as fft_len.");
		}
		if (overlap < -1) {
			throw std::invalid_argument("specest_welch: overlap can not be negative.");
		}
	}
	
    welch::sptr
    welch::make(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window)
    {
      specest_check_arguments_impl(fft_len, overlap, window);
      return gnuradio::get_initial_sptr
        (new welch_impl(fft_len, overlap, ma_len, fft_shift, window));
    }
    
    welch::sptr
    welch::make(unsigned fft_len, int overlap, int ma_len, bool fft_shift, int window_type, double beta)
    {
		std::vector<float> window;
		if (window_type != filter::firdes::WIN_RECTANGULAR) {
			std::vector<float> window = filter::firdes::window((filter::firdes::win_type)window_type, fft_len, beta);
		}
		return gnuradio::get_initial_sptr
			(new welch_impl(fft_len, overlap, ma_len, fft_shift, window));
    }   

    /*
     * The private constructor
     */
    welch_impl::welch_impl(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window)
      : gr::hier_block2("welch",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(float) * fft_len)),
		d_fft_len(fft_len),
		d_stream_to_vector(stream_to_vector_overlap::make(sizeof(gr_complex), fft_len, (overlap == -1) ? fft_len/2 : overlap)),
		d_fft(fft::fft_vcc::make(fft_len, true, window, fft_shift)),
		d_mag_square(blocks::complex_to_mag_squared::make(fft_len)),
		d_moving_average(moving_average_vff::make(ma_len, fft_len,
		specest_calculate_ma_scale_impl(fft_len, ma_len, window)))
    {
		connect(self(), 0, d_stream_to_vector, 0);
		connect(d_stream_to_vector, 0, d_fft, 0);
		connect(d_fft, 0, d_mag_square, 0);
		connect(d_mag_square, 0, d_moving_average, 0);
		connect(d_moving_average, 0, self(), 0);
    }

    /*
     * Our virtual destructor.
     */
    welch_impl::~welch_impl()
    {
    }


  } /* namespace specest */
} /* namespace gr */

