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

#include "pad_vector_impl.h"
#include <gnuradio/io_signature.h>
#include <cstring>

namespace gr {
namespace specest {

pad_vector::sptr pad_vector::make(size_t item_size, unsigned vlen_in, unsigned vlen_out)
{
    return gnuradio::get_initial_sptr(new pad_vector_impl(item_size, vlen_in, vlen_out));
}

pad_vector_impl::pad_vector_impl(size_t item_size, unsigned vlen_in, unsigned vlen_out)
    : gr::sync_block("pad_vector",
                     gr::io_signature::make(1, 1, vlen_in * item_size),
                     gr::io_signature::make(1, 1, vlen_out * item_size))
{
    if (item_size, vlen_in < vlen_out) {
        d_copylen = vlen_in * item_size;
        d_padlen = (vlen_out - vlen_in) * item_size;
    } else {
        d_copylen = vlen_out * item_size;
        d_padlen = 0;
    }
}

pad_vector_impl::~pad_vector_impl() {}

int pad_vector_impl::work(int noutput_items,
                          gr_vector_const_void_star& input_items,
                          gr_vector_void_star& output_items)
{
    const char* in = (const char*)input_items[0];
    char* out = (char*)output_items[0];

    for (int i = 0; i < noutput_items; i++) {
        memcpy(out, in, d_copylen);
        memset(out + d_copylen, 0, d_padlen);
        in += d_copylen;
        out += d_copylen + d_padlen;
    }

    return noutput_items;
}

} /* namespace specest */
} /* namespace gr */
