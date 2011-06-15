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

#include <specesti_arfmcov.h>
#include <stdexcept>
#include <cstring>


specesti_arfmcov::specesti_arfmcov(unsigned blocklen, unsigned order)
	: d_blocklen(blocklen), d_order(order),
	d_a(order+1, gr_complexd(0, 0)),
	d_ai(order+1, gr_complexd(0, 0)),
	d_c(order+1, gr_complexd(0, 0)),
	d_d(order+1, gr_complexd(0, 0)),
	d_ci(order+1, gr_complexd(0, 0)),
	d_di(order+1, gr_complexd(0, 0)),
	d_r(order, gr_complexd(0, 0))
{
	if (order > blocklen) {
		throw std::invalid_argument("specesti_arfmcov: order cannot exceed block length.");
	}
	if(!blocklen || !order) {
		throw std::invalid_argument ("specesti_arfmcov: block length and order must be at least 1.");
	}
}


specesti_arfmcov::~specesti_arfmcov()
{
}


void
specesti_arfmcov::set_order(unsigned order)
{
	d_order = order;
	d_a.resize(order+1);
	d_ai.resize(order+1);
	d_c.resize(order+1);
	d_d.resize(order+1);
	d_ci.resize(order+1);
	d_di.resize(order+1);
	d_r.resize(order);
}


void
specesti_arfmcov::set_blocklen(unsigned blocklen)
{
	d_blocklen = blocklen;
}


void
specesti_arfmcov::init_buffers()
{
	d_a.assign(d_order+1, 0.0);
	d_ai.assign(d_order+1, 0.0);
	d_c.assign(d_order+1, 0.0);
	d_d.assign(d_order+1, 0.0);
	d_ci.assign(d_order+1, 0.0);
	d_di.assign(d_order+1, 0.0);
	d_r.assign(d_order, 0.0);
}

// The variable names in this function follow those in "Digital Spectral Analysis and Applications",
// S.L.Marple,Jr. page 251-260.
float
specesti_arfmcov::calculate(const gr_complex *x, gr_complex *ar_coeff, int normalise)
{
	unsigned N = d_blocklen;
	unsigned pmax = d_order;
	init_buffers();

	// ------------------ INITIALIZATION -----------------------------------
	double var = 0.0;
	for (short j = 0; j < N; j++) {
		var += 2.0 * norm(x[j]);
	}
	double vari = var - norm(x[0]) - norm(x[N-1]);
	d_ai[0] = 1.0;
	d_c[pmax] = gr_complexd(x[N-1])/var;
	d_d[pmax] = conj(gr_complexd(x[0]))/var;
	gr_complexd lambda = conj(gr_complexd(x[0])) * conj(gr_complexd(x[N-1])) / var;
	double delta = 1 - norm(gr_complexd(x[0])) / var;
	double gamma = 1 - norm(gr_complexd(x[N-1])) / var;

	// ------------------ MAIN LOOP ----------------------------------------
	unsigned p;
	for (p = 1; p <= pmax; p++) {
		gr_complexd r0;
		r0 = 0.0;
		int i;
		for (i = 0; i < (N-p); i++)
			r0 += 2.0 * conj(gr_complexd(x[p+i])) * gr_complexd(x[i]);
		if (p > 1)
			for (i = p-1; i > 0; i--)
				d_r[i] = d_r[i-1]
						- gr_complexd(x[N-p]) * conj(gr_complexd(x[N-i]))
						- conj(gr_complexd(x[p-1]))*gr_complexd(x[i-1]);
		d_r[0] = r0;
		gr_complexd Z;
		Z = 0.0;
		for (i = 0; i < p; i++)
			Z -= conj(d_r[i]) * d_ai[i];
		for (i = 0; i < (p+1);i++)
			d_a[i] = d_ai[i] + Z/vari * conj(d_ai[p-i]);
		var = vari - norm(Z)/vari;

		double DEN;
		DEN = gamma*delta - norm(lambda);
		gr_complexd theta, phi, xi;
		theta = phi = xi = 0.0;
		for (i=0;i<p;i++) {
			theta += gr_complexd(x[N-i-1]) * d_d[pmax-p+1+i];
			phi += gr_complexd(x[N-i-1]) * d_c[pmax-p+1+i];
			xi += conj(gr_complexd(x[p-i-1])) * d_d[pmax-i];
		}
		gr_complexd lambdai, alpha2, alpha3, beta2, beta3;
		alpha2 = (theta*conj(lambda) + phi*delta)/DEN;
		beta2 = (phi*lambda + theta*gamma)/DEN;
		alpha3 = (xi*conj(lambda) + theta*delta)/DEN;
		beta3 = (theta*lambda + xi*gamma)/DEN;
		double gammai, deltai;
		gammai = gamma - (norm(phi)*delta + norm(theta)*gamma + 2*real(phi*lambda*conj(theta)))/DEN;
		deltai = delta - (norm(theta)*delta + norm(xi)*gamma + 2*real(theta*lambda*conj(xi)))/DEN;
		lambdai = lambda + alpha3*conj(phi) + beta3*conj(theta);
		for (i = 0; i < p; i++) {
			d_ci[pmax-p+1+i] = d_c[pmax-p+1+i] + alpha2*conj(d_c[pmax-i]) + beta2*conj(d_d[pmax-i]);
			d_di[pmax-p+1+i] = d_d[pmax-p+1+i] + alpha3*conj(d_c[pmax-i]) + beta3*conj(d_d[pmax-i]);
		}

		double DENi;
		DENi = gammai * deltai - norm(lambdai);
		gr_complexd efp, ebN;
		efp = ebN = 0.0;
		for (i = 0; i < (p+1); i++) {
			efp += gr_complexd(x[p-i]) * d_a[i];
			ebN += gr_complexd(x[N-1-i]) * conj(d_a[p-i]);
		}
		gr_complexd alpha1, beta1;
		alpha1 = (conj(ebN)*deltai + efp*lambdai)/DENi;
		beta1 = (efp*gammai + conj(ebN)*conj(lambdai))/DENi;
		for (i=0;i<(p+1);i++)
			d_ai[i] = d_a[i] + alpha1*d_ci[pmax-p+i] + beta1*d_di[pmax-p+i];
		vari = var - (norm(ebN)*deltai + norm(efp)*gammai + 2*real(efp*ebN*lambdai))/DENi;

		gamma = gammai - norm(ebN)/var;
		delta = deltai - norm(efp)/var;
		lambda = lambdai + conj(efp*ebN)/var;
		for (i=0;i<(p+1);i++) {
			d_c[pmax-p+i] = d_ci[pmax-p+i] + ebN/var * d_a[i];
			d_d[pmax-p+i] = d_di[pmax-p+i] + conj(efp)/var * d_a[i];
		}
	}

	// Copy to output buffer, normalise if requested
	if (normalise) {
		gr_complexd norm = (gr_complexd) (sqrt(var/ ((N-pmax)*normalise) ));
		for(p = 0; p < d_order+1; p++)
			ar_coeff[p] = gr_complex((d_a[p]) / norm);
	} else {
		for(p = 0; p < d_order+1; p++) {
			ar_coeff[p] = gr_complex(d_a[p]);
		}
	}

	return (float) ((var/(N-pmax))/2.0);
}

