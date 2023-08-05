      subroutine svrinit0
c initializes a Package
      integer drtdm
      common /svrrtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("svr")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call svrdata
      call svrwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_svr],[
Use(UOA_routines)
Use(UOA)
])
      block data svriyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_svr
      data n_uoa/0/,npt_uoa/0/,m_uoa/0/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine svrdata
Use_All_Groups_svr
      external svriyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(x_uoa))
      call clraddr(Point(w_uoa))

      return
       end
      subroutine svrdbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,2,10)
      return
       end
      subroutine svrwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /svrrtdm/ drtdm
Use_All_Groups_svr

      Address i000addr
      external varadr
      Address varadr


      call svrdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"UOA_routines")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "xnewuoa",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(n:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(npt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(x:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rhobeg:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rhoend:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(maxfun:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iprint:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"UOA")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"n_uoa",varadr(n_uoa),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npt_uoa",varadr(npt_uoa),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rhobeg_uoa",varadr(rhobeg_uoa),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rhoend_uoa",varadr(rhoend_uoa),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rho_uoa",varadr(rho_uoa),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"m_uoa",varadr(m_uoa),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"f_uoa",varadr(f_uoa),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(x_uoa) )
      i0001234=rtvare(drtdm,"x_uoa",i000addr,1,Quote(_double precision),
Quote((n_uoa)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(w_uoa) )
      i0001234=rtvare(drtdm,"w_uoa",i000addr,1,Quote(_double precision),
Quote((m_uoa)), "none")
      if(i0001234 = 0) go to 999
      call rtsetdoc(drtdm,"svr.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine svrxpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.1) then
         call svrxp1(name1234)
      else
         call baderr('svrxpf: impossible event')
      endif
      return
      end
      subroutine svrxp1(name1234)
      character*(*) name1234
      external svr_handler
      external [xnewuoa]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'xnewuoa') then
         call parexecf(svr_handler, 0, [xnewuoa])
      else
         call baderr('svrxp1: impossible event: '//name5678)
      endif
      return
      end
      function svrbfcn(ss,sp,nargs,name1234,sx)
      integer svrbfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in svr')
      call baderr(name1234)
      return(ERR)
      end
