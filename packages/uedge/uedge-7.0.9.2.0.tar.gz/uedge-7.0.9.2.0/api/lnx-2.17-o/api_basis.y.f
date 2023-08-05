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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/api_basis.d
c     ./api_basis.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































      subroutine apiinit0
cProlog
c initializes a Package
      integer drtdm
      common /apirtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("api")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call apidata
      call apiwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data apiiyiyi
c Replace pointer statements with Address types


c Group Dim_vars
      integer nx, ny, nzspt
      common /api00/ nx, ny, nzspt
c End of Dim_vars

c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2

c Group Normalization_constants
      double precision crni, ctemp
      common /api23/ crni, ctemp
c End of Normalization_constants

c Group Impfcn
c End of Impfcn

c Group Impurity_transport
      double precision dnimp, csexpn
      integer methimp
      common /api40/ methimp
      common /api43/ dnimp, csexpn
c End of Impurity_transport

c Group Impurity_source
      integer*8 psimpfix
      common /api56/ psimpfix
c End of Impurity_source

c Group Sources_at_walls
      integer nzsor
      integer*8 piszsorlb
      integer*8 pjxzsori
      integer*8 pjxzsoro
      integer*8 pixzbegi
      integer*8 pixzendi
      integer*8 pixzbego
      integer*8 pixzendo
      integer*8 pximpi
      integer*8 pximpo
      integer*8 pwimpi
      integer*8 pwimpo
      integer*8 pimpsori
      integer*8 pimpsoro
      common /api60/ nzsor
      common /api66/ piszsorlb, pjxzsori, pjxzsoro
      common /api66/ pixzbegi, pixzendi, pixzbego
      common /api66/ pixzendo, pximpi, pximpo
      common /api66/ pwimpi, pwimpo, pimpsori
      common /api66/ pimpsoro
c End of Sources_at_walls

c Group Input
      character*(256) inelrates(1)
      character*(256) inelrad(1)
      character*(256) inelmc(1)
      common /api10000/ inelrates
      common /api10001/ inelrad
      common /api10002/ inelmc
c End of Input

c Group Radiation
      double precision terad(40), xno(40), rntau(40)
      double precision radrate(40,40,40)
      double precision avgz(40,40,40)
      double precision avgz2(40,40,40)
      integer ncaset, ncaseno, ncasent
      common /api80/ ncaset, ncaseno, ncasent
      common /api83/ terad, xno, rntau, radrate, avgz, avgz2
c End of Radiation

c Group Impdata
      character*120 apidir
      common /api10003/ apidir
c End of Impdata

c Group MC_subs
c End of MC_subs

c Group Impurity_charge
      integer nnz
      integer*8 pzq
      common /api110/ nnz
      common /api116/ pzq
c End of Impurity_charge

c Group P93dat
      integer atn, atw, nt, nr, nn
      integer*8 ptdatm
      integer*8 prdatm
      integer*8 pndatm
      integer*8 pemdatm
      integer*8 pz1datm
      integer*8 pz2datm
      common /api120/ atn, atw, nt, nr, nn
      common /api126/ ptdatm, prdatm, pndatm
      common /api126/ pemdatm, pz1datm, pz2datm
c End of P93dat

c Group Imslwrk
      integer nxdata, nydata, nzdata, ldf, mdf, iflagi, nwork2, nwork3
      integer iworki(10), icont, kxords, kyords, kzords
      integer*8 pxdata
      integer*8 pydata
      integer*8 pzdata
      integer*8 pfdata
      integer*8 pwork2
      integer*8 pwork3
      integer*8 pxknots
      integer*8 pyknots
      integer*8 pzknots
      integer*8 pemcoef
      integer*8 pz1coef
      integer*8 pz2coef
      common /api130/ nxdata, nydata, nzdata, ldf, mdf, iflagi, nwork2
      common /api130/ nwork3, iworki, icont, kxords, kyords, kzords
      common /api136/ pxdata, pydata, pzdata
      common /api136/ pfdata, pwork2, pwork3
      common /api136/ pxknots, pyknots, pzknots
      common /api136/ pemcoef, pz1coef, pz2coef
c End of Imslwrk

c Group P93fcn
c End of P93fcn

c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

c Group Reduced_ion_variables
      double precision capm(3*5*3*5)
      double precision capn(3*5*3*5), caplam(3*5)
      double precision fmomenta(390), denz(5*26)
      double precision denmass(5*(26+1)), ela(3*3*5)
      double precision elab(3*5*3*5), mntau(5*5)
      double precision usol(3*26*5), sbar(3*6)
      double precision zi(5*26)
      common /api163/ capm, capn, caplam, fmomenta, denz, denmass, ela
      common /api163/ elab, mntau, usol, sbar, zi
c End of Reduced_ion_variables

c Group Cyield
      double precision ceth(7,12), cetf(7,12), cq(7,12), redf_haas
      integer ntars
      logical cidata(7,12)
      common /api170/ ntars
      common /api171/ cidata
      common /api173/ ceth, cetf, cq, redf_haas
c End of Cyield

c Group Sputt_subs
c End of Sputt_subs

