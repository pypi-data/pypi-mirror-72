c MPPL  = /usr/local/basis/vbasis/bin/mppl
c mppl  -r8 -i4
c     -DNO_INCLUDES=1
c     -I.
c     -I.
c     -I..
c     -I/mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include
c     -I/usr/local/basis/vbasis/include
c     -I/usr/local/pact/pact04_05_11/include
c     /usr/local/basis/vbasis/include/basis-m-defs.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/xuedge-m-defs.d
c     ../../sptodp
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/svr.d
c     ./../svrut2.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c












































      doubleprecision FUNCTION R1MACH9 (IDUM)
      INTEGER IDUM
c-----------------------------------------------------------------------
c This routine computes the unit roundoff of the machine.
c This is defined as the smallest positive machine number
c u such that  1.0 + u .ne. 1.0
c
c Subroutines/functions called by R1MACH9.. None
c-----------------------------------------------------------------------
      doubleprecision U, COMP
c
      U = 1.0d0
   10 U = U*0.5d0
      COMP = 1.0d0 + U
      IF (COMP .NE. 1.0d0) GO TO 10
      R1MACH9 = U*2.0d0
      RETURN
c----------------------- End of Function R1MACH9 ------------------------
      END
