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

#ifndef INCLUDED_SPECEST_RECIPROCAL_FF_H
#define INCLUDED_SPECEST_RECIPROCAL_FF_H

#include <gr_sync_block.h>
#include <specest_reciprocal_ff.h>


class specest_reciprocal_ff;
typedef boost::shared_ptr<specest_reciprocal_ff> specest_reciprocal_ff_sptr;

specest_reciprocal_ff_sptr
specest_make_reciprocal_ff (int vlen = 1);


/*!
 * \brief Calculate the reciprocal of the input (y = 1/x)
 *
 * \ingroup specest
 */
class specest_reciprocal_ff : public gr_sync_block
{
	friend specest_reciprocal_ff_sptr specest_make_reciprocal_ff (int vlen);

	specest_reciprocal_ff (int vlen);

	int d_vlen;

 public:
	~specest_reciprocal_ff () {};

	int work (int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items);
};


#endif /* INCLUDED_SPECEST_RECIPROCAL_FF_H */

