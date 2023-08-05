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
c     ./../wdf.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c









































































      subroutine write_degas
cProlog
      implicit none
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny from com package
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
c ixpt1,ixpt2 from com package
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
c geometry from com package
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf
c nptsvb,nptshb,nptskb,nptsw,npsegxz
c Group Auxw
      integer ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      integer nosegsxzb
      common /wdf10/ ixpt1b, ixtop1b, ixtop2b, ixpt2b, nohzsb, novzsb
      common /wdf10/ nosegsxzb
c End of Auxw
c ixpt1b,ixpt2b,ixtop1b,ixtop2b,
c nohzsb,novzsb,nosegsxzb
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
c iswdfon

c     main driver routine for wdf package

      if (mod((ixpt2(1)-ixpt1(1)),2) .ne. 0) then
         call remark(" ")
         call remark("*** Error:  write_degas procedure only valid when"
     &      )
         call remark("               ixpt2-ixpt1 is an even number")
         call remark(" ")
         call xerrab("")
      endif

c     allocate arrays for DEGAS

      ixpt1b = ixpt1(1)
      ixtop1b = ixpt1b + (ixpt2(1)-ixpt1(1))/2
      ixtop2b = ixtop1b + 1
      ixpt2b = ixpt2(1)
      if (geometry .eq. "dnbot") then
c we omit guard cells at the midplane
         ixtop1b=ixtop1b-1
c of up/down symmetric double nulls
         ixtop2b=ixtop2b+1
      endif

      novzsb = max(ixtop1b+2,nx-ixtop2b+3)
      nohzsb = 2*(ny+1)
      nosegsxzb = 2*novzsb+nohzsb+3

      nptsvb = nohzsb + 1
      nptshb = novzsb + 1
      nptsw = 2*nptshb + nptsvb + 1
      npsegxz = nptsw - 1
      call gallot("Degas1",0)
      call gallot("Degas2",0)
      call remark("***** allocated DEGAS arrays *****")

c     read data from grd and bbb packages
      if (iswdfon.eq.1) then
c write grd-wdf file from grd package
         call grd2wdf
c read grid data from grd package
         call readgrd
c write bbb-wdf file from bbb package
         call bbb2wdf
c read plasma data from bbb package
         call readbbb
      endif
c
c generate grid and wall arrays for DEGAS
      call degasgrid
c generate kzone arrays for DEGAS
      call defaultz
c write UEDGE plasma into DEGAS arrays
      call ueplasma
c convert from UEDGE to DEGAS units
      call cgsunits
c write DEGAS namelist input file
      call write_namelist

      return
      end

c----------------------------------------------------------------------c

      subroutine readgrd
cProlog
      implicit none
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      integer iunit, ios
      external remark, xerrab, gallot, allot
      external rdgrd1, rdgrd2, rdgrd3

c **************** read the output of the grd package ******************

      data iunit /55/
      open (iunit, file='grd-wdf', form='unformatted', iostat=ios, 
     &   status='old')
      if (ios .ne. 0) then
         call xerrab("**** grd-wdf file not found")
      endif

c     read dimensioning parameters and allot storage space for arrays --

      read (iunit) idimw,jdimw,nixw,noregsw
      call gallot("Linkgrd",0)
      call rdgrd1 (iunit)

      call rdgrd2 (iunit)

      read(iunit) nlimw
      call allot("xlimw",nlimw)
      call allot("ylimw",nlimw)

      call rdgrd3 (iunit)

      close(iunit)

      return
      end

c----------------------------------------------------------------------c

      subroutine rdgrd1 (iunit)
cProlog
      implicit none
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      integer iunit

      read (iunit) cmeshxw,cmeshyw, ilmaxw,ixpointw,jminw,jmaxw,jsptrxw,
     &   jaxisw

      return
      end

c----------------------------------------------------------------------c

      subroutine rdgrd2 (iunit)
cProlog
      implicit none
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      integer iunit

      read (iunit) bcentrw,rcentrw,rmagxw,zmagxw,simagxw,sibdryw, 
     &   rgrid1w,xdimw,zdimw

      return
      end

c----------------------------------------------------------------------c

      subroutine rdgrd3 (iunit)
cProlog
      implicit none
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      integer iunit

      read (iunit) xlimw,ylimw
      read (iunit) eshotw,etimew,rsepsw,zsepsw, rvsinw,zvsinw,rvsoutw,
     &   zvsoutw

      return
      end

c----------------------------------------------------------------------c

      subroutine degasgrid
