/* -*- c++ -*- */
/* 
 * Copyright 2011 Free Software Foundation, Inc.
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
#include <specest_music_spectrum_vcf.h>
#include <specesti_music_armadillo.h>


specest_music_spectrum_vcf_sptr
specest_make_music_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
{
	return specest_music_spectrum_vcf_sptr (new specest_music_spectrum_vcf (n, m, nsamples, pspectrum_len));
}


specest_music_spectrum_vcf::specest_music_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
	: gr_sync_block ("music_spectrum_vcf",
		gr_make_io_signature (1, 1, sizeof (gr_complex) * nsamples),
		gr_make_io_signature (1, 1, sizeof (float) * pspectrum_len)),
		d_m(m),
		d_n(n),
		d_nsamples(nsamples),
		d_pspectrum_len(pspectrum_len),
		d_impl(new specesti_music_armadillo(n,m))
{
}


specest_music_spectrum_vcf::~specest_music_spectrum_vcf ()
{
	delete d_impl;
}



int 
specest_music_spectrum_vcf::work (int noutput_items,
                                  gr_vector_const_void_star &input_items,
                                  gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];
	gr_complexd* double_input = new gr_complexd[d_nsamples];
	for(int i = 0; i < d_nsamples; i++)
		double_input[i] = static_cast<gr_complexd>(in[i]);

	float* out = static_cast<float*> (output_items[0]);
	double* tmpout = new double[d_pspectrum_len];
	d_impl->calculate_pseudospectrum(double_input, d_nsamples, tmpout, d_pspectrum_len);
	for(int i = 0; i < d_pspectrum_len; i++)
		out[i] = (float) tmpout[i];

	delete[] double_input;
	delete[] tmpout;

	return 1;
}

