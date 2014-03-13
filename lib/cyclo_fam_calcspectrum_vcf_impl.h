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

#ifndef INCLUDED_SPECEST_CYCLO_FAM_CALCSPECTRUM_VCF_IMPL_H
#define INCLUDED_SPECEST_CYCLO_FAM_CALCSPECTRUM_VCF_IMPL_H

#include <specest/cyclo_fam_calcspectrum_vcf.h>
#include <specest/cyclo_fam_calcspectrum_algo.h>

namespace gr {
  namespace specest {

    class cyclo_fam_calcspectrum_vcf_impl : public cyclo_fam_calcspectrum_vcf
    {
     private:
		cyclo_fam_calcspectrum_algo *d_calcspectrum;

		int      d_Np;
		int      d_P;
		int      d_N;
		int      d_L;
		unsigned d_p_index;
		int      d_K;            // Interpolation Factor

		float const *d_outbuffer;

     public:
      cyclo_fam_calcspectrum_vcf_impl(int Np, int P, int L);
      ~cyclo_fam_calcspectrum_vcf_impl();

      // Where all the action really happens
      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);

	  int get_Np(){ return d_Np; };
	  int get_N(){ return d_N; };
	  int get_P(){ return d_P; };
      int get_L(){ return d_L; };
      const std::vector<std::vector<float> > &get_estimate(){return d_calcspectrum->get_outputs();};
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_CYCLO_FAM_CALCSPECTRUM_VCF_IMPL_H */

