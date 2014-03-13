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


#ifndef INCLUDED_SPECEST_CYCLO_FAM_H
#define INCLUDED_SPECEST_CYCLO_FAM_H

#include <specest/api.h>
#include <gnuradio/hier_block2.h>

namespace gr {
  namespace specest {

    /*!
     * \brief Estimates the absolute value of the spectral correlation density \f$|Sxx^\alpha(f)|\f$ using the FAM.
	 *
	 * This first calculates
	 * \f[
	 * S_{xx}^\alpha(f) = \frac{1}{N} <X(n,f+\alpha/2) X^*(n,f-\alpha/2)>_N,
	 * \f]
	 * where < > denotes the time smoothing over a time span of \f$N=P*L\f$ samples.
	 *
	 * \param Np length of the first FFT (in literature usually denoted with N', see reference below)
	 * \param P  length of the second FFT
	 * \param L  decimation factor (must be smaller than Np/4)
	 * Parameters all have to be multiples of two.
	 *
	 * \b Function:
	 * The estimator works on input streams of complex samples.
	 * In a first step, the channelizer computes complex demodulates \f$X(n,f)\f$
	 * based on the number of Np samples per input.
	 * In the second step, the spectral correlation and time smoothing is done and
	 * the output is generated. The spectral correlation
	 * \f$X(f+\alpha/2)X^*(f-\alpha/2)\f$ is based on time smoothing of P=N/L
	 * complex demodulates.
	 * \f$f_s\f$ is the normalised sampling rate; \f$-0.5 \leq f_s \leq 0.5\f$.
	 *
	 * \b Output:
	 * \f$|Sxx^\alpha(f)|\f$ is a 2-dimensional matrix with dimensions 2N x 2Np.
	 * The output matrix is sliced in 2N vector items, where the first item
	 * contains the f-vector at the frequency \f$f=-f_s/2\f$.
	 * The last item contains the f-vector at the frequency \f$f=f_s/2\f$.
	 * The \f$\alpha\f$-vector starts at the frequency \f$\alpha = -f_s\f$ and ends
	 * at frequency \f$\alpha = f_s(1-1/N)\f$.
	 *
	 * \b Note:
	 * The first FFT uses a Hamming window and the products of the time smoothing
	 * (2nd FFT) a rectangular window.
	 *
	 * \b References:
	 * The FFT Accumulation Method (FAM) is described in
	 * "Computationally Efficient Algorithms for Cyclic Spectral Analysis"
	 * by Roberts, R.S.;   Brown, W.A.;   Loomis, H.H., Jr.
	 * in: Signal Processing Magazine, IEEE Apr 1991 Vol 8(2)
     * \ingroup specest
     *
     */
    class SPECEST_API cyclo_fam : virtual public gr::hier_block2
    {
     public:
      typedef boost::shared_ptr<cyclo_fam> sptr;
       
	/*
	 * \brief Create a FAM spectrum estimator with sample frequency independent parameters
	 */
	/**
	 * \param Np Number of input samples for the channelizer. Used for computing the complex demodulates. Frequency resolution is approx. fs/Np.
	 * \param P Number of samples the estimate is based on. Cycle frequency resolution is approx. fs/(P*L).
	 * \param decimation_factor Also called L. Complex demodulates overlap by (Np-L) samples.
	 */

      static sptr make(int Np, int P, int decimation_factor);
	/*
	 * \brief Create a FAM spectrum estimator with desired resolution in frequency and cycle frequency
	 */
 	/**
	 * \param sample_frequency
	 * \param delta_f Desired Frequency resolution
	 * \param delta_alpha Desired Cycle Frequency resolution
	 * \param overlap Overlap of the complex demodulates in percent. Should be between 75%...100% (maximum overlap)
	 */
      static sptr make(float sample_frequency, float delta_f, float delta_alpha, float overlap);
    
	  virtual int get_Np() = 0;
	  virtual int get_N() = 0;
      virtual int get_P() = 0;
      virtual int get_L() = 0;

	  virtual float get_sample_frequency() = 0;
      virtual float get_frequency_resolution() = 0;
      virtual float get_cycle_frequency_resolution() = 0;

	/**
	* Direct access to the estimate. Note: Estimate is a 2-dim array of size 2N x (2Np-1).
	*/
	  virtual const std::vector<std::vector<float> > &get_estimate() = 0;
	};
  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_CYCLO_FAM_H */

