/* -*- c++ -*- */
/* 
 * Copyright 2011 Communications Engineering Lab, KIT
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

#ifndef INCLUDED_SPECEST_MUSIC_H
#define INCLUDED_SPECEST_MUSIC_H

#include <gr_hier_block2.h>
#include <gr_stream_to_vector.h>
#include <gr_keep_one_in_n.h>
#include <specest_music_spectrum_vcf.h>

class specest_music;
typedef boost::shared_ptr<specest_music> specest_music_sptr;

specest_music_sptr specest_make_music (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);

/*!
 * \brief Convenience class to generate the MUSIC pseudospectrum
 *
 * The Estimator works on complex samples, if \p decimation is not set
 * it will attempt to work on the full samplerate. However if \p decimation is set
 * to anything else than one, it will throw away vectors of samples of length 
 * \p nsamples to win some time for calculation.
 *
 * \ingroup specest
 *
 */
class specest_music : public gr_hier_block2
{
	friend specest_music_sptr specest_make_music (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);

	/*!
	 * \param n How many sinusoids does your model have?
	 * \param m use a correlation matrix of dimension m x m
	 * \param nsamples use \p nsamples to get an estimate of the correlation matrix
	 * \param pspectrum_len length of the generated pseudospectrum
	 * \param decimation process only one in \p decimation vectors of length \p nsamples. Can be used to win some time for calculations.
	 */
	specest_music (unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len, unsigned int decimation);

 public:
	~specest_music ();
	unsigned int decimation();
	void set_decimation(unsigned int n);
 private:
	gr_stream_to_vector_sptr d_s2v;
	gr_keep_one_in_n_sptr d_decimate;
	specest_music_spectrum_vcf_sptr d_music;
	unsigned int d_decimation;
};

#endif /* INCLUDED_SPECEST_MUSIC_H */

