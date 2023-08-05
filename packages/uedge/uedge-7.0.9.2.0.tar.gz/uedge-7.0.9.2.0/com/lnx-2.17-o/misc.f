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
c     ./../misc.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c


























































































































































































































      function scal10 (y)
cProlog
c     ------------------------------------------------------------------
c     This service routine can be used to compute a proper scale for
c     graphical output. scal10(y) returns the least in magnitude
c     real value r with abs(r) .ge. abs(y) and which has a decimal
c     representation of the form
c           r  =  0,  or
c           r  =  sgn(y) * i1 * 10.0 ** i2
c     where i1 is 2 or 5 or 10, and i2 is an integer.
c     ------------------------------------------------------------------
      doubleprecision y
      integer i1, i2
      doubleprecision r1
      doubleprecision scal10
      doubleprecision one
      data one /1.d0/
c     ------------------------------------------------------------------
      if (y .eq. 0) then
         scal10 = 0
      else
         i2 = nint(log10(abs(y)) - 0.5d0)
         r1 = abs(y) * 10.0d0 ** (-i2)
c        r1 is in the range (1 .. 10), to machine accuracy.
         if (r1 .le. 2) then
            i1 = 2
         elseif (r1 .le. 5) then
            i1 = 5
         else
            i1 = 10
         endif
         scal10 = sign(one, y) * i1 * 10.0d0 ** (i2)
c xlf95 wants the above.  Cannot replace one by 1.0
      endif
c     ------------------------------------------------------------------
      return
c     ------------------------------------------------------------------
      end

c *********************************************************************
      subroutine quadsvr (neq,xs,xs1,xs2,xs3,ys1,ys2,ys3,yq1,yq2)
cProlog

cc    This routine calculates two guesses to all of the plasma
cc    variables base on a quadratic for the control parameter xs.
cc    The solution closest to the present one is in yq1, and the
cc    second one is in yq2.

      implicit none

c **--input variables--**
c number of equations
      integer neq
c new xs & previous values xs1,xs2, & xs3
      doubleprecision xs,xs1,xs2,xs3
c previous solutions
      doubleprecision ys1(neq),ys2(neq),ys3(neq)
c correponding to xs1, xs2, xs3

c **--output variables--**    # Two solutions to quadratic, yq1 and yq2
c yq1 is closest to solution ys1
      doubleprecision yq1(neq),yq2(neq)

c **--local variables--**
      integer iq
      doubleprecision dn1,dn2,dn3,aq,bq,cq,discr,srt,yqtemp
      doubleprecision epsi
      doubleprecision zero
      data zero /0/
      data epsi/1.d-30/

      do 23000 iq = 1, neq
         dn1 = xs1 / ( (ys2(iq)-ys1(iq))*(ys3(iq)-ys1(iq)) + epsi)
         dn2 = xs2 / ( (ys1(iq)-ys2(iq))*(ys3(iq)-ys2(iq)) + epsi)
         dn3 = xs3 / ( (ys1(iq)-ys3(iq))*(ys2(iq)-ys3(iq)) + epsi)
         aq = dn1 + dn2 + dn3
         bq = - (ys2(iq)+ys3(iq))*dn1 - (ys1(iq)+ys3(iq))*dn2 - (ys1(iq)
     &      +ys2(iq))*dn3
         cq = ys2(iq)*ys3(iq)*dn1 + ys1(iq)*ys3(iq)*dn2 + ys1(iq)*ys2(iq
     &      )*dn3 - xs
         discr = max( bq*bq - 4*aq*cq, zero)
c xlf95 wants the above.  Cannot replace zero by 0.
         srt = sqrt(discr)
         yq1(iq) = 0.5d0 * ( -bq + srt ) / aq
         yq2(iq) = 0.5d0 * ( -bq - srt ) / aq
         if ( abs(ys1(iq)-yq1(iq)) .gt. abs(ys1(iq)-yq2(iq)) ) then
            yqtemp = yq1(iq)
            yq1(iq) = yq2(iq)
            yq2(iq) = yqtemp
         endif
23000 continue

      return
      end
c ****end of subroutine quadsvr**********

c ****Function gettime ******************

      real function gettime(clk)
cProlog
      real clk, rcount, rrate
      integer count, rate
      gettime = 0
      call system_clock(count, rate)
      if (rate .ne. 0) then
         rcount = count
         rrate = rate
         gettime = rcount / rrate
      endif
      return
      end
c ****end of function gettime**********
