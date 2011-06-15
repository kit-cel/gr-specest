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

IF(DOXYGEN_FOUND)
  OPTION(DOXYGEN_ENABLE_HTML "Enable HTML documentation." ON)
  OPTION(DOXYGEN_ENABLE_XML  "Enable XML documentation."  OFF)
  IF(DOXYGEN_DOT_FOUND)
    SET(HAVE_DOT "YES")
  ELSE(DOXYGEN_DOT_FOUND)
    SET(HAVE_DOT "NO")
  ENDIF(DOXYGEN_DOT_FOUND)
  IF(DOXYGEN_DOT_FOUND)
    SET(HAVE_DOT "YES")
  ELSE(DOXYGEN_DOT_FOUND)
    SET(HAVE_DOT "NO")
  ENDIF(DOXYGEN_DOT_FOUND)
  IF(DOXYGEN_ENABLE_HTML)
    SET(ENABLE_HTML_DOCS "YES")
  ELSE(DOXYGEN_ENABLE_HTML)
    SET(ENABLE_HTML_DOCS "NO")
  ENDIF(DOXYGEN_ENABLE_HTML)
  IF(DOXYGEN_ENABLE_XML)
    SET(ENABLE_XML_DOCS "YES")
  ELSE(DOXYGEN_ENABLE_XML)
    SET(ENABLE_XML_DOCS "NO")
  ENDIF(DOXYGEN_ENABLE_XML)

  CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)
    ADD_CUSTOM_TARGET(doc ALL
    ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Generating API documentation with Doxygen" VERBATIM
  )

  IF(DOXYGEN_ENABLE_HTML)
    INSTALL(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/html
	    DESTINATION ${CMAKE_INSTALL_PREFIX}/share/doc/gr-specest)
  ENDIF(DOXYGEN_ENABLE_HTML)
  IF(DOXYGEN_ENABLE_XML)
    INSTALL(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/xml
	    DESTINATION ${CMAKE_INSTALL_PREFIX}/share/doc/gr-specest)
  ENDIF(DOXYGEN_ENABLE_XML)
ENDIF(DOXYGEN_FOUND)
