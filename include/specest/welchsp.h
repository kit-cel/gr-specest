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


#ifndef INCLUDED_SPECEST_WELCHSP_H
#define INCLUDED_SPECEST_WELCHSP_H

#include <gnuradio/hier_block2.h>
#include <specest/api.h>

#include <gnuradio/filter/firdes.h>

namespace gr {
namespace specest {

/*!
 * \brief Estimate spectral density Sxx(w) using a modified Welch's method.
 *
 * This estimator almost works exactly like specest_welch, but the moving average
 * is replaced by a single-pole IIR filter. This copies what's happening in
 * the QT Frequency Sink
 */
class SPECEST_API welchsp : virtual public gr::hier_block2
{
public:
    typedef boost::shared_ptr<welchsp> sptr;

    /*!
     * \param fft_len FFT length
     * \param overlap Number of samples overlap per periodogram. A value of -1
     *                sets it to fft_len/2.
     * \param alpha Averaging coefficient
     * \param fft_shift If true, DC is shifted to the middle
     * \param window Window taps. Must have the same length as fft_len
     */
    static sptr make(unsigned fft_len,
                     int overlap,
                     double alpha,
                     bool fft_shift,
                     const std::vector<float>& window);

    /*!
     * \param fft_len FFT length
     * \param overlap Number of samples overlap per periodogram. A value of -1
     *                sets it to fft_len/2.
     * \param alpha Averaging coefficient
     * \param fft_shift If true, DC is shifted to the middle
     * \param window Window type. The window taps are auto-calculated from
     *               \p fft_len and \p beta
     *\param beta Additional window parameter (see gr::filter::firdes::window)
     */
    static sptr make(unsigned fft_len,
                     int overlap = -1,
                     double alpha = .1,
                     bool fft_shift = false,
                     int window_type = (int)gr::filter::firdes::WIN_HAMMING,
                     double beta = 6.76);

    /**
     * \brief Set the window applied before FFT. Must have same length as FFT length.
     */
    virtual bool set_window(const std::vector<float>& window) = 0;

    /**
     * \brief Sets the window to the default (a Hamming window).
     */
    virtual bool set_hamming() = 0;
};

} // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_WELCHSP_H */
