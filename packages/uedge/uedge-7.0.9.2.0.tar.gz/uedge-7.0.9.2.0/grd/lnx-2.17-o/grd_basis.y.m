      subroutine grdinit0
c initializes a Package
      integer drtdm
      common /grdrtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("grd")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call grddata
      call grdwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_grd],[
Use(Dim_vars)
Use(Dimensions)
Use(Analgrd)
Use(Torannulus)
Use(Magmirror)
Use(Curves)
Use(Linkco)
Use(Transfm)
Use(Spline)
Use(Argfc)
Use(Inmesh)
Use(Transit)
Use(System)
Use(UEgrid)
Use(Mmod)
Use(Refinex)
Use(Xmesh)
Use(Dnull_temp)
Use(Expseed)
Use(Xfcn)
Use(Driver)
])
      block data grdiyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_grd
      data nix/NIX/,mseg/MSEG/,nalpha/NALPHA/,nptmp/300/,nconst/0/
      data radm/-1.e-4/,radx/0.04/,rad0/0./,rscalcore/1./,za0/0./
      data zax/1./,zaxpt/.75/,tiltang/0./,ixsnog/1/,zxpt_reset/0./
      data alfyt/-2./,tnoty/0./,sratiopf/0./,alfxt/4.0/,isadjalfxt/0/
      data tctr/0./,bpolfix/.3/,btfix/5./,isgdistort/0/,agsindx/0./
      data agsrsp/0./,iynod/0/,rnod/0./,ixdstar/1/
      data acore/0.5/,rm0/2./,edgewid/0.1/,dthlim/1e-4/,bpol0/0.2/
      data btor0/2./,ibpmodel/0/
      data yextend/0./,dsmin/0./,alpha1/45.0/
      data ityp/0,0,0,1,1,2,1,1,2,0,0,0/,dxleft/0./,ndxleft/0/
      data nord/4/
      data isspnew/0/,istpnew/0/,istptest/2*0/,isztest/2*0/
      data epslon_lim/1.e-3/,dalpha/5./
      data istream/0/,isupstreamx/0/,iplate/0/,wtold/0.5/,nsmooth/2/
      data fuzzm/1.0e-08/,delmax/1.0e-08/,wtmesh1/0.5/,dmix0/0./
      data cwtffu/1./,cwtffd/1./,isxtform/1/,iswtform/0/,nxdff1/0/
      data nxdff2/0/
      data isrefxptn/1/,nxmod/2/,alfxptl/1./,alfxpt2l/1./,alfxptu/1./
      data alfxpt2u/1./,alfxpt/1./,alfxpt2/1./,nsmoothx/8/
      data ndat/NDAT/,kxmesh/1/,slpxt/1.0/,alfx/2*0.1/,ileft/0/
      data dleft/0.0/,iright/0/,dright/0.0/,kord/4/,ndatp2/NDATP2/
      data kntopt/1/
      data fraclplt/.6,.6/,alfxdiv/.18,.18/,alfxcore/.4,.4/
      data shift_seed_leg/0.,0./,shift_seed_core/1.,1./,nxlplt/12,12/
      data nxlxpt/4,4/,fcorenunif/0.8/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine grddata
