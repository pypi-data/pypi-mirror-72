      subroutine flxinit0
c initializes a Package
      integer drtdm
      common /flxrtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("flx")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call flxdata
      call flxwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_flx],[
Use(Dim_flx)
Use(Dimflx)
Use(Flxin)
Use(Workdn)
Use(Inpf0)
Use(Inpf)
Use(Polflx)
Use(Rho)
Use(Efit)
])
      block data flxiyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_flx
      data nsearch/NSEARCH/
      data istchkon/0/,isthmmxn/1/,dtheta_exclude/2*1.5/
      data dtheta_overlap_sol/2*0.5/,dtheta_overlap_pf/2*0.25/
      data theta1fac/1.0/,theta2fac/0.0/,ymax1fac/1.0/,ymax2fac/3.0/
      data slpyt/1.0/,slp2fac/1.0/,slp3fac/1.0/,psifac/1.0005/
      data psi0max_inner/1.07/,psi0max_outer/1.07/,psi0min2_upper/0.98/
      data psi0min2_lower/0.98/,psi0min1/0.98/,psi0min2/0.98/
      data psi0sep/1.00001/,psi0max/1.07/,sfaclim/1.0/
      data alfcy_inner/.0001/,alfcy/.0001/,xoverlap/5.0,4.0/,iseqdskr/0/
      data kymesh/1/,xcutoff1/0./,ycutoff1/0./,mdsefit/0/
      data istcvon/0/,altsearch/0/,isetpath/0/
      data mrfac/4/,dsjumpf/0.1/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine flxdata
Use_All_Groups_flx
      external flxiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(rho))
      call clraddr(Point(tflx))
      call clraddr(Point(psitop))
      call clraddr(Point(psibot))
      call clraddr(Point(psi0_mp_inner))
      call clraddr(Point(psi0_mp_outer))
      call clraddr(Point(psi0_dp_lower_inner))
      call clraddr(Point(psi0_dp_lower_outer))
      call clraddr(Point(psi0_dp_upper_inner))
      call clraddr(Point(psi0_dp_upper_outer))
      call clraddr(Point(plflux0))
      call clraddr(Point(ncmin0))
      call clraddr(Point(ncmax0))
      call clraddr(Point(iserch0))
      call clraddr(Point(jserch0))
      call clraddr(Point(istepf0))
      call clraddr(Point(jstepf0))
      call clraddr(Point(xminf0))
      call clraddr(Point(xmaxf0))
      call clraddr(Point(yminf0))
      call clraddr(Point(ymaxf0))
      call clraddr(Point(iserch))
      call clraddr(Point(jserch))
      call clraddr(Point(leadir))
      call clraddr(Point(plflux))
      call clraddr(Point(x))
      call clraddr(Point(y))
      call clraddr(Point(f))
      call clraddr(Point(ijumpf))
      call clraddr(Point(ilast))
      call clraddr(Point(xcn))
      call clraddr(Point(ycn))

      return
       end
      subroutine flxdbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,8,125)
      return
       end
      subroutine flxwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /flxrtdm/ drtdm
