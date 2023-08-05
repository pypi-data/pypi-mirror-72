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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/wdf.d
c     ./wdf.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c








































































      subroutine wdfinit0
cProlog
c initializes a Package
      integer drtdm
      common /wdfrtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("wdf")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call wdfdata
      call wdfwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data wdfiyiyi
c Replace pointer statements with Address types


c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

c Group Auxw
      integer ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      integer nosegsxzb
      common /wdf10/ ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      common /wdf10/ nosegsxzb
c End of Auxw

c Group Linkgrd
      integer jaxisw
      integer*8 pcmeshxw
      integer*8 pcmeshyw
      integer*8 pilmaxw
      integer*8 pixpointw
      integer*8 pjsptrxw
      integer*8 pjminw
      integer*8 pjmaxw
      common /wdf20/ jaxisw
      common /wdf26/ pcmeshxw, pcmeshyw, pilmaxw
      common /wdf26/ pixpointw, pjsptrxw, pjminw
      common /wdf26/ pjmaxw
c End of Linkgrd

c Group Nodew
      integer njwall, numseg(3)
      integer*8 pjindx
      integer*8 pnodedwn
      integer*8 pnodewl
      integer*8 pnopts
      integer*8 pwalnodx
      integer*8 pwalnody
      common /wdf30/ njwall, numseg
      common /wdf36/ pjindx, pnodedwn, pnodewl
      common /wdf36/ pnopts, pwalnodx, pwalnody
c End of Nodew

c Group Options
      character*16 fname
      character*(80) idline
      character*(8) endmark
      double precision frr01, frr02
      integer iswdfon, ivnull
      common /wdf10000/ fname
      common /wdf10001/ idline
      common /wdf10002/ endmark
      common /wdf40/ iswdfon, ivnull
      common /wdf43/ frr01, frr02
c End of Options

c Group Degas1
      integer lflags, lgeomtry, lhalpha, lmaxwell, lmesh, lnamelst
      integer lneutral, loutput, lplasma, lprofh, lproft, lprofv
      integer lrandom, lrecycle, lrflct1, lrflct2, lrrulet, lshrtrun
      integer lsources, lsputter, lstat, lsymetry, lunit, lvolsrc, lwall
      integer lwalldst, maxerrs, mparts, ncount, nexit, nhyd(2)
      integer nocols, nohbs, nohzs, norows, nosplits, notasks, notzs
      double precision engymin, h2frac, lchex, leh0, plsang, rmajor
      double precision rminor, rrengy, scrrmax, shethp, sndspd, te0
      double precision wtmin0, xlen, ylen, zlen
      integer novbs, novzs, nowals, nwriter, nseed(4), ntty
      integer*8 pdeni0
      integer*8 pfictrr0
      integer*8 pnosegsxz
      integer*8 pnosegsy
      integer*8 pt0puff
      integer*8 pti0
      common /wdf50/ lflags, lgeomtry, lhalpha, lmaxwell, lmesh
      common /wdf50/ lnamelst, lneutral, loutput, lplasma, lprofh
      common /wdf50/ lproft, lprofv, lrandom, lrecycle, lrflct1, lrflct2
      common /wdf50/ lrrulet, lshrtrun, lsources, lsputter, lstat
      common /wdf50/ lsymetry, lunit, lvolsrc, lwall, lwalldst, maxerrs
      common /wdf50/ mparts, ncount, nexit, nhyd, nocols, nohbs, nohzs
      common /wdf50/ norows, nosplits, notasks, notzs, novbs, novzs
      common /wdf50/ nowals, nwriter, nseed, ntty
      common /wdf53/ engymin, h2frac, lchex, leh0, plsang, rmajor
      common /wdf53/ rminor, rrengy, scrrmax, shethp, sndspd, te0
      common /wdf53/ wtmin0, xlen, ylen, zlen
      common /wdf56/ pdeni0, pfictrr0, pnosegsxz
      common /wdf56/ pnosegsy, pt0puff, pti0
c End of Degas1

c Group Degas2
      character*8 kwmat(1000,10)
      integer*8 parcdeg
      integer*8 pcurrxzt
      integer*8 pdenehvt
      integer*8 pdenihvt
      integer*8 pficrrhvt
      integer*8 pfrabsorb
      integer*8 pgridx
      integer*8 pgridz
      integer*8 pkplrecyc
      integer*8 pksplzone
      integer*8 pkzone1
      integer*8 pkzone2
      integer*8 plboun1
      integer*8 plboun2
      integer*8 prflcoef
      integer*8 ptehvt
      integer*8 ptihvt
      integer*8 ptwall
      integer*8 pvflowx
      integer*8 pvflowy
      integer*8 pvflowz
      integer*8 pvsorchvt
      integer*8 pxwall
      integer*8 pzwall
      common /wdf10003/ kwmat
      common /wdf66/ parcdeg, pcurrxzt, pdenehvt
      common /wdf66/ pdenihvt, pficrrhvt, pfrabsorb
      common /wdf66/ pgridx, pgridz, pkplrecyc
      common /wdf66/ pksplzone, pkzone1, pkzone2
      common /wdf66/ plboun1, plboun2, prflcoef
      common /wdf66/ ptehvt, ptihvt, ptwall
      common /wdf66/ pvflowx, pvflowy, pvflowz
      common /wdf66/ pvsorchvt, pxwall, pzwall
