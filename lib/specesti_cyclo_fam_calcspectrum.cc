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

#include <cmath>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <specesti_cyclo_fam_calcspectrum.h>

specesti_cyclo_fam_calcspectrum::specesti_cyclo_fam_calcspectrum(int Np, int P, int L) :
    d_Np(Np),
    d_P(P),
    d_L(L),
    d_N(P * L),
	d_result(2*d_N, std::vector<float>(2*d_Np-1,0)),
	d_complex_demodulates(P, std::vector<gr_complex>(Np,0)),
	d_fft_in_buffer(P)
	
{
    // Calculate scaling factor
    std::vector<float> window = gr_firdes::window(gr_firdes::WIN_HAMMING, d_Np, 0);
    std::vector<float>::size_type sz = window.size();

    float h = 0;
    for (int i=0; i < sz; i++)
		h += window[i]*window[i];
    d_scale = h*d_P;

    // Prepare FFT-Buffers
    d_fft_out       = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex) * P);
    d_fft_in        = reinterpret_cast<fftwf_complex*>(&d_fft_in_buffer[0]);
    d_fft_p         = fftwf_plan_dft_1d(d_P, d_fft_in, d_fft_out, FFTW_FORWARD, FFTW_ESTIMATE);

}


specesti_cyclo_fam_calcspectrum::~specesti_cyclo_fam_calcspectrum()
{
    fftwf_destroy_plan(d_fft_p);
    fftwf_free(d_fft_out);

}

void specesti_cyclo_fam_calcspectrum::fft(int f_k, int f_l)
{
    // Prepare FFT
    // Copy vector to FFT-buffer
    for(int p = 0; p < d_P; p++) {
        d_fft_in_buffer[p] = d_complex_demodulates[p][f_k-1]*std::conj(d_complex_demodulates[p][f_l-1])/d_scale;
    }

    fftwf_execute(d_fft_p);

    // Rearange, scale, get absolute value & copy result to output stream
    
    int column = (f_k+f_l-2); 
    int row    = (f_k-f_l+d_Np)*(d_N/d_Np); // d_N/d_Np is intended (=floor(d_N/d_Np)) 
    
    // Top of the channel support region
    for(int i = 0; i < d_N/d_Np; i++) {
        d_result[row+i][column]     = std::sqrt(d_fft_out[i][0]*d_fft_out[i][0]+d_fft_out[i][1]*d_fft_out[i][1]);
    }
    // Bottom of the channel support region
    for(int i = 1; i <= d_N/d_Np; i++) {
        d_result[row-i][column]     = std::sqrt(d_fft_out[d_P-i][0]*d_fft_out[d_P-i][0]+d_fft_out[d_P-i][1]*d_fft_out[d_P-i][1]);
    }
}


void specesti_cyclo_fam_calcspectrum::calc(const gr_complex *in)
{
     int p = 0;
     int i = 0;

     // Copy input stream to d_complex_demodulates and do the phase shifting
     for(int m = 0; m < d_P*d_Np; m++) {
        d_complex_demodulates[p][i].real() = in[m].real()*cos(2*M_PI*i*(p*d_L)/d_Np)+
                                             in[m].imag()*sin(2*M_PI*i*(p*d_L)/d_Np);
        d_complex_demodulates[p][i].imag() = in[m].imag()*cos(2*M_PI*i*(p*d_L)/d_Np)-
                                             in[m].real()*sin(2*M_PI*i*(p*d_L)/d_Np);
        i++;

        if((m+1)%d_Np==0){ // End of vector length Np
            p++;
            i = 0;
        }
    }

    // FFT-Shift
    int half = d_Np/2;
    for (int k = 0 ; k < d_P ; k++){
		std::complex<float> * start_ptr = &d_complex_demodulates[k][0];
		std::complex<float> * swap_buffer = new std::complex<float>[half];

		memcpy(swap_buffer, start_ptr, half * sizeof(std::complex<float>));
		memcpy(start_ptr,  start_ptr + half, half * sizeof(std::complex<float>));
		memcpy(start_ptr + half, swap_buffer, half * sizeof(std::complex<float>));

		delete [] swap_buffer;
    }

    /*for (p=0;p<d_P;p++){ // Seems not to work for some reasons
        gr_complex * start = &d_complex_demodulates[p][0];
        gr_complex * mid   = &d_complex_demodulates[p][0] + d_P/2;
        gr_complex * end   = &d_complex_demodulates[p][0] + d_P;

        std::rotate(start, mid, end);
    }*/

    // Correlate Spectrum
    int f_k;
    int f_l;

    for (f_k = 1; f_k <= d_Np; f_k++) {
        for(f_l = 1; f_l <= d_Np; f_l++) {
            fft(f_k, f_l);
        }
    }
}

