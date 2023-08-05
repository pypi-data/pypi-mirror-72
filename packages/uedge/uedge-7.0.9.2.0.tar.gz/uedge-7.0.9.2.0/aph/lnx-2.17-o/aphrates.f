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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/aph.d
c     ./../aphrates.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c







































































c-----------------------------------------------------------------------
      doubleprecision function erl1 (te, ne, tau)
cProlog
      implicit none
      doubleprecision te, ne, tau
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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
c istabon
c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev
c Group Data_input
      character*120 aphdir
      character*120 data_directory
      double precision sgvcxc
      integer issgvcxc, isaphdir
      common /aph10/ issgvcxc, isaphdir
      common /aph10000/ aphdir
      common /aph10001/ data_directory
      common /aph13/ sgvcxc
c End of Data_input

c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt

      double precision htza ( 0:htns-1)
      pointer(phtza,htza)

      double precision htzn ( 0:htns-1)
      pointer(phtzn,htzn)

      double precision htn ( 0:htnn)
      pointer(phtn,htn)

      double precision htt ( 0:htnt)
      pointer(phtt,htt)

      double precision htln ( 0:htnn)
      pointer(phtln,htln)

      double precision htlt ( 0:htnt)
      pointer(phtlt,htlt)

      double precision htlsa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlsa,htlsa)

      double precision htlra ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlra,htlra)

      double precision htlcx ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlcx,htlcx)

      double precision htlqa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlqa,htlqa)
      common /aph10002/ labelht
      common /aph30/ htns, htnn, htnt
      common /aph36/ phtza, phtzn, phtn, phtt
      common /aph36/ phtln, phtlt, phtlsa
      common /aph36/ phtlra, phtlcx, phtlqa
c End of Rtdata

c Group Rtdegas
      double precision rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      double precision rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      double precision deltau
      integer mpe, mpd, mpr

      double precision wsveh ( mpe,mpd,mpr)
      pointer(pwsveh,wsveh)

      double precision wsveh0 ( mpe,mpd,mpr)
      pointer(pwsveh0,wsveh0)

      double precision wlemiss ( mpe,mpd)
      pointer(pwlemiss,wlemiss)

      double precision welms ( mpe,mpd)
      pointer(pwelms,welms)

      double precision welms1 ( mpe,mpd,mpr)
      pointer(pwelms1,welms1)

      double precision welms2 ( mpe,mpd,mpr)
      pointer(pwelms2,welms2)

      double precision pne3 ( mpe,mpd)
      pointer(ppne3,pne3)

      double precision pne31 ( mpe,mpd)
      pointer(ppne31,pne31)

      double precision pne32 ( mpe,mpd)
      pointer(ppne32,pne32)

      double precision pne2 ( mpe,mpd)
      pointer(ppne2,pne2)

      double precision pne21 ( mpe,mpd)
      pointer(ppne21,pne21)

      double precision pne22 ( mpe,mpd)
      pointer(ppne22,pne22)

      double precision pne41 ( mpe,mpd)
      pointer(ppne41,pne41)

      double precision pne42 ( mpe,mpd)
      pointer(ppne42,pne42)

      double precision pne51 ( mpe,mpd)
      pointer(ppne51,pne51)

      double precision pne52 ( mpe,mpd)
      pointer(ppne52,pne52)

      double precision pne61 ( mpe,mpd)
      pointer(ppne61,pne61)

      double precision pne62 ( mpe,mpd)
      pointer(ppne62,pne62)

      double precision pne71 ( mpe,mpd)
      pointer(ppne71,pne71)

      double precision pne72 ( mpe,mpd)
      pointer(ppne72,pne72)

      double precision pne81 ( mpe,mpd)
      pointer(ppne81,pne81)

      double precision pne82 ( mpe,mpd)
      pointer(ppne82,pne82)

      double precision pne91 ( mpe,mpd)
      pointer(ppne91,pne91)

      double precision pne92 ( mpe,mpd)
      pointer(ppne92,pne92)

      double precision svdum2 ( mpe,mpe)
      pointer(psvdum2,svdum2)

      double precision svphcx ( mpe,mpe)
      pointer(psvphcx,svphcx)

      double precision ekpt ( mpe)
      pointer(pekpt,ekpt)

      double precision dkpt ( mpd)
      pointer(pdkpt,dkpt)
      common /aph40/ mpe, mpd, mpr
      common /aph43/ rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      common /aph43/ rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      common /aph43/ deltau
      common /aph46/ pwsveh, pwsveh0, pwlemiss
      common /aph46/ pwelms, pwelms1, pwelms2
      common /aph46/ ppne3, ppne31, ppne32
      common /aph46/ ppne2, ppne21, ppne22
      common /aph46/ ppne41, ppne42, ppne51
      common /aph46/ ppne52, ppne61, ppne62
      common /aph46/ ppne71, ppne72, ppne81
      common /aph46/ ppne82, ppne91, ppne92
      common /aph46/ psvdum2, psvphcx, pekpt
      common /aph46/ pdkpt
c End of Rtdegas


c     local variables --
      integer je,jd,jr
      doubleprecision zloge,zlogd,zlogr,rle,rld,fje,fjd,fjr, erl111,
     &   erl112,erl121,erl122,erl11,erl12

c     procedures --
      doubleprecision rqa, rsa
      external rqa, rsa

c     Compute electron radiation loss rate per neutral H atom due to
c     "ionization" processes - D. Stotler's "coupling to the ground state"
c     te [J]          = electron temperature
c     ne [/m**3]      = electron density
c     erl1 [J/sec]    = radiation rate

c----------------------------------------------------------------------c
      if (istabon .le. 7) then
c various older models

         erl1 = (rqa(te,ne,0)-13.6d0*ev*rsa(te,ne,0.d0,0))*ne

c----------------------------------------------------------------------c
      elseif (istabon .eq. 8 .or. istabon .eq. 9) then
c linear interpolation

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     radiation rate --
         erl111=welms1(je,jd,jr)
         erl112=welms1(je,jd+1,jr)
         erl121=welms1(je+1,jd,jr)
         erl122=welms1(je+1,jd+1,jr)
         erl11=erl111+fjd*(erl112-erl111)
         erl12=erl121+fjd*(erl122-erl121)
         erl1 = erl11 + fje*(erl12-erl11)

c----------------------------------------------------------------------c
      elseif (istabon.gt.9 .and. istabon.lt.14) then
c logarith. interp on Stotler-95

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     radiation rate --
         erl111=log( welms1(je,jd,jr) )
         erl112=log( welms1(je,jd+1,jr) )
         erl121=log( welms1(je+1,jd,jr) )
         erl122=log( welms1(je+1,jd+1,jr) )
         erl11=erl111+fjd*(erl112-erl111)
         erl12=erl121+fjd*(erl122-erl121)
         erl1 = exp( erl11 + fje*(erl12-erl11) )

c----------------------------------------------------------------------c
      elseif (istabon.gt.13 .and. istabon.lt.16) then
c spatially-dependent

         if (tau.le.taumin) then
            jr = 1
            fjr = tau/taumin
         else
            zlogr = log10(tau/taumin)/deltau + 2.d0
            zlogr = min(zlogr,dble(mpr-1))
            jr = int(zlogr)
            fjr = zlogr - jr
         endif

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     radiation rate --
         if (istabon .eq. 14) then
            erl111=(1.d0-fjr)*welms1(je,jd,jr) + fjr *welms1(je,jd,jr+1)
            erl112=(1.d0-fjr)*welms1(je,jd+1,jr) + fjr *welms1(je,jd+1,
     &         jr+1)
            erl121=(1.d0-fjr)*welms1(je+1,jd,jr) + fjr *welms1(je+1,jd,
     &         jr+1)
            erl122=(1.d0-fjr)*welms1(je+1,jd+1,jr) + fjr *welms1(je+1,jd
     &         +1,jr+1)
            erl11=erl111+fjd*(erl112-erl111)
            erl12=erl121+fjd*(erl122-erl121)
            erl1 = erl11 + fje*(erl12-erl11)
         elseif (istabon .eq. 15) then
            erl111=(1.d0-fjr)*log( welms1(je,jd,jr) ) + fjr *log( welms1
     &         (je,jd,jr+1) )
            erl112=(1.d0-fjr)*log( welms1(je,jd+1,jr) ) + fjr *log( 
     &         welms1(je,jd+1,jr+1) )
            erl121=(1.d0-fjr)*log( welms1(je+1,jd,jr) ) + fjr *log( 
     &         welms1(je+1,jd,jr+1) )
            erl122=(1.d0-fjr)*log( welms1(je+1,jd+1,jr) ) + fjr *log( 
     &         welms1(je+1,jd+1,jr+1) )
            erl11=erl111+fjd*(erl112-erl111)
            erl12=erl121+fjd*(erl122-erl121)
            erl1 = exp( erl11 + fje*(erl12-erl11) )
         endif

c----------------------------------------------------------------------c
c write error message
      else
         call xerrab('function erl1 not defined for istabon > 15')
      endif

      return
      end

c-----------------------------------------------------------------------
      doubleprecision function erl2 (te, ne, tau)
cProlog
      implicit none
      doubleprecision te, ne, tau
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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
c istabon
c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev
c Group Data_input
      character*120 aphdir
      character*120 data_directory
      double precision sgvcxc
      integer issgvcxc, isaphdir
      common /aph10/ issgvcxc, isaphdir
      common /aph10000/ aphdir
      common /aph10001/ data_directory
      common /aph13/ sgvcxc
