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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/grd_basis.d
c     ./../grdread.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































c!include "../mppl.h"
c     ------------------------------------------------------------------

      subroutine copyflx
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

c Group Curves
      double precision xxpoint, yxpoint, rtanpl, ztanpl

      double precision xcurveg ( npts,jdim)
      pointer(pxcurveg,xcurveg)

      double precision ycurveg ( npts,jdim)
      pointer(pycurveg,ycurveg)

      integer npointg ( jdim)
      pointer(pnpointg,npointg)
      common /grd53/ xxpoint, yxpoint, rtanpl, ztanpl
      common /grd56/ pxcurveg, pycurveg, pnpointg
c End of Curves

      integer j,n

      do 23000 j=1,jdim
         npointg(j)=npoint(j)
         do 23002 n=1,npoint(j)
            xcurveg(n,j)=xcurve(n,j)
            ycurveg(n,j)=ycurve(n,j)
23002    continue
23000 continue

      return
      end

c     ------------------------------------------------------------------

      subroutine readflx
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

c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

c Group Curves
      double precision xxpoint, yxpoint, rtanpl, ztanpl

      double precision xcurveg ( npts,jdim)
      pointer(pxcurveg,xcurveg)

      double precision ycurveg ( npts,jdim)
      pointer(pycurveg,ycurveg)

      integer npointg ( jdim)
      pointer(pnpointg,npointg)
      common /grd53/ xxpoint, yxpoint, rtanpl, ztanpl
      common /grd56/ pxcurveg, pycurveg, pnpointg
c End of Curves

c Group Linkco
      double precision yextend, dsmin, dsminx, dyjump, alpha1, dxleft
      integer ixpoint(1:3,1:2), ityp(6,2), ndxleft

      double precision cmeshx ( idim,jdim)
      pointer(pcmeshx,cmeshx)

      double precision cmeshy ( idim,jdim)
      pointer(pcmeshy,cmeshy)
      common /grd60/ ixpoint, ityp, ndxleft
      common /grd63/ yextend, dsmin, dsminx, dyjump, alpha1, dxleft
      common /grd66/ pcmeshx, pcmeshy
c End of Linkco

c Group Transfm

      integer isegment ( npts,jdim)
      pointer(pisegment,isegment)

      integer isys ( mseg,jdim)
      pointer(pisys,isys)

      double precision alphasys ( nalpha)
      pointer(palphasys,alphasys)

      integer ijump ( jdim)
      pointer(pijump,ijump)
      common /grd76/ pisegment, pisys, palphasys
      common /grd76/ pijump
c End of Transfm

c Group Spline

      double precision splcoef ( npts,mseg,jdim)
      pointer(psplcoef,splcoef)

      double precision xknts ( npts,mseg,jdim)
      pointer(pxknts,xknts)

      integer ncap7 ( mseg,jdim)
      pointer(pncap7,ncap7)
      common /grd86/ psplcoef, pxknts, pncap7
c End of Spline

c Group Transit

      double precision xtrans ( npts)
      pointer(pxtrans,xtrans)

      double precision ytrans ( npts)
      pointer(pytrans,ytrans)

      double precision wg ( npts)
      pointer(pwg,wg)
      common /grd116/ pxtrans, pytrans, pwg
c End of Transit

c Group System
      integer ixpointc(1:3,1:2)

      integer istartg ( mseg,jdim)
      pointer(pistartg,istartg)

      integer iendg ( mseg,jdim)
      pointer(piendg,iendg)

      integer m ( mseg,jdim)
      pointer(pm,m)

      integer nseg ( jdim)
      pointer(pnseg,nseg)

      double precision xwork ( npts)
      pointer(pxwork,xwork)

      double precision ywork ( npts)
      pointer(pywork,ywork)

      integer istartc ( noregs)
      pointer(pistartc,istartc)

      integer iendc ( noregs)
      pointer(piendc,iendc)
      common /grd120/ ixpointc
      common /grd126/ pistartg, piendg, pm
      common /grd126/ pnseg, pxwork, pywork
      common /grd126/ pistartc, piendc
c End of System

