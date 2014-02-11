! Copyright 2010 Communications Engineering Lab, KIT

! This is free software; you can redistribute it and/or modify
! it under the terms of the GNU General Public License as published by
! the Free Software Foundation; either version 3, or (at your option)
! any later version.

! This software is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.

! You should have received a copy of the GNU General Public License
! along with this software; see the file COPYING.  If not, write to
! the Free Software Foundation, Inc., 51 Franklin Street,
! Boston, MA 02110-1301, USA.

SUBROUTINE ZESPRIT(SAMPLES, LSAMPLES, N, M, OMEGAS)
  IMPLICIT NONE
  INTEGER :: LSAMPLES, N, M, I
  COMPLEX*16 :: SAMPLES(LSAMPLES), R(M,M), EV(N)
  DOUBLE PRECISION :: OMEGAS(N)

  CALL ZCORREST(SAMPLES, LSAMPLES, M, R)
  CALL ZESPRIT_COMMON(R, N, M, EV)

  DO I = 1, N
    OMEGAS(I) = ATAN2(AIMAG(EV(I)), REAL(EV(I)))
  END DO

END SUBROUTINE ZESPRIT
