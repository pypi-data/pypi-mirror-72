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
c     ./../apifcn.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































c-----------------------------------------------------------------------
      subroutine getatau(nx, ny, uu, gx, ixpt1, ixpt2, iysptrx, atau, 
     &   tau1, tau2)
cProlog
      implicit none

c     This subroutine calculates the time for ions
c     to escape along open flux surfaces to either the left (inboard) or
c     right (outboard) divertor plate.

c ... Input arguments:
c poloidal dimension of mesh (excluding boundaries)
      integer nx
c radial   dimension of mesh (excluding boundaries)
      integer ny
c poloidal ion velocity
      doubleprecision uu(0:nx+1,0:ny+1)
c 1/(x-width) of primary mesh cells
      doubleprecision gx(0:nx+1,0:ny+1)
c ix of last private-flux cell before cut on left
      integer ixpt1
c ix of last core-plasma cell before cut on right
      integer ixpt2
c iy of cell just below the separatrix
      integer iysptrx

c ... Output arguments:
c lifetime of impurity
      doubleprecision atau(0:nx+1,0:ny+1)
c time to escape to inboard div. plate
      doubleprecision tau1(0:nx+1,0:ny+1)
c time to escape to outboard div. plate
      doubleprecision tau2(0:nx+1,0:ny+1)

c     local variables --
      integer ix, iy
      doubleprecision u, dxt, taumax

c     initialization --
c     Upper limit for particle confinement time
      taumax = 1.0d+00
c     Default values for core plasma confinement
      do 23000 ix = ixpt1+1, ixpt2
         do 23002 iy = 1, iysptrx
            tau1(ix,iy) = taumax
            tau2(ix,iy) = taumax
23002    continue
23000 continue

c     ------------------------------------------------------------------
c     For particles which flow toward the left plate --
c     ------------------------------------------------------------------

c     on private flux surfaces:
c
      do 23004 iy=1,iysptrx
         tau1(0,iy) = 0.d0
         do 23006 ix=1,ixpt1
            u = uu(ix-1,iy)
            dxt = 0.5d0/gx(ix-1,iy) + 0.5d0/gx(ix,iy)
            if (u .lt. 0.d0) then
               tau1(ix,iy) = min (taumax, tau1(ix-1,iy) + dxt / abs(u))
            else
               tau1(ix,iy) = taumax
            endif
23006    continue
         u = uu(ixpt2,iy)
         dxt = 0.5d0/gx(ixpt1,iy) + 0.5d0/gx(ixpt2+1,iy)
         if (u .lt. 0.d0) then
            tau1(ixpt2+1,iy) = min (taumax, tau1(ixpt1,iy) + dxt/abs(u))
         else
            tau1(ixpt2+1,iy) = taumax
         endif
         do 23008 ix=ixpt2+2,nx
            u = uu(ix-1,iy)
            dxt = 0.5d0/gx(ix-1,iy) + 0.5d0/gx(ix,iy)
            if (u .lt. 0.d0) then
               tau1(ix,iy) = min (taumax, tau1(ix-1,iy) + dxt / abs(u))
            else
               tau1(ix,iy) = taumax
            endif
23008    continue
         tau1(nx+1,iy) = taumax
23004 continue

c     on external flux surfaces :
c
      do 23010 iy=iysptrx+1,ny
         tau1(0,iy) = 0.d0
         do 23012 ix=1,nx
            u = uu(ix-1,iy)
            dxt = 0.5d0/gx(ix-1,iy) + 0.5d0/gx(ix,iy)
            if (u .lt. 0.d0) then
               tau1(ix,iy) = min (taumax, tau1(ix-1,iy) + dxt / abs(u))
            else
               tau1(ix,iy) = taumax
            endif
23012    continue
         tau1(nx+1,iy) = taumax
23010 continue

c     ------------------------------------------------------------------
c     For particles which flow toward the right plate --
c     ------------------------------------------------------------------

