# Copyright 2011,2012 Free Software Foundation, Inc.
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
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

########################################################################
# Fortran lib
########################################################################
add_library(gnuradio-specest-fortran SHARED
    zcorrest_algo.f90
    zesprit_common_algo.f90
    zesprit_algo.f90
    zesprit_spectrum_algo.f90
    zmusic_spectrum_algo.f90
    zmusic_algo.f90
)
target_link_libraries(gnuradio-specest-fortran ${LAPACK_LIBRARIES} ${BLAS_LIBRARIES})

########################################################################
# Configure Armadillo dependency
########################################################################
if(ARMADILLO_FOUND)
	set(CXX_ARMADILLO_SRCS
	    correst_algo.cc
    	music_armadillo_algo.cc
    	music_vcf_impl.cc
    	music_impl.cc
    	music_spectrum_vcf_impl.cc
	)
else()
	set(CXX_ARMADILLO_SRCS)
	set(ARMADILLO_LIBRARIES)
endif()

########################################################################
# Main library
########################################################################
include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND specest_sources
    reciprocal_ff_impl.cc
    pad_vector_impl.cc
    stream_to_vector_overlap_impl.cc
    moving_average_vff_impl.cc
    adaptiveweighting_vff_impl.cc
    arfcov_algo.cc
    arfcov_vcc_impl.cc
    fcov_impl.cc
    arfmcov_algo.cc
    arfmcov_vcc_impl.cc
    fmcov_impl.cc
    arburg_algo.cc
    arburg_vcc_impl.cc
    burg_impl.cc
    welch_impl.cc
    esprit_fortran_algo.cc
    esprit_vcf_impl.cc
    esprit_spectrum_vcf_impl.cc
    esprit_impl.cc
    music_fortran_algo.cc
    welchsp_impl.cc
    cyclo_fam_calcspectrum_algo.cc
    cyclo_fam_calcspectrum_vcf_impl.cc
    cyclo_fam_impl.cc
    ${CXX_ARMADILLO_SRCS}
    )

add_library(gnuradio-specest SHARED ${specest_sources})
target_link_libraries(gnuradio-specest gnuradio-specest-fortran
    ${ARMADILLO_LIBRARIES}
    ${Boost_LIBRARIES}
    ${GNURADIO_RUNTIME_LIBRARIES}
    ${GNURADIO_BLOCKS_LIBRARIES}
    ${GNURADIO_FILTER_LIBRARIES}
    ${GNURADIO_FFT_LIBRARIES}
    ${FFTW3F_LIBRARIES}
)
set_target_properties(gnuradio-specest PROPERTIES DEFINE_SYMBOL "gnuradio_specest_EXPORTS")

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-specest gnuradio-specest-fortran
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_specest_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_specest.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_specest.cc
)

add_executable(test-specest ${test_specest_sources})

target_link_libraries(
  test-specest
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  ${GNURADIO_BLOCKS_LIBRARIES}
  ${GNURADIO_FILTER_LIBRARIES}
  ${GNURADIO_FFT_LIBRARIES}
  ${FFTW3F_LIBRARIES}
  gnuradio-specest
)

GR_ADD_TEST(test_specest test-specest)
