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
#include <specest_esprit_spectrum_vcf.h>
#include <specest_esprit_fortran_impl.h>


specest_esprit_spectrum_vcf_sptr
specest_make_esprit_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
{
	return specest_esprit_spectrum_vcf_sptr (new specest_esprit_spectrum_vcf (n, m, nsamples, pspectrum_len));
}


specest_esprit_spectrum_vcf::specest_esprit_spectrum_vcf (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
	: gr_sync_block ("esprit_spectrum_vcf",
		gr_make_io_signature (1, 1, sizeof (gr_complex) * nsamples),
		gr_make_io_signature (1, 1, sizeof (float) * pspectrum_len)),
	d_m(m),
	d_n(n),
	d_nsamples(nsamples),
	d_pspectrum_len(pspectrum_len),
	d_impl(new specest_esprit_fortran_impl(n,m)),
	d_in_buf(d_nsamples, 0),
	d_out_buf(d_pspectrum_len, 0)
{
}


specest_esprit_spectrum_vcf::~specest_esprit_spectrum_vcf ()
{
	delete d_impl;
}


int
specest_esprit_spectrum_vcf::work (int noutput_items,
                                   gr_vector_const_void_star &input_items,
                                   gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];
	float* out = static_cast<float*> (output_items[0]);

	for (int item = 0; item < noutput_items; item++) {
		for(int i = 0; i < d_nsamples; i++)
			d_in_buf[i] = static_cast<gr_complexd>(in[i]);

		d_impl->calculate_pseudospectrum(&d_in_buf[0], d_nsamples, &d_out_buf[0], d_pspectrum_len);
		for(int i = 0; i < d_pspectrum_len; i++)
			out[i] = (float) d_out_buf[i];

		in += d_nsamples;
		out += d_pspectrum_len;
	}

	return noutput_items;
}

