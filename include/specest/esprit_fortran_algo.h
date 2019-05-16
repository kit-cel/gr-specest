/* -*- c++ -*- */
/*
 * Copyright 2011 Communications Engineering Lab, KIT
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
#ifndef INCLUDED_SPECESTI_ESPRIT_FORTRAN_H
#define INCLUDED_SPECESTI_ESPRIT_FORTRAN_H

#include <specest/api.h>
#include <specest/esprit_algo.h>

namespace gr {
namespace specest {

class SPECEST_API esprit_fortran_algo : virtual public esprit_algo
{
public:
    esprit_fortran_algo(unsigned n, unsigned m);
    void calculate(const gr_complexd* data, unsigned int data_len, double* omegas);
    void calculate_pseudospectrum(const gr_complexd* data,
                                  unsigned int data_len,
                                  double* pspectrum,
                                  unsigned int pspectrum_len);
    ~esprit_fortran_algo();

private:
    unsigned int d_n;
    unsigned int d_m;
};

} /* namespace specest */
} /* namespace gr */
#endif /* INCLUDED_SPECESTI_ESPRIT_FORTRAN_H */
