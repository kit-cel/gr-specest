/* -*- c++ -*- */
/*
 * Copyright 2004,2005 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdexcept>
#include <cstring>
#include <gr_io_signature.h>
#include <specest_stream_to_vector_overlap.h>

specest_stream_to_vector_overlap_sptr
specest_make_stream_to_vector_overlap (size_t item_size, size_t nitems_per_block, unsigned overlap)
{
  return specest_stream_to_vector_overlap_sptr (new specest_stream_to_vector_overlap (item_size, nitems_per_block, overlap));
}

specest_stream_to_vector_overlap::specest_stream_to_vector_overlap (size_t item_size, size_t nitems_per_block, unsigned overlap)
  : gr_sync_decimator ("stream_to_vector_overlap",
		       gr_make_io_signature (1, 1, item_size),
		       gr_make_io_signature (1, 1, item_size * nitems_per_block),
		       nitems_per_block - overlap),
	d_bytes_overlap(overlap * item_size)
{
	if (overlap + 1 >= nitems_per_block) {
		throw std::invalid_argument("specest_stream_to_vector_overlap: overlap must be smaller than the number of items per block.");
	}
	set_history(overlap + 1);
}

int
specest_stream_to_vector_overlap::work (int noutput_items,
			     gr_vector_const_void_star &input_items,
			     gr_vector_void_star &output_items)
{
  size_t block_size = output_signature()->sizeof_stream_item (0);

  char *in = (char *) input_items[0];
  char *out = (char *) output_items[0];

  for (int i = 0; i < noutput_items; i++) {
	  memcpy(out, in, block_size);
	  out += block_size;
	  in += block_size - d_bytes_overlap;
  }

  return noutput_items;
}

