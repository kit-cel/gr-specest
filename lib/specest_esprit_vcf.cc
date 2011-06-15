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
#include <specest_esprit_vcf.h>
#include <specesti_esprit_fortran.h>


specest_esprit_vcf_sptr
specest_make_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples)
{
	return specest_esprit_vcf_sptr (new specest_esprit_vcf (n, m, nsamples));
}


specest_esprit_vcf::specest_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples)
	: gr_sync_block ("esprit_vcf",
		gr_make_io_signature (1, 1, nsamples * sizeof (gr_complex)),
		gr_make_io_signature (1, 1, n * sizeof (float))),
	  d_n(n),
		d_m(m),
		d_nsamples(nsamples)
{
	d_impl = new specesti_esprit_fortran(n, m);
}

specest_esprit_vcf::~specest_esprit_vcf ()
{
	delete d_impl;
}

int 
specest_esprit_vcf::work (int noutput_items,
                          gr_vector_const_void_star &input_items,
                          gr_vector_void_star &output_items)
{
	const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
	gr_complexd* double_input = new gr_complexd[d_nsamples];
	for(int i = 0; i < d_nsamples; i++)
		double_input[i] = static_cast<gr_complexd>(in[i]);

	float* out = static_cast<float*> (output_items[0]);
	double* tmpout = new double[d_n];

	d_impl->calculate(double_input, d_nsamples, tmpout);

	for(int i = 0; i < d_n; i++)
		out[i] = float(tmpout[i]);

	delete[] double_input;
	delete[] tmpout;

	return 1;
}

