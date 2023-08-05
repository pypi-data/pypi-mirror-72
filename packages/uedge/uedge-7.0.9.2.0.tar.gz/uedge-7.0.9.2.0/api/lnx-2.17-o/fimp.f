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
c     ./../fimp.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































      subroutine imprates(temp,kk,nzarg,rioniz,rrecomb,rcxrecom)
cProlog
      doubleprecision temp
      integer kk, nzarg
      doubleprecision rioniz, rrecomb, rcxrecom
c ... Given temperature "temp" and a charge state "k", which is less
c     than or equal to the highest state "nzarg", interpolate from
c     tabulated rates for a particular impurity of ionization,
c     recombination, and charge-exchange recombination.
c    Note:  no scaling of temperatures is done here, so temp and tevb
c    must be provided in the same set of units.  tevb may not be in eV.
c
c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap

      double precision tevb ( ntev)
      pointer(ptevb,tevb)

      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)

      double precision rre ( ntev,1:nz)
      pointer(prre,rre)

      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)

      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)

      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)

      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)

      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)

      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)

      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)

      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)

      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)

      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)

      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)

      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)

      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)

      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge
c tevb,rsi,rre,rrcx

      integer itemp
      doubleprecision xltemn, dlogte
c
      rrecomb = 0.d0
      rcxrecom = 0.d0
c
      xltemn = log10(tevb(1))
      dlogte = log10(tevb(2)) - xltemn
c
c ... Find index itemp into table such that
c        tevb(itemp) .le. temp .lt. tevb(itemp+1)
c
      itemp = int( ( log10( temp ) - xltemn ) / dlogte + 1.d0 )
c
c ... For temperatures below minimum table temperature, extrapolate
c     downwards from table entries 1 and 2.

      itemp = max(1, itemp)
c
c ... For temperatures above maximum table temperature, extrapolate
c     upwards from table entries ntev-1 and ntev.

      itemp = min(ntev-1, itemp)
c
      if (kk .lt. nzarg)then
         rioniz = rsi(itemp,kk) + ( temp - tevb(itemp) ) * ( rsi(itemp+1
     &      ,kk) - rsi(itemp,kk) ) / ( tevb(itemp+1) - tevb(itemp) )
         if (kk .eq. 0) return
      else
         rioniz = 0.0d0
      endif
c
      rrecomb = rre(itemp,kk) + ( temp - tevb(itemp) ) * ( rre(itemp+1,
     &   kk) - rre(itemp,kk) ) / ( tevb(itemp+1) - tevb(itemp) )
c
      rcxrecom = rrcx(itemp,kk) + ( temp - tevb(itemp) ) * ( rrcx(itemp+
     &   1,kk) - rrcx(itemp,kk) ) / ( tevb(itemp+1) - tevb(itemp) )

      return
      end
c-----End of subroutine imprates----------------------------------------

      subroutine mcrates(ne,tmpe,tmpi,za,zamax,zn,rion,rrec,rcxr)
cProlog
      implicit none
      doubleprecision ne,tmpe,tmpi
      integer za,zamax,zn
      doubleprecision rion, rrec, rcxr
c
c ... Inputs are:
c        electron density, ne;
c        electron temperature, tmpe;
c        neutral hydrogen temperature, tmpi, for charge-exchange;
c        atomic charge state, za;
c        maximum atomic charge state, zamax;
c        nuclear charge state, zn;

c ... Outputs are:
c        rate parameters (sigma*v) for ionization, recombination,
c        and charge-exchange recombination on neutral hydrogen
c
c     The tables used in this subroutine are generated with a code
c     supplied by Bas Braams.  The data file it produces is called
c     'b2frates' by default.  This gives rates that may depend on both
c     density and temperature.
c
c     Input electron density is given in [parts/m**3]
c     Input electron temperature is given in [J].
c     Input temperature for neutral hydrogen is given in [J/AMU].
c     Table densities are given in [parts/m**3]
c     Table temperatures are given in [eV].
c     Output and table rates are all given in [m**3/s].
c
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
c cutlo
c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2
c ev2
c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap

      double precision tevb ( ntev)
      pointer(ptevb,tevb)

      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)

      double precision rre ( ntev,1:nz)
      pointer(prre,rre)

      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)

      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)

      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)

      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)

      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)

      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)

      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)

      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)

      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)

      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)

      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)

      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)

      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)

      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge
c rtln,rtlt,rtlsa,rtlra,rtlcx,iscxfit,isrtndep
c
      integer i1e,i1i,i,ii,j1
      doubleprecision nenonz,y,dlogn,fy
      doubleprecision tmpenonz,tmpinonz,xte,xti,dlogt,fxte,fxti,lrion,
     &   lrrec
c
      doubleprecision rcxr_zn6, rcxr_zn6b
      external rcxr_zn6, rcxr_zn6b
c
      rion = 0.d0
      rrec = 0.d0
      rcxr = 0.d0
c
c to avoid possible log(0) error
      tmpenonz = max(tmpe, cutlo)
c to avoid possible log(0) error
      tmpinonz = max(tmpi, cutlo)
      xte = log(tmpenonz/ev2)
      xti = log(tmpinonz/ev2)
      dlogt = rtlt(1) - rtlt(0)
c
c ... Find index i1 in temperature table such that
c                 rtlt(i1) .le. xt .lt. rtlt(i1+1)
c     or, equivalently,
c                  rtt(i1) .le. tmp .lt. rtt(i1+1).
c
      i1e = int( (xte-rtlt(0))/dlogt )
      i1i = int( (xti-rtlt(0))/dlogt )
c
c ... For temperatures below minimum table temperature, extrapolate
c     downwards from table entries 0 and 1.
c
      i1e = max(0, i1e)
      i1i = max(0, i1i)
