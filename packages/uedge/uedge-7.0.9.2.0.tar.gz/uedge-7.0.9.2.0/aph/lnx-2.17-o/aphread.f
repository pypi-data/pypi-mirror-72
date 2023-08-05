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
c     ./../aphread.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c







































































c-----------------------------------------------------------------------
      subroutine aphread
cProlog

c ... Set up tables for hydrogenic atomic-physics processes.

      implicit none

c ... Common blocks:
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
c nhdf, hdfilename
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
c istabon, aphdir, data_directory
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
c mpd, mpe

c ... Function:
c defined in the Basis runtime library
      integer utgetcl

c ... Local variable:
      integer MAXSTRING
      parameter (MAXSTRING=500)
      character*(MAXSTRING) aphdirx
      character*(MAXSTRING) adname
      character*(MAXSTRING) dataDir

      dataDir=data_directory

c ... Get length of string containing directory name (omitting trailing
c     blanks). Basis function basfilex expands $,~.
c     NOTE: basfilex will not exist for Python;
c     FACETS replaces aphdirx with aphdir in calls to findFile below
      call basfilex(aphdir,aphdirx)

c...  If istabon>0, set-up tables for ionization, recombination,
c...  charge exchange and energy loss.
      if (istabon .eq. 1) then
         call findFile('rates.adpak', aphdirx, dataDir, adname, isaphdir
     &      )
         call readrt(TRIM(adname))
      elseif (istabon .eq. 2) then
         call findFile('rates.strahl', aphdirx, dataDir, adname, 
     &      isaphdir)
         call readrt(TRIM(adname))
      elseif (istabon .eq. 3) then
         mpe=48
         mpd=11
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('eh.dat', aphdirx, dataDir, adname, isaphdir)
         call readeh(TRIM(adname))
         call findFile('atmc.dat', aphdirx, dataDir, adname, isaphdir)
         call readatmc(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 4) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('nwfits', aphdirx, dataDir, adname,isaphdir)
         call readnw(TRIM(adname))
         call setauxvar
      elseif ( (istabon .eq. 5) .or. (istabon .eq. 6) ) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('nwfits', aphdirx, dataDir, adname, isaphdir)
         call readnw(TRIM(adname))
         call setauxvar
         call splined
      elseif (istabon .eq. 8) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('ehr1.dat', aphdirx, dataDir, adname, isaphdir)
         call readehr1(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 9 .or. istabon .eq. 10) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('ehr2.dat', aphdirx, dataDir, adname, isaphdir)
         call readehr1(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 11) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('thin.dat', aphdirx, dataDir, adname, isaphdir)
         call readehr2(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 12) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('thickLyA.dat', aphdirx, dataDir, adname,isaphdir
     &      )
         call readehr2(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 13) then
         mpe=60
         mpd=15
         mpr=1
         call gallot("Rtdegas",0)
         call findFile('thickAllLy.dat',aphdirx,dataDir,adname,isaphdir)
         call readehr2(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 14 .or. istabon .eq. 15) then
         mpe=60
         mpd=15
         mpr=30
         call gallot("Rtdegas",0)
         call findFile('ehrtau.dat',aphdirx,dataDir,adname,isaphdir)
         call readehr1(TRIM(adname))
         call setauxvar
      elseif (istabon .eq. 16) then
         call readmc(nhdf,hdfilename)
c ...       Note that the rate parameter tables (in group Multicharge) have
c ...       the same ne-dimension and te-dimension for all species, so
c ...       the hydrogenic tables must have the same dimensions as the
c ...       impurity tables, if both are present.
      endif

      return
      end
c ... ............................................................
c ...  Determine where the data files exist.  The search order is:
c ...   dir1, then dir2, then $PWD
c ...  If flag is 1, then just assume $PWD and return
c ... ............................................................
      subroutine findFile(basename, dir1, dir2, fullname,flag)
cProlog
c
      implicit none
      character(*), intent(in) :: basename, dir1, dir2
      integer, intent(in) :: flag
      character(*), intent(out) :: fullname
      character*(500) :: fname
      logical fileExists

