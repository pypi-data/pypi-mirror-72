      subroutine aphinit0
c initializes a Package
      integer drtdm
      common /aphrtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("aph")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call aphdata
      call aphwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_aph],[
Use(Physical_constants)
Use(Data_input)
Use(Ionization_energy)
Use(Rtdata)
Use(Rtdegas)
Use(Rtfcn)
Use(Aphwrk)
Use(Subs)
])
      block data aphiyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_aph
      data ev/1.6022e-19/,m_prot/1.67e-27/
      data issgvcxc/0/,sgvcxc/2.e-14/,isaphdir/1/
      data erad/25./
      data mpe/48/,mpd/11/,mpr/1/
      data kxords/4/,kyords/4/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine aphdata
Use_All_Groups_aph
      external aphiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(htza))
      call clraddr(Point(htzn))
      call clraddr(Point(htn))
      call clraddr(Point(htt))
      call clraddr(Point(htln))
      call clraddr(Point(htlt))
      call clraddr(Point(htlsa))
      call clraddr(Point(htlra))
      call clraddr(Point(htlcx))
      call clraddr(Point(htlqa))
      call clraddr(Point(wsveh))
      call clraddr(Point(wsveh0))
      call clraddr(Point(wlemiss))
      call clraddr(Point(welms))
      call clraddr(Point(welms1))
      call clraddr(Point(welms2))
      call clraddr(Point(pne3))
      call clraddr(Point(pne31))
      call clraddr(Point(pne32))
      call clraddr(Point(pne2))
      call clraddr(Point(pne21))
      call clraddr(Point(pne22))
      call clraddr(Point(pne41))
      call clraddr(Point(pne42))
      call clraddr(Point(pne51))
      call clraddr(Point(pne52))
      call clraddr(Point(pne61))
      call clraddr(Point(pne62))
      call clraddr(Point(pne71))
      call clraddr(Point(pne72))
      call clraddr(Point(pne81))
      call clraddr(Point(pne82))
      call clraddr(Point(pne91))
      call clraddr(Point(pne92))
      call clraddr(Point(svdum2))
      call clraddr(Point(svphcx))
      call clraddr(Point(ekpt))
      call clraddr(Point(dkpt))
      call clraddr(Point(xdata))
      call clraddr(Point(ydata))
      call clraddr(Point(fdata))
      call clraddr(Point(xknots))
      call clraddr(Point(yknots))
      call clraddr(Point(workh))
      call clraddr(Point(rsacoef))
      call clraddr(Point(rracoef))
      call clraddr(Point(rqacoef))

      return
       end
      subroutine aphdbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,8,94)
      return
       end
      subroutine aphwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /aphrtdm/ drtdm
Use_All_Groups_aph

      Address i000addr
      external varadr
      Address varadr


      call aphdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Physical_constants")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ev",varadr(ev),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"m_prot",varadr(m_prot),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Data_input")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"issgvcxc",varadr(issgvcxc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sgvcxc",varadr(sgvcxc),0,Quote(double precision),
