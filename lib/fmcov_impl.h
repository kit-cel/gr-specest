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

#ifndef INCLUDED_SPECEST_FMCOV_IMPL_H
#define INCLUDED_SPECEST_FMCOV_IMPL_H

#include <specest/fmcov.h>

#include <gnuradio/blocks/complex_to_mag_squared.h>
#include <gnuradio/blocks/keep_one_in_n.h>
#include <gnuradio/filter/firdes.h>
#include <gnuradio/fft/fft_vcc.h>
#include <specest/reciprocal_ff.h>
#include <specest/arfmcov_vcc.h>
#include <specest/stream_to_vector_overlap.h>
#include <specest/pad_vector.h>

namespace gr {
  namespace specest {

    class fmcov_impl : public fmcov
    {
     private:
		stream_to_vector_overlap::sptr d_stream_to_vector;
		blocks::keep_one_in_n::sptr d_keep_one_in_n;
		arfmcov_vcc::sptr d_arfmcov;
		pad_vector::sptr d_pad_vector;
		fft::fft_vcc::sptr d_fft;
		blocks::complex_to_mag_squared::sptr d_mag_square;
		reciprocal_ff::sptr d_divide;

     public:
      fmcov_impl(unsigned block_len, unsigned fft_len, unsigned order, bool fftshift, int decimation);
      ~fmcov_impl();
      
      void set_decimation(int n); //!< Update the decimation rate at the input
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_FMCOV_IMPL_H */

