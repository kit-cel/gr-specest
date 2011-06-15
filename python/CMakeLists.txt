# Copyright 2011 Communications Engineering Lab, KIT
#
# This file is part of the GNU Radio Spectral Estimation Toolbox
#
# The GNU Radio Spectral Estimation Toolbox is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# The GNU Radio Spectral Estimation Toolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio Spectral Estimation Toolbox; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

EXECUTE_PROCESS(
    COMMAND ${PYTHON_EXECUTABLE} -c "from distutils import sysconfig; print sysconfig.get_python_lib(prefix='${CMAKE_INSTALL_PREFIX}')"
    OUTPUT_VARIABLE PYTHON_DIR OUTPUT_STRIP_TRAILING_WHITESPACE
)


################################################################################
# Add your tests here (don't put the qa_ ) in front
################################################################################

SET(PYTHON_QA
	specest_gendpss
	specest_burg
	specest_esprit
	specest_esprit_spectrum_vcf
	specest_fcov
	specest_fmcov
	specest_mtm
	specest_welch
	specest_vectormanip)

################################################################################
# Here we add the tests you added above
################################################################################

FOREACH(testcase ${PYTHON_QA})
ADD_TEST(${testcase}_py
	${CMAKE_CURRENT_SOURCE_DIR}/test_runner.py --test ${CMAKE_CURRENT_SOURCE_DIR}/qa_${testcase}.py --path ${CMAKE_BINARY_DIR}/swig)
ENDFOREACH(testcase ${PYTHON_QA})

IF(ARMADILLO_FOUND)
	ADD_TEST(py_specest_music
		${CMAKE_CURRENT_SOURCE_DIR}/test_runner.py --test ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_music.py --path ${CMAKE_BINARY_DIR}/swig)
ENDIF(ARMADILLO_FOUND)


################################################################################
# Here we add our python sourcecode that needs to be installed
################################################################################

#TODO add all
SET(SPECEST_PY_SRCS
	__init__.py
	specest_mtm.py
	specest_gendpss.py)

INSTALL(FILES ${SPECEST_PY_SRCS} DESTINATION ${PYTHON_DIR}/specest)