c     on private flux surfaces:
c
      do 23014 iy=1,iysptrx
         tau2(nx+1,iy) = 0.d0
         do 23016 ix=nx,ixpt2+1,-1
            u = uu(ix,iy)
            dxt = 0.5d0/gx(ix,iy) + 0.5d0/gx(ix+1,iy)
            if (u .gt. 0.d0) then
               tau2(ix,iy) = min (taumax, tau2(ix+1,iy) + dxt / abs(u))
            else
               tau2(ix,iy) = taumax
            endif
23016    continue
         u = uu(ixpt2,iy)
         dxt = 0.5d0/gx(ixpt1,iy) + 0.5d0/gx(ixpt2+1,iy)
         if (u .gt. 0.d0) then
            tau2(ixpt1,iy) = min (taumax, tau2(ixpt2+1,iy) + dxt/abs(u))
         else
            tau2(ixpt1,iy) = taumax
         endif
         do 23018 ix=ixpt1-1,1,-1
            u = uu(ix,iy)
            dxt = 0.5d0/gx(ix,iy) + 0.5d0/gx(ix+1,iy)
            if (u .gt. 0.d0) then
               tau2(ix,iy) = min (taumax, tau2(ix+1,iy) + dxt / abs(u))
            else
               tau2(ix,iy) = taumax
            endif
23018    continue
         tau2(0,iy) = taumax
23014 continue

c     on external flux surfaces :
c
      do 23020 iy=iysptrx+1,ny
         tau2(nx+1,iy) = 0.d0
         do 23022 ix=nx,1,-1
            u = uu(ix,iy)
            dxt = 0.5d0/gx(ix,iy) + 0.5d0/gx(ix+1,iy)
            if (u .gt. 0.d0) then
               tau2(ix,iy) = min (taumax, tau2(ix+1,iy) + dxt / abs(u))
            else
               tau2(ix,iy) = taumax
            endif
23022    continue
         tau2(0,iy) = taumax
23020 continue

c     ------------------------------------------------------------------
c     Combined loss to either plate --
c     ------------------------------------------------------------------

      do 23024 ix = 1, nx
         do 23026 iy = 1, ny
            atau(ix,iy) = min (tau1(ix,iy), tau2(ix,iy))
23026    continue
23024 continue

      return
      end
c-----------------------------------------------------------------------
      subroutine getprad(nx, ny, ngsp, te, ne, ng, afrac, atau, prad, na
     &   , ntau, nratio)
cProlog
      implicit none

c ... Input arguments:
c poloidal dimension of mesh (excluding boundaries)
      integer nx
c radial   dimension of mesh (excluding boundaries)
      integer ny
c number of gas species
      integer ngsp
c electron temperature
      doubleprecision te(0:nx+1,0:ny+1)
c electron density
      doubleprecision ne(0:nx+1,0:ny+1)
c gas density
      doubleprecision ng(0:nx+1,0:ny+1,1:ngsp)
c atomic concentration of impurity
      doubleprecision afrac(0:nx+1,0:ny+1)
c lifetime of impurity
      doubleprecision atau(0:nx+1,0:ny+1)

c ... Output arguments:
c electron energy loss due to
      doubleprecision prad(0:nx+1,0:ny+1)
c impurity radiation
c atomic density of impurity
      doubleprecision na(0:nx+1,0:ny+1)
c confinement parameter for impurity
      doubleprecision ntau(0:nx+1,0:ny+1)
c (neutral density) / (electron dens)
      doubleprecision nratio(0:nx+1,0:ny+1)

c     local variables --
      integer ix,iy,is

c     procedures --
      doubleprecision emissbs
      external emissbs

c     compute energy loss for electrons --

      do 23000 ix=1,nx
         do 23002 iy=1,ny
            na(ix,iy) = afrac(ix,iy) * ne(ix,iy)
            ntau(ix,iy) = atau(ix,iy) * ne(ix,iy)
            nratio(ix,iy) = 0.d0
            do 23004 is=1,ngsp
               nratio(ix,iy) = nratio(ix,iy) + ng(ix,iy,is)
23004       continue
            nratio(ix,iy) = nratio(ix,iy)/ne(ix,iy)
            prad(ix,iy) = na(ix,iy) * ne(ix,iy) * emissbs (te(ix,iy), 
     &         nratio(ix,iy), ntau(ix,iy))