c Group Emissivities
      integer ntemp, nlam, nden
      integer*8 petemp
      integer*8 plamb
      integer*8 peden
      integer*8 prate
      integer*8 pemiss
      common /api190/ ntemp, nlam, nden
      common /api196/ petemp, plamb, peden
      common /api196/ prate, pemiss
c End of Emissivities

c Group Pixels
      double precision rminpix, rmaxpix, zminpix, zmaxpix, drpix, dzpix
      integer nrpix, nzpix
      integer*8 pnpd
      integer*8 prp1
      integer*8 pzp1
      integer*8 prp2
      integer*8 pzp2
      integer*8 pwt
      common /api200/ nrpix, nzpix
      common /api203/ rminpix, rmaxpix, zminpix, zmaxpix, drpix, dzpix
      common /api206/ pnpd, prp1, pzp1, prp2
      common /api206/ pzp2, pwt
c End of Pixels


      data ev2/1.6022d-19/,qe2/1.6022d-19/
      data dnimp/1.d0/,methimp/33/,csexpn/0.d0/
      data nzsor/0/
      data inelrates/'edgrat.dat'/,inelrad/'carbavg.dat'/
      data inelmc/'carbmc.dat'/
      data ncaset/40/,ncaseno/40/,ncasent/40/
      data apidir/"."/
      data nnz/2/
      data icont/0/,kxords/4/,kyords/4/,kzords/4/
      data redf_haas/0.2d0/

      end
c restore definition from mppl.BASIS

      subroutine apidata
cProlog

c Group Dim_vars
      integer nx, ny, nzspt
      common /api00/ nx, ny, nzspt
c End of Dim_vars

c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2

c Group Normalization_constants
      double precision crni, ctemp
      common /api23/ crni, ctemp
c End of Normalization_constants

c Group Impfcn
c End of Impfcn

c Group Impurity_transport
      double precision dnimp, csexpn
      integer methimp
      common /api40/ methimp
      common /api43/ dnimp, csexpn
c End of Impurity_transport

c Group Impurity_source
      double precision simpfix ( nx,ny)
      pointer(psimpfix,simpfix)
      common /api56/ psimpfix
c End of Impurity_source

c Group Sources_at_walls
      integer nzsor
      integer iszsorlb ( nzspt,nzsor)
      pointer(piszsorlb,iszsorlb)
      integer jxzsori ( nzspt,nzsor)
      pointer(pjxzsori,jxzsori)
      integer jxzsoro ( nzspt,nzsor)
      pointer(pjxzsoro,jxzsoro)
      integer ixzbegi ( nzspt,nzsor)
      pointer(pixzbegi,ixzbegi)
      integer ixzendi ( nzspt,nzsor)
      pointer(pixzendi,ixzendi)
      integer ixzbego ( nzspt,nzsor)
      pointer(pixzbego,ixzbego)
      integer ixzendo ( nzspt,nzsor)
      pointer(pixzendo,ixzendo)
      double precision ximpi ( nzspt,nzsor)
      pointer(pximpi,ximpi)
      double precision ximpo ( nzspt,nzsor)
      pointer(pximpo,ximpo)
      double precision wimpi ( nzspt,nzsor)
      pointer(pwimpi,wimpi)
      double precision wimpo ( nzspt,nzsor)
      pointer(pwimpo,wimpo)
      double precision impsori ( nzspt,nzsor)
      pointer(pimpsori,impsori)
      double precision impsoro ( nzspt,nzsor)
      pointer(pimpsoro,impsoro)
      common /api60/ nzsor
      common /api66/ piszsorlb, pjxzsori, pjxzsoro
      common /api66/ pixzbegi, pixzendi, pixzbego
      common /api66/ pixzendo, pximpi, pximpo
      common /api66/ pwimpi, pwimpo, pimpsori
      common /api66/ pimpsoro
c End of Sources_at_walls

c Group Input
      character*(256) inelrates(1)
      character*(256) inelrad(1)
      character*(256) inelmc(1)
      common /api10000/ inelrates
      common /api10001/ inelrad
      common /api10002/ inelmc
c End of Input

c Group Radiation
      double precision terad(40), xno(40), rntau(40)
      double precision radrate(40,40,40)
      double precision avgz(40,40,40)
      double precision avgz2(40,40,40)
      integer ncaset, ncaseno, ncasent
      common /api80/ ncaset, ncaseno, ncasent
      common /api83/ terad, xno, rntau, radrate, avgz, avgz2
c End of Radiation

c Group Impdata
      character*120 apidir
      common /api10003/ apidir
c End of Impdata

c Group MC_subs
c End of MC_subs

c Group Impurity_charge
      integer nnz
      double precision zq ( nnz)
      pointer(pzq,zq)
      common /api110/ nnz
      common /api116/ pzq
c End of Impurity_charge