Use_All_Groups_flx

      Address i000addr
      external varadr
      Address varadr


      call flxdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Dimflx")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nsearch",varadr(nsearch),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Flxin")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"istchkon",varadr(istchkon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isthmmxn",varadr(isthmmxn),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( dtheta_exclude )
      i0001234=rtvare(drtdm,"dtheta_exclude",i000addr,0,Quote(double precision),
Quote((1:2)), "radians")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( dtheta_overlap_sol )
      i0001234=rtvare(drtdm,"dtheta_overlap_sol",i000addr,0,Quote(double precision),
Quote((1:2)), "radians")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( dtheta_overlap_pf )
      i0001234=rtvare(drtdm,"dtheta_overlap_pf",i000addr,0,Quote(double precision),
Quote((1:2)), "radians")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"thetax",varadr(thetax),0,Quote(double precision),
Quote(scalar), "radians")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( thetamin )
      i0001234=rtvare(drtdm,"thetamin",i000addr,0,Quote(double precision),
Quote((1:2)), "radians")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( thetamax )
      i0001234=rtvare(drtdm,"thetamax",i000addr,0,Quote(double precision),
Quote((1:2)), "radians")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"theta1fac",varadr(theta1fac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"theta2fac",varadr(theta2fac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ymax1fac",varadr(ymax1fac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ymax2fac",varadr(ymax2fac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"imagx",varadr(imagx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jmagx",varadr(jmagx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iseps",varadr(iseps),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jseps",varadr(jseps),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"icutoff1",varadr(icutoff1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jcutoff1",varadr(jcutoff1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slpyt",varadr(slpyt),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slp2fac",varadr(slp2fac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"slp3fac",varadr(slp3fac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"psifac",varadr(psifac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"psi0sep1",varadr(psi0sep1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"psi0sep2",varadr(psi0sep2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"psi0max_inner",varadr(psi0max_inner),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0max_outer",varadr(psi0max_outer),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0min2_upper",varadr(psi0min2_upper),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0min2_lower",varadr(psi0min2_lower),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0min1",varadr(psi0min1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0min2",varadr(psi0min2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0sep",varadr(psi0sep),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0max",varadr(psi0max),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"psi0lim",varadr(psi0lim),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sfaclim",varadr(sfaclim),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"alfcy_inner",varadr(alfcy_inner),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"alfcy",varadr(alfcy),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i000addr = varadr ( xoverlap )
      i0001234=rtvare(drtdm,"xoverlap",i000addr,0,Quote(double precision),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rho) )
      i0001234=rtvare(drtdm,"rho",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tflx) )
      i0001234=rtvare(drtdm,"tflx",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psitop) )
      i0001234=rtvare(drtdm,"psitop",i000addr,1,Quote(_double precision),
Quote((1:jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psibot) )
      i0001234=rtvare(drtdm,"psibot",i000addr,1,Quote(_double precision),
Quote((1:jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iseqdskr",varadr(iseqdskr),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kymesh",varadr(kymesh),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xcutoff1",varadr(xcutoff1),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ycutoff1",varadr(ycutoff1),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mdsefit",varadr(mdsefit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Workdn")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(psi0_mp_inner) )
      i0001234=rtvare(drtdm,"psi0_mp_inner",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psi0_mp_outer) )
      i0001234=rtvare(drtdm,"psi0_mp_outer",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psi0_dp_lower_inner) )
      i0001234=rtvare(drtdm,"psi0_dp_lower_inner",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psi0_dp_lower_outer) )
      i0001234=rtvare(drtdm,"psi0_dp_lower_outer",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psi0_dp_upper_inner) )
      i0001234=rtvare(drtdm,"psi0_dp_upper_inner",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psi0_dp_upper_outer) )
      i0001234=rtvare(drtdm,"psi0_dp_upper_outer",i000addr,1,Quote(_double precision),
Quote((0:nym)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Inpf0")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(plflux0) )
      i0001234=rtvare(drtdm,"plflux0",i000addr,1,Quote(_double precision),
Quote((jdim,nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ncmin0) )
      i0001234=rtvare(drtdm,"ncmin0",i000addr,1,Quote(_integer),
Quote((nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ncmax0) )
      i0001234=rtvare(drtdm,"ncmax0",i000addr,1,Quote(_integer),
Quote((nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iserch0) )
      i0001234=rtvare(drtdm,"iserch0",i000addr,1,Quote(_integer),
Quote((nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(jserch0) )
      i0001234=rtvare(drtdm,"jserch0",i000addr,1,Quote(_integer),
Quote((nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(istepf0) )
      i0001234=rtvare(drtdm,"istepf0",i000addr,1,Quote(_integer),
Quote((nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(jstepf0) )
      i0001234=rtvare(drtdm,"jstepf0",i000addr,1,Quote(_integer),
Quote((nsearch)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xminf0) )
      i0001234=rtvare(drtdm,"xminf0",i000addr,1,Quote(_double precision),
Quote((nsearch)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xmaxf0) )
      i0001234=rtvare(drtdm,"xmaxf0",i000addr,1,Quote(_double precision),
Quote((nsearch)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yminf0) )
      i0001234=rtvare(drtdm,"yminf0",i000addr,1,Quote(_double precision),
Quote((nsearch)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ymaxf0) )
      i0001234=rtvare(drtdm,"ymaxf0",i000addr,1,Quote(_double precision),
Quote((nsearch)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"istcvon",varadr(istcvon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"altsearch",varadr(altsearch),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isetpath",varadr(isetpath),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Inpf")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ncmin",varadr(ncmin),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncmax",varadr(ncmax),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iserch) )
      i0001234=rtvare(drtdm,"iserch",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(jserch) )
      i0001234=rtvare(drtdm,"jserch",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"istepf",varadr(istepf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jstepf",varadr(jstepf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(leadir) )
      i0001234=rtvare(drtdm,"leadir",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncmin1",varadr(ncmin1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncmax1",varadr(ncmax1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Polflx")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(plflux) )
      i0001234=rtvare(drtdm,"plflux",i000addr,1,Quote(_double precision),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mrfac",varadr(mrfac),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nx4",varadr(nx4),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ny4",varadr(ny4),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(x) )
      i0001234=rtvare(drtdm,"x",i000addr,1,Quote(_double precision),
Quote((nx4)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(y) )
      i0001234=rtvare(drtdm,"y",i000addr,1,Quote(_double precision),
Quote((ny4)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(f) )
      i0001234=rtvare(drtdm,"f",i000addr,1,Quote(_double precision),
Quote((nx4,ny4)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ijumpf) )
      i0001234=rtvare(drtdm,"ijumpf",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dsjumpf",varadr(dsjumpf),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ilast) )
      i0001234=rtvare(drtdm,"ilast",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcn) )
      i0001234=rtvare(drtdm,"xcn",i000addr,1,Quote(_double precision),
Quote((npts)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ycn) )
      i0001234=rtvare(drtdm,"ycn",i000addr,1,Quote(_double precision),
Quote((npts)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"imin",varadr(imin),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"imax",varadr(imax),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"istart",varadr(istart),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jmins",varadr(jmins),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jmaxs",varadr(jmaxs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jstart",varadr(jstart),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncontr",varadr(ncontr),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"pfr",varadr(pfr),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"twopie",varadr(twopie),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xminf",varadr(xminf),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xmaxf",varadr(xmaxf),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"yminf",varadr(yminf),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ymaxf",varadr(ymaxf),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rs_com",varadr(rs_com),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zs_com",varadr(zs_com),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Rho")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "rho1",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(alf:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho1dn",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t4:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r4:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(alf:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho2dn",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t4:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r4:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fac:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho3dn",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t4:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r4:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(slp2fac:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(slp3fac:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2p:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3p:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho1l",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1p:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho1r",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2p:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho2",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho3",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho4",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(s2:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rho5",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rho:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(t3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r3:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r2p:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Efit")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "aeqdsk",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "neqdsk",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readefit",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "procefit",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "refine",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "contours",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ns:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "flxrun",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "flxfin",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "inflx",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "theta_ok",jgrp,Quote(logical),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(r:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(z:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(n:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "efitvers",jgrp,Quote(integer),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(vmonth:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(vday:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(vyear:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "findstrike",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(js:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rs:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(zs:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      call rtsetdoc(drtdm,"flx_basis.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine flxxpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.7) then
         call flxxp7(name1234)
      elseif(iseg.eq.8) then
         call flxxp8(name1234)
      else
         call baderr('flxxpf: impossible event')
      endif
      return
      end
      subroutine flxxp7(name1234)
      character*(*) name1234
      external flx_handler
      external [rho1]
      external [rho1dn]
      external [rho2dn]
      external [rho3dn]
      external [rho1l]
      external [rho1r]
      external [rho2]
      external [rho3]
      external [rho4]
      external [rho5]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'rho1') then
         call parexecf(flx_handler, 0, [rho1])
      elseif(name1234 = 'rho1dn') then
         call parexecf(flx_handler, 1, [rho1dn])
      elseif(name1234 = 'rho2dn') then
         call parexecf(flx_handler, 2, [rho2dn])
      elseif(name1234 = 'rho3dn') then
         call parexecf(flx_handler, 3, [rho3dn])
      elseif(name1234 = 'rho1l') then
         call parexecf(flx_handler, 4, [rho1l])
      elseif(name1234 = 'rho1r') then
         call parexecf(flx_handler, 5, [rho1r])
      elseif(name1234 = 'rho2') then
         call parexecf(flx_handler, 6, [rho2])
      elseif(name1234 = 'rho3') then
         call parexecf(flx_handler, 7, [rho3])
      elseif(name1234 = 'rho4') then
         call parexecf(flx_handler, 8, [rho4])
      elseif(name1234 = 'rho5') then
         call parexecf(flx_handler, 9, [rho5])
      else
         call baderr('flxxp7: impossible event: '//name5678)
      endif
      return
      end
      subroutine flxxp8(name1234)
      character*(*) name1234
      external flx_handler
      external [aeqdsk]
      external [neqdsk]
      external [readefit]
      external [procefit]
      external [refine]
      external [contours]
      external [flxrun]
      external [flxfin]
      external [inflx]
      external [theta_ok]
      external [efitvers]
      external [findstrike]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'aeqdsk') then
         call parexecf(flx_handler, 10, [aeqdsk])
      elseif(name1234 = 'neqdsk') then
         call parexecf(flx_handler, 11, [neqdsk])
      elseif(name1234 = 'readefit') then
         call parexecf(flx_handler, 12, [readefit])
      elseif(name1234 = 'procefit') then
         call parexecf(flx_handler, 13, [procefit])
      elseif(name1234 = 'refine') then
         call parexecf(flx_handler, 14, [refine])
      elseif(name1234 = 'contours') then
         call parexecf(flx_handler, 15, [contours])
      elseif(name1234 = 'flxrun') then
         call parexecf(flx_handler, 16, [flxrun])
      elseif(name1234 = 'flxfin') then
         call parexecf(flx_handler, 17, [flxfin])
      elseif(name1234 = 'inflx') then
         call parexecf(flx_handler, 18, [inflx])
      elseif(name1234 = 'theta_ok') then
         call parexecf(flx_handler, 19, [theta_ok])
      elseif(name1234 = 'efitvers') then
         call parexecf(flx_handler, 20, [efitvers])
      elseif(name1234 = 'findstrike') then
         call parexecf(flx_handler, 21, [findstrike])
      else
         call baderr('flxxp8: impossible event: '//name5678)
      endif
      return
      end
      function flxbfcn(ss,sp,nargs,name1234,sx)
      integer flxbfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in flx')
      call baderr(name1234)
      return(ERR)
      end