cProlog
      implicit none
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nxm,nym from com package
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
c rm,zm from com package
c Group Linkbbb
      integer nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb, nxcore1bbb
      character*8 geometrybbb
      integer nxleg2bbb, nxcore2bbb

      double precision nibbb ( 0:nx+1,0:ny+1)
      pointer(pnibbb,nibbb)

      double precision tibbb ( 0:nx+1,0:ny+1)
      pointer(ptibbb,tibbb)

      double precision nebbb ( 0:nx+1,0:ny+1)
      pointer(pnebbb,nebbb)

      double precision tebbb ( 0:nx+1,0:ny+1)
      pointer(ptebbb,tebbb)

      double precision vflowxbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowxbbb,vflowxbbb)

      double precision vflowybbb ( 0:nx+1,0:ny+1)
      pointer(pvflowybbb,vflowybbb)

      double precision vflowzbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowzbbb,vflowzbbb)

      double precision fnixbbb ( 0:nx+1,0:ny+1)
      pointer(pfnixbbb,fnixbbb)

      double precision fngysibbb ( 0:nx+1)
      pointer(pfngysibbb,fngysibbb)

      double precision fngysobbb ( 0:nx+1)
      pointer(pfngysobbb,fngysobbb)
      common /com10007/ geometrybbb
      common /com150/ nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb
      common /com150/ nxcore1bbb, nxleg2bbb, nxcore2bbb
      common /com156/ pnibbb, ptibbb, pnebbb
      common /com156/ ptebbb, pvflowxbbb, pvflowybbb
      common /com156/ pvflowzbbb, pfnixbbb, pfngysibbb
      common /com156/ pfngysobbb
c End of Linkbbb
c nxbbb,nybbb from com package
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
c ixpt1b,ixpt2b,ixtop1b,ixtop2b
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

      integer ix,iy,i,j,itot,n
c
c     *** copy UEDGE (rm,zm) onto DEGAS (gridx,gridz)
c

c First, the inboard half of the mesh:
      do 23000 iy = 0, nybbb
         j = nybbb - iy + 1
         i = 1
         gridx(j,i,1) = rm(ixtop1b,iy,4) - rgrid1w
         gridz(j,i,1) = zm(ixtop1b,iy,4)
         do 23002 ix = ixtop1b, ixpt1b+1, -1
            i = i + 1
            gridx(j,i,1) = rm(ix,iy,3) - rgrid1w
            gridz(j,i,1) = zm(ix,iy,3)
23002    continue
         i = i + 1
         gridx(j,i,1) = gridx(j,i-1,1)
         gridz(j,i,1) = gridz(j,i-1,1)
         i = i + 1
         gridx(j,i,1) = rm(ixpt1b,iy,4) - rgrid1w
         gridz(j,i,1) = zm(ixpt1b,iy,4)
         do 23004 ix = ixpt1b, 1, -1
            i = i + 1
            gridx(j,i,1) = rm(ix,iy,3) - rgrid1w
            gridz(j,i,1) = zm(ix,iy,3)
23004    continue
23000 continue
c fill out the arrays by duplicating plate data
c while(i .lt. nptshb)
23006 if (i .lt. nptshb) then
         i = i + 1
         do 23008 j = 1, nybbb+1
            gridx(j,i,1) = gridx(j,i-1,1)
            gridz(j,i,1) = gridz(j,i-1,1)
23008    continue
         go to 23006
      endif
c endwhile
c Next, the outboard half of the mesh:
      do 23010 iy = 0, nybbb
         j = nybbb + iy + 3
         i = 1
         gridx(j,i,1) = rm(ixtop2b,iy,3) - rgrid1w
         gridz(j,i,1) = zm(ixtop2b,iy,3)
         do 23012 ix = ixtop2b, ixpt2b
            i = i + 1
            gridx(j,i,1) = rm(ix,iy,4) - rgrid1w
            gridz(j,i,1) = zm(ix,iy,4)
23012    continue
         i = i + 1
         gridx(j,i,1) = gridx(j,i-1,1)
         gridz(j,i,1) = gridz(j,i-1,1)
         i = i + 1
         gridx(j,i,1) = rm(ixpt2b+1,iy,3) - rgrid1w
         gridz(j,i,1) = zm(ixpt2b+1,iy,3)
         do 23014 ix = ixpt2b+1, nxbbb
            i = i + 1
            gridx(j,i,1) = rm(ix,iy,4) - rgrid1w
            gridz(j,i,1) = zm(ix,iy,4)
23014    continue
23010 continue
c fill out the arrays by duplicating plate data
c while(i .lt. nptshb)
23016 if (i .lt. nptshb) then
         i = i + 1
         do 23018 j = nybbb+3, 2*nybbb+3
            gridx(j,i,1) = gridx(j,i-1,1)
            gridz(j,i,1) = gridz(j,i-1,1)
