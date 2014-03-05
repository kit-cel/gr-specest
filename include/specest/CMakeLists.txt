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
# Install public header files
########################################################################
if(ARMADILLO_FOUND)
	set(CXX_ARMADILLO_HDRS
	correst_algo.h
    music_armadillo_algo.h
    music_vcf.h
    music.h
    music_spectrum_vcf.h 
	)
else()
	set(CXX_ARMADILLO_HDRS)
endif()
install(FILES
    api.h
    reciprocal_ff.h
    pad_vector.h
    stream_to_vector_overlap.h
    moving_average_vff.h
    adaptiveweighting_vff.h
    arfcov_algo.h
    arfcov_vcc.h
    fcov.h
    arfmcov_algo.h
    arfmcov_vcc.h
    fmcov.h
    arburg_algo.h
    arburg_vcc.h
    burg.h
    welch.h
    esprit_algo.h
    esprit_fortran_algo.h
    esprit_vcf.h
    esprit_spectrum_vcf.h
    esprit.h
    welchsp.h
    cyclo_fam_calcspectrum_algo.h
    cyclo_fam_calcspectrum_vcf.h
    cyclo_fam.h 
    music_fortran_algo.h
    music_algo.h
    ${CXX_ARMADILLO_HDRS}
    DESTINATION include/specest
)
