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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/com.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/bbb_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/flx_basis.d
c     ./../flxdriv.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c































































































































































c     ------------------------------------------------------------------

      subroutine flxrun
cProlog
      implicit none
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd

c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis

      double precision xold ( nxefit)
      pointer(pxold,xold)

      double precision yold ( nyefit)
      pointer(pyold,yold)

      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)

      double precision workk ( nxefit)
      pointer(pworkk,workk)

      double precision fpol ( nxefit)
      pointer(pfpol,fpol)

      double precision pres ( nxefit)
      pointer(ppres,pres)

      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)

      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)

      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)

      double precision xlim ( nlim)
      pointer(pxlim,xlim)

      double precision ylim ( nlim)
      pointer(pylim,ylim)

      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)

      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)

      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)

      double precision work ( nwork)
      pointer(pwork,work)

      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)

      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)

      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd


c     main driver routine for flx package
      call inflx
      call flxgen
c## No need to write flx-grd file (MER 08 Feb 2010)
c## These variables are now in com package and accessible to both flx and grd
      if (isfw.eq.1) call flxfin

      return
      end