c End of Data_input

c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt

      double precision htza ( 0:htns-1)
      pointer(phtza,htza)

      double precision htzn ( 0:htns-1)
      pointer(phtzn,htzn)

      double precision htn ( 0:htnn)
      pointer(phtn,htn)

      double precision htt ( 0:htnt)
      pointer(phtt,htt)

      double precision htln ( 0:htnn)
      pointer(phtln,htln)

      double precision htlt ( 0:htnt)
      pointer(phtlt,htlt)

      double precision htlsa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlsa,htlsa)

      double precision htlra ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlra,htlra)

      double precision htlcx ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlcx,htlcx)

      double precision htlqa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlqa,htlqa)
      common /aph10002/ labelht
      common /aph30/ htns, htnn, htnt
      common /aph36/ phtza, phtzn, phtn, phtt
      common /aph36/ phtln, phtlt, phtlsa
      common /aph36/ phtlra, phtlcx, phtlqa
c End of Rtdata

c Group Rtdegas
      double precision rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      double precision rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      double precision deltau
      integer mpe, mpd, mpr

      double precision wsveh ( mpe,mpd,mpr)
      pointer(pwsveh,wsveh)

      double precision wsveh0 ( mpe,mpd,mpr)
      pointer(pwsveh0,wsveh0)

      double precision wlemiss ( mpe,mpd)
      pointer(pwlemiss,wlemiss)

      double precision welms ( mpe,mpd)
      pointer(pwelms,welms)

      double precision welms1 ( mpe,mpd,mpr)
      pointer(pwelms1,welms1)

      double precision welms2 ( mpe,mpd,mpr)
      pointer(pwelms2,welms2)

      double precision pne3 ( mpe,mpd)
      pointer(ppne3,pne3)

      double precision pne31 ( mpe,mpd)
      pointer(ppne31,pne31)

      double precision pne32 ( mpe,mpd)
      pointer(ppne32,pne32)

      double precision pne2 ( mpe,mpd)
      pointer(ppne2,pne2)

      double precision pne21 ( mpe,mpd)
      pointer(ppne21,pne21)

      double precision pne22 ( mpe,mpd)
      pointer(ppne22,pne22)

      double precision pne41 ( mpe,mpd)
      pointer(ppne41,pne41)

      double precision pne42 ( mpe,mpd)
      pointer(ppne42,pne42)

      double precision pne51 ( mpe,mpd)
      pointer(ppne51,pne51)

      double precision pne52 ( mpe,mpd)
      pointer(ppne52,pne52)

      double precision pne61 ( mpe,mpd)
      pointer(ppne61,pne61)

      double precision pne62 ( mpe,mpd)
      pointer(ppne62,pne62)

      double precision pne71 ( mpe,mpd)
      pointer(ppne71,pne71)

      double precision pne72 ( mpe,mpd)
      pointer(ppne72,pne72)

      double precision pne81 ( mpe,mpd)
      pointer(ppne81,pne81)

      double precision pne82 ( mpe,mpd)
      pointer(ppne82,pne82)

      double precision pne91 ( mpe,mpd)
      pointer(ppne91,pne91)

      double precision pne92 ( mpe,mpd)
      pointer(ppne92,pne92)

      double precision svdum2 ( mpe,mpe)
      pointer(psvdum2,svdum2)

      double precision svphcx ( mpe,mpe)
      pointer(psvphcx,svphcx)

      double precision ekpt ( mpe)
      pointer(pekpt,ekpt)

      double precision dkpt ( mpd)
      pointer(pdkpt,dkpt)
      common /aph40/ mpe, mpd, mpr
      common /aph43/ rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      common /aph43/ rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      common /aph43/ deltau
      common /aph46/ pwsveh, pwsveh0, pwlemiss
      common /aph46/ pwelms, pwelms1, pwelms2
      common /aph46/ ppne3, ppne31, ppne32
      common /aph46/ ppne2, ppne21, ppne22
      common /aph46/ ppne41, ppne42, ppne51
      common /aph46/ ppne52, ppne61, ppne62
      common /aph46/ ppne71, ppne72, ppne81
      common /aph46/ ppne82, ppne91, ppne92
      common /aph46/ psvdum2, psvphcx, pekpt
      common /aph46/ pdkpt
c End of Rtdegas


c     local variables --
      integer je,jd,jr
      doubleprecision zloge,zlogd,zlogr,rle,rld,fje,fjd,fjr, erl211,
     &   erl212,erl221,erl222,erl21,erl22

c     procedures --
      doubleprecision rra
      external rra

c     Compute electron radiation loss rate per H ion due to
c     "recombination" processes - D. Stotler's "coupling to the continuum"
c     te [J]          = electron temperature
c     ne [/m**3]      = electron density
c     erl2 [J/sec]    = radiation rate

c----------------------------------------------------------------------c
      if (istabon .le. 7) then
c various older models

         erl2 = (13.6d0*ev+1.5d0*te)*ne*rra(te,ne,0.d0,1)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 8 .or. istabon .eq. 9) then
c linear interpolation

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     radiation rate --
         erl211=welms2(je,jd,jr)
         erl212=welms2(je,jd+1,jr)
         erl221=welms2(je+1,jd,jr)
         erl222=welms2(je+1,jd+1,jr)
         erl21=erl211+fjd*(erl212-erl211)
         erl22=erl221+fjd*(erl222-erl221)
         erl2 = erl21 + fje*(erl22-erl21)

c----------------------------------------------------------------------c
      elseif (istabon.gt.9 .and. istabon.lt.14) then
c log. interp. of Stotler-95

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     radiation rate --  now logarithm of rate
         erl211=log( welms2(je,jd,jr) )
         erl212=log( welms2(je,jd+1,jr) )
         erl221=log( welms2(je+1,jd,jr) )
         erl222=log( welms2(je+1,jd+1,jr) )
         erl21=erl211+fjd*(erl212-erl211)
         erl22=erl221+fjd*(erl222-erl221)
         erl2 = exp( erl21 + fje*(erl22-erl21) )

c----------------------------------------------------------------------c
      elseif (istabon.gt.13 .and. istabon.lt.16) then
c spatially-dependent

         if (tau.le.taumin) then
            jr = 1
            fjr = tau/taumin
         else
            zlogr = log10(tau/taumin)/deltau + 2.d0
            zlogr = min(zlogr,dble(mpr-1))
            jr = int(zlogr)
            fjr = zlogr - jr
         endif

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     radiation rate --
         if (istabon .eq. 14) then
            erl211=(1.d0-fjr)*welms2(je,jd,jr) + fjr *welms2(je,jd,jr+1)
            erl212=(1.d0-fjr)*welms2(je,jd+1,jr) + fjr *welms2(je,jd+1,
     &         jr+1)
            erl221=(1.d0-fjr)*welms2(je+1,jd,jr) + fjr *welms2(je+1,jd,
     &         jr+1)
            erl222=(1.d0-fjr)*welms2(je+1,jd+1,jr) + fjr *welms2(je+1,jd
     &         +1,jr+1)
            erl21=erl211+fjd*(erl212-erl211)
            erl22=erl221+fjd*(erl222-erl221)
            erl2 = erl21 + fje*(erl22-erl21)
         elseif (istabon .eq. 15) then
            erl211=(1.d0-fjr)*log( welms2(je,jd,jr) ) + fjr *log( welms2
     &         (je,jd,jr+1) )
            erl212=(1.d0-fjr)*log( welms2(je,jd+1,jr) ) + fjr *log( 
     &         welms2(je,jd+1,jr+1) )
            erl221=(1.d0-fjr)*log( welms2(je+1,jd,jr) ) + fjr *log( 
     &         welms2(je+1,jd,jr+1) )
            erl222=(1.d0-fjr)*log( welms2(je+1,jd+1,jr) ) + fjr *log( 
     &         welms2(je+1,jd+1,jr+1) )
            erl21=erl211+fjd*(erl212-erl211)
            erl22=erl221+fjd*(erl222-erl221)
            erl2 = exp( erl21 + fje*(erl22-erl21) )
         endif

c-----------------------------------------------------------------------
c write error message
      else
         call xerrab('function erl2 not defined for istabon > 15')
      endif

      return
      end

c-----------------------------------------------------------------------
      doubleprecision function rcx (t0, n0, k)
cProlog
      implicit none
      integer k
      doubleprecision t0, n0
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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
c istabon
c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev,m_prot
c Group Data_input
      character*120 aphdir
      character*120 data_directory
      double precision sgvcxc
      integer issgvcxc, isaphdir
      common /aph10/ issgvcxc, isaphdir
      common /aph10000/ aphdir
      common /aph10001/ data_directory
      common /aph13/ sgvcxc
c End of Data_input
c issgvcxc,sgvcxc
c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt

      double precision htza ( 0:htns-1)
      pointer(phtza,htza)

      double precision htzn ( 0:htns-1)
      pointer(phtzn,htzn)

      double precision htn ( 0:htnn)
      pointer(phtn,htn)

      double precision htt ( 0:htnt)
      pointer(phtt,htt)

      double precision htln ( 0:htnn)
      pointer(phtln,htln)

      double precision htlt ( 0:htnt)
      pointer(phtlt,htlt)

      double precision htlsa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlsa,htlsa)

      double precision htlra ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlra,htlra)

      double precision htlcx ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlcx,htlcx)

      double precision htlqa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlqa,htlqa)
      common /aph10002/ labelht
      common /aph30/ htns, htnn, htnt
      common /aph36/ phtza, phtzn, phtn, phtt
      common /aph36/ phtln, phtlt, phtlsa
      common /aph36/ phtlra, phtlcx, phtlqa
