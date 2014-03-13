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

#ifndef INCLUDED_SPECEST_RECIPROCAL_FF_H
#define INCLUDED_SPECEST_RECIPROCAL_FF_H

#include <specest/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace specest {

    /*!
     * \brief Calculate the reciprocal of the input (y = 1/x)
     *
     * \ingroup specest
     */
    class SPECEST_API reciprocal_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<reciprocal_ff> sptr;

      static sptr make(int vlen=1);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_RECIPROCAL_FF_H */

