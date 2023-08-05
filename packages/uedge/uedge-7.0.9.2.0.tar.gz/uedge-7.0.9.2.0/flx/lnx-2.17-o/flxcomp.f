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
c     ./../flxcomp.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c































































































































































c!include "../mppl.h"
c     ------------------------------------------------------------------
      subroutine flxgen
cProlog
      implicit none
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
cisfrc,ishalfm
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,npts,nxefit,nyefit,nlim
c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis

      double precision xold ( nxefit)
      pointer(pxold,xold)

      double precision yold ( nyefit)
      pointer(pyold,yold)

      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)

      double precision workk ( nxefit)
      pointer(pworkk,workk)

      double precision fpol ( nxefit)
      pointer(pfpol,fpol)

      double precision pres ( nxefit)
      pointer(ppres,pres)

      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)

      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)

      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)

      double precision xlim ( nlim)
      pointer(pxlim,xlim)

      double precision ylim ( nlim)
      pointer(pylim,ylim)

      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)

      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)

      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)

      double precision work ( nwork)
      pointer(pwork,work)

      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)

      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)

      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd
c
c Group Dimflx
      integer nsearch
      common /flx10/ nsearch
c End of Dimflx
cnsearch
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


      integer ns,kk,ll,j,n
      doubleprecision dxf,dyf
      external refine, contours, remark

c     insert a sub-grid into the EFIT mesh --
      call refine

c     *** clear the working arrays
      do 20 kk=1,jdim
         ilast(kk)=0
         npoint(kk)=0
         do 20 ll=1,npts
            xcurve(ll,kk)=0.0d0
            ycurve(ll,kk)=0.0d0
   20       continue

c     initialize the contour indexing variables
      ncmin=0
      ncmax=0

c     For each search region, call the contouring routines
      do 500 ns=1,nsearch
         if (nsearch.eq.4) then
c nycore is non-zero
            if (isfrc.eq.1 .and. ns.eq.2) then
c skip inboard half of p.f.
               continue
            elseif (isfrc.eq.1 .and. ns.eq.4) then
c skip outboard half of p.f.
               continue
            elseif (ishalfm.eq.1 .and. (ns.eq.1 .or. ns.eq.2)) then
c skip inboard half
               continue
            else
               call contours(ns)
            endif
         elseif (nsearch.eq.2) then
c nycore=0
            if (ishalfm.eq.1 .and. ns.eq.1) then
c skip inboard half
               continue
            else
               call contours(ns)
            endif
         endif
  500    continue

c     For core/p.f. contours, find the "jump" index:
      if (nycore(1) .gt. 0) then
         do 23003 j=jsptrx(1)+1,jsptrx(2)-1
            ijumpf(j)=0
            do 23005 n=1,npoint(j)-1
               dxf=xcurve(n+1,j)-xcurve(n,j)
               dyf=ycurve(n+1,j)-ycurve(n,j)
               if (sqrt(dxf**2+dyf**2) .gt. dsjumpf) then
                  ijumpf(j)=n
                  go to 23006
               endif
23005       continue
23006       continue
23003    continue
      endif

ccc   call remark("***** subroutine flxgen completed")

      return
      end

c     ------------------------------------------------------------------

      subroutine refine
cProlog
      implicit none
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,npts,nxefit,nyefit,nlim,nwork
c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis

      double precision xold ( nxefit)
      pointer(pxold,xold)

      double precision yold ( nyefit)
      pointer(pyold,yold)

      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)

      double precision workk ( nxefit)
      pointer(pworkk,workk)

      double precision fpol ( nxefit)
      pointer(pfpol,fpol)

      double precision pres ( nxefit)
      pointer(ppres,pres)

      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)

      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)

      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)

      double precision xlim ( nlim)
      pointer(pxlim,xlim)

      double precision ylim ( nlim)
      pointer(pylim,ylim)

      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)

      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)

      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)

      double precision work ( nwork)
      pointer(pwork,work)

      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)

      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)

      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd
c
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

      integer i,ix,iy,n
      doubleprecision dx,dy,frac
      doubleprecision B2VAhL
      external B2VAhL

c     This subroutine inserts a subgrid into the EFIT mesh


      frac=1/dble(mrfac)
c******* first refine the mesh in x-direction *******

      ix=0
      do 23000 i=1,nxefit-1
         dx=xold(i+1)-xold(i)
         ix=ix+1
         x(ix)=xold(i)
         do 23002 n=1,mrfac-1
            ix=ix+1
            x(ix)=xold(i)+n*frac*dx
23002    continue
23000 continue
      x(nx4)=xold(nxefit)

c******* now refine the mesh in y-direction *******

      iy=0
      do 23004 i=1,nyefit-1
         dy=yold(i+1)-yold(i)
         iy=iy+1
         y(iy)=yold(i)
         do 23006 n=1,mrfac-1
            iy=iy+1
            y(iy)=yold(i)+n*frac*dy
23006    continue
23004 continue
      y(ny4)=yold(nyefit)