c End of Degas2

c Group Eqdsk
      double precision xdimw, zdimw, rgrid1w, etimew, bcentrw, rcentrw
      double precision rmagxw, zmagxw, simagxw, sibdryw, rsepsw, zsepsw
      double precision rvsinw, zvsinw, rvsoutw, zvsoutw
      integer eshotw, nlimw
      integer*8 pxlimw
      integer*8 pylimw
      common /wdf70/ eshotw, nlimw
      common /wdf73/ xdimw, zdimw, rgrid1w, etimew, bcentrw, rcentrw
      common /wdf73/ rmagxw, zmagxw, simagxw, sibdryw, rsepsw, zsepsw
      common /wdf73/ rvsinw, zvsinw, rvsoutw, zvsoutw
      common /wdf76/ pxlimw, pylimw
c End of Eqdsk

c Group Urun
c End of Urun


      data nptskb/2/,npw/3/,npsegy/1/,nptp1/2/,ndec/2/,npis/2/,npns/2/
      data mpsegxz/1000/,mpw/10/
      data iswdfon/1/,frr01/.001d0/,frr02/.001d0/
      data h2frac/1.00d0/,lmaxwell/0/,lmesh/2/,loutput/3/,lproft/1/
      data lrflct1/1/,lrflct2/2/,lrrulet/1/,lsymetry/1/,lunit/-1/
      data maxerrs/100/,mparts/0/,ncount/100/,nhyd/2*2/,nocols/420/
      data norows/840/,nosplits/1/,nowals/1/,plsang/90.00d0/,scrrmax/
     &   1.01d0/
      data shethp/3.00d0/

      end
c restore definition from mppl.BASIS

      subroutine wdfdata
cProlog

c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

c Group Auxw
      integer ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      integer nosegsxzb
      common /wdf10/ ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      common /wdf10/ nosegsxzb
c End of Auxw

c Group Linkgrd
      integer jaxisw
      double precision cmeshxw ( idimw,jdimw)
      pointer(pcmeshxw,cmeshxw)
      double precision cmeshyw ( idimw,jdimw)
      pointer(pcmeshyw,cmeshyw)
      integer ilmaxw ( noregsw)
      pointer(pilmaxw,ilmaxw)
      integer ixpointw ( nixw,noregsw)
      pointer(pixpointw,ixpointw)
      integer jsptrxw ( noregsw)
      pointer(pjsptrxw,jsptrxw)
      integer jminw ( noregsw)
      pointer(pjminw,jminw)
      integer jmaxw ( noregsw)
      pointer(pjmaxw,jmaxw)
      common /wdf20/ jaxisw
      common /wdf26/ pcmeshxw, pcmeshyw, pilmaxw
      common /wdf26/ pixpointw, pjsptrxw, pjminw
      common /wdf26/ pjmaxw
c End of Linkgrd

c Group Nodew
      integer njwall, numseg(3)
      integer jindx ( ndec)
      pointer(pjindx,jindx)
      integer nodedwn ( ndec)
      pointer(pnodedwn,nodedwn)
      integer nodewl ( nptshb,ndec)
      pointer(pnodewl,nodewl)
      integer nopts ( ndec)
      pointer(pnopts,nopts)
      double precision walnodx ( nptshb,ndec)
      pointer(pwalnodx,walnodx)
      double precision walnody ( nptshb,ndec)
      pointer(pwalnody,walnody)
      common /wdf30/ njwall, numseg
      common /wdf36/ pjindx, pnodedwn, pnodewl
      common /wdf36/ pnopts, pwalnodx, pwalnody
c End of Nodew

c Group Options
      character*16 fname
      character*(80) idline
      character*(8) endmark
      double precision frr01, frr02
      integer iswdfon, ivnull
      common /wdf10000/ fname
      common /wdf10001/ idline
      common /wdf10002/ endmark
      common /wdf40/ iswdfon, ivnull
      common /wdf43/ frr01, frr02
c End of Options

