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
c     ./grd_basis.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































      subroutine grdinit0
cProlog
c initializes a Package
      integer drtdm
      common /grdrtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("grd")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call grddata
      call grdwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data grdiyiyi
c Replace pointer statements with Address types


c Group Dim_vars

      integer nx, ny, nxm, nym
      common /grd00/ nx, ny, nxm, nym
c End of Dim_vars

c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

c Group Analgrd
      double precision radm, radx, rad0, rscalcore, za0, zax, zaxpt
      double precision tiltang, zxpt_reset, alfyt, tnoty, sratiopf
      double precision alfxt, tctr, bpolfix, btfix, agsindx, agsrsp
      double precision rnod
      integer ixsnog, isadjalfxt, isgdistort, iynod, ixdstar
      common /grd20/ ixsnog, isadjalfxt, isgdistort, iynod, ixdstar
      common /grd23/ radm, radx, rad0, rscalcore, za0, zax, zaxpt
      common /grd23/ tiltang, zxpt_reset, alfyt, tnoty, sratiopf, alfxt
      common /grd23/ tctr, bpolfix, btfix, agsindx, agsrsp, rnod
c End of Analgrd

c Group Torannulus
      double precision acore, rm0, edgewid, dthlim, bpol0, btor0
      integer ibpmodel
      integer*8 pradf
      integer*8 pthpf
      common /grd30/ ibpmodel
      common /grd33/ acore, rm0, edgewid, dthlim, bpol0, btor0
      common /grd36/ pradf, pthpf
c End of Torannulus

c Group Magmirror
      integer nzc, nrc
      integer*8 pzu
      integer*8 pru
      integer*8 pbzu
      integer*8 pbru
      integer*8 pbmag
      common /grd40/ nzc, nrc
      common /grd46/ pzu, pru, pbzu, pbru
      common /grd46/ pbmag
c End of Magmirror

c Group Curves
      double precision xxpoint, yxpoint, rtanpl, ztanpl
      integer*8 pxcurveg
      integer*8 pycurveg
      integer*8 pnpointg
      common /grd53/ xxpoint, yxpoint, rtanpl, ztanpl
      common /grd56/ pxcurveg, pycurveg, pnpointg
c End of Curves

c Group Linkco
      double precision yextend, dsmin, dsminx, dyjump, alpha1, dxleft
      integer ixpoint(1:3,1:2), ityp(6,2), ndxleft
      integer*8 pcmeshx
      integer*8 pcmeshy
      common /grd60/ ixpoint, ityp, ndxleft
      common /grd63/ yextend, dsmin, dsminx, dyjump, alpha1, dxleft
      common /grd66/ pcmeshx, pcmeshy
c End of Linkco

c Group Transfm
      integer*8 pisegment
      integer*8 pisys
      integer*8 palphasys
      integer*8 pijump
      common /grd76/ pisegment, pisys, palphasys
      common /grd76/ pijump
c End of Transfm

c Group Spline
      integer*8 psplcoef
      integer*8 pxknts
      integer*8 pncap7
      common /grd86/ psplcoef, pxknts, pncap7
c End of Spline

c Group Argfc
      integer nord, mode
      integer*8 pxdatag
      integer*8 pydatag
      integer*8 psddata
      integer*8 pbkpt
      integer*8 pxconst
      integer*8 pyconst
      integer*8 pnderiv
      integer*8 pcoeff
      integer*8 pwsla
      integer*8 piwsla
      common /grd90/ nord, mode
      common /grd96/ pxdatag, pydatag, psddata
      common /grd96/ pbkpt, pxconst, pyconst
      common /grd96/ pnderiv, pcoeff, pwsla
      common /grd96/ piwsla
c End of Argfc

c Group Inmesh
      double precision rstrike(1:2), zstrike(1:2), rtpnew(1:2)
      double precision ztpnew(1:2), epslon_lim, dalpha
      integer isspnew, istpnew, istptest(1:2), ilmax(1:2), isztest(1:2)
      integer*8 pseedxp
      integer*8 pseedxpxl
      integer*8 pseed
      integer*8 pdissep
      integer*8 pdistxp
      integer*8 pdistxpxl
      integer*8 px0g
      integer*8 pxlast
      integer*8 py0g
      integer*8 pylast
      common /grd100/ isspnew, istpnew, istptest, ilmax, isztest
      common /grd103/ rstrike, zstrike, rtpnew, ztpnew, epslon_lim
      common /grd103/ dalpha
      common /grd106/ pseedxp, pseedxpxl, pseed
      common /grd106/ pdissep, pdistxp, pdistxpxl
      common /grd106/ px0g, pxlast, py0g, pylast
c End of Inmesh

c Group Transit
      integer*8 pxtrans
      integer*8 pytrans
      integer*8 pwg
      common /grd116/ pxtrans, pytrans, pwg
c End of Transit

c Group System
      integer ixpointc(1:3,1:2)
      integer*8 pistartg
      integer*8 piendg
      integer*8 pm
      integer*8 pnseg
      integer*8 pxwork
      integer*8 pywork
      integer*8 pistartc
      integer*8 piendc
      common /grd120/ ixpointc
      common /grd126/ pistartg, piendg, pm
      common /grd126/ pnseg, pxwork, pywork
      common /grd126/ pistartc, piendc
c End of System

c Group UEgrid
      integer ixtop
      common /grd130/ ixtop
c End of UEgrid

c Group Mmod
      integer ntop1, ntop2, istream, isupstreamx, nupstream1, nupstream2
      integer ndnstream1, ndnstream2, iplate, nplate1, nplate2, ntop
      integer ntop0, nbot, nupstream, ndnstream, nplate, nplate0
      double precision wtold, fuzzm, delmax, wtmesh1, dmix0, cwtffu
      double precision cwtffd, wtff1, slpxff1, slpxffu1, slpxffd1, wtff2
      integer nsmooth, nff1, nff2, nff, isxtform, iswtform, nxdff1
      double precision slpxff2, slpxffu2, slpxffd2
      integer nxdff2
      integer*8 pcmeshx0
      integer*8 pcmeshy0
      integer*8 pdsc
      integer*8 pxcrv
      integer*8 pycrv
      integer*8 pdsm
      integer*8 pdss
      integer*8 pdssleg
      integer*8 pdsmesh
      integer*8 pdsmesh0
      integer*8 pdsmesh1
      integer*8 pdsmesh2
      integer*8 pxmsh
      integer*8 pymsh
      integer*8 prtop1
      integer*8 pztop1
      integer*8 prtop2
      integer*8 pztop2
      integer*8 prupstream1
      integer*8 pzupstream1
      integer*8 prupstream2
      integer*8 pzupstream2
      integer*8 prdnstream1
      integer*8 pzdnstream1
      integer*8 prdnstream2
      integer*8 pzdnstream2
      integer*8 prplate1
      integer*8 pzplate1
      integer*8 prplate2
      integer*8 pzplate2
      integer*8 prtop
      integer*8 pztop
      integer*8 prtop0
      integer*8 pztop0
      integer*8 prbot
      integer*8 pzbot
      integer*8 prupstream
      integer*8 pzupstream
      integer*8 prdnstream
      integer*8 pzdnstream
      integer*8 prplate
      integer*8 pzplate
      integer*8 prplate0
      integer*8 pzplate0
      integer*8 pdsnorm
      integer*8 pwtm1
      integer*8 pcmeshx3
      integer*8 pcmeshy3
      integer*8 prff1
      integer*8 pzff1
      integer*8 prff2
      integer*8 pzff2
      integer*8 prff
      integer*8 pzff
      integer*8 pdsmesh3
      integer*8 pdsmeshff
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

