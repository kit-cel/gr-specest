/* -*- c++ -*- */
/* 
 * Copyright 2010 Communications Engineering Lab, KIT
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
#ifndef INCLUDED_SPECESTI_MUSIC_H
#define INCLUDED_SPECESTI_MUSIC_H

#include <gr_complex.h>

class specesti_music
{
	public:
		/*!
		 * \brief Calculate the estimates for the frequencies normalised to [-pi,pi]
		 * \param data complex samples / input data
		 * \param data_len size of the complex sample array we're working on
		 * \param omegas estimated frequencies
		 */
		virtual void calculate(const gr_complexd *data, unsigned int data_len,
		                       double* omegas) = 0;
		/*!
		 * \brief Calculate the pseudospectrum normalized to [-pi,pi]
		 * \param data complex samples / input data
		 * \param data_len size of the complex sample array we're working on
		 * \param pspectrum the resulting pseudospectrum will end up here
		 * \param pspectrum_len size of the pseudopectrum output we're looking for
		 */
		virtual void calculate_pseudospectrum(const gr_complexd* data, unsigned int data_len,
		                                      double* pspectrum, unsigned int pspectrum_len) = 0;
};

#endif /* INCLUDED_SPECESTI_MUSIC_H */