c Group Mmod
      integer ntop1, ntop2, istream, isupstreamx, nupstream1, nupstream2
      integer ndnstream1, ndnstream2, iplate, nplate1, nplate2, ntop
      integer ntop0, nbot, nupstream, ndnstream, nplate, nplate0
      double precision wtold, fuzzm, delmax, wtmesh1, dmix0, cwtffu
      double precision cwtffd, wtff1, slpxff1, slpxffu1, slpxffd1, wtff2
      integer nsmooth, nff1, nff2, nff, isxtform, iswtform, nxdff1
      double precision slpxff2, slpxffu2, slpxffd2
      integer nxdff2

      double precision cmeshx0 ( idim,jdim)
      pointer(pcmeshx0,cmeshx0)

      double precision cmeshy0 ( idim,jdim)
      pointer(pcmeshy0,cmeshy0)

      double precision dsc ( npts)
      pointer(pdsc,dsc)

      double precision xcrv ( npts)
      pointer(pxcrv,xcrv)

      double precision ycrv ( npts)
      pointer(pycrv,ycrv)

      double precision dsm ( idim)
      pointer(pdsm,dsm)

      double precision dss ( idim)
      pointer(pdss,dss)

      double precision dssleg ( idim)
      pointer(pdssleg,dssleg)

      double precision dsmesh ( idim)
      pointer(pdsmesh,dsmesh)

      double precision dsmesh0 ( idim)
      pointer(pdsmesh0,dsmesh0)

      double precision dsmesh1 ( idim)
      pointer(pdsmesh1,dsmesh1)

      double precision dsmesh2 ( idim)
      pointer(pdsmesh2,dsmesh2)

      double precision xmsh ( idim)
      pointer(pxmsh,xmsh)

      double precision ymsh ( idim)
      pointer(pymsh,ymsh)

      double precision rtop1 ( ntop1)
      pointer(prtop1,rtop1)

      double precision ztop1 ( ntop1)
      pointer(pztop1,ztop1)

      double precision rtop2 ( ntop2)
      pointer(prtop2,rtop2)

      double precision ztop2 ( ntop2)
      pointer(pztop2,ztop2)

      double precision rupstream1 ( nupstream1)
      pointer(prupstream1,rupstream1)

      double precision zupstream1 ( nupstream1)
      pointer(pzupstream1,zupstream1)

      double precision rupstream2 ( nupstream2)
      pointer(prupstream2,rupstream2)

      double precision zupstream2 ( nupstream2)
      pointer(pzupstream2,zupstream2)

      double precision rdnstream1 ( ndnstream1)
      pointer(prdnstream1,rdnstream1)

      double precision zdnstream1 ( ndnstream1)
      pointer(pzdnstream1,zdnstream1)

      double precision rdnstream2 ( ndnstream2)
      pointer(prdnstream2,rdnstream2)

      double precision zdnstream2 ( ndnstream2)
      pointer(pzdnstream2,zdnstream2)

      double precision rplate1 ( nplate1)
      pointer(prplate1,rplate1)

      double precision zplate1 ( nplate1)
      pointer(pzplate1,zplate1)

      double precision rplate2 ( nplate2)
      pointer(prplate2,rplate2)

      double precision zplate2 ( nplate2)
      pointer(pzplate2,zplate2)

      double precision rtop ( nptmp)
      pointer(prtop,rtop)

      double precision ztop ( nptmp)
      pointer(pztop,ztop)

      double precision rtop0 ( nptmp)
      pointer(prtop0,rtop0)

      double precision ztop0 ( nptmp)
      pointer(pztop0,ztop0)

      double precision rbot ( nptmp)
      pointer(prbot,rbot)

      double precision zbot ( nptmp)
      pointer(pzbot,zbot)

      double precision rupstream ( nptmp)
      pointer(prupstream,rupstream)

      double precision zupstream ( nptmp)
      pointer(pzupstream,zupstream)

      double precision rdnstream ( nptmp)
      pointer(prdnstream,rdnstream)

      double precision zdnstream ( nptmp)
      pointer(pzdnstream,zdnstream)

      double precision rplate ( nptmp)
      pointer(prplate,rplate)

      double precision zplate ( nptmp)
      pointer(pzplate,zplate)

      double precision rplate0 ( nptmp)
      pointer(prplate0,rplate0)

      double precision zplate0 ( nptmp)
      pointer(pzplate0,zplate0)

      double precision dsnorm ( idim)
      pointer(pdsnorm,dsnorm)

      double precision wtm1 ( idim)
      pointer(pwtm1,wtm1)

      double precision cmeshx3 ( idim,jdim)
      pointer(pcmeshx3,cmeshx3)

      double precision cmeshy3 ( idim,jdim)
      pointer(pcmeshy3,cmeshy3)

      double precision rff1 ( nff1)
      pointer(prff1,rff1)

      double precision zff1 ( nff1)
      pointer(pzff1,zff1)

      double precision rff2 ( nff2)
      pointer(prff2,rff2)

      double precision zff2 ( nff2)
      pointer(pzff2,zff2)

      double precision rff ( nptmp)
      pointer(prff,rff)

      double precision zff ( nptmp)
      pointer(pzff,zff)

      double precision dsmesh3 ( idim)
      pointer(pdsmesh3,dsmesh3)

      double precision dsmeshff ( idim)
      pointer(pdsmeshff,dsmeshff)
      common /grd140/ ntop1, ntop2, istream, isupstreamx, nupstream1
      common /grd140/ nupstream2, ndnstream1, ndnstream2, iplate
      common /grd140/ nplate1, nplate2, ntop, ntop0, nbot, nupstream
      common /grd140/ ndnstream, nplate, nplate0, nsmooth, nff1, nff2
      common /grd140/ nff, isxtform, iswtform, nxdff1, nxdff2
      common /grd143/ wtold, fuzzm, delmax, wtmesh1, dmix0, cwtffu
      common /grd143/ cwtffd, wtff1, slpxff1, slpxffu1, slpxffd1, wtff2
      common /grd143/ slpxff2, slpxffu2, slpxffd2
      common /grd146/ pcmeshx0, pcmeshy0, pdsc
      common /grd146/ pxcrv, pycrv, pdsm, pdss
      common /grd146/ pdssleg, pdsmesh, pdsmesh0
      common /grd146/ pdsmesh1, pdsmesh2, pxmsh
      common /grd146/ pymsh, prtop1, pztop1
      common /grd146/ prtop2, pztop2, prupstream1
      common /grd146/ pzupstream1, prupstream2
      common /grd146/ pzupstream2, prdnstream1
      common /grd146/ pzdnstream1, prdnstream2
      common /grd146/ pzdnstream2, prplate1, pzplate1
      common /grd146/ prplate2, pzplate2, prtop
      common /grd146/ pztop, prtop0, pztop0
      common /grd146/ prbot, pzbot, prupstream
      common /grd146/ pzupstream, prdnstream
      common /grd146/ pzdnstream, prplate, pzplate
      common /grd146/ prplate0, pzplate0, pdsnorm
      common /grd146/ pwtm1, pcmeshx3, pcmeshy3
      common /grd146/ prff1, pzff1, prff2, pzff2
      common /grd146/ prff, pzff, pdsmesh3
      common /grd146/ pdsmeshff
