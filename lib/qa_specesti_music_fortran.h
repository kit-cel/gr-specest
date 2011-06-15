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

#ifndef INCLUDED_QA_SPECESTI_MUSIC_FORTRAN_H
#define INCLUDED_QA_SPECESTI_MUSIC_FORTRAN_H

#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/TestFixture.h>
#include <gr_complex.h>

class qa_specesti_music_fortran : public CppUnit::TestFixture {

	CPPUNIT_TEST_SUITE (qa_specesti_music_fortran);
	CPPUNIT_TEST (t1);
	CPPUNIT_TEST (calculate);
	// CPPUNIT_TEST (bench);
	CPPUNIT_TEST_SUITE_END ();

 public:
	void setUp();
	void tearDown();

 private:
	gr_complexd* testdata;
	unsigned int testdata_len;
	double* testomegas;
	unsigned int testomegas_len;
	void t1();
	void calculate();
	void calculate_pseudospectrum();
	void bench ();
};

#endif /* INCLUDED_QA_SPECESTI_MUSIC_FORTRAN_H */

