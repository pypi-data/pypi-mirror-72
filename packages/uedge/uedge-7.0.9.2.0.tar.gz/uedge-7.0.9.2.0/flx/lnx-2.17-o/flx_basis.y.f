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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/bbb_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/flx_basis.d
c     ./flx_basis.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c































































































































































      subroutine flxinit0
cProlog
c initializes a Package
      integer drtdm
      common /flxrtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("flx")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call flxdata
      call flxwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data flxiyiyi
c Replace pointer statements with Address types


c Group Dim_flx

      integer nym
      common /flx00/ nym
c End of Dim_flx

c Group Dimflx
      integer nsearch
      common /flx10/ nsearch
c End of Dimflx

c Group Flxin
      double precision dtheta_exclude(1:2), dtheta_overlap_sol(1:2)
      double precision dtheta_overlap_pf(1:2), thetax, thetamin(1:2)
      double precision thetamax(1:2), theta1fac, theta2fac, ymax1fac
      integer istchkon, isthmmxn, imagx, jmagx, iseps, jseps, icutoff1
      double precision ymax2fac, slpyt, slp2fac, slp3fac, psifac
      double precision psi0sep1, psi0sep2, psi0max_inner, psi0max_outer
      double precision psi0min2_upper, psi0min2_lower, psi0min1
      double precision psi0min2, psi0sep, psi0max, psi0lim, sfaclim
      double precision alfcy_inner, alfcy, xoverlap(2), xcutoff1
      double precision ycutoff1
      integer jcutoff1, iseqdskr, kymesh, mdsefit
      integer*8 prho
      integer*8 ptflx
      integer*8 ppsitop
      integer*8 ppsibot
      common /flx20/ istchkon, isthmmxn, imagx, jmagx, iseps, jseps
      common /flx20/ icutoff1, jcutoff1, iseqdskr, kymesh, mdsefit
      common /flx23/ dtheta_exclude, dtheta_overlap_sol
      common /flx23/ dtheta_overlap_pf, thetax, thetamin, thetamax
      common /flx23/ theta1fac, theta2fac, ymax1fac, ymax2fac, slpyt
      common /flx23/ slp2fac, slp3fac, psifac, psi0sep1, psi0sep2
      common /flx23/ psi0max_inner, psi0max_outer, psi0min2_upper
      common /flx23/ psi0min2_lower, psi0min1, psi0min2, psi0sep
      common /flx23/ psi0max, psi0lim, sfaclim, alfcy_inner, alfcy
      common /flx23/ xoverlap, xcutoff1, ycutoff1
      common /flx26/ prho, ptflx, ppsitop
      common /flx26/ ppsibot
c End of Flxin

c Group Workdn
      integer*8 ppsi0_mp_inner
      integer*8 ppsi0_mp_outer
      integer*8 ppsi0_dp_lower_inner
      integer*8 ppsi0_dp_lower_outer
      integer*8 ppsi0_dp_upper_inner
      integer*8 ppsi0_dp_upper_outer
      common /flx36/ ppsi0_mp_inner, ppsi0_mp_outer
      common /flx36/ ppsi0_dp_lower_inner
      common /flx36/ ppsi0_dp_lower_outer
      common /flx36/ ppsi0_dp_upper_inner
      common /flx36/ ppsi0_dp_upper_outer
c End of Workdn

c Group Inpf0
      integer istcvon, altsearch, isetpath
      integer*8 pplflux0
      integer*8 pncmin0
      integer*8 pncmax0
      integer*8 piserch0
      integer*8 pjserch0
      integer*8 pistepf0
      integer*8 pjstepf0
      integer*8 pxminf0
      integer*8 pxmaxf0
      integer*8 pyminf0
      integer*8 pymaxf0
      common /flx40/ istcvon, altsearch, isetpath
      common /flx46/ pplflux0, pncmin0, pncmax0
      common /flx46/ piserch0, pjserch0, pistepf0
      common /flx46/ pjstepf0, pxminf0, pxmaxf0
      common /flx46/ pyminf0, pymaxf0
c End of Inpf0

