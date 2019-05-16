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

#include "arburg_vcc_impl.h"
#include <gnuradio/io_signature.h>
#include <cstring>

namespace gr {
namespace specest {

arburg_vcc::sptr arburg_vcc::make(unsigned blocklen, unsigned order, int normalise)
{
    return gnuradio::get_initial_sptr(new arburg_vcc_impl(blocklen, order, normalise));
}

arburg_vcc_impl::arburg_vcc_impl(unsigned blocklen, unsigned order, int normalise)
    : gr::sync_block(
          "arburg_vcc",
          gr::io_signature::make(1, 1, blocklen * sizeof(gr_complex)),
          gr::io_signature::make2(1, 2, (order + 1) * sizeof(gr_complex), sizeof(float))),
      d_blocklen(blocklen),
      d_order(order),
      d_normalise(normalise)
{
    // TODO catch?
    d_burg = new arburg_algo(blocklen, order);
}

arburg_vcc_impl::~arburg_vcc_impl()
{
    // TODO sptr
    delete d_burg;
}

int arburg_vcc_impl::work(int noutput_items,
                          gr_vector_const_void_star& input_items,
                          gr_vector_void_star& output_items)
{
    const gr_complex* in = (const gr_complex*)input_items[0];
    gr_complex* out_coeff = (gr_complex*)output_items[0];
    float* out_var;
    float var;
    int normalise;
    bool export_var = false;

    if (output_items.size() == 2) {
        export_var = true;
        out_var = (float*)output_items[1];
    }
    if (d_normalise == -1) {
        normalise = (output_items.size() == 1);
    } else {
        normalise = d_normalise;
    }

    for (int i = 0; i < noutput_items; i++) {
        var = d_burg->calculate(in, out_coeff, normalise);
        if (export_var) {
            out_var[i] = var;
        }
        out_coeff += d_order + 1;
        in += d_blocklen;
    }

    return noutput_items;
}

} /* namespace specest */
} /* namespace gr */
