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

#ifndef INCLUDED_SPECEST_WELCHSP_IMPL_H
#define INCLUDED_SPECEST_WELCHSP_IMPL_H

#include <specest/welchsp.h>

#include <gnuradio/blocks/complex_to_mag_squared.h>
#include <gnuradio/blocks/multiply_const_v.h>
#include <gnuradio/fft/fft_vcc.h>
#include <gnuradio/filter/single_pole_iir_filter_ff.h>
#include <specest/stream_to_vector_overlap.h>

namespace gr {
namespace specest {

class welchsp_impl : public welchsp
{
private:
    unsigned d_fft_len;

    gr::specest::stream_to_vector_overlap::sptr d_stream_to_vector;
    gr::fft::fft_vcc::sptr d_fft;
    gr::blocks::complex_to_mag_squared::sptr d_mag_square;
    gr::filter::single_pole_iir_filter_ff::sptr d_moving_average;
    gr::blocks::multiply_const_vff::sptr d_normalise;

public:
    welchsp_impl(unsigned fft_len,
                 int overlap,
                 double alpha,
                 bool fft_shift,
                 const std::vector<float>& window);
    ~welchsp_impl();

    /**
     * \brief Set the window applied before FFT. Must have same length as FFT length.
     */
    bool set_window(const std::vector<float>& window)
    {
        return d_fft->set_window(window);
    };

    /**
     * \brief Sets the window to the default (a Hamming window).
     */
    bool set_hamming()
    {
        return set_window(
            gr::filter::firdes::window(gr::filter::firdes::WIN_HAMMING, d_fft_len, 0));
    };
};

} // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_WELCHSP_IMPL_H */