23002    continue
23000 continue

      return
      end
c-----------------------------------------------------------------------
      subroutine sapitim (timingsw)
cProlog
      implicit none
      integer timingsw
c Group Timing
      double precision ttotfe, ttimpfe, ttotjf, ttimpjf, ttmatfac
      double precision ttmatsol, ttjstor, ttjrnorm, ttjreorder, ttimpc
      double precision tstart, tend, ttnpg, ttngxlog, ttngylog, ttngfd2
      double precision ttngfxy
      integer istimingon, iprinttim
      common /com140/ istimingon, iprinttim
      common /com143/ ttotfe, ttimpfe, ttotjf, ttimpjf, ttmatfac
      common /com143/ ttmatsol, ttjstor, ttjrnorm, ttjreorder, ttimpc
      common /com143/ tstart, tend, ttnpg, ttngxlog, ttngylog, ttngfd2
      common /com143/ ttngfxy
c End of Timing


      istimingon = timingsw

      return
      end
c-----------------------------------------------------------------------
      subroutine wapitim
cProlog
c ... Write timing data for the api package.
      implicit none
c Group Timing
      double precision ttotfe, ttimpfe, ttotjf, ttimpjf, ttmatfac
      double precision ttmatsol, ttjstor, ttjrnorm, ttjreorder, ttimpc
      double precision tstart, tend, ttnpg, ttngxlog, ttngylog, ttngfd2
      double precision ttngfxy
      integer istimingon, iprinttim
      common /com140/ istimingon, iprinttim
      common /com143/ ttotfe, ttimpfe, ttotjf, ttimpjf, ttmatfac
      common /com143/ ttmatsol, ttjstor, ttjrnorm, ttjreorder, ttimpc
      common /com143/ tstart, tend, ttnpg, ttngxlog, ttngylog, ttngfd2
      common /com143/ ttngfxy
c End of Timing


      write(*,902) 'Impur.:  physics w/o bookkeeping = ', ttimpc
  902 format(a36,f10.4,20x,' sec')
      write(*,*) '(included in above f & Jac numbers)'
      ttimpc = 0.d0

      return
      end
c-----------------------------------------------------------------------

      subroutine readrates(apidir,impfname)
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

      character*(*) apidir
      character*(*) impfname
      integer impunit, ios

c     Reads Isler's excitation rate data
c     Based on Gary Porter's read_rates script

c ... Function:
c defined in the Basis runtime library
      integer utgetcl

c ... Local variable:
      integer stringlen, MAXSTRING
      parameter (MAXSTRING=500)
      character*(MAXSTRING) apidirx

c ... Get length of string containing directory name (omitting trailing
c     blanks). Basis function basfilex expands $,~.
      call basfilex(apidir,apidirx)
      stringlen = utgetcl(apidirx)

      call freeus(impunit)
      open (impunit, file=apidirx(1:stringlen) // '/' // impfname, form=
     &   'formatted', iostat=ios, status='old')
      if (ios .ne. 0) then
         write(*,*) '*** Input file ',impfname,' not found'
         call xerrab("")
      else
         write(*,*) '*** Reading from impurity excitation rate file: ',
     &      impfname
      endif

      read (impunit,*) ntemp
      read (impunit,*) nlam
      read (impunit,*) nden

      call gchange("Emissivities",0)

      call readrates1(impunit)

      return
      end
c-----------------------------------------------------------------------

      subroutine readrates1(impunit)
cProlog
      implicit none
      integer impunit
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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

      integer ii,jj,kk
      character*8 zdum

      read (impunit, '(6f12.2)') (lamb(ii),ii=1,nlam)
      write (*, '(6f12.2)') (lamb(ii),ii=1,nlam)
      do 23000 ii=1,ntemp
         read (impunit, '(a8)') zdum
         read (impunit, '(a8)') zdum
         read (impunit, '(f9.2)') etemp(ii)
         read (impunit, '(a8)') zdum
         do 23002 jj=1,nden
            read (impunit, '(a8)') zdum
            read (impunit, '(1x,e12.3,f8.2)') eden(jj),etemp(ii)
            read (impunit, '(6e12.3)') (rate(kk,ii,jj),kk=1,nlam)
