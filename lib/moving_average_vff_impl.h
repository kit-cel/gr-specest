/* -*- c++ -*- */
/* 
 * Copyright 2010,2013 Communications Engineering Lab, KIT
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

#ifndef INCLUDED_SPECEST_MOVING_AVERAGE_VFF_IMPL_H
#define INCLUDED_SPECEST_MOVING_AVERAGE_VFF_IMPL_H

#include <specest/moving_average_vff.h>

namespace gr {
  namespace specest {

    class moving_average_vff_impl : public moving_average_vff
    {
     private:
      int d_length;
      int d_vlen;
      float d_scale;
      int d_max_iter;

     public:
      moving_average_vff_impl(int length, int vlen, float scale, int max_iter);
      ~moving_average_vff_impl();

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_MOVING_AVERAGE_VFF_IMPL_H */

