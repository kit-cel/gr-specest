# Copyright 2011,2012 Communications Engineering Lab, KIT
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


########################################################################
# Install public header files
########################################################################
if(ARMADILLO_FOUND)
	set(CXX_ARMADILLO_HDRS
		specest_music.h
		specest_music_vcf.h
		specest_music_spectrum_vcf.h
		specest_music_armadillo_impl.h
		specest_correst_impl.h
	)
else()
	set(CXX_ARMADILLO_HDRS)
endif()

install(FILES
    specest_api.h
    specest_adaptiveweighting_vff.h
    specest_api.h
    specest_arburg_vcc.h
    specest_arfcov_vcc.h
    specest_arfmcov_vcc.h
    specest_burg.h
    specest_cyclo_fam_calcspectrum_vcf.h
    specest_cyclo_fam.h
    specest_esprit.h
    specest_esprit_spectrum_vcf.h
    specest_esprit_vcf.h
    specest_fcov.h
    specest_fmcov.h
    specest_moving_average_vff.h
    specest_pad_vector.h
    specest_reciprocal_ff.h
    specest_stream_to_vector_overlap.h
    specest_welch.h
    specest_welchsp.h
    specest_arburg_impl.h
    specest_arfcov_impl.h
    specest_arfmcov_impl.h
    specest_cyclo_fam_calcspectrum_impl.h
    specest_esprit_fortran_impl.h
    specest_esprit_impl.h
    specest_music_fortran_impl.h
    specest_music_impl.h
    ${CXX_ARMADILLO_HDRS}
    DESTINATION include/specest
)


IF (ARMADILLO_FOUND)
	        SET(HAVE_ARMADILLO 1)
		        SET(armadillo_optional_headers "#include \"specest_music.h\" \n#include \"specest_music_vcf.h\" \n#include \"specest_music_spectrum_vcf.h\"")
			        SET(armadillo_optional_dot_i "%include \"specest_music.i\" \n%include \"specest_music_vcf.i\" \n%include \"specest_music_spectrum_vcf.i\"")
			ELSE(ARMADILLO_FOUND)
				        SET(armadillo_optional_headers "")
					        SET(armadillo_optional_dot_i "")
						        MESSAGE("-- As armadillo wasn't found, the MUSIC algorithm will not be built")
						ENDIF(ARMADILLO_FOUND)

