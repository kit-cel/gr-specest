/* -*- c++ -*- */
/*
 * Copyright 2004,2006 Free Software Foundation, Inc.
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

#ifndef INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_H
#define INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_H

#include <gr_sync_decimator.h>

class specest_stream_to_vector_overlap;
typedef boost::shared_ptr<specest_stream_to_vector_overlap> specest_stream_to_vector_overlap_sptr;

specest_stream_to_vector_overlap_sptr
specest_make_stream_to_vector_overlap (size_t item_size, size_t nitems_per_block, unsigned overlap);


/*!
 * \brief Convert a stream of items into a stream of overlapping blocks containing nitems_per_block.
 *
 * The i-th block will start with the same \p overlap items as the i-1-th block ended. The first
 * block is prepended with \p overlap zeros to ensure synchronicity.
 * \ingroup converter
 */
class specest_stream_to_vector_overlap : public gr_sync_decimator
{
  friend specest_stream_to_vector_overlap_sptr
    specest_make_stream_to_vector_overlap (size_t item_size, size_t nitems_per_block, unsigned overlap);

 protected:
  specest_stream_to_vector_overlap (size_t item_size, size_t nitems_per_block, unsigned overlap);

  int d_bytes_overlap;

 public:
  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);

  unsigned overlap() { return history() - 1; };
};


#endif /* INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_H */