c End of Rtdata

c Group Rtdegas
      double precision rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      double precision rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      double precision deltau
      integer mpe, mpd, mpr

      double precision wsveh ( mpe,mpd,mpr)
      pointer(pwsveh,wsveh)

      double precision wsveh0 ( mpe,mpd,mpr)
      pointer(pwsveh0,wsveh0)

      double precision wlemiss ( mpe,mpd)
      pointer(pwlemiss,wlemiss)

      double precision welms ( mpe,mpd)
      pointer(pwelms,welms)

      double precision welms1 ( mpe,mpd,mpr)
      pointer(pwelms1,welms1)

      double precision welms2 ( mpe,mpd,mpr)
      pointer(pwelms2,welms2)

      double precision pne3 ( mpe,mpd)
      pointer(ppne3,pne3)

      double precision pne31 ( mpe,mpd)
      pointer(ppne31,pne31)

      double precision pne32 ( mpe,mpd)
      pointer(ppne32,pne32)

      double precision pne2 ( mpe,mpd)
      pointer(ppne2,pne2)

      double precision pne21 ( mpe,mpd)
      pointer(ppne21,pne21)

      double precision pne22 ( mpe,mpd)
      pointer(ppne22,pne22)

      double precision pne41 ( mpe,mpd)
      pointer(ppne41,pne41)

      double precision pne42 ( mpe,mpd)
      pointer(ppne42,pne42)

      double precision pne51 ( mpe,mpd)
      pointer(ppne51,pne51)

      double precision pne52 ( mpe,mpd)
      pointer(ppne52,pne52)

      double precision pne61 ( mpe,mpd)
      pointer(ppne61,pne61)

      double precision pne62 ( mpe,mpd)
      pointer(ppne62,pne62)

      double precision pne71 ( mpe,mpd)
      pointer(ppne71,pne71)

      double precision pne72 ( mpe,mpd)
      pointer(ppne72,pne72)

      double precision pne81 ( mpe,mpd)
      pointer(ppne81,pne81)

      double precision pne82 ( mpe,mpd)
      pointer(ppne82,pne82)

      double precision pne91 ( mpe,mpd)
      pointer(ppne91,pne91)

      double precision pne92 ( mpe,mpd)
      pointer(ppne92,pne92)

      double precision svdum2 ( mpe,mpe)
      pointer(psvdum2,svdum2)

      double precision svphcx ( mpe,mpe)
      pointer(psvphcx,svphcx)

      double precision ekpt ( mpe)
      pointer(pekpt,ekpt)

      double precision dkpt ( mpd)
      pointer(pdkpt,dkpt)
      common /aph40/ mpe, mpd, mpr
      common /aph43/ rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      common /aph43/ rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      common /aph43/ deltau
      common /aph46/ pwsveh, pwsveh0, pwlemiss
      common /aph46/ pwelms, pwelms1, pwelms2
      common /aph46/ ppne3, ppne31, ppne32
      common /aph46/ ppne2, ppne21, ppne22
      common /aph46/ ppne41, ppne42, ppne51
      common /aph46/ ppne52, ppne61, ppne62
      common /aph46/ ppne71, ppne72, ppne81
      common /aph46/ ppne82, ppne91, ppne92
      common /aph46/ psvdum2, psvphcx, pekpt
      common /aph46/ pdkpt
c End of Rtdegas


c     local variables --
      doubleprecision a
      integer ini,iti
      doubleprecision rlni,rlti,fxni,fxti,a0,a1
      integer je,j0
      doubleprecision zloge,rle,fje,rcx1,rcx2
      doubleprecision kdum
      integer zn,za,zamax
      external mcrates

c     Compute rate parameter for k--->k-1 charge exchange on neutral hydrogen
c     k               = initial charge state
c     t0 [J]          = effective hydrogen temperature (per AMU)
c     n0 [/m**3]      = density (not used)
c     rcx [m**3/sec]  = <sigma v>

c----------------------------------------------------------------------c
      if ((istabon .eq. 1) .or. (istabon .eq. 2)) then
c			use ADPAK/STRAHL table look-up

c     indices for interpolation --
         iti = 0
         ini = 0
c     compute abscissae --
         rlti = log(t0/ev)
         rlni = max(htln(0),min(htln(htnn),log(n0)))
c     find iti --
   51    if (iti .lt. htnt-1) then
            if (htlt(iti+1) .le. rlti) then
               iti = iti + 1
               goto 51
            endif
         endif
   52    if (0 .lt. iti) then
            if (rlti .lt. htlt(iti)) then
               iti = iti - 1
               goto 52
            endif
         endif
c     find ini --
   53    if (ini .lt. htnn-1) then
            if (htln(ini+1) .le. rlni) then
               ini = ini + 1
               goto 53
            endif
         endif
   54    if (0 .lt. ini) then
            if (rlni .lt. htln(ini)) then
               ini = ini - 1
               goto 54
            endif
         endif
c     compute coefficients for linear interpolation --
         fxni = (rlni-htln(ini))/(htln(ini+1)-htln(ini))
         fxti = (rlti-htlt(iti))/(htlt(iti+1)-htlt(iti))
c     compute charge exchange rate parameter for k --> k-1 process --
         a0 = (1-fxni)*htlcx(iti,ini,k) + fxni*htlcx(iti,ini+1,k)
         a1 = (1-fxni)*htlcx(iti+1,ini,k) + fxni*htlcx(iti+1,ini+1,k)
         rcx = exp((1-fxti)*a0+fxti*a1)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 3) then
c			use DEGAS table look-up

c     compute abscissa --
         zloge=log(t0/ev)
         rle=max(rlemin, min(zloge,rlemax))
c     table index for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
c     fractional part of interval (je,je+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
c     charge exchange rate --
c assume neutral temperature is same as ions
         j0=je
         rcx1=svphcx(je,j0)
         rcx2=svphcx(je+1,j0)
         rcx = rcx1 + fje*(rcx2-rcx1)

c----------------------------------------------------------------------c
      elseif (istabon.eq.16) then
c For data in b2frates format (B2,SOLPS)
c nuclear charge for hydrogenic species
         zn=1
c maximum atomic charge for hydrogenic species
         zamax=1
c compute c-x rate for this charge state
         za=1
         call mcrates(n0,t0,t0,za,zamax,zn,kdum,kdum,rcx)

c----------------------------------------------------------------------c
c     use analytic model (hydrogen) for all other istabon
      else

         a = 3*t0 / (10*ev)
         rcx = 1.7d-14 * a**0.333d0
c use fixed sig-v
         if (issgvcxc.eq.1) rcx = sgvcxc
c fixed sig
         if (issgvcxc.eq.2) rcx = sgvcxc*sqrt(t0/m_prot)

c----------------------------------------------------------------------c
      endif

      return
      end
c-----------------------------------------------------------------------
      doubleprecision function rqa (te, ne, k)
cProlog
      implicit none
      integer k
      doubleprecision te, ne
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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
c istabon
c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev
c Group Data_input
      character*120 aphdir
      character*120 data_directory
      double precision sgvcxc
      integer issgvcxc, isaphdir
      common /aph10/ issgvcxc, isaphdir
      common /aph10000/ aphdir
      common /aph10001/ data_directory
      common /aph13/ sgvcxc
c End of Data_input

c Group Ionization_energy
      double precision erad
      common /aph23/ erad
c End of Ionization_energy
c erad
c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt

      double precision htza ( 0:htns-1)
      pointer(phtza,htza)

      double precision htzn ( 0:htns-1)
      pointer(phtzn,htzn)

      double precision htn ( 0:htnn)
      pointer(phtn,htn)

      double precision htt ( 0:htnt)
      pointer(phtt,htt)

      double precision htln ( 0:htnn)
      pointer(phtln,htln)

      double precision htlt ( 0:htnt)
      pointer(phtlt,htlt)

      double precision htlsa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlsa,htlsa)

      double precision htlra ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlra,htlra)

      double precision htlcx ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlcx,htlcx)

      double precision htlqa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlqa,htlqa)
      common /aph10002/ labelht
      common /aph30/ htns, htnn, htnt
      common /aph36/ phtza, phtzn, phtn, phtt
      common /aph36/ phtln, phtlt, phtlsa
      common /aph36/ phtlra, phtlcx, phtlqa
c End of Rtdata

