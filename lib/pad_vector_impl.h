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

#ifndef INCLUDED_SPECEST_PAD_VECTOR_IMPL_H
#define INCLUDED_SPECEST_PAD_VECTOR_IMPL_H

#include <specest/pad_vector.h>

namespace gr {
namespace specest {

class pad_vector_impl : public pad_vector
{
private:
    unsigned d_copylen;
    unsigned d_padlen;
    unsigned d_vlen_in;
    unsigned d_vlen_out;

public:
    pad_vector_impl(size_t item_size, unsigned vlen_in, unsigned vlen_out);
    ~pad_vector_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_PAD_VECTOR_IMPL_H */