c Group Inpf
      integer ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      integer*8 piserch
      integer*8 pjserch
      integer*8 pleadir
      common /flx50/ ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      common /flx56/ piserch, pjserch, pleadir
c End of Inpf

c Group Polflx
      integer mrfac, nx4, ny4, imin, imax, istart, jmins, jmaxs, jstart
      double precision dsjumpf, pfr, twopie, xminf, xmaxf, yminf, ymaxf
      double precision rs_com, zs_com
      integer ncontr
      integer*8 pplflux
      integer*8 px
      integer*8 py
      integer*8 pf
      integer*8 pijumpf
      integer*8 pilast
      integer*8 pxcn
      integer*8 pycn
      common /flx60/ mrfac, nx4, ny4, imin, imax, istart, jmins, jmaxs
      common /flx60/ jstart, ncontr
      common /flx63/ dsjumpf, pfr, twopie, xminf, xmaxf, yminf, ymaxf
      common /flx63/ rs_com, zs_com
      common /flx66/ pplflux, px, py, pf
      common /flx66/ pijumpf, pilast, pxcn, pycn
c End of Polflx

c Group Rho
c End of Rho

c Group Efit
c End of Efit


      data nsearch/4/
      data istchkon/0/,isthmmxn/1/,dtheta_exclude/2*1.5d0/
      data dtheta_overlap_sol/2*0.5d0/,dtheta_overlap_pf/2*0.25d0/
      data theta1fac/1.0d0/,theta2fac/0.0d0/,ymax1fac/1.0d0/,ymax2fac/
     &   3.0d0/
      data slpyt/1.0d0/,slp2fac/1.0d0/,slp3fac/1.0d0/,psifac/1.0005d0/
      data psi0max_inner/1.07d0/,psi0max_outer/1.07d0/,psi0min2_upper/
     &   0.98d0/
      data psi0min2_lower/0.98d0/,psi0min1/0.98d0/,psi0min2/0.98d0/
      data psi0sep/1.00001d0/,psi0max/1.07d0/,sfaclim/1.0d0/
      data alfcy_inner/.0001d0/,alfcy/.0001d0/,xoverlap/5.0d0,4.0d0/,
     &   iseqdskr/0/
      data kymesh/1/,xcutoff1/0.d0/,ycutoff1/0.d0/,mdsefit/0/
      data istcvon/0/,altsearch/0/,isetpath/0/
      data mrfac/4/,dsjumpf/0.1d0/

      end
c restore definition from mppl.BASIS

      subroutine flxdata
cProlog

c Group Dim_flx

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd


      integer nym
      common /flx00/ nym
c End of Dim_flx

c Group Dimflx
      integer nsearch
      common /flx10/ nsearch
c End of Dimflx

c Group Flxin
      double precision dtheta_exclude(1:2), dtheta_overlap_sol(1:2)
      double precision dtheta_overlap_pf(1:2), thetax, thetamin(1:2)
      double precision thetamax(1:2), theta1fac, theta2fac, ymax1fac
      integer istchkon, isthmmxn, imagx, jmagx, iseps, jseps, icutoff1
      double precision ymax2fac, slpyt, slp2fac, slp3fac, psifac
      double precision psi0sep1, psi0sep2, psi0max_inner, psi0max_outer
      double precision psi0min2_upper, psi0min2_lower, psi0min1
      double precision psi0min2, psi0sep, psi0max, psi0lim, sfaclim
      double precision alfcy_inner, alfcy, xoverlap(2), xcutoff1
      double precision ycutoff1
      integer jcutoff1, iseqdskr, kymesh, mdsefit
      double precision rho ( 0:nym)
      pointer(prho,rho)
      double precision tflx ( 0:nym)
      pointer(ptflx,tflx)
      double precision psitop ( 1:jdim)
      pointer(ppsitop,psitop)
      double precision psibot ( 1:jdim)
      pointer(ppsibot,psibot)
      common /flx20/ istchkon, isthmmxn, imagx, jmagx, iseps, jseps
      common /flx20/ icutoff1, jcutoff1, iseqdskr, kymesh, mdsefit
      common /flx23/ dtheta_exclude, dtheta_overlap_sol
      common /flx23/ dtheta_overlap_pf, thetax, thetamin, thetamax
      common /flx23/ theta1fac, theta2fac, ymax1fac, ymax2fac, slpyt
      common /flx23/ slp2fac, slp3fac, psifac, psi0sep1, psi0sep2
      common /flx23/ psi0max_inner, psi0max_outer, psi0min2_upper
      common /flx23/ psi0min2_lower, psi0min1, psi0min2, psi0sep
      common /flx23/ psi0max, psi0lim, sfaclim, alfcy_inner, alfcy
      common /flx23/ xoverlap, xcutoff1, ycutoff1
      common /flx26/ prho, ptflx, ppsitop
      common /flx26/ ppsibot