c Group Rtdegas
      double precision rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      double precision rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      double precision deltau
      integer mpe, mpd, mpr

      double precision wsveh ( mpe,mpd,mpr)
      pointer(pwsveh,wsveh)

      double precision wsveh0 ( mpe,mpd,mpr)
      pointer(pwsveh0,wsveh0)

      double precision wlemiss ( mpe,mpd)
      pointer(pwlemiss,wlemiss)

      double precision welms ( mpe,mpd)
      pointer(pwelms,welms)

      double precision welms1 ( mpe,mpd,mpr)
      pointer(pwelms1,welms1)

      double precision welms2 ( mpe,mpd,mpr)
      pointer(pwelms2,welms2)

      double precision pne3 ( mpe,mpd)
      pointer(ppne3,pne3)

      double precision pne31 ( mpe,mpd)
      pointer(ppne31,pne31)

      double precision pne32 ( mpe,mpd)
      pointer(ppne32,pne32)

      double precision pne2 ( mpe,mpd)
      pointer(ppne2,pne2)

      double precision pne21 ( mpe,mpd)
      pointer(ppne21,pne21)

      double precision pne22 ( mpe,mpd)
      pointer(ppne22,pne22)

      double precision pne41 ( mpe,mpd)
      pointer(ppne41,pne41)

      double precision pne42 ( mpe,mpd)
      pointer(ppne42,pne42)

      double precision pne51 ( mpe,mpd)
      pointer(ppne51,pne51)

      double precision pne52 ( mpe,mpd)
      pointer(ppne52,pne52)

      double precision pne61 ( mpe,mpd)
      pointer(ppne61,pne61)

      double precision pne62 ( mpe,mpd)
      pointer(ppne62,pne62)

      double precision pne71 ( mpe,mpd)
      pointer(ppne71,pne71)

      double precision pne72 ( mpe,mpd)
      pointer(ppne72,pne72)

      double precision pne81 ( mpe,mpd)
      pointer(ppne81,pne81)

      double precision pne82 ( mpe,mpd)
      pointer(ppne82,pne82)

      double precision pne91 ( mpe,mpd)
      pointer(ppne91,pne91)

      double precision pne92 ( mpe,mpd)
      pointer(ppne92,pne92)

      double precision svdum2 ( mpe,mpe)
      pointer(psvdum2,svdum2)

      double precision svphcx ( mpe,mpe)
      pointer(psvphcx,svphcx)

      double precision ekpt ( mpe)
      pointer(pekpt,ekpt)

      double precision dkpt ( mpd)
      pointer(pdkpt,dkpt)
      common /aph40/ mpe, mpd, mpr
      common /aph43/ rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      common /aph43/ rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      common /aph43/ deltau
      common /aph46/ pwsveh, pwsveh0, pwlemiss
      common /aph46/ pwelms, pwelms1, pwelms2
      common /aph46/ ppne3, ppne31, ppne32
      common /aph46/ ppne2, ppne21, ppne22
      common /aph46/ ppne41, ppne42, ppne51
      common /aph46/ ppne52, ppne61, ppne62
      common /aph46/ ppne71, ppne72, ppne81
      common /aph46/ ppne82, ppne91, ppne92
      common /aph46/ psvdum2, psvphcx, pekpt
      common /aph46/ pdkpt
c End of Rtdegas

c Group Aphwrk
      integer nxdata, nydata, ldf, iflag, kxords, kyords

      double precision xdata ( 1:nxdata)
      pointer(pxdata,xdata)

      double precision ydata ( 1:nydata)
      pointer(pydata,ydata)

      double precision fdata ( 1:nxdata,1:nydata)
      pointer(pfdata,fdata)

      double precision xknots ( 1:nxdata+kxords)
      pointer(pxknots,xknots)

      double precision yknots ( 1:nydata+kyords)
      pointer(pyknots,yknots)

      double precision workh ( 1:nxdata*nydata+2*kxords*nxdata+1)
      pointer(pworkh,workh)

      double precision rsacoef ( 1:nxdata,1:nydata)
      pointer(prsacoef,rsacoef)

      double precision rracoef ( 1:nxdata,1:nydata)
      pointer(prracoef,rracoef)

      double precision rqacoef ( 1:nxdata,1:nydata)
      pointer(prqacoef,rqacoef)
      common /aph60/ nxdata, nydata, ldf, iflag, kxords, kyords
      common /aph66/ pxdata, pydata, pfdata
      common /aph66/ pxknots, pyknots, pworkh
      common /aph66/ prsacoef, prracoef, prqacoef
c End of Aphwrk

c Group Timespl
      double precision totb2val, totintrv
      common /com163/ totb2val, totintrv
c End of Timespl

      real sec4, gettime, tsval

c     external procedures --
      doubleprecision rsa, svradp, B2VAhL
      external rsa, svradp, B2VAhL, gettime

c     local variables --
      doubleprecision a
      integer ine,ite
      doubleprecision rlne,rlte,fxne,fxte,t0,t1
      integer je,jd,jr
      doubleprecision zloge,zlogd,rle,rld,fje,fjd,w11,w12,w21,w22,w1,w2,
     &   w,vlogw
      integer nxcoef,nycoef
      doubleprecision xuse,yuse

c     Compute electron energy loss rate parameter for processes
c     starting from charge state k --
c     k                = initial charge state
c     te [J]           = electron temperature
c     ne [/m**3]       = electron density
c     rqa [J*m**3/sec] = <sigma*v>*dE where dE is electron energy loss

c----------------------------------------------------------------------c
      if (istabon .eq. 0) then
c use analytic model (hydrogen) with
c                                  # constant energy loss per ionization
         a = te / (10*ev)
         rqa = erad * ev * 3.0d-14 * a*a / (3.0d0 + a*a)

c----------------------------------------------------------------------c
      elseif ((istabon .eq. 1) .or. (istabon .eq. 2)) then
c			use ADPAK table look-up

c     indices for interpolation --
         ite = 0
         ine = 0
c     compute abscissae --
         rlte = log(te/ev)
         rlne = max(htln(0),min(htln(htnn),log(ne)))
c     find ite --
   51    if (ite .lt. htnt-1) then
            if (htlt(ite+1) .le. rlte) then
               ite = ite + 1
               goto 51
            endif
         endif
   52    if (0 .lt. ite) then
            if (rlte .lt. htlt(ite)) then
               ite = ite - 1
               goto 52
            endif
         endif
c     find ine --
   53    if (ine .lt. htnn-1) then
            if (htln(ine+1) .le. rlne) then
               ine = ine + 1
               goto 53
            endif
         endif
   54    if (0 .lt. ine) then
            if (rlne .lt. htln(ine)) then
               ine = ine - 1
               goto 54
            endif
         endif
c     compute coefficients for linear interpolation --
         fxne = (rlne-htln(ine))/(htln(ine+1)-htln(ine))
         fxte = (rlte-htlt(ite))/(htlt(ite+1)-htlt(ite))
c     compute electron energy loss rate parameter --
         t0 = (1-fxne)*htlqa(ite,ine,k) + fxne*htlqa(ite,ine+1,k)
         t1 = (1-fxne)*htlqa(ite+1,ine,k) + fxne*htlqa(ite+1,ine+1,k)
         rqa = ev*exp((1-fxte)*t0+fxte*t1)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 3) then
c			use DEGAS table look-up

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     electron energy loss per ionization --
         w11=welms(je,jd)
         w12=welms(je,jd+1)
         w21=welms(je+1,jd)
         w22=welms(je+1,jd+1)
         w1=w11+fjd*(w12-w11)
         w2=w21+fjd*(w22-w21)
         w = w1 + fje*(w2-w1)
c     electron energy loss rate parameter --
         rqa = ev * w * rsa(te,ne,0.d0,k)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 4) then
c			use POST93 table look-up

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     hydrogen line radiation rate --
         w11=wlemiss(je,jd)
         w12=wlemiss(je,jd+1)
         w21=wlemiss(je+1,jd)
         w22=wlemiss(je+1,jd+1)
         w1=w11+fjd*(w12-w11)
         w2=w21+fjd*(w22-w21)
         w = w1 + fje*(w2-w1)
c     electron energy loss rate parameter --
         rqa = w + 13.6d0 * ev * rsa(te,ne,0.d0,k)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 5) then
c			use spline fit to POST93 table data
c      xuse=min(max(xdata(1),log(te/ev)),xdata(nxdata))
c      yuse=min(max(ydata(1),log10(ne)),ydata(nydata))

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))

         xuse=rle
         yuse=rld

         nxcoef=nxdata
         nycoef=nydata

         vlogw = B2VAhL(xuse, yuse, 0, 0, xknots, yknots, nxcoef, nycoef
     &      , kxords, kyords, rqacoef, ldf, workh, iflag)
         w=10**vlogw
c     electron energy loss rate parameter --
         rqa = w + 13.6d0 * ev * rsa(te,ne,0.d0,k)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 6) then
c			use spline fit to POST93 table data
c      xuse=min(max(xdata(1),log(te/ev)),xdata(nxdata))
c      yuse=min(max(ydata(1),log10(ne)),ydata(nydata))

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))

         xuse=rle
         yuse=rld

         nxcoef=nxdata
         nycoef=nydata

         tsval = gettime(sec4)
         w = B2VAhL(xuse, yuse, 0, 0, xknots, yknots, nxcoef, nycoef, 
     &      kxords, kyords, rqacoef, ldf, workh, iflag)
         totb2val = totb2val + gettime(sec4) - tsval
c     electron energy loss rate parameter --
         rqa = w + 13.6d0 * ev * rsa(te,ne,0.d0,k)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 7) then
c                       use polynomial fit from Bob Campbell -  8/93
c     Note that the 13.6 * ev * rsa(te,ne,k) is omitted here as Campbell
c     has already added it in
         rqa = svradp(te/ev,ne)

c----------------------------------------------------------------------c
      elseif (istabon .gt. 7) then
c write error message
         call xerrab('**** function rqa is not defined for istabon > 7')

c----------------------------------------------------------------------c
      endif

      return
      end
