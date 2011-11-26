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

#ifndef INCLUDED_SPECESTI_CYCLO_FAM_CALCSPECTRUM_H
#define INCLUDED_SPECESTI_CYCLO_FAM_CALCSPECTRUM_H

#include <complex>
#include <fftw3.h>
#include <gr_complex.h>
#include <gr_firdes.h>

class specesti_cyclo_fam_calcspectrum
{
 public:
	specesti_cyclo_fam_calcspectrum(int Np, int P, int L);
	~specesti_cyclo_fam_calcspectrum();
	void calc(const gr_complex *in);
	const std::vector<std::vector<float> >  &get_outputs() { return d_result; };
	float get_value(int row, int column){ return d_result[row][column]; };

 private:
	int d_Np;
	int d_P;
	int d_L;
	int d_N;

	float d_scale;

	std::vector<std::vector<gr_complex> >  d_complex_demodulates;
	std::vector<std::vector<float> >       d_result;

	std::vector<gr_complex>  d_fft_in_buffer;
	fftwf_complex           *d_fft_in;
	fftwf_complex           *d_fft_out;
	fftwf_plan               d_fft_p;

	void fft(int f_k, int f_l);

};

#endif /* INCLUDED_SPECESTI_CYCLO_FAM_CALCSPECTRUM_H */

