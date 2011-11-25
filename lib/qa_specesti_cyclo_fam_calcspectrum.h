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

#ifndef INCLUDED_QA_SPECESTI_CYCLO_FAM_CALCSPECTRUM_H
#define INCLUDED_QA_SPECESTI_CYCLO_FAM_CALCSPECTRUM_H

#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/TestCase.h>

/**
 * Run tests on the FAM.
 */

class qa_specesti_cyclo_fam_calcspectrum : public CppUnit::TestCase {

	CPPUNIT_TEST_SUITE (qa_specesti_cyclo_fam_calcspectrum);
	CPPUNIT_TEST (test1);
	CPPUNIT_TEST (test2);
	CPPUNIT_TEST_SUITE_END ();

 private:
	void test1 ();
	void test2 ();
};

#endif /* INCLUDED_QA_SPECESTI_CYCLO_FAM_CALCSPECTRUM_H */