c End of Mmod

c Group Argfc
      integer nord, mode

      double precision xdatag ( npts)
      pointer(pxdatag,xdatag)

      double precision ydatag ( npts)
      pointer(pydatag,ydatag)

      double precision sddata ( npts)
      pointer(psddata,sddata)

      double precision bkpt ( npts)
      pointer(pbkpt,bkpt)

      double precision xconst ( nconst)
      pointer(pxconst,xconst)

      double precision yconst ( nconst)
      pointer(pyconst,yconst)

      integer nderiv ( nconst)
      pointer(pnderiv,nderiv)

      double precision coeff ( npts)
      pointer(pcoeff,coeff)

      double precision wsla ( nwdim)
      pointer(pwsla,wsla)

      integer iwsla ( niwdim)
      pointer(piwsla,iwsla)
      common /grd90/ nord, mode
      common /grd96/ pxdatag, pydatag, psddata
      common /grd96/ pbkpt, pxconst, pyconst
      common /grd96/ pnderiv, pcoeff, pwsla
      common /grd96/ piwsla
c End of Argfc

      integer iunit, ios
      external remark, xerrab, gallot, gchange
      external rdflx1, rdflx2, rdflx3

c **************** read the output of the flx package ******************

      data iunit /55/
      open (iunit, file='flx-grd', form='unformatted', iostat=ios, 
     &   status='old')
      if (ios .ne. 0) then
         call xerrab("**** flx-grd file not found")
      endif

c     read dimensioning parameters and allot storage space for arrays --

      read(iunit) jdim,noregs,npts,nycore(igrid),nysol(igrid)
      read(iunit) jmin,jmax,jsptrx,jaxis
      call gallot("Dimensions",0)
      call gallot("Curves",0)
      call rdflx1(iunit)

      read(iunit) nxefit,nyefit
