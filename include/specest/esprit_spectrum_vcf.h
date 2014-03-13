/* -*- c++ -*- */
/*
 * Copyright 2014 Communications Engineering Lab, KIT
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


#ifndef INCLUDED_SPECEST_ESPRIT_SPECTRUM_VCF_H
#define INCLUDED_SPECEST_ESPRIT_SPECTRUM_VCF_H

#include <specest/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace specest {

    /*!
     * \brief
     * \ingroup specest
     *
     */
    class SPECEST_API esprit_spectrum_vcf : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<esprit_spectrum_vcf> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of specest::esprit_spectrum_vcf.
       *
       * To avoid accidental use of raw pointers, specest::esprit_spectrum_vcf's
       * constructor is in a private implementation
       * class. specest::esprit_spectrum_vcf::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned int n, unsigned int m, unsigned int nsamples, unsigned int pspectrum_len);
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_ESPRIT_SPECTRUM_VCF_H */

