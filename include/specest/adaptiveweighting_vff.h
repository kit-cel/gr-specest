/* -*- c++ -*- */
/* 
 * Copyright 2010,2013 Communications Engineering Lab, KIT
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

#include <specest/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace specest {

    /*!
     * @brief Output is the PSD computed by Thomson's Multitaper Method. Adaptive weighting is used on the eigenspectra.
     * [1] "Spectral Analysis for Physical Applications" D.B. Percival and Andrew T. Walden 1993
     */
    class SPECEST_API adaptiveweighting_vff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<adaptiveweighting_vff> sptr;

      /*!
       * @param vlen: length of the eigenspectra which are connected by GNU Radio
       * @param lambdas: the different eigenvalues belonging to the eigenspectra
       */
      static sptr make(size_t vlen, const std::vector<float> &lambdas);
      virtual const std::vector<float> lambdas () const = 0;
      virtual void set_k (const std::vector<float> lambdas) = 0;
    };
  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_ADAPTIVEWEIGHTING_VFF_H */