c Group P93dat
      integer atn, atw, nt, nr, nn
      double precision tdatm ( nt,nr,nn)
      pointer(ptdatm,tdatm)
      double precision rdatm ( nt,nr,nn)
      pointer(prdatm,rdatm)
      double precision ndatm ( nt,nr,nn)
      pointer(pndatm,ndatm)
      double precision emdatm ( nt,nr,nn)
      pointer(pemdatm,emdatm)
      double precision z1datm ( nt,nr,nn)
      pointer(pz1datm,z1datm)
      double precision z2datm ( nt,nr,nn)
      pointer(pz2datm,z2datm)
      common /api120/ atn, atw, nt, nr, nn
      common /api126/ ptdatm, prdatm, pndatm
      common /api126/ pemdatm, pz1datm, pz2datm
c End of P93dat

c Group Imslwrk
      integer nxdata, nydata, nzdata, ldf, mdf, iflagi, nwork2, nwork3
      integer iworki(10), icont, kxords, kyords, kzords
      double precision xdata ( 1:nxdata)
      pointer(pxdata,xdata)
      double precision ydata ( 1:nydata)
      pointer(pydata,ydata)
      double precision zdata ( 1:nzdata)
      pointer(pzdata,zdata)
      double precision fdata ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pfdata,fdata)
      double precision work2 ( nwork2)
      pointer(pwork2,work2)
      double precision work3 ( nwork3)
      pointer(pwork3,work3)
      double precision xknots ( 1:nxdata+kxords)
      pointer(pxknots,xknots)
      double precision yknots ( 1:nydata+kyords)
      pointer(pyknots,yknots)
      double precision zknots ( 1:nzdata+kzords)
      pointer(pzknots,zknots)
      double precision emcoef ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pemcoef,emcoef)
      double precision z1coef ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pz1coef,z1coef)
      double precision z2coef ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pz2coef,z2coef)
      common /api130/ nxdata, nydata, nzdata, ldf, mdf, iflagi, nwork2
      common /api130/ nwork3, iworki, icont, kxords, kyords, kzords
      common /api136/ pxdata, pydata, pzdata
      common /api136/ pfdata, pwork2, pwork3
      common /api136/ pxknots, pyknots, pzknots
      common /api136/ pemcoef, pz1coef, pz2coef
c End of Imslwrk

c Group P93fcn
c End of P93fcn

c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

c Group Reduced_ion_variables
      double precision capm(3*5*3*5)
      double precision capn(3*5*3*5), caplam(3*5)
      double precision fmomenta(390), denz(5*26)
      double precision denmass(5*(26+1)), ela(3*3*5)
      double precision elab(3*5*3*5), mntau(5*5)
      double precision usol(3*26*5), sbar(3*6)
      double precision zi(5*26)
      common /api163/ capm, capn, caplam, fmomenta, denz, denmass, ela
      common /api163/ elab, mntau, usol, sbar, zi
c End of Reduced_ion_variables

c Group Cyield
      double precision ceth(7,12), cetf(7,12), cq(7,12), redf_haas
      integer ntars
      logical cidata(7,12)
      common /api170/ ntars
      common /api171/ cidata
      common /api173/ ceth, cetf, cq, redf_haas
c End of Cyield

c Group Sputt_subs
c End of Sputt_subs

c Group Emissivities
      integer ntemp, nlam, nden
      double precision etemp ( ntemp)
      pointer(petemp,etemp)
      double precision lamb ( nlam)
      pointer(plamb,lamb)
      double precision eden ( nden)
      pointer(peden,eden)
      double precision rate ( nlam,ntemp,nden)
      pointer(prate,rate)
      double precision emiss ( nlam,0:nx+1,0:ny+1)
      pointer(pemiss,emiss)
      common /api190/ ntemp, nlam, nden
      common /api196/ petemp, plamb, peden
      common /api196/ prate, pemiss
c End of Emissivities

c Group Pixels
      double precision rminpix, rmaxpix, zminpix, zmaxpix, drpix, dzpix
      integer nrpix, nzpix
      integer npd ( nrpix,nzpix)
      pointer(pnpd,npd)
      double precision rp1 ( nrpix,nzpix)
      pointer(prp1,rp1)
      double precision zp1 ( nrpix,nzpix)
      pointer(pzp1,zp1)
      double precision rp2 ( nrpix,nzpix)
      pointer(prp2,rp2)
      double precision zp2 ( nrpix,nzpix)
      pointer(pzp2,zp2)
      double precision wt ( nrpix,nzpix)
      pointer(pwt,wt)
      common /api200/ nrpix, nzpix
      common /api203/ rminpix, rmaxpix, zminpix, zmaxpix, drpix, dzpix
      common /api206/ pnpd, prp1, pzp1, prp2
      common /api206/ pzp2, pwt