23018    continue
         go to 23016
      endif
c endwhile
c Finally, the "magnetic axis" for core and private flux regions
      j = nybbb + 2
      do 23020 i = 1, ixtop1b-ixpt1b+2
         gridx(j,i,1) = rmagxw - rgrid1w
         gridz(j,i,1) = zmagxw
23020 continue
      do 23022 i = ixtop1b-ixpt1b+3, nptshb
         gridx(j,i,1) = 0.5d0*(gridx(j-1,nptshb,1)+gridx(j+1,nptshb,1))
         gridz(j,i,1) = 0.5d0*(gridz(j-1,nptshb,1)+gridz(j+1,nptshb,1))
23022 continue

c Wall construction:
      nowals = 3

c First, clockwise around the outside of the mesh
      j=1
      itot=0
      do 23024 i=1,nptshb
         itot=itot+1
         xwall(itot,1)=gridx(j,i,1)
         zwall(itot,1)=gridz(j,i,1)
23024 continue
c
      i=nptshb
      do 23026 j=1,nptsvb
         itot=itot+1
         xwall(itot,1)=gridx(j,i,1)
         zwall(itot,1)=gridz(j,i,1)
23026 continue
c
      j=nptsvb
      do 23028 i=nptshb,1,-1
         itot=itot+1
         xwall(itot,1)=gridx(j,i,1)
         zwall(itot,1)=gridz(j,i,1)
23028 continue
c re-connect with starting point
      itot=itot+1
      xwall(itot,1)=xwall(1,1)
      zwall(itot,1)=zwall(1,1)
      nosegsxz(1)=itot-1
c set default values for kwmat and twall -
      do 23030 n = 1, nosegsxz(1)
c room temperature
         twall(n,1,1) = 300.d0
c carbon
         kwmat(n,1) = "'c'"
23030 continue

c Second, clockwise around the private flux
      itot=1
      i=nptshb
c start at "magnetic axis" point
      j=nybbb+2
      xwall(itot,2)=gridx(j,i,1)
      zwall(itot,2)=gridz(j,i,1)
c jump to inboard half of p.f.
      j=j-1
      do 23032 i=ixtop1b+3,ixtop1b-ixpt1b+3,-1
         itot=itot+1
         xwall(itot,2)=gridx(j,i,1)
         zwall(itot,2)=gridz(j,i,1)
23032 continue
c jump to outboard half of p.f.
      j=j+2
      do 23034 i=ixpt2b-ixtop2b+4,nxbbb-ixtop2b+4
         itot=itot+1
         xwall(itot,2)=gridx(j,i,1)
         zwall(itot,2)=gridz(j,i,1)
23034 continue
c re-connect with starting point
      itot=itot+1
      xwall(itot,2)=xwall(1,2)
      zwall(itot,2)=zwall(1,2)
      nosegsxz(2)=itot-1
c set default values for kwmat and twall -
      do 23036 n = 1, nosegsxz(2)
c room temperature
         twall(n,1,2) = 300.d0
c carbon
         kwmat(n,2) = "'c'"
23036 continue

c Third, clockwise around the core
      itot=0
      j=nybbb+1
      do 23038 i=ixtop1b-ixpt1b+2,1,-1
         itot=itot+1
         xwall(itot,3)=gridx(j,i,1)
         zwall(itot,3)=gridz(j,i,1)
23038 continue
      j=j+2
      do 23040 i=1,ixtop1b-ixpt1b+2
         itot=itot+1
         xwall(itot,3)=gridx(j,i,1)
         zwall(itot,3)=gridz(j,i,1)
23040 continue
c re-connect with starting point
      itot=itot+1
      xwall(itot,3)=xwall(1,3)
      zwall(itot,3)=zwall(1,3)
      nosegsxz(3)=itot-1
c set default values for kwmat and twall -
      do 23042 n = 1, nosegsxz(3)
c room temperature
         twall(n,1,3) = 300.d0
c carbon
         kwmat(n,3) = "'c'"
23042 continue

      return
      end


c----------------------------------------------------------------------c

      subroutine readbbb
