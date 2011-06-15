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


#include <specesti_music_armadillo.h>
#include <specesti_correst.h>
#include <armadillo>

specesti_music_armadillo::specesti_music_armadillo(unsigned int n, unsigned int m) : d_n(n), d_m(m)
{
	if (n > m) 
			throw std::invalid_argument("specesti_music_armadillo: n cannot exceed m in length.");
}

specesti_music_armadillo::~specesti_music_armadillo()
{
}

inline
arma::cx_mat 
specesti_music_armadillo::diag(arma::cx_colvec c, int k)
{
	int n = c.n_rows+abs(k);
	arma::cx_mat A(n, n);
	A.diag(k) = c;
	return A;
}

arma::cx_mat 
specesti_music_armadillo::roots(arma::cx_rowvec c)
{
	int n = c.n_cols - 1;
	arma::cx_colvec B = arma::ones<arma::cx_colvec>(n-1);
	arma::cx_mat A = diag(B, -1);
	arma::cx_rowvec q = c.cols(1,n);
	A.row(0) = -1 * q/c(0);
	arma::cx_vec eigval;
	arma::cx_mat eigvec;
	eig_gen(eigval, eigvec, A);

	return eigval;
}


void 
specesti_music_armadillo::calculate(const gr_complexd* data, unsigned int data_len,
                                    double* omegas)
{
	arma::cx_mat R(d_m, d_m);
	specesti::correst(data, data_len, d_m, &R);
	arma::colvec eigvals;
	arma::cx_mat eigvec;
	arma::cx_mat G;
	arma::cx_mat Q;
	arma::cx_mat c(2*d_m-1, 1);
	arma::cx_vec z_all;
	arma::cx_vec z_inside_largest;

	// do an eigendecomposition
	arma::eig_sym(eigvals, eigvec, R);

	// generate a base for the noise subspace
	G = eigvec.cols(0, d_m-d_n-1);
	// solve a*GG*a = 0 => a*Qa = 0
	Q = G * arma::htrans(G);
	// get the coefficents of the complex polynom
	for(int i = 0; i < d_m-1; i++) {
		c(i+d_m,0) = arma::sum(Q.diag(i+1));
		c.row(d_m-2-i) = arma::conj(c.row(i+d_m));
	}
	c(d_m-1) = arma::sum(Q.diag());
	// calculate roots and get the largest inside the unit-cirle
	z_all = arma::sort(roots(arma::trans(c)), 1);
	for (unsigned int i = 0; i < z_all.n_rows; i++)
	{
		if (std::abs(z_all(i)) < 1)
		{
			z_inside_largest = z_all.rows(i, i+d_n-1);
			break;
		}
	}
	for(unsigned int i = 0; i < d_n; i++)
	{
		omegas[i] = arg(z_inside_largest(i));
	}

}

void
specesti_music_armadillo::calculate_pseudospectrum(const gr_complexd* data, unsigned int data_len,
                                                   double* pspectrum, unsigned int pspectrum_len)
{
	arma::cx_mat R(d_m, d_m);
	specesti::correst(data, data_len, d_m, &R);
	arma::colvec eigvals;
	arma::cx_mat eigvec;
	arma::cx_mat G;
	arma::cx_vec a(d_m);
	arma::cx_vec tmp;

	// do an eigendecomposition
	arma::eig_sym(eigvals, eigvec, R);

	// generate a base for the noise subspace
	G = eigvec.cols(0, d_m-d_n-1);
	for(int i = 0; i < pspectrum_len; i++)
	{
	  double omega = -M_PI + i * 2.0*M_PI/(pspectrum_len -1);
		for(int t = 0; t < d_m; t++)
			a[t] = exp(gr_complexd(0,-omega*t)); //TODO magic -1
		pspectrum[i] = 1.0 / pow((arma::norm(arma::htrans(G) * a, 2)),2);
	}
}
