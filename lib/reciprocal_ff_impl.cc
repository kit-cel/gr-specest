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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "reciprocal_ff_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace specest {

reciprocal_ff::sptr reciprocal_ff::make(int vlen)
{
    return gnuradio::get_initial_sptr(new reciprocal_ff_impl(vlen));
}

reciprocal_ff_impl::reciprocal_ff_impl(int vlen)
    : gr::sync_block("reciprocal_ff",
                     gr::io_signature::make(1, 1, sizeof(float) * vlen),
                     gr::io_signature::make(1, 1, sizeof(float) * vlen)),
      d_vlen(vlen)
{
}

reciprocal_ff_impl::~reciprocal_ff_impl() {}

int reciprocal_ff_impl::work(int noutput_items,
                             gr_vector_const_void_star& input_items,
                             gr_vector_void_star& output_items)
{
    const float* in = (const float*)input_items[0];
    float* out = (float*)output_items[0];

    for (int i = 0; i < noutput_items * d_vlen; i++) {
        out[i] = 1.0 / in[i];
    }

    return noutput_items;
}

} /* namespace specest */
} /* namespace gr */