c-----------------------------------------------------------------------
      doubleprecision function rra (te, ne, tau, k)
cProlog
      implicit none
      integer k
      doubleprecision te, ne, tau
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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
c istabon
c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev
c Group Data_input
      character*120 aphdir
      character*120 data_directory
      double precision sgvcxc
      integer issgvcxc, isaphdir
      common /aph10/ issgvcxc, isaphdir
      common /aph10000/ aphdir
      common /aph10001/ data_directory
      common /aph13/ sgvcxc
c End of Data_input

c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt

      double precision htza ( 0:htns-1)
      pointer(phtza,htza)

      double precision htzn ( 0:htns-1)
      pointer(phtzn,htzn)

      double precision htn ( 0:htnn)
      pointer(phtn,htn)

      double precision htt ( 0:htnt)
      pointer(phtt,htt)

      double precision htln ( 0:htnn)
      pointer(phtln,htln)

      double precision htlt ( 0:htnt)
      pointer(phtlt,htlt)

      double precision htlsa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlsa,htlsa)

      double precision htlra ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlra,htlra)

      double precision htlcx ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlcx,htlcx)

      double precision htlqa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlqa,htlqa)
      common /aph10002/ labelht
      common /aph30/ htns, htnn, htnt
      common /aph36/ phtza, phtzn, phtn, phtt
      common /aph36/ phtln, phtlt, phtlsa
      common /aph36/ phtlra, phtlcx, phtlqa
c End of Rtdata

c Group Rtdegas
      double precision rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      double precision rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      double precision deltau
      integer mpe, mpd, mpr

      double precision wsveh ( mpe,mpd,mpr)
      pointer(pwsveh,wsveh)

      double precision wsveh0 ( mpe,mpd,mpr)
      pointer(pwsveh0,wsveh0)

      double precision wlemiss ( mpe,mpd)
      pointer(pwlemiss,wlemiss)

      double precision welms ( mpe,mpd)
      pointer(pwelms,welms)

      double precision welms1 ( mpe,mpd,mpr)
      pointer(pwelms1,welms1)

      double precision welms2 ( mpe,mpd,mpr)
      pointer(pwelms2,welms2)

      double precision pne3 ( mpe,mpd)
      pointer(ppne3,pne3)

      double precision pne31 ( mpe,mpd)
      pointer(ppne31,pne31)

      double precision pne32 ( mpe,mpd)
      pointer(ppne32,pne32)

      double precision pne2 ( mpe,mpd)
      pointer(ppne2,pne2)

      double precision pne21 ( mpe,mpd)
      pointer(ppne21,pne21)

      double precision pne22 ( mpe,mpd)
      pointer(ppne22,pne22)

      double precision pne41 ( mpe,mpd)
      pointer(ppne41,pne41)

      double precision pne42 ( mpe,mpd)
      pointer(ppne42,pne42)

      double precision pne51 ( mpe,mpd)
      pointer(ppne51,pne51)

      double precision pne52 ( mpe,mpd)
      pointer(ppne52,pne52)

      double precision pne61 ( mpe,mpd)
      pointer(ppne61,pne61)

      double precision pne62 ( mpe,mpd)
      pointer(ppne62,pne62)

      double precision pne71 ( mpe,mpd)
      pointer(ppne71,pne71)

      double precision pne72 ( mpe,mpd)
      pointer(ppne72,pne72)

      double precision pne81 ( mpe,mpd)
      pointer(ppne81,pne81)

      double precision pne82 ( mpe,mpd)
      pointer(ppne82,pne82)

      double precision pne91 ( mpe,mpd)
      pointer(ppne91,pne91)

      double precision pne92 ( mpe,mpd)
      pointer(ppne92,pne92)

      double precision svdum2 ( mpe,mpe)
      pointer(psvdum2,svdum2)

      double precision svphcx ( mpe,mpe)
      pointer(psvphcx,svphcx)

      double precision ekpt ( mpe)
      pointer(pekpt,ekpt)

      double precision dkpt ( mpd)
      pointer(pdkpt,dkpt)
      common /aph40/ mpe, mpd, mpr
      common /aph43/ rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      common /aph43/ rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      common /aph43/ deltau
      common /aph46/ pwsveh, pwsveh0, pwlemiss
      common /aph46/ pwelms, pwelms1, pwelms2
      common /aph46/ ppne3, ppne31, ppne32
      common /aph46/ ppne2, ppne21, ppne22
      common /aph46/ ppne41, ppne42, ppne51
      common /aph46/ ppne52, ppne61, ppne62
      common /aph46/ ppne71, ppne72, ppne81
      common /aph46/ ppne82, ppne91, ppne92
      common /aph46/ psvdum2, psvphcx, pekpt
      common /aph46/ pdkpt
c End of Rtdegas

c Group Aphwrk
      integer nxdata, nydata, ldf, iflag, kxords, kyords

      double precision xdata ( 1:nxdata)
      pointer(pxdata,xdata)

      double precision ydata ( 1:nydata)
      pointer(pydata,ydata)

      double precision fdata ( 1:nxdata,1:nydata)
      pointer(pfdata,fdata)

      double precision xknots ( 1:nxdata+kxords)
      pointer(pxknots,xknots)

      double precision yknots ( 1:nydata+kyords)
      pointer(pyknots,yknots)

      double precision workh ( 1:nxdata*nydata+2*kxords*nxdata+1)
      pointer(pworkh,workh)

      double precision rsacoef ( 1:nxdata,1:nydata)
      pointer(prsacoef,rsacoef)

      double precision rracoef ( 1:nxdata,1:nydata)
      pointer(prracoef,rracoef)

      double precision rqacoef ( 1:nxdata,1:nydata)
      pointer(prqacoef,rqacoef)
      common /aph60/ nxdata, nydata, ldf, iflag, kxords, kyords
      common /aph66/ pxdata, pydata, pfdata
      common /aph66/ pxknots, pyknots, pworkh
      common /aph66/ prsacoef, prracoef, prqacoef
c End of Aphwrk

c Group Timespl
      double precision totb2val, totintrv
      common /com163/ totb2val, totintrv
c End of Timespl

      real sec4, gettime, tsval

c     external procedures --
      doubleprecision srecf, B2VAhL
      external srecf, B2VAhL, gettime

c     local variables --
      integer ine,ite
      doubleprecision rlne,rlte,fxne,fxte,t0,t1
      integer je,jd,jr
      doubleprecision zloge,zlogd,zlogr,rle,rld,fje,fjd,fjr, rra11,rra12
     &   ,rra21,rra22,rra1,rra2
      integer nxcoef,nycoef
      doubleprecision xuse,yuse,vlog10rra
      doubleprecision kdum
      integer zn,za,zamax

c     Compute rate parameter for k--->k-1 recombination
c     k               = initial charge state
c     te [J]          = electron temperature
c     ne [/m**3]      = electron density
c     rra [m**3/sec]  = <sigma v>

c----------------------------------------------------------------------c
      if (istabon .eq. 0) then
c use analytic model
         rra = 0.d0

c----------------------------------------------------------------------c
      elseif ((istabon .eq. 1) .or. (istabon .eq. 2)) then
c			use ADPAK table look-up

c     indices for interpolation --
         ite = 0
         ine = 0
c     compute abscissae --
         rlte = log(te/ev)
         rlne = max(htln(0),min(htln(htnn),log(ne)))
c     find ite --
   51    if (ite .lt. htnt-1) then
            if (htlt(ite+1) .le. rlte) then
               ite = ite + 1
               goto 51
            endif
         endif
   52    if (0 .lt. ite) then
            if (rlte .lt. htlt(ite)) then
               ite = ite - 1
               goto 52
            endif
         endif
c     find ine --
   53    if (ine .lt. htnn-1) then
            if (htln(ine+1) .le. rlne) then
               ine = ine + 1
               goto 53
            endif
         endif
   54    if (0 .lt. ine) then
            if (rlne .lt. htln(ine)) then
               ine = ine - 1
               goto 54
            endif
         endif
c     compute coefficients for linear interpolation --
         fxne = (rlne-htln(ine))/(htln(ine+1)-htln(ine))
         fxte = (rlte-htlt(ite))/(htlt(ite+1)-htlt(ite))
c     compute recombination rate parameter for k --> k-1 process  --
         t0 = (1-fxne)*htlra(ite,ine,k) + fxne*htlra(ite,ine+1,k)
         t1 = (1-fxne)*htlra(ite+1,ine,k) + fxne*htlra(ite+1,ine+1,k)
         rra = exp((1-fxte)*t0+fxte*t1)

c----------------------------------------------------------------------c
      elseif ((istabon .eq. 3) .or. (istabon .eq. 4) .or. (istabon .eq. 
     &   8) .or. (istabon .eq. 9)) then
c             use DEGAS or POST93 or DEGAS93 or Stotler95 table look-up

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     recombination rate parameter --
         rra11=wsveh0(je,jd,jr)
         rra12=wsveh0(je,jd+1,jr)
         rra21=wsveh0(je+1,jd,jr)
         rra22=wsveh0(je+1,jd+1,jr)
         rra1=rra11+fjd*(rra12-rra11)
         rra2=rra21+fjd*(rra22-rra21)
         rra = rra1 + fje*(rra2-rra1)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 5) then