c     Evaluate the spline on the refined grid --
      do 23008 ix=1,nx4
         do 23010 iy=1,ny4
            f(ix,iy) = B2VAhL (x(ix), y(iy), 0, 0, xknot, yknot, nxefit, 
     &         nyefit, kxord, kyord, bscoef, ldf, work, iflag)
23010    continue
23008 continue

      return
      end

c----------------------------------------------------------------------c

      subroutine contours(ns)
cProlog
      implicit none
      integer k, nc, i, j, ii, n, ndown, iprev, nup, nleft, nright
      doubleprecision tstval,tstvalh,tstvalv
c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,npts,nxefit,nyefit,nlim,nwork
c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis

      double precision xold ( nxefit)
      pointer(pxold,xold)

      double precision yold ( nyefit)
      pointer(pyold,yold)

      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)

      double precision workk ( nxefit)
      pointer(pworkk,workk)

      double precision fpol ( nxefit)
      pointer(pfpol,fpol)

      double precision pres ( nxefit)
      pointer(ppres,pres)

      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)

      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)

      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)

      double precision xlim ( nlim)
      pointer(pxlim,xlim)

      double precision ylim ( nlim)
      pointer(pylim,ylim)

      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)

      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)

      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)

      double precision work ( nwork)
      pointer(pwork,work)

      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)

      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)

      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd
c
c Group Dimflx
      integer nsearch
      common /flx10/ nsearch
c End of Dimflx
cnsearch
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

      integer ns
      integer right,down,left,up
      parameter(right=1,down=2,left=3,up=4)

c.....Get parameters for contour search path ns
      ncmin=ncmin0(ns)
      ncmax=ncmax0(ns)
      ncontr=ncmax-ncmin+1
      do 23000 k=1,ncontr
         plflux(k)=plflux0(k,ns)
23000 continue
      xminf=xminf0(ns)
      xmaxf=xmaxf0(ns)
      yminf=yminf0(ns)
      ymaxf=ymaxf0(ns)
c.....Start contour search at same point for all flux values
      do 23002 j=1,jdim
         iserch(j)=iserch0(ns)
         jserch(j)=jserch0(ns)
23002 continue
      istepf=istepf0(ns)
      jstepf=jstepf0(ns)


      do 17 nc=ncmin,ncmax
         pfr=plflux(nc-ncmin+1)

c........Find starting point (iserch,jserch,leadir) on each flux contour

         if (istepf.eq.0) then
c vertical search (in p.f.)
            i=iserch(nc)
            j=jserch(nc)-jstepf
   91       continue
            j=j+jstepf
            if ( (j+jstepf .lt. jmins) .or. (jmaxs .lt. j+jstepf) ) then
               write(*,*) "Error in loop 91 of subroutine contours:"
               write(*,*) "  contour psi0 = ",(pfr-simagx)/(sibdry-
     &            simagx), " not found in region ",ns
               call xerrab("")
            endif
            tstvalv=(f(i,j+jstepf)-pfr)*(f(i,j)-pfr)
c continue vertical stepping
            if (tstvalv .gt. 0) go to 91
c contour intersects vertical face between vertices (i,j) and (i,j+jstepf)
            iserch(nc)=i
c min => go up, so leadir= 1 or 3
            jserch(nc)=min(j,j+jstepf)
            if ( (ns.eq.2) .and. nsearch.eq.4 ) then
c inboard half of p.f. region
c search up; contour right, then left
               leadir(nc)=1
            elseif (ns.eq.4) then
c outboard half of p.f. region
c search up; contour left, then right
               leadir(nc)=3
            endif


         elseif (jstepf.eq.0) then
c horizontal search (in SOL)
            i=iserch(nc)-istepf
            j=jserch(nc)
   92       continue
            i=i+istepf
            if ( (i+istepf .lt. imin ) .or. (imax .lt. i+istepf) ) then
               write(*,*) "Error in loop 92 of subroutine contours:"
               write(*,*) "  contour psi0 = ",(pfr-simagx)/(sibdry-
     &            simagx), " not found in region ",ns
               call xerrab("")
            endif
            tstvalh=(f(i+istepf,j)-pfr)*(f(i,j)-pfr)
c continue horizontal stepping
            if (tstvalh .gt. 0) go to 92
c contour intersects horizontal face between vertices (i+istepf,j) and (i,j)
c min => go right, so leadir= 2 or 4
            iserch(nc)=min(i,i+istepf)
            jserch(nc)=j
            if (ns.eq.1) then
c inboard SOL
c search right; contour up, then down
               leadir(nc)=4
            elseif ( ns.eq.3 .or. ((ns.eq.2).and.(nsearch.eq.2)) ) then
c outboard SOL
c search right; contour up, then down
               leadir(nc)=4
            endif


         elseif (istepf*jstepf .ne. 0) then
c diagonal search (in p.f.)
            i=iserch(nc)-istepf
            j=jserch(nc)-jstepf
   93       continue
            i=i+istepf
            j=j+jstepf
            if ( (i+istepf .lt. imin ) .or. (imax .lt. i+istepf) .or. (j
     &         +jstepf .lt. jmins) .or. (jmaxs .lt. j+jstepf) ) then
               write(*,*) "Error in loop 93 of subroutine contours:"
               write(*,*) "  contour psi0 = ",(pfr-simagx)/(sibdry-
     &            simagx), " not found in region ",ns
               call xerrab("")
            endif
            tstval=(f(i+istepf,j+jstepf)-pfr)*(f(i,j)-pfr)
