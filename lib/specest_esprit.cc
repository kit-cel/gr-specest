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
#include <specest_esprit.h>


specest_esprit_sptr
specest_make_esprit (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation)
{
	return gnuradio::get_initial_sptr (new specest_esprit (n, m, nsamples, pspectrum_len, decimation));
}


specest_esprit::specest_esprit (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation)
	: gr_hier_block2 ("esprit",
		gr_make_io_signature (1, 1, sizeof (gr_complex)),
		gr_make_io_signature (1, 1, pspectrum_len * sizeof (float))),
		d_decimation(decimation),
		d_s2v(gr_make_stream_to_vector(sizeof(gr_complex),nsamples)),
		d_decimate(gr_make_keep_one_in_n(nsamples * sizeof(gr_complex), decimation)),
		d_esprit(specest_make_esprit_spectrum_vcf(n,m,nsamples,pspectrum_len))

{
	connect(self(), 0, d_s2v, 0);
	connect(d_s2v, 0, d_decimate, 0);
	connect(d_decimate, 0, d_esprit, 0);
	connect(d_esprit, 0, self(), 0);
}


specest_esprit::~specest_esprit ()
{
}

unsigned int
specest_esprit::decimation()
{
	return d_decimation;
}

void
specest_esprit::set_decimation(unsigned int n)
{
	d_decimate->set_n(n);
	d_decimation = n;
}
