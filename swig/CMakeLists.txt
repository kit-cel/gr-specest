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

INCLUDE(FindSWIG)
#TODO check SWIG_FOUND

IF(SWIG_FOUND)
INCLUDE(FindPythonInterp)
#TODO check PYTHONINTERP_FOUND

EXECUTE_PROCESS(
    COMMAND ${PYTHON_EXECUTABLE} -c "from distutils import sysconfig; print sysconfig.get_python_lib(prefix='${CMAKE_INSTALL_PREFIX}')"
    OUTPUT_VARIABLE PYTHON_DIR OUTPUT_STRIP_TRAILING_WHITESPACE
)

INCLUDE(FindPythonLibs)
#TODO check PYTHONLIBS_FOUND

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_DIRS})
LINK_DIRECTORIES(${PYTHON_LIBRARY_DIRS})

INCLUDE(UseSWIG)

SET(SWIG_FLAGS_INCLUDE_DIRS
    ${GNURADIO_CORE_INCLUDE_DIRS}
    ${GNURADIO_CORE_INCLUDE_DIRS}/swig
    ${GNURADIO_CORE_INCLUDE_DIRS}/gnuradio/swig
    ${Boost_INCLUDE_DIRS}
    ${UHD_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/swig
)

SET(CMAKE_SWIG_FLAGS -fvirtual -modern -keyword -w511 -module specest_swig)

FOREACH(swig_include_dir ${SWIG_FLAGS_INCLUDE_DIRS})
    LIST(APPEND CMAKE_SWIG_FLAGS "-I${swig_include_dir}")
ENDFOREACH(swig_include_dir)

SET_SOURCE_FILES_PROPERTIES(${CMAKE_BINARY_DIR}/swig/specest.i PROPERTIES CPLUSPLUS ON)

#TODO Find out how to do this without ${CMAKE_BINARY_DIR}
SWIG_ADD_MODULE(specest_swig python ${CMAKE_BINARY_DIR}/swig/specest.i)
SWIG_LINK_LIBRARIES(specest_swig gnuradio-specest ${GNURADIO_CORE_LIBRARIES} ${PYTHON_LIBRARIES})


INSTALL(TARGETS ${SWIG_MODULE_specest_swig_REAL_NAME}
    LIBRARY DESTINATION ${PYTHON_DIR}/specest # .so file
    ARCHIVE DESTINATION ${PYTHON_DIR}/specest # .lib file
    RUNTIME DESTINATION ${PYTHON_DIR}/specest # .dll file
)

INSTALL(FILES ${CMAKE_BINARY_DIR}/swig/specest_swig.py DESTINATION ${PYTHON_DIR}/specest)
FILE(GLOB DOT_I_FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.i)
INSTALL(FILES ${DOT_I_FILES} DESTINATION ${CMAKE_INSTALL_PREFIX}/include/specest/swig)
INSTALL(FILES ${CMAKE_BINARY_DIR}/swig/specest.i DESTINATION ${CMAKE_INSTALL_PREFIX}/include/specest/swig)
ENDIF(SWIG_FOUND)
