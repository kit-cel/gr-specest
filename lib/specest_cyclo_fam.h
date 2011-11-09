/* -*- c++ -*- */
/* 
 * Copyright Communications Engineering Lab, KIT
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

#include <gr_hier_block2.h>
#include <specest_cyclo_fam_calcspectrum_vcf.h>
#include <specest_stream_to_vector_overlap.h>
#include <gr_fft_vcc.h>
#include <gr_firdes.h>

class specest_cyclo_fam;
typedef boost::shared_ptr<specest_cyclo_fam> specest_cyclo_fam_sptr;

/*
 * \brief Create a FAM spectrum estimator
 */
specest_cyclo_fam_sptr specest_make_cyclo_fam (int Np, int P, int decimation_factor);

/**
 * \brief Estimates the absolute value of the spectral correlation density |Sxx^\alpha(f)| using the FAM
 *
 * Parameters all have to be powers of two:
 * Np: length of the first FFT (in literature usually denoted with N', see reference below)
 * P:  length of the second FFT
 * L:  decimation factor (must be smaller than Np/4)
 *
 * Sxx(f)^alpha=1/N <X(n,f+alpha/2)X^*(n,f-alpha/2)>_N, where < > denotes the time smoothing over a time span of N=P*L samples.
 *
 * Function:
 * The estimator works on complex input signals. 
 * In a first step the channlizer computes de complex demodulates X(n,f) based on the number of Np samples per input.
 * In the second step the spectral correlation and time smoothing is done and the ouput is generated.
 * The spectral corrlation X(f+alpha/2)X^*(f-alpha/2) is based on time smoothing of P=N/L complex demodulates.
 * 
 * 
 *
 * Output:
 * |Sxx^\alpha(f)| is a 2-dimensional matrix with dimensions 2N x 2Np
 * The output matrix ist sliced in 2N vector items, where the first item contains the f-vector at the frequency f=-fs/2.
 * The last item contains the f-vector at the frequency f=fs/2. 
 * The alpha-vector starts at the frequency alpha = -fs and ends up at frequency alpha = fs(1-1/N) 
 * 
 *
 * Note:
 * The first FFT uses a hamming window and the products of the time smoothing a weighted by a rectangular window.
 *
 * Usage:
 * i.e. specest_make_cyclo_fam (64, 512, 4)
 *
 * References:
 * The FFT Accumulation Method (FAM) is described in
 * "Computationally Efficient Algorithms for Cyclic Spectral Analysis"
 * by Roberts, R.S.;   Brown, W.A.;   Loomis, H.H., Jr.
 * in: Signal Processing Magazine, IEEE Apr 1991 Vol 8(2)
 *
 * \ingroup specest
 */
class specest_cyclo_fam : public gr_hier_block2
{
	friend specest_cyclo_fam_sptr specest_make_cyclo_fam (int Np, int P, int L);
    /**
	 * \param Np Number of input samples for the channelizer. Used for computing the complex demodulates. Frequency resolution is approx. fs/Np  
	 * \param P Number of samples the estimate is based on. Cycle frequency resolution is approx. fs/(P*L)
	 * \param decimation_factor Also called L. Complex demodulates overlap by (Np-L) samples.
	 */   
    specest_cyclo_fam (int Np, int P, int decimation_factor);
    
    //Blocks
    specest_stream_to_vector_overlap_sptr        d_stream_to_vector;
    gr_fft_vcc_sptr                              d_Np_fft;
    specest_cyclo_fam_calcspectrum_vcf_sptr      d_calcspectrum;
    
  
    unsigned int                                 d_decimation_factor;

 public:

	~specest_cyclo_fam ();

    const float* get_estimate(){return d_calcspectrum->get_estimate();};
    /**
    * Direkt access to the estimate. Note estimate is an 1-dim array of size 2N*(2Np-1). 
    */
};

#endif /* INCLUDED_SPECEST_CYCLO_FAM_H */