c End of Flxin

c Group Workdn
      double precision psi0_mp_inner ( 0:nym)
      pointer(ppsi0_mp_inner,psi0_mp_inner)
      double precision psi0_mp_outer ( 0:nym)
      pointer(ppsi0_mp_outer,psi0_mp_outer)
      double precision psi0_dp_lower_inner ( 0:nym)
      pointer(ppsi0_dp_lower_inner,psi0_dp_lower_inner)
      double precision psi0_dp_lower_outer ( 0:nym)
      pointer(ppsi0_dp_lower_outer,psi0_dp_lower_outer)
      double precision psi0_dp_upper_inner ( 0:nym)
      pointer(ppsi0_dp_upper_inner,psi0_dp_upper_inner)
      double precision psi0_dp_upper_outer ( 0:nym)
      pointer(ppsi0_dp_upper_outer,psi0_dp_upper_outer)
      common /flx36/ ppsi0_mp_inner, ppsi0_mp_outer
      common /flx36/ ppsi0_dp_lower_inner
      common /flx36/ ppsi0_dp_lower_outer
      common /flx36/ ppsi0_dp_upper_inner
      common /flx36/ ppsi0_dp_upper_outer
c End of Workdn

c Group Inpf0
      integer istcvon, altsearch, isetpath
      double precision plflux0 ( jdim,nsearch)
      pointer(pplflux0,plflux0)
      integer ncmin0 ( nsearch)
      pointer(pncmin0,ncmin0)
      integer ncmax0 ( nsearch)
      pointer(pncmax0,ncmax0)
      integer iserch0 ( nsearch)
      pointer(piserch0,iserch0)
      integer jserch0 ( nsearch)
      pointer(pjserch0,jserch0)
      integer istepf0 ( nsearch)
      pointer(pistepf0,istepf0)
      integer jstepf0 ( nsearch)
      pointer(pjstepf0,jstepf0)
      double precision xminf0 ( nsearch)
      pointer(pxminf0,xminf0)
      double precision xmaxf0 ( nsearch)
      pointer(pxmaxf0,xmaxf0)
      double precision yminf0 ( nsearch)
      pointer(pyminf0,yminf0)
      double precision ymaxf0 ( nsearch)
      pointer(pymaxf0,ymaxf0)
      common /flx40/ istcvon, altsearch, isetpath
      common /flx46/ pplflux0, pncmin0, pncmax0
      common /flx46/ piserch0, pjserch0, pistepf0
      common /flx46/ pjstepf0, pxminf0, pxmaxf0
      common /flx46/ pyminf0, pymaxf0
c End of Inpf0

c Group Inpf
      integer ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      integer iserch ( jdim)
      pointer(piserch,iserch)
      integer jserch ( jdim)
      pointer(pjserch,jserch)
      integer leadir ( jdim)
      pointer(pleadir,leadir)
      common /flx50/ ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      common /flx56/ piserch, pjserch, pleadir
c End of Inpf

