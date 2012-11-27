! Copyright 2012 Communications Engineering Lab, KIT

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

SUBROUTINE ZROOTS(COEFFS, LCOEFFS, ROOTS, LROOTS)
  IMPLICIT NONE
  INTEGER :: LCOEFFS, LROOTS, I, J, LWORK, INFO
  COMPLEX*16 :: COEFFS(LCOEFFS), ROOTS(LROOTS), B(LCOEFFS), A(LCOEFFS-1,LCOEFFS-1)
  DOUBLE PRECISION :: RWORK(3*(LCOEFFS-1) - 2)
  COMPLEX*16, ALLOCATABLE :: WORK(:)
  COMPLEX*16 :: VL, VR

! Set the subdiagonal of the matrix to ones
  DO I = 1, LCOEFFS-2
    A(I+1,I) = 1
  END DO

  DO I = 1, LCOEFFS-1
    A(1,I) = -1 * COEFFS(I) / COEFFS(1)
  END DO

  !DO J = 1, LCOEFFS-1
    !DO I = 1, LCOEFFS-1
      !WRITE (*,"(3f8.3,3f8.3)",advance="no") A(J,I)
    !END DO
    !PRINT *," "
  !END DO

  ALLOCATE( WORK(1) )
  LWORK = -1
  CALL ZGEEV('N', 'N', LCOEFFS-1, A, LCOEFFS-1, ROOTS, VL, 1, VR, 1, WORK, LWORK, RWORK, INFO)
  LWORK = INT(WORK(1))
  DEALLOCATE (WORK)
  ALLOCATE( WORK(LWORK) )
  CALL ZGEEV('N', 'N', LCOEFFS-1, A, LCOEFFS-1, ROOTS, VL, 1, VR, 1, WORK, LWORK, RWORK, INFO)

END SUBROUTINE ZROOTS