c Group Degas1
      integer lflags, lgeomtry, lhalpha, lmaxwell, lmesh, lnamelst
      integer lneutral, loutput, lplasma, lprofh, lproft, lprofv
      integer lrandom, lrecycle, lrflct1, lrflct2, lrrulet, lshrtrun
      integer lsources, lsputter, lstat, lsymetry, lunit, lvolsrc, lwall
      integer lwalldst, maxerrs, mparts, ncount, nexit, nhyd(2)
      integer nocols, nohbs, nohzs, norows, nosplits, notasks, notzs
      double precision engymin, h2frac, lchex, leh0, plsang, rmajor
      double precision rminor, rrengy, scrrmax, shethp, sndspd, te0
      double precision wtmin0, xlen, ylen, zlen
      integer novbs, novzs, nowals, nwriter, nseed(4), ntty
      double precision deni0 ( npis)
      pointer(pdeni0,deni0)
      double precision fictrr0 ( npns)
      pointer(pfictrr0,fictrr0)
      integer nosegsxz ( npw)
      pointer(pnosegsxz,nosegsxz)
      integer nosegsy ( npw)
      pointer(pnosegsy,nosegsy)
      double precision t0puff ( npns)
      pointer(pt0puff,t0puff)
      double precision ti0 ( npis)
      pointer(pti0,ti0)
      common /wdf50/ lflags, lgeomtry, lhalpha, lmaxwell, lmesh
      common /wdf50/ lnamelst, lneutral, loutput, lplasma, lprofh
      common /wdf50/ lproft, lprofv, lrandom, lrecycle, lrflct1, lrflct2
      common /wdf50/ lrrulet, lshrtrun, lsources, lsputter, lstat
      common /wdf50/ lsymetry, lunit, lvolsrc, lwall, lwalldst, maxerrs
      common /wdf50/ mparts, ncount, nexit, nhyd, nocols, nohbs, nohzs
      common /wdf50/ norows, nosplits, notasks, notzs, novbs, novzs
      common /wdf50/ nowals, nwriter, nseed, ntty
      common /wdf53/ engymin, h2frac, lchex, leh0, plsang, rmajor
      common /wdf53/ rminor, rrengy, scrrmax, shethp, sndspd, te0
      common /wdf53/ wtmin0, xlen, ylen, zlen
      common /wdf56/ pdeni0, pfictrr0, pnosegsxz
      common /wdf56/ pnosegsy, pt0puff, pti0
c End of Degas1

c Group Degas2
      character*8 kwmat(1000,10)
      double precision arcdeg ( nptp1)
      pointer(parcdeg,arcdeg)
      double precision currxzt ( npsegxz,npsegy,npw,npis)
      pointer(pcurrxzt,currxzt)
      double precision denehvt ( nptsvb,nptshb,nptskb)
      pointer(pdenehvt,denehvt)
      double precision denihvt ( nptsvb,nptshb,nptskb,npis)
      pointer(pdenihvt,denihvt)
      double precision ficrrhvt ( nptsvb,nptshb,nptskb,npns)
      pointer(pficrrhvt,ficrrhvt)
      double precision frabsorb ( npsegxz,npsegy,npw,npns)
      pointer(pfrabsorb,frabsorb)
      double precision gridx ( nptsvb,nptshb,nptskb)
      pointer(pgridx,gridx)
      double precision gridz ( nptsvb,nptshb,nptskb)
      pointer(pgridz,gridz)
      integer kplrecyc ( nptsvb,nptshb)
      pointer(pkplrecyc,kplrecyc)
      integer ksplzone ( nptsvb,nptshb,nptskb)
      pointer(pksplzone,ksplzone)
      integer kzone1 ( nptsvb,nptshb)
      pointer(pkzone1,kzone1)
      integer kzone2 ( nptsvb,nptshb)
      pointer(pkzone2,kzone2)
      integer lboun1 ( nptsvb)
      pointer(plboun1,lboun1)
      integer lboun2 ( nptshb)
      pointer(plboun2,lboun2)
      double precision rflcoef ( npsegxz,npsegy,npw)
      pointer(prflcoef,rflcoef)
      double precision tehvt ( nptsvb,nptshb,nptskb)
      pointer(ptehvt,tehvt)
      double precision tihvt ( nptsvb,nptshb,nptskb,npis)
      pointer(ptihvt,tihvt)
      double precision twall ( npsegxz,npsegy,npw)
      pointer(ptwall,twall)
      double precision vflowx ( nptsvb,nptshb,nptskb)
      pointer(pvflowx,vflowx)
      double precision vflowy ( nptsvb,nptshb,nptskb)
      pointer(pvflowy,vflowy)
      double precision vflowz ( nptsvb,nptshb,nptskb)
      pointer(pvflowz,vflowz)
      double precision vsorchvt ( nptsvb,nptshb,nptskb,npns)
      pointer(pvsorchvt,vsorchvt)
      double precision xwall ( nptsw,npw)
      pointer(pxwall,xwall)
      double precision zwall ( nptsw,npw)
      pointer(pzwall,zwall)
      common /wdf10003/ kwmat
      common /wdf66/ parcdeg, pcurrxzt, pdenehvt
      common /wdf66/ pdenihvt, pficrrhvt, pfrabsorb
      common /wdf66/ pgridx, pgridz, pkplrecyc
      common /wdf66/ pksplzone, pkzone1, pkzone2
      common /wdf66/ plboun1, plboun2, prflcoef
      common /wdf66/ ptehvt, ptihvt, ptwall
      common /wdf66/ pvflowx, pvflowy, pvflowz
      common /wdf66/ pvsorchvt, pxwall, pzwall
