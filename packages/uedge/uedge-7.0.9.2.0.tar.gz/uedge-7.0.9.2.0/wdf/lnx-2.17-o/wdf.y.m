      subroutine wdfinit0
c initializes a Package
      integer drtdm
      common /wdfrtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("wdf")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call wdfdata
      call wdfwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_wdf],[
Use(Dimwdf)
Use(Auxw)
Use(Linkgrd)
Use(Nodew)
Use(Options)
Use(Degas1)
Use(Degas2)
Use(Eqdsk)
Use(Urun)
])
      block data wdfiyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_wdf
      data nptskb/2/,npw/3/,npsegy/1/,nptp1/2/,ndec/2/,npis/2/,npns/2/
      data mpsegxz/MPSEGXZ/,mpw/MPW/
      data iswdfon/1/,frr01/.001/,frr02/.001/
      data h2frac/1.00/,lmaxwell/0/,lmesh/2/,loutput/3/,lproft/1/
      data lrflct1/1/,lrflct2/2/,lrrulet/1/,lsymetry/1/,lunit/-1/
      data maxerrs/100/,mparts/0/,ncount/100/,nhyd/NPHYD*2/,nocols/420/
      data norows/840/,nosplits/1/,nowals/1/,plsang/90.00/,scrrmax/1.01/
      data shethp/3.00/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine wdfdata
Use_All_Groups_wdf
      external wdfiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(cmeshxw))
      call clraddr(Point(cmeshyw))
      call clraddr(Point(ilmaxw))
      call clraddr(Point(ixpointw))
      call clraddr(Point(jsptrxw))
      call clraddr(Point(jminw))
      call clraddr(Point(jmaxw))
      call clraddr(Point(jindx))
      call clraddr(Point(nodedwn))
      call clraddr(Point(nodewl))
      call clraddr(Point(nopts))
      call clraddr(Point(walnodx))
      call clraddr(Point(walnody))
      call clraddr(Point(deni0))
      call clraddr(Point(fictrr0))
      call clraddr(Point(nosegsxz))
      call clraddr(Point(nosegsy))
      call clraddr(Point(t0puff))
      call clraddr(Point(ti0))
      call clraddr(Point(arcdeg))
      call clraddr(Point(currxzt))
      call clraddr(Point(denehvt))
      call clraddr(Point(denihvt))
      call clraddr(Point(ficrrhvt))
      call clraddr(Point(frabsorb))
      call clraddr(Point(gridx))
      call clraddr(Point(gridz))
      call clraddr(Point(kplrecyc))
      call clraddr(Point(ksplzone))
      call clraddr(Point(kzone1))
      call clraddr(Point(kzone2))
      call clraddr(Point(lboun1))
      call clraddr(Point(lboun2))
      call clraddr(Point(rflcoef))
      call clraddr(Point(tehvt))
      call clraddr(Point(tihvt))
      call clraddr(Point(twall))
      call clraddr(Point(vflowx))
      call clraddr(Point(vflowy))
      call clraddr(Point(vflowz))
      call clraddr(Point(vsorchvt))
      call clraddr(Point(xwall))
      call clraddr(Point(zwall))
      call clraddr(Point(xlimw))
      call clraddr(Point(ylimw))

      return
       end
      subroutine wdfdbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,9,162)
      return
       end
      subroutine wdfwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /wdfrtdm/ drtdm