cc      if (flag/=1) then
      if (flag .ne. 1) then
         fullname=basename
         return
      endif
      fname=TRIM(dir1) // '/'//TRIM(basename)
      INQUIRE(FILE=TRIM(fname),EXIST=fileExists)
      if (fileExists) then
         fullname=fname
      else
         fname=TRIM(dir2) // '/'//TRIM(basename)
         INQUIRE(FILE=TRIM(fname),EXIST=fileExists)
         if (fileExists) then
            fullname=fname
         else
            fname=basename
            INQUIRE(FILE=TRIM(fname),EXIST=fileExists)
            if (fileExists) then
               fullname=fname
            else
               write(*,*) "Cannot find "//TRIM(fname)//" in:"
               write(*,*) TRIM(dir1)
               write(*,*) TRIM(dir2)
               write(*,*) " or current directory"
            endif
         endif
      endif
      return
cc       end subroutine
      end
c-----------------------------------------------------------------------
      subroutine readrt (fname)
cProlog
      implicit none
      character*(*) fname
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


c     local variables --
      integer ios, n, nget
      character idcod*8, idtyp*8, id1*32

c     procedures --
      external freeus, xerrab, gallot, readrt1

c----------------------------------------------------------------------c
c     Read ADPAK rate data from 'un*formatted' file (B. Braams)
c----------------------------------------------------------------------c

      call freeus(nget)
      open (nget, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab('**** ADPAK data file not found; set aphdir path')
      endif

c     read header --
c     un*formatted read for header data
      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,'(1x,1a120)') labelht

c     read dimensions --
c     un*formatted read for integer data
      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) htnt,htnn,htns

c     allocate storage --
      call gallot("Rtdata",0)

c     read abscissae and rates --
      call readrt1 (nget)

      close (nget)

      return
      end
c-----------------------------------------------------------------------
      subroutine readrt1 (nget)
cProlog
      implicit none
      integer nget
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


c     local variables --
      integer i, j, k, n
      character idcod*8, idtyp*8, id1*32