c continue diagonal stepping
            if (tstval .gt. 0.d0) go to 93
c contour intersects diagonal between vertices (i,j) and (i+istepf,j+jstepf)
            tstvalh=(f(i+istepf,j)-pfr)*(f(i,j)-pfr)
            tstvalv=(f(i,j+jstepf)-pfr)*(f(i,j)-pfr)
            if (tstvalh .lt. 0.d0) then
c contour intersects horizontal face between vertices (i,j) and (i+istepf,j)
c => go right, so leadir= 2 or 4
               iserch(nc)=min(i,i+istepf)
               jserch(nc)=j
               if ( (ns.eq.2) .and. nsearch.eq.4 ) then
c inboard half of p.f. region
c search right; contour down, then up
                  leadir(nc)=2
               elseif (ns.eq.4) then
c outboard half of p.f. region
c search right; contour up, then down
                  leadir(nc)=4
               endif
            elseif (tstvalv .lt. 0) then
c contour intersects vertical face between vertices (i,j) and (i,j+jstepf)
               iserch(nc)=i
c => go up, so leadir= 1 or 3
               jserch(nc)=min(j,j+jstepf)
               if ( (ns.eq.2) .and. nsearch.eq.4 ) then
c inboard half of p.f. region
c search up; contour right, then left
                  leadir(nc)=1
               elseif (ns.eq.4) then
c outboard half of p.f. region
c search up; contour left, then right
                  leadir(nc)=3
               endif
            else
c contour intersects vertical face at i+istepf between j and j+jstepf
c and horizontal face at j+jstepf between i and i+istepf
               iserch(nc)=i+istepf
c => go up, so leadir= 1 or 3
               jserch(nc)=min(j,j+jstepf)
               if ( (ns.eq.2) .and. nsearch.eq.4 ) then
c inboard half of p.f. region
c search up; contour right, then left
                  leadir(nc)=1
               elseif (ns.eq.4) then
c outboard half of p.f. region
c search up; contour left, then right
                  leadir(nc)=3
               endif
            endif
         endif
c end if-test on istepf and jstepf


c........Go to appropriate section for search and subsequent contouring:
         go to (140,110,130,120,150,160) leadir(nc)

  110    continue
c     ** Next is horizontal search from left to right
c     ** and contouring, down then up.
c     ** Find the first point on the "pfr" contour
         i=iserch(nc)-1
         j=jserch(nc)
c top of loop that steps horizontally to the right
  100    continue
         i=i+1
         if (i+1 .gt. imax) then
            write(*,*) "Error in section 110 of subroutine contours:"
            write(*,*) "flux contour not found on jserch ", 
     &         "between iserch and imax"
            write(*,*) "psi0 =   ",(pfr-simagx)/(sibdry-simagx)
            write(*,*) "jserch = ",jserch(nc)
            write(*,*) "iserch = ",iserch(nc)
            write(*,*) "imax =   ",imax
            call xerrab("")
         endif
         tstval=(f(i+1,j)-pfr)*(f(i,j)-pfr)
         if (tstval .gt. 0.0d0) go to 100
c     ** We know that pfr is on horiz. face between vertices (i,j) and (i+1,j)
c     ** going down
         jstart=j
         istart=i
         call go(down,n,nc,ns)
         ndown=n
         npoint(nc)=npoint(nc)+ndown
         if (n .gt. 0) then
c     ** copy xcn(1) to xcn(n) into xcurve in reverse order
            iprev=ilast(nc)
            do 23005 ii=1,n
               xcurve(iprev+ii,nc)=xcn(n-ii+1)
               ycurve(iprev+ii,nc)=ycn(n-ii+1)
               xcn(n-ii+1)=0.d0
               ycn(n-ii+1)=0.d0
23005       continue
            ilast(nc)=ilast(nc)+n
         endif
c     ** going up
         jstart=j-1
         istart=i
         call go(up,n,nc,ns)
         npoint(nc)=npoint(nc)+n
         if (n .gt. 0) then
c     ** copy xcn(1) to xcn(n) into xcurve
            iprev=ilast(nc)
            do 23007 ii=1,n
               xcurve(iprev+ii,nc)=xcn(ii)
               ycurve(iprev+ii,nc)=ycn(ii)
               xcn(ii)=0.d0
               ycn(ii)=0.d0
23007       continue
            ilast(nc)=ilast(nc)+n
         endif
         go to 17

  120    continue
c     ** Next is horizontal search from left to right
c     ** and contouring, up then down
c     ** Find the first point on the "pfr" contour
         i=iserch(nc)-1
         j=jserch(nc)
