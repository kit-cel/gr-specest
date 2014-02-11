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


#ifndef INCLUDED_SPECEST_WELCHSP_H
#define INCLUDED_SPECEST_WELCHSP_H

#include <specest/api.h>
#include <gnuradio/hier_block2.h>

#include <gnuradio/filter/firdes.h>

namespace gr {
  namespace specest {

    /*!
     * \brief Estimate spectral density Sxx(w) using a modified Welch's method.
	 *
	 * This estimator almost works exactly like specest_welch, but the moving average
	 * is replaced by a single-pole IIR filter. This copies what's happening in
	 * uhd_fft.py
	 *
     */
    class SPECEST_API welchsp : virtual public gr::hier_block2
    {
     public:
      typedef boost::shared_ptr<welchsp> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of specest::welchsp.
       *
       * To avoid accidental use of raw pointers, specest::welchsp's
       * constructor is in a private implementation
       * class. specest::welchsp::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned fft_len, int overlap, double alpha, bool fft_shift, const std::vector<float> &window);
      static sptr make(unsigned fft_len, int overlap = -1, double alpha = .1, bool fft_shift = false, int window_type = (int) gr::filter::firdes::WIN_HAMMING, double beta = 6.76);
    
		/**
		 * \brief Set the window applied before FFT. Must have same length as FFT length.
		 */
	  virtual bool set_window(const std::vector<float> &window) = 0;

		/**
		 * \brief Sets the window to the default (a Hamming window).
		 */
	  virtual bool set_hamming() = 0;
	};

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_WELCHSP_H */