Use_All_Groups_grd
      external grdiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(radf))
      call clraddr(Point(thpf))
      call clraddr(Point(zu))
      call clraddr(Point(ru))
      call clraddr(Point(bzu))
      call clraddr(Point(bru))
      call clraddr(Point(bmag))
      call clraddr(Point(xcurveg))
      call clraddr(Point(ycurveg))
      call clraddr(Point(npointg))
      call clraddr(Point(cmeshx))
      call clraddr(Point(cmeshy))
      call clraddr(Point(isegment))
      call clraddr(Point(isys))
      call clraddr(Point(alphasys))
      call clraddr(Point(ijump))
      call clraddr(Point(splcoef))
      call clraddr(Point(xknts))
      call clraddr(Point(ncap7))
      call clraddr(Point(xdatag))
      call clraddr(Point(ydatag))
      call clraddr(Point(sddata))
      call clraddr(Point(bkpt))
      call clraddr(Point(xconst))
      call clraddr(Point(yconst))
      call clraddr(Point(nderiv))
      call clraddr(Point(coeff))
      call clraddr(Point(wsla))
      call clraddr(Point(iwsla))
      call clraddr(Point(seedxp))
      call clraddr(Point(seedxpxl))
      call clraddr(Point(seed))
      call clraddr(Point(dissep))
      call clraddr(Point(distxp))
      call clraddr(Point(distxpxl))
      call clraddr(Point(x0g))
      call clraddr(Point(xlast))
      call clraddr(Point(y0g))
      call clraddr(Point(ylast))
      call clraddr(Point(xtrans))
      call clraddr(Point(ytrans))
      call clraddr(Point(wg))
      call clraddr(Point(istartg))
      call clraddr(Point(iendg))
      call clraddr(Point(m))
      call clraddr(Point(nseg))
      call clraddr(Point(xwork))
      call clraddr(Point(ywork))
      call clraddr(Point(istartc))
      call clraddr(Point(iendc))
      call clraddr(Point(cmeshx0))
      call clraddr(Point(cmeshy0))
      call clraddr(Point(dsc))
      call clraddr(Point(xcrv))
      call clraddr(Point(ycrv))
      call clraddr(Point(dsm))
      call clraddr(Point(dss))
      call clraddr(Point(dssleg))
      call clraddr(Point(dsmesh))
      call clraddr(Point(dsmesh0))
      call clraddr(Point(dsmesh1))
      call clraddr(Point(dsmesh2))
      call clraddr(Point(xmsh))
      call clraddr(Point(ymsh))
      call clraddr(Point(rtop1))
      call clraddr(Point(ztop1))
      call clraddr(Point(rtop2))
      call clraddr(Point(ztop2))
      call clraddr(Point(rupstream1))
      call clraddr(Point(zupstream1))
      call clraddr(Point(rupstream2))
      call clraddr(Point(zupstream2))
      call clraddr(Point(rdnstream1))
      call clraddr(Point(zdnstream1))
      call clraddr(Point(rdnstream2))
      call clraddr(Point(zdnstream2))
      call clraddr(Point(rplate1))
      call clraddr(Point(zplate1))
      call clraddr(Point(rplate2))
      call clraddr(Point(zplate2))
      call clraddr(Point(rtop))
      call clraddr(Point(ztop))
      call clraddr(Point(rtop0))
      call clraddr(Point(ztop0))
      call clraddr(Point(rbot))
      call clraddr(Point(zbot))
      call clraddr(Point(rupstream))
      call clraddr(Point(zupstream))
      call clraddr(Point(rdnstream))
      call clraddr(Point(zdnstream))
      call clraddr(Point(rplate))
      call clraddr(Point(zplate))
      call clraddr(Point(rplate0))
      call clraddr(Point(zplate0))
      call clraddr(Point(dsnorm))
      call clraddr(Point(wtm1))
      call clraddr(Point(cmeshx3))
      call clraddr(Point(cmeshy3))
      call clraddr(Point(rff1))
      call clraddr(Point(zff1))
      call clraddr(Point(rff2))
      call clraddr(Point(zff2))
      call clraddr(Point(rff))
      call clraddr(Point(zff))
      call clraddr(Point(dsmesh3))
      call clraddr(Point(dsmeshff))
      call clraddr(Point(rsu))
      call clraddr(Point(zsu))
      call clraddr(Point(rsx))
      call clraddr(Point(zsx))
      call clraddr(Point(rflux))
      call clraddr(Point(zflux))
      call clraddr(Point(dsflux))
      call clraddr(Point(rmm))
      call clraddr(Point(zmm))
      call clraddr(Point(xdat))
      call clraddr(Point(tdat))
      call clraddr(Point(tknt))
      call clraddr(Point(z1work))
      call clraddr(Point(z1cscoef))
      call clraddr(Point(wrk1))
      call clraddr(Point(rmb))
      call clraddr(Point(zmb))
      call clraddr(Point(rmu))
      call clraddr(Point(zmu))

      return
       end
      subroutine grddbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,20,340)
      return
       end
      subroutine grdwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /grdrtdm/ drtdm