c Group Polflx
      integer mrfac, nx4, ny4, imin, imax, istart, jmins, jmaxs, jstart
      double precision dsjumpf, pfr, twopie, xminf, xmaxf, yminf, ymaxf
      double precision rs_com, zs_com
      integer ncontr
      double precision plflux ( jdim)
      pointer(pplflux,plflux)
      double precision x ( nx4)
      pointer(px,x)
      double precision y ( ny4)
      pointer(py,y)
      double precision f ( nx4,ny4)
      pointer(pf,f)
      integer ijumpf ( jdim)
      pointer(pijumpf,ijumpf)
      integer ilast ( jdim)
      pointer(pilast,ilast)
      double precision xcn ( npts)
      pointer(pxcn,xcn)
      double precision ycn ( npts)
      pointer(pycn,ycn)
      common /flx60/ mrfac, nx4, ny4, imin, imax, istart, jmins, jmaxs
      common /flx60/ jstart, ncontr
      common /flx63/ dsjumpf, pfr, twopie, xminf, xmaxf, yminf, ymaxf
      common /flx63/ rs_com, zs_com
      common /flx66/ pplflux, px, py, pf
      common /flx66/ pijumpf, pilast, pxcn, pycn
c End of Polflx

c Group Rho
c End of Rho

c Group Efit
c End of Efit


      external flxiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(prho)
      call clraddr(ptflx)
      call clraddr(ppsitop)
      call clraddr(ppsibot)
      call clraddr(ppsi0_mp_inner)
      call clraddr(ppsi0_mp_outer)
      call clraddr(ppsi0_dp_lower_inner)
      call clraddr(ppsi0_dp_lower_outer)
      call clraddr(ppsi0_dp_upper_inner)
      call clraddr(ppsi0_dp_upper_outer)
      call clraddr(pplflux0)
      call clraddr(pncmin0)
      call clraddr(pncmax0)
      call clraddr(piserch0)
      call clraddr(pjserch0)
      call clraddr(pistepf0)
      call clraddr(pjstepf0)
      call clraddr(pxminf0)
      call clraddr(pxmaxf0)
      call clraddr(pyminf0)
      call clraddr(pymaxf0)
      call clraddr(piserch)
      call clraddr(pjserch)
      call clraddr(pleadir)
      call clraddr(pplflux)
      call clraddr(px)
      call clraddr(py)
      call clraddr(pf)
      call clraddr(pijumpf)
      call clraddr(pilast)
      call clraddr(pxcn)
      call clraddr(pycn)

      return
      end
      subroutine flxdbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,8,125)
      return
      end
      subroutine flxwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /flxrtdm/ drtdm

c Group Dim_flx

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd


      integer nym
      common /flx00/ nym
c End of Dim_flx

c Group Dimflx
      integer nsearch
      common /flx10/ nsearch
c End of Dimflx

c Group Flxin
      double precision dtheta_exclude(1:2), dtheta_overlap_sol(1:2)
      double precision dtheta_overlap_pf(1:2), thetax, thetamin(1:2)
      double precision thetamax(1:2), theta1fac, theta2fac, ymax1fac
      integer istchkon, isthmmxn, imagx, jmagx, iseps, jseps, icutoff1
      double precision ymax2fac, slpyt, slp2fac, slp3fac, psifac
      double precision psi0sep1, psi0sep2, psi0max_inner, psi0max_outer
      double precision psi0min2_upper, psi0min2_lower, psi0min1
      double precision psi0min2, psi0sep, psi0max, psi0lim, sfaclim
      double precision alfcy_inner, alfcy, xoverlap(2), xcutoff1
      double precision ycutoff1
      integer jcutoff1, iseqdskr, kymesh, mdsefit
      double precision rho ( 0:nym)
      pointer(prho,rho)
      double precision tflx ( 0:nym)
      pointer(ptflx,tflx)
      double precision psitop ( 1:jdim)
      pointer(ppsitop,psitop)
      double precision psibot ( 1:jdim)
      pointer(ppsibot,psibot)
      common /flx20/ istchkon, isthmmxn, imagx, jmagx, iseps, jseps
      common /flx20/ icutoff1, jcutoff1, iseqdskr, kymesh, mdsefit
      common /flx23/ dtheta_exclude, dtheta_overlap_sol
      common /flx23/ dtheta_overlap_pf, thetax, thetamin, thetamax
      common /flx23/ theta1fac, theta2fac, ymax1fac, ymax2fac, slpyt
      common /flx23/ slp2fac, slp3fac, psifac, psi0sep1, psi0sep2
      common /flx23/ psi0max_inner, psi0max_outer, psi0min2_upper
      common /flx23/ psi0min2_lower, psi0min1, psi0min2, psi0sep
      common /flx23/ psi0max, psi0lim, sfaclim, alfcy_inner, alfcy
      common /flx23/ xoverlap, xcutoff1, ycutoff1
      common /flx26/ prho, ptflx, ppsitop
      common /flx26/ ppsibot