23002    continue
23000 continue

      close(impunit)

c     Convert to m^-3 for UEDGE compatibility
      do 23004 ii=1,nden
         eden(ii)=eden(ii)*1d6
23004 continue

      write (*,*) 
     &   'Emission rate [ph/m^3/s] is rate*(appropriate density)'

      return
      end
c-----------------------------------------------------------------------

      subroutine calcrates(ne,te,density)
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

      doubleprecision ne(0:nx+1,0:ny+1),te(0:nx+1,0:ny+1),density(0:nx+1
     &   ,0:ny+1)
      doubleprecision ev
      doubleprecision newrate
      integer ii,ix,iy,ij,indxden,indxte

      data ev /1.6022d-19/

c     Calculates emission rates for each cell and wavelength:
c     Interpolate on (ne,te) in Isler data to get coeff for each line.
c     Multiply by appropriate input density to get emissivity.

      do 23000 ix=0,nx+1
         do 23002 iy=0,ny+1
            indxden=1
            indxte=1
            do 23004 ij=1,nden
               if (ne(ix,iy) .gt. eden(ij)) indxden=ij
23004       continue
            do 23006 ij=1,ntemp
               if (te(ix,iy)/ev .gt. etemp(ij)) indxte=ij
23006       continue
            do 23008 ii=1,nlam
               if (indxte .eq. 1) then
                  newrate=0.d0
               elseif ((indxden .eq. 1) .and. (indxte .lt. ntemp)) then
                  newrate=rate(ii,indxte,1) + (te(ix,iy)/ev-etemp(indxte
     &               ))* (rate(ii,indxte+1,1)-rate(ii,indxte,1))/ (etemp
     &               (indxte+1)-etemp(indxte))
                  newrate=newrate*ne(ix,iy)/eden(1)
               elseif ((indxden .ge. nden) .and. (indxte .ge. ntemp))
     &                then
                  newrate=rate(ii,ntemp,nden)*ne(ix,iy)/eden(nden)
               elseif ((indxden .ge. nden) .and. (indxte .lt. ntemp))
     &                then
                  newrate=rate(ii,indxte,nden) + (te(ix,iy)/ev-etemp(
     &               indxte))* (rate(ii,indxte+1,nden)-rate(ii,indxte,
     &               nden))/ (etemp(indxte+1)-etemp(indxte))
                  newrate=newrate*ne(ix,iy)/eden(nden)
               elseif ((indxden .lt. nden) .and. (indxte .ge. ntemp))
     &                then
                  newrate=rate(ii,ntemp,indxden) + (ne(ix,iy)-eden(
     &               indxden))* (rate(ii,ntemp,indxden+1)-rate(ii,ntemp,
     &               indxden))/ (eden(indxden+1)-eden(indxden))
               else
                  newrate=rate(ii,indxte,indxden) + (te(ix,iy)/ev-etemp(
     &               indxte))* (rate(ii,indxte+1,indxden)-rate(ii,indxte
     &               ,indxden))/ (etemp(indxte+1)-etemp(indxte)) + (ne(
     &               ix,iy)-eden(indxden))* (rate(ii,indxte,indxden+1)-
     &               rate(ii,indxte,indxden))/ (eden(indxden+1)-eden(
     &               indxden))
               endif
               emiss(ii,ix,iy)=newrate*density(ix,iy)
23008       continue
23002    continue
23000 continue

      return
      end
c-----------------------------------------------------------------------

      doubleprecision function lineintegral(arg,rvertex,zvertex)
cProlog
      implicit none
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

      doubleprecision arg(nrpix,nzpix)
      doubleprecision rvertex(2),zvertex(2)
      doubleprecision r1,r2,z1,z2,rp,zp
      integer iv1,iv2,jv1,jv2,k,ii,jj
      integer j,jbeg,jend,jstep
      integer i,ibeg,iend,istep

