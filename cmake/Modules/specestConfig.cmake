INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SPECEST specest)

FIND_PATH(
    SPECEST_INCLUDE_DIRS
    NAMES specest/api.h
    HINTS $ENV{SPECEST_DIR}/include
        ${PC_SPECEST_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SPECEST_LIBRARIES
    NAMES gnuradio-specest
    HINTS $ENV{SPECEST_DIR}/lib
        ${PC_SPECEST_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SPECEST DEFAULT_MSG SPECEST_LIBRARIES SPECEST_INCLUDE_DIRS)
MARK_AS_ADVANCED(SPECEST_LIBRARIES SPECEST_INCLUDE_DIRS)

