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

#ifndef INCLUDED_SPECEST_ARBURG_VCC_H
#define INCLUDED_SPECEST_ARBURG_VCC_H

#include <gr_sync_block.h>
#include <specesti_arburg.h>


class specest_arburg_vcc;
typedef boost::shared_ptr<specest_arburg_vcc> specest_arburg_vcc_sptr;

specest_arburg_vcc_sptr
specest_make_arburg_vcc (unsigned blocklen, unsigned order, int normalise = -1);


/*!
 * \brief Takes an input vector and outputs the AR model coefficients using
 *        Burg's method.
 *
 * Output is a complex vector of length \p order+1. An optional, second output
 * gives the power (variance) of an equivalent noise source (when modeling the
 * spectrum by use of white noise plus the coefficients as a filter).
 *
 * The coefficients can also be normalised by the noise power which is useful
 * when this block is used for spectral analysis by passing a Boolean value to
 * \p normalise. This defaults to true (do normalise) if only one output is
 * connected and to false (don't normalise) if two output are connected, but can
 * be overriden by \p normalise. 
 *
 * \ingroup specest
 */
class specest_arburg_vcc : public gr_sync_block
{
	friend specest_arburg_vcc_sptr
		specest_make_arburg_vcc(unsigned blocklen,
		                        unsigned order,
		                        int normalise);

	specest_arburg_vcc(unsigned blocklen, unsigned order, int normalise);

	unsigned d_blocklen; //!< Number of input samples per calculation
	unsigned d_order;    //!< Order of the AR model
	int d_normalise;

	specesti_arburg *d_burg;

 public:
	~specest_arburg_vcc ();

	int work (int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items);
};

#endif /* INCLUDED_SPECEST_ARBURG_VCC_H */

