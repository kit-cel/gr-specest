/*
 * Copyright 2010 Communications Engineering Lab, KIT
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

#include <specesti_arfcov.h>
#include <stdexcept>
#include <cstring>



specesti_arfcov::specesti_arfcov(unsigned blocklen, unsigned order)
	: d_blocklen(blocklen), d_order(order)
{
	if (order > blocklen) {
		throw std::invalid_argument("specesti_arburg: order cannot exceed block length.");
	}
	if(!blocklen || !order) {
		throw std::invalid_argument ("specesti_arburg: block length and order must be at least 1.");
	}
	af = new gr_complexd [order+1];
	ab = new gr_complexd [order+1];
	afi = new gr_complexd [order+1];
	abii = new gr_complexd [order+1];
	c = new gr_complexd [order+1];
	d = new gr_complexd [order+1];
	ci = new gr_complexd [order+1];
	dii = new gr_complexd [order+1];
	r = new gr_complexd [order];
}


specesti_arfcov::~specesti_arfcov()
{
	delete[] af;
	delete[] ab;
	delete[] afi;
	delete[] abii;
	delete[] c;
	delete[] d;
	delete[] ci;
	delete[] dii;
	delete[] r;
}


void
specesti_arfcov::set_order(unsigned order)
{
	d_order = order;
	delete[] af;
	delete[] ab;
	delete[] afi;
	delete[] abii;
	delete[] c;
	delete[] d;
	delete[] ci;
	delete[] dii;
	delete[] r;
	af = new gr_complexd [order+1];
	ab = new gr_complexd [order+1];
	afi = new gr_complexd [order+1];
	abii = new gr_complexd [order+1];
	c = new gr_complexd [order+1];
	d = new gr_complexd [order+1];
	ci = new gr_complexd [order+1];
	dii = new gr_complexd [order+1];
	r = new gr_complexd [order];
}


void
specesti_arfcov::set_blocklen(unsigned blocklen)
{
	d_blocklen = blocklen;
}


void
specesti_arfcov::init_buffers()
{
  for (int j=0;j<(d_order+1);j++) {
    af[j] = 0.0;
    ab[j] = 0.0;
    afi[j] = 0.0;
    abii[j] = 0.0;
    c[j] = 0.0;
    d[j] = 0.0;
    ci[j] = 0.0;
    dii[j] = 0.0;
    if (j<d_order)
      r[j] = 0.0;
  }
}

// The variable names in this function follow those in "Digital Spectral Analysis and Applications",
// S.L.Marple,Jr. page 241-251.
float
specesti_arfcov::calculate(const gr_complex *x, gr_complex *ar_coeff, int normalise)
{
  unsigned N = d_blocklen;
  unsigned pmax = d_order;
  init_buffers();
  
//------------------INITIALIZATION--------------------------
  int i;
  double sum = 0.0;
  for (i=1;i<(N-1);i++)
    sum += norm(x[i]);
  double vf = sum + norm(x[0]) + norm(x[N-1]); //Forward prediction error
  double vb; // Backward prediction error
  double vfi = sum + norm(x[N-1]);
  double vbii = sum + norm(x[0]);
  
  double delta = 1 - norm(x[0])/vf;
  double gamma = 1 - norm(x[N-1])/vf;
  d[pmax] = gr_complexd(conj(x[0]))/vf;
  c[0] = gr_complexd(conj(x[N-1]))/vf;
  gr_complexd efp = gr_complexd(x[0]);
  gr_complexd ebN = gr_complexd(x[N-1]);
  afi[0] = 1.0;
  abii[pmax] = 1.0;
  
  /*// Debug-Code
  cout << "delta= " << delta << endl;
  cout << "gamma= " << gamma << endl;
  cout << "d[pmax]= " << real(d[pmax]) << ", " << imag(d[pmax]) << endl;
  cout << "c[0]= " << real(c[0]) << ", " << imag(c[0]) << endl;
  cout << "afi[0]= " << real(afi[0]) << endl;
  cout << "---------------\n";*/
  
//---------------------MAIN LOOP------------------------
  unsigned p;
  
  for (p=1;p<(pmax+1);p++) {
    gr_complexd r0;
    r0 = 0.0;
    for (i=0;i<(N-p);i++)
      r0 += conj(x[p+i]) * x[i];
    if (p>1)
      for (i=p-1;i>0;i--)
	r[i] = r[i-1] - gr_complexd(x[N-p]*conj(x[N-i]));
    r[0] = r0;
    gr_complexd Z;
    Z = 0.0;
    for (i=0;i<p;i++)
      Z -= conj(r[i])*afi[i];
    for (i=0;i<(p+1);i++) {
      af[i] = afi[i] + Z/vbii * abii[pmax-p+i];
      ab[pmax-p+i] = abii[pmax-p+i] + conj(Z)/vfi * afi[i];
    }
    vf = vfi - norm(Z)/vbii;
    vb = vbii - norm(Z)/vfi;
    
    gr_complexd theta;
    double deltaii, gammai;
    theta = 0.0;
    for (i=0;i<p;i++)
      theta += gr_complexd(x[p-1-i]) * c[i];
    deltaii = delta - norm(theta)/gamma;
    gammai = gamma - norm(theta)/delta;
    for (i=0;i<p;i++) {
      dii[pmax+1-p+i] = d[pmax+1-p+i] + conj(theta)/gamma * c[i];
      ci[i] = c[i] + theta/delta * d[pmax+1-p+i];
    }
    
    efp = ebN = 0.0;
    for (i=0;i<(p+1);i++) {
      efp += gr_complexd(x[p-i]) * af[i];
      ebN += gr_complexd(x[N-1-i]) * ab[pmax-p+i];
    }
    for (i=0;i<(p+1);i++) {
      afi[i] = af[i] + efp/deltaii * dii[pmax-p+i];
      abii[pmax-p+i] = ab[pmax-p+i] + ebN/gammai * ci[i];
    }
    vfi = vf - norm(efp)/deltaii;
    vbii = vb - norm(ebN)/gammai;
    
    gr_complexd d0,cp;
    d0 = conj(efp)/vf;
    cp = conj(ebN)/vb;
    for (i=0;i<(p+1);i++) {
      d[pmax-p+i] = dii[pmax-p+i] + d0*af[i];
      c[i] = ci[i] + cp*ab[pmax-p+i];
    }
    delta = deltaii - norm(efp)/vf;
    gamma = gammai - norm(ebN)/vb;
    
  }
  
  /*for (p=0;p<pmax+1;p++)
    ar_coeff[p] = gr_complex(af[p]);*/
  // Copy to output buffer
  if (normalise) {
    gr_complexd norm = (gr_complexd) (sqrt(vf/ ((N-pmax)*normalise) ));
    for(p = 0; p < d_order+1; p++)
      ar_coeff[p] = gr_complex((af[p]) / norm);
  } else {
    for(p = 0; p < d_order+1; p++) {
      ar_coeff[p] = gr_complex(af[p]);
    }
  }
    
  return (float) (vf/(N-pmax));
}