c End of Degas2

c Group Eqdsk
      double precision xdimw, zdimw, rgrid1w, etimew, bcentrw, rcentrw
      double precision rmagxw, zmagxw, simagxw, sibdryw, rsepsw, zsepsw
      double precision rvsinw, zvsinw, rvsoutw, zvsoutw
      integer eshotw, nlimw
      double precision xlimw ( nlimw)
      pointer(pxlimw,xlimw)
      double precision ylimw ( nlimw)
      pointer(pylimw,ylimw)
      common /wdf70/ eshotw, nlimw
      common /wdf73/ xdimw, zdimw, rgrid1w, etimew, bcentrw, rcentrw
      common /wdf73/ rmagxw, zmagxw, simagxw, sibdryw, rsepsw, zsepsw
      common /wdf73/ rvsinw, zvsinw, rvsoutw, zvsoutw
      common /wdf76/ pxlimw, pylimw
c End of Eqdsk

c Group Urun
c End of Urun


      external wdfiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(pcmeshxw)
      call clraddr(pcmeshyw)
      call clraddr(pilmaxw)
      call clraddr(pixpointw)
      call clraddr(pjsptrxw)
      call clraddr(pjminw)
      call clraddr(pjmaxw)
      call clraddr(pjindx)
      call clraddr(pnodedwn)
      call clraddr(pnodewl)
      call clraddr(pnopts)
      call clraddr(pwalnodx)
      call clraddr(pwalnody)
      call clraddr(pdeni0)
      call clraddr(pfictrr0)
      call clraddr(pnosegsxz)
      call clraddr(pnosegsy)
      call clraddr(pt0puff)
      call clraddr(pti0)
      call clraddr(parcdeg)
      call clraddr(pcurrxzt)
      call clraddr(pdenehvt)
      call clraddr(pdenihvt)
      call clraddr(pficrrhvt)
      call clraddr(pfrabsorb)
      call clraddr(pgridx)
      call clraddr(pgridz)
      call clraddr(pkplrecyc)
      call clraddr(pksplzone)
      call clraddr(pkzone1)
      call clraddr(pkzone2)
      call clraddr(plboun1)
      call clraddr(plboun2)
      call clraddr(prflcoef)
      call clraddr(ptehvt)
      call clraddr(ptihvt)
      call clraddr(ptwall)
      call clraddr(pvflowx)
      call clraddr(pvflowy)
      call clraddr(pvflowz)
      call clraddr(pvsorchvt)
      call clraddr(pxwall)
      call clraddr(pzwall)
      call clraddr(pxlimw)
      call clraddr(pylimw)

      return
      end
      subroutine wdfdbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,9,162)
      return
      end
      subroutine wdfwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /wdfrtdm/ drtdm

c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

c Group Auxw
      integer ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      integer nosegsxzb
      common /wdf10/ ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      common /wdf10/ nosegsxzb
c End of Auxw

c Group Linkgrd
      integer jaxisw
      double precision cmeshxw ( idimw,jdimw)
      pointer(pcmeshxw,cmeshxw)
      double precision cmeshyw ( idimw,jdimw)
      pointer(pcmeshyw,cmeshyw)
      integer ilmaxw ( noregsw)
      pointer(pilmaxw,ilmaxw)
      integer ixpointw ( nixw,noregsw)
      pointer(pixpointw,ixpointw)
      integer jsptrxw ( noregsw)
      pointer(pjsptrxw,jsptrxw)
      integer jminw ( noregsw)
      pointer(pjminw,jminw)
      integer jmaxw ( noregsw)
      pointer(pjmaxw,jmaxw)
      common /wdf20/ jaxisw
      common /wdf26/ pcmeshxw, pcmeshyw, pilmaxw
      common /wdf26/ pixpointw, pjsptrxw, pjminw
      common /wdf26/ pjmaxw
c End of Linkgrd

c Group Nodew
      integer njwall, numseg(3)
      integer jindx ( ndec)
      pointer(pjindx,jindx)
      integer nodedwn ( ndec)
      pointer(pnodedwn,nodedwn)
      integer nodewl ( nptshb,ndec)
      pointer(pnodewl,nodewl)
      integer nopts ( ndec)
      pointer(pnopts,nopts)
      double precision walnodx ( nptshb,ndec)
      pointer(pwalnodx,walnodx)
      double precision walnody ( nptshb,ndec)
      pointer(pwalnody,walnody)
      common /wdf30/ njwall, numseg
      common /wdf36/ pjindx, pnodedwn, pnodewl
      common /wdf36/ pnopts, pwalnodx, pwalnody
