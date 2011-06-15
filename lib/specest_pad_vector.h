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

#ifndef INCLUDED_SPECEST_PAD_VECTOR_H
#define INCLUDED_SPECEST_PAD_VECTOR_H

#include <gr_sync_block.h>

class specest_pad_vector;
typedef boost::shared_ptr<specest_pad_vector> specest_pad_vector_sptr;

specest_pad_vector_sptr
specest_make_pad_vector (size_t item_size, unsigned vlen_in, unsigned vlen_out);

/*!
 * \brief Increases or decreases the length of vectors.
 *
 * If the output length is smaller than the input length, vectors will be truncated.
 * Otherwise, vectors will be zero-padded.
 *
 * \ingroup specest
 */
class specest_pad_vector : public gr_sync_block
{
	friend specest_pad_vector_sptr specest_make_pad_vector (size_t item_size, unsigned vlen_in, unsigned vlen_out);

	unsigned  d_copylen;
	unsigned  d_padlen;
	unsigned  d_vlen_in;
	unsigned  d_vlen_out;

	specest_pad_vector (size_t item_size, unsigned vlen_in, unsigned vlen_out);

 public:
	~specest_pad_vector () {};
	int work (int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items);
};

#endif /* INCLUDED_SPECEST_PAD_VECTOR_H */

