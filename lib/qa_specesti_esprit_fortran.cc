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

#include <qa_specesti_esprit_fortran.h>
#include <cppunit/TestAssert.h>
#include <specesti_esprit_fortran.h>
#include <algorithm>
#include <stdexcept>

void
qa_specesti_esprit_fortran::setUp()
{
	#include "test_fixtures_1.h"
	testomegas_len = sizeof(realomegas)/sizeof(double);
	testomegas = new double[testomegas_len];
	testdata_len = sizeof(data)/sizeof(gr_complexd);
	testdata = new gr_complexd[testdata_len];

	for (int i = 0; i < testomegas_len; i++)
	{
		testomegas[i] = realomegas[i];
	}
	for (int i = 0; i < testdata_len; i++)
	{
		testdata[i] = data[i];
	}
}
void
qa_specesti_esprit_fortran::tearDown()
{
	delete testomegas;
	delete testdata;
}
void
qa_specesti_esprit_fortran::t1()
{
	CPPUNIT_ASSERT_THROW(specesti_esprit *esprit = new specesti_esprit_fortran(5, 1), std::invalid_argument);
}

void
qa_specesti_esprit_fortran::calculate()
{
	double omegas[testomegas_len];

	specesti_esprit* esprit = new specesti_esprit_fortran(testomegas_len, 80);
	esprit->calculate(testdata, testdata_len, omegas);

	std::sort(omegas, omegas+testomegas_len);
	for(int i = 0; i < testomegas_len; i++)
	{
		CPPUNIT_ASSERT_DOUBLES_EQUAL(omegas[i], testomegas[i], 0.01);
	}
	delete esprit;
}

void
qa_specesti_esprit_fortran::calculate_pseudospectrum()
{
	const int pspectrum_len = 1024;
	double pspectrum[pspectrum_len];
	std::ofstream out("qa_specesti_esprit_fortran.dat");
	if(!out)
		printf("Couldn't open file!");

	specesti_esprit* esprit = new specesti_esprit_fortran(testomegas_len ,80);
	esprit->calculate_pseudospectrum(testdata, testdata_len, pspectrum, pspectrum_len);

	for(int i = 0; i < pspectrum_len; i++)
		out << pspectrum[i] << " ";
	out.close();
	delete esprit;
}
void
qa_specesti_esprit_fortran::bench()
{
	const int pspectrum_len = 1024;
	const int n = 6;
	double omegas[n];
	double pspectrum[pspectrum_len];
	int iterations = 10;
	timespec start, end;
	long long delta_calc;
	long long delta_calc_pspec;
	std::ofstream out("qa_specesti_esprit_fortran_bench.dat");
	for(int m = 10; m <= 100; m++)
	{
		printf("Starting fortran ESPRIT benchmark with m=%u, ", m);
		specesti_esprit_fortran* esprit = new specesti_esprit_fortran(n, m);
		clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
		for(int i = 0; i < iterations; i++)
		{
			esprit->calculate(testdata, testdata_len, omegas);
		}
		clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
		delta_calc = (end.tv_sec - start.tv_sec)*1000000000LL + end.tv_nsec - start.tv_nsec;
		printf("took %llu ns\n", delta_calc);

		printf("Starting fortran spectrum ESPRIT benchmark with m=%u, ", m);
		clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
		for(int i = 0; i < iterations; i++)
		{
			esprit->calculate_pseudospectrum(testdata, testdata_len, pspectrum, pspectrum_len);
		}
		clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
		delta_calc_pspec = (end.tv_sec - start.tv_sec)*1000000000LL + end.tv_nsec - start.tv_nsec;
		printf("took  %llu ns\n", delta_calc_pspec);

		out << m << " " << iterations << " " << delta_calc << " " << delta_calc_pspec << std::endl;
		delete esprit;
	}
}
