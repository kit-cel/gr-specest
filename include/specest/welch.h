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


#ifndef INCLUDED_SPECEST_WELCH_H
#define INCLUDED_SPECEST_WELCH_H

#include <gnuradio/hier_block2.h>
#include <specest/api.h>

#include <gnuradio/filter/firdes.h>

namespace gr {
namespace specest {

/**
 * \brief Estimate spectral density Sxx(w) using Welch's method.
 *
 * The estimator works on complex input signals. If \p overlap is left unspecified or -1,
 * a 50% overlap is calculated. The standard window is a Hamming window, but can be
 * changed to be anything else. The output is a vector containing the moving average of the
 * last \p ma_len overlapping, windowed periodograms signal segments. The first element is
 * Sxx(0), then goes up to Sxx(pi) and wraps around to Sxx(-pi), unless \p fft_shift is
 * set to True, in which case the DC carrier is shifted to the middle. The sum over one
 * output vector multiplied by 2 * pi / \p fft_len is the estimated power in the last \p
 * ma_len blocks.
 *
 * \ingroup specest
 */

class SPECEST_API welch : virtual public gr::hier_block2
{
public:
    typedef boost::shared_ptr<welch> sptr;

    /*!
     * \param fft_len FFT length
     * \param overlap Number of samples overlap per periodogram. A value of -1
     *                sets it to fft_len/2.
     * \param ma_len Moving-Average Length (number of periodograms to average)
     * \param fft_shift If true, DC is shifted to the middle
     * \param window Window taps. Must have the same length as fft_len
     */
    static sptr make(unsigned fft_len,
                     int overlap,
                     int ma_len,
                     bool fft_shift,
                     const std::vector<float>& window);

    /*!
     * \param fft_len FFT length
     * \param overlap Number of samples overlap per periodogram. A value of -1
     *                sets it to fft_len/2.
     * \param ma_len Moving-Average Length (number of periodograms to average)
     * \param fft_shift If true, DC is shifted to the middle
     * \param window Window type. The window taps are auto-calculated from
     *               \p fft_len and \p beta
     *\param beta Additional window parameter (see gr::filter::firdes::window)
     */
    static sptr make(unsigned fft_len,
                     int overlap = -1,
                     int ma_len = 8,
                     bool fft_shift = false,
                     int window_type = (int)gr::filter::firdes::WIN_HAMMING,
                     double beta = 6.76);
    // Declaring int instead of win_type makes it compatible with Python

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

#endif /* INCLUDED_SPECEST_WELCH_H */
