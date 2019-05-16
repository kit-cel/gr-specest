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

#include "stream_to_vector_overlap_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace specest {

stream_to_vector_overlap::sptr stream_to_vector_overlap::make(size_t item_size,
                                                              size_t nitems_per_block,
                                                              unsigned overlap)
{
    return gnuradio::get_initial_sptr(
        new stream_to_vector_overlap_impl(item_size, nitems_per_block, overlap));
}

stream_to_vector_overlap_impl::stream_to_vector_overlap_impl(size_t item_size,
                                                             size_t nitems_per_block,
                                                             unsigned overlap)
    : gr::sync_decimator("stream_to_vector_overlap",
                         gr::io_signature::make(1, 1, item_size),
                         gr::io_signature::make(1, 1, item_size * nitems_per_block),
                         nitems_per_block - overlap),
      d_bytes_overlap(overlap * item_size)
{
    if (overlap + 1 >= nitems_per_block) {
        throw std::invalid_argument("specest_stream_to_vector_overlap: overlap must be "
                                    "smaller than the number of items per block.");
    }
    set_history(overlap + 1);
}

stream_to_vector_overlap_impl::~stream_to_vector_overlap_impl() {}

int stream_to_vector_overlap_impl::work(int noutput_items,
                                        gr_vector_const_void_star& input_items,
                                        gr_vector_void_star& output_items)
{
    size_t block_size = output_signature()->sizeof_stream_item(0);
    char* in = (char*)input_items[0];
    char* out = (char*)output_items[0];

    for (int i = 0; i < noutput_items; i++) {
        memcpy(out, in, block_size);
        out += block_size;
        in += block_size - d_bytes_overlap;
    }

    return noutput_items;
}

} /* namespace specest */
} /* namespace gr */
