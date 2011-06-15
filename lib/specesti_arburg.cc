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

#include <specesti_arburg.h>
#include <stdexcept>
#include <cstring>


inline double
mag_square(gr_complexd c)
{
	return c.real()*c.real() + c.imag()*c.imag();
}


specesti_arburg::specesti_arburg(unsigned blocklen, unsigned order)
	: d_blocklen(blocklen), d_order(order)
{
	if (order > blocklen) {
		throw std::invalid_argument("specesti_arburg: order cannot exceed block length.");
	}
	if(!blocklen || !order) {
		throw std::invalid_argument("specesti_arburg: block length and order must be at least 1.");
	}

	d_ef = new gr_complexd[d_blocklen];
	d_eb = new gr_complexd[d_blocklen];
	d_efp = new gr_complexd[d_blocklen];	
	d_arcoeff = new gr_complexd[d_order+1];	
	d_arcoeff2 = new gr_complexd[d_order+1];
}


specesti_arburg::~specesti_arburg()
{
	delete[] d_ef;
	delete[] d_eb;
	delete[] d_efp;
	delete[] d_arcoeff;
	delete[] d_arcoeff2;
}


void
specesti_arburg::set_order(unsigned order)
{
	d_order = order;
	delete[] d_arcoeff;
	delete[] d_arcoeff2;
	d_arcoeff = new gr_complexd[d_order+1];	
	d_arcoeff2 = new gr_complexd[d_order+1];
}


void
specesti_arburg::set_blocklen(unsigned blocklen)
{
	d_blocklen = blocklen;
	delete[] d_ef;
	delete[] d_eb;
	delete[] d_efp;
	d_ef = new gr_complexd[d_blocklen];
	d_eb = new gr_complexd[d_blocklen];
	d_efp = new gr_complexd[d_blocklen];	
}


void
specesti_arburg::init_buffers(const gr_complex *data, double &var)
{
	var = 0;

	for(unsigned i = 0; i < d_blocklen; i++) {
		d_ef[i] = d_eb[i] = gr_complexd(data[i]);
		var += mag_square(data[i]);
	}
}


// The variable names in this function follow those in "Spectral analysis of signals",
// P. Stoica and R. Moses, Chapter 3.9.3.
float
specesti_arburg::calculate(const gr_complex *data, gr_complex *ar_coeff, int normalise)
{
	double var;
	gr_complexd k;
	init_buffers(data, var);

	d_arcoeff[0] = 1;
	for(unsigned p = 0; p < d_order; p++) {
		k = calc_k(p);

		for(unsigned t = 0; t < d_blocklen-p-1; t++) {
			d_efp[t] = d_ef[t+1] + k * d_eb[t];
			d_eb[t] = d_eb[t] + conj(k) * d_ef[t+1];
			d_ef[t] = d_efp[t];
		}
		var *= (1 - mag_square(k));

		memcpy(d_arcoeff2+1, d_arcoeff+1, sizeof(gr_complexd) * p);
		for(unsigned r = 1; r <= p; r++)
			d_arcoeff[r] += conj(d_arcoeff2[p+1-r]) * k;
		d_arcoeff[p+1] = k;
	}
	var = var/d_blocklen;

	// Copy to output buffer
	if (normalise) {
		gr_complexd norm = (gr_complexd) (sqrt(var/ normalise));
		for(unsigned p = 0; p < d_order+1; p++)
			ar_coeff[p] = gr_complex((d_arcoeff[p]) / norm);
	} else {
		for(unsigned p = 0; p < d_order+1; p++) {
			ar_coeff[p] = gr_complex(d_arcoeff[p]);
		}
	}

	return (float) var;
}


// Calculates \hat{k}_p (the p-th PARCOR coefficient)
gr_complexd
specesti_arburg::calc_k(int p)
{
	gr_complexd k_num = 0;
	gr_complexd k_den = 0;

	for(unsigned t = 1; t < d_blocklen-p; t++) {
		k_num += d_ef[t] * conj(d_eb[t-1]);
		k_den += d_ef[t] * conj(d_ef[t]) + d_eb[t-1] * conj(d_eb[t-1]);
	}

	return -2.0 * k_num / k_den;
}

