# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

########################################################################
# Install python sources
########################################################################
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    fam_matplotlib.py
    logpwrspectrum.py
    signal_generator.py
    specest_gendpss.py
    specest_mtm.py
    specest_window.py
    spectrum_sink_gl.py
    DESTINATION ${GR_PYTHON_DIR}/specest
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-specest)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_specest_burg ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_burg.py)
GR_ADD_TEST(qa_specest_cyclo_fam ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_cyclo_fam.py)
GR_ADD_TEST(qa_specest_esprit ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_esprit.py)
GR_ADD_TEST(qa_specest_esprit_spectrum_vcf ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_esprit_spectrum_vcf.py)
GR_ADD_TEST(qa_specest_esprit_vcf ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_esprit_vcf.py)
GR_ADD_TEST(qa_specest_fcov ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_fcov.py)
GR_ADD_TEST(qa_specest_fmcov ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_fmcov.py)
GR_ADD_TEST(qa_specest_gendpss ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_gendpss.py)
GR_ADD_TEST(qa_specest_mtm ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_mtm.py)
GR_ADD_TEST(qa_specest_music ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_music.py)
GR_ADD_TEST(qa_specest_vectormanip ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_vectormanip.py)
GR_ADD_TEST(qa_specest_welch ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_welch.py)
GR_ADD_TEST(qa_specest_welchsp ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_welchsp.py)

