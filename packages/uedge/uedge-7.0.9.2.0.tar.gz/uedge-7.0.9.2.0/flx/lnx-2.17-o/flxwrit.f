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
c     ./../flxwrit.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c































































































































































c     ------------------------------------------------------------------
      subroutine flxfin
cProlog
      implicit none

c Group Share
      integer nycore(30), nysol(30), nyout(30), nxleg(30,2)
      character*16 geometry
      integer nxcore(30,2), nxomit, nxxpt, nyomitmx, igrid, nxc, ismpsym
      integer isudsym, islimon, ix_lim, iy_lims, isnonog, ismmon
      integer isoldgrid, isgrdsym, spheromak, isfrc, ishalfm, isbphicon
      character*(256) hdfilename(1:12)
      character*(256) mcfilename(1:12)
      character*120 coronalimpfname
      double precision simagxs, sibdrys, theta_split, cutlo, epslon
      integer nhdf, nzdf, istabon, reset_core_og
      common /com10003/ geometry
      common /com10004/ hdfilename
      common /com10005/ mcfilename
      common /com10006/ coronalimpfname
      common /com80/ nycore, nysol, nyout, nxleg, nxcore, nxomit, nxxpt
      common /com80/ nyomitmx, igrid, nxc, ismpsym, isudsym, islimon
      common /com80/ ix_lim, iy_lims, isnonog, ismmon, isoldgrid
      common /com80/ isgrdsym, spheromak, isfrc, ishalfm, isbphicon
      common /com80/ nhdf, nzdf, istabon, reset_core_og
      common /com83/ simagxs, sibdrys, theta_split, cutlo, epslon
c End of Share
cnycore,nysol,igrid
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,noregs,npts,nxefit,nyefit,nlim,nwork
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
c
c Group Aeqflxgrd
      double precision etime, rseps, zseps, rseps1, zseps1, rseps2
      integer vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop, magpri
      character*128 aeqdskfname
      double precision zseps2, rvsin, zvsin, rvsout, zvsout
      integer nfcoil, nesum

      double precision rco2v ( mco2v)
      pointer(prco2v,rco2v)

      double precision dco2v ( mco2v)
      pointer(pdco2v,dco2v)

      double precision rco2r ( mco2r)
      pointer(prco2r,rco2r)

      double precision dco2r ( mco2r)
      pointer(pdco2r,dco2r)

      double precision csilop ( nsilop)
      pointer(pcsilop,csilop)

      double precision cmpr2 ( magpri)
      pointer(pcmpr2,cmpr2)

      double precision ccbrsp ( nfcoil)
      pointer(pccbrsp,ccbrsp)

      double precision eccurt ( nesum)
      pointer(peccurt,eccurt)
      common /com10002/ aeqdskfname
      common /com50/ vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop
      common /com50/ magpri, nfcoil, nesum
      common /com53/ etime, rseps, zseps, rseps1, zseps1, rseps2, zseps2
      common /com53/ rvsin, zvsin, rvsout, zvsout
      common /com56/ prco2v, pdco2v, prco2r
      common /com56/ pdco2r, pcsilop, pcmpr2
      common /com56/ pccbrsp, peccurt
c End of Aeqflxgrd
c
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Inpf
      integer ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1

      integer iserch ( jdim)
      pointer(piserch,iserch)

      integer jserch ( jdim)
      pointer(pjserch,jserch)

      integer leadir ( jdim)
      pointer(pleadir,leadir)
      common /flx50/ ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      common /flx56/ piserch, pjserch, pleadir
c End of Inpf


      integer nunit
c
c ********* Write the file to be read by the grd package *************

      data nunit /66/
      open (nunit, file='flx-grd', form='unformatted', status='unknown')

      write(nunit) jdim,noregs,npts,nycore(igrid),nysol(igrid)
      write(nunit) jmin,jmax,jsptrx,jaxis
      write(nunit) npoint,xcurve,ycurve
      write(nunit) nxefit,nyefit
      write(nunit) xold,yold,fold
      write(nunit) fpol
      write(nunit) bcentr,rcentr,rmagx,zmagx,simagx,sibdry, rgrid1,xdim,
     &   zdim,zmid
      write(nunit) nlim
      write(nunit) xlim,ylim
      write(nunit) eshot,etime,rseps,zseps, rvsin,zvsin,rvsout,zvsout
      write(nunit) xlbnd,xubnd,ylbnd,yubnd
      write(nunit) runid
      write(nunit) geometry

      close (nunit)

ccc   call remark("***** subroutine flxfin completed")

      return
      end