c top of loop that steps horizontally to the right
  200    continue
         i=i+1
         if (i+1 .gt. imax) then
            write(*,*) "Error in section 120 of subroutine contours:"
            write(*,*) "flux contour not found on jserch", 
     &         "between iserch and imax"
            write(*,*) "psi0 =   ",(pfr-simagx)/(sibdry-simagx)
            write(*,*) "jserch = ",jserch(nc)
            write(*,*) "iserch = ",iserch(nc)
            write(*,*) "imax =   ",imax
            call xerrab("")
         endif
         tstval=(f(i+1,j)-pfr)*(f(i,j)-pfr)
         if (tstval .gt. 0.0d0) go to 200
c     ** We know that pfr is on horiz. face between vertices (i,j) and (i+1,j)
c     ** going up
         jstart=j-1
         istart=i
         call go(up,n,nc,ns)
         nup=n
         npoint(nc)=npoint(nc)+nup
         if (n .gt. 0) then
c     ** copy xcn(1) to xcn(n) into xcurve in reverse order
            iprev=ilast(nc)
            do 23009 ii=1,n
               xcurve(iprev+ii,nc)=xcn(n-ii+1)
               ycurve(iprev+ii,nc)=ycn(n-ii+1)
               xcn(n-ii+1)=0.d0
               ycn(n-ii+1)=0.d0
23009       continue
            ilast(nc)=ilast(nc)+n
         endif
c     ** going down
         jstart=j
         istart=i
         call go(down,n,nc,ns)
         npoint(nc)=npoint(nc)+n
         if (n .gt. 0) then
c     ** copy xcn(1) to xcn(n) into xcurve
            iprev=ilast(nc)
            do 23011 ii=1,n
               xcurve(iprev+ii,nc)=xcn(ii)
               ycurve(iprev+ii,nc)=ycn(ii)
               xcn(ii)=0.d0
               ycn(ii)=0.d0
23011       continue
            ilast(nc)=ilast(nc)+n
         endif
         go to 17

  130    continue
c     ** Next is vertical search upward
c     ** and contouring, left then right
c     ** Find the first point on the "pfr" contour
         i=iserch(nc)
         j=jserch(nc)-1
c top of loop that steps vertically upward
  300    continue
         j=j+1
         if (j+1 .gt. jmaxs) then
            write(*,*) "Error in section 130 of subroutine contours:"
            write(*,*) "flux contour not found on iserch ", 
     &         "between jserch and jmaxs"
            write(*,*) "psi0 =   ",(pfr-simagx)/(sibdry-simagx)
            write(*,*) "iserch = ",iserch(nc)
            write(*,*) "jserch = ",jserch(nc)
            write(*,*) "jmaxs =  ",jmaxs
            call xerrab("")
         endif
         tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
         if (tstval .gt. 0.0d0) go to 300
c     ** We know that pfr is on vert. face between vertices (i,j) and (i,j+1)
c     ** going left
         istart=i
         jstart=j
         call go(left,n,nc,ns)
         nleft=n
         npoint(nc)=npoint(nc)+nleft
         if (n .gt. 0) then
c     ** copy xcn(1) to xcn(n) into xcurve in reverse order
            iprev=ilast(nc)
            do 23013 ii=1,n
               xcurve(iprev+ii,nc)=xcn(n-ii+1)
               ycurve(iprev+ii,nc)=ycn(n-ii+1)
               xcn(n-ii+1)=0.0d0
               ycn(n-ii+1)=0.0d0
23013       continue
            ilast(nc)=ilast(nc)+n
         endif
c     ** going right
         istart=i-1
         jstart=j
         call go(right,n,nc,ns)
         npoint(nc)=npoint(nc)+n
         if (n .gt. 0) then
c     ** copy xcn and ycn into xcurve and ycurve
            iprev=ilast(nc)
            do 23015 ii=1,n
               xcurve(iprev+ii,nc)=xcn(ii)
               ycurve(iprev+ii,nc)=ycn(ii)
               xcn(ii)=0.0d0
               ycn(ii)=0.0d0
23015       continue
            ilast(nc)=ilast(nc)+n
         endif
         go to 17

  140    continue
c     ** Next is vertical search upward
c     ** and contouring, right then left
c     ** Find the first point on the "pfr" contour
         i=iserch(nc)
         j=jserch(nc)-1
c top of loop that steps vertically upward
  400    continue
         j=j+1
         if (j+1 .gt. jmaxs) then
            write(*,*) "Error in section 140 of subroutine contours:"
            write(*,*) "flux contour not found on iserch ", 
     &         "between jserch and jmaxs"
            write(*,*) "psi0 =   ",(pfr-simagx)/(sibdry-simagx)
            write(*,*) "iserch = ",iserch(nc)
            write(*,*) "jserch = ",jserch(nc)
            write(*,*) "jmaxs =  ",jmaxs
            call xerrab("")
         endif
         tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
         if (tstval .gt. 0.0d0) go to 400
c     ** We know that pfr is on vert. face between vertices (i,j) and (i,j+1)
c     ** going right
         istart=i-1
         jstart=j
         call go(right,n,nc,ns)
         nright=n
         npoint(nc)=npoint(nc)+nright
         if (n .gt. 0) then
