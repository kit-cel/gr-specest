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

#ifndef INCLUDED_SPECEST_MOVING_AVERAGE_VFF_H
#define INCLUDED_SPECEST_MOVING_AVERAGE_VFF_H

#include <specest/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace specest {

    /*!
     * \brief output is the moving sum of the last N samples, scaled by the \p scale factor.
     *
     * The moving average of the vectors is calculated per element.
     *
     * \p max_iter limits how long we go without flushing the accumulator. This is necessary
     * to avoid numerical instability for float and complex.
     *
     * \ingroup filter
     */
    class SPECEST_API moving_average_vff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<moving_average_vff> sptr;

      static sptr make(int length, int vlen, float scale, int max_iter = 4096);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_MOVING_AVERAGE_VFF_H */