c
c ... For temperatures above maximum table temperature, extrapolate
c     upwards from table entries rtnt-1 and rtnt.
c
      i1e = min(rtnt-1, i1e)
      i1i = min(rtnt-1, i1i)
c
c ... Compute coefficient for linear interpolation.
c
      fxte = (xte-rtlt(i1e))/(rtlt(i1e+1)-rtlt(i1e))
      fxti = (xti-rtlt(i1i))/(rtlt(i1i+1)-rtlt(i1i))
c
c ... Now the density dependence --
c     Default is to use the lowest density in the table -
      j1 = 0
      fy = 0.d0
c     Otherwise, use linear interpolation -
      if (isrtndep .ne. 0) then
         nenonz = max(ne, cutlo)
         y = log(nenonz)
         dlogn = rtln(1) - rtln(0)
         j1 = int( (y-rtln(0))/dlogn )
         j1 = max(0, j1)
         j1 = min(rtnn-1, j1)
         fy = (y-rtln(j1))/(rtln(j1+1)-rtln(j1))
c        Do not extrapolate beyond table minimum and maximum densities
         fy = max(0.d0, fy)
         fy = min(1.d0, fy)
      endif
c
c ... For given za and zn, find the species index, ii, in the table.
c
      ii = -1
      do 23000 i=0,rtnsd-1
         if ((zn .eq. nint(rtzn(i))) .and. (za .eq. nint(rtza(i)))) then
            ii = i
            go to 23001
         endif
23000 continue
23001 continue
      if (ii .lt. 0) then
         write (*,*) '*** mcrates could not find za=',za,' zn=',zn
         write (*,*) '*** check mcfilenames array'
         call xerrab("")
      endif
c
c     Compute rate parameters for transitions from table species ii.
c
      if (za .lt. zamax) then
         lrion = ( fy)*((1-fxte)*rtlsa(i1e,j1+1,ii)+fxte*rtlsa(i1e+1,j1+
     &      1,ii)) + (1-fy)*((1-fxte)*rtlsa(i1e,j1 ,ii)+fxte*rtlsa(i1e+1
     &      ,j1 ,ii))
         rion = exp(lrion)
         if (za .eq. 0) return
      endif
      lrrec = ( fy)*((1-fxte)*rtlra(i1e,j1+1,ii)+fxte*rtlra(i1e+1,j1+1,
     &   ii)) + (1-fy)*((1-fxte)*rtlra(i1e,j1 ,ii)+fxte*rtlra(i1e+1,j1 ,
     &   ii))
      rrec = exp(lrrec)
      rcxr = exp((1-fxti)*rtlcx(i1i,0,ii)+fxti*rtlcx(i1i+1,0,ii))
c
c     Use special analytic fit for carbon c-x on neutral hydrogen.
c
      if ( (iscxfit .gt. 0) .and. (zn .eq. 6) .and. (za .le. zamax) ) 
     &      then
         if (iscxfit.ge.1.d0 .and. iscxfit.le.2.d0) then
            rcxr = (2.d0-iscxfit)*rcxr_zn6 (tmpi, za) + (iscxfit-1.d0)*
     &         rcxr_zn6b(tmpi, za)
         endif
ccc         if (iscxfit .eq. 1) rcxr = rcxr_zn6 (tmpi, za)
ccc         if (iscxfit .eq. 2) rcxr = rcxr_zn6b (tmpi, za)
      endif
c
      return
      end

c-----End of subroutine mcrates----------------------------------------

      doubleprecision function rcxr_zn6 (tmp, za)
cProlog
      implicit none
      doubleprecision tmp
      integer za
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
c cutlo
c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2
c ev2
c
c     Charge exchange rate parameter for carbon on neutral hydrogen.
c     Input (neutral hydrogen) temperature, tmp, is in [Joules/AMU].
c     Initial carbon charge state is za.
c     Output rate parameter (sigma-v) is in [m**3/sec].
c
c     This power-law fit was derived by Tom Rognlien from Figure 8.1
c     of a PhD thesis by C.F. Maggi on "Measurement and Interpretation
c     of Spectral Emission from JET Divertor Plasmas", January 1997,
c     JET report JET-IR(96)05.
c
c     local variables --
      doubleprecision x, m0(6), m1(6), m2(6)
      data m0/-16.104d0,-18.27d0,-14.48d0,-14.85d0,-14.213d0,-17.576d0/
      data m1/0.5335d0,2.3657d0,0.05715d0,0.5219d0,0.42193d0,1.8758d0/
      data m2/-0.0009571d0,-0.29616d0,0.080947d0,0.048885d0,-0.033125d0,
     &   -0.095951d0/

      x = log10(max(tmp, cutlo)/ev2)
      rcxr_zn6 = 10**( m0(za) + m1(za)*x + m2(za)*x*x )
c
      return
      end
c
c-------End of function rcxr_zn6---------------------------------------

      doubleprecision function rcxr_zn6b (tmp, za)
cProlog
      implicit none
      doubleprecision tmp
      integer za
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
c cutlo
c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2
c ev2
c
c     Charge exchange rate parameter for carbon on neutral hydrogen.
c     Input (neutral hydrogen) temperature, tmp, is in [Joules/AMU].
c     Initial carbon charge state is za.
c     Output rate parameter (sigma-v) is in [m**3/sec].
c
c     This is a modified of the function rcxr_zn6; only za=1 case is
c     changed to use a (lower) fit guided by plots from A. Pigarov.
c     Other za's same as for rxcr_zn6 from thesis by C.F. Maggi (fit
c     by T. Rognlien)
c
c     local variables --
      doubleprecision x, m0(6), m1(6), m2(6)
      data m0/-20.027d0,-18.27d0,-14.48d0,-14.85d0,-14.213d0,-17.576d0/
      data m1/3.6433d0,2.3657d0,0.05715d0,0.5219d0,0.42193d0,1.8758d0/
      data m2/-0.59189d0,-0.29616d0,0.080947d0,0.048885d0,-0.033125d0,
     &   -0.095951d0/

      x = log10(max(tmp, cutlo)/ev2)
      rcxr_zn6b = 10**( m0(za) + m1(za)*x + m2(za)*x*x )
