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

#include <cppunit/TestAssert.h>
#include <specesti_cyclo_fam_calcspectrum.h>
#include <qa_specesti_cyclo_fam_calcspectrum.h>
#include <cstdio>
#include <stdexcept>
#include <iostream>


void
qa_specesti_cyclo_fam_calcspectrum::t1()
{
	CPPUNIT_ASSERT_THROW( specesti_cyclo_fam_calcspectrum *cfcs = new specesti_cyclo_fam_calcspectrum(15,4,2), std::invalid_argument );
	CPPUNIT_ASSERT_THROW( specesti_cyclo_fam_calcspectrum *cfcs = new specesti_cyclo_fam_calcspectrum(16,5,2), std::invalid_argument );
    CPPUNIT_ASSERT_THROW( specesti_cyclo_fam_calcspectrum *cfcs = new specesti_cyclo_fam_calcspectrum(16,4,3), std::invalid_argument );
}

void
qa_specesti_cyclo_fam_calcspectrum::t2()
{
	// Insert CPPUNIT tests/asserts here
}