cProlog
      implicit none
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Linkbbb
      integer nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb, nxcore1bbb
      character*8 geometrybbb
      integer nxleg2bbb, nxcore2bbb

      double precision nibbb ( 0:nx+1,0:ny+1)
      pointer(pnibbb,nibbb)

      double precision tibbb ( 0:nx+1,0:ny+1)
      pointer(ptibbb,tibbb)

      double precision nebbb ( 0:nx+1,0:ny+1)
      pointer(pnebbb,nebbb)

      double precision tebbb ( 0:nx+1,0:ny+1)
      pointer(ptebbb,tebbb)

      double precision vflowxbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowxbbb,vflowxbbb)

      double precision vflowybbb ( 0:nx+1,0:ny+1)
      pointer(pvflowybbb,vflowybbb)

      double precision vflowzbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowzbbb,vflowzbbb)

      double precision fnixbbb ( 0:nx+1,0:ny+1)
      pointer(pfnixbbb,fnixbbb)

      double precision fngysibbb ( 0:nx+1)
      pointer(pfngysibbb,fngysibbb)

      double precision fngysobbb ( 0:nx+1)
      pointer(pfngysobbb,fngysobbb)
      common /com10007/ geometrybbb
      common /com150/ nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb
      common /com150/ nxcore1bbb, nxleg2bbb, nxcore2bbb
      common /com156/ pnibbb, ptibbb, pnebbb
      common /com156/ ptebbb, pvflowxbbb, pvflowybbb
      common /com156/ pvflowzbbb, pfnixbbb, pfngysibbb
      common /com156/ pfngysobbb
c End of Linkbbb

      integer iunit, ios
      external remark, xerrab, gallot, allot

c **************** read the output of the bbb package ******************

      data iunit /55/
      open (iunit, file='bbb-wdf', form='unformatted', iostat=ios, 
     &   status='old')
      if (ios .ne. 0) then
         call xerrab("**** bbb-wdf file not found")
      endif

      read (iunit) nxbbb,nybbb,nycorebbb,nysolbbb,nxleg1bbb,nxcore1bbb, 
     &   nxleg2bbb,nxcore2bbb
      read (iunit) nibbb,tibbb,nebbb,tebbb,vflowxbbb,vflowybbb,vflowzbbb
     &   , fnixbbb,fngysibbb,fngysobbb
      read (iunit) geometrybbb

      close (iunit)

      return
      end

c----------------------------------------------------------------------c

      subroutine ueplasma
cProlog
      implicit none
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c from com package
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
c from com package
c Group Linkbbb
      integer nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb, nxcore1bbb
      character*8 geometrybbb
      integer nxleg2bbb, nxcore2bbb

      double precision nibbb ( 0:nx+1,0:ny+1)
      pointer(pnibbb,nibbb)

      double precision tibbb ( 0:nx+1,0:ny+1)
      pointer(ptibbb,tibbb)

      double precision nebbb ( 0:nx+1,0:ny+1)
      pointer(pnebbb,nebbb)

      double precision tebbb ( 0:nx+1,0:ny+1)
      pointer(ptebbb,tebbb)

      double precision vflowxbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowxbbb,vflowxbbb)

      double precision vflowybbb ( 0:nx+1,0:ny+1)
      pointer(pvflowybbb,vflowybbb)

      double precision vflowzbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowzbbb,vflowzbbb)

      double precision fnixbbb ( 0:nx+1,0:ny+1)
      pointer(pfnixbbb,fnixbbb)

      double precision fngysibbb ( 0:nx+1)
      pointer(pfngysibbb,fngysibbb)

      double precision fngysobbb ( 0:nx+1)
      pointer(pfngysobbb,fngysobbb)
      common /com10007/ geometrybbb
      common /com150/ nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb
      common /com150/ nxcore1bbb, nxleg2bbb, nxcore2bbb
      common /com156/ pnibbb, ptibbb, pnebbb
      common /com156/ ptebbb, pvflowxbbb, pvflowybbb
      common /com156/ pvflowzbbb, pfnixbbb, pfngysibbb
      common /com156/ pfngysobbb
c End of Linkbbb

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
c ixpt1b,ixpt2b,ixtop1b,ixtop2b,nosegsxzb,novzsb
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

      integer ix,iy,jh,iv,iseg

c     Convert UEDGE plasma information to DEGAS namelist arrays

      do 23000 ix=1,nxbbb
         do 23002 iy=1,nybbb