c
      return
      end
c
c-------End of function rcxr_zn6b---------------------------------------

      subroutine readmc(nzdf,mcfilename)
cProlog

      implicit none
      integer nzdf
      character*256 mcfilename(*)
      character*256 fname
c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap

      double precision tevb ( ntev)
      pointer(ptevb,tevb)

      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)

      double precision rre ( ntev,1:nz)
      pointer(prre,rre)

      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)

      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)

      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)

      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)

      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)

      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)

      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)

      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)

      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)

      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)

      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)

      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)

      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)

      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge

c Group Impdata
      character*120 apidir
      common /api10003/ apidir
c End of Impdata
capidir

c ... Function:
c defined in the Basis runtime library
      integer utgetcl

c     local variables --
      integer i, ios, kstart, n, nget, rtnt_old, rtnn_old, rtnsd_old, kk
     &   , stringlen1, stringlen2, iprt_imp_file
      character idcod*8, idtyp*8, id1*32, mcfnuse*256

c     procedures --
      external freeus, gchange, xerrab

c ... Initialize iprt_imp_file on
      data iprt_imp_file/1/

c----------------------------------------------------------------------c
c     Read rate data from 'un*formatted' files.
c           (file format from b2.5 code by B. Braams)
c----------------------------------------------------------------------c

      do 23000 i=1,nzdf
         rtnt_old = rtnt
         rtnn_old = rtnn
         rtnsd_old = rtnsd

         mcfnuse = mcfilename(i)
         call freeus(nget)
         fname = TRIM(apidir) //'/'//TRIM(mcfnuse)
         open (nget, file=TRIM(apidir)//'/'//TRIM(mcfnuse), form=
     &      'formatted', iostat=ios, status='old')
         if (ios .ne. 0) then
            write(*,*) '*** Input file mcfilename = "', mcfilename(i), 
     &         '" not found.'
            call xerrab("")
         endif

c     read header --
c     un*formatted read for header data
         read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
         if (n .lt. 0 .and. iprt_imp_file .eq. 1) then
            write(*,*) '***Impurity file using new 2012 format is ',
     &         mcfilename(i)
            mcfformat(i) = 1
            iprt_imp_file = 0
         elseif (iprt_imp_file .eq. 1) then
            write(*,*) '***Impurity file using pre-2012 format is ',
     &         mcfilename(i)
            mcfformat(i) = 0
            iprt_imp_file = 0
         endif
         read (nget,'(1x,1a120)') labelrt(i)

c     read dimensions --
c     un*formatted read for integer data
         read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
         read (nget,*) rtnt,rtnn,rtns

c     Test for compatibility of (rtnt,rtnn) from different tables:
         if ( (i .gt. 1) .and. ((rtnt .ne. rtnt_old) .or. (rtnn .ne. 
     &      rtnn_old)) ) then
            write(*,*) 
     &         '*** subroutine readmc: incompatible table dimensions in 
     &', mcfilename(i),' and ',mcfilename(i-1)
            call xerrab("")
         endif

c     allocate storage --
         rtnsd=rtnsd+rtns
ccaution: can set vars, but not use here
         call gchange("Multicharge",0)

c     read abscissae and rates --
c starting species index for this table
         kstart=rtnsd_old
         do 23002 kk = kstart, kstart+rtns-1
            chgstate_format(kk) = mcfformat(i)
23002    continue

         call readmc1 (nget, kstart)

         close (nget)

23000 continue

      return
      end

c-----------------------------------------------------------------------

      subroutine readmc1 (nget, kstart)
cProlog
      implicit none
      integer nget, kstart
c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap

      double precision tevb ( ntev)
      pointer(ptevb,tevb)

      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)

      double precision rre ( ntev,1:nz)
      pointer(prre,rre)

      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)

      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)

      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)

      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)

      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)

      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)

      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)

      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)

      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)

      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)

      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)

      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)

      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)

      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge


c     local variables --
      integer i, j, k, n
      character idcod*8, idtyp*8, id1*32

c     read abscissae --
c     un*formatted read for real data

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtza(k),k=kstart,kstart+rtns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtzn(k),k=kstart,kstart+rtns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtza2(k),k=kstart,kstart+rtns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtt(i),i=0,rtnt)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtn(j),j=0,rtnn)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtlt(i),i=0,rtnt)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (rtln(j),j=0,rtnn)

c     read rate coefficients --
c     un*formatted read for real data

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((rtlsa(i,j,k),i=0,rtnt),j=0,rtnn), k=kstart,kstart
     &   +rtns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((rtlra(i,j,k),i=0,rtnt),j=0,rtnn), k=kstart,kstart
     &   +rtns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((rtlqa(i,j,k),i=0,rtnt),j=0,rtnn), k=kstart,kstart
     &   +rtns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((rtlcx(i,j,k),i=0,rtnt),j=0,rtnn), k=kstart,kstart
     &   +rtns-1)

      return
      end

c----------------------------------------------------------------------c

      function radmc(zmax, znuc, te, dene, denz, radz)
cProlog
      implicit none
      doubleprecision radmc
c ... input args
      integer zmax, znuc
      doubleprecision te, dene, denz(0:zmax)
c ... output args
      doubleprecision radz(0:zmax)
