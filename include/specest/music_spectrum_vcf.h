/* -*- c++ -*- */
/*
 * Copyright 2014,2019 Communications Engineering Lab, KIT
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


#ifndef INCLUDED_SPECEST_MUSIC_SPECTRUM_VCF_H
#define INCLUDED_SPECEST_MUSIC_SPECTRUM_VCF_H

#include <gnuradio/sync_block.h>
#include <specest/api.h>

namespace gr {
namespace specest {

/*! Calculate pseudospectrum from vectors of samples
 *
 * Consumes a vector of length \p nsamples to produce a vector of length
 * \p pspectrum_len.
 */
class SPECEST_API music_spectrum_vcf : virtual public gr::sync_block
{
public:
    typedef boost::shared_ptr<music_spectrum_vcf> sptr;

    /*!
     * \param n How many sinusoids does your model have?
     * \param m use a correlation matrix of dimension m x m
     * \param nsamples use \p nsamples to get an estimate of the correlation matrix
     * \param pspectrum_len length of the generated pseudospectrum
     * \param decimation process only one in \p decimation vectors of length \p nsamples.
     *                   Can be used to win some time for calculations.
     */
    static sptr make(unsigned int n,
                     unsigned int m,
                     unsigned int nsamples,
                     unsigned int pspectrum_len);
};

} // namespace specest
} // namespace gr

#endif /* INCLUDED_SPECEST_MUSIC_SPECTRUM_VCF_H */