c End of Pixels


      external apiiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(psimpfix)
      call clraddr(piszsorlb)
      call clraddr(pjxzsori)
      call clraddr(pjxzsoro)
      call clraddr(pixzbegi)
      call clraddr(pixzendi)
      call clraddr(pixzbego)
      call clraddr(pixzendo)
      call clraddr(pximpi)
      call clraddr(pximpo)
      call clraddr(pwimpi)
      call clraddr(pwimpo)
      call clraddr(pimpsori)
      call clraddr(pimpsoro)
      call clraddr(pzq)
      call clraddr(ptdatm)
      call clraddr(prdatm)
      call clraddr(pndatm)
      call clraddr(pemdatm)
      call clraddr(pz1datm)
      call clraddr(pz2datm)
      call clraddr(pxdata)
      call clraddr(pydata)
      call clraddr(pzdata)
      call clraddr(pfdata)
      call clraddr(pwork2)
      call clraddr(pwork3)
      call clraddr(pxknots)
      call clraddr(pyknots)
      call clraddr(pzknots)
      call clraddr(pemcoef)
      call clraddr(pz1coef)
      call clraddr(pz2coef)
      call clraddr(petemp)
      call clraddr(plamb)
      call clraddr(peden)
      call clraddr(prate)
      call clraddr(pemiss)
      call clraddr(pnpd)
      call clraddr(prp1)
      call clraddr(pzp1)
      call clraddr(prp2)
      call clraddr(pzp2)
      call clraddr(pwt)

      return
      end
      subroutine apidbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,20,152)
      return
      end
      subroutine apiwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /apirtdm/ drtdm

c Group Dim_vars
      integer nx, ny, nzspt
      common /api00/ nx, ny, nzspt
c End of Dim_vars

c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2

c Group Normalization_constants
      double precision crni, ctemp
      common /api23/ crni, ctemp
c End of Normalization_constants

c Group Impfcn
c End of Impfcn

c Group Impurity_transport
      double precision dnimp, csexpn
      integer methimp
      common /api40/ methimp
      common /api43/ dnimp, csexpn
c End of Impurity_transport

c Group Impurity_source
      double precision simpfix ( nx,ny)
      pointer(psimpfix,simpfix)
      common /api56/ psimpfix
c End of Impurity_source

c Group Sources_at_walls
      integer nzsor
      integer iszsorlb ( nzspt,nzsor)
      pointer(piszsorlb,iszsorlb)
      integer jxzsori ( nzspt,nzsor)
      pointer(pjxzsori,jxzsori)
      integer jxzsoro ( nzspt,nzsor)
      pointer(pjxzsoro,jxzsoro)
      integer ixzbegi ( nzspt,nzsor)
      pointer(pixzbegi,ixzbegi)
      integer ixzendi ( nzspt,nzsor)
      pointer(pixzendi,ixzendi)
      integer ixzbego ( nzspt,nzsor)
      pointer(pixzbego,ixzbego)
      integer ixzendo ( nzspt,nzsor)
      pointer(pixzendo,ixzendo)
      double precision ximpi ( nzspt,nzsor)
      pointer(pximpi,ximpi)
      double precision ximpo ( nzspt,nzsor)
      pointer(pximpo,ximpo)
      double precision wimpi ( nzspt,nzsor)
      pointer(pwimpi,wimpi)
      double precision wimpo ( nzspt,nzsor)
      pointer(pwimpo,wimpo)
      double precision impsori ( nzspt,nzsor)
      pointer(pimpsori,impsori)
      double precision impsoro ( nzspt,nzsor)
      pointer(pimpsoro,impsoro)
      common /api60/ nzsor
      common /api66/ piszsorlb, pjxzsori, pjxzsoro
      common /api66/ pixzbegi, pixzendi, pixzbego
      common /api66/ pixzendo, pximpi, pximpo
      common /api66/ pwimpi, pwimpo, pimpsori
      common /api66/ pimpsoro
c End of Sources_at_walls

c Group Input
      character*(256) inelrates(1)
      character*(256) inelrad(1)
      character*(256) inelmc(1)
      common /api10000/ inelrates
      common /api10001/ inelrad
      common /api10002/ inelmc
c End of Input

c Group Radiation
      double precision terad(40), xno(40), rntau(40)
      double precision radrate(40,40,40)
      double precision avgz(40,40,40)
      double precision avgz2(40,40,40)
      integer ncaset, ncaseno, ncasent
      common /api80/ ncaset, ncaseno, ncasent
      common /api83/ terad, xno, rntau, radrate, avgz, avgz2
c End of Radiation

c Group Impdata
      character*120 apidir
      common /api10003/ apidir
c End of Impdata

c Group MC_subs
c End of MC_subs

c Group Impurity_charge
      integer nnz
      double precision zq ( nnz)
      pointer(pzq,zq)
      common /api110/ nnz
      common /api116/ pzq
c End of Impurity_charge

c Group P93dat
      integer atn, atw, nt, nr, nn
      double precision tdatm ( nt,nr,nn)
      pointer(ptdatm,tdatm)
      double precision rdatm ( nt,nr,nn)
      pointer(prdatm,rdatm)
      double precision ndatm ( nt,nr,nn)
      pointer(pndatm,ndatm)
      double precision emdatm ( nt,nr,nn)
      pointer(pemdatm,emdatm)
      double precision z1datm ( nt,nr,nn)
      pointer(pz1datm,z1datm)
      double precision z2datm ( nt,nr,nn)
      pointer(pz2datm,z2datm)
      common /api120/ atn, atw, nt, nr, nn
      common /api126/ ptdatm, prdatm, pndatm
      common /api126/ pemdatm, pz1datm, pz2datm
c End of P93dat