c translate UEDGE cell index (ix,iy) to DEGAS cell index (iv,jh)
            if ((1 .le. ix) .and. (ix .le. ixpt1b)) then
               jh = nybbb + 1 - iy
               iv = ixtop1b + 3 - ix
            elseif ((ixpt1b+1 .le. ix) .and. (ix .le. ixtop1b)) then
               jh = nybbb + 1 - iy
               iv = ixtop1b + 1 - ix
            elseif ((ixtop2b .le. ix) .and. (ix .le. ixpt2b)) then
               jh = nybbb + 2 + iy
               iv = ix - ixtop2b + 1
            elseif ((ixpt2b+1 .le. ix) .and. (ix .le. nxbbb)) then
               jh = nybbb + 2 + iy
               iv = ix - ixtop2b + 3
            endif
            denihvt(jh,iv,1,1) = nibbb(ix,iy)
            tihvt(jh,iv,1,1) = tibbb(ix,iy)
            denehvt(jh,iv,1) = nebbb(ix,iy)
            tehvt(jh,iv,1) = tebbb(ix,iy)
            vflowx(jh,iv,1) = vflowxbbb(ix,iy)
            vflowy(jh,iv,1) = vflowybbb(ix,iy)
            vflowz(jh,iv,1) = vflowzbbb(ix,iy)
23002    continue
23000 continue

      do 23004 iy=1,nybbb
c translate UEDGE plate index (0,iy) to DEGAS wall segment index (iseg)
         iseg = novzsb + 1 + (nybbb + 1 - iy)
         currxzt(iseg,1,1,1) = - fnixbbb(0,iy)
c translate UEDGE plate index (nxm,iy) to DEGAS wall segment index (iseg)
         iseg = novzsb + 1 + nybbb + 2 + (iy)
         currxzt(iseg,1,1,1) = fnixbbb(nxbbb,iy)
23004 continue

c translate UEDGE private flux wall index (ix) to DEGAS private region
c wall segment index (iseg) on wall number 2
      do 23006 ix=1,ixpt1b
         iseg = 1 + ix
c NOTE negative for puffing
         currxzt(iseg,1,2,1) = - abs(fngysibbb(ix))
23006 continue
      do 23008 ix=ixpt2b+1,nxbbb
         iseg = 1 + ixpt1b + 1 + (ix-ixpt2b)
         currxzt(iseg,1,2,1) = - abs(fngysibbb(ix))
23008 continue

c translate UEDGE outermost flux wall index (ix) to DEGAS external
c wall segment index (iseg) on wall number 1
      do 23010 ix=1,ixtop1b
         iseg = ixtop1b-ix+1
         currxzt(iseg,1,1,1) = - abs(fngysobbb(ix))
23010 continue
      do 23012 ix=ixtop2b,nxbbb
         iseg = nosegsxzb-ix+ixtop2b-1
         currxzt(iseg,1,1,1) = - abs(fngysobbb(ix))
23012 continue

      return
      end

c----------------------------------------------------------------------c

      subroutine defaultz
cProlog
      integer jb,jj,ib,ii
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
c ixpt1b
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


c.....Initialize some variables with default values.
      endmark = " $"
      fname = "degas.in"
      idline = "plasma information from UEDGE"

c.....Define default plasma zone boundaries.
c.....along horizontal direction
      jb=0
      do 23000 jj=1,nptsvb,1
         jb = jb +1
         lboun1(jb) = jj
23000 continue
      nohbs = jb
      nohzs = nohbs -1
c.....along vertical direction
      ib=0
      do 23002 ii=1,nptshb,1
         ib = ib + 1
         lboun2(ib) = ii
23002 continue
      novbs = ib
      novzs = novbs - 1

c vertical index of non-physical zone
      ivnull = ixtop1b - ixpt1b + 2
c between core and private flux

c.....set kzone arrays
      call setkz

c.....Set default values for other DEGAS input parameters -
      xlen = xdimw
      zlen = zdimw
      rmajor = rgrid1w + xdimw/2.d0

      return
      end

c----------------------------------------------------------------------c

      subroutine setkz
cProlog
      implicit none
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      integer i,j,iv,jh,kzvalue

c.....Define kzone arrays for DEGAS
      do 23000 jh=1,nohzs
         do 23002 j=lboun1(jh),lboun1(jh+1)-1
            kzone1(j,1)=jh
23002    continue
23000 continue
c
      do 23004 i=2,nptshb-1
         do 23006 j=1,nptsvb-1
            kzone1(j,i)=kzone1(j,1)
23006    continue
23004 continue
c
      do 23008 iv=1,novzs
         do 23010 i=lboun2(iv),lboun2(iv+1)-1
            kzone2(1,i)=iv
23010    continue
23008 continue
c
      do 23012 i=1,nptshb-1
         kzvalue=kzone2(1,i)
         do 23014 j=1,nptsvb-1
            kzone2(j,i)=kzone2(1,i)
            if (kzvalue .eq. ivnull) then
               kzone1(j,i)=-1
               kzone2(j,i)=-1
            endif
23014    continue
23012 continue

      return
      end

