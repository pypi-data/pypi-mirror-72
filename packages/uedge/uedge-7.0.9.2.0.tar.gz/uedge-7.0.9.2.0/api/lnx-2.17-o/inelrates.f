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
c     ./../inelrates.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































      subroutine inelinput (impflag, crniarg, ctemparg, zqarg, nzarg)
cProlog
c
c    this subroutine reads impurity rate information
c
      implicit none
c
c ... Input arguments:
      integer impflag, nzarg
      doubleprecision ctemparg, crniarg, zqarg(nzarg)
c
c ... Common blocks:
c Group Normalization_constants
      double precision crni, ctemp
      common /api23/ crni, ctemp
c End of Normalization_constants
c crni,ctemp
c Group Input
      character*(256) inelrates(1)
      character*(256) inelrad(1)
      character*(256) inelmc(1)
      common /api10000/ inelrates
      common /api10001/ inelrad
      common /api10002/ inelmc
c End of Input
c inelrates,inelrad,inelmc
c Group Radiation
      double precision terad(40), xno(40), rntau(40)
      double precision radrate(40,40,40)
      double precision avgz(40,40,40)
      double precision avgz2(40,40,40)
      integer ncaset, ncaseno, ncasent
      common /api80/ ncaset, ncaseno, ncasent
      common /api83/ terad, xno, rntau, radrate, avgz, avgz2
c End of Radiation
c ncaset,ncaseno,ncasent,terad,xno,rntau,
c radrate,avgz,avgz2
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
c ntev,nz,tevb,rsi,rre,rpwr,rrcx
c Group Impurity_charge
      integer nnz

      double precision zq ( nnz)
      pointer(pzq,zq)
      common /api110/ nnz
      common /api116/ pzq
c End of Impurity_charge
c zq

      namelist/inrad/ terad, xno, rntau, radrate, avgz, avgz2
c
c ... Local variables:
      integer us, ios
      integer i, j, k
      doubleprecision rl, cs
c
c ... Store constants for conversions to MKS units.
      crni = crniarg
      ctemp = ctemparg

c ... Set constants so that rates are unchanged from MKS rates.
      rl = 1.d0
      cs = 1.d0
c
c ... Allocate memory for rates and radiation info.
      call gallot("Radiation",0)
c
c----------------------------------------------------------------------c
      if (impflag .eq. 1) then
c----------------------------------------------------------------------c
c
c ... Read in rate tables from namelist inrad in the file whose name
c     is given in the variable inelrad (formerly carbavg.dat).
         call freeus (us)
         open (us, file=inelrad(1), form='formatted', iostat=ios, status
     &      ='old')
         if (ios .ne. 0) then
            write (*,*) '*** Input file inelrad=', inelrad(1), 
     &         ' not found'
            call xerrab("")
         endif
         read(us,inrad)
         close (us)
c
         do 102 i = 1,ncaset
            terad(i)=terad(i)*1.602d-19/ctemp
  102       continue
c
         do 103 i = 1,ncasent
            rntau(i)=rntau(i)*crni*rl/cs
  103       continue
c
c
         do 111 i = 1,ncaset
            do 111 j = 1,ncaseno
               do 111 k = 1,ncasent
c
                  radrate(i,j,k)=radrate(i,j,k)*crni*rl*1.602d-19 /cs/
     &               ctemp/1.5d0
c
  111             continue
c
c----------------------------------------------------------------------c
      elseif (impflag .eq. 2) then
c----------------------------------------------------------------------c
c
c     read in multi charge state data (e.g., file 'carbmc.dat')
c
c
         if (nzarg .gt. 6) then
            write (*,*) '*** inelinput -- format of file ', inelmc(1), 
     &         ' may be incompatible with format statements'
         endif
         nnz = nzarg
         call gallot("Multicharge",0)
         call gallot("Impurity_charge",0)
c
         do 23005 k = 1,nzarg
            zq(k) = dble(k)
            if (abs(zq(k) - zqarg(k)) .gt. 1.d-4) then
               call remark( 
     &            '*** Routine inelinput -- bbb.ziin incompatible with')
               call remark( 
     &            '          assumptions of multi-charge state model')
               call xerrab("")
            endif
23005    continue
c
         call freeus (us)
         open (us, file=inelmc(1), form='formatted', iostat=ios, status=
     &      'old')
         if (ios .ne. 0) then
            write (*,*) '*** Input file inelmc=', inelmc(1), 
     &         ' not found'
            call xerrab("")
         endif
c
c   ionization rate
c
         do 200 i = 1,ntev
            read(us,1000) tevb(i),(rsi(i,k),k=0,nz-1)
            do 201 k = 0,nz-1
  201          rsi(i,k) = rsi(i,k)*crni*rl/cs
  200       continue
c
c   recombination rate
c
         do 210 i = 1,ntev
            read(us,1000) tevb(i),(rre(i,k),k=1,nz)
            do 211 k = 1,nz
  211          rre(i,k) = rre(i,k)*crni*rl/cs
  210       continue
