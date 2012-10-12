#include <specest_correst_impl.h>

void
specest_impl::correst(const gr_complexd* data, unsigned int data_len, unsigned int m, arma::cx_mat* R)
{
	arma::cx_rowvec y(data, data_len); //TODO possible speedup with the other two options ...

	arma::cx_mat y_est(m, y.n_cols-(m-1));

	for (unsigned int i = 0; i < m; i++)
		y_est.row((m-1)-i) = y.cols(i, y.n_cols-(m-1)+i-1);

	for (unsigned int i = 0; i < y.n_cols-(m-1); i++)
#if ARMA_VERSION_MAJOR < 2
		*(R) = *(R) + y_est.col(i)*arma::htrans(y_est.col(i));
#else
		*(R) = *(R) + y_est.col(i)*arma::trans(y_est.col(i));
#endif

	*(R) = *(R) / (y.n_cols-(m-1));
}
