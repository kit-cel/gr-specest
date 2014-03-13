#ifndef _SPECESTI_CORREST_H
#define _SPECESTI_CORREST_H

#include <armadillo>
#include <gnuradio/gr_complex.h>

//namespace gr {
//  namespace specest {

	namespace specest_correst
	{
	void
	correst(const gr_complexd* data, unsigned int data_len, unsigned int m, arma::cx_mat *R);
	}

//  } /* namespace specest */
//} /* namespace gr */

#endif
