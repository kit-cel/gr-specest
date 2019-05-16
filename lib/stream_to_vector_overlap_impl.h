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

#ifndef INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_IMPL_H
#define INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_IMPL_H

#include <specest/stream_to_vector_overlap.h>

namespace gr {
namespace specest {

class stream_to_vector_overlap_impl : public stream_to_vector_overlap
{
private:
    int d_bytes_overlap;

public:
    stream_to_vector_overlap_impl(size_t item_size,
                                  size_t nitems_per_block,
                                  unsigned overlap);
    ~stream_to_vector_overlap_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
    unsigned overlap() { return history() - 1; };
};

} // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_IMPL_H */