c
c ... Compute the radiation rates, radz(0:zmax), for all charge states
c     of an impurity with nuclear charge, znuc, and return the total
c     electron energy loss rate, radmc, including both the radiation
c     and binding energy contributions.
c
c     The tables used in this subroutine are generated with a code
c     supplied by Bas Braams.  The data file it produces is called
c     'b2frates' by default.  This gives rates that may depend on both
c     density and temperature.
c
c ... Input temperature te is in [J].
c     Input densities are in [/m**3].
c     Output rates are in [J/m**3/s].
c     Table temperatures are in [eV].
c     Table rate parameters are in [m**3/s] and [eV*m**3/s].
c
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
c cutlo
c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2
c ev2
c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap

      double precision tevb ( ntev)
      pointer(ptevb,tevb)

      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)

      double precision rre ( ntev,1:nz)
      pointer(prre,rre)

      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)

      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)

      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)

      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)

      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)

      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)

      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)

      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)

      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)

      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)

      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)

      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)

      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)

      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge
c rtln,rtlt,rtnn,rtnt,rtlqa,rtlsa,rtlra
c isrtndep,chgstate_format,ispradextrap
c
      doubleprecision ebindz
      external ebindz
c
      integer i1,k,k0,j1
      doubleprecision nenonz,y,dlogn,fy
      doubleprecision tenonz,xt,dlogt,fxt
      doubleprecision kionz,krecz,keelz,lionz,lrecz,leelz,fac_rad,
     &   temintab
c
c to avoid possible log(0) error
      tenonz = max(te, cutlo)
      xt = log(tenonz/ev2)
      dlogt = rtlt(1) - rtlt(0)

c ... Define minimum Te in table
      temintab = 0.2d0*ev2
c
c ... Find index i1 in table such that rtlt(i1) .le. xt .lt. rtlt(i1+1)
c     or, equivalently, rtt(i1) .le. te .lt. rtt(i1+1).
c
      i1 = int( (xt-rtlt(0))/dlogt )
c
c ... For temperatures below minimum table temperature, extrapolate
c     downwards from table entries 0 and 1.

      i1 = max(0, i1)
c
c ... For temperatures above maximum table temperature, extrapolate
c     upwards from table entries rtnt-1 and rtnt.

      i1 = min(rtnt-1, i1)
c
c ... Compute coefficient for linear interpolation.
c
      fxt = (xt-rtlt(i1))/(rtlt(i1+1)-rtlt(i1))
c
c ... Now the density dependence --
c     Default is to use the lowest density in the table -
      j1 = 0
      fy = 0.d0
c     Otherwise, use linear interpolation -
      if (isrtndep .ne. 0) then
         nenonz = max(dene, cutlo)
         y = log(nenonz)
         dlogn = rtln(1) - rtln(0)
         j1 = int( (y-rtln(0))/dlogn )
         j1 = max(0, j1)
         j1 = min(rtnn-1, j1)
         fy = (y-rtln(j1))/(rtln(j1+1)-rtln(j1))
c        Do not extrapolate beyond table minimum and maximum densities
         fy = max(0.d0, fy)
         fy = min(1.d0, fy)
      endif
c
c     Compute rates for each charge state and total rate:

c     First, find the species index of the neutral impurity atom
      k0 = -1
      do 23000 k=0,rtnsd-1
         if ((nint(rtzn(k)) .eq. znuc) .and. (nint(rtza(k)) .eq. 0)) 
     &         then
            k0 = k
            go to 23001
         endif
23000 continue
23001 continue
      if (k0 .lt. 0) then
         write (*,*) '*** radmc could not find za=',0,' zn=',znuc
         write (*,*) '*** check mcfilenames array'
         call xerrab("")
      endif

c total electron energy loss rate
      radmc = 0.d0
      do 23002 k=0,zmax
         lionz = ( fy)*((1-fxt)*rtlsa(i1,j1+1,k0+k)+fxt*rtlsa(i1+1,j1+1,
     &      k0+k))+ (1-fy)*((1-fxt)*rtlsa(i1,j1 ,k0+k)+fxt*rtlsa(i1+1,j1 
     &      ,k0+k))
         kionz = exp(lionz)
         lrecz = ( fy)*((1-fxt)*rtlra(i1,j1+1,k0+k)+fxt*rtlra(i1+1,j1+1,
     &      k0+k))+ (1-fy)*((1-fxt)*rtlra(i1,j1 ,k0+k)+fxt*rtlra(i1+1,j1 
     &      ,k0+k))
         krecz = exp(lrecz)
         leelz = ( fy)*((1-fxt)*rtlqa(i1,j1+1,k0+k)+fxt*rtlqa(i1+1,j1+1,
     &      k0+k))+ (1-fy)*((1-fxt)*rtlqa(i1,j1 ,k0+k)+fxt*rtlqa(i1+1,j1 
     &      ,k0+k))
         keelz = exp(leelz)
         fac_rad = 1.d0
         if (ispradextrap.eq.1 .and. k.eq.0 .and. te.lt.temintab) then
cextrap below min Te
            fac_rad = (te/(temintab))**6
         endif
         radz(k) = fac_rad*dene*denz(k)*keelz*ev2
         radmc = radmc + radz(k)
c     binding energy contributions:
         if (chgstate_format(k0+k) .eq. 0) then
cuse pre-2012 format definitions
            if (k .lt. zmax) then
c ionization
               radz(k) = radz(k) - dene*denz(k)*kionz*ebindz(k,znuc)*ev2
            endif
            if (k .gt. 0) then
c recombination
               radz(k) = radz(k) + dene*denz(k)*krecz*ebindz(k-1,znuc)*
     &            ev2
            endif
cuse new 2012 format definitions
         else
            if (k .lt. zmax) then
c ionization
               radmc = radmc + dene*denz(k)*kionz*ebindz(k,znuc)*ev2
            endif
            if (k .gt. 0) then
c recombination
               radmc = radmc - dene*denz(k)*krecz*ebindz(k-1,znuc)*ev2
            endif
         endif