c----------------------------------------------------------------------c

      subroutine frrate
cProlog
c.....For neutral atoms,
c.....set fictitious reaction rate = frr01, for denihvt .eq. zero
c.....                             =     0, for denihvt .ne. zero
c.....and similarly for neutral molecules,
c.....set fictitious reaction rate = frr02, for denihvt .eq. zero
c.....                             =     0, for denihvt .ne. zero
      integer j,i
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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


      do 23000 j=1,nohzs
         do 23002 i=1,novzs
            if (denihvt(j,i,1,1) .eq. 0.d0) then
               ficrrhvt(j,i,1,1) = frr01
               ficrrhvt(j,i,1,2) = frr02
            else
               ficrrhvt(j,i,1,1) = 0.d0
               ficrrhvt(j,i,1,2) = 0.d0
            endif
23002    continue
23000 continue

      return
      end

c----------------------------------------------------------------------c

      subroutine cgsunits
cProlog
      implicit none
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      integer i,j,k,l,m,iv,jh
      doubleprecision ev
      data ev/1.6022d-19/

c     Convert lengths from [m] to [cm] for DEGAS

      do 23000 k=1,nptskb
         do 23002 j=1,nptsvb
            do 23004 i=1,nptshb
               gridx(j,i,k)=100.d0*gridx(j,i,k)
               gridz(j,i,k)=100.d0*gridz(j,i,k)
23004       continue
23002    continue
23000 continue

      do 23006 m=1,npw
         do 23008 l=1,nptsw
            xwall(l,m)=100.d0*xwall(l,m)
            zwall(l,m)=100.d0*zwall(l,m)
23008    continue
23006 continue

      xlen=xlen*100.d0
      zlen=zlen*100.d0
      rmajor=rmajor*100.d0

c convert plasma from UEDGE to DEGAS units :
      do 23010 jh=1,nohzs
         do 23012 iv=1,novzs
            denihvt(jh,iv,1,1) = denihvt(jh,iv,1,1) * 1.0d-06
            tihvt(jh,iv,1,1) = tihvt(jh,iv,1,1) / ev
            denehvt(jh,iv,1) = denehvt(jh,iv,1) * 1.0d-06
            tehvt(jh,iv,1) = tehvt(jh,iv,1) / ev
            vflowx(jh,iv,1) = vflowx(jh,iv,1) * 100.d0
            vflowy(jh,iv,1) = vflowy(jh,iv,1) * 100.d0
            vflowz(jh,iv,1) = vflowz(jh,iv,1) * 100.d0
23012    continue
23010 continue

      return
      end

c----------------------------------------------------------------------c

      subroutine write_namelist
cProlog
      integer nunit,i,jwall,k,j,iv,jh
c Group Dimwdf
      integer noregsw, nptsvb, nptshb, nptskb, npw, npsegxz, nptsw
      integer npsegy, nptp1, ndec, npis, npns, mpsegxz, mpw, idimw
      integer jdimw, nixw
      common /wdf00/ noregsw, nptsvb, nptshb, nptskb, npw, npsegxz
      common /wdf00/ nptsw, npsegy, nptp1, ndec, npis, npns, mpsegxz
      common /wdf00/ mpw, idimw, jdimw, nixw
c End of Dimwdf

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

      external remark

c     Write output file to be read by DEGAS code;
c     file name is given by the variable 'fname' in group Io

      data nunit /66/
      open (nunit, file=fname, form='formatted', status='unknown')

      write(nunit,1000)idline
 1000 format(1a80)
c
c     first degas namelist /input/
c
      write(nunit,998)
  998 format(1x,"$input")
      write(nunit, 999) mparts,maxerrs,ncount
  999 format(" mparts=  ",i5," maxerrs= ",i5," ncount=  ",i5)
      write(nunit,1001) lmesh,lprofh,lproft,lprofv, loutput,lrflct1,
     &   lrflct2, lrrulet,lsputter,lsymetry,lunit
 1001 format(" lmesh=   ",i5," lprofh=  ",i5," lproft=  ",i5,
     &   " lprofv=  ",i5/, " loutput= ",i5," lrflct1= ",i5," lrflct2= ",
     &   i5/, " lrrulet= ",i5," lsputter=",i5," lsymetry=",i5,
     &   " lunit=   ",i5)
      write(nunit,1002) nexit,nhyd(1),nocols,nohbs,nohzs,norows
 1002 format(" nexit=   ",i5," nhyd=    ",i5," nocols=  ",i5,
     &   " nohbs=   ",i5/, " nohzs=   ",i5," norows=  ",i5)
      write(nunit,1003)(nosegsxz(i),i=1,nowals)
 1003 format(" nosegsxz=",5(i5,1x))
      write(nunit,1004) nosplits,novbs,novzs,nowals,nptshb,nptsvb
 1004 format(" nosplits=",i5," novbs=   ",i5," novzs=   ",i5,
     &   " nowals=  ",i5/, " nptshb=  ",i5," nptsvb=  ",i5)
      write(nunit,1005) h2frac,plsang,rmajor,scrrmax,xlen,zlen
 1005 format(" h2frac= ",f6.4," plsang= ",f6.2," rmajor= ",f6.2/, 
     &   " scrrmax=",f6.4," xlen=   ",f6.2," zlen=   ",f6.2)
      write(nunit,1006) lmaxwell,shethp
 1006 format(" lmaxwell=",i5," shethp= ",f6.2)
      write(nunit,1007)(t0puff(i),i=1,npns)
 1007 format(" t0puff= ",5(f6.3,9x))