c     ** copy xcn and ycn into xcurve and ycurve in reverse order
            iprev=ilast(nc)
            do 23017 ii=1,n
               xcurve( iprev+ii,nc)=xcn(n-ii+1)
               ycurve( iprev+ii,nc)=ycn(n-ii+1)
               xcn(n-ii+1)=0.0d0
               ycn(n-ii+1)=0.0d0
23017       continue
            ilast(nc)=ilast(nc)+n
         endif
c     ** going left
         istart=i
c        jstart=j
         call go(left,n,nc,ns)
         npoint(nc)=npoint(nc)+n
         if (n .gt. 0) then
c     ** copy xcn(1) to xcn(n) into xcurve
            iprev=ilast(nc)
            do 23019 ii=1,n
               xcurve(iprev+ii,nc)=xcn(ii)
               ycurve(iprev+ii,nc)=ycn(ii)
               xcn(ii)=0.0d0
               ycn(ii)=0.0d0
23019       continue
            ilast(nc)=ilast(nc)+n
         endif
         go to 17

  150    continue
c     ** Next is vertical search downward
c     ** and contouring, left then right
c     ** Find the first point on the "pfr" contour
         i=iserch(nc)
         j=jserch(nc)
c top of loop that steps vertically downward
  500    continue
         j=j-1
         if (j .lt. jmins) then
            write(*,*) "Error in section 150 of subroutine contours:"
            write(*,*) "flux contour not found on iserch ", 
     &         "between jmins and jserch"
            write(*,*) "psi0 =   ",(pfr-simagx)/(sibdry-simagx)
            write(*,*) "iserch = ",iserch(nc)
            write(*,*) "jmins =  ",jmins
            write(*,*) "jserch = ",jserch(nc)
            call xerrab("")
         endif
         tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
         if (tstval .gt. 0.0d0) go to 500
c     ** We know that pfr is on vert. face between vertices (i,j) and (i,j+1)
c     ** going left
         istart=i
         jstart=j
         call go(left,n,nc,ns)
         nleft=n
         npoint(nc)=npoint(nc)+nleft
         if (n .gt. 0) then
c     ** copy xcn and ycn into xcurve and ycurve in reverse order
            iprev=ilast(nc)
            do 23021 ii=1,n
               xcurve(iprev+ii,nc)=xcn(n-ii+1)
               ycurve(iprev+ii,nc)=ycn(n-ii+1)
               xcn(n-ii+1)=0.0d0
               ycn(n-ii+1)=0.0d0
23021       continue
            ilast(nc)=ilast(nc)+n
         endif
c     ** going right
         istart=i-1
         jstart=j
         call go(right,n,nc,ns)
         npoint(nc)=npoint(nc)+n
         if (n .gt. 0) then
c     ** copy xcn and ycn into xcurve and ycurve
            iprev=ilast(nc)
            do 23023 ii=1,n
               xcurve(iprev+ii,nc)=xcn(ii)
               ycurve(iprev+ii,nc)=ycn(ii)
               xcn(ii)=0.0d0
               ycn(ii)=0.0d0
23023       continue
            ilast(nc)=ilast(nc)+n
         endif
         go to 17

  160    continue
c     ** Next is vertical search downward
c     ** and contouring, right then left
c     ** Find the first point on the "pfr" contour
         i=iserch(nc)
         j=jserch(nc)
c top of loop that steps vertically downward
  600    continue
         j=j-1
         if (j .lt. jmins) then
            write(*,*) "Error in section 160 of subroutine contours:"
            write(*,*) "flux contour not found on iserch ", 
     &         "between jmins and jserch"
            write(*,*) "psi0 =   ",(pfr-simagx)/(sibdry-simagx)
            write(*,*) "iserch = ",iserch(nc)
            write(*,*) "jmins =  ",jmins
            write(*,*) "jserch = ",jserch(nc)
            call xerrab("")
         endif
         tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
         if (tstval .gt. 0.0d0) go to 600
c     ** We know that pfr is on vert. face between vertices (i,j) and (i,j+1)
c     ** going right
         istart=i-1
         jstart=j
         call go(right,n,nc,ns)
         nright=n
         npoint(nc)=npoint(nc)+nright
         if (n .gt. 0) then
c    *** copy xcn and ycn into xcurve and ycurve in reverse order
            iprev=ilast(nc)
            do 23025 ii=1,n
               xcurve(iprev+ii,nc)=xcn(n-ii+1)
               ycurve(iprev+ii,nc)=ycn(n-ii+1)
               xcn(n-ii+1)=0.0d0
               ycn(n-ii+1)=0.0d0
23025       continue
            ilast(nc)=ilast(nc)+n
         endif
c     ** going left
         istart=i
         jstart=j
         call go(left,n,nc,ns)
         npoint(nc)=npoint(nc)+n
         if (n .gt. 0) then
c     ** copy xcn and ycn into xcurve and ycurve
            iprev=ilast(nc)
            do 23027 ii=1,n
               xcurve(iprev+ii,nc)=xcn(ii)
               ycurve(iprev+ii,nc)=ycn(ii)
               xcn(ii)=0.0d0
               ycn(ii)=0.0d0
23027       continue
            ilast(nc)=ilast(nc)+n
         endif
         go to 17