c Group Refinex
      double precision alfxptl, alfxpt2l, alfxptu, alfxpt2u, alfxpt
      double precision alfxpt2
      integer isrefxptn, nxmod, nflux, nsmoothx
      integer*8 prsu
      integer*8 pzsu
      integer*8 prsx
      integer*8 pzsx
      integer*8 prflux
      integer*8 pzflux
      integer*8 pdsflux
      integer*8 prmm
      integer*8 pzmm
      common /grd150/ isrefxptn, nxmod, nflux, nsmoothx
      common /grd153/ alfxptl, alfxpt2l, alfxptu, alfxpt2u, alfxpt
      common /grd153/ alfxpt2
      common /grd156/ prsu, pzsu, prsx, pzsx
      common /grd156/ prflux, pzflux, pdsflux
      common /grd156/ prmm, pzmm
c End of Refinex

c Group Xmesh
      double precision slpxt, alfx(2), dxgas(2), dt1, dx1, dt2, dx2
      integer ndat, kxmesh, nxgas(2), ileft, iright, kord, ndatp2
      double precision dleft, dright
      integer kntopt, iflag1
      integer*8 pxdat
      integer*8 ptdat
      integer*8 ptknt
      integer*8 pz1work
      integer*8 pz1cscoef
      integer*8 pwrk1
      common /grd160/ ndat, kxmesh, nxgas, ileft, iright, kord, ndatp2
      common /grd160/ kntopt, iflag1
      common /grd163/ slpxt, alfx, dxgas, dt1, dx1, dt2, dx2, dleft
      common /grd163/ dright
      common /grd166/ pxdat, ptdat, ptknt
      common /grd166/ pz1work, pz1cscoef, pwrk1
c End of Xmesh

c Group Dnull_temp
      integer nxmb, nymb, ixpt1b, ixtopb, ixpt2b, iysptrxb, nxmu, nymu
      integer ixpt1u, ixtopu, ixpt2u, iysptrxu
      integer*8 prmb
      integer*8 pzmb
      integer*8 prmu
      integer*8 pzmu
      common /grd170/ nxmb, nymb, ixpt1b, ixtopb, ixpt2b, iysptrxb, nxmu
      common /grd170/ nymu, ixpt1u, ixtopu, ixpt2u, iysptrxu
      common /grd176/ prmb, pzmb, prmu, pzmu
c End of Dnull_temp

c Group Expseed
      double precision fraclplt(2), alfxdiv(2), alfxcore(2)
      double precision shift_seed_leg(2), shift_seed_core(2), fcorenunif
      integer nxlplt(2), nxlxpt(2)
      common /grd180/ nxlplt, nxlxpt
      common /grd183/ fraclplt, alfxdiv, alfxcore, shift_seed_leg
      common /grd183/ shift_seed_core, fcorenunif
c End of Expseed

c Group Xfcn
c End of Xfcn

c Group Driver
c End of Driver


      data nix/3/,mseg/15/,nalpha/4/,nptmp/300/,nconst/0/
      data radm/-1.d-4/,radx/0.04d0/,rad0/0.d0/,rscalcore/1.d0/,za0/0.d0
     &   /
      data zax/1.d0/,zaxpt/.75d0/,tiltang/0.d0/,ixsnog/1/,zxpt_reset/
     &   0.d0/
      data alfyt/-2.d0/,tnoty/0.d0/,sratiopf/0.d0/,alfxt/4.0d0/,
     &   isadjalfxt/0/
      data tctr/0.d0/,bpolfix/.3d0/,btfix/5.d0/,isgdistort/0/,agsindx/
     &   0.d0/
      data agsrsp/0.d0/,iynod/0/,rnod/0.d0/,ixdstar/1/
      data acore/0.5d0/,rm0/2.d0/,edgewid/0.1d0/,dthlim/1d-4/,bpol0/
     &   0.2d0/
      data btor0/2.d0/,ibpmodel/0/
      data yextend/0.d0/,dsmin/0.d0/,alpha1/45.0d0/
      data ityp/0,0,0,1,1,2,1,1,2,0,0,0/,dxleft/0.d0/,ndxleft/0/
      data nord/4/
      data isspnew/0/,istpnew/0/,istptest/2*0/,isztest/2*0/
      data epslon_lim/1.d-3/,dalpha/5.d0/
      data istream/0/,isupstreamx/0/,iplate/0/,wtold/0.5d0/,nsmooth/2/
      data fuzzm/1.0d-08/,delmax/1.0d-08/,wtmesh1/0.5d0/,dmix0/0.d0/
      data cwtffu/1.d0/,cwtffd/1.d0/,isxtform/1/,iswtform/0/,nxdff1/0/
      data nxdff2/0/
      data isrefxptn/1/,nxmod/2/,alfxptl/1.d0/,alfxpt2l/1.d0/,alfxptu/
     &   1.d0/
      data alfxpt2u/1.d0/,alfxpt/1.d0/,alfxpt2/1.d0/,nsmoothx/8/
      data ndat/7/,kxmesh/1/,slpxt/1.0d0/,alfx/2*0.1d0/,ileft/0/
      data dleft/0.0d0/,iright/0/,dright/0.0d0/,kord/4/,ndatp2/9/
      data kntopt/1/
      data fraclplt/.6d0,.6d0/,alfxdiv/.18d0,.18d0/,alfxcore/.4d0,.4d0/
      data shift_seed_leg/0.d0,0.d0/,shift_seed_core/1.d0,1.d0/,nxlplt/
     &   12,12/
      data nxlxpt/4,4/,fcorenunif/0.8d0/

      end
c restore definition from mppl.BASIS

      subroutine grddata
cProlog

c Group Dim_vars

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd


      integer nx, ny, nxm, nym
      common /grd00/ nx, ny, nxm, nym
c End of Dim_vars

c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

c Group Analgrd
      double precision radm, radx, rad0, rscalcore, za0, zax, zaxpt
      double precision tiltang, zxpt_reset, alfyt, tnoty, sratiopf
      double precision alfxt, tctr, bpolfix, btfix, agsindx, agsrsp
      double precision rnod
      integer ixsnog, isadjalfxt, isgdistort, iynod, ixdstar
      common /grd20/ ixsnog, isadjalfxt, isgdistort, iynod, ixdstar
      common /grd23/ radm, radx, rad0, rscalcore, za0, zax, zaxpt
      common /grd23/ tiltang, zxpt_reset, alfyt, tnoty, sratiopf, alfxt
      common /grd23/ tctr, bpolfix, btfix, agsindx, agsrsp, rnod
c End of Analgrd

c Group Torannulus
      double precision acore, rm0, edgewid, dthlim, bpol0, btor0
      integer ibpmodel
      double precision radf ( 0:nym+1,0:4)
      pointer(pradf,radf)
      double precision thpf ( 1:nxm,0:4)
      pointer(pthpf,thpf)
      common /grd30/ ibpmodel
      common /grd33/ acore, rm0, edgewid, dthlim, bpol0, btor0
      common /grd36/ pradf, pthpf
c End of Torannulus

