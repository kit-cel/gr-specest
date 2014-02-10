/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_SPECEST_ARFMCOV_VCC_H
#define INCLUDED_SPECEST_ARFMCOV_VCC_H

#include <specest/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace specest {

    /*!
     * \brief <+description of block+>
     * \ingroup specest
     *
     */
    class SPECEST_API arfmcov_vcc : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<arfmcov_vcc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of specest::arfmcov_vcc.
       *
       * To avoid accidental use of raw pointers, specest::arfmcov_vcc's
       * constructor is in a private implementation
       * class. specest::arfmcov_vcc::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned blocklen, unsigned order, int normalise = -1);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_ARFMCOV_VCC_H */

