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
c     ./aph.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c







































































      subroutine aphinit0
cProlog
c initializes a Package
      integer drtdm
      common /aphrtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("aph")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call aphdata
      call aphwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data aphiyiyi
c Replace pointer statements with Address types


c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants

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

c Group Rtdata
      character*120 labelht
      integer htns, htnn, htnt
      integer*8 phtza
      integer*8 phtzn
      integer*8 phtn
      integer*8 phtt
      integer*8 phtln
      integer*8 phtlt
      integer*8 phtlsa
      integer*8 phtlra
      integer*8 phtlcx
      integer*8 phtlqa
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
      integer*8 pwsveh
      integer*8 pwsveh0
      integer*8 pwlemiss
      integer*8 pwelms
      integer*8 pwelms1
      integer*8 pwelms2
      integer*8 ppne3
      integer*8 ppne31
      integer*8 ppne32
      integer*8 ppne2
      integer*8 ppne21
      integer*8 ppne22
      integer*8 ppne41
      integer*8 ppne42
      integer*8 ppne51
      integer*8 ppne52
      integer*8 ppne61
      integer*8 ppne62
      integer*8 ppne71
      integer*8 ppne72
      integer*8 ppne81
      integer*8 ppne82
      integer*8 ppne91
      integer*8 ppne92
      integer*8 psvdum2
      integer*8 psvphcx
      integer*8 pekpt
      integer*8 pdkpt
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

c Group Rtfcn
c End of Rtfcn

c Group Aphwrk
      integer nxdata, nydata, ldf, iflag, kxords, kyords
      integer*8 pxdata
      integer*8 pydata
      integer*8 pfdata
      integer*8 pxknots
      integer*8 pyknots
      integer*8 pworkh
      integer*8 prsacoef
      integer*8 prracoef
      integer*8 prqacoef
      common /aph60/ nxdata, nydata, ldf, iflag, kxords, kyords
      common /aph66/ pxdata, pydata, pfdata
      common /aph66/ pxknots, pyknots, pworkh
      common /aph66/ prsacoef, prracoef, prqacoef
c End of Aphwrk

c Group Subs
c End of Subs


      data ev/1.6022d-19/,m_prot/1.67d-27/
      data issgvcxc/0/,sgvcxc/2.d-14/,isaphdir/1/
      data erad/25.d0/
      data mpe/48/,mpd/11/,mpr/1/
      data kxords/4/,kyords/4/

      end
c restore definition from mppl.BASIS

      subroutine aphdata
cProlog

c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants

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

c Group Rtfcn
c End of Rtfcn

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

c Group Subs
c End of Subs


      external aphiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(phtza)
      call clraddr(phtzn)
      call clraddr(phtn)
      call clraddr(phtt)
      call clraddr(phtln)
      call clraddr(phtlt)
      call clraddr(phtlsa)
      call clraddr(phtlra)
      call clraddr(phtlcx)
      call clraddr(phtlqa)
      call clraddr(pwsveh)
      call clraddr(pwsveh0)
      call clraddr(pwlemiss)
      call clraddr(pwelms)
      call clraddr(pwelms1)
      call clraddr(pwelms2)
      call clraddr(ppne3)
      call clraddr(ppne31)
      call clraddr(ppne32)
      call clraddr(ppne2)
      call clraddr(ppne21)
      call clraddr(ppne22)
      call clraddr(ppne41)
      call clraddr(ppne42)
      call clraddr(ppne51)
      call clraddr(ppne52)
      call clraddr(ppne61)
      call clraddr(ppne62)
      call clraddr(ppne71)
      call clraddr(ppne72)
      call clraddr(ppne81)
      call clraddr(ppne82)
      call clraddr(ppne91)
      call clraddr(ppne92)
      call clraddr(psvdum2)
      call clraddr(psvphcx)
      call clraddr(pekpt)
      call clraddr(pdkpt)
      call clraddr(pxdata)
      call clraddr(pydata)
      call clraddr(pfdata)
      call clraddr(pxknots)
      call clraddr(pyknots)
      call clraddr(pworkh)
      call clraddr(prsacoef)
      call clraddr(prracoef)
      call clraddr(prqacoef)

      return
      end
      subroutine aphdbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,8,94)
      return
      end
      subroutine aphwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /aphrtdm/ drtdm

c Group Physical_constants
      double precision ev, m_prot
      common /aph03/ ev, m_prot
c End of Physical_constants

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

c Group Rtfcn
c End of Rtfcn

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