Use_All_Groups_grd

      Address i000addr
      external varadr
      Address varadr


      call grddbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Dimensions")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"idim",varadr(idim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nix",varadr(nix),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mseg",varadr(mseg),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nalpha",varadr(nalpha),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nxuse )
      i0001234=rtvare(drtdm,"nxuse",i000addr,0,Quote(integer),
Quote((1:2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptmp",varadr(nptmp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndata",varadr(ndata),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nbkpt",varadr(nbkpt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nconst",varadr(nconst),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nwdim",varadr(nwdim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"niwdim",varadr(niwdim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Analgrd")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"radm",varadr(radm),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"radx",varadr(radx),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rad0",varadr(rad0),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rscalcore",varadr(rscalcore),0,Quote(double precision),
Quote(scalar), " ")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"za0",varadr(za0),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zax",varadr(zax),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zaxpt",varadr(zaxpt),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tiltang",varadr(tiltang),0,Quote(double precision),
Quote(scalar), "deg")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixsnog",varadr(ixsnog),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zxpt_reset",varadr(zxpt_reset),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfyt",varadr(alfyt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tnoty",varadr(tnoty),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sratiopf",varadr(sratiopf),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxt",varadr(alfxt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isadjalfxt",varadr(isadjalfxt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tctr",varadr(tctr),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"bpolfix",varadr(bpolfix),0,Quote(double precision),
Quote(scalar), "T")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"btfix",varadr(btfix),0,Quote(double precision),
Quote(scalar), "T")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isgdistort",varadr(isgdistort),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"agsindx",varadr(agsindx),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"agsrsp",varadr(agsrsp),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iynod",varadr(iynod),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rnod",varadr(rnod),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixdstar",varadr(ixdstar),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Torannulus")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"acore",varadr(acore),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rm0",varadr(rm0),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"edgewid",varadr(edgewid),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dthlim",varadr(dthlim),0,Quote(double precision),
Quote(scalar), "rad")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"bpol0",varadr(bpol0),0,Quote(double precision),
Quote(scalar), "T")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"btor0",varadr(btor0),0,Quote(double precision),
Quote(scalar), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(radf) )
      i0001234=rtvare(drtdm,"radf",i000addr,1,Quote(_double precision),
Quote((0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(thpf) )
      i0001234=rtvare(drtdm,"thpf",i000addr,1,Quote(_double precision),
Quote((1:nxm,0:4)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ibpmodel",varadr(ibpmodel),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Magmirror")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(zu) )
      i0001234=rtvare(drtdm,"zu",i000addr,1,Quote(_double precision),
Quote((1:nxm,1:nym,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ru) )
      i0001234=rtvare(drtdm,"ru",i000addr,1,Quote(_double precision),
Quote((1:nxm,1:nym,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bzu) )
      i0001234=rtvare(drtdm,"bzu",i000addr,1,Quote(_double precision),
Quote((1:nxm,1:nym,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bru) )
      i0001234=rtvare(drtdm,"bru",i000addr,1,Quote(_double precision),
Quote((1:nxm,1:nym,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bmag) )
      i0001234=rtvare(drtdm,"bmag",i000addr,1,Quote(_double precision),
Quote((1:nxm,1:nym,0:4)), "T")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzc",varadr(nzc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nrc",varadr(nrc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Curves")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(xcurveg) )
      i0001234=rtvare(drtdm,"xcurveg",i000addr,1,Quote(_double precision),
Quote((npts,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ycurveg) )
      i0001234=rtvare(drtdm,"ycurveg",i000addr,1,Quote(_double precision),
Quote((npts,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(npointg) )
      i0001234=rtvare(drtdm,"npointg",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xxpoint",varadr(xxpoint),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"yxpoint",varadr(yxpoint),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rtanpl",varadr(rtanpl),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ztanpl",varadr(ztanpl),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Linkco")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(cmeshx) )
      i0001234=rtvare(drtdm,"cmeshx",i000addr,1,Quote(_double precision),
Quote((idim,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(cmeshy) )
      i0001234=rtvare(drtdm,"cmeshy",i000addr,1,Quote(_double precision),
Quote((idim,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( ixpoint )
      i0001234=rtvare(drtdm,"ixpoint",i000addr,0,Quote(integer),
Quote((1:3,1:2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"yextend",varadr(yextend),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dsmin",varadr(dsmin),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dsminx",varadr(dsminx),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dyjump",varadr(dyjump),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alpha1",varadr(alpha1),0,Quote(double precision),
Quote(scalar), "degrees")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( ityp )
      i0001234=rtvare(drtdm,"ityp",i000addr,0,Quote(integer),
Quote((6,2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dxleft",varadr(dxleft),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndxleft",varadr(ndxleft),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Transfm")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(isegment) )
      i0001234=rtvare(drtdm,"isegment",i000addr,1,Quote(_integer),
Quote((npts,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(isys) )
      i0001234=rtvare(drtdm,"isys",i000addr,1,Quote(_integer),
Quote((mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(alphasys) )
      i0001234=rtvare(drtdm,"alphasys",i000addr,1,Quote(_double precision),
Quote((nalpha)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ijump) )
      i0001234=rtvare(drtdm,"ijump",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Spline")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(splcoef) )
      i0001234=rtvare(drtdm,"splcoef",i000addr,1,Quote(_double precision),
Quote((npts,mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xknts) )
      i0001234=rtvare(drtdm,"xknts",i000addr,1,Quote(_double precision),
Quote((npts,mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ncap7) )
      i0001234=rtvare(drtdm,"ncap7",i000addr,1,Quote(_integer),
Quote((mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Argfc")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(xdatag) )
      i0001234=rtvare(drtdm,"xdatag",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ydatag) )
      i0001234=rtvare(drtdm,"ydatag",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(sddata) )
      i0001234=rtvare(drtdm,"sddata",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nord",varadr(nord),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bkpt) )
      i0001234=rtvare(drtdm,"bkpt",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xconst) )
      i0001234=rtvare(drtdm,"xconst",i000addr,1,Quote(_double precision),
Quote((nconst)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yconst) )
      i0001234=rtvare(drtdm,"yconst",i000addr,1,Quote(_double precision),
Quote((nconst)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nderiv) )
      i0001234=rtvare(drtdm,"nderiv",i000addr,1,Quote(_integer),
Quote((nconst)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mode",varadr(mode),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(coeff) )
      i0001234=rtvare(drtdm,"coeff",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wsla) )
      i0001234=rtvare(drtdm,"wsla",i000addr,1,Quote(_double precision),
Quote((nwdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iwsla) )
      i0001234=rtvare(drtdm,"iwsla",i000addr,1,Quote(_integer),
Quote((niwdim)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Inmesh")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"isspnew",varadr(isspnew),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( rstrike )
      i0001234=rtvare(drtdm,"rstrike",i000addr,0,Quote(double precision),
Quote((1:2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( zstrike )
      i0001234=rtvare(drtdm,"zstrike",i000addr,0,Quote(double precision),
Quote((1:2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"istpnew",varadr(istpnew),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( rtpnew )
      i0001234=rtvare(drtdm,"rtpnew",i000addr,0,Quote(double precision),
Quote((1:2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( ztpnew )
      i0001234=rtvare(drtdm,"ztpnew",i000addr,0,Quote(double precision),
Quote((1:2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( istptest )
      i0001234=rtvare(drtdm,"istptest",i000addr,0,Quote(integer),
Quote((1:2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( ilmax )
      i0001234=rtvare(drtdm,"ilmax",i000addr,0,Quote(integer),
Quote((1:2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(seedxp) )
      i0001234=rtvare(drtdm,"seedxp",i000addr,1,Quote(_double precision),
Quote((idim,noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(seedxpxl) )
      i0001234=rtvare(drtdm,"seedxpxl",i000addr,1,Quote(_double precision),
Quote((idim,noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(seed) )
      i0001234=rtvare(drtdm,"seed",i000addr,1,Quote(_double precision),
Quote((idim,noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dissep) )
      i0001234=rtvare(drtdm,"dissep",i000addr,1,Quote(_double precision),
Quote((npts,noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(distxp) )
      i0001234=rtvare(drtdm,"distxp",i000addr,1,Quote(_double precision),
Quote((noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(distxpxl) )
      i0001234=rtvare(drtdm,"distxpxl",i000addr,1,Quote(_double precision),
Quote((noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(x0g) )
      i0001234=rtvare(drtdm,"x0g",i000addr,1,Quote(_double precision),
Quote((noregs)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xlast) )
      i0001234=rtvare(drtdm,"xlast",i000addr,1,Quote(_double precision),
Quote((noregs)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(y0g) )
      i0001234=rtvare(drtdm,"y0g",i000addr,1,Quote(_double precision),
Quote((noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ylast) )
      i0001234=rtvare(drtdm,"ylast",i000addr,1,Quote(_double precision),
Quote((noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( isztest )
      i0001234=rtvare(drtdm,"isztest",i000addr,0,Quote(integer),
Quote((1:2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"epslon_lim",varadr(epslon_lim),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dalpha",varadr(dalpha),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Transit")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(xtrans) )
      i0001234=rtvare(drtdm,"xtrans",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ytrans) )
      i0001234=rtvare(drtdm,"ytrans",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wg) )
      i0001234=rtvare(drtdm,"wg",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"System")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(istartg) )
      i0001234=rtvare(drtdm,"istartg",i000addr,1,Quote(_integer),
Quote((mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iendg) )
      i0001234=rtvare(drtdm,"iendg",i000addr,1,Quote(_integer),
Quote((mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(m) )
      i0001234=rtvare(drtdm,"m",i000addr,1,Quote(_integer),
Quote((mseg,jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nseg) )
      i0001234=rtvare(drtdm,"nseg",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( ixpointc )
      i0001234=rtvare(drtdm,"ixpointc",i000addr,0,Quote(integer),
Quote((1:3,1:2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xwork) )
      i0001234=rtvare(drtdm,"xwork",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ywork) )
      i0001234=rtvare(drtdm,"ywork",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(istartc) )
      i0001234=rtvare(drtdm,"istartc",i000addr,1,Quote(_integer),
Quote((noregs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iendc) )
      i0001234=rtvare(drtdm,"iendc",i000addr,1,Quote(_integer),
Quote((noregs)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"UEgrid")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ixtop",varadr(ixtop),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Mmod")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(cmeshx0) )
      i0001234=rtvare(drtdm,"cmeshx0",i000addr,1,Quote(_double precision),
Quote((idim,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(cmeshy0) )
      i0001234=rtvare(drtdm,"cmeshy0",i000addr,1,Quote(_double precision),
Quote((idim,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsc) )
      i0001234=rtvare(drtdm,"dsc",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcrv) )
      i0001234=rtvare(drtdm,"xcrv",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ycrv) )
      i0001234=rtvare(drtdm,"ycrv",i000addr,1,Quote(_double precision),
Quote((npts)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsm) )
      i0001234=rtvare(drtdm,"dsm",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dss) )
      i0001234=rtvare(drtdm,"dss",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dssleg) )
      i0001234=rtvare(drtdm,"dssleg",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsmesh) )
      i0001234=rtvare(drtdm,"dsmesh",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsmesh0) )
      i0001234=rtvare(drtdm,"dsmesh0",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsmesh1) )
      i0001234=rtvare(drtdm,"dsmesh1",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsmesh2) )
      i0001234=rtvare(drtdm,"dsmesh2",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xmsh) )
      i0001234=rtvare(drtdm,"xmsh",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ymsh) )
      i0001234=rtvare(drtdm,"ymsh",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ntop1",varadr(ntop1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtop1) )
      i0001234=rtvare(drtdm,"rtop1",i000addr,1,Quote(_double precision),
Quote((ntop1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ztop1) )
      i0001234=rtvare(drtdm,"ztop1",i000addr,1,Quote(_double precision),
Quote((ntop1)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ntop2",varadr(ntop2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtop2) )
      i0001234=rtvare(drtdm,"rtop2",i000addr,1,Quote(_double precision),
Quote((ntop2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ztop2) )
      i0001234=rtvare(drtdm,"ztop2",i000addr,1,Quote(_double precision),
Quote((ntop2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"istream",varadr(istream),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isupstreamx",varadr(isupstreamx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nupstream1",varadr(nupstream1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rupstream1) )
      i0001234=rtvare(drtdm,"rupstream1",i000addr,1,Quote(_double precision),
Quote((nupstream1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zupstream1) )
      i0001234=rtvare(drtdm,"zupstream1",i000addr,1,Quote(_double precision),
Quote((nupstream1)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nupstream2",varadr(nupstream2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rupstream2) )
      i0001234=rtvare(drtdm,"rupstream2",i000addr,1,Quote(_double precision),
Quote((nupstream2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zupstream2) )
      i0001234=rtvare(drtdm,"zupstream2",i000addr,1,Quote(_double precision),
Quote((nupstream2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndnstream1",varadr(ndnstream1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rdnstream1) )
      i0001234=rtvare(drtdm,"rdnstream1",i000addr,1,Quote(_double precision),
Quote((ndnstream1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zdnstream1) )
      i0001234=rtvare(drtdm,"zdnstream1",i000addr,1,Quote(_double precision),
Quote((ndnstream1)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndnstream2",varadr(ndnstream2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rdnstream2) )
      i0001234=rtvare(drtdm,"rdnstream2",i000addr,1,Quote(_double precision),
Quote((ndnstream2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zdnstream2) )
      i0001234=rtvare(drtdm,"zdnstream2",i000addr,1,Quote(_double precision),
Quote((ndnstream2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iplate",varadr(iplate),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nplate1",varadr(nplate1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rplate1) )
      i0001234=rtvare(drtdm,"rplate1",i000addr,1,Quote(_double precision),
Quote((nplate1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zplate1) )
      i0001234=rtvare(drtdm,"zplate1",i000addr,1,Quote(_double precision),
Quote((nplate1)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nplate2",varadr(nplate2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rplate2) )
      i0001234=rtvare(drtdm,"rplate2",i000addr,1,Quote(_double precision),
Quote((nplate2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zplate2) )
      i0001234=rtvare(drtdm,"zplate2",i000addr,1,Quote(_double precision),
Quote((nplate2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ntop",varadr(ntop),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtop) )
      i0001234=rtvare(drtdm,"rtop",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ztop) )
      i0001234=rtvare(drtdm,"ztop",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ntop0",varadr(ntop0),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtop0) )
      i0001234=rtvare(drtdm,"rtop0",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ztop0) )
      i0001234=rtvare(drtdm,"ztop0",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nbot",varadr(nbot),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rbot) )
      i0001234=rtvare(drtdm,"rbot",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zbot) )
      i0001234=rtvare(drtdm,"zbot",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nupstream",varadr(nupstream),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rupstream) )
      i0001234=rtvare(drtdm,"rupstream",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zupstream) )
      i0001234=rtvare(drtdm,"zupstream",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndnstream",varadr(ndnstream),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rdnstream) )
      i0001234=rtvare(drtdm,"rdnstream",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zdnstream) )
      i0001234=rtvare(drtdm,"zdnstream",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nplate",varadr(nplate),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rplate) )
      i0001234=rtvare(drtdm,"rplate",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zplate) )
      i0001234=rtvare(drtdm,"zplate",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nplate0",varadr(nplate0),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rplate0) )
      i0001234=rtvare(drtdm,"rplate0",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zplate0) )
      i0001234=rtvare(drtdm,"zplate0",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsnorm) )
      i0001234=rtvare(drtdm,"dsnorm",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"wtold",varadr(wtold),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nsmooth",varadr(nsmooth),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"fuzzm",varadr(fuzzm),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"delmax",varadr(delmax),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"wtmesh1",varadr(wtmesh1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wtm1) )
      i0001234=rtvare(drtdm,"wtm1",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dmix0",varadr(dmix0),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(cmeshx3) )
      i0001234=rtvare(drtdm,"cmeshx3",i000addr,1,Quote(_double precision),
Quote((idim,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(cmeshy3) )
      i0001234=rtvare(drtdm,"cmeshy3",i000addr,1,Quote(_double precision),
Quote((idim,jdim)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nff1",varadr(nff1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rff1) )
      i0001234=rtvare(drtdm,"rff1",i000addr,1,Quote(_double precision),
Quote((nff1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zff1) )
      i0001234=rtvare(drtdm,"zff1",i000addr,1,Quote(_double precision),
Quote((nff1)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nff2",varadr(nff2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rff2) )
      i0001234=rtvare(drtdm,"rff2",i000addr,1,Quote(_double precision),
Quote((nff2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zff2) )
      i0001234=rtvare(drtdm,"zff2",i000addr,1,Quote(_double precision),
Quote((nff2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nff",varadr(nff),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rff) )
      i0001234=rtvare(drtdm,"rff",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zff) )
      i0001234=rtvare(drtdm,"zff",i000addr,1,Quote(_double precision),
Quote((nptmp)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsmesh3) )
      i0001234=rtvare(drtdm,"dsmesh3",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsmeshff) )
      i0001234=rtvare(drtdm,"dsmeshff",i000addr,1,Quote(_double precision),
Quote((idim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"cwtffu",varadr(cwtffu),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"cwtffd",varadr(cwtffd),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isxtform",varadr(isxtform),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iswtform",varadr(iswtform),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"wtff1",varadr(wtff1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxff1",varadr(slpxff1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxffu1",varadr(slpxffu1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxffd1",varadr(slpxffd1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxdff1",varadr(nxdff1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"wtff2",varadr(wtff2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxff2",varadr(slpxff2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxffu2",varadr(slpxffu2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxffd2",varadr(slpxffd2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxdff2",varadr(nxdff2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Refinex")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"isrefxptn",varadr(isrefxptn),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxmod",varadr(nxmod),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxptl",varadr(alfxptl),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt2l",varadr(alfxpt2l),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxptu",varadr(alfxptu),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt2u",varadr(alfxpt2u),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt",varadr(alfxpt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfxpt2",varadr(alfxpt2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rsu) )
      i0001234=rtvare(drtdm,"rsu",i000addr,1,Quote(_double precision),
Quote((0:nym+2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zsu) )
      i0001234=rtvare(drtdm,"zsu",i000addr,1,Quote(_double precision),
Quote((0:nym+2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rsx) )
      i0001234=rtvare(drtdm,"rsx",i000addr,1,Quote(_double precision),
Quote((0:nym+2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zsx) )
      i0001234=rtvare(drtdm,"zsx",i000addr,1,Quote(_double precision),
Quote((0:nym+2)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nflux",varadr(nflux),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rflux) )
      i0001234=rtvare(drtdm,"rflux",i000addr,1,Quote(_double precision),
Quote((npts)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zflux) )
      i0001234=rtvare(drtdm,"zflux",i000addr,1,Quote(_double precision),
Quote((npts)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dsflux) )
      i0001234=rtvare(drtdm,"dsflux",i000addr,1,Quote(_double precision),
Quote((npts)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rmm) )
      i0001234=rtvare(drtdm,"rmm",i000addr,1,Quote(_double precision),
Quote((0:nym,0:nxm)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zmm) )
      i0001234=rtvare(drtdm,"zmm",i000addr,1,Quote(_double precision),
Quote((0:nym,0:nxm)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nsmoothx",varadr(nsmoothx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Xmesh")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ndat",varadr(ndat),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xdat) )
      i0001234=rtvare(drtdm,"xdat",i000addr,1,Quote(_double precision),
Quote((ndat)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tdat) )
      i0001234=rtvare(drtdm,"tdat",i000addr,1,Quote(_double precision),
Quote((ndat)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kxmesh",varadr(kxmesh),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpxt",varadr(slpxt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( alfx )
      i0001234=rtvare(drtdm,"alfx",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( dxgas )
      i0001234=rtvare(drtdm,"dxgas",i000addr,0,Quote(double precision),
Quote((2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nxgas )
      i0001234=rtvare(drtdm,"nxgas",i000addr,0,Quote(integer),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dt1",varadr(dt1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dx1",varadr(dx1),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dt2",varadr(dt2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dx2",varadr(dx2),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ileft",varadr(ileft),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dleft",varadr(dleft),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iright",varadr(iright),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dright",varadr(dright),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kord",varadr(kord),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndatp2",varadr(ndatp2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kntopt",varadr(kntopt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tknt) )
      i0001234=rtvare(drtdm,"tknt",i000addr,1,Quote(_double precision),
Quote((ndatp2+4)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(z1work) )
      i0001234=rtvare(drtdm,"z1work",i000addr,1,Quote(_double precision),
Quote((5*(ndat+2))), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(z1cscoef) )
      i0001234=rtvare(drtdm,"z1cscoef",i000addr,1,Quote(_double precision),
Quote((ndatp2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wrk1) )
      i0001234=rtvare(drtdm,"wrk1",i000addr,1,Quote(_double precision),
Quote((3*kord)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iflag1",varadr(iflag1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Dnull_temp")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nxmb",varadr(nxmb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nymb",varadr(nymb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rmb) )
      i0001234=rtvare(drtdm,"rmb",i000addr,1,Quote(_double precision),
Quote((0:nxmb+1,0:nymb+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zmb) )
      i0001234=rtvare(drtdm,"zmb",i000addr,1,Quote(_double precision),
Quote((0:nxmb+1,0:nymb+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixpt1b",varadr(ixpt1b),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixtopb",varadr(ixtopb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixpt2b",varadr(ixpt2b),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iysptrxb",varadr(iysptrxb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxmu",varadr(nxmu),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nymu",varadr(nymu),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rmu) )
      i0001234=rtvare(drtdm,"rmu",i000addr,1,Quote(_double precision),
Quote((0:nxmu+1,0:nymu+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zmu) )
      i0001234=rtvare(drtdm,"zmu",i000addr,1,Quote(_double precision),
Quote((0:nxmu+1,0:nymu+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixpt1u",varadr(ixpt1u),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixtopu",varadr(ixtopu),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixpt2u",varadr(ixpt2u),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iysptrxu",varadr(iysptrxu),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Expseed")
      if(jgrp = 0) go to 999
      i000addr = varadr ( fraclplt )
      i0001234=rtvare(drtdm,"fraclplt",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( alfxdiv )
      i0001234=rtvare(drtdm,"alfxdiv",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( alfxcore )
      i0001234=rtvare(drtdm,"alfxcore",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( shift_seed_leg )
      i0001234=rtvare(drtdm,"shift_seed_leg",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( shift_seed_core )
      i0001234=rtvare(drtdm,"shift_seed_core",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nxlplt )
      i0001234=rtvare(drtdm,"nxlplt",i000addr,0,Quote(integer),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nxlxpt )
      i0001234=rtvare(drtdm,"nxlxpt",i000addr,0,Quote(integer),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"fcorenunif",varadr(fcorenunif),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Xfcn")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn2",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn3",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "xfcn4",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nxtotal:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "xcscoef",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Driver")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "setidim",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "grdrun",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "ingrd",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "codsys",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(icood:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iseg:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(is:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(dy:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(region:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(alpha1:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "findalph",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nsys:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iseg:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(xob:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(yob:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(alphab:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readflx",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "prune",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "extend",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "splfit",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "sow",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "meshgen",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(region:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "orthogx",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ixtyp:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j0:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(xob:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(yob:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(alphab:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "orthogrd",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ixtyp:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j0:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(xob:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(yob:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(alphab:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readgrid",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(runid:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_runid_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "writesn",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(runid:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_runid_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "writedn",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(runid:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_runid_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "writedata",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(runid:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_runid_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "writednf",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(runid:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_runid_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "intersect2",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(x1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(y1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i1min:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i1max:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(x2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(y2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i2min:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i2max:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(xc:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(yc:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i1c:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i2c:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fuzz:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ierr:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "meshmod2",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(region:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "smooth",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j1:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j2:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "writeue",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "grd2wdf",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "evalspln",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iseg:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(xo:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(yo:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "idealgrd",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "mirrorgrd",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "gett",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "getu",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "getd",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "getp",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "meshmod3",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(region:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "smoother",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "smoother2",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "meshff",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(region:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "fpoloidal",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(psi:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "pressure",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(psi:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "psif",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(z:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "brf",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(z:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "bzf",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(z:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rsurface",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(quadrant:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "fluxcurve",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(quadrant:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iy:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "refinexm",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "refine_xpt",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "smoothx",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rmm:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(zmm:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nd1:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nd2:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iy1:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iy2:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(quadrant:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "mapdnbot",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "mapdntop",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "magnetics",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ixmin:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ixmax:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iymin:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iymax:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "add_guardc_tp",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "exponseed",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      call rtsetdoc(drtdm,"grd_basis.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine grdxpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.19) then
         call grdxp19(name1234)
      elseif(iseg.eq.20) then
         call grdxp20(name1234)
      else
         call baderr('grdxpf: impossible event')
      endif
      return
      end
      subroutine grdxp19(name1234)
      character*(*) name1234
      external grd_handler
      external [xfcn]
      external [xfcn2]
      external [xfcn3]
      external [xfcn4]
      external [xcscoef]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'xfcn') then
         call parexecf(grd_handler, 0, [xfcn])
      elseif(name1234 = 'xfcn2') then
         call parexecf(grd_handler, 1, [xfcn2])
      elseif(name1234 = 'xfcn3') then
         call parexecf(grd_handler, 2, [xfcn3])
      elseif(name1234 = 'xfcn4') then
         call parexecf(grd_handler, 3, [xfcn4])
      elseif(name1234 = 'xcscoef') then
         call parexecf(grd_handler, 4, [xcscoef])
      else
         call baderr('grdxp19: impossible event: '//name5678)
      endif
      return
      end
      subroutine grdxp20(name1234)
      character*(*) name1234
      external grd_handler
      external [setidim]
      external [grdrun]
      external [ingrd]
      external [codsys]
      external [findalph]
      external [readflx]
      external [prune]
      external [extend]
      external [splfit]
      external [sow]
      external [meshgen]
      external [orthogx]
      external [orthogrd]
      external [readgrid]
      external [writesn]
      external [writedn]
      external [writedata]
      external [writednf]
      external [intersect2]
      external [meshmod2]
      external [smooth]
      external [writeue]
      external [grd2wdf]
      external [evalspln]
      external [idealgrd]
      external [mirrorgrd]
      external [gett]
      external [getu]
      external [getd]
      external [getp]
      external [meshmod3]
      external [smoother]
      external [smoother2]
      external [meshff]
      external [fpoloidal]
      external [pressure]
      external [psif]
      external [brf]
      external [bzf]
      external [rsurface]
      external [fluxcurve]
      external [refinexm]
      external [refine_xpt]
      external [smoothx]
      external [mapdnbot]
      external [mapdntop]
      external [magnetics]
      external [add_guardc_tp]
      external [exponseed]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'setidim') then
         call parexecf(grd_handler, 5, [setidim])
      elseif(name1234 = 'grdrun') then
         call parexecf(grd_handler, 6, [grdrun])
      elseif(name1234 = 'ingrd') then
         call parexecf(grd_handler, 7, [ingrd])
      elseif(name1234 = 'codsys') then
         call parexecf(grd_handler, 8, [codsys])
      elseif(name1234 = 'findalph') then
         call parexecf(grd_handler, 9, [findalph])
      elseif(name1234 = 'readflx') then
         call parexecf(grd_handler, 10, [readflx])
      elseif(name1234 = 'prune') then
         call parexecf(grd_handler, 11, [prune])
      elseif(name1234 = 'extend') then
         call parexecf(grd_handler, 12, [extend])
      elseif(name1234 = 'splfit') then
         call parexecf(grd_handler, 13, [splfit])
      elseif(name1234 = 'sow') then
         call parexecf(grd_handler, 14, [sow])
      elseif(name1234 = 'meshgen') then
         call parexecf(grd_handler, 15, [meshgen])
      elseif(name1234 = 'orthogx') then
         call parexecf(grd_handler, 16, [orthogx])
      elseif(name1234 = 'orthogrd') then
         call parexecf(grd_handler, 17, [orthogrd])
      elseif(name1234 = 'readgrid') then
         call parexecf(grd_handler, 18, [readgrid])
      elseif(name1234 = 'writesn') then
         call parexecf(grd_handler, 19, [writesn])
      elseif(name1234 = 'writedn') then
         call parexecf(grd_handler, 20, [writedn])
      elseif(name1234 = 'writedata') then
         call parexecf(grd_handler, 21, [writedata])
      elseif(name1234 = 'writednf') then
         call parexecf(grd_handler, 22, [writednf])
      elseif(name1234 = 'intersect2') then
         call parexecf(grd_handler, 23, [intersect2])
      elseif(name1234 = 'meshmod2') then
         call parexecf(grd_handler, 24, [meshmod2])
      elseif(name1234 = 'smooth') then
         call parexecf(grd_handler, 25, [smooth])
      elseif(name1234 = 'writeue') then
         call parexecf(grd_handler, 26, [writeue])
      elseif(name1234 = 'grd2wdf') then
         call parexecf(grd_handler, 27, [grd2wdf])
      elseif(name1234 = 'evalspln') then
         call parexecf(grd_handler, 28, [evalspln])
      elseif(name1234 = 'idealgrd') then
         call parexecf(grd_handler, 29, [idealgrd])
      elseif(name1234 = 'mirrorgrd') then
         call parexecf(grd_handler, 30, [mirrorgrd])
      elseif(name1234 = 'gett') then
         call parexecf(grd_handler, 31, [gett])
      elseif(name1234 = 'getu') then
         call parexecf(grd_handler, 32, [getu])
      elseif(name1234 = 'getd') then
         call parexecf(grd_handler, 33, [getd])
      elseif(name1234 = 'getp') then
         call parexecf(grd_handler, 34, [getp])
      elseif(name1234 = 'meshmod3') then
         call parexecf(grd_handler, 35, [meshmod3])
      elseif(name1234 = 'smoother') then
         call parexecf(grd_handler, 36, [smoother])
      elseif(name1234 = 'smoother2') then
         call parexecf(grd_handler, 37, [smoother2])
      elseif(name1234 = 'meshff') then
         call parexecf(grd_handler, 38, [meshff])
      elseif(name1234 = 'fpoloidal') then
         call parexecf(grd_handler, 39, [fpoloidal])
      elseif(name1234 = 'pressure') then
         call parexecf(grd_handler, 40, [pressure])
      elseif(name1234 = 'psif') then
         call parexecf(grd_handler, 41, [psif])
      elseif(name1234 = 'brf') then
         call parexecf(grd_handler, 42, [brf])
      elseif(name1234 = 'bzf') then
         call parexecf(grd_handler, 43, [bzf])
      elseif(name1234 = 'rsurface') then
         call parexecf(grd_handler, 44, [rsurface])
      elseif(name1234 = 'fluxcurve') then
         call parexecf(grd_handler, 45, [fluxcurve])
      elseif(name1234 = 'refinexm') then
         call parexecf(grd_handler, 46, [refinexm])
      elseif(name1234 = 'refine_xpt') then
         call parexecf(grd_handler, 47, [refine_xpt])
      elseif(name1234 = 'smoothx') then
         call parexecf(grd_handler, 48, [smoothx])
      elseif(name1234 = 'mapdnbot') then
         call parexecf(grd_handler, 49, [mapdnbot])
      elseif(name1234 = 'mapdntop') then
         call parexecf(grd_handler, 50, [mapdntop])
      elseif(name1234 = 'magnetics') then
         call parexecf(grd_handler, 51, [magnetics])
      elseif(name1234 = 'add_guardc_tp') then
         call parexecf(grd_handler, 52, [add_guardc_tp])
      elseif(name1234 = 'exponseed') then
         call parexecf(grd_handler, 53, [exponseed])
      else
         call baderr('grdxp20: impossible event: '//name5678)
      endif
      return
      end
      function grdbfcn(ss,sp,nargs,name1234,sx)
      integer grdbfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in grd')
      call baderr(name1234)
      return(ERR)
      end
