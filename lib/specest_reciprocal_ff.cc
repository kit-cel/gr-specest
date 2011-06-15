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

#include <specest_reciprocal_ff.h>
#include <gr_io_signature.h>


specest_reciprocal_ff_sptr
specest_make_reciprocal_ff (int vlen)
{
	return specest_reciprocal_ff_sptr (new specest_reciprocal_ff (vlen));
}


specest_reciprocal_ff::specest_reciprocal_ff (int vlen)
	: gr_sync_block ("reciprocal_ff",
			gr_make_io_signature (1, 1, vlen * sizeof(float)),
			gr_make_io_signature (1, 1, vlen * sizeof(float))),
	d_vlen(vlen)
{
}


int
specest_reciprocal_ff::work (int noutput_items,
		gr_vector_const_void_star &input_items,
		gr_vector_void_star &output_items)
{
	const float *in = (const float *) input_items[0];
	float *out = (float *) output_items[0];

	for (int i = 0; i < noutput_items * d_vlen; i++) {
		out[i] = 1.0/in[i];
	}

	return noutput_items;
}