c			use spline fit to POST93 table data
c      xuse=min(max(xdata(1),log(te/ev)),xdata(nxdata))
c      yuse=min(max(ydata(1),log10(ne)),ydata(nydata))

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))

         xuse=rle
         yuse=rld

         nxcoef=nxdata
         nycoef=nydata

         vlog10rra = B2VAhL(xuse, yuse, 0, 0, xknots, yknots, nxcoef, 
     &      nycoef, kxords, kyords, rracoef, ldf, workh, iflag)
         rra=10**vlog10rra

c----------------------------------------------------------------------c
      elseif (istabon .eq. 6) then
c			use spline fit to POST93 table data
c      xuse=min(max(xdata(1),log(te/ev)),xdata(nxdata))
c      yuse=min(max(ydata(1),log10(ne)),ydata(nydata))

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))

         xuse=rle
         yuse=rld

         nxcoef=nxdata
         nycoef=nydata

         tsval = gettime(sec4)
         rra = B2VAhL(xuse, yuse, 0, 0, xknots, yknots, nxcoef, nycoef, 
     &      kxords, kyords, rracoef, ldf, workh, iflag)
         totb2val = totb2val + gettime(sec4) - tsval
c----------------------------------------------------------------------c
      elseif (istabon .eq. 7) then
c                       use polynomial fit from Bob Campbell -  8/93
         rra = srecf(te/ev,ne)

c----------------------------------------------------------------------c
      elseif (istabon.gt.9 .and. istabon.lt.14) then
c use log interp on Stotler
         jr = 1
c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     recombination rate parameter --
         rra11=log( wsveh0(je,jd,jr) )
         rra12=log( wsveh0(je,jd+1,jr) )
         rra21=log( wsveh0(je+1,jd,jr) )
         rra22=log( wsveh0(je+1,jd+1,jr) )
         rra1=rra11+fjd*(rra12-rra11)
         rra2=rra21+fjd*(rra22-rra21)
         rra = exp( rra1 + fje*(rra2-rra1) )

c----------------------------------------------------------------------c
      elseif (istabon.gt.13 .and. istabon.lt.16) then
c spatially-dep opt-depth

         if (tau.le.taumin) then
            jr = 1
            fjr = tau/taumin
         else
            zlogr = log10(tau/taumin)/deltau + 2.d0
            zlogr = min(zlogr,dble(mpr-1))
            jr = int(zlogr)
            fjr = zlogr - jr
         endif

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     recombination rate parameter --
         if (istabon .eq. 14) then
            rra11=(1.d0-fjr)*wsveh0(je,jd,jr) + fjr *wsveh0(je,jd,jr+1)
            rra12=(1.d0-fjr)*wsveh0(je,jd+1,jr) + fjr *wsveh0(je,jd+1,jr
     &         +1)
            rra21=(1.d0-fjr)*wsveh0(je+1,jd,jr) + fjr *wsveh0(je+1,jd,jr
     &         +1)
            rra22=(1.d0-fjr)*wsveh0(je+1,jd+1,jr) + fjr *wsveh0(je+1,jd+
     &         1,jr+1)
            rra1=rra11+fjd*(rra12-rra11)
            rra2=rra21+fjd*(rra22-rra21)
            rra =rra1 + fje*(rra2-rra1)
         elseif (istabon .eq. 15) then
            rra11=(1.d0-fjr)*log( wsveh0(je,jd,jr) ) + fjr *log( wsveh0(
     &         je,jd,jr+1) )
            rra12=(1.d0-fjr)*log( wsveh0(je,jd+1,jr) ) + fjr *log( 
     &         wsveh0(je,jd+1,jr+1) )
            rra21=(1.d0-fjr)*log( wsveh0(je+1,jd,jr) ) + fjr *log( 
     &         wsveh0(je+1,jd,jr+1) )
            rra22=(1.d0-fjr)*log( wsveh0(je+1,jd+1,jr) ) + fjr *log( 
     &         wsveh0(je+1,jd+1,jr+1) )
            rra1=rra11+fjd*(rra12-rra11)
            rra2=rra21+fjd*(rra22-rra21)
            rra = exp( rra1 + fje*(rra2-rra1) )
         endif

c----------------------------------------------------------------------c
      elseif (istabon.eq.16) then
c nuclear charge for hydrogenic species
         zn=1
c maximum atomic charge for hydrogenic species
         zamax=1
c compute recombination rate for this charge state
         za=1
         call mcrates(ne,te,te,za,zamax,zn,kdum,rra,kdum)

c----------------------------------------------------------------------c
      endif

      return
      end
c-----------------------------------------------------------------------
      doubleprecision function rsa (te, ne, tau, k)
cProlog
      implicit none
      integer k
      doubleprecision te, ne, tau
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

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
c istabon
c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev
c Group Data_input
      character*120 aphdir
      character*120 data_directory
      double precision sgvcxc
      integer issgvcxc, isaphdir
      common /aph10/ issgvcxc, isaphdir
      common /aph10000/ aphdir
      common /aph10001/ data_directory
      common /aph13/ sgvcxc
c End of Data_input

c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt

      double precision htza ( 0:htns-1)
      pointer(phtza,htza)

      double precision htzn ( 0:htns-1)
      pointer(phtzn,htzn)

      double precision htn ( 0:htnn)
      pointer(phtn,htn)

      double precision htt ( 0:htnt)
      pointer(phtt,htt)

      double precision htln ( 0:htnn)
      pointer(phtln,htln)

      double precision htlt ( 0:htnt)
      pointer(phtlt,htlt)

      double precision htlsa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlsa,htlsa)

      double precision htlra ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlra,htlra)

      double precision htlcx ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlcx,htlcx)

      double precision htlqa ( 0:htnt,0:htnn,0:htns-1)
      pointer(phtlqa,htlqa)
      common /aph10002/ labelht
      common /aph30/ htns, htnn, htnt
      common /aph36/ phtza, phtzn, phtn, phtt
      common /aph36/ phtln, phtlt, phtlsa
      common /aph36/ phtlra, phtlcx, phtlqa
c End of Rtdata

c Group Rtdegas
      double precision rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      double precision rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      double precision deltau
      integer mpe, mpd, mpr

      double precision wsveh ( mpe,mpd,mpr)
      pointer(pwsveh,wsveh)

      double precision wsveh0 ( mpe,mpd,mpr)
      pointer(pwsveh0,wsveh0)

      double precision wlemiss ( mpe,mpd)
      pointer(pwlemiss,wlemiss)

      double precision welms ( mpe,mpd)
      pointer(pwelms,welms)

      double precision welms1 ( mpe,mpd,mpr)
      pointer(pwelms1,welms1)

      double precision welms2 ( mpe,mpd,mpr)
      pointer(pwelms2,welms2)

      double precision pne3 ( mpe,mpd)
      pointer(ppne3,pne3)

      double precision pne31 ( mpe,mpd)
      pointer(ppne31,pne31)

      double precision pne32 ( mpe,mpd)
      pointer(ppne32,pne32)

      double precision pne2 ( mpe,mpd)
      pointer(ppne2,pne2)

      double precision pne21 ( mpe,mpd)
      pointer(ppne21,pne21)

      double precision pne22 ( mpe,mpd)
      pointer(ppne22,pne22)

      double precision pne41 ( mpe,mpd)
      pointer(ppne41,pne41)

      double precision pne42 ( mpe,mpd)
      pointer(ppne42,pne42)

      double precision pne51 ( mpe,mpd)
      pointer(ppne51,pne51)

      double precision pne52 ( mpe,mpd)
      pointer(ppne52,pne52)

      double precision pne61 ( mpe,mpd)
      pointer(ppne61,pne61)

      double precision pne62 ( mpe,mpd)
      pointer(ppne62,pne62)

      double precision pne71 ( mpe,mpd)
      pointer(ppne71,pne71)

      double precision pne72 ( mpe,mpd)
      pointer(ppne72,pne72)

      double precision pne81 ( mpe,mpd)
      pointer(ppne81,pne81)

      double precision pne82 ( mpe,mpd)
      pointer(ppne82,pne82)

      double precision pne91 ( mpe,mpd)
      pointer(ppne91,pne91)

      double precision pne92 ( mpe,mpd)
      pointer(ppne92,pne92)

      double precision svdum2 ( mpe,mpe)
      pointer(psvdum2,svdum2)

      double precision svphcx ( mpe,mpe)
      pointer(psvphcx,svphcx)

      double precision ekpt ( mpe)
      pointer(pekpt,ekpt)

      double precision dkpt ( mpd)
      pointer(pdkpt,dkpt)
      common /aph40/ mpe, mpd, mpr
      common /aph43/ rlemin, rlemax, erefmin, erefmax, delekpt, rldmin
      common /aph43/ rldmax, drefmin, drefmax, deldkpt, taumin, taumax
      common /aph43/ deltau
      common /aph46/ pwsveh, pwsveh0, pwlemiss
      common /aph46/ pwelms, pwelms1, pwelms2
      common /aph46/ ppne3, ppne31, ppne32
      common /aph46/ ppne2, ppne21, ppne22
      common /aph46/ ppne41, ppne42, ppne51
      common /aph46/ ppne52, ppne61, ppne62
      common /aph46/ ppne71, ppne72, ppne81
      common /aph46/ ppne82, ppne91, ppne92
      common /aph46/ psvdum2, psvphcx, pekpt
      common /aph46/ pdkpt
c End of Rtdegas