23002 continue

      return
      end

c----------------------------------------------------------------------c

      function ebindz(zatomic, znuclear)
cProlog
      implicit none
      doubleprecision ebindz
      integer zatomic, znuclear

c     This function returns the ionization energy (eV) for an atom
c     with atomic charge, zatomic, and nuclear charge, znuclear.
c     Data is from CRC Handbook of Chemistry and Physics, except as noted.

      if (zatomic .ge. znuclear) then
         write (*,*) '*** ebindz: input error'
         write (*,*) ' zatomic=',zatomic,'   .ge.   znuclear=',znuclear
         call xerrab("")
      endif

      if (znuclear .eq. 1) then
c hydrogen
         if (zatomic .eq. 0) then
            ebindz=13.59844d0
         endif
      elseif (znuclear .eq. 2) then
c helium
         if (zatomic .eq. 0) then
            ebindz=24.58741d0
         elseif (zatomic .eq. 1) then
            ebindz=54.41778d0
         endif
      elseif (znuclear .eq. 3) then
c lithium
         if (zatomic .eq. 0) then
            ebindz=5.39172d0
         elseif (zatomic .eq. 1) then
            ebindz=75.64018d0
         elseif (zatomic .eq. 2) then
            ebindz=122.45429d0
         endif
      elseif (znuclear .eq. 4) then
c beryllium
         if (zatomic .eq. 0) then
            ebindz=9.32263d0
         elseif (zatomic .eq. 1) then
            ebindz=18.21116d0
         elseif (zatomic .eq. 2) then
            ebindz=153.89661d0
         elseif (zatomic .eq. 3) then
            ebindz=217.71865d0
         endif
      elseif (znuclear .eq. 5) then
c boron
         if (zatomic .eq. 0) then
            ebindz=8.29803d0
         elseif (zatomic .eq. 1) then
            ebindz=25.15484d0
         elseif (zatomic .eq. 2) then
            ebindz=37.93064d0
         elseif (zatomic .eq. 3) then
            ebindz=259.37521d0
         elseif (zatomic .eq. 4) then
            ebindz=340.22580d0
         endif
      elseif (znuclear .eq. 6) then
c carbon
         if (zatomic .eq. 0) then
            ebindz=11.26030d0
         elseif (zatomic .eq. 1) then
            ebindz=24.38332d0
         elseif (zatomic .eq. 2) then
            ebindz=47.8878d0
         elseif (zatomic .eq. 3) then
            ebindz=64.4939d0
         elseif (zatomic .eq. 4) then
            ebindz=392.087d0
         elseif (zatomic .eq. 5) then
            ebindz=489.99334d0
         endif
      elseif (znuclear .eq. 7) then
c nitrogen
         if (zatomic .eq. 0) then
            ebindz=14.53414d0
         elseif (zatomic .eq. 1) then
            ebindz=29.6013d0
         elseif (zatomic .eq. 2) then
            ebindz=47.44924d0
         elseif (zatomic .eq. 3) then
            ebindz=77.4735d0
         elseif (zatomic .eq. 4) then
            ebindz=97.8902d0
         elseif (zatomic .eq. 5) then
            ebindz=552.0718d0
         elseif (zatomic .eq. 6) then
            ebindz=667.046d0
         endif
      elseif (znuclear .eq. 8) then
c oxygen
         if (zatomic .eq. 0) then
            ebindz=13.61806d0
         elseif (zatomic .eq. 1) then
            ebindz=35.11730d0
         elseif (zatomic .eq. 2) then
            ebindz=54.9355d0
         elseif (zatomic .eq. 3) then
            ebindz=77.41353d0
         elseif (zatomic .eq. 4) then
            ebindz=113.8990d0
         elseif (zatomic .eq. 5) then
            ebindz=138.1197d0
         elseif (zatomic .eq. 6) then
            ebindz=739.29d0
         elseif (zatomic .eq. 7) then
            ebindz=871.4101d0
         endif
      elseif (znuclear .eq. 9) then
c fluorine
         if (zatomic .eq. 0) then
            ebindz=17.42282d0
         elseif (zatomic .eq. 1) then
            ebindz=34.97082d0
         elseif (zatomic .eq. 2) then
            ebindz=62.7084d0
         elseif (zatomic .eq. 3) then
            ebindz=87.1398d0
         elseif (zatomic .eq. 4) then
            ebindz=114.2428d0
         elseif (zatomic .eq. 5) then
            ebindz=157.1651d0
         elseif (zatomic .eq. 6) then
            ebindz=185.186d0
         elseif (zatomic .eq. 7) then
            ebindz=953.9112d0
         elseif (zatomic .eq. 8) then
            ebindz=1103.1176d0
         endif
      elseif (znuclear .eq. 10) then
c neon
         if (zatomic .eq. 0) then
            ebindz=21.56454d0
         elseif (zatomic .eq. 1) then
            ebindz=40.96328d0
         elseif (zatomic .eq. 2) then
            ebindz=63.45d0
         elseif (zatomic .eq. 3) then
            ebindz=97.12d0
         elseif (zatomic .eq. 4) then
            ebindz=126.21d0
         elseif (zatomic .eq. 5) then
            ebindz=157.93d0
         elseif (zatomic .eq. 6) then
            ebindz=207.2759d0
         elseif (zatomic .eq. 7) then
            ebindz=239.0989d0
         elseif (zatomic .eq. 8) then
            ebindz=1195.8286d0
         elseif (zatomic .eq. 9) then
            ebindz=1362.1995d0
         endif
      elseif (znuclear .eq. 18) then