c     set length for 2-d spline workspace --
      nwork = nxefit*nyefit + 2*max(kxord*(nxefit+1),kyord*(nyefit+1))
      call gallot("Comflxgrd",0)
      call rdflx2(iunit)

      read(iunit) nlim
      call gchange("Comflxgrd",0)
      call rdflx3(iunit)

      read(iunit) eshot,etime,rseps,zseps, rvsin,zvsin,rvsout,zvsout

      read(iunit) xlbnd,xubnd,ylbnd,yubnd
      read(iunit) runid
      read(iunit) geometry

      close (iunit)

c sets angle-like indices and dimensioning parameters
      call setidim
c for Inmesh, Linkco and Mmod groups
      call gchange("Inmesh",0)
      call gallot("Linkco",0)
      call gallot("Transfm",0)
      call gallot("Spline",0)
      call gallot("Transit",0)
      call gallot("System",0)
      call gchange("Mmod",0)
c     Arrays for SLATEC spline routine FC --
      ndata=npts
      nbkpt=npts
c >=5*(nbkpt-1)+2*max(ndata,nbkpt)+nbkpt+16
      nwdim=8*npts+11
c >=2*(nbkpt-3)
      niwdim=2*npts-6
      call gchange("Argfc",0)

      return
      end

c     ------------------------------------------------------------------

      subroutine rdflx1(iunit)
cProlog
      implicit none
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,npts
c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

c Group Curves
      double precision xxpoint, yxpoint, rtanpl, ztanpl

      double precision xcurveg ( npts,jdim)
      pointer(pxcurveg,xcurveg)

      double precision ycurveg ( npts,jdim)
      pointer(pycurveg,ycurveg)

      integer npointg ( jdim)
      pointer(pnpointg,npointg)
      common /grd53/ xxpoint, yxpoint, rtanpl, ztanpl
      common /grd56/ pxcurveg, pycurveg, pnpointg
c End of Curves

      integer iunit

      read(iunit) npointg,xcurveg,ycurveg

      return
      end

c     ------------------------------------------------------------------

      subroutine rdflx2(iunit)
cProlog
      implicit none
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cnlim,nxefit,nyefit
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

c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

      integer iunit

      read(iunit) xold,yold,fold
      read(iunit) fpol
      read(iunit) bcentr,rcentr,rmagx,zmagx,simagx,sibdry, rgrid1,xdim,
     &   zdim,zmid

      return
      end

c     ------------------------------------------------------------------

      subroutine rdflx3(iunit)
cProlog
      implicit none
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cnlim,nxefit,nyefit
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

c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

      integer iunit

      read(iunit) xlim,ylim

      return
      end

c     ------------------------------------------------------------------

      subroutine readgridpars(fname, runid)
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
c geometry
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nxm,nym
c Group Xpoint_indices
      integer iysptrx

      integer ixlb ( 1:nxpt)
      pointer(pixlb,ixlb)

      integer ixpt1 ( 1:nxpt)
      pointer(pixpt1,ixpt1)

      integer ixmdp ( 1:nxpt)
      pointer(pixmdp,ixmdp)

      integer ixpt2 ( 1:nxpt)
      pointer(pixpt2,ixpt2)

      integer ixrb ( 1:nxpt)
      pointer(pixrb,ixrb)

      integer iysptrx1 ( 1:nxpt)
      pointer(piysptrx1,iysptrx1)

      integer iysptrx2 ( 1:nxpt)
      pointer(piysptrx2,iysptrx2)
      common /com90/ iysptrx
      common /com96/ pixlb, pixpt1, pixmdp
      common /com96/ pixpt2, pixrb, piysptrx1
      common /com96/ piysptrx2
c End of Xpoint_indices
c ixlb,ixpt1,ixmdp,ixpt2,ixrb,iysptrx1,iysptrx2
      character*(*) fname, runid
      integer nuno,ios
      external freeus,remark,xerrab,gallot,rdgrid

