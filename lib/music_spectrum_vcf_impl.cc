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
#include "music_spectrum_vcf_impl.h"
#ifdef ARMADILLO_FOUND 
#include <specest/music_armadillo_algo.h>
#else
#include <specest/music_fortran_algo.h>
#endif

namespace gr {
  namespace specest {

    music_spectrum_vcf::sptr
    music_spectrum_vcf::make(unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
    {
      return gnuradio::get_initial_sptr
        (new music_spectrum_vcf_impl(n, m, nsamples, pspectrum_len));
    }

#ifdef ARMADILLO_FOUND 
    /*
     * The private constructor, ARMADILLO
     */
    music_spectrum_vcf_impl::music_spectrum_vcf_impl(unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
	: gr::sync_block ("music_spectrum_vcf",
		gr::io_signature::make (1, 1, sizeof (gr_complex) * nsamples),
		gr::io_signature::make (1, 1, sizeof (float) * pspectrum_len)),
		d_m(m),
		d_n(n),
		d_nsamples(nsamples),
		d_pspectrum_len(pspectrum_len),
		d_algo(new music_armadillo_algo(n,m))
{
}
#else
    /*
     * The private constructor, FORTRAN
     */
    music_spectrum_vcf_impl::music_spectrum_vcf_impl(unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len)
	: gr::sync_block ("music_spectrum_vcf",
		gr::io_signature::make (1, 1, sizeof (gr_complex) * nsamples),
		gr::io_signature::make (1, 1, sizeof (float) * pspectrum_len)),
		d_m(m),
		d_n(n),
		d_nsamples(nsamples),
		d_pspectrum_len(pspectrum_len),
		d_algo(new music_fortran_algo(n,m))
{
}
#endif

    /*
     * Our virtual destructor.
     */
    music_spectrum_vcf_impl::~music_spectrum_vcf_impl()
    {
    	delete d_algo;
    }

    int
    music_spectrum_vcf_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
		const gr_complex *in = (const gr_complex *) input_items[0];
		gr_complexd* double_input = new gr_complexd[d_nsamples];
		for(int i = 0; i < d_nsamples; i++)
			double_input[i] = static_cast<gr_complexd>(in[i]);

		float* out = static_cast<float*> (output_items[0]);
		double* tmpout = new double[d_pspectrum_len];
		d_algo->calculate_pseudospectrum(double_input, d_nsamples, tmpout, d_pspectrum_len);
		for(int i = 0; i < d_pspectrum_len; i++)
			out[i] = (float) tmpout[i];

		delete[] double_input;
		delete[] tmpout;

		return 1;
    }

  } /* namespace specest */
} /* namespace gr */