c argon
         if (zatomic .eq. 0) then
            ebindz=15.75962d0
         elseif (zatomic .eq. 1) then
            ebindz=27.62967d0
         elseif (zatomic .eq. 2) then
            ebindz=40.74d0
         elseif (zatomic .eq. 3) then
            ebindz=59.81d0
         elseif (zatomic .eq. 4) then
            ebindz=75.02d0
         elseif (zatomic .eq. 5) then
            ebindz=91.009d0
         elseif (zatomic .eq. 6) then
            ebindz=124.323d0
         elseif (zatomic .eq. 7) then
            ebindz=143.460d0
         elseif (zatomic .eq. 8) then
            ebindz=422.45d0
         elseif (zatomic .eq. 9) then
            ebindz=478.69d0
         elseif (zatomic .eq. 10) then
            ebindz=538.96d0
         elseif (zatomic .eq. 11) then
            ebindz=618.26d0
         elseif (zatomic .eq. 12) then
            ebindz=686.10d0
         elseif (zatomic .eq. 13) then
            ebindz=755.74d0
         elseif (zatomic .eq. 14) then
            ebindz=854.77d0
         elseif (zatomic .eq. 15) then
            ebindz=918.03d0
         elseif (zatomic .eq. 16) then
            ebindz=4120.8857d0
         elseif (zatomic .eq. 17) then
            ebindz=4426.2296d0
         endif
      elseif (znuclear .eq. 36) then
c krypton from CRC; state 30 and above
         if (zatomic .eq. 0) then
c are arbitrary values-need updating
            ebindz=13.99961d0
         elseif (zatomic .eq. 1) then
            ebindz=24.35985d0
         elseif (zatomic .eq. 2) then
            ebindz=36.950d0
         elseif (zatomic .eq. 3) then
            ebindz=52.5d0
         elseif (zatomic .eq. 4) then
            ebindz=64.7d0
         elseif (zatomic .eq. 5) then
            ebindz=78.5d0
         elseif (zatomic .eq. 6) then
            ebindz=111.0d0
         elseif (zatomic .eq. 7) then
            ebindz=125.802d0
         elseif (zatomic .eq. 8) then
            ebindz=230.85d0
         elseif (zatomic .eq. 9) then
            ebindz=268.2d0
         elseif (zatomic .eq. 10) then
            ebindz=308.d0
         elseif (zatomic .eq. 11) then
            ebindz=350.d0
         elseif (zatomic .eq. 12) then
            ebindz=391.d0
         elseif (zatomic .eq. 13) then
            ebindz=447.d0
         elseif (zatomic .eq. 14) then
            ebindz=492.d0
         elseif (zatomic .eq. 15) then
            ebindz=541.d0
         elseif (zatomic .eq. 16) then
            ebindz=592.d0
         elseif (zatomic .eq. 17) then
            ebindz=641.d0
         elseif (zatomic .eq. 18) then
            ebindz=786.d0
         elseif (zatomic .eq. 19) then
            ebindz=833.d0
         elseif (zatomic .eq. 20) then
            ebindz=884.d0
         elseif (zatomic .eq. 21) then
            ebindz=937.d0
         elseif (zatomic .eq. 22) then
            ebindz=998.d0
         elseif (zatomic .eq. 23) then
            ebindz=1051.d0
         elseif (zatomic .eq. 24) then
            ebindz=1151.d0
         elseif (zatomic .eq. 25) then
            ebindz=1205.3d0
         elseif (zatomic .eq. 26) then
            ebindz=2928.d0
         elseif (zatomic .eq. 27) then
            ebindz=3070.d0
         elseif (zatomic .eq. 28) then
            ebindz=3227.d0
         elseif (zatomic .eq. 29) then
            ebindz=3381.d0
         elseif (zatomic .eq. 30) then
c guesses to fill out table
            ebindz=3500.d0
         elseif (zatomic .eq. 31) then
            ebindz=3700.d0
         elseif (zatomic .eq. 32) then
            ebindz=3900.d0
         elseif (zatomic .eq. 33) then
            ebindz=4100.d0
         elseif (zatomic .eq. 34) then
            ebindz=4300.d0
         elseif (zatomic .eq. 35) then
            ebindz=4500.d0
         endif
      elseif (znuclear .eq. 42) then
c molybdenum from ADAS
         if (zatomic .eq. 0) then
            ebindz=5.737d0
         elseif (zatomic .eq. 1) then
            ebindz=14.56d0
         elseif (zatomic .eq. 2) then
            ebindz=29.15d0
         elseif (zatomic .eq. 3) then
            ebindz=43.37d0
         elseif (zatomic .eq. 4) then
            ebindz=57.59d0
         elseif (zatomic .eq. 5) then
            ebindz=71.81d0
         elseif (zatomic .eq. 6) then
            ebindz=124.0d0
         elseif (zatomic .eq. 7) then
            ebindz=145.8d0
         elseif (zatomic .eq. 8) then
            ebindz=167.5d0
         elseif (zatomic .eq. 9) then
            ebindz=189.2d0
         elseif (zatomic .eq. 10) then
            ebindz=216.7d0
         elseif (zatomic .eq. 11) then
            ebindz=238.7d0
         elseif (zatomic .eq. 12) then
            ebindz=288.1d0
         elseif (zatomic .eq. 13) then
            ebindz=312.5d0
         elseif (zatomic .eq. 14) then
            ebindz=505.3d0
         elseif (zatomic .eq. 15) then
            ebindz=570.8d0
         elseif (zatomic .eq. 16) then
            ebindz=636.2d0
         elseif (zatomic .eq. 17) then
            ebindz=701.7d0
         elseif (zatomic .eq. 18) then
            ebindz=767.1d0
         elseif (zatomic .eq. 19) then
            ebindz=832.6d0
         elseif (zatomic .eq. 20) then
            ebindz=902.2d0
         elseif (zatomic .eq. 21) then
            ebindz=968.4d0
         elseif (zatomic .eq. 22) then
            ebindz=1034.d0
         elseif (zatomic .eq. 23) then
            ebindz=1101.d0
         elseif (zatomic .eq. 24) then
            ebindz=1305.d0
         elseif (zatomic .eq. 25) then
            ebindz=1368.d0
         elseif (zatomic .eq. 26) then
            ebindz=1431.d0
         elseif (zatomic .eq. 27) then
            ebindz=1494.d0
         elseif (zatomic .eq. 28) then
            ebindz=1591.d0
         elseif (zatomic .eq. 29) then
            ebindz=1655.d0
         elseif (zatomic .eq. 30) then
            ebindz=1805.d0
         elseif (zatomic .eq. 31) then
            ebindz=1869.d0
         elseif (zatomic .eq. 32) then
            ebindz=3990.d0
         elseif (zatomic .eq. 33) then
            ebindz=4191.d0
         elseif (zatomic .eq. 34) then
            ebindz=4392.d0
         elseif (zatomic .eq. 35) then
            ebindz=4593.d0
         elseif (zatomic .eq. 36) then
            ebindz=4902.d0
         elseif (zatomic .eq. 37) then
            ebindz=5110.d0
         elseif (zatomic .eq. 38) then
            ebindz=5407.d0
         elseif (zatomic .eq. 39) then
            ebindz=5585.d0
         elseif (zatomic .eq. 40) then
            ebindz=23120.d0
         elseif (zatomic .eq. 41) then
            ebindz=23890.d0
         endif
      elseif (znuclear .eq. 50) then