c
      write(nunit,1009)endmark
 1009 format(1a8)
c
c     second degas namelist /arrays/
c
      write(nunit,2000)
 2000 format(1x,"$arrays")

c.....recycling current at divertor plates and walls
      do 23000 jwall=1,nowals
         write(nunit,2001)jwall
         write(nunit,2002)(currxzt(i,1,jwall,1),i=1,nosegsxz(jwall))
23000 continue
 2001 format(1x,"currxzt(1,1,",i1,",1)=")
 2002 format(18x,1p6e10.3)

c.....electron density
      do 23002 i=1,novzs
         write(nunit,2010)i,(denehvt(k,i,1),k=1,min0(6,nohzs))
         do 23004 j=7,nohzs,6
            write(nunit,2011)(denehvt(k,i,1),k=j,min0(j+5,nohzs))
23004    continue
23002 continue
 2010 format(" denehvt(1,",i2,",1)=",1p6e10.3)
 2011 format(17x,1p6e10.3)

c.....ion density
      do 23006 i=1,novzs
         write(nunit,2020)i,(denihvt(k,i,1,1),k=1,min0(6,nohzs))
         do 23008 j=7,nohzs,6
            write(nunit,2021)(denihvt(k,i,1,1),k=j,min0(j+5,nohzs))
23008    continue
23006 continue
 2020 format(" denihvt(1,",i2,",1,1)=",1p6e10.3)
 2021 format(19x,1p6e10.3)

c.....fictitious reaction rate for neutrals

      if (frr01 .ne. 0.d0) then
         do 23010 i=1,novzs
            write(nunit,2030)i,(ficrrhvt(k,i,1,1),k=1,min0(6,nohzs))
            do 23012 j=7,nohzs,6
               write(nunit,2031)(ficrrhvt(k,i,1,1),k=j,min0(j+5,nohzs))
23012       continue
23010    continue
 2030    format(" ficrrhvt(1,",i2,",1,1)=",1p6e9.2)
 2031    format(20x,1p6e9.2)
      endif

      if (frr02 .ne. 0.d0) then
         do 23014 i=1,novzs
            write(nunit,2032)i,(ficrrhvt(k,i,1,2),k=1,min0(6,nohzs))
            do 23016 j=7,nohzs,6
               write(nunit,2033)(ficrrhvt(k,i,1,2),k=j,min0(j+5,nohzs))
23016       continue
23014    continue
 2032    format(" ficrrhvt(1,",i2,",1,2)=",1p6e9.2)
 2033    format(20x,1p6e9.2)
      endif

c.....wall absorption fraction
      do 23018 jwall=1,nowals
         write(nunit,2040)jwall
         write(nunit,2041)(frabsorb(i,1,jwall,1),i=1,nosegsxz(jwall))
23018 continue
 2040 format(1x,"frabsorb(1,1,",i1,",1)=")
 2041 format(19x,5f9.4)

c.....2-d grid coordinates
      do 23020 iv=1,nptshb
         write(nunit,2050)iv
         write(nunit,2051)(gridx(jh,iv,1),jh=1,nptsvb)
         write(nunit,2052)iv
         write(nunit,2051)(gridz(jh,iv,1),jh=1,nptsvb)
23020 continue
 2050 format(1x,'gridx(1,',i3,',1)=')
 2051 format(5(1x,f10.2))
 2052 format(1x,'gridz(1,',i3,',1)=')

c.....flight splitting factors for plasma zones
      if (nosplits .gt. 1) then
         do 23022 i=1,novzs
            write(nunit,2055)i
            write(nunit,2056)(ksplzone(j,i,1),j=1,nohzs)
