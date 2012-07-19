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

SUBROUTINE ZCORREST(SAMPLES, LSAMPLES, M, R)
  IMPLICIT NONE
  INTEGER :: LSAMPLES, M, I, LCORR
  COMPLEX*16 :: SAMPLES(LSAMPLES), R(M,M)
  DOUBLE PRECISION :: ALPHA

  R = 0

  LCORR = LSAMPLES - M + 1
  ALPHA = 1.0d0/LCORR

  DO I = 1, LCORR
    CALL ZHER('L', M, ALPHA, SAMPLES(I+M-1:I:-1), 1, R, M)
  END DO

END SUBROUTINE ZCORREST