c
c   radiative power rate
c
         do 220 i = 1,ntev
            read(us,1001) tevb(i),(rpwr(i,k),k=0,nz)
c       write(*,*) i,(rpwr(i,k),k=0,nz)
            do 221 k = 0,nz
               rpwr(i,k) = rpwr(i,k)*crni*rl*1.602d-19 /cs/ctemp/1.5d0
  221          continue
  220       continue
c
c   CX recomb. rate
c
         do 230 i = 1,ntev
            read(us,1000) tevb(i),(rrcx(i,k),k=1,nz)
            do 231 k = 1,nz
  231          rrcx(i,k) = rrcx(i,k)*crni*rl/cs
  230       continue
c
c ... Scale temperature scale for multi-charge rates to code units.
         do 23015 i = 1, ntev
            tevb(i)=tevb(i)*1.602d-19/ctemp
23015    continue
c
         close (us)
c----------------------------------------------------------------------c
      endif
c----------------------------------------------------------------------c
 1000 format(7(1pe12.4))
 1001 format(8(1pe12.4))
c
      return
      end
c-----End of subroutine inelinput-----

      function radneq(temp,rnone)
cProlog
c
c ... This function computes the factor that must be multiplied by
c     (electron density) * (impurity density) to yield the impurity
c     radiation rate.
c
      implicit none
c
      doubleprecision radneq, temp, rnone, radup, raddwn
c
      integer itloc, jdloc, kloc, itbnd, jdbnd, i, j
c
c ... Common blocks:
c Group Radiation
      double precision terad(40), xno(40), rntau(40)
      double precision radrate(40,40,40)
      double precision avgz(40,40,40)
      double precision avgz2(40,40,40)
      integer ncaset, ncaseno, ncasent
      common /api80/ ncaset, ncaseno, ncasent
      common /api83/ terad, xno, rntau, radrate, avgz, avgz2
c End of Radiation
c ncaset,ncaseno,terad,xno,radrate
c
c *****************************************
c
c   locate table position
c
      itloc = ncaset
      jdloc = ncaseno
      kloc = 1
c
      do 10 i = 1,ncaset
c
         if ( terad(i) .gt. temp ) then
            itloc = i
            goto 11
         endif
c
   10    continue
   11 continue
c
      do 20 j = 1,ncaseno
c
         if ( xno(j) .gt. rnone ) then
            jdloc = j
            goto 21
         endif
c
   20    continue
   21 continue
c
      itbnd = 0
      jdbnd = 0
c
      if ( itloc .eq. 1 .or. itloc .eq. ncaset ) itbnd = 1
      if ( jdloc .eq. 1 .or. jdloc .eq. ncaseno )jdbnd = 1
c
      if ( itbnd .ne. 1 .and. jdbnd .ne. 1 ) then
c
c
         radup = radrate(itloc-1,jdloc,kloc)*(terad(itloc)-temp) /(terad
     &      (itloc)-terad(itloc-1)) + radrate(itloc,jdloc,kloc)*(temp-
     &      terad(itloc-1)) /(terad(itloc)-terad(itloc-1))
c
         raddwn = radrate(itloc-1,jdloc-1,kloc)*(terad(itloc)-temp) /(
     &      terad(itloc)-terad(itloc-1)) + radrate(itloc,jdloc-1,kloc)*(
     &      temp-terad(itloc-1)) /(terad(itloc)-terad(itloc-1))
c
         radneq = raddwn*(xno(jdloc)-rnone) /(xno(jdloc)-xno(jdloc-1)) + 
     &      radup*(rnone-xno(jdloc-1)) /(xno(jdloc)-xno(jdloc-1))
c
c
      elseif ( itbnd .eq. 1 .and. jdbnd .ne. 1 ) then
c
         radneq = radrate(itloc,jdloc-1,kloc)*(xno(jdloc)-rnone) /(xno(
     &      jdloc)-xno(jdloc-1)) + radrate(itloc,jdloc,kloc)*(rnone-xno(
     &      jdloc-1)) /(xno(jdloc)-xno(jdloc-1))
c
      elseif ( jdbnd .eq. 1 .and. itbnd .ne. 1 ) then
c
         radneq = radrate(itloc-1,jdloc,kloc)*(terad(itloc)-temp) /(
     &      terad(itloc)-terad(itloc-1)) + radrate(itloc,jdloc,kloc)*(
     &      temp-terad(itloc-1)) /(terad(itloc)-terad(itloc-1))
c
      else
c
         radneq = radrate(itloc,jdloc,kloc)
c
      endif
c
      return
      end
c-----End of function radneq-----

      function zimp(temp)
cProlog
c
c   this function computes imp. avgz
c   [note that dependence on rnone (=(neutral density)/(electron density))
c   is ignored (rnone=0), as is dependence on confinement time (kloc=1)]
      implicit none
c
      doubleprecision zimp, temp, rnone, zimpup, zimpdwn
c
      integer itloc, jdloc, kloc, itbnd, jdbnd, i, j
