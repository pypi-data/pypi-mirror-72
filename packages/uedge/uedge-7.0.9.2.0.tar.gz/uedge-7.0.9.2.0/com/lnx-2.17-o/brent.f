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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/aph.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/api_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/bbb_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/grd_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/flx_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/wdf.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/com.d
c     ./../brent.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c


























































































































































































































      doubleprecision FUNCTION BRENT(iprint,ITMAX,AX,BX,CX,F,TOL,XMIN)
c ... Given a function F, and given a bracketing triplet of abscissas
c     AX, BX, CX (such that BX is between AX and CX, and F(BX) is less
c     than both F(AX) and F(CX)), this routine isolates the minimum to
c     a fractional precision of about TOL using Brent's method.  The
c     abscissa of the minimum is returned as XMIN, and the minimum
c     function value is returned as BRENT, the returned function value.
c ... This version of BRENT uses an additional (first) argument ITMAX,
c     the maximum allowed number of iterations, and returns to the
c     Basis parser by calling kaboom if convergence is not achieved in
c     ITMAX iterations.

      implicit none

c ... Input variables:
      integer iprint
      integer ITMAX
      doubleprecision AX, BX, CX, TOL

c ... Output variable:
      doubleprecision XMIN

c ... External function:
      external F
      doubleprecision F

c ... Local variables:
      integer ITER
      doubleprecision A, B, D, ETEMP, FU, FV, FW, FX, P, Q, R, TOL1, 
     &   TOL2
      doubleprecision U, V, W, X, XM, E

c ... CGOLD is the golden ratio; ZEPS is a small number that protects
c     against trying to achieve fractional accuracy for a minimum that
c     happens to be exactly zero.
      doubleprecision CGOLD, ZEPS
      PARAMETER (CGOLD=.3819660d0)
      ZEPS = tol

c ... Description of the algorithm is in "Numerical Recipes in C" by
c     W.H. Press, et al., Sec. 10.2.
      A=MIN(AX,CX)
      B=MAX(AX,CX)
      V=BX
      W=V
      X=V
      E=0.d0
      FX=F(X)
      FV=FX
      FW=FX
      DO 11 ITER=1,ITMAX
      if (iprint .gt. 1) write(*,90) 'brent:  iteration ', ITER, 
     &      ' -- test point has f(', X, ') = ', FX
   90 format(a,i2,2(a,f11.7))
      XM=0.5d0*(A+B)
      TOL1=TOL*ABS(X)+ZEPS
      TOL2=2.d0*TOL1
      IF(ABS(X-XM).LE.(TOL2-.5d0*(B-A))) GOTO 3
      IF(ABS(E).GT.TOL1) THEN
      R=(X-W)*(FX-FV)
      Q=(X-V)*(FX-FW)
      P=(X-V)*Q-(X-W)*R
      Q=2.d0*(Q-R)
      IF(Q.GT.0.d0) P=-P
      Q=ABS(Q)
      ETEMP=E
      E=D
      IF(ABS(P).GE.ABS(.5d0*Q*ETEMP).OR.P.LE.Q*(A-X).OR. P.GE.Q*(B-X)) 
     &   GOTO 1
      D=P/Q
      U=X+D
      IF(U-A.LT.TOL2 .OR. B-U.LT.TOL2) D=SIGN(TOL1,XM-X)
      GOTO 2
      ENDIF
    1 IF(X.GE.XM) THEN
      E=A-X
      ELSE
      E=B-X
      ENDIF
      D=CGOLD*E
    2 IF(ABS(D).GE.TOL1) THEN
      U=X+D
      ELSE
      U=X+SIGN(TOL1,D)
      ENDIF
      FU=F(U)
      IF(FU.LE.FX) THEN
      IF(U.GE.X) THEN
      A=X
      ELSE
      B=X
      ENDIF
      V=W
      FV=FW
      W=X
      FW=FX
      X=U
      FX=FU
      ELSE
      IF(U.LT.X) THEN
      A=U
      ELSE
      B=U
      ENDIF
      IF(FU.LE.FW .OR. W.EQ.X) THEN
      V=W
      FV=FW
      W=U
      FW=FU
      ELSE IF(FU.LE.FV .OR. V.EQ.X .OR. V.EQ.W) THEN
      V=U
      FV=FU
      ENDIF
      ENDIF
   11 CONTINUE
      call xerrab ('*** brent exceeded maximum iterations.')
    3 XMIN=X
      BRENT=FX
      if (iprint .ge. 1) write(*,91) 'brent:  final point has f(', X, 
     &      ') = ', FX
   91 format(2(a,f11.7))
      RETURN
      END