c     Read mesh parameters from a UEDGE code grid data file

      call freeus (nuno)
      open (nuno, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab("**** requested grid data file not found")
      endif

      if (geometry.eq."dnull" .or. geometry.eq."snowflake15" .or. 
     &   geometry.eq."snowflake45" .or. geometry.eq."snowflake75" .or. 
     &   geometry.eq."dnXtarget" .or. geometry.eq."isoleg") then
         read(nuno,1999) nxm,nym
         read(nuno,1999) iysptrx1(1),iysptrx2(1)
         read(nuno,1999) ixlb(1),ixpt1(1),ixmdp(1),ixpt2(1),ixrb(1)
         read(nuno,1999) iysptrx1(2),iysptrx2(2)
         read(nuno,1999) ixlb(2),ixpt1(2),ixmdp(2),ixpt2(2),ixrb(2)
         if (geometry.eq."dnXtarget") nxc = ixmdp(1)
      else
         read(nuno,1999) nxm,nym,ixpt1(1),ixpt2(1),iysptrx1(1)
         ixlb(1)=0
         ixrb(1)=nxm
         iysptrx2(1)=iysptrx1(1)
      endif

      close (nuno)

 1999 format(5i4)

      return
      end

c     ------------------------------------------------------------------

      subroutine readgrid(fname, runid)
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
c geometry
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nxm,nym
c Group Xpoint_indices
      integer iysptrx

      integer ixlb ( 1:nxpt)
      pointer(pixlb,ixlb)

      integer ixpt1 ( 1:nxpt)
      pointer(pixpt1,ixpt1)

      integer ixmdp ( 1:nxpt)
      pointer(pixmdp,ixmdp)

      integer ixpt2 ( 1:nxpt)
      pointer(pixpt2,ixpt2)

      integer ixrb ( 1:nxpt)
      pointer(pixrb,ixrb)

      integer iysptrx1 ( 1:nxpt)
      pointer(piysptrx1,iysptrx1)

      integer iysptrx2 ( 1:nxpt)
      pointer(piysptrx2,iysptrx2)
      common /com90/ iysptrx
      common /com96/ pixlb, pixpt1, pixmdp
      common /com96/ pixpt2, pixrb, piysptrx1
      common /com96/ piysptrx2
c End of Xpoint_indices
c ixlb,ixpt1,ixmdp,ixpt2,ixrb,iysptrx1,iysptrx2
      character*(*) fname, runid
      integer nuno,ios
      external freeus,remark,xerrab,gallot,rdgrid

c     Read a UEDGE code grid data file

      call freeus (nuno)
      open (nuno, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab("**** requested grid data file not found")
      endif

      if (geometry.eq."dnull" .or. geometry.eq."snowflake15" .or. 
     &   geometry.eq."snowflake45" .or. geometry.eq."snowflake75" .or. 
     &   geometry.eq."dnXtarget" .or. geometry.eq."isoleg") then
         read(nuno,1999) nxm,nym
         read(nuno,1999) iysptrx1(1),iysptrx2(1)
         read(nuno,1999) ixlb(1),ixpt1(1),ixmdp(1),ixpt2(1),ixrb(1)
         read(nuno,1999) iysptrx1(2),iysptrx2(2)
         read(nuno,1999) ixlb(2),ixpt1(2),ixmdp(2),ixpt2(2),ixrb(2)
         if (geometry.eq."dnXtarget") nxc = ixmdp(1)
      else
         read(nuno,1999) nxm,nym,ixpt1(1),ixpt2(1),iysptrx1(1)
         ixlb(1)=0
         ixrb(1)=nxm
         iysptrx2(1)=iysptrx1(1)
      endif
 1999 format(5i4)
      call gallot("RZ_grid_info",0)
      call rdgrid(nuno, runid)

      close (nuno)

      return
      end

c     ------------------------------------------------------------------

      subroutine rdgrid(nuno, runid)
cProlog
      implicit none
      integer nuno
      character*(*) runid

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nxm,nym
c Group RZ_grid_info

      double precision rm ( 0:nxm+1,0:nym+1,0:4)
      pointer(prm,rm)

      double precision zm ( 0:nxm+1,0:nym+1,0:4)
      pointer(pzm,zm)

      double precision rmt ( 0:nxm+1,0:nym+1,0:4)
      pointer(prmt,rmt)

      double precision zmt ( 0:nxm+1,0:nym+1,0:4)
      pointer(pzmt,zmt)

      double precision rv ( 0:nxm+2,-1:nym+1)
      pointer(prv,rv)

      double precision zv ( 0:nxm+2,-1:nym+1)
      pointer(pzv,zv)

      double precision psi ( 0:nxm+1,0:nym+1,0:4)
      pointer(ppsi,psi)

      double precision br ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbr,br)

      double precision bz ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbz,bz)

      double precision bpol ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbpol,bpol)

      double precision bphi ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbphi,bphi)

      double precision b ( 0:nxm+1,0:nym+1,0:4)
      pointer(pb,b)

      double precision bsqr ( 0:nxm+1,0:nym+1)
      pointer(pbsqr,bsqr)

      double precision b12 ( 0:nxm+1,0:nym+1)
      pointer(pb12,b12)

      double precision b12ctr ( 0:nxm+1,0:nym+1)
      pointer(pb12ctr,b12ctr)

      double precision b32 ( 0:nxm+1,0:nym+1)
      pointer(pb32,b32)
      common /com66/ prm, pzm, prmt, pzmt
      common /com66/ prv, pzv, ppsi, pbr
      common /com66/ pbz, pbpol, pbphi, pb
      common /com66/ pbsqr, pb12, pb12ctr, pb32