c Group Imslwrk
      integer nxdata, nydata, nzdata, ldf, mdf, iflagi, nwork2, nwork3
      integer iworki(10), icont, kxords, kyords, kzords
      double precision xdata ( 1:nxdata)
      pointer(pxdata,xdata)
      double precision ydata ( 1:nydata)
      pointer(pydata,ydata)
      double precision zdata ( 1:nzdata)
      pointer(pzdata,zdata)
      double precision fdata ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pfdata,fdata)
      double precision work2 ( nwork2)
      pointer(pwork2,work2)
      double precision work3 ( nwork3)
      pointer(pwork3,work3)
      double precision xknots ( 1:nxdata+kxords)
      pointer(pxknots,xknots)
      double precision yknots ( 1:nydata+kyords)
      pointer(pyknots,yknots)
      double precision zknots ( 1:nzdata+kzords)
      pointer(pzknots,zknots)
      double precision emcoef ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pemcoef,emcoef)
      double precision z1coef ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pz1coef,z1coef)
      double precision z2coef ( 1:nxdata,1:nydata,1:nzdata)
      pointer(pz2coef,z2coef)
      common /api130/ nxdata, nydata, nzdata, ldf, mdf, iflagi, nwork2
      common /api130/ nwork3, iworki, icont, kxords, kyords, kzords
      common /api136/ pxdata, pydata, pzdata
      common /api136/ pfdata, pwork2, pwork3
      common /api136/ pxknots, pyknots, pzknots
      common /api136/ pemcoef, pz1coef, pz2coef
c End of Imslwrk

c Group P93fcn
c End of P93fcn

c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

c Group Reduced_ion_variables
      double precision capm(3*5*3*5)
      double precision capn(3*5*3*5), caplam(3*5)
      double precision fmomenta(390), denz(5*26)
      double precision denmass(5*(26+1)), ela(3*3*5)
      double precision elab(3*5*3*5), mntau(5*5)
      double precision usol(3*26*5), sbar(3*6)
      double precision zi(5*26)
      common /api163/ capm, capn, caplam, fmomenta, denz, denmass, ela
      common /api163/ elab, mntau, usol, sbar, zi
c End of Reduced_ion_variables

c Group Cyield
      double precision ceth(7,12), cetf(7,12), cq(7,12), redf_haas
      integer ntars
      logical cidata(7,12)
      common /api170/ ntars
      common /api171/ cidata
      common /api173/ ceth, cetf, cq, redf_haas
c End of Cyield

c Group Sputt_subs
c End of Sputt_subs

c Group Emissivities
      integer ntemp, nlam, nden
      double precision etemp ( ntemp)
      pointer(petemp,etemp)
      double precision lamb ( nlam)
      pointer(plamb,lamb)
      double precision eden ( nden)
      pointer(peden,eden)
      double precision rate ( nlam,ntemp,nden)
      pointer(prate,rate)
      double precision emiss ( nlam,0:nx+1,0:ny+1)
      pointer(pemiss,emiss)
      common /api190/ ntemp, nlam, nden
      common /api196/ petemp, plamb, peden
      common /api196/ prate, pemiss
c End of Emissivities

c Group Pixels
      double precision rminpix, rmaxpix, zminpix, zmaxpix, drpix, dzpix
      integer nrpix, nzpix
      integer npd ( nrpix,nzpix)
      pointer(pnpd,npd)
      double precision rp1 ( nrpix,nzpix)
      pointer(prp1,rp1)
      double precision zp1 ( nrpix,nzpix)
      pointer(pzp1,zp1)
      double precision rp2 ( nrpix,nzpix)
      pointer(prp2,rp2)
      double precision zp2 ( nrpix,nzpix)
      pointer(pzp2,zp2)
      double precision wt ( nrpix,nzpix)
      pointer(pwt,wt)
      common /api200/ nrpix, nzpix
      common /api203/ rminpix, rmaxpix, zminpix, zmaxpix, drpix, dzpix
      common /api206/ pnpd, prp1, pzp1, prp2
      common /api206/ pzp2, pwt