c Group Aphwrk
      integer nxdata, nydata, ldf, iflag, kxords, kyords

      double precision xdata ( 1:nxdata)
      pointer(pxdata,xdata)

      double precision ydata ( 1:nydata)
      pointer(pydata,ydata)

      double precision fdata ( 1:nxdata,1:nydata)
      pointer(pfdata,fdata)

      double precision xknots ( 1:nxdata+kxords)
      pointer(pxknots,xknots)

      double precision yknots ( 1:nydata+kyords)
      pointer(pyknots,yknots)

      double precision workh ( 1:nxdata*nydata+2*kxords*nxdata+1)
      pointer(pworkh,workh)

      double precision rsacoef ( 1:nxdata,1:nydata)
      pointer(prsacoef,rsacoef)

      double precision rracoef ( 1:nxdata,1:nydata)
      pointer(prracoef,rracoef)

      double precision rqacoef ( 1:nxdata,1:nydata)
      pointer(prqacoef,rqacoef)
      common /aph60/ nxdata, nydata, ldf, iflag, kxords, kyords
      common /aph66/ pxdata, pydata, pfdata
      common /aph66/ pxknots, pyknots, pworkh
      common /aph66/ prsacoef, prracoef, prqacoef
c End of Aphwrk

c Group Timespl
      double precision totb2val, totintrv
      common /com163/ totb2val, totintrv
c End of Timespl

      real sec4, gettime, tsval

c     external procedures --
      doubleprecision sionf, B2VAhL
      external sionf, B2VAhL, gettime

c     local variables --
      doubleprecision a
      integer ine,ite
      doubleprecision rlne,rlte,fxne,fxte,t0,t1
      integer je,jd,jr
      doubleprecision zloge,zlogd,zlogr,rle,rld,fje,fjd,fjr, rsa11,rsa12
     &   ,rsa21,rsa22,rsa1,rsa2
      integer nxcoef,nycoef
      doubleprecision xuse,yuse,vlog10rsa
      doubleprecision kdum
      integer zn,za,zamax
      external mcrates

c     Compute rate parameter for k--->k+1 ionization by electrons
c     k               = initial charge state
c     te [J]          = electron temperature
c     ne [/m**3]      = electron density
c     rsa [m**3/sec]  = <sigma v>

c----------------------------------------------------------------------c
      if (istabon .eq. 0) then
c use analytic model (hydrogen)
         a = te / (10*ev)
         rsa = 3.0d-14 * a*a / (3.0d0 + a*a)

c----------------------------------------------------------------------c
      elseif ((istabon .eq. 1) .or. (istabon .eq. 2)) then
c			use ADPAK table look-up

c     indices for interpolation --
         ite = 0
         ine = 0
c     compute abscissae --
         rlte = log(te/ev)
         rlne = max(htln(0),min(htln(htnn),log(ne)))
c     find ite --
   51    if (ite .lt. htnt-1) then
            if (htlt(ite+1) .le. rlte) then
               ite = ite + 1
               goto 51
            endif
         endif
   52    if (0 .lt. ite) then
            if (rlte .lt. htlt(ite)) then
               ite = ite - 1
               goto 52
            endif
         endif
c     find ine --
   53    if (ine .lt. htnn-1) then
            if (htln(ine+1) .le. rlne) then
               ine = ine + 1
               goto 53
            endif
         endif
   54    if (0 .lt. ine) then
            if (rlne .lt. htln(ine)) then
               ine = ine - 1
               goto 54
            endif
         endif
c     compute coefficients for linear interpolation --
         fxne = (rlne-htln(ine))/(htln(ine+1)-htln(ine))
         fxte = (rlte-htlt(ite))/(htlt(ite+1)-htlt(ite))
c     compute ionization rate parameter for k --> k+1 process --
         t0 = (1-fxne)*htlsa(ite,ine,k) + fxne*htlsa(ite,ine+1,k)
         t1 = (1-fxne)*htlsa(ite+1,ine,k) + fxne*htlsa(ite+1,ine+1,k)
         rsa = exp((1-fxte)*t0+fxte*t1)

c----------------------------------------------------------------------c
      elseif ((istabon .eq. 3) .or. (istabon .eq. 4) .or. (istabon .eq. 
     &   8) .or. (istabon .eq. 9)) then
c       	use DEGAS or POST93 or DEGAS93 or Stotler95 table look-up

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     ionization rate parameter --
         rsa11=wsveh(je,jd,jr)
         rsa12=wsveh(je,jd+1,jr)
         rsa21=wsveh(je+1,jd,jr)
         rsa22=wsveh(je+1,jd+1,jr)
         rsa1=rsa11+fjd*(rsa12-rsa11)
         rsa2=rsa21+fjd*(rsa22-rsa21)
         rsa = rsa1 + fje*(rsa2-rsa1)

c----------------------------------------------------------------------c
      elseif (istabon .eq. 5) then
c			use spline fit to POST93 table data
c      xuse=min(max(xdata(1),log(te/ev)),xdata(nxdata))
c      yuse=min(max(ydata(1),log10(ne)),ydata(nydata))

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))

         xuse=rle
         yuse=rld

         nxcoef=nxdata
         nycoef=nydata

         vlog10rsa = B2VAhL(xuse, yuse, 0, 0, xknots, yknots, nxcoef, 
     &      nycoef, kxords, kyords, rsacoef, ldf, workh, iflag)
         rsa=10**vlog10rsa

c----------------------------------------------------------------------c
      elseif (istabon .eq. 6) then
c			use spline fit to POST93 table data
c      xuse=min(max(xdata(1),log(te/ev)),xdata(nxdata))
c      yuse=min(max(ydata(1),log10(ne)),ydata(nydata))

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))

         xuse=rle
         yuse=rld

         nxcoef=nxdata
         nycoef=nydata

         tsval = gettime(sec4)
         rsa = B2VAhL(xuse, yuse, 0, 0, xknots, yknots, nxcoef, nycoef, 
     &      kxords, kyords, rsacoef, ldf, workh, iflag)
         totb2val = totb2val + gettime(sec4) - tsval
c----------------------------------------------------------------------c
      elseif (istabon .eq. 7) then
c                       use polynomial fit from Bob Campbell -  8/93
         rsa = sionf(te/ev,ne)

c----------------------------------------------------------------------c
      elseif (istabon.gt.9 .and. istabon.lt.14) then
c log interp on Stotler

         jr = 1

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     ionization rate parameter -- now logarithm of rates
         rsa11=log( wsveh(je,jd,jr) )
         rsa12=log( wsveh(je,jd+1,jr) )
         rsa21=log( wsveh(je+1,jd,jr) )
         rsa22=log( wsveh(je+1,jd+1,jr) )
         rsa1=rsa11 + fjd*(rsa12-rsa11)
         rsa2=rsa21 + fjd*(rsa22-rsa21)
         rsa = exp( rsa1 + fje*(rsa2-rsa1) )

c----------------------------------------------------------------------c
      elseif (istabon.gt.13 .and. istabon.lt.16) then
c spatially-dep opt-depth

         if (tau.le.taumin) then
            jr = 1
            fjr = tau/taumin
         else
            zlogr = log10(tau/taumin)/deltau + 2.d0
            zlogr = min(zlogr,dble(mpr-1))
            jr = int(zlogr)
            fjr = zlogr - jr
         endif

c     compute abscissae --
         zloge=log(te/ev)
         rle=max(rlemin, min(zloge,rlemax))
         zlogd=log10(ne)
         rld=max(rldmin, min(zlogd,rldmax))
c     table indicies for interpolation --
         je=int((rle-rlemin)/delekpt) + 1
         je=min(je,mpe-1)
         jd=int((rld-rldmin)/deldkpt) + 1
         jd=min(jd,mpd-1)
c     fractional parts of intervals (je,je+1) and (jd,jd+1) --
         fje=(rle-ekpt(je))/(ekpt(je+1)-ekpt(je))
         fjd=(rld-dkpt(jd))/(dkpt(jd+1)-dkpt(jd))
c     ionization rate parameter
         if (istabon .eq. 14) then
            rsa11=(1.d0-fjr)*wsveh(je,jd,jr) + fjr *wsveh(je,jd,jr+1)
            rsa12=(1.d0-fjr)*wsveh(je,jd+1,jr) + fjr *wsveh(je,jd+1,jr+1
     &         )
            rsa21=(1.d0-fjr)*wsveh(je+1,jd,jr) + fjr *wsveh(je+1,jd,jr+1
     &         )
            rsa22=(1.d0-fjr)*wsveh(je+1,jd+1,jr) + fjr *wsveh(je+1,jd+1,
     &         jr+1)
            rsa1=rsa11+fjd*(rsa12-rsa11)
            rsa2=rsa21+fjd*(rsa22-rsa21)
            rsa =rsa1 + fje*(rsa2-rsa1)
         elseif (istabon .eq. 15) then
            rsa11=(1.d0-fjr)*log( wsveh(je,jd,jr) ) + fjr *log( wsveh(je
     &         ,jd,jr+1) )
            rsa12=(1.d0-fjr)*log( wsveh(je,jd+1,jr) ) + fjr *log( wsveh(
     &         je,jd+1,jr+1) )
            rsa21=(1.d0-fjr)*log( wsveh(je+1,jd,jr) ) + fjr *log( wsveh(
     &         je+1,jd,jr+1) )
            rsa22=(1.d0-fjr)*log( wsveh(je+1,jd+1,jr) ) + fjr *log( 
     &         wsveh(je+1,jd+1,jr+1) )
            rsa1=rsa11+fjd*(rsa12-rsa11)
            rsa2=rsa21+fjd*(rsa22-rsa21)
            rsa = exp( rsa1 + fje*(rsa2-rsa1) )
         endif