c tin
c Calculated by Jim Schofield at LLNL
c (via Howard Scott on 13 Sep 2000)
         if (zatomic .eq. 0) then
            ebindz=5.8d0
c            ebindz=7.34381             # CRC handbook value
         elseif (zatomic .eq. 1) then
            ebindz=12.9d0
c            ebindz=14.63225            # CRC handbook value
         elseif (zatomic .eq. 2) then
            ebindz=30.1d0
c            ebindz=30.50260            # CRC handbook value
         elseif (zatomic .eq. 3) then
            ebindz=40.6d0
c            ebindz=40.73502            # CRC handbook value
         elseif (zatomic .eq. 4) then
            ebindz=76.4d0
c            ebindz=72.28               # CRC handbook value
         elseif (zatomic .eq. 5) then
            ebindz=96.0d0
         elseif (zatomic .eq. 6) then
            ebindz=116.5d0
         elseif (zatomic .eq. 7) then
            ebindz=137.9d0
         elseif (zatomic .eq. 8) then
            ebindz=160.2d0
         elseif (zatomic .eq. 9) then
            ebindz=183.3d0
         elseif (zatomic .eq. 10) then
            ebindz=208.7d0
         elseif (zatomic .eq. 11) then
            ebindz=233.4d0
         elseif (zatomic .eq. 12) then
            ebindz=258.7d0
         elseif (zatomic .eq. 13) then
            ebindz=284.8d0
         elseif (zatomic .eq. 14) then
            ebindz=382.1d0
         elseif (zatomic .eq. 15) then
            ebindz=410.5d0
         elseif (zatomic .eq. 16) then
            ebindz=439.4d0
         elseif (zatomic .eq. 17) then
            ebindz=468.6d0
         elseif (zatomic .eq. 18) then
            ebindz=509.7d0
         elseif (zatomic .eq. 19) then
            ebindz=540.3d0
         elseif (zatomic .eq. 20) then
            ebindz=615.0d0
         elseif (zatomic .eq. 21) then
            ebindz=647.6d0
         elseif (zatomic .eq. 22) then
            ebindz=1132.7d0
         elseif (zatomic .eq. 23) then
            ebindz=1204.6d0
         elseif (zatomic .eq. 24) then
            ebindz=1278.0d0
         elseif (zatomic .eq. 25) then
            ebindz=1352.8d0
         elseif (zatomic .eq. 26) then
            ebindz=1429.2d0
         elseif (zatomic .eq. 27) then
            ebindz=1507.0d0
         elseif (zatomic .eq. 28) then
            ebindz=1597.7d0
         elseif (zatomic .eq. 29) then
            ebindz=1679.0d0
         elseif (zatomic .eq. 30) then
            ebindz=1761.6d0
         elseif (zatomic .eq. 31) then
            ebindz=1845.6d0
         elseif (zatomic .eq. 32) then
            ebindz=2082.5d0
         elseif (zatomic .eq. 33) then
            ebindz=2157.8d0
         elseif (zatomic .eq. 34) then
            ebindz=2233.8d0
         elseif (zatomic .eq. 35) then
            ebindz=2310.2d0
         elseif (zatomic .eq. 36) then
            ebindz=2446.8d0
         elseif (zatomic .eq. 37) then
            ebindz=2526.1d0
         elseif (zatomic .eq. 38) then
            ebindz=2683.87d0
         elseif (zatomic .eq. 39) then
            ebindz=2762.49d0
         elseif (zatomic .eq. 40) then
            ebindz=6415.48d0
         elseif (zatomic .eq. 41) then
            ebindz=6627.3d0
         elseif (zatomic .eq. 42) then
            ebindz=6841.0d0
         elseif (zatomic .eq. 43) then
            ebindz=7055.9d0
         elseif (zatomic .eq. 44) then
            ebindz=7536.3d0
         elseif (zatomic .eq. 45) then
            ebindz=7762.9d0
         elseif (zatomic .eq. 46) then
            ebindz=8107.20d0
         elseif (zatomic .eq. 47) then
            ebindz=8306.99d0
         elseif (zatomic .eq. 48) then
            ebindz=34256.71d0
         elseif (zatomic .eq. 49) then
            ebindz=35192.32d0
         endif
      elseif (znuclear .eq. 74) then
