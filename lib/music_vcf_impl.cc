/* -*- c++ -*- */
/*
 * Copyright 2014 Communications Engineering Lab, KIT
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

#include <gnuradio/io_signature.h>
#include "music_vcf_impl.h"
#include <specest/music_armadillo_algo.h>

namespace gr {
  namespace specest {

    music_vcf::sptr
    music_vcf::make(unsigned int n, unsigned int m, unsigned int nsamples)
    {
      return gnuradio::get_initial_sptr
        (new music_vcf_impl(n, m, nsamples));
    }

    /*
     * The private constructor
     */
    music_vcf_impl::music_vcf_impl(unsigned int n, unsigned int m, unsigned int nsamples)
      : gr::sync_block("music_vcf",
			gr::io_signature::make (1, 1, nsamples * sizeof (gr_complex)),
			gr::io_signature::make (1, 1, n * sizeof (float))),
	  	d_n(n),
		d_m(m),
		d_nsamples(nsamples),
		d_algo(new music_armadillo_algo(n, m))
    {}

    /*
     * Our virtual destructor.
     */
    music_vcf_impl::~music_vcf_impl()
    {
    }

    int
    music_vcf_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
		const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
		gr_complexd* double_input = new gr_complexd[d_nsamples];
		for(int i = 0; i < d_nsamples; i++)
			double_input[i] = static_cast<gr_complexd>(in[i]);
		//double* out = (double *) output_items[0];
		float* out = static_cast<float*> (output_items[0]);
		double* tmpout = new double[d_n];
		d_algo->calculate(double_input, d_nsamples, tmpout);
		for(int i = 0; i < d_n; i++)
			out[i] = float(tmpout[i]);

		delete[] double_input;
		delete[] tmpout;

		// Tell runtime system how many output items we produced.
		//return noutput_items;
		return 1;
    }

  } /* namespace specest */
} /* namespace gr */