c End of Pixels



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call apidbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Physical_constants2")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ev2",varadr(ev2),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"qe2",varadr(qe2),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Normalization_constants")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"crni",varadr(crni),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ctemp",varadr(ctemp),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Impfcn")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "getatau",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nx:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ny:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'uu:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'gx:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ixpt1:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ixpt2:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iysptrx:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'atau:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'tau1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'tau2:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "getprad",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nx:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ny:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ngsp:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ng:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'afrac:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'atau:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'prad:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'na:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ntau:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nratio:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Impurity_transport")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dnimp",varadr(dnimp),0,'double precision',
     &   'scalar', "m**2/s")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"methimp",varadr(methimp),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"csexpn",varadr(csexpn),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Impurity_source")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( psimpfix )
      i0001234=rtvare(drtdm,"simpfix",i000addr,1,'double precision',
     &   '(nx,ny)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Sources_at_walls")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzsor",varadr(nzsor),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piszsorlb )
      i0001234=rtvare(drtdm,"iszsorlb",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,1)
      i000addr = varadr ( pjxzsori )
      i0001234=rtvare(drtdm,"jxzsori",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,1)
      i000addr = varadr ( pjxzsoro )
      i0001234=rtvare(drtdm,"jxzsoro",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,1)
      i000addr = varadr ( pixzbegi )
      i0001234=rtvare(drtdm,"ixzbegi",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixzendi )
      i0001234=rtvare(drtdm,"ixzendi",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixzbego )
      i0001234=rtvare(drtdm,"ixzbego",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixzendo )
      i0001234=rtvare(drtdm,"ixzendo",i000addr,1,'integer',
     &   '(nzspt,nzsor)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pximpi )
      i0001234=rtvare(drtdm,"ximpi",i000addr,1,'double precision',
     &   '(nzspt,nzsor)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pximpo )
      i0001234=rtvare(drtdm,"ximpo",i000addr,1,'double precision',
     &   '(nzspt,nzsor)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwimpi )
      i0001234=rtvare(drtdm,"wimpi",i000addr,1,'double precision',
     &   '(nzspt,nzsor)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwimpo )
      i0001234=rtvare(drtdm,"wimpo",i000addr,1,'double precision',
     &   '(nzspt,nzsor)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pimpsori )
      i0001234=rtvare(drtdm,"impsori",i000addr,1,'double precision',
     &   '(nzspt,nzsor)', "Amp")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pimpsoro )
      i0001234=rtvare(drtdm,"impsoro",i000addr,1,'double precision',
     &   '(nzspt,nzsor)', "Amp")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Input")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( inelrates )
      i0001234=rtvare(drtdm,"inelrates",i000addr,0,'character*(256)',
     &   '(1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( inelrad )
      i0001234=rtvare(drtdm,"inelrad",i000addr,0,'character*(256)','(1)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( inelmc )
      i0001234=rtvare(drtdm,"inelmc",i000addr,0,'character*(256)','(1)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Radiation")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncaset",varadr(ncaset),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncaseno",varadr(ncaseno),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncasent",varadr(ncasent),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( terad )
      i0001234=rtvare(drtdm,"terad",i000addr,0,'double precision','(40)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( xno )
      i0001234=rtvare(drtdm,"xno",i000addr,0,'double precision','(40)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( rntau )
      i0001234=rtvare(drtdm,"rntau",i000addr,0,'double precision','(40)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( radrate )
      i0001234=rtvare(drtdm,"radrate",i000addr,0,'double precision',
     &   '(40,40,40)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( avgz )
      i0001234=rtvare(drtdm,"avgz",i000addr,0,'double precision',
     &   '(40,40,40)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( avgz2 )
      i0001234=rtvare(drtdm,"avgz2",i000addr,0,'double precision',
     &   '(40,40,40)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Impdata")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"apidir",varadr(apidir),0,'character*120',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"MC_subs")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readmc",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nzdf:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'mcfilename:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_mcfilename_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "mcrates",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ti:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'za:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'zamax:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'zn:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rion:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rrec:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rcxr:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "radmc",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nz:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'znuc:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'dene:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'denz:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'radz:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rcxr_zn6",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'tmp:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'za:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Impurity_charge")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nnz",varadr(nnz),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzq )
      i0001234=rtvare(drtdm,"zq",i000addr,1,'double precision','(nnz)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"P93dat")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"atn",varadr(atn),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"atw",varadr(atw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nt",varadr(nt),0,'integer','scalar', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nr",varadr(nr),0,'integer','scalar', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nn",varadr(nn),0,'integer','scalar', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptdatm )
      i0001234=rtvare(drtdm,"tdatm",i000addr,1,'double precision',
     &   '(nt,nr,nn)', "J")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prdatm )
      i0001234=rtvare(drtdm,"rdatm",i000addr,1,'double precision',
     &   '(nt,nr,nn)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pndatm )
      i0001234=rtvare(drtdm,"ndatm",i000addr,1,'double precision',
     &   '(nt,nr,nn)', "sec/m**3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pemdatm )
      i0001234=rtvare(drtdm,"emdatm",i000addr,1,'double precision',
     &   '(nt,nr,nn)', "Watts-m**3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pz1datm )
      i0001234=rtvare(drtdm,"z1datm",i000addr,1,'double precision',
     &   '(nt,nr,nn)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pz2datm )
      i0001234=rtvare(drtdm,"z2datm",i000addr,1,'double precision',
     &   '(nt,nr,nn)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Imslwrk")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxdata",varadr(nxdata),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nydata",varadr(nydata),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzdata",varadr(nzdata),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxdata )
      i0001234=rtvare(drtdm,"xdata",i000addr,1,'double precision',
     &   '(1:nxdata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pydata )
      i0001234=rtvare(drtdm,"ydata",i000addr,1,'double precision',
     &   '(1:nydata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzdata )
      i0001234=rtvare(drtdm,"zdata",i000addr,1,'double precision',
     &   '(1:nzdata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfdata )
      i0001234=rtvare(drtdm,"fdata",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata,1:nzdata)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ldf",varadr(ldf),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mdf",varadr(mdf),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iflagi",varadr(iflagi),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nwork2",varadr(nwork2),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwork2 )
      i0001234=rtvare(drtdm,"work2",i000addr,1,'double precision',
     &   '(nwork2)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nwork3",varadr(nwork3),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwork3 )
      i0001234=rtvare(drtdm,"work3",i000addr,1,'double precision',
     &   '(nwork3)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( iworki )
      i0001234=rtvare(drtdm,"iworki",i000addr,0,'integer','(10)', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"icont",varadr(icont),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kxords",varadr(kxords),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kyords",varadr(kyords),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kzords",varadr(kzords),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxknots )
      i0001234=rtvare(drtdm,"xknots",i000addr,1,'double precision',
     &   '(1:nxdata+kxords)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyknots )
      i0001234=rtvare(drtdm,"yknots",i000addr,1,'double precision',
     &   '(1:nydata+kyords)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzknots )
      i0001234=rtvare(drtdm,"zknots",i000addr,1,'double precision',
     &   '(1:nzdata+kzords)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pemcoef )
      i0001234=rtvare(drtdm,"emcoef",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata,1:nzdata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pz1coef )
      i0001234=rtvare(drtdm,"z1coef",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata,1:nzdata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pz2coef )
      i0001234=rtvare(drtdm,"z2coef",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata,1:nzdata)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"P93fcn")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readpost",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "splinem",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "emissbs",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nratio:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ntau:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "z1avgbs",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nratio:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ntau:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "z2avgbs",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nratio:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ntau:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Reduced_ion_constants")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"coulom",varadr(coulom),0,'double precision'
     &   ,'scalar', "coulomb")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"epsilo",varadr(epsilo),0,'double precision'
     &   ,'scalar', "farad/m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"promas",varadr(promas),0,'double precision'
     &   ,'scalar', "kg")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xj7kv",varadr(xj7kv),0,'double precision',
     &   'scalar', "J/keV")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"one",varadr(one),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"pi0",varadr(pi0),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zero",varadr(zero),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sumforce",varadr(sumforce),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"totmass",varadr(totmass),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"anorm",varadr(anorm),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"acci",varadr(acci),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"acci0",varadr(acci0),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( al32 )
      i0001234=rtvare(drtdm,"al32",i000addr,0,'double precision','(3)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"miso",varadr(miso),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzch",varadr(nzch),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mise",varadr(mise),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ilam1",varadr(ilam1),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ilam2",varadr(ilam2),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ilam3",varadr(ilam3),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iacci",varadr(iacci),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iforc",varadr(iforc),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( natom )
      i0001234=rtvare(drtdm,"natom",i000addr,0,'integer','(5)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Reduced_ion_variables")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( capm )
      i0001234=rtvare(drtdm,"capm",i000addr,0,'double precision',
     &   '(3*5*3*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( capn )
      i0001234=rtvare(drtdm,"capn",i000addr,0,'double precision',
     &   '(3*5*3*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( caplam )
      i0001234=rtvare(drtdm,"caplam",i000addr,0,'double precision',
     &   '(3*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( fmomenta )
      i0001234=rtvare(drtdm,"fmomenta",i000addr,0,'double precision',
     &   '(390)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( denz )
      i0001234=rtvare(drtdm,"denz",i000addr,0,'double precision',
     &   '(5*26)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( denmass )
      i0001234=rtvare(drtdm,"denmass",i000addr,0,'double precision',
     &   '(5*(26+1))', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ela )
      i0001234=rtvare(drtdm,"ela",i000addr,0,'double precision',
     &   '(3*3*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( elab )
      i0001234=rtvare(drtdm,"elab",i000addr,0,'double precision',
     &   '(3*5*3*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( mntau )
      i0001234=rtvare(drtdm,"mntau",i000addr,0,'double precision',
     &   '(5*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( usol )
      i0001234=rtvare(drtdm,"usol",i000addr,0,'double precision',
     &   '(3*26*5)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( sbar )
      i0001234=rtvare(drtdm,"sbar",i000addr,0,'double precision','(3*6)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( zi )
      i0001234=rtvare(drtdm,"zi",i000addr,0,'double precision','(5*26)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Cyield")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( ceth )
      i0001234=rtvare(drtdm,"ceth",i000addr,0,'double precision',
     &   '(7,12)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( cetf )
      i0001234=rtvare(drtdm,"cetf",i000addr,0,'double precision',
     &   '(7,12)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( cq )
      i0001234=rtvare(drtdm,"cq",i000addr,0,'double precision','(7,12)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntars",varadr(ntars),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( cidata )
      i0001234=rtvare(drtdm,"cidata",i000addr,0,'logical','(7,12)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"redf_haas",varadr(redf_haas),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Sputt_subs")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "syld96",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'matt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'matp:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'cion:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'cizb:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'crmb:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "yld96",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'matt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'matp:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'energy:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "sputchem",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ioptchem:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ee0:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'temp:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'flux:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ychem:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Emissivities")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntemp",varadr(ntemp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nlam",varadr(nlam),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nden",varadr(nden),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( petemp )
      i0001234=rtvare(drtdm,"etemp",i000addr,1,'double precision',
     &   '(ntemp)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plamb )
      i0001234=rtvare(drtdm,"lamb",i000addr,1,'double precision',
     &   '(nlam)', "Angstrom")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( peden )
      i0001234=rtvare(drtdm,"eden",i000addr,1,'double precision',
     &   '(nden)', "m^-3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prate )
      i0001234=rtvare(drtdm,"rate",i000addr,1,'double precision',
     &   '(nlam,ntemp,nden)', "ph/s")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pemiss )
      i0001234=rtvare(drtdm,"emiss",i000addr,1,'double precision',
     &   '(nlam,0:nx+1,0:ny+1)', "ph/m^3/s")
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readrates",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'apidir:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_apidir_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'impfname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_impfname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "calcrates",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'density:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Pixels")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nrpix",varadr(nrpix),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzpix",varadr(nzpix),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnpd )
      i0001234=rtvare(drtdm,"npd",i000addr,1,'integer','(nrpix,nzpix)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( prp1 )
      i0001234=rtvare(drtdm,"rp1",i000addr,1,'double precision',
     &   '(nrpix,nzpix)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pzp1 )
      i0001234=rtvare(drtdm,"zp1",i000addr,1,'double precision',
     &   '(nrpix,nzpix)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( prp2 )
      i0001234=rtvare(drtdm,"rp2",i000addr,1,'double precision',
     &   '(nrpix,nzpix)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pzp2 )
      i0001234=rtvare(drtdm,"zp2",i000addr,1,'double precision',
     &   '(nrpix,nzpix)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pwt )
      i0001234=rtvare(drtdm,"wt",i000addr,1,'double precision',
     &   '(nrpix,nzpix)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i0001234=rtvare(drtdm,"rminpix",varadr(rminpix),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rmaxpix",varadr(rmaxpix),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zminpix",varadr(zminpix),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zmaxpix",varadr(zmaxpix),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"drpix",varadr(drpix),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dzpix",varadr(dzpix),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "lineintegral",jgrp,'double precision',
     &   "none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'arg:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rvertex:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'zvertex:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"api_basis.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine apixpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.3) then
         call apixp3(name1234)
      elseif (iseg.eq.10) then
         call apixp10(name1234)
      elseif (iseg.eq.14) then
         call apixp14(name1234)
      elseif (iseg.eq.18) then
         call apixp18(name1234)
      elseif (iseg.eq.19) then
         call apixp19(name1234)
      elseif (iseg.eq.20) then
         call apixp20(name1234)
      else
         call baderr('apixpf: impossible event')
      endif
      return
      end
      subroutine apixp3(name1234)
cProlog
      character*(*) name1234
      external api_handler
      external getatau
      external getprad
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'getatau') then
         call parexecf(api_handler, 0, getatau)
      elseif (name1234 .eq. 'getprad') then
         call parexecf(api_handler, 1, getprad)
      else
         call baderr('apixp3: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp10(name1234)
cProlog
      character*(*) name1234
      external api_handler
      external readmc
      external mcrates
      external radmc
      external rcxr_zn6
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'readmc') then
         call parexecf(api_handler, 2, readmc)
      elseif (name1234 .eq. 'mcrates') then
         call parexecf(api_handler, 3, mcrates)
      elseif (name1234 .eq. 'radmc') then
         call parexecf(api_handler, 4, radmc)
      elseif (name1234 .eq. 'rcxr_zn6') then
         call parexecf(api_handler, 5, rcxr_zn6)
      else
         call baderr('apixp10: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp14(name1234)
cProlog
      character*(*) name1234
      external api_handler
      external readpost
      external splinem
      external emissbs
      external z1avgbs
      external z2avgbs
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'readpost') then
         call parexecf(api_handler, 6, readpost)
      elseif (name1234 .eq. 'splinem') then
         call parexecf(api_handler, 7, splinem)
      elseif (name1234 .eq. 'emissbs') then
         call parexecf(api_handler, 8, emissbs)
      elseif (name1234 .eq. 'z1avgbs') then
         call parexecf(api_handler, 9, z1avgbs)
      elseif (name1234 .eq. 'z2avgbs') then
         call parexecf(api_handler, 10, z2avgbs)
      else
         call baderr('apixp14: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp18(name1234)
cProlog
      character*(*) name1234
      external api_handler
      external syld96
      external yld96
      external sputchem
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'syld96') then
         call parexecf(api_handler, 11, syld96)
      elseif (name1234 .eq. 'yld96') then
         call parexecf(api_handler, 12, yld96)
      elseif (name1234 .eq. 'sputchem') then
         call parexecf(api_handler, 13, sputchem)
      else
         call baderr('apixp18: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp19(name1234)
cProlog
      character*(*) name1234
      external api_handler
      external readrates
      external calcrates
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'readrates') then
         call parexecf(api_handler, 14, readrates)
      elseif (name1234 .eq. 'calcrates') then
         call parexecf(api_handler, 15, calcrates)
      else
         call baderr('apixp19: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp20(name1234)
cProlog
      character*(*) name1234
      external api_handler
      external lineintegral
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'lineintegral') then
         call parexecf(api_handler, 16, lineintegral)
      else
         call baderr('apixp20: impossible event: '//name5678)
      endif
      return
      end
      function apibfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer apibfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in api')
      call baderr(name1234)
      apibfcn = -1
      return
      end
