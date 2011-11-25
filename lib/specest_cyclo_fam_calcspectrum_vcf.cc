/* -*- c++ -*- */
/*
 * Copyright 2011 Communications Engineering Lab, KIT
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
#include <specest_cyclo_fam_calcspectrum_vcf.h>


specest_cyclo_fam_calcspectrum_vcf_sptr
specest_make_cyclo_fam_calcspectrum_vcf (int Np, int P, int L)
{
	return specest_cyclo_fam_calcspectrum_vcf_sptr (new specest_cyclo_fam_calcspectrum_vcf (Np, P, L));
}


specest_cyclo_fam_calcspectrum_vcf::specest_cyclo_fam_calcspectrum_vcf (int Np, int P, int L)
    :gr_sync_interpolator ("cyclo_fam_calcspectrum_vcf",
     gr_make_io_signature (1, 1, sizeof (gr_complex)*Np),
     gr_make_io_signature (1, 1, sizeof (float)*(2*Np)), 2*L),
     d_Np(Np),
     d_P(P),
     d_N(P*L),
     d_L(L),
     d_p_index(0)
{
    set_history(P);

    d_calcspectrum = new specesti_cyclo_fam_calcspectrum(Np,P,L);
    //d_outbuffer = d_calcspectrum->get_outputs();
}


specest_cyclo_fam_calcspectrum_vcf::~specest_cyclo_fam_calcspectrum_vcf ()
{
    delete d_calcspectrum;
}


int
specest_cyclo_fam_calcspectrum_vcf::work (int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
{
    const gr_complex *in = (const gr_complex *) input_items[0];
	float *out = (float *) output_items[0];
	d_K = interpolation();
    int ninput_items = noutput_items/(d_K);

    for(int w = 0; w < ninput_items; w++) {
       
        // Write estimate to outputstream
        for(int p = 0; p < d_K ;p++) {
	
	        for(int i_column = 0; i_column < (2*d_Np-1); i_column++) {
	        
	        out[w*2*d_Np*d_K+p*2*d_Np+i_column]  = d_calcspectrum->get_value(p+d_p_index*d_K,i_column);
	        }
	            
	        out[w*2*d_Np*d_K+p*2*d_Np+2*d_Np-1]  = d_calcspectrum->get_value(p+d_p_index*d_K,0); //peridoicity
	    	
	    }


        /*for(int p = 0; p < d_K ;p++) {                            // No. of output w: w*2*d_Np*d_K
            out[w*2*d_Np*d_K+p*2*d_Np]=d_outbuffer[p+d_p_index*d_K]; // alpha_index = d_p_index*d_K

            for(int i = 1; i < 2*d_Np-1; i++) {
                out[w*2*d_Np*d_K+p*2*d_Np+i] = d_outbuffer[p+d_p_index*d_K+2*d_N*i];
            }
            out[w*2*d_Np*d_K+p*2*d_Np+2*d_Np-1] = d_outbuffer[p+d_p_index*d_K]; //peridoicity
        }*/


        // check if there are P new input items, if so calc new estimate
        if(++d_p_index == (2*d_N/d_K)) {
            d_calcspectrum->calc(in);
            d_p_index=0;
        }

        in += d_Np; // Move input pointer
	}
	// Tell runtime system how many output items we produced.
	return noutput_items;
}