c end of do-loop over flux contours in region ns
   17    continue

      return
      end

c     ------------------------------------------------------------------

      subroutine go(idir,n,jj,ns)
cProlog
      implicit none
      integer idir, n, jj, ns, i, j, nmx, ncod
      doubleprecision xnew, dx, dy, tstval, dy1, rat, dx1
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,npts
c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis

      double precision xold ( nxefit)
      pointer(pxold,xold)

      double precision yold ( nyefit)
      pointer(pyold,yold)

      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)

      double precision workk ( nxefit)
      pointer(pworkk,workk)

      double precision fpol ( nxefit)
      pointer(pfpol,fpol)

      double precision pres ( nxefit)
      pointer(ppres,pres)

      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)

      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)

      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)

      double precision xlim ( nlim)
      pointer(pxlim,xlim)

      double precision ylim ( nlim)
      pointer(pylim,ylim)

      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)

      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)

      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)

      double precision work ( nwork)
      pointer(pwork,work)

      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)

      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)

      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd
c
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
cistchkon
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

      external theta_ok
      logical theta_ok

c     This subroutine computes data points on the jjth flux contour
c     in subregion ns, and stores them in the (xcn,ycn) arrays.
c
c     On entry, common block variables (istart,jstart) are the indices of
c     a vertex adjacent to the jjth flux contour, pfr, in subregion ns;
c     (istart,jstart) refer to (i,j) indices on the refined-EFIT rectangular
c     mesh, so x(i) and y(j) are the (R,Z) coord's of this vertex.

c     On entry, idir is the flag that indicates which face of the (i,j)
c     "cell" intersects the pfr contour:
c     idir=1    # go right; pfr is on vert face between (i+1,j) and (i+1,j+1)
c     idir=2    # go down; pfr is on horiz face between (i,j) and (i+1,j)
c     idir=3    # go left; pfr is on vert face between (i,j) and (i,j+1)
c     idir=4    # go up; pfr is on horiz face between (i,j+1) and (i+1,j+1)

c     On exit, the n data points are stored in the first n entries of the
c     common block arrays (xcn,ycn).

      i=istart
      j=jstart
      n=0
      nmx=npts-npoint(jj)
      xnew=x(i)

      go to(1,2,3,4)idir
c
    1 continue
c     *** going right
      if (n.ge.nmx) then
         write (6,901) npts, jj
         return
      endif
      ncod=1
      i=i+1
c MER 12/13/90
      if (i .ge. imax) return
      dx=x(i+1)-x(i)
      dy=y(j+1)-y(j)
c     *** check on upright
      tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 11
c     *** find coordinates
c         xold=xnew
      xnew=x(i)
c     if(xnew.gt.xold) return
      n=n+1
      dy1=dy*(pfr-f(i,j))/(f(i,j+1)-f(i,j))
      xcn(n)=xnew
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (i.eq.imax) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 12
c
   11 continue
      write(6,900) ncod
      return
c
c     ***
   12 continue