Quote(scalar), "m^2/s")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isaphdir",varadr(isaphdir),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"aphdir",varadr(aphdir),0,Quote(character*120),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"data_directory",varadr(data_directory),0,Quote(character*120),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Ionization_energy")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"erad",varadr(erad),0,Quote(double precision),
Quote(scalar), "eV")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Rtdata")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"labelht",varadr(labelht),0,Quote(character*120),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"htns",varadr(htns),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"htnn",varadr(htnn),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"htnt",varadr(htnt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htza) )
      i0001234=rtvare(drtdm,"htza",i000addr,1,Quote(_double precision),
Quote((0:htns-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htzn) )
      i0001234=rtvare(drtdm,"htzn",i000addr,1,Quote(_double precision),
Quote((0:htns-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htn) )
      i0001234=rtvare(drtdm,"htn",i000addr,1,Quote(_double precision),
Quote((0:htnn)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htt) )
      i0001234=rtvare(drtdm,"htt",i000addr,1,Quote(_double precision),
Quote((0:htnt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htln) )
      i0001234=rtvare(drtdm,"htln",i000addr,1,Quote(_double precision),
Quote((0:htnn)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htlt) )
      i0001234=rtvare(drtdm,"htlt",i000addr,1,Quote(_double precision),
Quote((0:htnt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htlsa) )
      i0001234=rtvare(drtdm,"htlsa",i000addr,1,Quote(_double precision),
Quote((0:htnt,0:htnn,0:htns-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htlra) )
      i0001234=rtvare(drtdm,"htlra",i000addr,1,Quote(_double precision),
Quote((0:htnt,0:htnn,0:htns-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htlcx) )
      i0001234=rtvare(drtdm,"htlcx",i000addr,1,Quote(_double precision),
Quote((0:htnt,0:htnn,0:htns-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(htlqa) )
      i0001234=rtvare(drtdm,"htlqa",i000addr,1,Quote(_double precision),
Quote((0:htnt,0:htnn,0:htns-1)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Rtdegas")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"mpe",varadr(mpe),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mpd",varadr(mpd),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mpr",varadr(mpr),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wsveh) )
      i0001234=rtvare(drtdm,"wsveh",i000addr,1,Quote(_double precision),
Quote((mpe,mpd,mpr)), "m**3/s")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wsveh0) )
      i0001234=rtvare(drtdm,"wsveh0",i000addr,1,Quote(_double precision),
Quote((mpe,mpd,mpr)), "m**3/s")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wlemiss) )
      i0001234=rtvare(drtdm,"wlemiss",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "W m**3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(welms) )
      i0001234=rtvare(drtdm,"welms",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(welms1) )
      i0001234=rtvare(drtdm,"welms1",i000addr,1,Quote(_double precision),
Quote((mpe,mpd,mpr)), "J/sec")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(welms2) )
      i0001234=rtvare(drtdm,"welms2",i000addr,1,Quote(_double precision),
Quote((mpe,mpd,mpr)), "J/sec")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne3) )
      i0001234=rtvare(drtdm,"pne3",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne31) )
      i0001234=rtvare(drtdm,"pne31",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne32) )
      i0001234=rtvare(drtdm,"pne32",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne2) )
      i0001234=rtvare(drtdm,"pne2",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne21) )
      i0001234=rtvare(drtdm,"pne21",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne22) )
      i0001234=rtvare(drtdm,"pne22",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne41) )
      i0001234=rtvare(drtdm,"pne41",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne42) )
      i0001234=rtvare(drtdm,"pne42",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne51) )
      i0001234=rtvare(drtdm,"pne51",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne52) )
      i0001234=rtvare(drtdm,"pne52",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne61) )
      i0001234=rtvare(drtdm,"pne61",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne62) )
      i0001234=rtvare(drtdm,"pne62",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne71) )
      i0001234=rtvare(drtdm,"pne71",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne72) )
      i0001234=rtvare(drtdm,"pne72",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne81) )
      i0001234=rtvare(drtdm,"pne81",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne82) )
      i0001234=rtvare(drtdm,"pne82",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne91) )
      i0001234=rtvare(drtdm,"pne91",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pne92) )
      i0001234=rtvare(drtdm,"pne92",i000addr,1,Quote(_double precision),
Quote((mpe,mpd)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(svdum2) )
      i0001234=rtvare(drtdm,"svdum2",i000addr,1,Quote(_double precision),
Quote((mpe,mpe)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(svphcx) )
      i0001234=rtvare(drtdm,"svphcx",i000addr,1,Quote(_double precision),
Quote((mpe,mpe)), "m**3/s")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ekpt) )
      i0001234=rtvare(drtdm,"ekpt",i000addr,1,Quote(_double precision),
Quote((mpe)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rlemin",varadr(rlemin),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rlemax",varadr(rlemax),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"erefmin",varadr(erefmin),0,Quote(double precision),
Quote(scalar), "eV")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"erefmax",varadr(erefmax),0,Quote(double precision),
Quote(scalar), "eV")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"delekpt",varadr(delekpt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dkpt) )
      i0001234=rtvare(drtdm,"dkpt",i000addr,1,Quote(_double precision),
Quote((mpd)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rldmin",varadr(rldmin),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rldmax",varadr(rldmax),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"drefmin",varadr(drefmin),0,Quote(double precision),
Quote(scalar), "/m**3")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"drefmax",varadr(drefmax),0,Quote(double precision),
Quote(scalar), "/m**3")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"deldkpt",varadr(deldkpt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"taumin",varadr(taumin),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"taumax",varadr(taumax),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"deltau",varadr(deltau),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Rtfcn")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "rsa",jgrp,Quote(double precision),"m**3/sec")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(k:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rra",jgrp,Quote(double precision),"m**3/sec")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(k:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rcx",jgrp,Quote(double precision),"m**3/sec")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t0:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(n0:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(k:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rqa",jgrp,Quote(double precision),"J*m**3/sec")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(k:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "erl1",jgrp,Quote(double precision),"J/sec")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "erl2",jgrp,Quote(double precision),"J/sec")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "svdiss",jgrp,Quote(double precision),"m**3/s")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readrt",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readeh",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readnw",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readehr1",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readehr2",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Aphwrk")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nxdata",varadr(nxdata),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nydata",varadr(nydata),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xdata) )
      i0001234=rtvare(drtdm,"xdata",i000addr,1,Quote(_double precision),
Quote((1:nxdata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ydata) )
      i0001234=rtvare(drtdm,"ydata",i000addr,1,Quote(_double precision),
Quote((1:nydata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fdata) )
      i0001234=rtvare(drtdm,"fdata",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ldf",varadr(ldf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iflag",varadr(iflag),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kxords",varadr(kxords),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kyords",varadr(kyords),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xknots) )
      i0001234=rtvare(drtdm,"xknots",i000addr,1,Quote(_double precision),
Quote((1:nxdata+kxords)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yknots) )
      i0001234=rtvare(drtdm,"yknots",i000addr,1,Quote(_double precision),
Quote((1:nydata+kyords)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(workh) )
      i0001234=rtvare(drtdm,"workh",i000addr,1,Quote(_double precision),
Quote((1:nxdata*nydata+2*kxords*(nxdata+1))), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rsacoef) )
      i0001234=rtvare(drtdm,"rsacoef",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rracoef) )
      i0001234=rtvare(drtdm,"rracoef",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rqacoef) )
      i0001234=rtvare(drtdm,"rqacoef",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Subs")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "aphread",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      call rtsetdoc(drtdm,"aph.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine aphxpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.6) then
         call aphxp6(name1234)
      elseif(iseg.eq.8) then
         call aphxp8(name1234)
      else
         call baderr('aphxpf: impossible event')
      endif
      return
      end
      subroutine aphxp6(name1234)
      character*(*) name1234
      external aph_handler
      external [rsa]
      external [rra]
      external [rcx]
      external [rqa]
      external [erl1]
      external [erl2]
      external [svdiss]
      external [readrt]
      external [readeh]
      external [readnw]
      external [readehr1]
      external [readehr2]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'rsa') then
         call parexecf(aph_handler, 0, [rsa])
      elseif(name1234 = 'rra') then
         call parexecf(aph_handler, 1, [rra])
      elseif(name1234 = 'rcx') then
         call parexecf(aph_handler, 2, [rcx])
      elseif(name1234 = 'rqa') then
         call parexecf(aph_handler, 3, [rqa])
      elseif(name1234 = 'erl1') then
         call parexecf(aph_handler, 4, [erl1])
      elseif(name1234 = 'erl2') then
         call parexecf(aph_handler, 5, [erl2])
      elseif(name1234 = 'svdiss') then
         call parexecf(aph_handler, 6, [svdiss])
      elseif(name1234 = 'readrt') then
         call parexecf(aph_handler, 7, [readrt])
      elseif(name1234 = 'readeh') then
         call parexecf(aph_handler, 8, [readeh])
      elseif(name1234 = 'readnw') then
         call parexecf(aph_handler, 9, [readnw])
      elseif(name1234 = 'readehr1') then
         call parexecf(aph_handler, 10, [readehr1])
      elseif(name1234 = 'readehr2') then
         call parexecf(aph_handler, 11, [readehr2])
      else
         call baderr('aphxp6: impossible event: '//name5678)
      endif
      return
      end
      subroutine aphxp8(name1234)
      character*(*) name1234
      external aph_handler
      external [aphread]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'aphread') then
         call parexecf(aph_handler, 12, [aphread])
      else
         call baderr('aphxp8: impossible event: '//name5678)
      endif
      return
      end
      function aphbfcn(ss,sp,nargs,name1234,sx)
      integer aphbfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in aph')
      call baderr(name1234)
      return(ERR)
      end