c End of Nodew

c Group Options
      character*16 fname
      character*(80) idline
      character*(8) endmark
      double precision frr01, frr02
      integer iswdfon, ivnull
      common /wdf10000/ fname
      common /wdf10001/ idline
      common /wdf10002/ endmark
      common /wdf40/ iswdfon, ivnull
      common /wdf43/ frr01, frr02
c End of Options

c Group Degas1
      integer lflags, lgeomtry, lhalpha, lmaxwell, lmesh, lnamelst
      integer lneutral, loutput, lplasma, lprofh, lproft, lprofv
      integer lrandom, lrecycle, lrflct1, lrflct2, lrrulet, lshrtrun
      integer lsources, lsputter, lstat, lsymetry, lunit, lvolsrc, lwall
      integer lwalldst, maxerrs, mparts, ncount, nexit, nhyd(2)
      integer nocols, nohbs, nohzs, norows, nosplits, notasks, notzs
      double precision engymin, h2frac, lchex, leh0, plsang, rmajor
      double precision rminor, rrengy, scrrmax, shethp, sndspd, te0
      double precision wtmin0, xlen, ylen, zlen
      integer novbs, novzs, nowals, nwriter, nseed(4), ntty
      double precision deni0 ( npis)
      pointer(pdeni0,deni0)
      double precision fictrr0 ( npns)
      pointer(pfictrr0,fictrr0)
      integer nosegsxz ( npw)
      pointer(pnosegsxz,nosegsxz)
      integer nosegsy ( npw)
      pointer(pnosegsy,nosegsy)
      double precision t0puff ( npns)
      pointer(pt0puff,t0puff)
      double precision ti0 ( npis)
      pointer(pti0,ti0)
      common /wdf50/ lflags, lgeomtry, lhalpha, lmaxwell, lmesh
      common /wdf50/ lnamelst, lneutral, loutput, lplasma, lprofh
      common /wdf50/ lproft, lprofv, lrandom, lrecycle, lrflct1, lrflct2
      common /wdf50/ lrrulet, lshrtrun, lsources, lsputter, lstat
      common /wdf50/ lsymetry, lunit, lvolsrc, lwall, lwalldst, maxerrs
      common /wdf50/ mparts, ncount, nexit, nhyd, nocols, nohbs, nohzs
      common /wdf50/ norows, nosplits, notasks, notzs, novbs, novzs
      common /wdf50/ nowals, nwriter, nseed, ntty
      common /wdf53/ engymin, h2frac, lchex, leh0, plsang, rmajor
      common /wdf53/ rminor, rrengy, scrrmax, shethp, sndspd, te0
      common /wdf53/ wtmin0, xlen, ylen, zlen
      common /wdf56/ pdeni0, pfictrr0, pnosegsxz
      common /wdf56/ pnosegsy, pt0puff, pti0
c End of Degas1

c Group Degas2
      character*8 kwmat(1000,10)
      double precision arcdeg ( nptp1)
      pointer(parcdeg,arcdeg)
      double precision currxzt ( npsegxz,npsegy,npw,npis)
      pointer(pcurrxzt,currxzt)
      double precision denehvt ( nptsvb,nptshb,nptskb)
      pointer(pdenehvt,denehvt)
      double precision denihvt ( nptsvb,nptshb,nptskb,npis)
      pointer(pdenihvt,denihvt)
      double precision ficrrhvt ( nptsvb,nptshb,nptskb,npns)
      pointer(pficrrhvt,ficrrhvt)
      double precision frabsorb ( npsegxz,npsegy,npw,npns)
      pointer(pfrabsorb,frabsorb)
      double precision gridx ( nptsvb,nptshb,nptskb)
      pointer(pgridx,gridx)
      double precision gridz ( nptsvb,nptshb,nptskb)
      pointer(pgridz,gridz)
      integer kplrecyc ( nptsvb,nptshb)
      pointer(pkplrecyc,kplrecyc)
      integer ksplzone ( nptsvb,nptshb,nptskb)
      pointer(pksplzone,ksplzone)
      integer kzone1 ( nptsvb,nptshb)
      pointer(pkzone1,kzone1)
      integer kzone2 ( nptsvb,nptshb)
      pointer(pkzone2,kzone2)
      integer lboun1 ( nptsvb)
      pointer(plboun1,lboun1)
      integer lboun2 ( nptshb)
      pointer(plboun2,lboun2)
      double precision rflcoef ( npsegxz,npsegy,npw)
      pointer(prflcoef,rflcoef)
      double precision tehvt ( nptsvb,nptshb,nptskb)
      pointer(ptehvt,tehvt)
      double precision tihvt ( nptsvb,nptshb,nptskb,npis)
      pointer(ptihvt,tihvt)
      double precision twall ( npsegxz,npsegy,npw)
      pointer(ptwall,twall)
      double precision vflowx ( nptsvb,nptshb,nptskb)
      pointer(pvflowx,vflowx)
      double precision vflowy ( nptsvb,nptshb,nptskb)
      pointer(pvflowy,vflowy)
      double precision vflowz ( nptsvb,nptshb,nptskb)
      pointer(pvflowz,vflowz)
      double precision vsorchvt ( nptsvb,nptshb,nptskb,npns)
      pointer(pvsorchvt,vsorchvt)
      double precision xwall ( nptsw,npw)
      pointer(pxwall,xwall)
      double precision zwall ( nptsw,npw)
      pointer(pzwall,zwall)
      common /wdf10003/ kwmat
      common /wdf66/ parcdeg, pcurrxzt, pdenehvt
      common /wdf66/ pdenihvt, pficrrhvt, pfrabsorb
      common /wdf66/ pgridx, pgridz, pkplrecyc
      common /wdf66/ pksplzone, pkzone1, pkzone2
      common /wdf66/ plboun1, plboun2, prflcoef
      common /wdf66/ ptehvt, ptihvt, ptwall
      common /wdf66/ pvflowx, pvflowy, pvflowz
      common /wdf66/ pvsorchvt, pxwall, pzwall