c----------------------------------------------------------------------c
      elseif (istabon.eq.16) then
c nuclear charge for hydrogenic species
         zn=1
c maximum atomic charge for hydrogenic species
         zamax=1
c compute ionization rate for this charge state
         za=0
         call mcrates(ne,te,te,za,zamax,zn,rsa,kdum,kdum)

c----------------------------------------------------------------------c
      endif

      return
      end

c----------------------------------------------------------------------c
      doubleprecision function sionf(temp,den)
cProlog
c
c  this function is the new H ionization curve fit from
c  R.B. Campbell 1/94
c
c    0.1 eV < te < 500 eV
c
c    1.0e18 1/m3 < ne < 1.022 1/m3
c
c    y = log10(te(eV))
c    x = log10(ne(1/m3))
c caution: other version may reverse x,y and then correct later
c
c Both ionization and recombination rates are in m3/sec.
c Etai is in eV.
c
      implicit none

      doubleprecision temp,den,x,y,ain,bin,cin,din,ein,gin,hin,riin

c Fit for Ionization Rate

      ain(x) = -49.05905d0 + 2.51313783d0 * x - 0.049159714d0*x*x
      bin(x) = 41.1855162d0 - 2.3298672d0 * x + 4.24769144d-2*x*x
      cin(x) = -32.798921d0+1.72102919d0*x-0.038692357d0*x*x
      din(x) = 27.370466d0-1.6824361d0*x+0.0462317894d0*x*x
      ein(x) = -7.9990454d0+0.127573157d0*x-6.3586911d-3*x*x
      gin(x) = -4.5832951d0+0.776264783d0*x-1.8866089d-2*x*x
      hin(x) = 3.08056833d0-0.39114789d0*x+9.86833304d-3*x*x
      riin(x) = -0.4648639d0+0.0551428018d0*x-1.404213d-3*x*x
c
c *************************************************************
c
      x = min(22.d0,log10(den))
      y = log10(temp)
c
c
      sionf = 10**( ain(x)+bin(x)*y+cin(x)*y*y+din(x)*y*y*y + ein(x)*y*y
     &   *y*y + gin(x)*y*y*y*y*y + hin(x)*y*y*y*y*y*y + riin(x)*y*y*y*y*
     &   y*y*y )

c
      return
      end
c
c----------------------------------------------------------------------c

      doubleprecision function srecf(temp,den)
cProlog
c
c  this function is the H recombination curve fit from
c  R.B. Campbell 8/93
c
c    0.1 eV < te < 500 eV
c
c    1.0e18 1/m3 < ne < 1.022 1/m3
c
c    y = log10(te(eV))
c    x = log10(ne(1/m3))
c caution: other version may reverse x,y and then correct later
c
c Both ionization and recombination rates are in m3/sec.
c Etai is in eV.
c
c
      implicit none

      doubleprecision temp,den,x,y,ar,br,cr,dr,er,gr
c
c Fit for Recombination Rate
c
      ar(x) = -0.4575652d0 - 2.144012d0 * x + 6.7072142d-2 * x * x 
     &   -1.391667d-4 * x * x * x
      br(x) = -121.8401d0 + 18.001822d0 * x -0.8679488d0 * x * x + 
     &   1.33165d-2 * x * x * x
      cr(x) = 80.897256d0 -13.29602d0 * x + 0.71881414d0 * x * x 
     &   -0.0126549d0 * x * x * x
      dr(x) = 56.406823d0 - 7.301996d0 * x + 0.29339793d0 * x * x 
     &   -3.50898d-3 * x * x * x
      er(x) = -55.73559d0 + 7.9634283d0 * x - 0.370274d0 * x * x + 
     &   5.567961d-3 * x * x * x
      gr(x) = 10.866692d0 - 1.584193d0 * x + 0.07563791d0 * x * x 
     &   -1.177562d-3 * x * x * x
c
c *************************************************************
c
      x = min(22.d0,log10(den))
      y = log10(temp)
c
c
      srecf = 10**( ar(x)+br(x)*y+cr(x)*y*y+dr(x)*y*y*y + er(x)*y*y*y*y 
     &   + gr(x)*y*y*y*y*y )
c
      return
      end

c----------------------------------------------------------------------c

      doubleprecision function svradp(temp,den)
cProlog
c
c  this function is the H radiation curve fit from
c  R.B. Campbell 8/93
c
c    0.1 eV < te < 500 eV
c
c    1.0e18 1/m3 < ne < 1.022 1/m3
c
c    y = log10(te(eV))
c    x = log10(ne(1/m3))
c caution: other version may reverse x,y and then correct later
c
c Both ionization and recombination rates are in m3/sec.
c Etai is in eV.
c

      implicit none

      doubleprecision temp,den,x,y,ai,bi,ci,di,ei,gi,ae,be,ce,de,ee,ge,
     &   sionfl,etai

c Fit for Ionization Rate

      ai(x) = -275.845d0 + 37.010817d0 * x -1.788045d0 * x * x + 
     &   0.029078333d0 * x * x * x
      bi(x) = 2200.9478d0 - 326.1153d0 * x + 16.148655d0 * x * x - 
     &   0.2660702d0 * x * x * x
      ci(x) = -2.935221d3 + 4.3757698d2 * x -21.73964d0 * x * x + 
     &   0.358962d0 * x * x * x
      di(x) = 1604.1466d0 - 239.6959d0 * x + 11.923707d0 * x * x - 
     &   0.1970501d0 * x * x * x
      ei(x) = -390.8635d0 + 58.474495d0 * x -2.910997d0 * x * x + 
     &   0.048133829d0 * x * x * x
      gi(x) = 35.012574d0 - 5.24202d0 * x + 0.26109962d0 * x * x 
     &   -4.319238d-3 * x * x * x
c
c Fit for (Erad-13.6)*svion Net hydrogenic  energy loss / ionization

      ae(x) = 2860.4173d0 - 610.2452d0 * x + 48.275821d0 * x * x 
     &   -1.687994d0 * x * x * x + 0.02201375d0 * x * x * x * x
      be(x) = 10612.067d0 - 2046.397d0 * x + 147.73914d0 * x * x - 
     &   4.729973d0 * x * x * x + 0.056671796d0 * x * x * x * x
      ce(x) = -4.231708d4 + 8494.6102d0 * x - 639.0226d0 * x * x + 
     &   21.350311d0 * x * x * x -0.2673466d0 * x * x * x * x
      de(x) = -8.385144d3 + 1887.6244d0 * x -157.8502d0 * x * x + 
     &   5.820501d0 * x * x * x - 0.07992837d0 * x * x * x * x
      ee(x) = 3.938282d4 -8.131339d3 * x + 628.8119d0 * x * x 
     &   -21.58636d0 * x * x * x + 0.27756029d0 * x * x * x * x
      ge(x) = -1.038281d4 + 2.1349333d3 * x -164.4201d0 * x * x + 
     &   5.6210487d0 * x * x * x - 0.07197622d0 * x * x * x * x
c
      sionfl(x,y) = 10**( ai(x)+bi(x)*y+ci(x)*y*y+di(x)*y*y*y + ei(x)*y*
     &   y*y*y + gi(x)*y*y*y*y*y )
c
      etai(x,y) =( 10**( ae(x)+be(x)*y+ce(x)*y*y+de(x)*y*y*y + ee(x)*y*y
     &   *y*y + ge(x)*y*y*y*y*y ) ) / sionfl(x,y)
c
c *************************************************************
c
      x = min(22.d0,log10(den))
      y = log10(temp)
c
c
c Above 100eV, etai is constant at the 100eV value
c
      svradp = max( 0.d0,(13.6d0+etai(x,min(2.d0,y))) ) * 1.602d-19 * 
     &   sionfl(x,y)
c
      return
      end

c----------------------------------------------------------------------c

      doubleprecision function svdiss (te)
cProlog
      implicit none
      doubleprecision te

c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants
c ev

c     Compute rate parameter for molecular dissociation by electrons
c        input:  te [J]   =  electron temperature (J)
c        output: svdiss   = <sigma v> (m**3/s)

c     Polynomial fit from HYDHEL data file of EIRENE Monte Carlo code,
c     reaction number 2.2.5, attributed to preprint by Janev.

c     local variables --
      doubleprecision logt, logsv
      doubleprecision b0,b1,b2,b3,b4,b5,b6,b7,b8

      b0 = -2.787217511174d+01
      b1 = 1.052252660075d+01
      b2 = -4.973212347860d+00
      b3 = 1.451198183114d+00
      b4 = -3.062790554644d-01
      b5 = 4.433379509258d-02
      b6 = -4.096344172875d-03
      b7 = 2.159670289222d-04
      b8 = -4.928545325189d-06

      logt = log (te/ev)
      logsv = b0+logt*(b1+logt*(b2+logt*(b3+logt*(b4 +logt*(b5+logt*(b6+
     &   logt*(b7+logt*b8)))))))
      svdiss = (1d-6)*exp(logsv)
      return
      end

c----------------------------------------------------------------------c
