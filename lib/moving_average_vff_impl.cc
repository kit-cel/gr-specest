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

#include "moving_average_vff_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace specest {

moving_average_vff::sptr
moving_average_vff::make(int length, int vlen, float scale, int max_iter)
{
    return gnuradio::get_initial_sptr(
        new moving_average_vff_impl(length, vlen, scale, max_iter));
}

moving_average_vff_impl::moving_average_vff_impl(int length,
                                                 int vlen,
                                                 float scale,
                                                 int max_iter)
    : gr::sync_block("moving_average_vff",
                     gr::io_signature::make(1, 1, sizeof(float) * vlen),
                     gr::io_signature::make(1, 1, sizeof(float) * vlen)),
      d_length(length),
      d_vlen(vlen),
      d_scale(scale),
      d_max_iter(max_iter)
{
    set_history(length);
}

moving_average_vff_impl::~moving_average_vff_impl() {}

int moving_average_vff_impl::work(int noutput_items,
                                  gr_vector_const_void_star& input_items,
                                  gr_vector_void_star& output_items)
{
    const float* in = (const float*)input_items[0];
    float* out = (float*)output_items[0];

    std::vector<float> sum(d_vlen, 0);
    int num_iter = (noutput_items > d_max_iter) ? d_max_iter : noutput_items;

    for (int i = 0; i < d_length - 1; i++) {
        const float* in_vec = &in[i * d_vlen];
        for (int k = 0; k < d_vlen; k++) {
            sum[k] += in_vec[k];
        }
    }

    for (int i = 0; i < num_iter; i++) {
        const float* in_vec_old = &in[i * d_vlen];
        const float* in_vec_new = &in[(i + d_length - 1) * d_vlen];
        float* out_vec = &out[i * d_vlen];
        for (int k = 0; k < d_vlen; k++) {
            sum[k] += in_vec_new[k];
            out_vec[k] = sum[k] * d_scale;
            sum[k] -= in_vec_old[k];
        }
    }

    return num_iter;
}

} /* namespace specest */
} /* namespace gr */