c Group Magmirror
      integer nzc, nrc
      double precision zu ( 1:nxm,1:nym,0:4)
      pointer(pzu,zu)
      double precision ru ( 1:nxm,1:nym,0:4)
      pointer(pru,ru)
      double precision bzu ( 1:nxm,1:nym,0:4)
      pointer(pbzu,bzu)
      double precision bru ( 1:nxm,1:nym,0:4)
      pointer(pbru,bru)
      double precision bmag ( 1:nxm,1:nym,0:4)
      pointer(pbmag,bmag)
      common /grd40/ nzc, nrc
      common /grd46/ pzu, pru, pbzu, pbru
      common /grd46/ pbmag
c End of Magmirror

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

c Group UEgrid
      integer ixtop
      common /grd130/ ixtop
c End of UEgrid

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

c Group Refinex
      double precision alfxptl, alfxpt2l, alfxptu, alfxpt2u, alfxpt
      double precision alfxpt2
      integer isrefxptn, nxmod, nflux, nsmoothx
      double precision rsu ( 0:nym+2)
      pointer(prsu,rsu)
      double precision zsu ( 0:nym+2)
      pointer(pzsu,zsu)
      double precision rsx ( 0:nym+2)
      pointer(prsx,rsx)
      double precision zsx ( 0:nym+2)
      pointer(pzsx,zsx)
      double precision rflux ( npts)
      pointer(prflux,rflux)
      double precision zflux ( npts)
      pointer(pzflux,zflux)
      double precision dsflux ( npts)
      pointer(pdsflux,dsflux)
      double precision rmm ( 0:nym,0:nxm)
      pointer(prmm,rmm)
      double precision zmm ( 0:nym,0:nxm)
      pointer(pzmm,zmm)
      common /grd150/ isrefxptn, nxmod, nflux, nsmoothx
      common /grd153/ alfxptl, alfxpt2l, alfxptu, alfxpt2u, alfxpt
      common /grd153/ alfxpt2
      common /grd156/ prsu, pzsu, prsx, pzsx
      common /grd156/ prflux, pzflux, pdsflux
      common /grd156/ prmm, pzmm
c End of Refinex

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

c Group Dnull_temp
      integer nxmb, nymb, ixpt1b, ixtopb, ixpt2b, iysptrxb, nxmu, nymu
      integer ixpt1u, ixtopu, ixpt2u, iysptrxu
      double precision rmb ( 0:nxmb+1,0:nymb+1,0:4)
      pointer(prmb,rmb)
      double precision zmb ( 0:nxmb+1,0:nymb+1,0:4)
      pointer(pzmb,zmb)
      double precision rmu ( 0:nxmu+1,0:nymu+1,0:4)
      pointer(prmu,rmu)
      double precision zmu ( 0:nxmu+1,0:nymu+1,0:4)
      pointer(pzmu,zmu)
      common /grd170/ nxmb, nymb, ixpt1b, ixtopb, ixpt2b, iysptrxb, nxmu
      common /grd170/ nymu, ixpt1u, ixtopu, ixpt2u, iysptrxu
      common /grd176/ prmb, pzmb, prmu, pzmu
c End of Dnull_temp

c Group Expseed
      double precision fraclplt(2), alfxdiv(2), alfxcore(2)
      double precision shift_seed_leg(2), shift_seed_core(2), fcorenunif
      integer nxlplt(2), nxlxpt(2)
      common /grd180/ nxlplt, nxlxpt
      common /grd183/ fraclplt, alfxdiv, alfxcore, shift_seed_leg
      common /grd183/ shift_seed_core, fcorenunif
c End of Expseed

c Group Xfcn
c End of Xfcn

c Group Driver
c End of Driver


      external grdiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(pradf)
      call clraddr(pthpf)
      call clraddr(pzu)
      call clraddr(pru)
      call clraddr(pbzu)
      call clraddr(pbru)
      call clraddr(pbmag)
      call clraddr(pxcurveg)
      call clraddr(pycurveg)
      call clraddr(pnpointg)
      call clraddr(pcmeshx)
      call clraddr(pcmeshy)
      call clraddr(pisegment)
      call clraddr(pisys)
      call clraddr(palphasys)
      call clraddr(pijump)
      call clraddr(psplcoef)
      call clraddr(pxknts)
      call clraddr(pncap7)
      call clraddr(pxdatag)
      call clraddr(pydatag)
      call clraddr(psddata)
      call clraddr(pbkpt)
      call clraddr(pxconst)
      call clraddr(pyconst)
      call clraddr(pnderiv)
      call clraddr(pcoeff)
      call clraddr(pwsla)
      call clraddr(piwsla)
      call clraddr(pseedxp)
      call clraddr(pseedxpxl)
      call clraddr(pseed)
      call clraddr(pdissep)
      call clraddr(pdistxp)
      call clraddr(pdistxpxl)
      call clraddr(px0g)
      call clraddr(pxlast)
      call clraddr(py0g)
      call clraddr(pylast)
      call clraddr(pxtrans)
      call clraddr(pytrans)
      call clraddr(pwg)
      call clraddr(pistartg)
      call clraddr(piendg)
      call clraddr(pm)
      call clraddr(pnseg)
      call clraddr(pxwork)
      call clraddr(pywork)
      call clraddr(pistartc)
      call clraddr(piendc)
      call clraddr(pcmeshx0)
      call clraddr(pcmeshy0)
      call clraddr(pdsc)
      call clraddr(pxcrv)
      call clraddr(pycrv)
      call clraddr(pdsm)
      call clraddr(pdss)
      call clraddr(pdssleg)
      call clraddr(pdsmesh)
      call clraddr(pdsmesh0)
      call clraddr(pdsmesh1)
      call clraddr(pdsmesh2)
      call clraddr(pxmsh)
      call clraddr(pymsh)
      call clraddr(prtop1)
      call clraddr(pztop1)
      call clraddr(prtop2)
      call clraddr(pztop2)
      call clraddr(prupstream1)
      call clraddr(pzupstream1)
      call clraddr(prupstream2)
      call clraddr(pzupstream2)
      call clraddr(prdnstream1)
      call clraddr(pzdnstream1)
      call clraddr(prdnstream2)
      call clraddr(pzdnstream2)
      call clraddr(prplate1)
      call clraddr(pzplate1)
      call clraddr(prplate2)
      call clraddr(pzplate2)
      call clraddr(prtop)
      call clraddr(pztop)
      call clraddr(prtop0)
      call clraddr(pztop0)
      call clraddr(prbot)
      call clraddr(pzbot)
      call clraddr(prupstream)
      call clraddr(pzupstream)
      call clraddr(prdnstream)
      call clraddr(pzdnstream)
      call clraddr(prplate)
      call clraddr(pzplate)
      call clraddr(prplate0)
      call clraddr(pzplate0)
      call clraddr(pdsnorm)
      call clraddr(pwtm1)
      call clraddr(pcmeshx3)
      call clraddr(pcmeshy3)
      call clraddr(prff1)
      call clraddr(pzff1)
      call clraddr(prff2)
      call clraddr(pzff2)
      call clraddr(prff)
      call clraddr(pzff)
      call clraddr(pdsmesh3)
      call clraddr(pdsmeshff)
      call clraddr(prsu)
      call clraddr(pzsu)
      call clraddr(prsx)
      call clraddr(pzsx)
      call clraddr(prflux)
      call clraddr(pzflux)
      call clraddr(pdsflux)
      call clraddr(prmm)
      call clraddr(pzmm)
      call clraddr(pxdat)
      call clraddr(ptdat)
      call clraddr(ptknt)
      call clraddr(pz1work)
      call clraddr(pz1cscoef)
      call clraddr(pwrk1)
      call clraddr(prmb)
      call clraddr(pzmb)
      call clraddr(prmu)
      call clraddr(pzmu)

      return
      end
      subroutine grddbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,20,340)
      return
      end
      subroutine grdwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /grdrtdm/ drtdm

