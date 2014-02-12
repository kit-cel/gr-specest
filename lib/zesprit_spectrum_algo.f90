! Copyright 2010 Communications Engineering Lab, KIT
!
! This is free software; you can redistribute it and/or modify
! it under the terms of the GNU General Public License as published by
! the Free Software Foundation; either version 3, or (at your option)
! any later version.
!
! This software is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.
!
! You should have received a copy of the GNU General Public License
! along with this software; see the file COPYING.  If not, write to
! the Free Software Foundation, Inc., 51 Franklin Street,
! Boston, MA 02110-1301, USA.

SUBROUTINE ZESPRIT_SPECTRUM(SAMPLES, LSAMPLES, N, M, PSPECTRUM, LPSPECTRUM)
  IMPLICIT NONE
  INTEGER :: LSAMPLES, N, M, I, K, LPSPECTRUM
  COMPLEX*16 :: SAMPLES(LSAMPLES), R(M,M), EV(N)
  DOUBLE PRECISION :: PSPECTRUM(LPSPECTRUM)
  DOUBLE PRECISION :: PI, OMEGA, DELTA

  PI = 3.1415926535897932384626433832795028841971d0

  CALL ZCORREST(SAMPLES, LSAMPLES, M, R)
  CALL ZESPRIT_COMMON(R, N, M, EV)

  OMEGA = -PI
  DELTA = 2*PI/(LPSPECTRUM-1)
  DO I = 1, LPSPECTRUM
    PSPECTRUM(I) = 1.0d0
    DO K = 1, N
      PSPECTRUM(I) = PSPECTRUM(I) / (ABS(EXP((0,1)*OMEGA) - EV(K)) ** 2.0d0)
    END DO
    OMEGA = OMEGA + DELTA
  END DO

END SUBROUTINE ZESPRIT_SPECTRUM
