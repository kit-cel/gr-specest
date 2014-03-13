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


#ifndef INCLUDED_SPECEST_CYCLO_FAM_CALCSPECTRUM_VCF_H
#define INCLUDED_SPECEST_CYCLO_FAM_CALCSPECTRUM_VCF_H

#include <specest/api.h>
#include <gnuradio/sync_interpolator.h>

namespace gr {
  namespace specest {

    /*!
     * \brief Does the heavy lifting of specest_cyclo_fam.
     * \ingroup specest
     *
     */
    class SPECEST_API cyclo_fam_calcspectrum_vcf : virtual public gr::sync_interpolator
    {
     public:
      typedef boost::shared_ptr<cyclo_fam_calcspectrum_vcf> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of specest::cyclo_fam_calcspectrum_vcf.
       *
       * To avoid accidental use of raw pointers, specest::cyclo_fam_calcspectrum_vcf's
       * constructor is in a private implementation
       * class. specest::cyclo_fam_calcspectrum_vcf::make is the public interface for
       * creating new instances.
       */
      static sptr make(int Np, int P, int L);

	  virtual int get_Np() = 0;
	  virtual int get_N() = 0;
	  virtual int get_P() = 0;
      virtual int get_L() = 0;
      virtual const std::vector<std::vector<float> > &get_estimate() = 0;
    };

  } // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_CYCLO_FAM_CALCSPECTRUM_VCF_H */

