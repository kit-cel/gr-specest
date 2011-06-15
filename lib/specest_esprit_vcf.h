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

#ifndef INCLUDED_SPECEST_ESPRIT_VCF_H
#define INCLUDED_SPECEST_ESPRIT_VCF_H

#include <gr_sync_block.h>
#include <specesti_esprit.h>

class specest_esprit_vcf;
typedef boost::shared_ptr<specest_esprit_vcf> specest_esprit_vcf_sptr;

specest_esprit_vcf_sptr specest_make_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples);

/*!
 * \brief 
 *
 */
class specest_esprit_vcf : public gr_sync_block
{
	friend specest_esprit_vcf_sptr specest_make_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples);

	specest_esprit_vcf (unsigned int n, unsigned int m, unsigned int nsamples);

 public:
	~specest_esprit_vcf ();


	int work (int noutput_items,
	          gr_vector_const_void_star &input_items,
	          gr_vector_void_star &output_items);

	specesti_esprit* d_impl;
	unsigned int d_m;
	unsigned int d_n;
	unsigned int d_nsamples;
};

#endif /* INCLUDED_SPECEST_ESPRIT_VCF_H */