c Group Dim_vars

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd


      integer nx, ny, nxm, nym
      common /grd00/ nx, ny, nxm, nym
c End of Dim_vars

c Group Dimensions
      integer idim, nix, mseg, nalpha, nxuse(1:2), nptmp, ndata, nbkpt
      integer nconst, nwdim, niwdim
      common /grd10/ idim, nix, mseg, nalpha, nxuse, nptmp, ndata, nbkpt
      common /grd10/ nconst, nwdim, niwdim
c End of Dimensions

c Group Analgrd
      double precision radm, radx, rad0, rscalcore, za0, zax, zaxpt
      double precision tiltang, zxpt_reset, alfyt, tnoty, sratiopf
      double precision alfxt, tctr, bpolfix, btfix, agsindx, agsrsp
      double precision rnod
      integer ixsnog, isadjalfxt, isgdistort, iynod, ixdstar
      common /grd20/ ixsnog, isadjalfxt, isgdistort, iynod, ixdstar
      common /grd23/ radm, radx, rad0, rscalcore, za0, zax, zaxpt
      common /grd23/ tiltang, zxpt_reset, alfyt, tnoty, sratiopf, alfxt
      common /grd23/ tctr, bpolfix, btfix, agsindx, agsrsp, rnod
c End of Analgrd

c Group Torannulus
      double precision acore, rm0, edgewid, dthlim, bpol0, btor0
      integer ibpmodel
      double precision radf ( 0:nym+1,0:4)
      pointer(pradf,radf)
      double precision thpf ( 1:nxm,0:4)
      pointer(pthpf,thpf)
      common /grd30/ ibpmodel
      common /grd33/ acore, rm0, edgewid, dthlim, bpol0, btor0
      common /grd36/ pradf, pthpf
c End of Torannulus

c Group Magmirror
      integer nzc, nrc
      double precision zu ( 1:nxm,1:nym,0:4)
      pointer(pzu,zu)
      double precision ru ( 1:nxm,1:nym,0:4)
      pointer(pru,ru)
      double precision bzu ( 1:nxm,1:nym,0:4)
      pointer(pbzu,bzu)
      double precision bru ( 1:nxm,1:nym,0:4)
      pointer(pbru,bru)
      double precision bmag ( 1:nxm,1:nym,0:4)
      pointer(pbmag,bmag)
      common /grd40/ nzc, nrc
      common /grd46/ pzu, pru, pbzu, pbru
      common /grd46/ pbmag
c End of Magmirror

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

c Group UEgrid
      integer ixtop
      common /grd130/ ixtop
c End of UEgrid

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

c Group Refinex
      double precision alfxptl, alfxpt2l, alfxptu, alfxpt2u, alfxpt
      double precision alfxpt2
      integer isrefxptn, nxmod, nflux, nsmoothx
      double precision rsu ( 0:nym+2)
      pointer(prsu,rsu)
      double precision zsu ( 0:nym+2)
      pointer(pzsu,zsu)
      double precision rsx ( 0:nym+2)
      pointer(prsx,rsx)
      double precision zsx ( 0:nym+2)
      pointer(pzsx,zsx)
      double precision rflux ( npts)
      pointer(prflux,rflux)
      double precision zflux ( npts)
      pointer(pzflux,zflux)
      double precision dsflux ( npts)
      pointer(pdsflux,dsflux)
      double precision rmm ( 0:nym,0:nxm)
      pointer(prmm,rmm)
      double precision zmm ( 0:nym,0:nxm)
      pointer(pzmm,zmm)
      common /grd150/ isrefxptn, nxmod, nflux, nsmoothx
      common /grd153/ alfxptl, alfxpt2l, alfxptu, alfxpt2u, alfxpt
      common /grd153/ alfxpt2
      common /grd156/ prsu, pzsu, prsx, pzsx
      common /grd156/ prflux, pzflux, pdsflux
      common /grd156/ prmm, pzmm
c End of Refinex

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

c Group Dnull_temp
      integer nxmb, nymb, ixpt1b, ixtopb, ixpt2b, iysptrxb, nxmu, nymu
      integer ixpt1u, ixtopu, ixpt2u, iysptrxu
      double precision rmb ( 0:nxmb+1,0:nymb+1,0:4)
      pointer(prmb,rmb)
      double precision zmb ( 0:nxmb+1,0:nymb+1,0:4)
      pointer(pzmb,zmb)
      double precision rmu ( 0:nxmu+1,0:nymu+1,0:4)
      pointer(prmu,rmu)
      double precision zmu ( 0:nxmu+1,0:nymu+1,0:4)
      pointer(pzmu,zmu)
      common /grd170/ nxmb, nymb, ixpt1b, ixtopb, ixpt2b, iysptrxb, nxmu
      common /grd170/ nymu, ixpt1u, ixtopu, ixpt2u, iysptrxu
      common /grd176/ prmb, pzmb, prmu, pzmu
c End of Dnull_temp

c Group Expseed
      double precision fraclplt(2), alfxdiv(2), alfxcore(2)
      double precision shift_seed_leg(2), shift_seed_core(2), fcorenunif
      integer nxlplt(2), nxlxpt(2)
      common /grd180/ nxlplt, nxlxpt
      common /grd183/ fraclplt, alfxdiv, alfxcore, shift_seed_leg
      common /grd183/ shift_seed_core, fcorenunif
c End of Expseed

c Group Xfcn
c End of Xfcn

