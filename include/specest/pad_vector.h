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

#ifndef INCLUDED_SPECEST_PAD_VECTOR_H
#define INCLUDED_SPECEST_PAD_VECTOR_H

#include <specest/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace specest {

    /*!
     * \brief Increases or decreases the length of vectors.
     *
     * If the output length is smaller than the input length, vectors will be truncated.
     * Otherwise, vectors will be zero-padded.
     *
     * \ingroup specest
     */
    class SPECEST_API pad_vector : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<pad_vector> sptr;

      /*!
       * \param item_size Item size
       * \param vlen_in Length of incoming vectors
       * \param vlen_out New length of vectors (output signature)
       */
      static sptr make(size_t item_size, unsigned vlen_in, unsigned vlen_out);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_PAD_VECTOR_H */