c MER 02 Jul 2003
c Compute the line integral of the 2-d array arg(nrpix,nzpix) along the
c path (rvertex(1:2),zvertex(1:2)).  We assume that arg(ii,jj) is the
c pixel representation of some UEDGE array arg_ue(ix,iy), obtained by mapping
c the UEDGE cells (rm,zm) onto a rectangular pixel domain via the DCE
c subroutine rzxform, e.g.,
c
c    arg = rzxform(arg_ue,rm,zm,nrpix,nzpix,rminpix,rmaxpix,zminpix,zmaxpix)
c
c The path integral is obtained via an algorithm which finds the
c intersection points of the line-of-sight (LOS) with horizontal
c and vertical pixel boundaries; these points then define the path
c length of the LOS in each cell.

c Initialize arrays:
      npd=0
      rp1=0.d0
      zp1=0.d0
      rp2=0.d0
      zp2=0.d0
      wt=0.d0

c Find the indices of the pixels containing the LOS vertices:
      r1=rvertex(1)
      z1=zvertex(1)
      r2=rvertex(2)
      z2=zvertex(2)
c rpixel zone containing vertex 1
      iv1=int((r1-rminpix)/drpix)+1
c zpixel zone containing vertex 1
      jv1=int((z1-zminpix)/dzpix)+1
c rpixel zone containing vertex 2
      iv2=int((r2-rminpix)/drpix)+1
c zpixel zone containing vertex 2
      jv2=int((z2-zminpix)/dzpix)+1

c Find the intersection of the LOS with the horizontal cell boundaries
c between the LOS vertices:
      if (jv2 .ge. jv1) then
c first horiz. boundary above vertex 1
         jbeg=max(0,jv1)
c last  horiz. boundary below vertex 2
         jend=min(nzpix,jv2-1)
         jstep=1
      else
c last  horiz. boundary below vertex 1
         jbeg=min(nzpix,jv1-1)
c first horiz. boundary above vertex 2
         jend=max(0,jv2)
         jstep=-1
      endif
      do 23000 j=jbeg,jend,jstep
         zp=zminpix+j*dzpix
         rp=r1+(r2-r1)*(zp-z1)/(z2-z1)
czp lies between zpixel zones jj and jj+1
         jj=j
         if (rp .gt. rminpix) then
crp lies in rpixel zone ii
            ii=int((rp-rminpix)/drpix)+1
         else
            ii=0
         endif
c Assign this point to pixels in rows jj and jj+1
         if ( (1 .le. ii ) .and. (ii .le. nrpix) .and. (1 .le. jj+1) 
     &      .and. (jj+1 .le. nzpix) ) then
            if (npd(ii,jj+1).eq.0) then
               rp1(ii,jj+1)=rp
               zp1(ii,jj+1)=zp
               npd(ii,jj+1)=npd(ii,jj+1)+1
            elseif (npd(ii,jj+1).eq.1) then
               rp2(ii,jj+1)=rp
               zp2(ii,jj+1)=zp
               npd(ii,jj+1)=npd(ii,jj+1)+1
            else
               write (*,*) 'error:  ', 
     &            'tried to assign more than 2 points to jj+1 pixel (', 
     &            ii,',',jj+1,')'
               call xerrab("")
            endif
         endif
         if ( (1 .le. ii) .and. (ii .le. nrpix) .and. (1 .le. jj) .and. 
     &      (jj .le. nzpix) ) then
            if (npd(ii,jj).eq.0) then
               rp1(ii,jj)=rp
               zp1(ii,jj)=zp
               npd(ii,jj)=npd(ii,jj)+1
            elseif (npd(ii,jj).eq.1) then
               rp2(ii,jj)=rp
               zp2(ii,jj)=zp
               npd(ii,jj)=npd(ii,jj)+1
            else
               write (*,*) 'error:  ', 
     &            'tried to assign more than 2 points to jj pixel (', ii
     &            ,',',jj,')'
               call xerrab("")
            endif
         endif
23000 continue

c Find the intersection of the LOS with the vertical cell boundaries
c between the LOS vertices:
      if (iv2 .ge. iv1) then
c first vertical boundary right of vertex 1
         ibeg=max(0,iv1)
