/* -*- c++ -*- */
/*
 * Copyright 2009 Institut fuer Nachrichtentechnik / Uni Karlsruhe
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

#ifndef INCLUDED_SPECEST_BURG_H
#define INCLUDED_SPECEST_BURG_H

#include <gr_hier_block2.h>
#include <gr_fft_vcc.h>
#include <gr_complex_to_xxx.h>
#include <gr_keep_one_in_n.h>
#include <gr_firdes.h>
#include <specest_reciprocal_ff.h>
#include <specest_arburg_vcc.h>
#include <specest_stream_to_vector_overlap.h>
#include <specest_pad_vector.h>

class specest_burg;
typedef boost::shared_ptr<specest_burg> specest_burg_sptr;

specest_burg_sptr
specest_make_burg(unsigned block_len,
					unsigned fft_len,
					unsigned order,
					bool fftshift = false,
					int decimation = 1);


/**
 * \brief Estimate PSD using Burg's method.
 *
 * Split the input stream into chunks, and performs the following operation on
 * each chunk:
 * - Calculate the AR coefficients of the given order by Burg's algorithm
 * - Use an FFT on the coefficients to calculate the spectral estimate
 *
 * No averaging in time is performed. To do this, append a moving_average_vff or
 * single_pole_iir_filter_ff.
 *
 * \ingroup specest
 */
class specest_burg : public gr_hier_block2
{
 private:
	friend specest_burg_sptr specest_make_burg(unsigned block_len,
												unsigned fft_len,
												unsigned order,
												bool fftshift,
												int decimation);
	/**
	 * \param block_len Number of input samples to be analysed for one output vector
	 * \param fft_len Number of points in FFT (equal to the output vector length)
	 * \param order The order of the AR model
	 * \param fftshift True means DC is shifted to the middle
	 * \param decimation Only process every n-th block. Results in less
	 *                   operations per input sample, but results in a lower
	 *                   update rate of the spectrum estimate.
	 */
	specest_burg(unsigned block_len,
					unsigned fft_len,
					unsigned order,
					bool fftshift,
					int decimation);
	
	specest_stream_to_vector_overlap_sptr d_stream_to_vector;
	gr_keep_one_in_n_sptr d_keep_one_in_n;
	specest_arburg_vcc_sptr d_arburg;
	specest_pad_vector_sptr d_pad_vector;
	gr_fft_vcc_sptr d_fft;
	gr_complex_to_mag_squared_sptr d_mag_square;
	specest_reciprocal_ff_sptr d_divide;

 public:
	~specest_burg();

	void set_decimation(int n); //!< Update the decimation rate at the input
};

#endif /* INCLUDED_SPECEST_BURG_H */

