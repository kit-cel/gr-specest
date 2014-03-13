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
#include "burg_impl.h"

namespace gr {
  namespace specest {
  
	// I'd prefer doing this in the specest constructor, but for some reason
	// throwing exceptions in the constructor ends up in segfaults in the Python
	// domain
	inline void
	specest_check_arguments_impl(unsigned fft_len, unsigned num_samples, unsigned order)
	{
	  if (fft_len < 2) {
		throw std::invalid_argument("specest_burg: The length of FFT window should be greater than or equal to 2.");
	  }
	  if (num_samples < 2) {
		throw std::invalid_argument("specest_burg: The number of samples should be greater than or equal to 2.");
	  }
	  if (order < 2) {
		throw std::invalid_argument("specest_burg: The order of AR filter should be greater than or equal to 2.");
	  }
	}

    burg::sptr
    burg::make(unsigned block_len, unsigned fft_len, unsigned order, bool fftshift, int decimation)
    {
      specest_check_arguments_impl(fft_len, block_len, order);
      return gnuradio::get_initial_sptr
        (new burg_impl(block_len, fft_len, order, fftshift, decimation));
    }

    /*
     * The private constructor
     */
    burg_impl::burg_impl(unsigned block_len, unsigned fft_len, unsigned order, bool fftshift, int decimation)
      : gr::hier_block2("burg",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1,sizeof(float)*fft_len)),
		d_stream_to_vector(stream_to_vector_overlap::make(sizeof(gr_complex), block_len, 0)),
		d_keep_one_in_n(blocks::keep_one_in_n::make(sizeof(gr_complex) * block_len, decimation)),
		d_arburg(arburg_vcc::make(block_len, order, fft_len)),
		d_pad_vector(pad_vector::make(sizeof(gr_complex), order+1, fft_len)),
		d_fft(fft::fft_vcc::make(fft_len, true, filter::firdes::window(filter::firdes::WIN_RECTANGULAR, fft_len, 1), fftshift)),
		d_mag_square(blocks::complex_to_mag_squared::make(fft_len)),
		d_divide(reciprocal_ff::make(fft_len))              
    {
		connect(self(), 0, d_stream_to_vector, 0);
		connect(d_stream_to_vector, 0, d_keep_one_in_n, 0);
		connect(d_keep_one_in_n, 0, d_arburg, 0);
		connect(d_arburg, 0, d_pad_vector, 0);
		connect(d_pad_vector, 0, d_fft, 0);
		connect(d_fft, 0, d_mag_square, 0);
		connect(d_mag_square, 0, d_divide, 0);
		connect(d_divide, 0, self(), 0);
    }

    /*
     * Our virtual destructor.
     */
    burg_impl::~burg_impl()
    {
    }

	void
	burg_impl::set_decimation(int n)
	{
		d_keep_one_in_n->set_n(n);
	}

  } /* namespace specest */
} /* namespace gr */