c Group Driver
c End of Driver



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call grddbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Dimensions")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"idim",varadr(idim),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nix",varadr(nix),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mseg",varadr(mseg),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nalpha",varadr(nalpha),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nxuse )
      i0001234=rtvare(drtdm,"nxuse",i000addr,0,'integer','(1:2)', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptmp",varadr(nptmp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndata",varadr(ndata),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nbkpt",varadr(nbkpt),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nconst",varadr(nconst),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nwdim",varadr(nwdim),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"niwdim",varadr(niwdim),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Analgrd")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"radm",varadr(radm),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"radx",varadr(radx),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rad0",varadr(rad0),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rscalcore",varadr(rscalcore),0,
     &   'double precision','scalar', " ")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"za0",varadr(za0),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zax",varadr(zax),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zaxpt",varadr(zaxpt),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tiltang",varadr(tiltang),0,
     &   'double precision','scalar', "deg")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixsnog",varadr(ixsnog),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zxpt_reset",varadr(zxpt_reset),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfyt",varadr(alfyt),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tnoty",varadr(tnoty),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sratiopf",varadr(sratiopf),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxt",varadr(alfxt),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isadjalfxt",varadr(isadjalfxt),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tctr",varadr(tctr),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"bpolfix",varadr(bpolfix),0,
     &   'double precision','scalar', "T")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"btfix",varadr(btfix),0,'double precision',
     &   'scalar', "T")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isgdistort",varadr(isgdistort),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"agsindx",varadr(agsindx),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"agsrsp",varadr(agsrsp),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iynod",varadr(iynod),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rnod",varadr(rnod),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixdstar",varadr(ixdstar),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Torannulus")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"acore",varadr(acore),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rm0",varadr(rm0),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"edgewid",varadr(edgewid),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dthlim",varadr(dthlim),0,'double precision'
     &   ,'scalar', "rad")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"bpol0",varadr(bpol0),0,'double precision',
     &   'scalar', "T")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"btor0",varadr(btor0),0,'double precision',
     &   'scalar', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pradf )
      i0001234=rtvare(drtdm,"radf",i000addr,1,'double precision',
     &   '(0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pthpf )
      i0001234=rtvare(drtdm,"thpf",i000addr,1,'double precision',
     &   '(1:nxm,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ibpmodel",varadr(ibpmodel),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Magmirror")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pzu )
      i0001234=rtvare(drtdm,"zu",i000addr,1,'double precision',
     &   '(1:nxm,1:nym,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pru )
      i0001234=rtvare(drtdm,"ru",i000addr,1,'double precision',
     &   '(1:nxm,1:nym,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbzu )
      i0001234=rtvare(drtdm,"bzu",i000addr,1,'double precision',
     &   '(1:nxm,1:nym,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbru )
      i0001234=rtvare(drtdm,"bru",i000addr,1,'double precision',
     &   '(1:nxm,1:nym,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbmag )
      i0001234=rtvare(drtdm,"bmag",i000addr,1,'double precision',
     &   '(1:nxm,1:nym,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzc",varadr(nzc),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nrc",varadr(nrc),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Curves")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pxcurveg )
      i0001234=rtvare(drtdm,"xcurveg",i000addr,1,'double precision',
     &   '(npts,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pycurveg )
      i0001234=rtvare(drtdm,"ycurveg",i000addr,1,'double precision',
     &   '(npts,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnpointg )
      i0001234=rtvare(drtdm,"npointg",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xxpoint",varadr(xxpoint),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"yxpoint",varadr(yxpoint),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rtanpl",varadr(rtanpl),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ztanpl",varadr(ztanpl),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Linkco")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pcmeshx )
      i0001234=rtvare(drtdm,"cmeshx",i000addr,1,'double precision',
     &   '(idim,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcmeshy )
      i0001234=rtvare(drtdm,"cmeshy",i000addr,1,'double precision',
     &   '(idim,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ixpoint )
      i0001234=rtvare(drtdm,"ixpoint",i000addr,0,'integer','(1:3,1:2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"yextend",varadr(yextend),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dsmin",varadr(dsmin),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dsminx",varadr(dsminx),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dyjump",varadr(dyjump),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alpha1",varadr(alpha1),0,'double precision'
     &   ,'scalar', "degrees")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ityp )
      i0001234=rtvare(drtdm,"ityp",i000addr,0,'integer','(6,2)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dxleft",varadr(dxleft),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndxleft",varadr(ndxleft),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Transfm")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pisegment )
      i0001234=rtvare(drtdm,"isegment",i000addr,1,'integer',
     &   '(npts,jdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pisys )
      i0001234=rtvare(drtdm,"isys",i000addr,1,'integer','(mseg,jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( palphasys )
      i0001234=rtvare(drtdm,"alphasys",i000addr,1,'double precision',
     &   '(nalpha)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pijump )
      i0001234=rtvare(drtdm,"ijump",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Spline")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( psplcoef )
      i0001234=rtvare(drtdm,"splcoef",i000addr,1,'double precision',
     &   '(npts,mseg,jdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxknts )
      i0001234=rtvare(drtdm,"xknts",i000addr,1,'double precision',
     &   '(npts,mseg,jdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pncap7 )
      i0001234=rtvare(drtdm,"ncap7",i000addr,1,'integer','(mseg,jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Argfc")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pxdatag )
      i0001234=rtvare(drtdm,"xdatag",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pydatag )
      i0001234=rtvare(drtdm,"ydatag",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psddata )
      i0001234=rtvare(drtdm,"sddata",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nord",varadr(nord),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbkpt )
      i0001234=rtvare(drtdm,"bkpt",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxconst )
      i0001234=rtvare(drtdm,"xconst",i000addr,1,'double precision',
     &   '(nconst)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyconst )
      i0001234=rtvare(drtdm,"yconst",i000addr,1,'double precision',
     &   '(nconst)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnderiv )
      i0001234=rtvare(drtdm,"nderiv",i000addr,1,'integer','(nconst)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mode",varadr(mode),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcoeff )
      i0001234=rtvare(drtdm,"coeff",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwsla )
      i0001234=rtvare(drtdm,"wsla",i000addr,1,'double precision',
     &   '(nwdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piwsla )
      i0001234=rtvare(drtdm,"iwsla",i000addr,1,'integer','(niwdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Inmesh")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isspnew",varadr(isspnew),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( rstrike )
      i0001234=rtvare(drtdm,"rstrike",i000addr,0,'double precision',
     &   '(1:2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( zstrike )
      i0001234=rtvare(drtdm,"zstrike",i000addr,0,'double precision',
     &   '(1:2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istpnew",varadr(istpnew),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( rtpnew )
      i0001234=rtvare(drtdm,"rtpnew",i000addr,0,'double precision',
     &   '(1:2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ztpnew )
      i0001234=rtvare(drtdm,"ztpnew",i000addr,0,'double precision',
     &   '(1:2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( istptest )
      i0001234=rtvare(drtdm,"istptest",i000addr,0,'integer','(1:2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ilmax )
      i0001234=rtvare(drtdm,"ilmax",i000addr,0,'integer','(1:2)', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pseedxp )
      i0001234=rtvare(drtdm,"seedxp",i000addr,1,'double precision',
     &   '(idim,noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pseedxpxl )
      i0001234=rtvare(drtdm,"seedxpxl",i000addr,1,'double precision',
     &   '(idim,noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pseed )
      i0001234=rtvare(drtdm,"seed",i000addr,1,'double precision',
     &   '(idim,noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdissep )
      i0001234=rtvare(drtdm,"dissep",i000addr,1,'double precision',
     &   '(npts,noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdistxp )
      i0001234=rtvare(drtdm,"distxp",i000addr,1,'double precision',
     &   '(noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdistxpxl )
      i0001234=rtvare(drtdm,"distxpxl",i000addr,1,'double precision',
     &   '(noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( px0g )
      i0001234=rtvare(drtdm,"x0g",i000addr,1,'double precision',
     &   '(noregs)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxlast )
      i0001234=rtvare(drtdm,"xlast",i000addr,1,'double precision',
     &   '(noregs)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( py0g )
      i0001234=rtvare(drtdm,"y0g",i000addr,1,'double precision',
     &   '(noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pylast )
      i0001234=rtvare(drtdm,"ylast",i000addr,1,'double precision',
     &   '(noregs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( isztest )
      i0001234=rtvare(drtdm,"isztest",i000addr,0,'integer','(1:2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"epslon_lim",varadr(epslon_lim),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dalpha",varadr(dalpha),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Transit")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pxtrans )
      i0001234=rtvare(drtdm,"xtrans",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pytrans )
      i0001234=rtvare(drtdm,"ytrans",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwg )
      i0001234=rtvare(drtdm,"wg",i000addr,1,'double precision','(npts)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"System")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pistartg )
      i0001234=rtvare(drtdm,"istartg",i000addr,1,'integer','(mseg,jdim)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piendg )
      i0001234=rtvare(drtdm,"iendg",i000addr,1,'integer','(mseg,jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pm )
      i0001234=rtvare(drtdm,"m",i000addr,1,'integer','(mseg,jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnseg )
      i0001234=rtvare(drtdm,"nseg",i000addr,1,'integer','(jdim)', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ixpointc )
      i0001234=rtvare(drtdm,"ixpointc",i000addr,0,'integer','(1:3,1:2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxwork )
      i0001234=rtvare(drtdm,"xwork",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pywork )
      i0001234=rtvare(drtdm,"ywork",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pistartc )
      i0001234=rtvare(drtdm,"istartc",i000addr,1,'integer','(noregs)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piendc )
      i0001234=rtvare(drtdm,"iendc",i000addr,1,'integer','(noregs)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"UEgrid")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixtop",varadr(ixtop),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Mmod")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pcmeshx0 )
      i0001234=rtvare(drtdm,"cmeshx0",i000addr,1,'double precision',
     &   '(idim,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcmeshy0 )
      i0001234=rtvare(drtdm,"cmeshy0",i000addr,1,'double precision',
     &   '(idim,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsc )
      i0001234=rtvare(drtdm,"dsc",i000addr,1,'double precision','(npts)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcrv )
      i0001234=rtvare(drtdm,"xcrv",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pycrv )
      i0001234=rtvare(drtdm,"ycrv",i000addr,1,'double precision',
     &   '(npts)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsm )
      i0001234=rtvare(drtdm,"dsm",i000addr,1,'double precision','(idim)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdss )
      i0001234=rtvare(drtdm,"dss",i000addr,1,'double precision','(idim)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdssleg )
      i0001234=rtvare(drtdm,"dssleg",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsmesh )
      i0001234=rtvare(drtdm,"dsmesh",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsmesh0 )
      i0001234=rtvare(drtdm,"dsmesh0",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsmesh1 )
      i0001234=rtvare(drtdm,"dsmesh1",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsmesh2 )
      i0001234=rtvare(drtdm,"dsmesh2",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxmsh )
      i0001234=rtvare(drtdm,"xmsh",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pymsh )
      i0001234=rtvare(drtdm,"ymsh",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntop1",varadr(ntop1),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtop1 )
      i0001234=rtvare(drtdm,"rtop1",i000addr,1,'double precision',
     &   '(ntop1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pztop1 )
      i0001234=rtvare(drtdm,"ztop1",i000addr,1,'double precision',
     &   '(ntop1)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntop2",varadr(ntop2),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtop2 )
      i0001234=rtvare(drtdm,"rtop2",i000addr,1,'double precision',
     &   '(ntop2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pztop2 )
      i0001234=rtvare(drtdm,"ztop2",i000addr,1,'double precision',
     &   '(ntop2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istream",varadr(istream),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isupstreamx",varadr(isupstreamx),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nupstream1",varadr(nupstream1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prupstream1 )
      i0001234=rtvare(drtdm,"rupstream1",i000addr,1,'double precision',
     &   '(nupstream1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzupstream1 )
      i0001234=rtvare(drtdm,"zupstream1",i000addr,1,'double precision',
     &   '(nupstream1)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nupstream2",varadr(nupstream2),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prupstream2 )
      i0001234=rtvare(drtdm,"rupstream2",i000addr,1,'double precision',
     &   '(nupstream2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzupstream2 )
      i0001234=rtvare(drtdm,"zupstream2",i000addr,1,'double precision',
     &   '(nupstream2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndnstream1",varadr(ndnstream1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prdnstream1 )
      i0001234=rtvare(drtdm,"rdnstream1",i000addr,1,'double precision',
     &   '(ndnstream1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzdnstream1 )
      i0001234=rtvare(drtdm,"zdnstream1",i000addr,1,'double precision',
     &   '(ndnstream1)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndnstream2",varadr(ndnstream2),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prdnstream2 )
      i0001234=rtvare(drtdm,"rdnstream2",i000addr,1,'double precision',
     &   '(ndnstream2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzdnstream2 )
      i0001234=rtvare(drtdm,"zdnstream2",i000addr,1,'double precision',
     &   '(ndnstream2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iplate",varadr(iplate),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nplate1",varadr(nplate1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prplate1 )
      i0001234=rtvare(drtdm,"rplate1",i000addr,1,'double precision',
     &   '(nplate1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzplate1 )
      i0001234=rtvare(drtdm,"zplate1",i000addr,1,'double precision',
     &   '(nplate1)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nplate2",varadr(nplate2),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prplate2 )
      i0001234=rtvare(drtdm,"rplate2",i000addr,1,'double precision',
     &   '(nplate2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzplate2 )
      i0001234=rtvare(drtdm,"zplate2",i000addr,1,'double precision',
     &   '(nplate2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntop",varadr(ntop),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtop )
      i0001234=rtvare(drtdm,"rtop",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pztop )
      i0001234=rtvare(drtdm,"ztop",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntop0",varadr(ntop0),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtop0 )
      i0001234=rtvare(drtdm,"rtop0",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pztop0 )
      i0001234=rtvare(drtdm,"ztop0",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nbot",varadr(nbot),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prbot )
      i0001234=rtvare(drtdm,"rbot",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzbot )
      i0001234=rtvare(drtdm,"zbot",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nupstream",varadr(nupstream),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prupstream )
      i0001234=rtvare(drtdm,"rupstream",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzupstream )
      i0001234=rtvare(drtdm,"zupstream",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndnstream",varadr(ndnstream),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prdnstream )
      i0001234=rtvare(drtdm,"rdnstream",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzdnstream )
      i0001234=rtvare(drtdm,"zdnstream",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nplate",varadr(nplate),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prplate )
      i0001234=rtvare(drtdm,"rplate",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzplate )
      i0001234=rtvare(drtdm,"zplate",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nplate0",varadr(nplate0),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prplate0 )
      i0001234=rtvare(drtdm,"rplate0",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzplate0 )
      i0001234=rtvare(drtdm,"zplate0",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsnorm )
      i0001234=rtvare(drtdm,"dsnorm",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"wtold",varadr(wtold),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nsmooth",varadr(nsmooth),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"fuzzm",varadr(fuzzm),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"delmax",varadr(delmax),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"wtmesh1",varadr(wtmesh1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwtm1 )
      i0001234=rtvare(drtdm,"wtm1",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dmix0",varadr(dmix0),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcmeshx3 )
      i0001234=rtvare(drtdm,"cmeshx3",i000addr,1,'double precision',
     &   '(idim,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcmeshy3 )
      i0001234=rtvare(drtdm,"cmeshy3",i000addr,1,'double precision',
     &   '(idim,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nff1",varadr(nff1),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prff1 )
      i0001234=rtvare(drtdm,"rff1",i000addr,1,'double precision',
     &   '(nff1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzff1 )
      i0001234=rtvare(drtdm,"zff1",i000addr,1,'double precision',
     &   '(nff1)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nff2",varadr(nff2),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prff2 )
      i0001234=rtvare(drtdm,"rff2",i000addr,1,'double precision',
     &   '(nff2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzff2 )
      i0001234=rtvare(drtdm,"zff2",i000addr,1,'double precision',
     &   '(nff2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nff",varadr(nff),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prff )
      i0001234=rtvare(drtdm,"rff",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzff )
      i0001234=rtvare(drtdm,"zff",i000addr,1,'double precision',
     &   '(nptmp)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsmesh3 )
      i0001234=rtvare(drtdm,"dsmesh3",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsmeshff )
      i0001234=rtvare(drtdm,"dsmeshff",i000addr,1,'double precision',
     &   '(idim)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"cwtffu",varadr(cwtffu),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"cwtffd",varadr(cwtffd),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isxtform",varadr(isxtform),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iswtform",varadr(iswtform),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"wtff1",varadr(wtff1),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxff1",varadr(slpxff1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxffu1",varadr(slpxffu1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxffd1",varadr(slpxffd1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxdff1",varadr(nxdff1),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"wtff2",varadr(wtff2),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxff2",varadr(slpxff2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxffu2",varadr(slpxffu2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxffd2",varadr(slpxffd2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxdff2",varadr(nxdff2),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Refinex")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isrefxptn",varadr(isrefxptn),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxmod",varadr(nxmod),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxptl",varadr(alfxptl),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt2l",varadr(alfxpt2l),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxptu",varadr(alfxptu),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt2u",varadr(alfxpt2u),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt",varadr(alfxpt),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt2",varadr(alfxpt2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prsu )
      i0001234=rtvare(drtdm,"rsu",i000addr,1,'double precision',
     &   '(0:nym+2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzsu )
      i0001234=rtvare(drtdm,"zsu",i000addr,1,'double precision',
     &   '(0:nym+2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prsx )
      i0001234=rtvare(drtdm,"rsx",i000addr,1,'double precision',
     &   '(0:nym+2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzsx )
      i0001234=rtvare(drtdm,"zsx",i000addr,1,'double precision',
     &   '(0:nym+2)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nflux",varadr(nflux),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prflux )
      i0001234=rtvare(drtdm,"rflux",i000addr,1,'double precision',
     &   '(npts)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzflux )
      i0001234=rtvare(drtdm,"zflux",i000addr,1,'double precision',
     &   '(npts)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdsflux )
      i0001234=rtvare(drtdm,"dsflux",i000addr,1,'double precision',
     &   '(npts)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prmm )
      i0001234=rtvare(drtdm,"rmm",i000addr,1,'double precision',
     &   '(0:nym,0:nxm)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzmm )
      i0001234=rtvare(drtdm,"zmm",i000addr,1,'double precision',
     &   '(0:nym,0:nxm)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nsmoothx",varadr(nsmoothx),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Xmesh")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndat",varadr(ndat),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxdat )
      i0001234=rtvare(drtdm,"xdat",i000addr,1,'double precision',
     &   '(ndat)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptdat )
      i0001234=rtvare(drtdm,"tdat",i000addr,1,'double precision',
     &   '(ndat)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kxmesh",varadr(kxmesh),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpxt",varadr(slpxt),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( alfx )
      i0001234=rtvare(drtdm,"alfx",i000addr,0,'double precision','(2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( dxgas )
      i0001234=rtvare(drtdm,"dxgas",i000addr,0,'double precision','(2)', 
     &   "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nxgas )
      i0001234=rtvare(drtdm,"nxgas",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dt1",varadr(dt1),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dx1",varadr(dx1),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dt2",varadr(dt2),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dx2",varadr(dx2),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ileft",varadr(ileft),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dleft",varadr(dleft),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iright",varadr(iright),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dright",varadr(dright),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kord",varadr(kord),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndatp2",varadr(ndatp2),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kntopt",varadr(kntopt),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptknt )
      i0001234=rtvare(drtdm,"tknt",i000addr,1,'double precision',
     &   '(ndatp2+4)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pz1work )
      i0001234=rtvare(drtdm,"z1work",i000addr,1,'double precision',
     &   '(5*(ndat+2))', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pz1cscoef )
      i0001234=rtvare(drtdm,"z1cscoef",i000addr,1,'double precision',
     &   '(ndatp2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwrk1 )
      i0001234=rtvare(drtdm,"wrk1",i000addr,1,'double precision',
     &   '(3*kord)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iflag1",varadr(iflag1),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Dnull_temp")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxmb",varadr(nxmb),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nymb",varadr(nymb),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prmb )
      i0001234=rtvare(drtdm,"rmb",i000addr,1,'double precision',
     &   '(0:nxmb+1,0:nymb+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzmb )
      i0001234=rtvare(drtdm,"zmb",i000addr,1,'double precision',
     &   '(0:nxmb+1,0:nymb+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixpt1b",varadr(ixpt1b),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixtopb",varadr(ixtopb),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixpt2b",varadr(ixpt2b),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iysptrxb",varadr(iysptrxb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxmu",varadr(nxmu),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nymu",varadr(nymu),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prmu )
      i0001234=rtvare(drtdm,"rmu",i000addr,1,'double precision',
     &   '(0:nxmu+1,0:nymu+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzmu )
      i0001234=rtvare(drtdm,"zmu",i000addr,1,'double precision',
     &   '(0:nxmu+1,0:nymu+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixpt1u",varadr(ixpt1u),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixtopu",varadr(ixtopu),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixpt2u",varadr(ixpt2u),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iysptrxu",varadr(iysptrxu),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Expseed")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( fraclplt )
      i0001234=rtvare(drtdm,"fraclplt",i000addr,0,'double precision',
     &   '(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( alfxdiv )
      i0001234=rtvare(drtdm,"alfxdiv",i000addr,0,'double precision',
     &   '(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( alfxcore )
      i0001234=rtvare(drtdm,"alfxcore",i000addr,0,'double precision',
     &   '(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( shift_seed_leg )
      i0001234=rtvare(drtdm,"shift_seed_leg",i000addr,0,
     &   'double precision','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( shift_seed_core )
      i0001234=rtvare(drtdm,"shift_seed_core",i000addr,0,
     &   'double precision','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nxlplt )
      i0001234=rtvare(drtdm,"nxlplt",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nxlxpt )
      i0001234=rtvare(drtdm,"nxlxpt",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"fcorenunif",varadr(fcorenunif),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Xfcn")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn2",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn3",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn4",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nxtotal:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xcscoef",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Driver")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "setidim",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "grdrun",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "ingrd",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "codsys",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'icood:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iseg:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'is:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'dy:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'region:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'alpha1:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "findalph",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nsys:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iseg:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'xob:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'yob:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'alphab:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readflx",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "prune",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "extend",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "splfit",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "sow",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "meshgen",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'region:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "orthogx",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ixtyp:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j0:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'xob:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'yob:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'alphab:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "orthogrd",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ixtyp:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j0:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'xob:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'yob:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'alphab:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readgrid",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'runid:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_runid_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "writesn",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'runid:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_runid_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "writedn",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'runid:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_runid_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "writedata",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'runid:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_runid_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "writednf",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'runid:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_runid_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "intersect2",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'x1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'y1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i1min:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i1max:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'x2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'y2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i2min:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i2max:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'xc:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'yc:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i1c:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i2c:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fuzz:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ierr:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "meshmod2",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'region:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "smooth",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j1:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j2:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "writeue",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "grd2wdf",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "evalspln",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iseg:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'xo:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'yo:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "idealgrd",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "mirrorgrd",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "gett",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "getu",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "getd",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "getp",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "meshmod3",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'region:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "smoother",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "smoother2",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "meshff",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'region:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "fpoloidal",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'psi:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "pressure",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'psi:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "psif",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'z:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "brf",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'z:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "bzf",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'z:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rsurface",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'quadrant:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "fluxcurve",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'quadrant:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iy:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "refinexm",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "refine_xpt",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "smoothx",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rmm:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'zmm:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nd1:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nd2:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iy1:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iy2:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'quadrant:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "mapdnbot",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "mapdntop",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "magnetics",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ixmin:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ixmax:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iymin:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iymax:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "add_guardc_tp",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "exponseed",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"grd_basis.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine grdxpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.19) then
         call grdxp19(name1234)
      elseif (iseg.eq.20) then
         call grdxp20(name1234)
      else
         call baderr('grdxpf: impossible event')
      endif
      return
      end
      subroutine grdxp19(name1234)
cProlog
      character*(*) name1234
      external grd_handler
      external xfcn
      external xfcn2
      external xfcn3
      external xfcn4
      external xcscoef
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'xfcn') then
         call parexecf(grd_handler, 0, xfcn)
      elseif (name1234 .eq. 'xfcn2') then
         call parexecf(grd_handler, 1, xfcn2)
      elseif (name1234 .eq. 'xfcn3') then
         call parexecf(grd_handler, 2, xfcn3)
      elseif (name1234 .eq. 'xfcn4') then
         call parexecf(grd_handler, 3, xfcn4)
      elseif (name1234 .eq. 'xcscoef') then
         call parexecf(grd_handler, 4, xcscoef)
      else
         call baderr('grdxp19: impossible event: '//name5678)
      endif
      return
      end
      subroutine grdxp20(name1234)
cProlog
      character*(*) name1234
      external grd_handler
      external setidim
      external grdrun
      external ingrd
      external codsys
      external findalph
      external readflx
      external prune
      external extend
      external splfit
      external sow
      external meshgen
      external orthogx
      external orthogrd
      external readgrid
      external writesn
      external writedn
      external writedata
      external writednf
      external intersect2
      external meshmod2
      external smooth
      external writeue
      external grd2wdf
      external evalspln
      external idealgrd
      external mirrorgrd
      external gett
      external getu
      external getd
      external getp
      external meshmod3
      external smoother
      external smoother2
      external meshff
      external fpoloidal
      external pressure
      external psif
      external brf
      external bzf
      external rsurface
      external fluxcurve
      external refinexm
      external refine_xpt
      external smoothx
      external mapdnbot
      external mapdntop
      external magnetics
      external add_guardc_tp
      external exponseed
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'setidim') then
         call parexecf(grd_handler, 5, setidim)
      elseif (name1234 .eq. 'grdrun') then
         call parexecf(grd_handler, 6, grdrun)
      elseif (name1234 .eq. 'ingrd') then
         call parexecf(grd_handler, 7, ingrd)
      elseif (name1234 .eq. 'codsys') then
         call parexecf(grd_handler, 8, codsys)
      elseif (name1234 .eq. 'findalph') then
         call parexecf(grd_handler, 9, findalph)
      elseif (name1234 .eq. 'readflx') then
         call parexecf(grd_handler, 10, readflx)
      elseif (name1234 .eq. 'prune') then
         call parexecf(grd_handler, 11, prune)
      elseif (name1234 .eq. 'extend') then
         call parexecf(grd_handler, 12, extend)
      elseif (name1234 .eq. 'splfit') then
         call parexecf(grd_handler, 13, splfit)
      elseif (name1234 .eq. 'sow') then
         call parexecf(grd_handler, 14, sow)
      elseif (name1234 .eq. 'meshgen') then
         call parexecf(grd_handler, 15, meshgen)
      elseif (name1234 .eq. 'orthogx') then
         call parexecf(grd_handler, 16, orthogx)
      elseif (name1234 .eq. 'orthogrd') then
         call parexecf(grd_handler, 17, orthogrd)
      elseif (name1234 .eq. 'readgrid') then
         call parexecf(grd_handler, 18, readgrid)
      elseif (name1234 .eq. 'writesn') then
         call parexecf(grd_handler, 19, writesn)
      elseif (name1234 .eq. 'writedn') then
         call parexecf(grd_handler, 20, writedn)
      elseif (name1234 .eq. 'writedata') then
         call parexecf(grd_handler, 21, writedata)
      elseif (name1234 .eq. 'writednf') then
         call parexecf(grd_handler, 22, writednf)
      elseif (name1234 .eq. 'intersect2') then
         call parexecf(grd_handler, 23, intersect2)
      elseif (name1234 .eq. 'meshmod2') then
         call parexecf(grd_handler, 24, meshmod2)
      elseif (name1234 .eq. 'smooth') then
         call parexecf(grd_handler, 25, smooth)
      elseif (name1234 .eq. 'writeue') then
         call parexecf(grd_handler, 26, writeue)
      elseif (name1234 .eq. 'grd2wdf') then
         call parexecf(grd_handler, 27, grd2wdf)
      elseif (name1234 .eq. 'evalspln') then
         call parexecf(grd_handler, 28, evalspln)
      elseif (name1234 .eq. 'idealgrd') then
         call parexecf(grd_handler, 29, idealgrd)
      elseif (name1234 .eq. 'mirrorgrd') then
         call parexecf(grd_handler, 30, mirrorgrd)
      elseif (name1234 .eq. 'gett') then
         call parexecf(grd_handler, 31, gett)
      elseif (name1234 .eq. 'getu') then
         call parexecf(grd_handler, 32, getu)
      elseif (name1234 .eq. 'getd') then
         call parexecf(grd_handler, 33, getd)
      elseif (name1234 .eq. 'getp') then
         call parexecf(grd_handler, 34, getp)
      elseif (name1234 .eq. 'meshmod3') then
         call parexecf(grd_handler, 35, meshmod3)
      elseif (name1234 .eq. 'smoother') then
         call parexecf(grd_handler, 36, smoother)
      elseif (name1234 .eq. 'smoother2') then
         call parexecf(grd_handler, 37, smoother2)
      elseif (name1234 .eq. 'meshff') then
         call parexecf(grd_handler, 38, meshff)
      elseif (name1234 .eq. 'fpoloidal') then
         call parexecf(grd_handler, 39, fpoloidal)
      elseif (name1234 .eq. 'pressure') then
         call parexecf(grd_handler, 40, pressure)
      elseif (name1234 .eq. 'psif') then
         call parexecf(grd_handler, 41, psif)
      elseif (name1234 .eq. 'brf') then
         call parexecf(grd_handler, 42, brf)
      elseif (name1234 .eq. 'bzf') then
         call parexecf(grd_handler, 43, bzf)
      elseif (name1234 .eq. 'rsurface') then
         call parexecf(grd_handler, 44, rsurface)
      elseif (name1234 .eq. 'fluxcurve') then
         call parexecf(grd_handler, 45, fluxcurve)
      elseif (name1234 .eq. 'refinexm') then
         call parexecf(grd_handler, 46, refinexm)
      elseif (name1234 .eq. 'refine_xpt') then
         call parexecf(grd_handler, 47, refine_xpt)
      elseif (name1234 .eq. 'smoothx') then
         call parexecf(grd_handler, 48, smoothx)
      elseif (name1234 .eq. 'mapdnbot') then
         call parexecf(grd_handler, 49, mapdnbot)
      elseif (name1234 .eq. 'mapdntop') then
         call parexecf(grd_handler, 50, mapdntop)
      elseif (name1234 .eq. 'magnetics') then
         call parexecf(grd_handler, 51, magnetics)
      elseif (name1234 .eq. 'add_guardc_tp') then
         call parexecf(grd_handler, 52, add_guardc_tp)
      elseif (name1234 .eq. 'exponseed') then
         call parexecf(grd_handler, 53, exponseed)
      else
         call baderr('grdxp20: impossible event: '//name5678)
      endif
      return
      end
      function grdbfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer grdbfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in grd')
      call baderr(name1234)
      grdbfcn = -1
      return
      end
