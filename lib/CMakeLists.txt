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

SET(CXX_LDFLAGS ${GNURADIO_CORE_LDFLAGS})
SET(CMAKE_CXX_FLAGS -fPIC)

###############################################################################
# Our C++ sources go here
###############################################################################

SET(CXX_SRCS
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_esprit_fortran.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_esprit_spectrum_vcf.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_esprit_vcf.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_esprit.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_burg.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_arburg.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_arburg_vcc.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_reciprocal_ff.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_pad_vector.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_fcov.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_arfcov.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_arfcov_vcc.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_arfmcov.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_arfmcov_vcc.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_fmcov.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_welch.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_adaptiveweighting_vff.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_moving_average_vff.cc
	${CMAKE_CURRENT_SOURCE_DIR}/specest_stream_to_vector_overlap.cc)

###############################################################################
# Our C++ code depending on armadillo goes here
###############################################################################
SET(CXX_ARMADILLO_SRCS
		${CMAKE_CURRENT_SOURCE_DIR}/specesti_music_armadillo.cc
		${CMAKE_CURRENT_SOURCE_DIR}/specest_music.cc
		${CMAKE_CURRENT_SOURCE_DIR}/specest_music_vcf.cc
		${CMAKE_CURRENT_SOURCE_DIR}/specest_music_spectrum_vcf.cc
		${CMAKE_CURRENT_SOURCE_DIR}/specesti_correst.cc)

###############################################################################
# Our Fortran sources go here 
###############################################################################

SET(F_SRCS
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_zesprit_common.f90
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_zcorrest.f90
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_zesprit.f90
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_zesprit_spectrum.f90
	${CMAKE_CURRENT_SOURCE_DIR}/specesti_zmusic_spectrum.f90)

###############################################################################
# Our QA sources go here
###############################################################################

SET(CXX_QA_SRCS
	${CMAKE_CURRENT_SOURCE_DIR}/qa_specest.cc
	${CMAKE_CURRENT_SOURCE_DIR}/qa_specesti_esprit_fortran.cc
	${CMAKE_CURRENT_SOURCE_DIR}/qa_specest_arburg.cc)

SET(CXX_QA_ARMADILLO_SRCS
	${CMAKE_CURRENT_SOURCE_DIR}/qa_specesti_music_armadillo.cc)

###############################################################################
# Our CXX unit tests go here
###############################################################################

SET(CXX_QA
	specest_arburg
	specesti_esprit_fortran)

################################################################################
# Here we add the tests you added above
################################################################################

FOREACH(testcase ${CXX_QA})
	ADD_TEST(${testcase}_cxx ${EXECUTABLE_OUTPUT_PATH}/test_runner qa_${testcase})
ENDFOREACH(testcase ${CXX_QA})

# If armadillo is found we also add the test for specesti_armadillo_music
IF(ARMADILLO_FOUND)
	ADD_TEST(specesti_music_armadillo_cxx ${EXECUTABLE_OUTPUT_PATH}/test_runner "qa_specesti_music_armadillo")
ENDIF(ARMADILLO_FOUND)

###############################################################################
# Here we finally create our targets
###############################################################################

###############################################################################
# Our Fortran libraries
###############################################################################

ADD_LIBRARY(gnuradio-specest-fortran SHARED ${F_SRCS})
TARGET_LINK_LIBRARIES(gnuradio-specest-fortran
	${LAPACK_LIBRARIES}
	${BLAS_LIBRARIES})

ADD_LIBRARY(gnuradio-specest-fortran-static ${F_SRCS})
SET_TARGET_PROPERTIES(gnuradio-specest-fortran-static
	PROPERTIES
	OUTPUT_NAME
	"gnuradio-specest-fortran")

SET_TARGET_PROPERTIES(gnuradio-specest-fortran-static
	PROPERTIES
	PREFIX
	"lib")
TARGET_LINK_LIBRARIES(gnuradio-specest-fortran-static
	${LAPACK_LIBRARIES}
	${BLAS_LIBRARIES})

###############################################################################
# Our main library
###############################################################################

IF(ARMADILLO_FOUND)
	# our shared library
	ADD_LIBRARY(gnuradio-specest SHARED ${CXX_SRCS}
		${CXX_ARMADILLO_SRCS})
	TARGET_LINK_LIBRARIES(gnuradio-specest
			gnuradio-specest-fortran 
			${ARMADILLO_LIBRARIES}
			${CXX_LDFLAGS})

	# our static library
	ADD_LIBRARY(gnuradio-specest-static ${CXX_SRCS}
		${CXX_ARMADILLO_SRCS})
	TARGET_LINK_LIBRARIES(gnuradio-specest-static
			gnuradio-specest-fortran 
			${ARMADILLO_LIBRARIES}
			${CXX_LDFLAGS})

ELSE(ARMADILLO_FOUND)
	# our shared library without the armadillo stuff
	ADD_LIBRARY(gnuradio-specest SHARED ${CXX_SRCS})
	TARGET_LINK_LIBRARIES(gnuradio-specest
			gnuradio-specest-fortran 
			${CXX_LDFLAGS})

	# our static library without the armadillo stuff
	ADD_LIBRARY(gnuradio-specest-static ${CXX_SRCS})
	TARGET_LINK_LIBRARIES(gnuradio-specest-static
			gnuradio-specest-fortran-static
			${CXX_LDFLAGS})
ENDIF(ARMADILLO_FOUND)

# we do this to have the same name for our static library
SET_TARGET_PROPERTIES(gnuradio-specest-static
		PROPERTIES
		OUTPUT_NAME
		"gnuradio-specest")
SET_TARGET_PROPERTIES(gnuradio-specest-static
	PROPERTIES
	PREFIX
	"lib")

###############################################################################
# Our QA library
###############################################################################

IF(ARMADILLO_FOUND)
	ADD_LIBRARY(gnuradio-specest-qa ${CXX_QA_SRCS} ${CXX_QA_ARMADILLO_SRCS})
ELSE()
	ADD_LIBRARY(gnuradio-specest-qa ${CXX_QA_SRCS})
ENDIF()

TARGET_LINK_LIBRARIES(gnuradio-specest-qa
	gnuradio-specest
	gnuradio-specest-fortran
	rt
	pthread)

###############################################################################
# Our testrunner
###############################################################################

ADD_EXECUTABLE(test_runner ${CMAKE_CURRENT_SOURCE_DIR}/test_runner.cc)
TARGET_LINK_LIBRARIES(test_runner
	gnuradio-specest-static
	gnuradio-specest-fortran-static
	gnuradio-specest-qa
	${CPPUNIT_LIBRARIES}
	${CPPUNIT}
	${CXX_LDFLAGS})

###############################################################################
# Install the stuff
###############################################################################

IF(UNIX AND EXISTS "/usr/lib64")
	SET(LIB_POSTFIX 64)
ENDIF(UNIX AND EXISTS "/usr/lib64")

INSTALL(TARGETS gnuradio-specest gnuradio-specest-static gnuradio-specest-fortran gnuradio-specest-fortran-static
	LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib${LIB_POSTFIX}
	ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib${LIB_POSTFIX}
	RUNTIME DESTINATION	${CMAKE_INSTALL_PREFIX}/lib${LIB_POSTFIX})

FILE(GLOB CXX_HDRS ${CMAKE_CURRENT_SOURCE_DIR}/specest_*.h)
INSTALL(FILES ${CXX_HDRS} DESTINATION ${CMAKE_INSTALL_PREFIX}/include/specest)