c
c ... Common blocks:
c Group Radiation
      double precision terad(40), xno(40), rntau(40)
      double precision radrate(40,40,40)
      double precision avgz(40,40,40)
      double precision avgz2(40,40,40)
      integer ncaset, ncaseno, ncasent
      common /api80/ ncaset, ncaseno, ncasent
      common /api83/ terad, xno, rntau, radrate, avgz, avgz2
c End of Radiation
c ncaset,ncaseno,terad,xno,avgz
c
c *****************************************
c
c   locate table position
c
      itloc = ncaset
      jdloc = ncaseno
      kloc = 1
c
      do 10 i = 1,ncaset
c
         if ( terad(i) .gt. temp ) then
            itloc = i
            goto 11
         endif
c
   10    continue
   11 continue
c
      rnone = 0.d0
      do 20 j = 1,ncaseno
c
         if ( xno(j) .gt. rnone ) then
            jdloc = j
            goto 21
         endif
c
   20    continue
   21 continue
c
      itbnd = 0
      jdbnd = 0
c
      if ( itloc .eq. 1 .or. itloc .eq. ncaset ) itbnd = 1
      if ( jdloc .eq. 1 .or. jdloc .eq. ncaseno )jdbnd = 1
c
      if ( itbnd .ne. 1 .and. jdbnd .ne. 1 ) then
c
c
         zimpup = avgz(itloc-1,jdloc,kloc)*(terad(itloc)-temp) /(terad(
     &      itloc)-terad(itloc-1)) + avgz(itloc,jdloc,kloc)*(temp-terad(
     &      itloc-1)) /(terad(itloc)-terad(itloc-1))
c
         zimpdwn = avgz(itloc-1,jdloc-1,kloc)*(terad(itloc)-temp) /(
     &      terad(itloc)-terad(itloc-1)) + avgz(itloc,jdloc-1,kloc)*(
     &      temp-terad(itloc-1)) /(terad(itloc)-terad(itloc-1))
c
         zimp = zimpdwn*(xno(jdloc)-rnone) /(xno(jdloc)-xno(jdloc-1)) + 
     &      zimpup*(rnone-xno(jdloc-1)) /(xno(jdloc)-xno(jdloc-1))
c
c
      elseif ( itbnd .eq. 1 .and. jdbnd .ne. 1 ) then
c
         zimp = avgz(itloc,jdloc-1,kloc)*(xno(jdloc)-rnone) /(xno(jdloc)
     &      -xno(jdloc-1)) + avgz(itloc,jdloc,kloc)*(rnone-xno(jdloc-1)) 
     &      /(xno(jdloc)-xno(jdloc-1))
c
      elseif ( jdbnd .eq. 1 .and. itbnd .ne. 1 ) then
c
         zimp = avgz(itloc-1,jdloc,kloc)*(terad(itloc)-temp) /(terad(
     &      itloc)-terad(itloc-1)) + avgz(itloc,jdloc,kloc)*(temp-terad(
     &      itloc-1)) /(terad(itloc)-terad(itloc-1))
c
      else
c
         zimp = avgz(itloc,jdloc,kloc)
c
      endif
c
c
      return
      end
c-----End of function zimp-----

      function radimpmc(nzarg,tep,rnep,rimpp,radpwr)
cProlog
c
c  this function computes the impurity radiation source term
c
      implicit none
c
      doubleprecision radimpmc
c
c     input variables
c
      integer nzarg
      doubleprecision tep, rnep
      doubleprecision rimpp(0:nzarg)
c
c     output variable
c
      doubleprecision radpwr(0:nzarg)
c
c   common blocks
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
c ntev,tevb,rpwr
c
c   local variables
c
      integer itemp, kk
      doubleprecision xltemn, dlogte, temp
c
c ************************************************************
c
c    obtain power radiation rates at Te = tep
c    Note:  no scaling of temperatures is done here, so tep and tevb
c    must be provided in the same set of units.  tevb may not be in eV.
c
      xltemn = log10(tevb(1))
      dlogte = log10(tevb(2)) - xltemn
c
      temp = tep
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
c      write(*,*)'temp,itemp,xltemn,dlogte=',
c     .           temp,itemp,xltemn,dlogte
c
      do 2 kk = 1,nzarg
c
         radpwr(kk) = rpwr(itemp,kk) + ( temp - tevb(itemp) ) * ( rpwr(
     &      itemp+1,kk) - rpwr(itemp,kk) ) / ( tevb(itemp+1) - tevb(
     &      itemp) )
c
    2    continue
c
c      write(*,*)'radpwr(1)=',radpwr(1)
c      write(*,*)'rpwr(itemp,1)=',rpwr(itemp,1)
c   compute sink term radimpmc
c
      radimpmc = 0.d0
c
      do 10 kk = 1,nzarg
         radpwr(kk) = rimpp(kk)*radpwr(kk)*rnep
         radimpmc = radimpmc + radpwr(kk)
   10    continue
c
      return
      end
c-----End of function radimpmc-----


