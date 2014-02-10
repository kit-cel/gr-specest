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

#ifndef INCLUDED_SPECEST_WELCH_IMPL_H
#define INCLUDED_SPECEST_WELCH_IMPL_H

#include <specest/welch.h>

#include <gnuradio/fft/fft_vcc.h>
#include <gnuradio/blocks/complex_to_mag_squared.h>
#include <specest/stream_to_vector_overlap.h>
#include <specest/moving_average_vff.h>

namespace gr {
  namespace specest {

    class welch_impl : public welch
    {
     private:
		unsigned d_fft_len;
		stream_to_vector_overlap::sptr d_stream_to_vector;
		fft::fft_vcc::sptr d_fft;
		blocks::complex_to_mag_squared::sptr  d_mag_square;
		moving_average_vff::sptr d_moving_average;

     public:
      welch_impl(unsigned fft_len, int overlap, int ma_len, bool fft_shift, const std::vector<float> &window);
      ~welch_impl();

		/**
		 * \brief Set the window applied before FFT. Must have same length as FFT length.
		 */
		bool set_window(const std::vector<float> &window) { return d_fft->set_window(window); };

		/**
		 * \brief Sets the window to the default (a Hamming window).
		 */
		bool set_hamming() { return set_window(filter::firdes::window(filter::firdes::WIN_HAMMING, d_fft_len, 0)); };
		};

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_WELCH_IMPL_H */

