/* -*- c++ -*- */
/* 
 * Copyright 2011 <YOU OR YOUR COMPANY>.
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
 
#include <qa_specesti_cyclo_fam_calcspectrum.h>
#include <cppunit/TestAssert.h>
#include <specesti_cyclo_fam_calcspectrum.h>

#include <cstdio>
#include <stdexcept>
#include <iostream>
#include <iomanip>
#include <gr_complex.h>


void
qa_specesti_cyclo_fam_calcspectrum::test1()
{
	//
}

void
qa_specesti_cyclo_fam_calcspectrum::test2()
{
	
	int P=4;
	int Np=4;
	int L=2;
	
	specesti_cyclo_fam_calcspectrum *cfcs = new specesti_cyclo_fam_calcspectrum(P,Np,L);
	gr_complex data[Np*P];

    data[0]=std::complex<float>(1.7000 , 0);
    data[1]=std::complex<float>(-0.6900, -0.6900);
    data[2]=std::complex<float>(0, 0);
    data[3]=std::complex<float>(-0.6900, 0.6900);

    data[4]=std::complex<float>(1.7000 , 0);
    data[5]=std::complex<float>(-0.6900, -0.6900);
    data[6]=std::complex<float>(0, 0);
    data[7]=std::complex<float>(-0.6900, 0.6900);
    
    data[8]=std::complex<float>(1.7000 , 0);
    data[9]=std::complex<float>(-0.6900, -0.6900);
    data[10]=std::complex<float>(0, 0);
    data[11]=std::complex<float>(-0.6900, 0.6900);

    data[12]=std::complex<float>(1.7000 , 0);
    data[13]=std::complex<float>(-0.6900, -0.6900);
    data[14]=std::complex<float>(0, 0);
    data[15]=std::complex<float>(-0.6900, 0.6900);


	/*for(int i = 1; i <= (Np*P);i++) {
	    data[i-1]=(1,0);
	    std::cout << data[i-1] <<  "\t \t";
	
        if((i % (Np)) == 0) {
        std::cout << "|" << std::endl;
        } 
	
	}*/
	/*gr_complex input_data[4*16]
	                         ((1,0), (1,0), (1,0), (1,0), // 1
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0),
	                         (1,0), (1,0), (1,0), (1,0));  // 16
	                         // 1     2     3      4
	*/                      
	cfcs->calc(&data[0]); 
	//float *out = cfcs->get_outputs();              
	std::cout<<std::endl;
	std::cout.precision ( 3 );
	for(int row = 0; row < (2*P*L); row++) {
	
	    for(int column = 0; column < (2*Np-1); column++) {
	    
	    std::cout << std::setw(8) << cfcs->get_value(row,column) <<  "\t";
	    
	    }
	    
	    std::cout<< " | "<<std::endl;
	
	}
	
	std::vector<std::vector<float> > values = cfcs->get_outputs();
	
		for(int row = 0; row < (2*P*L); row++) {
	
	    for(int column = 0; column < (2*Np-1); column++) {
	    
	    std::cout << std::setw(8) << values[row][column] <<  "\t";
	    
	    }
	    
	    std::cout<< " | "<<std::endl;
	
	}
	
	                         
}