Use_All_Groups_wdf

      Address i000addr
      external varadr
      Address varadr


      call wdfdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Dimwdf")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"noregsw",varadr(noregsw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptsvb",varadr(nptsvb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptshb",varadr(nptshb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptskb",varadr(nptskb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npw",varadr(npw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npsegxz",varadr(npsegxz),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptsw",varadr(nptsw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npsegy",varadr(npsegy),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptp1",varadr(nptp1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ndec",varadr(ndec),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npis",varadr(npis),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npns",varadr(npns),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mpsegxz",varadr(mpsegxz),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mpw",varadr(mpw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"idimw",varadr(idimw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jdimw",varadr(jdimw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nixw",varadr(nixw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Auxw")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ixpt1b",varadr(ixpt1b),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixtop1b",varadr(ixtop1b),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixtop2b",varadr(ixtop2b),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixpt2b",varadr(ixpt2b),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nohzsb",varadr(nohzsb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"novzsb",varadr(novzsb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nosegsxzb",varadr(nosegsxzb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Linkgrd")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(cmeshxw) )
      i0001234=rtvare(drtdm,"cmeshxw",i000addr,1,Quote(_double precision),
Quote((idimw,jdimw)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(cmeshyw) )
      i0001234=rtvare(drtdm,"cmeshyw",i000addr,1,Quote(_double precision),
Quote((idimw,jdimw)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ilmaxw) )
      i0001234=rtvare(drtdm,"ilmaxw",i000addr,1,Quote(_integer),
Quote((noregsw)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixpointw) )
      i0001234=rtvare(drtdm,"ixpointw",i000addr,1,Quote(_integer),
Quote((nixw,noregsw)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(jsptrxw) )
      i0001234=rtvare(drtdm,"jsptrxw",i000addr,1,Quote(_integer),
Quote((noregsw)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jaxisw",varadr(jaxisw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(jminw) )
      i0001234=rtvare(drtdm,"jminw",i000addr,1,Quote(_integer),
Quote((noregsw)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(jmaxw) )
      i0001234=rtvare(drtdm,"jmaxw",i000addr,1,Quote(_integer),
Quote((noregsw)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Nodew")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(jindx) )
      i0001234=rtvare(drtdm,"jindx",i000addr,1,Quote(_integer),
Quote((ndec)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"njwall",varadr(njwall),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nodedwn) )
      i0001234=rtvare(drtdm,"nodedwn",i000addr,1,Quote(_integer),
Quote((ndec)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nodewl) )
      i0001234=rtvare(drtdm,"nodewl",i000addr,1,Quote(_integer),
Quote((nptshb,ndec)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nopts) )
      i0001234=rtvare(drtdm,"nopts",i000addr,1,Quote(_integer),
Quote((ndec)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( numseg )
      i0001234=rtvare(drtdm,"numseg",i000addr,0,Quote(integer),
Quote((3)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(walnodx) )
      i0001234=rtvare(drtdm,"walnodx",i000addr,1,Quote(_double precision),
Quote((nptshb,ndec)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(walnody) )
      i0001234=rtvare(drtdm,"walnody",i000addr,1,Quote(_double precision),
Quote((nptshb,ndec)), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Options")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"iswdfon",varadr(iswdfon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"fname",varadr(fname),0,Quote(character*16),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"idline",varadr(idline),0,Quote(character*(NCHAR)),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"endmark",varadr(endmark),0,Quote(character*(8)),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ivnull",varadr(ivnull),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"frr01",varadr(frr01),0,Quote(double precision),
Quote(scalar), "/sec")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"frr02",varadr(frr02),0,Quote(double precision),
Quote(scalar), "/sec")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Degas1")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(deni0) )
      i0001234=rtvare(drtdm,"deni0",i000addr,1,Quote(_double precision),
Quote((npis)), "/cm**3")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"engymin",varadr(engymin),0,Quote(double precision),
Quote(scalar), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fictrr0) )
      i0001234=rtvare(drtdm,"fictrr0",i000addr,1,Quote(_double precision),
Quote((npns)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"h2frac",varadr(h2frac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lchex",varadr(lchex),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"leh0",varadr(leh0),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lflags",varadr(lflags),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lgeomtry",varadr(lgeomtry),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lhalpha",varadr(lhalpha),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lmaxwell",varadr(lmaxwell),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lmesh",varadr(lmesh),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lnamelst",varadr(lnamelst),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lneutral",varadr(lneutral),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"loutput",varadr(loutput),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lplasma",varadr(lplasma),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lprofh",varadr(lprofh),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lproft",varadr(lproft),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lprofv",varadr(lprofv),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lrandom",varadr(lrandom),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lrecycle",varadr(lrecycle),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lrflct1",varadr(lrflct1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lrflct2",varadr(lrflct2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lrrulet",varadr(lrrulet),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lshrtrun",varadr(lshrtrun),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lsources",varadr(lsources),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lsputter",varadr(lsputter),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lstat",varadr(lstat),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lsymetry",varadr(lsymetry),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lunit",varadr(lunit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lvolsrc",varadr(lvolsrc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lwall",varadr(lwall),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lwalldst",varadr(lwalldst),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"maxerrs",varadr(maxerrs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mparts",varadr(mparts),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncount",varadr(ncount),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nexit",varadr(nexit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nhyd )
      i0001234=rtvare(drtdm,"nhyd",i000addr,0,Quote(integer),
Quote((NPHYD)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nocols",varadr(nocols),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nohbs",varadr(nohbs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nohzs",varadr(nohzs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"norows",varadr(norows),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nosegsxz) )
      i0001234=rtvare(drtdm,"nosegsxz",i000addr,1,Quote(_integer),
Quote((npw)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nosegsy) )
      i0001234=rtvare(drtdm,"nosegsy",i000addr,1,Quote(_integer),
Quote((npw)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nosplits",varadr(nosplits),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"notasks",varadr(notasks),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"notzs",varadr(notzs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"novbs",varadr(novbs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"novzs",varadr(novzs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nowals",varadr(nowals),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nwriter",varadr(nwriter),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nseed )
      i0001234=rtvare(drtdm,"nseed",i000addr,0,Quote(integer),
Quote((NTASK)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ntty",varadr(ntty),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"plsang",varadr(plsang),0,Quote(double precision),
Quote(scalar), "degrees")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rmajor",varadr(rmajor),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rminor",varadr(rminor),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rrengy",varadr(rrengy),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"scrrmax",varadr(scrrmax),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"shethp",varadr(shethp),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sndspd",varadr(sndspd),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(t0puff) )
      i0001234=rtvare(drtdm,"t0puff",i000addr,1,Quote(_double precision),
Quote((npns)), "eV")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,.025)
      i0001234=rtvare(drtdm,"te0",varadr(te0),0,Quote(double precision),
Quote(scalar), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ti0) )
      i0001234=rtvare(drtdm,"ti0",i000addr,1,Quote(_double precision),
Quote((npis)), "eV")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"wtmin0",varadr(wtmin0),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xlen",varadr(xlen),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ylen",varadr(ylen),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zlen",varadr(zlen),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Degas2")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(arcdeg) )
      i0001234=rtvare(drtdm,"arcdeg",i000addr,1,Quote(_double precision),
Quote((nptp1)), "degrees")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(currxzt) )
      i0001234=rtvare(drtdm,"currxzt",i000addr,1,Quote(_double precision),
Quote((npsegxz,npsegy,npw,npis)), "/sec")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(denehvt) )
      i0001234=rtvare(drtdm,"denehvt",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "/cm**3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(denihvt) )
      i0001234=rtvare(drtdm,"denihvt",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb,npis)), "/cm**3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ficrrhvt) )
      i0001234=rtvare(drtdm,"ficrrhvt",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb,npns)), "/sec")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(frabsorb) )
      i0001234=rtvare(drtdm,"frabsorb",i000addr,1,Quote(_double precision),
Quote((npsegxz,npsegy,npw,npns)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gridx) )
      i0001234=rtvare(drtdm,"gridx",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "cm")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gridz) )
      i0001234=rtvare(drtdm,"gridz",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "cm")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(kplrecyc) )
      i0001234=rtvare(drtdm,"kplrecyc",i000addr,1,Quote(_integer),
Quote((nptsvb,nptshb)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ksplzone) )
      i0001234=rtvare(drtdm,"ksplzone",i000addr,1,Quote(_integer),
Quote((nptsvb,nptshb,nptskb)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( kwmat )
      i0001234=rtvare(drtdm,"kwmat",i000addr,0,Quote(character*8),
Quote((MPSEGXZ,MPW)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(kzone1) )
      i0001234=rtvare(drtdm,"kzone1",i000addr,1,Quote(_integer),
Quote((nptsvb,nptshb)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(kzone2) )
      i0001234=rtvare(drtdm,"kzone2",i000addr,1,Quote(_integer),
Quote((nptsvb,nptshb)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lboun1) )
      i0001234=rtvare(drtdm,"lboun1",i000addr,1,Quote(_integer),
Quote((nptsvb)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lboun2) )
      i0001234=rtvare(drtdm,"lboun2",i000addr,1,Quote(_integer),
Quote((nptshb)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rflcoef) )
      i0001234=rtvare(drtdm,"rflcoef",i000addr,1,Quote(_double precision),
Quote((npsegxz,npsegy,npw)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tehvt) )
      i0001234=rtvare(drtdm,"tehvt",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tihvt) )
      i0001234=rtvare(drtdm,"tihvt",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb,npis)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(twall) )
      i0001234=rtvare(drtdm,"twall",i000addr,1,Quote(_double precision),
Quote((npsegxz,npsegy,npw)), "degrees K")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(vflowx) )
      i0001234=rtvare(drtdm,"vflowx",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "cm/sec")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(vflowy) )
      i0001234=rtvare(drtdm,"vflowy",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "cm/sec")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(vflowz) )
      i0001234=rtvare(drtdm,"vflowz",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb)), "cm/sec")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(vsorchvt) )
      i0001234=rtvare(drtdm,"vsorchvt",i000addr,1,Quote(_double precision),
Quote((nptsvb,nptshb,nptskb,npns)), "/sec")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xwall) )
      i0001234=rtvare(drtdm,"xwall",i000addr,1,Quote(_double precision),
Quote((nptsw,npw)), "cm")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zwall) )
      i0001234=rtvare(drtdm,"zwall",i000addr,1,Quote(_double precision),
Quote((nptsw,npw)), "cm")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Eqdsk")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"xdimw",varadr(xdimw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zdimw",varadr(zdimw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rgrid1w",varadr(rgrid1w),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"eshotw",varadr(eshotw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"etimew",varadr(etimew),0,Quote(double precision),
Quote(scalar), "msec")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"bcentrw",varadr(bcentrw),0,Quote(double precision),
Quote(scalar), "Tesla")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rcentrw",varadr(rcentrw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rmagxw",varadr(rmagxw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zmagxw",varadr(zmagxw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"simagxw",varadr(simagxw),0,Quote(double precision),
Quote(scalar), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sibdryw",varadr(sibdryw),0,Quote(double precision),
Quote(scalar), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rsepsw",varadr(rsepsw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zsepsw",varadr(zsepsw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rvsinw",varadr(rvsinw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zvsinw",varadr(zvsinw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rvsoutw",varadr(rvsoutw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zvsoutw",varadr(zvsoutw),0,Quote(double precision),
Quote(scalar), "cm")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nlimw",varadr(nlimw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xlimw) )
      i0001234=rtvare(drtdm,"xlimw",i000addr,1,Quote(_double precision),
Quote((nlimw)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ylimw) )
      i0001234=rtvare(drtdm,"ylimw",i000addr,1,Quote(_double precision),
Quote((nlimw)), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Urun")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "write_degas",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "write_namelist",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "frrate",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "ueplasma",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      call rtsetdoc(drtdm,"wdf.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine wdfxpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.9) then
         call wdfxp9(name1234)
      else
         call baderr('wdfxpf: impossible event')
      endif
      return
      end
      subroutine wdfxp9(name1234)
      character*(*) name1234
      external wdf_handler
      external [write_degas]
      external [write_namelist]
      external [frrate]
      external [ueplasma]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'write_degas') then
         call parexecf(wdf_handler, 0, [write_degas])
      elseif(name1234 = 'write_namelist') then
         call parexecf(wdf_handler, 1, [write_namelist])
      elseif(name1234 = 'frrate') then
         call parexecf(wdf_handler, 2, [frrate])
      elseif(name1234 = 'ueplasma') then
         call parexecf(wdf_handler, 3, [ueplasma])
      else
         call baderr('wdfxp9: impossible event: '//name5678)
      endif
      return
      end
      function wdfbfcn(ss,sp,nargs,name1234,sx)
      integer wdfbfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in wdf')
      call baderr(name1234)
      return(ERR)
      end