c     read abscissae --
c     un*formatted read for real data

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (htza(i),i=0,htns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (htzn(i),i=0,htns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (htt(i),i=0,htnt)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (htn(i),i=0,htnn)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (htlt(i),i=0,htnt)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (htln(i),i=0,htnn)

c     read rate coefficients --
c     un*formatted read for real data

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((htlsa(i,j,k),i=0,htnt),j=0,htnn),k=0,htns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((htlra(i,j,k),i=0,htnt),j=0,htnn),k=0,htns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((htlqa(i,j,k),i=0,htnt),j=0,htnn),k=0,htns-1)

      read (nget,'(2a8,i12,4x,a32)') idcod, idtyp, n, id1
      read (nget,*) (((htlcx(i,j,k),i=0,htnt),j=0,htnn),k=0,htns-1)

      return
      end
c-----------------------------------------------------------------------
      subroutine readnw (fname)
cProlog
      implicit none
      character*(*) fname
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
      integer ios, nget, jd, jt, jr

c     procedures --
      external freeus, xerrab

c----------------------------------------------------------------------c
c     Read density-dependent rate data from POST93 data file 'nwfits'
c----------------------------------------------------------------------c

      call freeus(nget)
      open (nget, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab('**** data file nwfits not found; set aphdir path')
      endif

      jr = 1

c     ionization rate (cm**3/sec):
      read(nget,9012)((wsveh(jt,jd,jr),jt=1,mpe),jd=1,mpd)
c     recombination rate (cm**3/sec):
      read(nget,9012)((wsveh0(jt,jd,jr),jt=1,mpe),jd=1,mpd)
c     hydrogen line radiation (erg-cm**3/sec):
      read(nget,9012)((wlemiss(jt,jd),jt=1,mpe),jd=1,mpd)

      close (nget)

c     convert to SI units:
      do 23000 jt=1,mpe
         do 23002 jd=1,mpd
            wsveh(jt,jd,jr)=max(1.d-50, wsveh(jt,jd,jr))*1.0d-06
            wsveh0(jt,jd,jr)=max(1.d-50, wsveh0(jt,jd,jr))*1.0d-06
            wlemiss(jt,jd)=max(1.d-75, wlemiss(jt,jd))*1.0d-13
23002    continue
23000 continue

 9012 format(10(6(1x,e12.5)/))

      return
      end
c-----------------------------------------------------------------------
      subroutine readeh (fname)
cProlog
      implicit none
      character*(*) fname
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
      integer ios, nget, jd, jt, jr

c     procedures --
      external freeus, xerrab

c----------------------------------------------------------------------c
c     Read density-dependent rate data from DEGAS file 'eh.dat'
c----------------------------------------------------------------------c

      call freeus(nget)
      open (nget, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab('**** DEGAS file eh.dat not found; set aphdir path'
     &      )
      endif

      jr = 1

c     ionization rate (cm**3/sec):
      read(nget,9012)((wsveh(jt,jd,jr),jt=1,mpe),jd=1,mpd)
c     recombination rate (cm**3/sec):
      read(nget,9012)((wsveh0(jt,jd,jr),jt=1,mpe),jd=1,mpd)
c     hydrogen line radiation (erg-cm**3/sec):
      read(nget,9012)((wlemiss(jt,jd),jt=1,mpe),jd=1,mpd)
c     electron energy loss (eV) per ionization:
      read(nget,9012)((welms(jt,jd),jt=1,mpe),jd=1,mpd)
c     n=3 excited state fraction:
      read(nget,9012)((pne3(jt,jd),jt=1,mpe),jd=1,mpd)
c     n=2 excited state fraction:
      read(nget,9012)((pne2(jt,jd),jt=1,mpe),jd=1,mpd)

      close (nget)

c     convert to SI units:
      do 23000 jt=1,mpe
         do 23002 jd=1,mpd
            wsveh(jt,jd,jr)=max(1.d-50, wsveh(jt,jd,jr))*1.0d-06
            wsveh0(jt,jd,jr)=max(1.d-50, wsveh0(jt,jd,jr))*1.0d-06
            wlemiss(jt,jd)=max(1.d-75, wlemiss(jt,jd))*1.0d-13
23002    continue
23000 continue

 9012 format(8(6(1x,e12.5)/))

      return
      end
c-----------------------------------------------------------------------
      subroutine readehr1 (fname)
cProlog
      implicit none
      character*(*) fname
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
      integer ios, nget, jd, jt, jr
      character*80 zdummy

c     procedures --
      external freeus, xerrab

c----------------------------------------------------------------------c
c     Read density-dependent hydrogenic rate file, e.g., 'ehr1.dat'
c----------------------------------------------------------------------c

      call freeus(nget)
      open (nget, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab(
     &      '**** hydrogenic rate file not found; set aphdir path or isa
     &phdir = 0')
      endif

      do 100 jr=1,mpr

         if (mpr.gt.1) then
c reads extra header lines in ehrtau.dat
            read(nget,9013) zdummy
         endif

c     ionization rate (cm**3/sec):
         read(nget,9013) zdummy
         do 12 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(wsveh(jt,jd,jr),jt=1,mpe)
   12       continue
c     recombination rate (cm**3/sec):
         read(nget,9013) zdummy
         do 14 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(wsveh0(jt,jd,jr),jt=1,mpe)
   14       continue
c     neutral-electron radiation loss rate (erg/sec):
         read(nget,9013) zdummy
         do 16 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(welms1(jt,jd,jr),jt=1,mpe)
   16       continue
c     continuum-electron radiation loss rate (erg/sec):
         read(nget,9013) zdummy
         do 18 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(welms2(jt,jd,jr),jt=1,mpe)
   18       continue

c     neutral "n=3/n=1" ratio:
         read(nget,9013) zdummy
         do 20 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(pne31(jt,jd),jt=1,mpe)
   20       continue
c     continuum "n=3/n=1" ratio:
         read(nget,9013) zdummy
         do 22 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(pne32(jt,jd),jt=1,mpe)
   22       continue
c     neutral "n=2/n=1" ratio:
         read(nget,9013) zdummy
         do 24 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(pne21(jt,jd),jt=1,mpe)
   24       continue
c     continuum "n=2/n=1" ratio:
         read(nget,9013) zdummy
         do 26 jd=1,mpd
            read(nget,9013) zdummy
            read(nget,9012)(pne22(jt,jd),jt=1,mpe)
   26       continue

  100    continue

      close (nget)

c     convert to SI units:
      do 23009 jt=1,mpe
         do 23011 jd=1,mpd
            do 23013 jr=1,mpr
               wsveh(jt,jd,jr)=max(1.d-50, wsveh(jt,jd,jr))*1.0d-06
               wsveh0(jt,jd,jr)=max(1.d-50, wsveh0(jt,jd,jr))*1.0d-06
               welms1(jt,jd,jr)=max(1.d-50, welms1(jt,jd,jr))*1.0d-07
               welms2(jt,jd,jr)=max(1.d-50, welms2(jt,jd,jr))*1.0d-07
23013       continue
23011    continue
23009 continue

 9012 format(10(6(1x,e12.5)/))
 9013 format(a80)

      return
      end
c-----------------------------------------------------------------------
      subroutine readehr2 (fname)
cProlog
      implicit none
      character*(*) fname
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
      integer ios, nget, jd, jt
      character*80 zdummy

c     procedures --
      external freeus, xerrab

c----------------------------------------------------------------------c
c     Read dens-depend hydro. + n=2-9 data, e.g., thin.dat
c----------------------------------------------------------------------c

      call freeus(nget)
      open (nget, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab(
     &      '**** hydrogenic rate file not found; set aphdir path')
      endif

c     ionization rate (cm**3/sec):
      read(nget,9013) zdummy
      do 12 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(wsveh(jt,jd,1),jt=1,mpe)
   12    continue
c     recombination rate (cm**3/sec):
      read(nget,9013) zdummy
      do 14 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(wsveh0(jt,jd,1),jt=1,mpe)
   14    continue
c     neutral-electron radiation loss rate (erg/sec):
      read(nget,9013) zdummy
      do 16 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(welms1(jt,jd,1),jt=1,mpe)
   16    continue
c     continuum-electron radiation loss rate (erg/sec):
      read(nget,9013) zdummy
      do 18 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(welms2(jt,jd,1),jt=1,mpe)
   18    continue
c     neutral "n=3/n=1" ratio:
      read(nget,9013) zdummy
      do 20 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne31(jt,jd),jt=1,mpe)
   20    continue
c     continuum "n=3/n=1" ratio:
      read(nget,9013) zdummy
      do 22 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne32(jt,jd),jt=1,mpe)
   22    continue
c     neutral "n=2/n=1" ratio:
      read(nget,9013) zdummy
      do 24 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne21(jt,jd),jt=1,mpe)
   24    continue
c     continuum "n=2/n=1" ratio:
      read(nget,9013) zdummy
      do 26 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne22(jt,jd),jt=1,mpe)
   26    continue
c     neutral "n=4/n=1" ratio:
      read(nget,9013) zdummy
      do 23008 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne41(jt,jd),jt=1,mpe)
23008 continue
c     continuum "n=4/n=1" ratio:
      read(nget,9013) zdummy
      do 23010 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne42(jt,jd),jt=1,mpe)