c End of RZ_grid_info
c rm,zm,psi,br,bz,bpol,bphi,b

      integer ix,iy,n

      read(nuno,2000)
      read(nuno,2001) (((rm(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((zm(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((psi(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((br(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((bz(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((bpol(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((bphi(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2000)
      read(nuno,2001) (((b(ix,iy,n),ix=0,nxm+1),iy=0,nym+1),n=0,4)
      read(nuno,2002) runid
 2000 format()
 2001 format(1p3d23.15)
 2002 format(a60)

      return
      end

c----------------------------------------------------------------------#

      subroutine setidim
cProlog
      implicit none
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,npts,noregs
c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

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
c islimon
c Group Linkco
      double precision yextend, dsmin, dsminx, dyjump, alpha1, dxleft
      integer ixpoint(1:3,1:2), ityp(6,2), ndxleft

      double precision cmeshx ( idim,jdim)
      pointer(pcmeshx,cmeshx)

      double precision cmeshy ( idim,jdim)
      pointer(pcmeshy,cmeshy)
      common /grd60/ ixpoint, ityp, ndxleft
      common /grd63/ yextend, dsmin, dsminx, dyjump, alpha1, dxleft
      common /grd66/ pcmeshx, pcmeshy
c End of Linkco

c Group Inmesh
      double precision rstrike(1:2), zstrike(1:2), rtpnew(1:2)
      double precision ztpnew(1:2), epslon_lim, dalpha
      integer isspnew, istpnew, istptest(1:2), ilmax(1:2), isztest(1:2)

      double precision seedxp ( idim,noregs)
      pointer(pseedxp,seedxp)

      double precision seedxpxl ( idim,noregs)
      pointer(pseedxpxl,seedxpxl)

      double precision seed ( idim,noregs)
      pointer(pseed,seed)

      double precision dissep ( npts,noregs)
      pointer(pdissep,dissep)

      double precision distxp ( noregs)
      pointer(pdistxp,distxp)

      double precision distxpxl ( noregs)
      pointer(pdistxpxl,distxpxl)

      double precision x0g ( noregs)
      pointer(px0g,x0g)

      double precision xlast ( noregs)
      pointer(pxlast,xlast)

      double precision y0g ( noregs)
      pointer(py0g,y0g)

      double precision ylast ( noregs)
      pointer(pylast,ylast)
      common /grd100/ isspnew, istpnew, istptest, ilmax, isztest
      common /grd103/ rstrike, zstrike, rtpnew, ztpnew, epslon_lim
      common /grd103/ dalpha
      common /grd106/ pseedxp, pseedxpxl, pseed
      common /grd106/ pdissep, pdistxp, pdistxpxl
      common /grd106/ px0g, pxlast, py0g, pylast
c End of Inmesh

c Group Mmod
      integer ntop1, ntop2, istream, isupstreamx, nupstream1, nupstream2
      integer ndnstream1, ndnstream2, iplate, nplate1, nplate2, ntop
      integer ntop0, nbot, nupstream, ndnstream, nplate, nplate0
      double precision wtold, fuzzm, delmax, wtmesh1, dmix0, cwtffu
      double precision cwtffd, wtff1, slpxff1, slpxffu1, slpxffd1, wtff2
      integer nsmooth, nff1, nff2, nff, isxtform, iswtform, nxdff1
      double precision slpxff2, slpxffu2, slpxffd2
      integer nxdff2

      double precision cmeshx0 ( idim,jdim)
      pointer(pcmeshx0,cmeshx0)

      double precision cmeshy0 ( idim,jdim)
      pointer(pcmeshy0,cmeshy0)

      double precision dsc ( npts)
      pointer(pdsc,dsc)

      double precision xcrv ( npts)
      pointer(pxcrv,xcrv)

      double precision ycrv ( npts)
      pointer(pycrv,ycrv)

      double precision dsm ( idim)
      pointer(pdsm,dsm)

      double precision dss ( idim)
      pointer(pdss,dss)

      double precision dssleg ( idim)
      pointer(pdssleg,dssleg)

      double precision dsmesh ( idim)
      pointer(pdsmesh,dsmesh)

      double precision dsmesh0 ( idim)
      pointer(pdsmesh0,dsmesh0)

      double precision dsmesh1 ( idim)
      pointer(pdsmesh1,dsmesh1)

      double precision dsmesh2 ( idim)
      pointer(pdsmesh2,dsmesh2)

      double precision xmsh ( idim)
      pointer(pxmsh,xmsh)

      double precision ymsh ( idim)
      pointer(pymsh,ymsh)

      double precision rtop1 ( ntop1)
      pointer(prtop1,rtop1)

      double precision ztop1 ( ntop1)
      pointer(pztop1,ztop1)

      double precision rtop2 ( ntop2)
      pointer(prtop2,rtop2)

      double precision ztop2 ( ntop2)
      pointer(pztop2,ztop2)

      double precision rupstream1 ( nupstream1)
      pointer(prupstream1,rupstream1)

      double precision zupstream1 ( nupstream1)
      pointer(pzupstream1,zupstream1)

      double precision rupstream2 ( nupstream2)
      pointer(prupstream2,rupstream2)

      double precision zupstream2 ( nupstream2)
      pointer(pzupstream2,zupstream2)

      double precision rdnstream1 ( ndnstream1)
      pointer(prdnstream1,rdnstream1)

      double precision zdnstream1 ( ndnstream1)
      pointer(pzdnstream1,zdnstream1)

      double precision rdnstream2 ( ndnstream2)
      pointer(prdnstream2,rdnstream2)

      double precision zdnstream2 ( ndnstream2)
      pointer(pzdnstream2,zdnstream2)

      double precision rplate1 ( nplate1)
      pointer(prplate1,rplate1)

      double precision zplate1 ( nplate1)
      pointer(pzplate1,zplate1)

      double precision rplate2 ( nplate2)
      pointer(prplate2,rplate2)

      double precision zplate2 ( nplate2)
      pointer(pzplate2,zplate2)

      double precision rtop ( nptmp)
      pointer(prtop,rtop)

      double precision ztop ( nptmp)
      pointer(pztop,ztop)

      double precision rtop0 ( nptmp)
      pointer(prtop0,rtop0)

      double precision ztop0 ( nptmp)
      pointer(pztop0,ztop0)

      double precision rbot ( nptmp)
      pointer(prbot,rbot)

      double precision zbot ( nptmp)
      pointer(pzbot,zbot)

      double precision rupstream ( nptmp)
      pointer(prupstream,rupstream)

      double precision zupstream ( nptmp)
      pointer(pzupstream,zupstream)

      double precision rdnstream ( nptmp)
      pointer(prdnstream,rdnstream)

      double precision zdnstream ( nptmp)
      pointer(pzdnstream,zdnstream)

      double precision rplate ( nptmp)
      pointer(prplate,rplate)

      double precision zplate ( nptmp)
      pointer(pzplate,zplate)

      double precision rplate0 ( nptmp)
      pointer(prplate0,rplate0)

      double precision zplate0 ( nptmp)
      pointer(pzplate0,zplate0)

      double precision dsnorm ( idim)
      pointer(pdsnorm,dsnorm)

      double precision wtm1 ( idim)
      pointer(pwtm1,wtm1)

      double precision cmeshx3 ( idim,jdim)
      pointer(pcmeshx3,cmeshx3)

      double precision cmeshy3 ( idim,jdim)
      pointer(pcmeshy3,cmeshy3)

      double precision rff1 ( nff1)
      pointer(prff1,rff1)

      double precision zff1 ( nff1)
      pointer(pzff1,zff1)

      double precision rff2 ( nff2)
      pointer(prff2,rff2)

      double precision zff2 ( nff2)
      pointer(pzff2,zff2)

      double precision rff ( nptmp)
      pointer(prff,rff)

      double precision zff ( nptmp)
      pointer(pzff,zff)

      double precision dsmesh3 ( idim)
      pointer(pdsmesh3,dsmesh3)

      double precision dsmeshff ( idim)
      pointer(pdsmeshff,dsmeshff)
      common /grd140/ ntop1, ntop2, istream, isupstreamx, nupstream1
      common /grd140/ nupstream2, ndnstream1, ndnstream2, iplate
      common /grd140/ nplate1, nplate2, ntop, ntop0, nbot, nupstream
      common /grd140/ ndnstream, nplate, nplate0, nsmooth, nff1, nff2
      common /grd140/ nff, isxtform, iswtform, nxdff1, nxdff2
      common /grd143/ wtold, fuzzm, delmax, wtmesh1, dmix0, cwtffu
      common /grd143/ cwtffd, wtff1, slpxff1, slpxffu1, slpxffd1, wtff2
      common /grd143/ slpxff2, slpxffu2, slpxffd2
      common /grd146/ pcmeshx0, pcmeshy0, pdsc
      common /grd146/ pxcrv, pycrv, pdsm, pdss
      common /grd146/ pdssleg, pdsmesh, pdsmesh0
      common /grd146/ pdsmesh1, pdsmesh2, pxmsh
      common /grd146/ pymsh, prtop1, pztop1
      common /grd146/ prtop2, pztop2, prupstream1
      common /grd146/ pzupstream1, prupstream2
      common /grd146/ pzupstream2, prdnstream1
      common /grd146/ pzdnstream1, prdnstream2
      common /grd146/ pzdnstream2, prplate1, pzplate1
      common /grd146/ prplate2, pzplate2, prtop
      common /grd146/ pztop, prtop0, pztop0
      common /grd146/ prbot, pzbot, prupstream
      common /grd146/ pzupstream, prdnstream
      common /grd146/ pzdnstream, prplate, pzplate
      common /grd146/ prplate0, pzplate0, pdsnorm
      common /grd146/ pwtm1, pcmeshx3, pcmeshy3
      common /grd146/ prff1, pzff1, prff2, pzff2
      common /grd146/ prff, pzff, pdsmesh3
      common /grd146/ pdsmeshff
c End of Mmod

c Group Xmesh
      double precision slpxt, alfx(2), dxgas(2), dt1, dx1, dt2, dx2
      integer ndat, kxmesh, nxgas(2), ileft, iright, kord, ndatp2
      double precision dleft, dright
      integer kntopt, iflag1

      double precision xdat ( ndat)
      pointer(pxdat,xdat)

      double precision tdat ( ndat)
      pointer(ptdat,tdat)

      double precision tknt ( ndatp2+4)
      pointer(ptknt,tknt)

      double precision z1work ( 5*ndat+2)
      pointer(pz1work,z1work)

      double precision z1cscoef ( ndatp2)
      pointer(pz1cscoef,z1cscoef)

      double precision wrk1 ( 3*kord)
      pointer(pwrk1,wrk1)
      common /grd160/ ndat, kxmesh, nxgas, ileft, iright, kord, ndatp2
      common /grd160/ kntopt, iflag1
      common /grd163/ slpxt, alfx, dxgas, dt1, dx1, dt2, dx2, dleft
      common /grd163/ dright
      common /grd166/ pxdat, ptdat, ptknt
      common /grd166/ pz1work, pz1cscoef, pwrk1
c End of Xmesh

      integer region
      external gchange

c     Set angle-like parameters and allocate space for arrays --

      if ( (geometry .eq. "dnbot") .or. (geometry .eq. "dnull") .or. (
     &   geometry .eq. "isoleg") .or. (islimon .ne. 0) ) then
c nxcore includes guard cells
         nxuse(1) = max(0,nxcore(igrid,1)-1)
c at the internal mesh boundaries
         nxuse(2) = nxcore(igrid,2) - 1
      else
c nxcore specifies the number
         nxuse(1) = nxcore(igrid,1)
c of finite-size cells
         nxuse(2) = nxcore(igrid,2)
      endif

c     Set some angle-surface parameters --
      idim=0
      do 23000 region=1,noregs
         ixpoint(1,region) = nxuse(region) + 1
         ixpoint(2,region) = ixpoint(1,region) + 1
         ixpoint(3,region) = ixpoint(2,region) + 1
         ilmax(region) = ixpoint(3,region) + nxleg(igrid,region)
         idim = max( idim, ilmax(region) )
23000 continue

c     Allocate space for angle-dependent arrays --
      call gchange("Linkco",0)
      call gchange("Inmesh",0)
      call gchange("Mmod",0)

c     and for poloidal mesh distribution data --
      call gchange("Xmesh",0)

      return
      end