c End of Degas2

c Group Eqdsk
      double precision xdimw, zdimw, rgrid1w, etimew, bcentrw, rcentrw
      double precision rmagxw, zmagxw, simagxw, sibdryw, rsepsw, zsepsw
      double precision rvsinw, zvsinw, rvsoutw, zvsoutw
      integer eshotw, nlimw
      double precision xlimw ( nlimw)
      pointer(pxlimw,xlimw)
      double precision ylimw ( nlimw)
      pointer(pylimw,ylimw)
      common /wdf70/ eshotw, nlimw
      common /wdf73/ xdimw, zdimw, rgrid1w, etimew, bcentrw, rcentrw
      common /wdf73/ rmagxw, zmagxw, simagxw, sibdryw, rsepsw, zsepsw
      common /wdf73/ rvsinw, zvsinw, rvsoutw, zvsoutw
      common /wdf76/ pxlimw, pylimw
c End of Eqdsk

c Group Urun
c End of Urun



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call wdfdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Dimwdf")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"noregsw",varadr(noregsw),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptsvb",varadr(nptsvb),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptshb",varadr(nptshb),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptskb",varadr(nptskb),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npw",varadr(npw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npsegxz",varadr(npsegxz),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptsw",varadr(nptsw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npsegy",varadr(npsegy),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptp1",varadr(nptp1),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ndec",varadr(ndec),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npis",varadr(npis),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npns",varadr(npns),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mpsegxz",varadr(mpsegxz),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mpw",varadr(mpw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"idimw",varadr(idimw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jdimw",varadr(jdimw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nixw",varadr(nixw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Auxw")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixpt1b",varadr(ixpt1b),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixtop1b",varadr(ixtop1b),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixtop2b",varadr(ixtop2b),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixpt2b",varadr(ixpt2b),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nohzsb",varadr(nohzsb),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"novzsb",varadr(novzsb),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nosegsxzb",varadr(nosegsxzb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Linkgrd")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pcmeshxw )
      i0001234=rtvare(drtdm,"cmeshxw",i000addr,1,'double precision',
     &   '(idimw,jdimw)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcmeshyw )
      i0001234=rtvare(drtdm,"cmeshyw",i000addr,1,'double precision',
     &   '(idimw,jdimw)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pilmaxw )
      i0001234=rtvare(drtdm,"ilmaxw",i000addr,1,'integer','(noregsw)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixpointw )
      i0001234=rtvare(drtdm,"ixpointw",i000addr,1,'integer',
     &   '(nixw,noregsw)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pjsptrxw )
      i0001234=rtvare(drtdm,"jsptrxw",i000addr,1,'integer','(noregsw)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jaxisw",varadr(jaxisw),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pjminw )
      i0001234=rtvare(drtdm,"jminw",i000addr,1,'integer','(noregsw)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pjmaxw )
      i0001234=rtvare(drtdm,"jmaxw",i000addr,1,'integer','(noregsw)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Nodew")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pjindx )
      i0001234=rtvare(drtdm,"jindx",i000addr,1,'integer','(ndec)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"njwall",varadr(njwall),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnodedwn )
      i0001234=rtvare(drtdm,"nodedwn",i000addr,1,'integer','(ndec)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnodewl )
      i0001234=rtvare(drtdm,"nodewl",i000addr,1,'integer',
     &   '(nptshb,ndec)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnopts )
      i0001234=rtvare(drtdm,"nopts",i000addr,1,'integer','(ndec)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( numseg )
      i0001234=rtvare(drtdm,"numseg",i000addr,0,'integer','(3)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwalnodx )
      i0001234=rtvare(drtdm,"walnodx",i000addr,1,'double precision',
     &   '(nptshb,ndec)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwalnody )
      i0001234=rtvare(drtdm,"walnody",i000addr,1,'double precision',
     &   '(nptshb,ndec)', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Options")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iswdfon",varadr(iswdfon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"fname",varadr(fname),0,'character*16',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"idline",varadr(idline),0,'character*(80)',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"endmark",varadr(endmark),0,'character*(8)',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ivnull",varadr(ivnull),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"frr01",varadr(frr01),0,'double precision',
     &   'scalar', "/sec")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"frr02",varadr(frr02),0,'double precision',
     &   'scalar', "/sec")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Degas1")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pdeni0 )
      i0001234=rtvare(drtdm,"deni0",i000addr,1,'double precision',
     &   '(npis)', "/cm**3")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"engymin",varadr(engymin),0,
     &   'double precision','scalar', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfictrr0 )
      i0001234=rtvare(drtdm,"fictrr0",i000addr,1,'double precision',
     &   '(npns)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"h2frac",varadr(h2frac),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lchex",varadr(lchex),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"leh0",varadr(leh0),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lflags",varadr(lflags),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lgeomtry",varadr(lgeomtry),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lhalpha",varadr(lhalpha),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lmaxwell",varadr(lmaxwell),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lmesh",varadr(lmesh),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lnamelst",varadr(lnamelst),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lneutral",varadr(lneutral),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"loutput",varadr(loutput),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lplasma",varadr(lplasma),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lprofh",varadr(lprofh),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lproft",varadr(lproft),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lprofv",varadr(lprofv),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lrandom",varadr(lrandom),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lrecycle",varadr(lrecycle),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lrflct1",varadr(lrflct1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lrflct2",varadr(lrflct2),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lrrulet",varadr(lrrulet),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lshrtrun",varadr(lshrtrun),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lsources",varadr(lsources),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lsputter",varadr(lsputter),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lstat",varadr(lstat),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lsymetry",varadr(lsymetry),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lunit",varadr(lunit),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lvolsrc",varadr(lvolsrc),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lwall",varadr(lwall),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lwalldst",varadr(lwalldst),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"maxerrs",varadr(maxerrs),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mparts",varadr(mparts),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncount",varadr(ncount),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nexit",varadr(nexit),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nhyd )
      i0001234=rtvare(drtdm,"nhyd",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nocols",varadr(nocols),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nohbs",varadr(nohbs),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nohzs",varadr(nohzs),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"norows",varadr(norows),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnosegsxz )
      i0001234=rtvare(drtdm,"nosegsxz",i000addr,1,'integer','(npw)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnosegsy )
      i0001234=rtvare(drtdm,"nosegsy",i000addr,1,'integer','(npw)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nosplits",varadr(nosplits),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"notasks",varadr(notasks),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"notzs",varadr(notzs),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"novbs",varadr(novbs),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"novzs",varadr(novzs),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nowals",varadr(nowals),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nwriter",varadr(nwriter),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nseed )
      i0001234=rtvare(drtdm,"nseed",i000addr,0,'integer','(4)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntty",varadr(ntty),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"plsang",varadr(plsang),0,'double precision'
     &   ,'scalar', "degrees")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rmajor",varadr(rmajor),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rminor",varadr(rminor),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rrengy",varadr(rrengy),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"scrrmax",varadr(scrrmax),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"shethp",varadr(shethp),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sndspd",varadr(sndspd),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pt0puff )
      i0001234=rtvare(drtdm,"t0puff",i000addr,1,'double precision',
     &   '(npns)', "eV")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,.025d0)
      i0001234=rtvare(drtdm,"te0",varadr(te0),0,'double precision',
     &   'scalar', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pti0 )
      i0001234=rtvare(drtdm,"ti0",i000addr,1,'double precision','(npis)'
     &   , "eV")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"wtmin0",varadr(wtmin0),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xlen",varadr(xlen),0,'double precision',
     &   'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ylen",varadr(ylen),0,'double precision',
     &   'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zlen",varadr(zlen),0,'double precision',
     &   'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Degas2")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( parcdeg )
      i0001234=rtvare(drtdm,"arcdeg",i000addr,1,'double precision',
     &   '(nptp1)', "degrees")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcurrxzt )
      i0001234=rtvare(drtdm,"currxzt",i000addr,1,'double precision',
     &   '(npsegxz,npsegy,npw,npis)', "/sec")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdenehvt )
      i0001234=rtvare(drtdm,"denehvt",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "/cm**3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdenihvt )
      i0001234=rtvare(drtdm,"denihvt",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb,npis)', "/cm**3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pficrrhvt )
      i0001234=rtvare(drtdm,"ficrrhvt",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb,npns)', "/sec")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfrabsorb )
      i0001234=rtvare(drtdm,"frabsorb",i000addr,1,'double precision',
     &   '(npsegxz,npsegy,npw,npns)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgridx )
      i0001234=rtvare(drtdm,"gridx",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "cm")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgridz )
      i0001234=rtvare(drtdm,"gridz",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "cm")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pkplrecyc )
      i0001234=rtvare(drtdm,"kplrecyc",i000addr,1,'integer',
     &   '(nptsvb,nptshb)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pksplzone )
      i0001234=rtvare(drtdm,"ksplzone",i000addr,1,'integer',
     &   '(nptsvb,nptshb,nptskb)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( kwmat )
      i0001234=rtvare(drtdm,"kwmat",i000addr,0,'character*8','(1000,10)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pkzone1 )
      i0001234=rtvare(drtdm,"kzone1",i000addr,1,'integer',
     &   '(nptsvb,nptshb)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pkzone2 )
      i0001234=rtvare(drtdm,"kzone2",i000addr,1,'integer',
     &   '(nptsvb,nptshb)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plboun1 )
      i0001234=rtvare(drtdm,"lboun1",i000addr,1,'integer','(nptsvb)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plboun2 )
      i0001234=rtvare(drtdm,"lboun2",i000addr,1,'integer','(nptshb)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prflcoef )
      i0001234=rtvare(drtdm,"rflcoef",i000addr,1,'double precision',
     &   '(npsegxz,npsegy,npw)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptehvt )
      i0001234=rtvare(drtdm,"tehvt",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptihvt )
      i0001234=rtvare(drtdm,"tihvt",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb,npis)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptwall )
      i0001234=rtvare(drtdm,"twall",i000addr,1,'double precision',
     &   '(npsegxz,npsegy,npw)', "degrees K")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pvflowx )
      i0001234=rtvare(drtdm,"vflowx",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "cm/sec")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pvflowy )
      i0001234=rtvare(drtdm,"vflowy",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "cm/sec")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pvflowz )
      i0001234=rtvare(drtdm,"vflowz",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb)', "cm/sec")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pvsorchvt )
      i0001234=rtvare(drtdm,"vsorchvt",i000addr,1,'double precision',
     &   '(nptsvb,nptshb,nptskb,npns)', "/sec")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxwall )
      i0001234=rtvare(drtdm,"xwall",i000addr,1,'double precision',
     &   '(nptsw,npw)', "cm")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzwall )
      i0001234=rtvare(drtdm,"zwall",i000addr,1,'double precision',
     &   '(nptsw,npw)', "cm")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Eqdsk")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xdimw",varadr(xdimw),0,'double precision',
     &   'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zdimw",varadr(zdimw),0,'double precision',
     &   'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rgrid1w",varadr(rgrid1w),0,
     &   'double precision','scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"eshotw",varadr(eshotw),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"etimew",varadr(etimew),0,'double precision'
     &   ,'scalar', "msec")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"bcentrw",varadr(bcentrw),0,
     &   'double precision','scalar', "Tesla")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rcentrw",varadr(rcentrw),0,
     &   'double precision','scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rmagxw",varadr(rmagxw),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zmagxw",varadr(zmagxw),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"simagxw",varadr(simagxw),0,
     &   'double precision','scalar', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sibdryw",varadr(sibdryw),0,
     &   'double precision','scalar', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rsepsw",varadr(rsepsw),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zsepsw",varadr(zsepsw),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rvsinw",varadr(rvsinw),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zvsinw",varadr(zvsinw),0,'double precision'
     &   ,'scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rvsoutw",varadr(rvsoutw),0,
     &   'double precision','scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zvsoutw",varadr(zvsoutw),0,
     &   'double precision','scalar', "cm")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nlimw",varadr(nlimw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxlimw )
      i0001234=rtvare(drtdm,"xlimw",i000addr,1,'double precision',
     &   '(nlimw)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pylimw )
      i0001234=rtvare(drtdm,"ylimw",i000addr,1,'double precision',
     &   '(nlimw)', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Urun")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "write_degas",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "write_namelist",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "frrate",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "ueplasma",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"wdf.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine wdfxpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.9) then
         call wdfxp9(name1234)
      else
         call baderr('wdfxpf: impossible event')
      endif
      return
      end
      subroutine wdfxp9(name1234)
cProlog
      character*(*) name1234
      external wdf_handler
      external write_degas
      external write_namelist
      external frrate
      external ueplasma
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'write_degas') then
         call parexecf(wdf_handler, 0, write_degas)
      elseif (name1234 .eq. 'write_namelist') then
         call parexecf(wdf_handler, 1, write_namelist)
      elseif (name1234 .eq. 'frrate') then
         call parexecf(wdf_handler, 2, frrate)
      elseif (name1234 .eq. 'ueplasma') then
         call parexecf(wdf_handler, 3, ueplasma)
      else
         call baderr('wdfxp9: impossible event: '//name5678)
      endif
      return
      end
      function wdfbfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer wdfbfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in wdf')
      call baderr(name1234)
      wdfbfcn = -1
      return
      end
