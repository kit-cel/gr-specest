/* -*- c++ -*- */
/*
 * Copyright 2008 Free Software Foundation, Inc.
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

// WARNING: this file is machine generated.  Edits will be over written

#ifndef INCLUDED_SPECEST_MOVING_AVERAGE_VFF_H
#define INCLUDED_SPECEST_MOVING_AVERAGE_VFF_H

#include <gr_sync_block.h>

class specest_moving_average_vff;

typedef boost::shared_ptr<specest_moving_average_vff> specest_moving_average_vff_sptr;

specest_moving_average_vff_sptr specest_make_moving_average_vff (int length, int vlen, float scale, int max_iter = 4096);

/*!
 * \brief output is the moving sum of the last N samples, scaled by the \p scale factor.
 *
 * The moving average of the vectors is calculated per element.
 *
 * \p max_iter limits how long we go without flushing the accumulator. This is necessary
 * to avoid numerical instability for float and complex.
 *
 * \ingroup filter
 */
class specest_moving_average_vff : public gr_sync_block
{
private:
  friend specest_moving_average_vff_sptr specest_make_moving_average_vff(int length, int vlen, float scale, int max_iter);

  specest_moving_average_vff (int length, int vlen, float scale, int max_iter = 4096);

  int d_length;
  int d_vlen;
  float d_scale;
  int d_max_iter;

public:
  ~specest_moving_average_vff ();

  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_SPECEST_MOVING_AVERAGE_VFF_H */