23010 continue
c     neutral "n=5/n=1" ratio:
      read(nget,9013) zdummy
      do 23012 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne51(jt,jd),jt=1,mpe)
23012 continue
c     continuum "n=5/n=1" ratio:
      read(nget,9013) zdummy
      do 23014 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne52(jt,jd),jt=1,mpe)
23014 continue
c     neutral "n=6/n=1" ratio:
      read(nget,9013) zdummy
      do 23016 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne61(jt,jd),jt=1,mpe)
23016 continue
c     continuum "n=6/n=1" ratio:
      read(nget,9013) zdummy
      do 23018 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne62(jt,jd),jt=1,mpe)
23018 continue
c     neutral "n=7/n=1" ratio:
      read(nget,9013) zdummy
      do 23020 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne71(jt,jd),jt=1,mpe)
23020 continue
c     continuum "n=7/n=1" ratio:
      read(nget,9013) zdummy
      do 23022 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne72(jt,jd),jt=1,mpe)
23022 continue
c     neutral "n=8/n=1" ratio:
      read(nget,9013) zdummy
      do 23024 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne81(jt,jd),jt=1,mpe)
23024 continue
c     continuum "n=8/n=1" ratio:
      read(nget,9013) zdummy
      do 23026 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne82(jt,jd),jt=1,mpe)
