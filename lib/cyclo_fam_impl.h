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

#ifndef INCLUDED_SPECEST_CYCLO_FAM_IMPL_H
#define INCLUDED_SPECEST_CYCLO_FAM_IMPL_H

#include <specest/cyclo_fam.h>
#include <specest/cyclo_fam_calcspectrum_vcf.h>
#include <specest/stream_to_vector_overlap.h>
#include <gnuradio/fft/fft_vcc.h>
#include <gnuradio/filter/firdes.h>

namespace gr {
  namespace specest {

    class cyclo_fam_impl : public cyclo_fam
    {
     private:
		//Blocks
		gr::specest::stream_to_vector_overlap::sptr d_stream_to_vector;
		gr::fft::fft_vcc::sptr                              d_Np_fft;
		gr::specest::cyclo_fam_calcspectrum_vcf::sptr      d_calcspectrum;

		float d_fs;
		float d_df;
		float d_dalpha;

     public:
      cyclo_fam_impl(int Np, int P, int decimation_factor);
      cyclo_fam_impl(int Np, int P, int decimation_factor, float fs);
      ~cyclo_fam_impl();

	  int get_Np() { return d_calcspectrum->get_Np(); };
	  int get_N() { return d_calcspectrum->get_N(); };
      int get_P() { return d_calcspectrum->get_P(); };
      int get_L() { return d_calcspectrum->get_L(); };

	  float get_sample_frequency() { return d_fs; };
      float get_frequency_resolution()  { return d_df; };
      float get_cycle_frequency_resolution() { return d_dalpha; };
	/**
	* Direct access to the estimate. Note: Estimate is a 2-dim array of size 2N x (2Np-1).
	*/
	  const std::vector<std::vector<float> > &get_estimate() { return d_calcspectrum->get_estimate(); };
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_CYCLO_FAM_IMPL_H */

