#ifndef _SPECESTI_CORREST_H
#define _SPECESTI_CORREST_H

#include <armadillo>
#include <gr_complex.h>

namespace specest_impl
{
void 
correst(const gr_complexd* data, unsigned int data_len, unsigned int m, arma::cx_mat *R);
}

#endif
