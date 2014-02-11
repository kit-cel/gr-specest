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

SUBROUTINE ZESPRIT_COMMON(R, N, M, EV)
  IMPLICIT NONE
  INTEGER :: N, M, LWORK, INFO
  COMPLEX*16 :: R(M,M), EV(N)
  DOUBLE PRECISION :: ALPHA, W(M), RWORK(3*M - 2)
  COMPLEX*16, ALLOCATABLE :: WORK(:)
  COMPLEX*16 :: S(M, N)
  COMPLEX*16 :: S1(M-1,N), S2(M-1,N)
  COMPLEX*16 :: VL, VR

  ALLOCATE( WORK(1) )

  LWORK = -1
  CALL ZHEEV('V', 'L', M, R, M, W, WORK, LWORK, RWORK, INFO)
  LWORK = INT(WORK(1))
  DEALLOCATE (WORK)
  ALLOCATE( WORK(LWORK) )
  CALL ZHEEV('V', 'L', M, R, M, W, WORK, LWORK, RWORK, INFO)

  S = R(:, M-N+1:M)
  S1 = S(1:M-1, :)
  S2 = S(2:M, :)

  LWORK = -1
  CALL ZGELS('N', M-1, N, N, S2, M-1, S1, M-1, WORK, LWORK, INFO)
  LWORK = INT(WORK(1))
  DEALLOCATE (WORK)
  ALLOCATE( WORK(LWORK) )
  CALL ZGELS('N', M-1, N, N, S2, M-1, S1, M-1, WORK, LWORK, INFO)

  LWORK = -1
  CALL ZGEEV('N', 'N', N, S1(1:N,:), N, EV, VL, 1, VR, 1, WORK, LWORK, RWORK, INFO)
  LWORK = INT(WORK(1))
  DEALLOCATE (WORK)
  ALLOCATE( WORK(LWORK) )
  CALL ZGEEV('N', 'N', N, S1(1:N,:), N, EV, VL, 1, VR, 1, WORK, LWORK, RWORK, INFO)

  DEALLOCATE(WORK)

END SUBROUTINE ZESPRIT_COMMON