23022    continue
 2055    format(1x,'ksplzone(1,',i3,',1)=')
 2056    format(20(1x,i2))
      endif

c.....wall materials
      do 23024 jwall=1,nowals
         write(nunit,2060)jwall
         write(nunit,2061)(kwmat(i,jwall),i=1,nosegsxz(jwall))
23024 continue
 2060 format(1x,"kwmat(1,",i1,")= ")
 2061 format(7(1x,1a8,1x))

c.....kzone arrays
      do 23026 j=1,nptshb-1
         write(nunit,2070)j
         write(nunit,2071)(kzone1(i,j),i=1,nptsvb-1)
23026 continue
      do 23028 j=1,nptshb-1
         write(nunit,2072)j
         write(nunit,2071)(kzone2(i,j),i=1,nptsvb-1)
23028 continue
 2070 format(1x,'kzone1(1,',i3,')=')
 2071 format(20(1x,i2))
 2072 format(1x,'kzone2(1,',i3,')=')

c.....plasma zone boundaries
      write(nunit,2080)
      write(nunit,2081)(lboun1(i),i=1,nohbs)
      write(nunit,2082)
      write(nunit,2081)(lboun2(i),i=1,novbs)
 2080 format(1x,"lboun1=")
 2081 format(24(1x,i2))
 2082 format(1x,"lboun2=")

c.....electron temperature
      do 23030 i=1,novzs
         write(nunit,2090)i,(tehvt(k,i,1),k=1,min0(6,nohzs))
         do 23032 j=7,nohzs,6
            write(nunit,2091)(tehvt(k,i,1),k=j,min0(j+5,nohzs))
23032    continue
23030 continue
 2090 format(" tehvt(1,",i2,",1)=",1p6e10.3)
 2091 format(15x,1p6e10.3)

c.....ion temperature
      do 23034 i=1,novzs
         write(nunit,2100)i,(tihvt(k,i,1,1),k=1,min0(6,nohzs))
         do 23036 j=7,nohzs,6
            write(nunit,2101)(tihvt(k,i,1,1),k=j,min0(j+5,nohzs))
23036    continue
23034 continue
 2100 format(" tihvt(1,",i2,",1,1)=",1p6e10.3)
 2101 format(17x,1p6e10.3)

c.....ion flow velocity
      do 23038 i=1,novzs
         write(nunit,2102)i,(vflowx(k,i,1),k=1,min0(6,nohzs))
         do 23040 j=7,nohzs,6
            write(nunit,2103)(vflowx(k,i,1),k=j,min0(j+5,nohzs))
23040    continue
23038 continue
 2102 format(" vflowx(1,",i2,",1)= ",1p6e10.3)
 2103 format(17x,1p6e10.3)
      do 23042 i=1,novzs
         write(nunit,2104)i,(vflowy(k,i,1),k=1,min0(6,nohzs))
         do 23044 j=7,nohzs,6
            write(nunit,2105)(vflowy(k,i,1),k=j,min0(j+5,nohzs))
23044    continue
23042 continue
 2104 format(" vflowy(1,",i2,",1)= ",1p6e10.3)
 2105 format(17x,1p6e10.3)
      do 23046 i=1,novzs
         write(nunit,2106)i,(vflowz(k,i,1),k=1,min0(6,nohzs))
         do 23048 j=7,nohzs,6
            write(nunit,2107)(vflowz(k,i,1),k=j,min0(j+5,nohzs))
23048    continue
23046 continue
 2106 format(" vflowz(1,",i2,",1)= ",1p6e10.3)
 2107 format(17x,1p6e10.3)

c.....wall temperature
      do 23050 jwall=1,nowals
         write(nunit,2110)jwall
         write(nunit,2111)(twall(i,1,jwall),i=1,nosegsxz(jwall))
23050 continue
 2110 format(1x,"twall(1,1,",i1,")=")
 2111 format(5(1x,f10.2))

c.....wall node coordinates
      do 23052 jwall=1,nowals
         write(nunit,2120)jwall
         write(nunit,2121)(xwall(i,jwall),i=1,nosegsxz(jwall)+1)
         write(nunit,2122)jwall
         write(nunit,2121)(zwall(i,jwall),i=1,nosegsxz(jwall)+1)
23052 continue
 2120 format(1x,'xwall(1,',i1,')=')
 2121 format(5(1x,f10.2))
 2122 format(1x,'zwall(1,',i1,')=')

c
      write(nunit,3000)endmark
 3000 format(1a8)

      close(nunit)

      call remark("***** Wrote DEGAS input file degas.in *****")

      return
      end

c----------------------------------------------------------------------c