c Group Subs
c End of Subs



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call aphdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Physical_constants")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ev",varadr(ev),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"m_prot",varadr(m_prot),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Data_input")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"issgvcxc",varadr(issgvcxc),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sgvcxc",varadr(sgvcxc),0,'double precision'
     &   ,'scalar', "m^2/s")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isaphdir",varadr(isaphdir),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"aphdir",varadr(aphdir),0,'character*120',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"data_directory",varadr(data_directory),0,
     &   'character*120','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Ionization_energy")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"erad",varadr(erad),0,'double precision',
     &   'scalar', "eV")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Rtdata")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"labelht",varadr(labelht),0,'character*120',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"htns",varadr(htns),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"htnn",varadr(htnn),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"htnt",varadr(htnt),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtza )
      i0001234=rtvare(drtdm,"htza",i000addr,1,'double precision',
     &   '(0:htns-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtzn )
      i0001234=rtvare(drtdm,"htzn",i000addr,1,'double precision',
     &   '(0:htns-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtn )
      i0001234=rtvare(drtdm,"htn",i000addr,1,'double precision',
     &   '(0:htnn)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtt )
      i0001234=rtvare(drtdm,"htt",i000addr,1,'double precision',
     &   '(0:htnt)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtln )
      i0001234=rtvare(drtdm,"htln",i000addr,1,'double precision',
     &   '(0:htnn)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtlt )
      i0001234=rtvare(drtdm,"htlt",i000addr,1,'double precision',
     &   '(0:htnt)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtlsa )
      i0001234=rtvare(drtdm,"htlsa",i000addr,1,'double precision',
     &   '(0:htnt,0:htnn,0:htns-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtlra )
      i0001234=rtvare(drtdm,"htlra",i000addr,1,'double precision',
     &   '(0:htnt,0:htnn,0:htns-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtlcx )
      i0001234=rtvare(drtdm,"htlcx",i000addr,1,'double precision',
     &   '(0:htnt,0:htnn,0:htns-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phtlqa )
      i0001234=rtvare(drtdm,"htlqa",i000addr,1,'double precision',
     &   '(0:htnt,0:htnn,0:htns-1)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Rtdegas")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mpe",varadr(mpe),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mpd",varadr(mpd),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mpr",varadr(mpr),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwsveh )
      i0001234=rtvare(drtdm,"wsveh",i000addr,1,'double precision',
     &   '(mpe,mpd,mpr)', "m**3/s")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwsveh0 )
      i0001234=rtvare(drtdm,"wsveh0",i000addr,1,'double precision',
     &   '(mpe,mpd,mpr)', "m**3/s")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwlemiss )
      i0001234=rtvare(drtdm,"wlemiss",i000addr,1,'double precision',
     &   '(mpe,mpd)', "W m**3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwelms )
      i0001234=rtvare(drtdm,"welms",i000addr,1,'double precision',
     &   '(mpe,mpd)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwelms1 )
      i0001234=rtvare(drtdm,"welms1",i000addr,1,'double precision',
     &   '(mpe,mpd,mpr)', "J/sec")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwelms2 )
      i0001234=rtvare(drtdm,"welms2",i000addr,1,'double precision',
     &   '(mpe,mpd,mpr)', "J/sec")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne3 )
      i0001234=rtvare(drtdm,"pne3",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne31 )
      i0001234=rtvare(drtdm,"pne31",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne32 )
      i0001234=rtvare(drtdm,"pne32",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne2 )
      i0001234=rtvare(drtdm,"pne2",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne21 )
      i0001234=rtvare(drtdm,"pne21",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne22 )
      i0001234=rtvare(drtdm,"pne22",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne41 )
      i0001234=rtvare(drtdm,"pne41",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne42 )
      i0001234=rtvare(drtdm,"pne42",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne51 )
      i0001234=rtvare(drtdm,"pne51",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne52 )
      i0001234=rtvare(drtdm,"pne52",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne61 )
      i0001234=rtvare(drtdm,"pne61",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne62 )
      i0001234=rtvare(drtdm,"pne62",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne71 )
      i0001234=rtvare(drtdm,"pne71",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne72 )
      i0001234=rtvare(drtdm,"pne72",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne81 )
      i0001234=rtvare(drtdm,"pne81",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne82 )
      i0001234=rtvare(drtdm,"pne82",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne91 )
      i0001234=rtvare(drtdm,"pne91",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppne92 )
      i0001234=rtvare(drtdm,"pne92",i000addr,1,'double precision',
     &   '(mpe,mpd)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psvdum2 )
      i0001234=rtvare(drtdm,"svdum2",i000addr,1,'double precision',
     &   '(mpe,mpe)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psvphcx )
      i0001234=rtvare(drtdm,"svphcx",i000addr,1,'double precision',
     &   '(mpe,mpe)', "m**3/s")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pekpt )
      i0001234=rtvare(drtdm,"ekpt",i000addr,1,'double precision','(mpe)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rlemin",varadr(rlemin),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rlemax",varadr(rlemax),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"erefmin",varadr(erefmin),0,
     &   'double precision','scalar', "eV")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"erefmax",varadr(erefmax),0,
     &   'double precision','scalar', "eV")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"delekpt",varadr(delekpt),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdkpt )
      i0001234=rtvare(drtdm,"dkpt",i000addr,1,'double precision','(mpd)'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rldmin",varadr(rldmin),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rldmax",varadr(rldmax),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"drefmin",varadr(drefmin),0,
     &   'double precision','scalar', "/m**3")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"drefmax",varadr(drefmax),0,
     &   'double precision','scalar', "/m**3")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"deldkpt",varadr(deldkpt),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"taumin",varadr(taumin),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"taumax",varadr(taumax),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"deltau",varadr(deltau),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Rtfcn")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rsa",jgrp,'double precision',"m**3/sec")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'k:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rra",jgrp,'double precision',"m**3/sec")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'k:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rcx",jgrp,'double precision',"m**3/sec")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 't0:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'n0:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'k:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "rqa",jgrp,'double precision',"J*m**3/sec")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'k:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "erl1",jgrp,'double precision',"J/sec")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "erl2",jgrp,'double precision',"J/sec")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ne:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'r:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "svdiss",jgrp,'double precision',"m**3/s")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'te:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readrt",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readeh",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readnw",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readehr1",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readehr2",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Aphwrk")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxdata",varadr(nxdata),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nydata",varadr(nydata),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxdata )
      i0001234=rtvare(drtdm,"xdata",i000addr,1,'double precision',
     &   '(1:nxdata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pydata )
      i0001234=rtvare(drtdm,"ydata",i000addr,1,'double precision',
     &   '(1:nydata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfdata )
      i0001234=rtvare(drtdm,"fdata",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ldf",varadr(ldf),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iflag",varadr(iflag),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kxords",varadr(kxords),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kyords",varadr(kyords),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxknots )
      i0001234=rtvare(drtdm,"xknots",i000addr,1,'double precision',
     &   '(1:nxdata+kxords)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyknots )
      i0001234=rtvare(drtdm,"yknots",i000addr,1,'double precision',
     &   '(1:nydata+kyords)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pworkh )
      i0001234=rtvare(drtdm,"workh",i000addr,1,'double precision',
     &   '(1:nxdata*nydata+2*kxords*(nxdata+1))', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prsacoef )
      i0001234=rtvare(drtdm,"rsacoef",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prracoef )
      i0001234=rtvare(drtdm,"rracoef",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prqacoef )
      i0001234=rtvare(drtdm,"rqacoef",i000addr,1,'double precision',
     &   '(1:nxdata,1:nydata)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Subs")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "aphread",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"aph.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine aphxpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.6) then
         call aphxp6(name1234)
      elseif (iseg.eq.8) then
         call aphxp8(name1234)
      else
         call baderr('aphxpf: impossible event')
      endif
      return
      end
      subroutine aphxp6(name1234)
cProlog
      character*(*) name1234
      external aph_handler
      external rsa
      external rra
      external rcx
      external rqa
      external erl1
      external erl2
      external svdiss
      external readrt
      external readeh
      external readnw
      external readehr1
      external readehr2
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'rsa') then
         call parexecf(aph_handler, 0, rsa)
      elseif (name1234 .eq. 'rra') then
         call parexecf(aph_handler, 1, rra)
      elseif (name1234 .eq. 'rcx') then
         call parexecf(aph_handler, 2, rcx)
      elseif (name1234 .eq. 'rqa') then
         call parexecf(aph_handler, 3, rqa)
      elseif (name1234 .eq. 'erl1') then
         call parexecf(aph_handler, 4, erl1)
      elseif (name1234 .eq. 'erl2') then
         call parexecf(aph_handler, 5, erl2)
      elseif (name1234 .eq. 'svdiss') then
         call parexecf(aph_handler, 6, svdiss)
      elseif (name1234 .eq. 'readrt') then
         call parexecf(aph_handler, 7, readrt)
      elseif (name1234 .eq. 'readeh') then
         call parexecf(aph_handler, 8, readeh)
      elseif (name1234 .eq. 'readnw') then
         call parexecf(aph_handler, 9, readnw)
      elseif (name1234 .eq. 'readehr1') then
         call parexecf(aph_handler, 10, readehr1)
      elseif (name1234 .eq. 'readehr2') then
         call parexecf(aph_handler, 11, readehr2)
      else
         call baderr('aphxp6: impossible event: '//name5678)
      endif
      return
      end
      subroutine aphxp8(name1234)
cProlog
      character*(*) name1234
      external aph_handler
      external aphread
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'aphread') then
         call parexecf(aph_handler, 12, aphread)
      else
         call baderr('aphxp8: impossible event: '//name5678)
      endif
      return
      end
      function aphbfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer aphbfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in aph')
      call baderr(name1234)
      aphbfcn = -1
      return
      end
