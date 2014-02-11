/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_SPECEST_ESPRIT_SPECTRUM_VCF_IMPL_H
#define INCLUDED_SPECEST_ESPRIT_SPECTRUM_VCF_IMPL_H

#include <specest/esprit_spectrum_vcf.h>
#include <specest/esprit_algo.h>

namespace gr {
  namespace specest {

    class esprit_spectrum_vcf_impl : public esprit_spectrum_vcf
    {
     private:
		esprit_algo* d_algo;
		unsigned int d_n;
		unsigned int d_m;
		unsigned int d_nsamples;
		unsigned int d_pspectrum_len;

		std::vector<gr_complexd> d_in_buf;
		std::vector<double> d_out_buf;
     public:
      esprit_spectrum_vcf_impl(unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len);
      ~esprit_spectrum_vcf_impl();

      // Where all the action really happens
      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_ESPRIT_SPECTRUM_VCF_IMPL_H */

