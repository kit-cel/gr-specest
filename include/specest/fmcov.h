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


#ifndef INCLUDED_SPECEST_FMCOV_H
#define INCLUDED_SPECEST_FMCOV_H

#include <specest/api.h>
#include <gnuradio/hier_block2.h>

namespace gr {
  namespace specest {

	/**
	 * \brief Estimate PSD using the (fast) modified covariance method.
	 *
	 * Split the input stream into chunks, and performs the following operation on each chunk:
	 * - Calculate the AR coefficients of the given order by Marple's fast modified covariance algorithm
	 * - Use an FFT on the coefficients to calculate the spectral estimate
	 *
	 * No averaging in time is performed. To do this, append a moving_average_vff or
	 * single_pole_iir_filter_ff.
	 *
	 * \ingroup specest
	 */
	 
	/**
	 * \param block_len Number of input samples to be analysed for one output vector
	 * \param fft_len Number of points in FFT (equal to the output vector length)
	 * \param order The order of the AR model
	 * \param fftshift True means DC is shifted to the middle
	 * \param decimation Only process every n-th block. Results in less operations per input sample, but
	 *                   results in a lower update rate of the spectrum estimate.
	 */
	 
    class SPECEST_API fmcov : virtual public gr::hier_block2
    {
     public:
      typedef boost::shared_ptr<fmcov> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of specest::fmcov.
       *
       * To avoid accidental use of raw pointers, specest::fmcov's
       * constructor is in a private implementation
       * class. specest::fmcov::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned block_len, unsigned fft_len, unsigned order, bool fftshift = false, int decimation = 1);
      virtual void set_decimation(int n) = 0; //!< Update the decimation rate at the input      
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_FMCOV_H */

