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
 *
 */


#ifndef INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_H
#define INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_H

#include <specest/api.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace specest {

    /*!
     * \brief Convert a stream of items into a stream of overlapping blocks containing nitems_per_block.
     *
     * The i-th block will start with the same \p overlap items as the i-1-th block ended. The first
     * block is prepended with \p overlap zeros to ensure synchronicity.
     * \ingroup converter
     */
    class SPECEST_API stream_to_vector_overlap : virtual public gr::sync_decimator
    {
     public:
      typedef boost::shared_ptr<stream_to_vector_overlap> sptr;

      /*!
       * \param item_size Item size
       * \param nitems_per_block Output vector length
       * \param overlap Number of overlapping items between blocks
       */
      static sptr make(size_t item_size, size_t nitems_per_block, unsigned overlap);
      virtual unsigned overlap() = 0;
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_STREAM_TO_VECTOR_OVERLAP_H */