c End of Flxin

c Group Workdn
      double precision psi0_mp_inner ( 0:nym)
      pointer(ppsi0_mp_inner,psi0_mp_inner)
      double precision psi0_mp_outer ( 0:nym)
      pointer(ppsi0_mp_outer,psi0_mp_outer)
      double precision psi0_dp_lower_inner ( 0:nym)
      pointer(ppsi0_dp_lower_inner,psi0_dp_lower_inner)
      double precision psi0_dp_lower_outer ( 0:nym)
      pointer(ppsi0_dp_lower_outer,psi0_dp_lower_outer)
      double precision psi0_dp_upper_inner ( 0:nym)
      pointer(ppsi0_dp_upper_inner,psi0_dp_upper_inner)
      double precision psi0_dp_upper_outer ( 0:nym)
      pointer(ppsi0_dp_upper_outer,psi0_dp_upper_outer)
      common /flx36/ ppsi0_mp_inner, ppsi0_mp_outer
      common /flx36/ ppsi0_dp_lower_inner
      common /flx36/ ppsi0_dp_lower_outer
      common /flx36/ ppsi0_dp_upper_inner
      common /flx36/ ppsi0_dp_upper_outer
c End of Workdn

c Group Inpf0
      integer istcvon, altsearch, isetpath
      double precision plflux0 ( jdim,nsearch)
      pointer(pplflux0,plflux0)
      integer ncmin0 ( nsearch)
      pointer(pncmin0,ncmin0)
      integer ncmax0 ( nsearch)
      pointer(pncmax0,ncmax0)
      integer iserch0 ( nsearch)
      pointer(piserch0,iserch0)
      integer jserch0 ( nsearch)
      pointer(pjserch0,jserch0)
      integer istepf0 ( nsearch)
      pointer(pistepf0,istepf0)
      integer jstepf0 ( nsearch)
      pointer(pjstepf0,jstepf0)
      double precision xminf0 ( nsearch)
      pointer(pxminf0,xminf0)
      double precision xmaxf0 ( nsearch)
      pointer(pxmaxf0,xmaxf0)
      double precision yminf0 ( nsearch)
      pointer(pyminf0,yminf0)
      double precision ymaxf0 ( nsearch)
      pointer(pymaxf0,ymaxf0)
      common /flx40/ istcvon, altsearch, isetpath
      common /flx46/ pplflux0, pncmin0, pncmax0
      common /flx46/ piserch0, pjserch0, pistepf0
      common /flx46/ pjstepf0, pxminf0, pxmaxf0
      common /flx46/ pyminf0, pymaxf0
c End of Inpf0

c Group Inpf
      integer ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      integer iserch ( jdim)
      pointer(piserch,iserch)
      integer jserch ( jdim)
      pointer(pjserch,jserch)
      integer leadir ( jdim)
      pointer(pleadir,leadir)
      common /flx50/ ncmin, ncmax, istepf, jstepf, ncmin1, ncmax1
      common /flx56/ piserch, pjserch, pleadir
c End of Inpf

c Group Polflx
      integer mrfac, nx4, ny4, imin, imax, istart, jmins, jmaxs, jstart
      double precision dsjumpf, pfr, twopie, xminf, xmaxf, yminf, ymaxf
      double precision rs_com, zs_com
      integer ncontr
      double precision plflux ( jdim)
      pointer(pplflux,plflux)
      double precision x ( nx4)
      pointer(px,x)
      double precision y ( ny4)
      pointer(py,y)
      double precision f ( nx4,ny4)
      pointer(pf,f)
      integer ijumpf ( jdim)
      pointer(pijumpf,ijumpf)
      integer ilast ( jdim)
      pointer(pilast,ilast)
      double precision xcn ( npts)
      pointer(pxcn,xcn)
      double precision ycn ( npts)
      pointer(pycn,ycn)
      common /flx60/ mrfac, nx4, ny4, imin, imax, istart, jmins, jmaxs
      common /flx60/ jstart, ncontr
      common /flx63/ dsjumpf, pfr, twopie, xminf, xmaxf, yminf, ymaxf
      common /flx63/ rs_com, zs_com
      common /flx66/ pplflux, px, py, pf
      common /flx66/ pijumpf, pilast, pxcn, pycn
