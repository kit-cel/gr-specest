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

#include "fcov_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace specest {

inline void
check_arguments_algo(unsigned int fft_len, unsigned int num_samples, unsigned int order)
{
    if (fft_len < 2) {
        throw std::invalid_argument("specest_fcov: The length of FFT window should be "
                                    "greater than or equal to 2.");
    }
    if (num_samples < 2) {
        throw std::invalid_argument(
            "specest_fcov: The number of samples should be greater than or equal to 2.");
    }
    if (order < 2) {
        throw std::invalid_argument(
            "specest_fcov: The order of AR filter should be greater than or equal to 2.");
    }
}

fcov::sptr fcov::make(
    unsigned block_len, unsigned fft_len, unsigned order, bool fftshift, int decimation)
{
    check_arguments_algo(fft_len, block_len, order);
    return gnuradio::get_initial_sptr(
        new fcov_impl(block_len, fft_len, order, fftshift, decimation));
}

/*
 * The private constructor
 */
fcov_impl::fcov_impl(
    unsigned block_len, unsigned fft_len, unsigned order, bool fftshift, int decimation)
    : gr::hier_block2("fcov",
                      gr::io_signature::make(1, 1, sizeof(gr_complex)),
                      gr::io_signature::make(1, 1, sizeof(float) * fft_len)),
      d_stream_to_vector(
          stream_to_vector_overlap::make(sizeof(gr_complex), block_len, 0)),
      d_keep_one_in_n(
          blocks::keep_one_in_n::make(sizeof(gr_complex) * block_len, decimation)),
      d_arfcov(arfcov_vcc::make(block_len, order, fft_len)),
      d_pad_vector(pad_vector::make(sizeof(gr_complex), order + 1, fft_len)),
      d_fft(fft::fft_vcc::make(
          fft_len,
          true,
          filter::firdes::window(filter::firdes::WIN_RECTANGULAR, fft_len, 1),
          fftshift)), // TODO: it fails here!
      d_mag_square(blocks::complex_to_mag_squared::make(fft_len)),
      d_divide(reciprocal_ff::make(fft_len))
{
    connect(self(), 0, d_stream_to_vector, 0);
    connect(d_stream_to_vector, 0, d_keep_one_in_n, 0);
    connect(d_keep_one_in_n, 0, d_arfcov, 0);
    connect(d_arfcov, 0, d_pad_vector, 0);
    connect(d_pad_vector, 0, d_fft, 0);
    connect(d_fft, 0, d_mag_square, 0);
    connect(d_mag_square, 0, d_divide, 0);
    connect(d_divide, 0, self(), 0);
}

/*
 * Our virtual destructor.
 */
fcov_impl::~fcov_impl() {}

void fcov_impl::set_decimation(int n) { d_keep_one_in_n->set_n(n); }

} /* namespace specest */
} /* namespace gr */
