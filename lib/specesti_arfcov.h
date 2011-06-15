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

#include <gr_complex.h>



/*#include <complex>
typedef std::complex<float>			gr_complex;
typedef std::complex<double>			gr_complexd;*/


class specesti_arfcov
{
 public:
	specesti_arfcov(unsigned blocklen, unsigned order);
	~specesti_arfcov();

	/** \brief Calculate the AR model coefficients from the the given input data.
	 *
	 * \p normalise determines whether the coefficients are normalised to the power
	 *  of the equivalent noise source. If normalise is of an other value than 1,
	 *  the coefficients are additionally normalised by the square root of \p normalise.
	 *
	 * \param[in] data Pointer to \p blocklen complex signal values. \p ar_coeff
	 * \param[out] ar_coeff Points to preallocated space for \p order+1 (!) complex coefficients.
	 * \param[in] normalise Normalisation factor, normalise == 0 means no normalisation.
	 */
	float calculate(const gr_complex *data, gr_complex *ar_coeff, int normalise);

	void set_order(unsigned order);
	void set_blocklen(unsigned blocklen);
	unsigned get_order() { return d_order; };
	unsigned get_blocklen() { return d_blocklen; };

 private:
	unsigned d_blocklen; //!< Block length of input sample vectors
	unsigned d_order; //!< The order of the AR model which is estimated

	gr_complexd *af; //!< Forward AR coefficients
	gr_complexd *ab; //!< Backward AR coefficients
	gr_complexd *afi; 
	gr_complexd *abii;
	gr_complexd *c;
	gr_complexd *d;
	gr_complexd *ci;
	gr_complexd *dii;
	gr_complexd *r;

	void init_buffers();
};