23026 continue
c     neutral "n=9/n=1" ratio:
      read(nget,9013) zdummy
      do 23028 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne91(jt,jd),jt=1,mpe)
23028 continue
c     continuum "n=9/n=1" ratio:
      read(nget,9013) zdummy
      do 23030 jd=1,mpd
         read(nget,9013) zdummy
         read(nget,9012)(pne92(jt,jd),jt=1,mpe)
23030 continue

      close (nget)

c     convert to SI units:
      do 23032 jt=1,mpe
         do 23034 jd=1,mpd
            wsveh(jt,jd,1)=max(1.d-50, wsveh(jt,jd,1))*1.0d-06
            wsveh0(jt,jd,1)=max(1.d-50, wsveh0(jt,jd,1))*1.0d-06
            welms1(jt,jd,1)=max(1.d-50, welms1(jt,jd,1))*1.0d-07
            welms2(jt,jd,1)=max(1.d-50, welms2(jt,jd,1))*1.0d-07
23034    continue
23032 continue

 9012 format(10(6(1x,e12.5)/))
 9013 format(a80)

      return
      end
c-----------------------------------------------------------------------
      subroutine readatmc (fname)
cProlog
      implicit none
      character*(*) fname
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
      integer ios, nget, je, jt

c     procedures --
      external freeus, xerrab

c----------------------------------------------------------------------c
c     Read charge exchange rate data from DEGAS file 'atmc.dat'
c----------------------------------------------------------------------c

      call freeus(nget)
      open (nget, file=fname, form='formatted', iostat=ios, status='old'
     &   )
      if (ios .ne. 0) then
         call xerrab(
     &      '**** DEGAS file atmc.dat not found; set aphdir path')
      endif

c     unused data:
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)

      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)

      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)
      read(nget,9015)((svdum2(jt,je),jt=1,mpe),je=1,mpe)

c     charge exchange rate (cm**3/sec):
      read(nget,9015)((svphcx(jt,je),jt=1,mpe),je=1,mpe)

      close (nget)

c     convert to SI units:
      do 23000 jt=1,mpe
         do 23002 je=1,mpe
            svphcx(jt,je)=svphcx(jt,je)*1.0d-06
23002    continue
23000 continue

 9015 format(/,8(6(1x,e12.5)/))

      return
      end
c-----------------------------------------------------------------------
      subroutine setauxvar
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


c-----------------------------------------------------------------------
c     Set density and temperature data for DEGAS and POST93 rate tables
c-----------------------------------------------------------------------

c     local variables --
      integer jd,je
      doubleprecision ddkpt,dekpt

c     dkpt = log10 of density(/m**3) :
      ddkpt = 0.5d0
      dkpt(1)=16.0d0
      do 23000 jd=2,mpd
         dkpt(jd)=dkpt(jd-1)+ddkpt
23000 continue
      rldmin=dkpt(1)
      rldmax=dkpt(mpd)
      drefmin=10.0d0**rldmin
      drefmax=10.0d0**rldmax
      deldkpt=(rldmax-rldmin)/dble(mpd-1)

