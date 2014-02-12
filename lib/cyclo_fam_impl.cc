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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "cyclo_fam_impl.h"
#include <stdexcept>

namespace gr {
  namespace specest {
  
	inline int
	specest_round_to_even_impl(float x)
	{

	  return int(x) + int(x) % 2;

	}


	inline void
	specest_check_arguments_impl(int Np, int P, int decimation_factor)
	{
		if (!(Np % 2 == 0)) {
			throw  std::invalid_argument("specest_cyclo_fam: Np has to be a even number");
		}
		if (!(P % 2 == 0)) {
			throw std::invalid_argument("specest_cyclo_famh: P has to be a even number");
		}
		if (!(decimation_factor % 2 == 0)) {
			throw std::invalid_argument("speces_cyclo_fam: Decimation factor L has to be a even number");
		}

		//if (decimation_factor >> (Np/4)) {
		//	throw std::invalid_argument("specest_cyclo_fam: Decimation factor L must be smaller than Np/4");
		//}

		if ( Np >= P*decimation_factor) {
			throw std::invalid_argument("specest_cyclo_fam: N must be greater than Np");
		}

		//TODO check if N>>Np
	}


    cyclo_fam::sptr
    cyclo_fam::make(int Np, int P, int L)
    {
		specest_check_arguments_impl(Np,P,L);
		return gnuradio::get_initial_sptr (new cyclo_fam_impl (Np, P, L));
    }
    
    cyclo_fam::sptr
    cyclo_fam::make(float fs, float df, float dalpha, float q)
    {
		// Check if overlap is between 0.75..1
		if (!(0.75 <= q && q <= 1)) {
			throw std::invalid_argument("speces_cyclo_fam: overlap has to be between 0.75 and 1");
		}

		// Calculate Parameters Np, P, L
		int Np,P,L;

		Np = specest_round_to_even_impl(fs/df);
		float N = fs/dalpha;
		L = specest_round_to_even_impl(N*(1-q));

		// Ensure that L is at least the minimum value of 2
		if(L<2){ L = 2; }

		P = specest_round_to_even_impl(N/L);

		specest_check_arguments_impl(Np,P,L);

		// Return block with desired parametrization
      return gnuradio::get_initial_sptr (new cyclo_fam_impl (Np, P, L, fs));
    }
    /*
     * The private constructor
     */
    cyclo_fam_impl::cyclo_fam_impl(int Np, int P, int L)
      : gr::hier_block2("cyclo_fam",
		         gr::io_signature::make (1, 1, sizeof(gr_complex)),
		         gr::io_signature::make (1, 1, sizeof(float)*(2*Np))),
	 	d_stream_to_vector(gr::specest::stream_to_vector_overlap::make(sizeof(gr_complex), Np, Np-L)),
		d_Np_fft(gr::fft::fft_vcc::make(Np, true, gr::filter::firdes::window(gr::filter::firdes::WIN_HAMMING, Np, 0), false)),
		d_calcspectrum(gr::specest::cyclo_fam_calcspectrum_vcf::make(Np, P, L))
	{
		connect(self(), 0, d_stream_to_vector, 0);
		connect(d_stream_to_vector, 0, d_Np_fft, 0);
		connect(d_Np_fft, 0, d_calcspectrum, 0);
		connect(d_calcspectrum, 0, self(), 0);
	}
	
	cyclo_fam_impl::cyclo_fam_impl (int Np, int P, int L, float fs)
		: gr::hier_block2 ("cyclo_fam",
				     gr::io_signature::make (1, 1, sizeof(gr_complex)),
				     gr::io_signature::make (1, 1, sizeof(float)*(2*Np))),
	 	d_stream_to_vector(gr::specest::stream_to_vector_overlap::make(sizeof(gr_complex), Np, Np-L)),
		d_Np_fft(gr::fft::fft_vcc::make(Np, true, gr::filter::firdes::window(gr::filter::firdes::WIN_HAMMING, Np, 0), false)),
		d_calcspectrum(gr::specest::cyclo_fam_calcspectrum_vcf::make(Np, P, L))
	{
		d_fs = fs;

		//actual resolutions
		d_df = fs/Np;
		d_dalpha = fs/(P*L);

		//TODO are desired resolutions met?
		connect(self(), 0, d_stream_to_vector, 0);
		connect(d_stream_to_vector, 0, d_Np_fft, 0);
		connect(d_Np_fft, 0, d_calcspectrum, 0);
		connect(d_calcspectrum, 0, self(), 0);
	}

    /*
     * Our virtual destructor.
     */
    cyclo_fam_impl::~cyclo_fam_impl()
    {
    }


  } /* namespace specest */
} /* namespace gr */

