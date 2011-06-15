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

PROJECT(GR-SPECEST)
ENABLE_LANGUAGE(Fortran)
ENABLE_LANGUAGE(CXX)

CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

IF(UNIX AND EXISTS "/usr/lib64")
	LIST(APPEND BOOST_LIBRARYDIR "/usr/lib64") #fedora 64-bit fix
	SET(LIB_POSTFIX 64)
ENDIF(UNIX AND EXISTS "/usr/lib64")

LIST(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/CMake)

###############################################################################
# Search for the required packages
###############################################################################

FIND_PACKAGE(Boost REQUIRED)
FIND_PACKAGE(CppUnit REQUIRED)
FIND_PACKAGE(BLAS REQUIRED)
FIND_PACKAGE(LAPACK REQUIRED)
FIND_PACKAGE(Doxygen)
FIND_PACKAGE(UHD)

FIND_PACKAGE(Armadillo)
INCLUDE(Armadillo)

INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(GNURADIO_CORE REQUIRED gnuradio-core)
PKG_CHECK_MODULES(GNURADIO_UHD REQUIRED gnuradio-uhd)

INCLUDE_DIRECTORIES(${GNURADIO_CORE_INCLUDE_DIRS})
INCLUDE_DIRECTORIES(SYSTEM ${CMAKE_SOURCE_DIR}/lib ${CMAKE_BINARY_DIR}/lib)

SUBDIRS(lib swig python grc apps doc)

#TODO generate the specest.i out of source
CONFIGURE_FILE(${CMAKE_SOURCE_DIR}/swig/specest.i.in ${CMAKE_BINARY_DIR}/swig/specest.i)
CONFIGURE_FILE(${CMAKE_SOURCE_DIR}/lib/config.h.in ${CMAKE_BINARY_DIR}/lib/config.h)
CONFIGURE_FILE(${CMAKE_SOURCE_DIR}/gnuradio-specest.pc.in ${CMAKE_BINARY_DIR}/gnuradio-specest.pc @ONLY)

ENABLE_TESTING()

MESSAGE("\n=============================================================================================")
MESSAGE("GNU Radio Spectral Estimation Toolbox")
MESSAGE("Copyright 2009-2011 Communications Engineering Lab, KIT\n")
MESSAGE("This program comes with ABSOLUTELY NO WARRANTY.")
MESSAGE("This is free software, and you are welcome to redistribute it under certain conditions.")
MESSAGE("For further information see COPYING")
MESSAGE("=============================================================================================\n")

INSTALL(FILES ${CMAKE_BINARY_DIR}/gnuradio-specest.pc DESTINATION ${CMAKE_INSTALL_PREFIX}/lib${LIB_POSTFIX}/pkgconfig)