c End of Polflx

c Group Rho
c End of Rho

c Group Efit
c End of Efit



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call flxdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Dimflx")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nsearch",varadr(nsearch),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Flxin")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istchkon",varadr(istchkon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isthmmxn",varadr(isthmmxn),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( dtheta_exclude )
      i0001234=rtvare(drtdm,"dtheta_exclude",i000addr,0,
     &   'double precision','(1:2)', "radians")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( dtheta_overlap_sol )
      i0001234=rtvare(drtdm,"dtheta_overlap_sol",i000addr,0,
     &   'double precision','(1:2)', "radians")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( dtheta_overlap_pf )
      i0001234=rtvare(drtdm,"dtheta_overlap_pf",i000addr,0,
     &   'double precision','(1:2)', "radians")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"thetax",varadr(thetax),0,'double precision'
     &   ,'scalar', "radians")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( thetamin )
      i0001234=rtvare(drtdm,"thetamin",i000addr,0,'double precision',
     &   '(1:2)', "radians")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( thetamax )
      i0001234=rtvare(drtdm,"thetamax",i000addr,0,'double precision',
     &   '(1:2)', "radians")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"theta1fac",varadr(theta1fac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"theta2fac",varadr(theta2fac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ymax1fac",varadr(ymax1fac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ymax2fac",varadr(ymax2fac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"imagx",varadr(imagx),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jmagx",varadr(jmagx),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iseps",varadr(iseps),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jseps",varadr(jseps),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"icutoff1",varadr(icutoff1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jcutoff1",varadr(jcutoff1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slpyt",varadr(slpyt),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slp2fac",varadr(slp2fac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"slp3fac",varadr(slp3fac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"psifac",varadr(psifac),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"psi0sep1",varadr(psi0sep1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"psi0sep2",varadr(psi0sep2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"psi0max_inner",varadr(psi0max_inner),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0max_outer",varadr(psi0max_outer),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0min2_upper",varadr(psi0min2_upper),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0min2_lower",varadr(psi0min2_lower),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0min1",varadr(psi0min1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0min2",varadr(psi0min2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0sep",varadr(psi0sep),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0max",varadr(psi0max),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"psi0lim",varadr(psi0lim),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sfaclim",varadr(sfaclim),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"alfcy_inner",varadr(alfcy_inner),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"alfcy",varadr(alfcy),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i000addr = varadr ( xoverlap )
      i0001234=rtvare(drtdm,"xoverlap",i000addr,0,'double precision',
     &   '(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prho )
      i0001234=rtvare(drtdm,"rho",i000addr,1,'double precision',
     &   '(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptflx )
      i0001234=rtvare(drtdm,"tflx",i000addr,1,'double precision',
     &   '(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsitop )
      i0001234=rtvare(drtdm,"psitop",i000addr,1,'double precision',
     &   '(1:jdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsibot )
      i0001234=rtvare(drtdm,"psibot",i000addr,1,'double precision',
     &   '(1:jdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iseqdskr",varadr(iseqdskr),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kymesh",varadr(kymesh),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xcutoff1",varadr(xcutoff1),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ycutoff1",varadr(ycutoff1),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mdsefit",varadr(mdsefit),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Workdn")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( ppsi0_mp_inner )
      i0001234=rtvare(drtdm,"psi0_mp_inner",i000addr,1,
     &   'double precision','(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsi0_mp_outer )
      i0001234=rtvare(drtdm,"psi0_mp_outer",i000addr,1,
     &   'double precision','(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsi0_dp_lower_inner )
      i0001234=rtvare(drtdm,"psi0_dp_lower_inner",i000addr,1,
     &   'double precision','(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsi0_dp_lower_outer )
      i0001234=rtvare(drtdm,"psi0_dp_lower_outer",i000addr,1,
     &   'double precision','(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsi0_dp_upper_inner )
      i0001234=rtvare(drtdm,"psi0_dp_upper_inner",i000addr,1,
     &   'double precision','(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsi0_dp_upper_outer )
      i0001234=rtvare(drtdm,"psi0_dp_upper_outer",i000addr,1,
     &   'double precision','(0:nym)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Inpf0")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pplflux0 )
      i0001234=rtvare(drtdm,"plflux0",i000addr,1,'double precision',
     &   '(jdim,nsearch)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pncmin0 )
      i0001234=rtvare(drtdm,"ncmin0",i000addr,1,'integer','(nsearch)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pncmax0 )
      i0001234=rtvare(drtdm,"ncmax0",i000addr,1,'integer','(nsearch)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piserch0 )
      i0001234=rtvare(drtdm,"iserch0",i000addr,1,'integer','(nsearch)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pjserch0 )
      i0001234=rtvare(drtdm,"jserch0",i000addr,1,'integer','(nsearch)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pistepf0 )
      i0001234=rtvare(drtdm,"istepf0",i000addr,1,'integer','(nsearch)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pjstepf0 )
      i0001234=rtvare(drtdm,"jstepf0",i000addr,1,'integer','(nsearch)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxminf0 )
      i0001234=rtvare(drtdm,"xminf0",i000addr,1,'double precision',
     &   '(nsearch)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxmaxf0 )
      i0001234=rtvare(drtdm,"xmaxf0",i000addr,1,'double precision',
     &   '(nsearch)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyminf0 )
      i0001234=rtvare(drtdm,"yminf0",i000addr,1,'double precision',
     &   '(nsearch)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pymaxf0 )
      i0001234=rtvare(drtdm,"ymaxf0",i000addr,1,'double precision',
     &   '(nsearch)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istcvon",varadr(istcvon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"altsearch",varadr(altsearch),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isetpath",varadr(isetpath),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Inpf")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncmin",varadr(ncmin),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncmax",varadr(ncmax),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piserch )
      i0001234=rtvare(drtdm,"iserch",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pjserch )
      i0001234=rtvare(drtdm,"jserch",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istepf",varadr(istepf),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jstepf",varadr(jstepf),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pleadir )
      i0001234=rtvare(drtdm,"leadir",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncmin1",varadr(ncmin1),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncmax1",varadr(ncmax1),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Polflx")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pplflux )
      i0001234=rtvare(drtdm,"plflux",i000addr,1,'double precision',
     &   '(jdim)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mrfac",varadr(mrfac),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nx4",varadr(nx4),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ny4",varadr(ny4),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( px )
      i0001234=rtvare(drtdm,"x",i000addr,1,'double precision','(nx4)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( py )
      i0001234=rtvare(drtdm,"y",i000addr,1,'double precision','(ny4)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pf )
      i0001234=rtvare(drtdm,"f",i000addr,1,'double precision',
     &   '(nx4,ny4)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pijumpf )
      i0001234=rtvare(drtdm,"ijumpf",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dsjumpf",varadr(dsjumpf),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pilast )
      i0001234=rtvare(drtdm,"ilast",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcn )
      i0001234=rtvare(drtdm,"xcn",i000addr,1,'double precision','(npts)'
     &   , "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pycn )
      i0001234=rtvare(drtdm,"ycn",i000addr,1,'double precision','(npts)'
     &   , "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"imin",varadr(imin),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"imax",varadr(imax),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istart",varadr(istart),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jmins",varadr(jmins),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jmaxs",varadr(jmaxs),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jstart",varadr(jstart),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncontr",varadr(ncontr),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"pfr",varadr(pfr),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"twopie",varadr(twopie),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xminf",varadr(xminf),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xmaxf",varadr(xmaxf),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"yminf",varadr(yminf),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ymaxf",varadr(ymaxf),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rs_com",varadr(rs_com),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zs_com",varadr(zs_com),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Rho")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho1",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'alf:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho1dn",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't4:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r4:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'alf:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho2dn",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't4:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r4:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fac:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho3dn",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't4:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r4:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'slp2fac:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'slp3fac:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2p:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3p:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho1l",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1p:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho1r",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2p:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho2",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho3",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho4",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 's2:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rho5",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rho:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'nt:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r1:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r3:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r2p:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Efit")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "aeqdsk",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "neqdsk",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readefit",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "procefit",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "refine",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "contours",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ns:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "flxrun",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "flxfin",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "inflx",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "theta_ok",jgrp,'logical',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'z:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'n:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "efitvers",jgrp,'integer',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'vmonth:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'vday:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'vyear:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "findstrike",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'js:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'rs:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'zs:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"flx_basis.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine flxxpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.7) then
         call flxxp7(name1234)
      elseif (iseg.eq.8) then
         call flxxp8(name1234)
      else
         call baderr('flxxpf: impossible event')
      endif
      return
      end
      subroutine flxxp7(name1234)
cProlog
      character*(*) name1234
      external flx_handler
      external rho1
      external rho1dn
      external rho2dn
      external rho3dn
      external rho1l
      external rho1r
      external rho2
      external rho3
      external rho4
      external rho5
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'rho1') then
         call parexecf(flx_handler, 0, rho1)
      elseif (name1234 .eq. 'rho1dn') then
         call parexecf(flx_handler, 1, rho1dn)
      elseif (name1234 .eq. 'rho2dn') then
         call parexecf(flx_handler, 2, rho2dn)
      elseif (name1234 .eq. 'rho3dn') then
         call parexecf(flx_handler, 3, rho3dn)
      elseif (name1234 .eq. 'rho1l') then
         call parexecf(flx_handler, 4, rho1l)
      elseif (name1234 .eq. 'rho1r') then
         call parexecf(flx_handler, 5, rho1r)
      elseif (name1234 .eq. 'rho2') then
         call parexecf(flx_handler, 6, rho2)
      elseif (name1234 .eq. 'rho3') then
         call parexecf(flx_handler, 7, rho3)
      elseif (name1234 .eq. 'rho4') then
         call parexecf(flx_handler, 8, rho4)
      elseif (name1234 .eq. 'rho5') then
         call parexecf(flx_handler, 9, rho5)
      else
         call baderr('flxxp7: impossible event: '//name5678)
      endif
      return
      end
      subroutine flxxp8(name1234)
cProlog
      character*(*) name1234
      external flx_handler
      external aeqdsk
      external neqdsk
      external readefit
      external procefit
      external refine
      external contours
      external flxrun
      external flxfin
      external inflx
      external theta_ok
      external efitvers
      external findstrike
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'aeqdsk') then
         call parexecf(flx_handler, 10, aeqdsk)
      elseif (name1234 .eq. 'neqdsk') then
         call parexecf(flx_handler, 11, neqdsk)
      elseif (name1234 .eq. 'readefit') then
         call parexecf(flx_handler, 12, readefit)
      elseif (name1234 .eq. 'procefit') then
         call parexecf(flx_handler, 13, procefit)
      elseif (name1234 .eq. 'refine') then
         call parexecf(flx_handler, 14, refine)
      elseif (name1234 .eq. 'contours') then
         call parexecf(flx_handler, 15, contours)
      elseif (name1234 .eq. 'flxrun') then
         call parexecf(flx_handler, 16, flxrun)
      elseif (name1234 .eq. 'flxfin') then
         call parexecf(flx_handler, 17, flxfin)
      elseif (name1234 .eq. 'inflx') then
         call parexecf(flx_handler, 18, inflx)
      elseif (name1234 .eq. 'theta_ok') then
         call parexecf(flx_handler, 19, theta_ok)
      elseif (name1234 .eq. 'efitvers') then
         call parexecf(flx_handler, 20, efitvers)
      elseif (name1234 .eq. 'findstrike') then
         call parexecf(flx_handler, 21, findstrike)
      else
         call baderr('flxxp8: impossible event: '//name5678)
      endif
      return
      end
      function flxbfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer flxbfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in flx')
      call baderr(name1234)
      flxbfcn = -1
      return
      end
