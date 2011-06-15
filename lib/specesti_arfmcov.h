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
#include <vector>


class specesti_arfmcov
{
 public:
	specesti_arfmcov(unsigned blocklen, unsigned order);
	~specesti_arfmcov();

	/** \brief Calculate the AR model coefficients from the the given input data.
	 * This class uses the fast modified covariance algorith from
	 * S.L. Marple, Jr.: "Digital Spectral Analysis and Applications", page 251-260
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

	std::vector<gr_complexd> d_a; //!< AR coefficients
	std::vector<gr_complexd> d_ai; //!< auxiliary vectors
	std::vector<gr_complexd> d_c;
	std::vector<gr_complexd> d_d;
	std::vector<gr_complexd> d_ci;
	std::vector<gr_complexd> d_di;
	std::vector<gr_complexd> d_r;

	void init_buffers();
};

