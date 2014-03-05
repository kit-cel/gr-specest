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

#ifndef INCLUDED_SPECEST_MUSIC_IMPL_H
#define INCLUDED_SPECEST_MUSIC_IMPL_H

#include <specest/music.h>
#include <gnuradio/blocks/stream_to_vector.h>
#include <gnuradio/blocks/keep_one_in_n.h>
#include <specest/music_spectrum_vcf.h>

namespace gr {
  namespace specest {

    class music_impl : public music
    {
     private:
		gr::blocks::stream_to_vector::sptr d_s2v;
		gr::blocks::keep_one_in_n::sptr d_decimate;
		gr::specest::music_spectrum_vcf::sptr d_music;
		unsigned int d_decimation;

     public:
      music_impl(unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);
      ~music_impl();

      unsigned int decimation();
	  void set_decimation(unsigned int n);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_MUSIC_IMPL_H */