c     ekpt = natural log of temperature(eV) :
      if (istabon .eq. 3) then
c old DEGAS tables start at 1 eV
         ekpt(1)=0.0d0
      else
c new tables start at .06 eV
         ekpt(1)=-1.2d0*log(10.0d0)
      endif

      dekpt = 0.1d0
      do 23002 je=2,mpe
         ekpt(je)=ekpt(je-1)+dekpt*log(10.0d0)
23002 continue
      rlemin=ekpt(1)
      rlemax=ekpt(mpe)
      erefmin=exp(rlemin)
      erefmax=exp(rlemax)
      delekpt=(rlemax-rlemin)/dble(mpe-1)

c minimum tabulated tau
      taumin = 1.d-4
c maximum tabulated tau
      taumax = 1.d+10
      deltau = log10(taumax/taumin)/(dble(mpr-2))

      return
      end
c-----------------------------------------------------------------------

      subroutine splined
cProlog
      implicit none
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

      external gchange, splined1

c     Construct 2-dimensional B-spline representation for atomic
c     physics rates as a function of temperature and density
c     (data from POST 93 tables)

c     Allocate arrays for spline fitting --
c temperature
      nxdata=mpe
c density
      nydata=mpd
      call gchange("Aphwrk",0)

      call splined1

      return
      end

c----------------------------------------------------------------------c

      subroutine splined1
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

      integer i,j

c     Define data arrays --
      do 23000 i=1,nxdata
         xdata(i)=ekpt(i)
23000 continue
      do 23002 j=1,nydata
         ydata(j)=dkpt(j)
23002 continue
      ldf=nxdata

c     Define the order of the spline fit
c     kxords=4		# cubic in x=log(temperature)
c     kyords=4		# cubic in y=log10(density)

c     Compute the coefficients --
c     first, for ionization:
      do 23004 i=1,nxdata
         do 23006 j=1,nydata
            if (istabon .eq. 5) then
               fdata(i,j)=log10( wsveh(i,j,1) )
            elseif (istabon .eq. 6) then
               fdata(i,j)=wsveh(i,j,1)
            endif
23006    continue
23004 continue
      iflag = 1
      call s2copy (nxdata,nydata,fdata,1,nxdata,rsacoef,1,nxdata)
      call B2INhT (xdata, nxdata, ydata, nydata, kxords, kyords, xknots, 
     &   yknots, rsacoef, ldf, workh, iflag)
c     next, for recombination:
      do 23008 i=1,nxdata
         do 23010 j=1,nydata
            if (istabon .eq. 5) then
               fdata(i,j)=log10( wsveh0(i,j,1) )
            elseif (istabon .eq. 6) then
               fdata(i,j)=wsveh0(i,j,1)
            endif
23010    continue
23008 continue
      iflag = 1
      call s2copy (nxdata,nydata,fdata,1,nxdata,rracoef,1,nxdata)
      call B2INhT (xdata, nxdata, ydata, nydata, kxords, kyords, xknots, 
     &   yknots, rracoef, ldf, workh, iflag)
c     next, for hydrogen line radiation:
      do 23012 i=1,nxdata
         do 23014 j=1,nydata
            if (istabon .eq. 5) then
               fdata(i,j)=log10( wlemiss(i,j) )
            elseif (istabon .eq. 6) then
               fdata(i,j)=wlemiss(i,j)
            endif
23014    continue
23012 continue
      iflag = 1
      call s2copy (nxdata,nydata,fdata,1,nxdata,rqacoef,1,nxdata)
      call B2INhT (xdata, nxdata, ydata, nydata, kxords, kyords, xknots, 
     &   yknots, rqacoef, ldf, workh, iflag)
      return
      end

c ------------- Routine to get set aphdir

      subroutine uedge_setDataDirectory(passedDataDirname)
cProlog
      implicit none
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
c istabon, aphdir, data_directory
      character*(*), intent(in) :: passedDataDirname
c     Allows the framework to set the data directory
      data_directory=passedDataDirname
      return
      end
