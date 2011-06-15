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

#ifndef INCLUDED_SPECEST_ADAPTIVEWEIGHTING_VFF_H
#define INCLUDED_SPECEST_ADAPTIVEWEIGHTING_VFF_H

#include <gr_sync_block.h>

class specest_adaptiveweighting_vff;

typedef boost::shared_ptr<specest_adaptiveweighting_vff> specest_adaptiveweighting_vff_sptr;

specest_adaptiveweighting_vff_sptr specest_make_adaptiveweighting_vff (size_t vlen, const std::vector<float> lambdas);

/*!
 * @brief Output is the PSD computed by Thomson's Multitaper Method. Adaptive weighting is used on the eigenspectra.
 *
 * @param vlen: length of the eigenspectra which are connected by GNU Radio
 * @param lambdas: the diffirent eigenvalues belonging to the eigenspectra
 * 
 */
class specest_adaptiveweighting_vff : public gr_sync_block
{
private:
  friend specest_adaptiveweighting_vff_sptr specest_make_adaptiveweighting_vff(size_t vlen, const std::vector<float> lambdas);

  std::vector<float> d_lambdas; // the eigenvalues
  specest_adaptiveweighting_vff (size_t vlen, const std::vector<float> lambdas);

  size_t d_vlen;

 public:
  const std::vector<float> lambdas () const { return d_lambdas; }
  void set_k (const std::vector<float> lambdas) { d_lambdas = lambdas; }

  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_SPECEST_ADAPTIVEWEIGHTING_VFF_H */