c tungsten from ADAS
         if (zatomic .eq. 0) then
            ebindz=7.130d0
         elseif (zatomic .eq. 1) then
            ebindz=15.08d0
         elseif (zatomic .eq. 2) then
            ebindz=25.43d0
         elseif (zatomic .eq. 3) then
            ebindz=39.29d0
         elseif (zatomic .eq. 4) then
            ebindz=53.15d0
         elseif (zatomic .eq. 5) then
            ebindz=67.01d0
         elseif (zatomic .eq. 6) then
            ebindz=119.7d0
         elseif (zatomic .eq. 7) then
            ebindz=140.8d0
         elseif (zatomic .eq. 8) then
            ebindz=162.0d0
         elseif (zatomic .eq. 9) then
            ebindz=183.1d0
         elseif (zatomic .eq. 10) then
            ebindz=204.2d0
         elseif (zatomic .eq. 11) then
            ebindz=240.5d0
         elseif (zatomic .eq. 12) then
            ebindz=263.1d0
         elseif (zatomic .eq. 13) then
            ebindz=294.6d0
         elseif (zatomic .eq. 14) then
            ebindz=339.9d0
         elseif (zatomic .eq. 15) then
            ebindz=369.9d0
         elseif (zatomic .eq. 16) then
            ebindz=395.0d0
         elseif (zatomic .eq. 17) then
            ebindz=435.5d0
         elseif (zatomic .eq. 18) then
            ebindz=480.8d0
         elseif (zatomic .eq. 19) then
            ebindz=526.1d0
         elseif (zatomic .eq. 20) then
            ebindz=571.4d0
         elseif (zatomic .eq. 21) then
            ebindz=616.7d0
         elseif (zatomic .eq. 22) then
            ebindz=664.6d0
         elseif (zatomic .eq. 23) then
            ebindz=710.2d0
         elseif (zatomic .eq. 24) then
            ebindz=755.8d0
         elseif (zatomic .eq. 25) then
            ebindz=801.4d0
         elseif (zatomic .eq. 26) then
            ebindz=846.9d0
         elseif (zatomic .eq. 27) then
            ebindz=892.5d0
         elseif (zatomic .eq. 28) then
            ebindz=1154.d0
         elseif (zatomic .eq. 29) then
            ebindz=1206.d0
         elseif (zatomic .eq. 30) then
            ebindz=1259.d0
         elseif (zatomic .eq. 31) then
            ebindz=1312.d0
         elseif (zatomic .eq. 32) then
            ebindz=1365.d0
         elseif (zatomic .eq. 33) then
            ebindz=1417.d0
         elseif (zatomic .eq. 34) then
            ebindz=1483.d0
         elseif (zatomic .eq. 35) then
            ebindz=1537.d0
         elseif (zatomic .eq. 36) then
            ebindz=1591.d0
         elseif (zatomic .eq. 37) then
            ebindz=1645.d0
         elseif (zatomic .eq. 38) then
            ebindz=1870.d0
         elseif (zatomic .eq. 39) then
            ebindz=1926.d0
         elseif (zatomic .eq. 40) then
            ebindz=1981.d0
         elseif (zatomic .eq. 41) then
            ebindz=2037.d0
         elseif (zatomic .eq. 42) then
            ebindz=2163.d0
         elseif (zatomic .eq. 43) then
            ebindz=2223.d0
         elseif (zatomic .eq. 44) then
            ebindz=2386.d0
         elseif (zatomic .eq. 45) then
            ebindz=2447.d0
         elseif (zatomic .eq. 46) then
            ebindz=3734.d0
         elseif (zatomic .eq. 47) then
            ebindz=3882.d0
         elseif (zatomic .eq. 48) then
            ebindz=4029.d0
         elseif (zatomic .eq. 49) then
            ebindz=4177.d0
         elseif (zatomic .eq. 50) then
            ebindz=4325.d0
         elseif (zatomic .eq. 51) then
            ebindz=4472.d0
         elseif (zatomic .eq. 52) then
            ebindz=4684.d0
         elseif (zatomic .eq. 53) then
            ebindz=4836.d0
         elseif (zatomic .eq. 54) then
            ebindz=4987.d0
         elseif (zatomic .eq. 55) then
            ebindz=5139.d0
         elseif (zatomic .eq. 56) then
            ebindz=5538.d0
         elseif (zatomic .eq. 57) then
            ebindz=5671.d0
         elseif (zatomic .eq. 58) then
            ebindz=5803.d0
         elseif (zatomic .eq. 59) then
            ebindz=5936.d0
         elseif (zatomic .eq. 60) then
            ebindz=6468.d0
         elseif (zatomic .eq. 61) then
            ebindz=6611.d0
         elseif (zatomic .eq. 62) then
            ebindz=6919.d0
         elseif (zatomic .eq. 63) then
            ebindz=7055.d0
         elseif (zatomic .eq. 64) then
            ebindz=14760.d0
         elseif (zatomic .eq. 65) then
            ebindz=15140.d0
         elseif (zatomic .eq. 66) then
            ebindz=15520.d0
         elseif (zatomic .eq. 67) then
            ebindz=15900.d0
         elseif (zatomic .eq. 68) then
            ebindz=17630.d0
         elseif (zatomic .eq. 69) then
            ebindz=18060.d0
         elseif (zatomic .eq. 70) then
            ebindz=18800.d0
         elseif (zatomic .eq. 71) then
            ebindz=19150.d0
         elseif (zatomic .eq. 72) then
            ebindz=77510.d0
         elseif (zatomic .eq. 73) then
            ebindz=78990.d0
         endif
c data not available
      else
         write (*,*) '*** ebindz: no binding energy data'
         write (*,*) '    for znuclear=',znuclear,', zatomic=',zatomic
         call xerrab("")
      endif

      return
      end

c----------------------------------------------------------------------c