c     *** check diagonal
      tstval=(f(i+1,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 4
c     *** find coordinates
      rat=(pfr-f(i,j))/(f(i+1,j+1)-f(i,j))
      dx1=dx*rat
      dy1=dy*rat
      n=n+1
      xcn(n)=x(i)+dx1
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 14
c
c     ***
   14 continue
c     *** check horizontal
      tstval=(f(i+1,j)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 1
c     *** find coordinates
      dx1=dx*(pfr-f(i,j))/(f(i+1,j)-f(i,j))
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.lt.xold) return
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if (j.eq.jmins) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 2
c
c     ***************************
    2 continue
c     *** going down
      if (n.ge.nmx) then
         write (6,901) npts, jj
         return
      endif
      ncod=2
      j=j-1
c MER 12/13/90
      if (j .le. jmins) return
      dx=x(i+1)-x(i)
      dy=y(j+1)-y(j)
c     *** check diagonal
      tstval=(f(i+1,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 22
c     *** find coordinates
      rat=(pfr-f(i,j))/(f(i+1,j+1)-f(i,j))
      dx1=dx*rat
      dy1=dy*rat
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.gt.xold) return
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 21
c
c     ***
   21 continue
c     *** check horizontal
      tstval=(f(i+1,j)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 1
c     *** find coordinates
      dx1=dx*(pfr-f(i,j))/(f(i+1,j)-f(i,j))
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.gt.xold) return
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if (j.eq.jmins) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 2
c
c     ***
   22 continue
c     *** check vertical
      tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) return
c     *** find coordinates
c         xold=xnew
      xnew=x(i)
c     if(xnew.gt.xold) return
      n=n+1
      dy1=dy*(pfr-f(i,j))/(f(i,j+1)-f(i,j))
      xcn(n)=xnew
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (i.eq.imin) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 3
c
c     ******************************
    3 continue
c     *** going left
      if (n.ge.nmx) then
         write (6,901) npts, jj
         return
      endif
      ncod=3
      i=i-1
c MER 12/13/90
      if (i .le. imin) return
      dx=x(i+1)-x(i)
      dy=y(j+1)-y(j)
c     *** check diagonal
      tstval=(f(i+1,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 32
c     *** find coordinates
      rat=(pfr-f(i,j))/(f(i+1,j+1)-f(i,j))
      dx1=dx*rat
      dy1=dy*rat
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.gt.xold) return
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 31
c
c     ***
   31 continue
c     *** check vertical
      tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 4
c     *** find coordinates
c         xold=xnew
      xnew=x(i)
      dy1=dy*(pfr-f(i,j))/(f(i,j+1)-f(i,j))
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (i.eq.imin) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 3
c
c     ***
   32 continue
c     *** check horizontal
      tstval=(f(i+1,j)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) return
c     *** ind coordinates
      dx1=dx*(pfr-f(i,j))/(f(i+1,j)-f(i,j))
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.gt.xold) return
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if (j.eq.jmins) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 2
c
c     ***************************
    4 continue
c     *** going up
      if (n.ge.nmx) then
         write (6,901) npts, jj
         return
      endif
      ncod=4
      j=j+1
c MER 12/13/90
      if (j .ge. jmaxs) return
      dx=x(i+1)-x(i)
      dy=y(j+1)-y(j)
c     *** check horizontal
      tstval=(f(i+1,j)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) return
c     *** find coordinates
      dx1=dx*(pfr-f(i,j))/(f(i+1,j)-f(i,j))
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.gt.xold) return
      n=n+1
      xcn(n)=xnew
      ycn(n)=y(j)
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if (j.eq.jmaxs) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 41
c
c     ***
   41 continue
c     *** check diagonal
      tstval=(f(i+1,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 1
c     *** find coordinates
      rat=(pfr-f(i,j))/(f(i+1,j+1)-f(i,j))
      dx1=dx*rat
      dy1=dy*rat
c         xold=xnew
      xnew=x(i)+dx1
c     if(xnew.gt.xold) return
      n=n+1
      xcn(n)=x(i)+dx1
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 42
c
c     ***
   42 continue
c     *** check vertical
      tstval=(f(i,j+1)-pfr)*(f(i,j)-pfr)
      if (tstval.gt.0.0d0) go to 4
c         xold=xnew
      xnew=x(i)
c     if(xnew.gt.xold) return
      dy1=dy*(pfr-f(i,j))/(f(i,j+1)-f(i,j))
      n=n+1
      xcn(n)=x(i)
      ycn(n)=y(j)+dy1
      if ((xcn(n).gt.xmaxf).or.(xcn(n).lt.xminf)) return
      if ((ycn(n).gt.ymaxf).or.(ycn(n).lt.yminf)) return
      if (i.eq.imin) return
      if (istchkon .eq. 1) then
c MER 97/03/24
         if ( .not. theta_ok(xcn(n),ycn(n),ns) ) return
      endif
      go to 3
c
  900 format(' go - section = ',i2)
  901 format(' more than npts = ',i4, ' data points on contour segment '
     &   ,i3)
c     ***
  999 continue
      return
      end


c----------------------------------------------------------------------c

      logical function theta_ok (r, z, n)
cProlog
      implicit none
      integer n
      doubleprecision r, z

c     This function checks to see that the point (r,z) lies within
c     an acceptable polar angle for various flux-contouring regions.
c     The origin of the coordinate sytem for calculating the polar
c     angle is the magnetic axis.  By setting limits on the polar
c     angle we avoid tracing endless loops around closed core plasma
c     flux contours.

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd
cjdim,nxefit,nyefit,nlim
c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis

      double precision xold ( nxefit)
      pointer(pxold,xold)

      double precision yold ( nyefit)
      pointer(pyold,yold)

      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)

      double precision workk ( nxefit)
      pointer(pworkk,workk)

      double precision fpol ( nxefit)
      pointer(pfpol,fpol)

      double precision pres ( nxefit)
      pointer(ppres,pres)

      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)

      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)

      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)

      double precision xlim ( nlim)
      pointer(pxlim,xlim)

      double precision ylim ( nlim)
      pointer(pylim,ylim)

      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)

      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)

      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)

      double precision work ( nwork)
      pointer(pwork,work)

      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)

      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)

      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd
c
c Group Aeqflxgrd
      double precision etime, rseps, zseps, rseps1, zseps1, rseps2
      integer vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop, magpri
      character*128 aeqdskfname
      double precision zseps2, rvsin, zvsin, rvsout, zvsout
      integer nfcoil, nesum

      double precision rco2v ( mco2v)
      pointer(prco2v,rco2v)

      double precision dco2v ( mco2v)
      pointer(pdco2v,dco2v)

      double precision rco2r ( mco2r)
      pointer(prco2r,rco2r)

      double precision dco2r ( mco2r)
      pointer(pdco2r,dco2r)

      double precision csilop ( nsilop)
      pointer(pcsilop,csilop)

      double precision cmpr2 ( magpri)
      pointer(pcmpr2,cmpr2)

      double precision ccbrsp ( nfcoil)
      pointer(pccbrsp,ccbrsp)

      double precision eccurt ( nesum)
      pointer(peccurt,eccurt)
      common /com10002/ aeqdskfname
      common /com50/ vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop
      common /com50/ magpri, nfcoil, nesum
      common /com53/ etime, rseps, zseps, rseps1, zseps1, rseps2, zseps2
      common /com53/ rvsin, zvsin, rvsout, zvsout
      common /com56/ prco2v, pdco2v, prco2r
      common /com56/ pdco2r, pcsilop, pcmpr2
      common /com56/ pccbrsp, peccurt
