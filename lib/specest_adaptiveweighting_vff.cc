/* -*- c++ -*- */
/*
 * Copyright 2010 Communications Engineering Lab, KIT
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

#include <gr_io_signature.h>
#include <specest_adaptiveweighting_vff.h>

specest_adaptiveweighting_vff_sptr
specest_make_adaptiveweighting_vff (size_t vlen, const std::vector<float> lambdas)
{
	return specest_adaptiveweighting_vff_sptr (new specest_adaptiveweighting_vff (vlen, lambdas));
}


specest_adaptiveweighting_vff::specest_adaptiveweighting_vff (size_t vlen, const std::vector<float> lambdas)
	: gr_sync_block ("adaptiveweighting_vff",
			gr_make_io_signature (1, -1, sizeof (float)*vlen),
			gr_make_io_signature (1,  1, sizeof (float)*vlen)),
	d_vlen(vlen),
	d_lambdas(lambdas)
{
}


int
specest_adaptiveweighting_vff::work (int noutput_items,
		gr_vector_const_void_star &input_items,
		gr_vector_void_star &output_items)
{
	float *optr = (float *) output_items[0];
	int ninputs = input_items.size ();
	int n_items_per_block = output_signature()->sizeof_stream_item(0)/sizeof(float);
	//two dimensional vector
	//rather ugly
	std::vector< std::vector< float> > d_k(ninputs, std::vector<float>(d_vlen));
	std::vector< float > spectrum(d_vlen);
	//initial PSD-Estimate
	for (int i = 0; i < d_vlen; i++){
		spectrum[i]  += (1./2.) * (((float *) input_items[0])[i] + ((float *) input_items[1])[i]);
	}
	// the accuracy of the psd-estimate increases with the number of runs. 3 runs is a good compromise according to [1]
	for (int run = 0; run < 3; run++){
		//calculating Power
		float sigma2 = 0;
		for (int i = 0; i < d_vlen; i++){
			sigma2 += spectrum[i];
		}
		sigma2 /= d_vlen;
		//calculating weighting coefficients
		for (int i = 0; i < ninputs; i++){
			for (int j = 0; j < d_vlen; j++){
				d_k[i][j] = ( spectrum[j]/(d_lambdas[i]*spectrum[j] + (1 - d_lambdas[i])*sigma2) );
			}
		}
		//calculating new PSD see [1] p 370
		for (int i = 0; i < d_vlen; i++){
			float numerator = d_lambdas[0] * d_k[0][i] * d_k[0][i]*( ((float *) input_items[0])[i]);
			float denominator = d_lambdas[0] * d_k[0][i] * d_k[0][i];
			float factor;
			for (int j = 1; j < ninputs; j++){
				factor = d_lambdas[j] * d_k[j][i] * d_k[j][i];
				numerator += factor * (((float *) input_items[j])[i]);
				denominator += factor;
			}
			spectrum[i] = (float) numerator/denominator;
		}
	}
	for (int i = 0; i < n_items_per_block; i++){
		*optr++ = spectrum[i];
	}
	return noutput_items;
}

/* [1] "Spectral Analysis for Physical Applications" D.B. Percival and Andrew T. Walden 1993 */

