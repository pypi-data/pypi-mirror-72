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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/svr.d
c     ./svr.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c












































      subroutine svrinit0
cProlog
c initializes a Package
      integer drtdm
      common /svrrtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("svr")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call svrdata
      call svrwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data svriyiyi
c Replace pointer statements with Address types


c Group UOA_routines
c End of UOA_routines

c Group UOA
      double precision rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      integer n_uoa, npt_uoa, m_uoa
      integer*8 px_uoa
      integer*8 pw_uoa
      common /svr10/ n_uoa, npt_uoa, m_uoa
      common /svr13/ rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      common /svr16/ px_uoa, pw_uoa
c End of UOA


      data n_uoa/0/,npt_uoa/0/,m_uoa/0/

      end
c restore definition from mppl.BASIS

      subroutine svrdata
cProlog

c Group UOA_routines
c End of UOA_routines

c Group UOA
      double precision rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      integer n_uoa, npt_uoa, m_uoa
      double precision x_uoa ( n_uoa)
      pointer(px_uoa,x_uoa)
      double precision w_uoa ( m_uoa)
      pointer(pw_uoa,w_uoa)
      common /svr10/ n_uoa, npt_uoa, m_uoa
      common /svr13/ rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      common /svr16/ px_uoa, pw_uoa
c End of UOA


      external svriyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(px_uoa)
      call clraddr(pw_uoa)

      return
      end
      subroutine svrdbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,2,10)
      return
      end
      subroutine svrwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /svrrtdm/ drtdm

c Group UOA_routines
c End of UOA_routines

c Group UOA
      double precision rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      integer n_uoa, npt_uoa, m_uoa
      double precision x_uoa ( n_uoa)
      pointer(px_uoa,x_uoa)
      double precision w_uoa ( m_uoa)
      pointer(pw_uoa,w_uoa)
      common /svr10/ n_uoa, npt_uoa, m_uoa
      common /svr13/ rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      common /svr16/ px_uoa, pw_uoa
c End of UOA



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call svrdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"UOA_routines")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xnewuoa",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'n:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'npt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'x:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rhobeg:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rhoend:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'maxfun:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'iprint:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"UOA")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"n_uoa",varadr(n_uoa),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npt_uoa",varadr(npt_uoa),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rhobeg_uoa",varadr(rhobeg_uoa),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rhoend_uoa",varadr(rhoend_uoa),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rho_uoa",varadr(rho_uoa),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"m_uoa",varadr(m_uoa),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"f_uoa",varadr(f_uoa),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( px_uoa )
      i0001234=rtvare(drtdm,"x_uoa",i000addr,1,'double precision',
     &   '(n_uoa)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pw_uoa )
      i0001234=rtvare(drtdm,"w_uoa",i000addr,1,'double precision',
     &   '(m_uoa)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"svr.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine svrxpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.1) then
         call svrxp1(name1234)
      else
         call baderr('svrxpf: impossible event')
      endif
      return
      end
      subroutine svrxp1(name1234)
cProlog
      character*(*) name1234
      external svr_handler
      external xnewuoa
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'xnewuoa') then
         call parexecf(svr_handler, 0, xnewuoa)
      else
         call baderr('svrxp1: impossible event: '//name5678)
      endif
      return
      end
      function svrbfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer svrbfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in svr')
      call baderr(name1234)
      svrbfcn = -1
      return
      end