c last  vertical boundary left  of vertex 2
         iend=min(nrpix,iv2-1)
         istep=1
      else
c last  vertical boundary left  of vertex 1
         ibeg=min(nrpix,iv1-1)
c first vertical boundary right of vertex 2
         iend=max(0,iv2)
         istep=-1
      endif
      do 23002 i=ibeg,iend,istep
         rp=rminpix+i*drpix
         zp=z1+(z2-z1)*(rp-r1)/(r2-r1)
crp lies between rpixel zones ii and ii+1
         ii=i
         if (zp .gt. zminpix) then
czp lies in zpixel zone jj
            jj=int((zp-zminpix)/dzpix)+1
         else
            jj=0
         endif
c Assign this point to pixels in column ii and ii+1
         if ( (1 .le. ii+1) .and. (ii+1 .le. nrpix) .and. (1 .le. jj ) 
     &      .and. (jj .le. nzpix) ) then
            if (npd(ii+1,jj).eq.0) then
               rp1(ii+1,jj)=rp
               zp1(ii+1,jj)=zp
               npd(ii+1,jj)=npd(ii+1,jj)+1
            elseif (npd(ii+1,jj).eq.1) then
               rp2(ii+1,jj)=rp
               zp2(ii+1,jj)=zp
               npd(ii+1,jj)=npd(ii+1,jj)+1
            else
               write (*,*) 'error:  ', 
     &            'tried to assign more than 2 points to ii+1 pixel (', 
     &            ii+1,',',jj,')'
               call xerrab("")
            endif
         endif
         if ( (1 .le. ii) .and. (ii .le. nrpix) .and. (1 .le. jj) .and. 
     &      (jj .le. nzpix) ) then
            if (npd(ii,jj).eq.0) then
               rp1(ii,jj)=rp
               zp1(ii,jj)=zp
               npd(ii,jj)=npd(ii,jj)+1
            elseif (npd(ii,jj).eq.1) then
               rp2(ii,jj)=rp
               zp2(ii,jj)=zp
               npd(ii,jj)=npd(ii,jj)+1
            else
               write (*,*) 'error:  ', 
     &            'tried to assign more than 2 points to ii pixel (', ii
     &            ,',',jj,')'
               call xerrab("")
            endif
         endif
23002 continue

c End-point contributions:
c Assign LOS vertices to pixels (iv1,jv1) and (iv2,jv2):
      if ( (1 .le. iv1) .and. (iv1 .le. nrpix) .and. (1 .le. jv1) .and. 
     &   (jv1 .le. nzpix) ) then
         if (npd(iv1,jv1).eq.1) then
            rp2(iv1,jv1)=r1
            zp2(iv1,jv1)=z1
            npd(iv1,jv1)=npd(iv1,jv1)+1
         else
            write (*,*) 'error in end-point 1 pixel (',iv1,',',jv1,')'
            call xerrab("")
         endif
      endif
      if ( (1 .le. iv2) .and. (iv2 .le. nrpix) .and. (1 .le. jv2) .and. 
     &   (jv2 .le. nzpix) ) then
         if (npd(iv2,jv2).eq.1) then
            rp2(iv2,jv2)=r2
            zp2(iv2,jv2)=z2
            npd(iv2,jv2)=npd(iv2,jv2)+1
         else
            write (*,*) 'error in end-point 2 pixel (',iv2,',',jv2,')'
            call xerrab("")
         endif
      endif

c Compute the weights (path lengths) for each pixel and sum contributions
c to lineintegral:
      lineintegral=0.d0
      do 23004 ii=max(1,min(nrpix,iv1)),max(1,min(nrpix,iv2)),istep
         do 23006 jj=max(1,min(nzpix,jv1)),max(1,min(nzpix,jv2)),jstep
            wt(ii,jj) = sqrt( (rp1(ii,jj)-rp2(ii,jj))**2 + (zp1(ii,jj)-
     &         zp2(ii,jj))**2 )
            lineintegral=lineintegral+wt(ii,jj)*arg(ii,jj)
23006    continue
23004 continue

      return
      end