c End of Aeqflxgrd
c
c Group Dimflx
      integer nsearch
      common /flx10/ nsearch
c End of Dimflx
cnsearch
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
ctheta1fac,theta2fac

c     local variables
      doubleprecision theta, thetap, thetamaxp, theta1, theta2, pi, 
     &   twopi

c     initialize
      pi = 4.d0*atan2(1.d0,1.d0)
      twopi = 2*pi
      theta_ok = .false.
c -pi < theta < +pi
      theta = atan2 (z-zmagx, r-rmagx)

c----------------------------------------------------------------------c
      if (nsearch .eq. 2) then
c SOL only; no core region
c----------------------------------------------------------------------c
         if (n .eq. 1) then
c region 1: inboard SOL
c in rotated frame where thetamin(1) = 0 (see subr inflx1)
            thetap = theta - thetamin(1)
            if (thetap .lt. 0) thetap = thetap + twopi
            if (thetap .gt. twopi) thetap = thetap - twopi
            thetamaxp = thetamax(1) - thetamin(1)
            if (thetamaxp .lt. 0) thetamaxp = thetamaxp + twopi
            if (thetamaxp .gt. twopi) thetamaxp = thetamaxp - twopi
            if (thetap .lt. thetamaxp) theta_ok = .true.
         elseif (n .eq. 2) then
c region 2: outboard SOL
c in rotated frame where thetamin(2) = 0 (see subr inflx1)
            thetap = theta - thetamin(2)
            if (thetap .lt. 0) thetap = thetap + twopi
            if (thetap .gt. twopi) thetap = thetap - twopi
            thetamaxp = thetamax(2) - thetamin(2)
            if (thetamaxp .lt. 0) thetamaxp = thetamaxp + twopi
            if (thetamaxp .gt. twopi) thetamaxp = thetamaxp - twopi
            if (thetap .lt. thetamaxp) theta_ok = .true.
         else
            call remark("*** ")
            call remark("*** function theta_ok: illegal argument n")
            call remark("*** ")
            call xerrab("")
         endif
c----------------------------------------------------------------------c
      elseif (nsearch .eq. 4) then
c SOL + finite core region
c----------------------------------------------------------------------c
         if (n .eq. 1) then
c region 1: inboard SOL & core
c in rotated frame where thetamin(1) = 0 (see subr inflx1)
            thetap = theta - thetamin(1)
            if (thetap .lt. 0) thetap = thetap + twopi
            if (thetap .gt. twopi) thetap = thetap - twopi
            thetamaxp = thetamax(1) - thetamin(1)
            if (thetamaxp .lt. 0) thetamaxp = thetamaxp + twopi
            if (thetamaxp .gt. twopi) thetamaxp = thetamaxp - twopi
            if (thetap .lt. thetamaxp) theta_ok = .true.
         elseif (n .eq. 2) then
c region 2: inboard private flux
c MER (09 Feb 2015) Avoid discontinuity in theta=atan2(y,x) near +/-pi
c by transforming all theta's such that 0 <= theta < +twopi
            theta1 = theta1fac*pi
            theta2 = twopi + thetax + dtheta_overlap_pf(1)
            if (theta .lt. 0) theta = theta + twopi
            if ((theta1 .lt. theta) .and. (theta .lt. theta2)) theta_ok 
     &            = .true.
         elseif (n .eq. 3) then
c region 3: outboard SOL & core
c in rotated frame where thetamin(2) = 0 (see subr inflx1)
            thetap = theta - thetamin(2)
            if (thetap .lt. 0) thetap = thetap + twopi
            if (thetap .gt. twopi) thetap = thetap - twopi
            thetamaxp = thetamax(2) - thetamin(2)
            if (thetamaxp .lt. 0) thetamaxp = thetamaxp + twopi
            if (thetamaxp .gt. twopi) thetamaxp = thetamaxp - twopi
            if (thetap .lt. thetamaxp) theta_ok = .true.
         elseif (n .eq. 4) then
c region 4: outboard private flux
            theta1 = thetax - dtheta_overlap_pf(2)
c MER (09 Feb 2015) Insert user-defined multiplicative factor in theta2:
            theta2 = theta2fac*pi
            if ((theta1 .lt. theta) .and. (theta .lt. theta2)) theta_ok 
     &            = .true.
         else
            call remark("*** ")
            call remark("*** function theta_ok: illegal argument n")
            call remark("*** ")
            call xerrab("")
         endif
c----------------------------------------------------------------------c
      else
c----------------------------------------------------------------------c
         call remark("*** ")
         call remark("*** function theta_ok: nsearch must be 2 or 4")
         call remark("*** ")
         call xerrab("")
c----------------------------------------------------------------------c
      endif
c----------------------------------------------------------------------c

      return
      end




