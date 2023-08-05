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
c     ./../fmombal.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































c!include "../mppl.h"
c!include "../sptodp.h"
c!include "api.h"
c	SEE FMOMBAL SUBROUTINE FOR INPUT PARAMETER SPECIFICATIONS
      subroutine coulfric(amu,denz2,dloglam,mntau,zi,capm,capn, ela,elab
     &   ,tempa)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision capm(3,miso,3,miso),denz2(miso), capn(3,3,miso,
     &   miso),mntau(miso,miso), amu(miso),tempa(miso), ela(*),elab(*),
     &   zi(miso,nzch)
c
c	COMPUTES COULOMB COLLISION FRICTION TERMS
c	ELA AND ELAB, WHERE THE FRICTION FORCE IS
c
c	R sub (ALPHA,Z) sup (M) == FRICTION FOR SPECIES ALPHA,
c					   CHARGE STATE Z (M-th FORCE)
c
c	= ZI(ALPHA,Z)*[ SUM(K) { ELA(M,K,ALPHA)*U sub (ALPHA,Z) (K) }
c
c			  + LAMBDA(ALPHA,M) ]
c
c	LAMBDA(ALPHA,M) = SUM(BETA) SUM(K) [ ELAB(M,K,ALPHA,BETA) *
c
c				    U sub (ALPHA) sup(2) (K) ]
c
c	ELA(M,K,ALPHA) = SUM(BETA)[ <<MA NA/TAU-AB>> CAPM(M,K,ALPHA,BETA) ]
c
c	ELAB(M,K,ALPHA,BETA) = <<MA NA/TAU-AB>> CAPN(M,K,ALPHA,BETA)
c
c*****	Calculate M''s and N''s for each isotope.
      call neomn(amu,capm,capn,tempa)
c*****	Evaluate calculating n/tauab.
      const=(4.0d0/3.0d0/sqrt(pi0))*4.0d0*pi0*(coulom/(4.0d0*pi0*epsilo)
     &   )**2 *dloglam
      do 100 misa=1,miso
c*****	Thermal velocity-m/s (TEMP in Joules)
         vtherm=sqrt(2.0d0*tempa(misa)/amu(misa)/promas)
         dza = (denz2(misa)*coulom) * ( const /(promas*amu(misa)*vtherm
     &      **3))
         do 90 misb=1,miso
            mntau(misa,misb) = dza * (denz2(misb)*coulom)
   90       continue
  100    continue
c*****	Calculate la(=ela) and lab (=elab)
      call neolab(mntau,capm,capn,ela,elab)
      return
      end
c---- End of subroutine coulfric ---------------------------------------
c-----------------------------------------------------------------------
      subroutine fmombal(amu,den,dloglam,epar,friction,gradp,gradt, 
     &   nuion,nurec,qcond,qneut,ucond,uneut,umass, parcurrent,tempa,
     &   natomic,misotope,nchstate,ldir,fricc)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

c Group Reduced_ion_variables
      double precision capm(3*5*3*5)
      double precision capn(3*5*3*5), caplam(3*5)
      double precision fmomenta(390), denz(5*26)
      double precision denmass(5*(26+1)), ela(3*3*5)
      double precision elab(3*5*3*5), mntau(5*5)
      double precision usol(3*26*5), sbar(3*6)
      double precision zi(5*26)
      common /api163/ capm, capn, caplam, fmomenta, denz, denmass, ela
      common /api163/ elab, mntau, usol, sbar, zi
c End of Reduced_ion_variables

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
c istimingon,ttimpc
      real sec4, gettime, tsval
      doubleprecision amu(misotope), den(misotope*(nchstate+1)), gradp(
     &   misotope*nchstate), gradt(misotope*nchstate), nurec(misotope*
     &   nchstate), nuion(misotope*(nchstate+1)), tempa(misotope), qcond
     &   (*), friction(*), ucond(*), uneut(*), qneut(*), fricc(*)
      doubleprecision amat(3*(6)*3*(6)), denz2(5), caplams(3*5), uresp(5
     &   *390), usave(3*26*5)
      integer natomic(misotope)
      integer ndima
      save uresp, usave, caplams
c
c	****	DESCRIPTION OF INPUT VARIABLES	****
c
c
c	ALL PHYSICAL QUANTITIES ARE IN MKS UNITS, INCLUDING
c	TEMPERATURE IN JOULES (1 eV = 1.6022E-19 Joule)
c	DENSITY IN 1/METERS**3
c	ELECTRIC FIELD IN VOLTS/METER
c	VELOCITY IN METERS/SEC
c	HEAT FLUX IN JOULE/(METER**2 - SEC)
c
c	INTEGERS:
c
c	  MISOTOPE
c		NUMBER OF DISTINCT ISOTOPES (DIFFERENT MASSES).
c		THE ORDERING OF ALL ARRAYS A(ISO) BELOW MUST BE AS FOLLOWS:
c		FIRST ISOTOPE (ISO=1) <==> ELECTRONS
c		SUBSEQUENT ISOTOPES (2 <= ISO <= MISOTOPE)
c
c	  NATOMIC(1:MISOTOPE)
c		FOR IONS, THE NUCLEAR CHARGE OF ISOTOPE (ISO). FOR ELECTRONS,
c		NATOMIC(1) == 1.
c
c	  NCHSTATE
c		THE MAXIMUM OF NATOMIC(ISO) OVER ALL MISOTOPE ISOTOPES
c
c	  LDIR
c		IF LDIR >= 2, THEN A COMPLETE (NEW) MATRIX INVERSION
c		IS DONE TO COMPUTE THE FLOWS. FOR LDIR < 2, AN INCREMENTAL
c		MATRIX INVERSION IS DONE, BASED ON A PREVIOUS CALL TO
c		FMOMBAL WITH LDIR >= 2. THIS SAVES CPU TIME AND IS USEFUL
c		WHEN SMALL VARIABLE PERTURBATIONS
c		ARE MADE TO COMPUTE THE NUMERICAL JACOBIAN.
c
c
c	REAL VARIABLES:
c
c	  AMU(1:MISOTOPE)
c		ATOMIC MASS OF ISOTOPE (ISO), RELATIVE TO THE PROTON MASS.
c		FOR EXAMPLE, AMU(1) = 5.45E-4.
c
c	  DEN(1:MISOTOPE,0:NCHSTATE)	[1/M**3]
c		DEN(ISO,NZ) IS THE DENSITY OF THE ISOTOPE
c		(ISO) AND CHARGE STATE (NZ). NOTE THAT NZ=0 CORRESPONDS
c		TO THE NEUTRAL DENSITY (NEEDED FOR ATOMIC PHYSICS), AND
c		NZ = NATOM(ISO) TO THE FULLY STRIPPED ION. DEN
c		SHOULD BE PRESCRIBED AT THE SAME SPATIAL GRID POINT
c		REQUIRED FOR THE VELOCITIES AND HEAT FLUXES.
c
c	  DLOGLAM
c		LOG(LAMBDA) REQUIRED FOR THE COULOMB COLLISION RATE
c
c	  EPAR		[VOLTS/METER]
c		PARALLEL ELECTRIC FIELD (INPUT)
c
c	  FRICTION(1:MISOTOPE,1:NCHSTATE)		[JOULES/METER**4]
c		FRICTION(ISO,NZ) IS THE PARALLEL COMPONENT OF
c		THE FRICTION FORCE (COULOMB+ATOMIC COLLISIONS)
c		FOR ISOTOPE ISO, CHARGE STATE NZ (NOT INCLUDING NEUTRALS)
c
c         FRICC(1:MISOPTE,1:NCHSTATE,1:4)                [JOULES/METER**4]
c               COMPONENTS OF FRICTION WITH
c               FRICC(,,1) = ela(1,)*usol(1,,) for velocity
c               FRICC(,,2) = ela(2,)*usol(2,,) for qcond
c               FRICC(,,3) = ela(3,)*usol(3,,) for h
c               FRICC(,,4) = caplam ? same for all isotope charge states
c               FRICC(,,5) = ioniz and recomb totals
c
c	  GRADP,GRADT(1:MISOTOPE,1:NCHSTATE)		[JOULES/METER**4]
c		GRADP,GRADT(ISO,NZ) IS THE PARALLEL COMPONENT OF
c		THE PRESSURE(TEMPERATURE) GRADIENT,
c
c		GRADP,T  =  B dot Grad (P,T) / |B|
c
c		EVALUATED AT THE SAME SPATIAL GRID POINT WHERE THE
c		PARALLEL SPEEDS AND HEAT FLUXES ARE TO BE COMPUTED, OF
c		CHARGE STATE NZ OF ISOTOPE ISO. NEUTRAL GRADIENTS
c		ARE NOT INCLUDED HERE
c
c	  NUION(1:MISOTOPE,0:NCHSTATE)	[1/SEC]
c		NUION(ISO,NZ) IS THE IONIZATION RATE (DUE TO
c		ELECTRON IMPACT) FOR ISOTOPE ISO, STATE NZ, FOR NZ = 0
c		TO NZ = NATOM(ISO)-1
c
c	  NUREC(1:MISOTOPE,1:NCHSTATE)	[1/SEC]
c		NUREC(ISO,NZ) IS THE RECOMBINATION RATE (DUE TO
c		ELECTRON IMPACT) FOR ISOTOPE ISO, STATE NZ, FOR NZ = 1
c		TO NZ = NATOM(ISO)
c
c	  PARCURRENT			[A/METER**2]
c		PARALLEL CURRENT AT PRESENT GRID POINT (OUTPUT, COMPUTED FROM OHMS LAW)
c
c	  QCOND(1:MISOTOPE,1:NCHSTATE)	[JOULE/(METER**2-SEC)]
c		QCOND(ISO,NZ) IS THE PARALLEL RANDOM HEAT FLUX FOR CHARGE
c		STATE NZ OF ISOTOPE ISO IN RESPONSE TO THE ELECTRIC
c		AND PRESSURE FORCES. (NEUTRALS NOT INCLUDED HERE)
c		THIS, TOGETHER WITH UCOND AND EPAR, COMPRISES THE
c		OUTPUT FROM THIS CALCULATION
c
c	  UCOND(1:MISOTOPE,1:NCHSTATE)	[METER/SEC]
c		PARALLEL FLOW SPEED (ABSOLUTE, NOT RELATIVE TO UMASS)
c		OF EACH CHARGE STATE FOR EACH ISOTOPE (NOT
c		INCLUDING NEUTRALS)
c
c	  QNEUT(1:MISOTOPE), UNEUT(1:MISOTOPE)
c		HEAT FLUX AND PARALLEL FLOW SPEED OF NEUTRAL
c		SPECIES FOR EACH ISOTOPE. IF QNEUT UNKNOWN, USE 0 FOR NOW
c
c	  TEMPA(1:MISOTOPE)		[JOULES]
c		TEMPA(ISO) IS THE TEMPERATURE AT GRID POINT
c		FOR ISOTOPE ISO
c
c	  UMASS		[METERS/SEC]
c		THE (EXTERNALLY PROVIDED) MEAN MASS FLOW ALONG
c		MAGNETIC FIELD LINES, WHICH IS THE SUM OVER ALL
c		IONIZED SPECIES (AND ELECTRONS) OF THE INDIVIDUAL
c		MASS-DENSITY WEIGHTED FLOWS:
c
c		UMASS = SUM ( MASS*DENSITY*U|| )
c 		        ________________________
c		        SUM ( MASS*DENSITY )
c
c		THE EQUATION FOR EVOLVING UMASS IN TIME IS OBTAINED
c		BY SUMMING THE INDIVIDUAL MOMENTUM EQUATIONS FOR ALL
c		IONS. THIS SUMMATION ANNIHILATES THE DOMINANT COULOMB
c		FRICTION TERMS AND INCLUDES RESIDUAL COLLISIONAL
c		COUPLING (DUE TO ATOMIC PHYSICS) TO THE NEUTRALS
c		POPULATION (THROUGH UNEUT,QNEUT).
c

c ... Start timing impurity calculations.
      if (istimingon .eq. 1 .and. misotope .gt. 1) tsval = gettime(sec4)

c ... Initialize amat array.
      ndima=3*(6)*3*(6)
      do 23000 i=1,ndima
         amat(i)=zero
23000 continue

c****	Setup zi, mass-density, Z*e*density arrays
      call setden(amu,den,denmass,denz,denz2,zi)

c****	Setup force arrays (gradp, gradt stuff)
      call setforce(den,denz,denmass,epar,gradp,gradt, tempa,uneut,qneut
     &   ,umass,fmomenta,nuion)

c*****	Compute Coulomb friction coefficients la, lab
      call coulfric(amu,denz2,dloglam,mntau,zi,capm,capn, ela,elab,tempa
     &   )

c*****	Compute response matrices for inversion of momentum equations
c*****	in charge-state space
      call zrespond(den,denmass,zi,ela,nuion,nurec,uresp, usave,caplams,
     &   fmomenta,ldir)

c*****	Solve average-ion equations in mass-isotope space
      call mrespond(elab,zi,den,denmass,uresp,sbar, 3*(miso+1),amat,
     &   nurec,umass,ldir)

c*****	Compute individual ion flows (for all charge states)
c
c	NOTE: USOL(m=1,Z,mass) = PARTICLE FLOW RELATIVE TO UMASS
c
c	      USOL(m=2,Z,mass) = -(2/5)*CONDUCTIVE HEAT FLUX / PRESSURE
c
c	      USOL(m=3,Z,mass) = HIGHER-ORDER FLOW (H)
c
      call mzrespond(elab,uresp,sbar,caplam,caplams,usol, usave,den,denz
     &   ,parcurrent,qcond,ucond,tempa,umass,ldir)
c
c	COMPUTE FRICTION FORCES
c
      call getfrict(friction,fricc,caplam,denmass,ela,nuion, nurec,usol,
     &   zi)

c ... End timing impurity calculations.
      if (istimingon .eq. 1 .and. misotope .gt. 1) ttimpc = ttimpc + 
     &      gettime(sec4) - tsval

      return
      end
c---- End of subroutine fmombal ----------------------------------------
c-----------------------------------------------------------------------
      subroutine getfrict(friction,fricc,caplam,denmass,ela, nuion,nurec
     &   ,usol,zi)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision friction(miso,nzch), usol(3,nzch,miso), fricc(miso
     &   ,nzch,5)
      doubleprecision nuion(miso,0:nzch), nurec(miso,nzch)
      doubleprecision denmass(miso,0:nzch), caplam(3,miso), ela(3,3,miso
     &   ), zi(miso,nzch)
cONLY FRICTION FORCE
      m = 1
      do 23000 misa = 1,miso
         nzmax = natom(misa)
         do 23002 nz = 1,nzmax
            friction(misa,nz) = zi(misa,nz) * ( ela(m,1,misa)*usol(1,nz,
     &         misa) + ela(m,2,misa)*usol(2,nz,misa) + ela(m,3,misa)*
     &         usol(3,nz,misa) + caplam(m,misa) )
            fricc(misa,nz,1) = zi(misa,nz)*ela(m,1,misa)*usol(1,nz,misa)
            fricc(misa,nz,2) = zi(misa,nz)*ela(m,2,misa)*usol(2,nz,misa)
            fricc(misa,nz,3) = zi(misa,nz)*ela(m,3,misa)*usol(3,nz,misa)
            fricc(misa,nz,4) = zi(misa,nz)*caplam(m,misa)
            friction(misa,nz) = friction(misa,nz) - denmass(misa,nz)*
     &         usol(m,nz,misa)* (nuion(misa,nz) + nurec(misa,nz))*al32(m
     &         )
            fricc(misa,nz,5) = - denmass(misa,nz)*usol(m,nz,misa)* (
     &         nuion(misa,nz) + nurec(misa,nz))*al32(m)
            if ( nz.gt.1 ) friction(misa,nz) = friction(misa,nz) + usol(
     &            m,nz-1,misa) *denmass(misa,nz-1) * nuion(misa,nz-1) * 
     &            al32(m)
            fricc(misa,nz,5) = fricc(misa,nz,5) + usol(m,nz-1,misa) *
     &         denmass(misa,nz-1) * nuion(misa,nz-1) * al32(m)
            if ( nz.lt.nzmax ) friction(misa,nz) = friction(misa,nz) + 
     &            usol(m,nz+1,misa) *denmass(misa,nz+1) * nurec(misa,nz+
     &            1) * al32(m)
            fricc(misa,nz,5) = fricc(misa,nz,5) + usol(m,nz+1,misa) *
     &         denmass(misa,nz+1) * nurec(misa,nz+1) * al32(m)
23002    continue
23000 continue
      return
      end
c---- End of subroutine getfrict ---------------------------------------
c-----------------------------------------------------------------------
      subroutine inicon
cProlog
c*****	******************************************************************
c*****	INICON loads the common block containing physical constants and  *
c*****	conversion constants.                                           *
c*****	Last Revision:12/85 W.A.Houlberg and S.E.Attenberger ORNL.       *
c*****	******************************************************************
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

c*****	Physical constants.
c*****	Elementary charge - (coulomb).
      coulom=1.6022d-19
c*****	Permittivity of free space - (farad/meter).
      epsilo=8.8419d-12
c*****	Proton mass - (kilogram).
      promas=1.6726d-27
c*****	Unit conversions.
c*****	Joules per keV.
      xj7kv=1.6022d-16
c****	Constants
      one = 1.0d0
c*****	Calculate pi0 for greatest accuracy.
      pi0=acos(-one)
c*****	Set zero for initializing arrays.
      zero=0.d0
c*****	Integer constants
      ilam1 = 1
      ilam2 = 2
      ilam3 = 3
      iacci = 4
      iforc = 5

      al32(1) = 1.d0
      al32(2) = 5.d0/2.d0
      al32(3) = 35.d0/8.d0
      return
      end
c---- End of subroutine inicon -----------------------------------------
c-----------------------------------------------------------------------
      subroutine initmombal(misotope,natomic,nchstate)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      integer natomic(misotope)

cElectrons MUST be 1st element
      mise = 1

c****	Load common block elements
      miso = misotope
      nzch = nchstate
      if ( miso.gt.5 ) call xerrab('MISO > MXMISO')
      if ( nzch.gt.26 ) call xerrab('NZCH > MXNZCH')
      do 23000 misa = 1,miso
         natom(misa) = natomic(misa)
23000 continue

      return
      end
c---- End of subroutine initmombal -------------------------------------
c-----------------------------------------------------------------------
      subroutine mrespond(elab,zi,den,denmass,uresp,sbar, nmat,amat,
     &   nurec,umass,ldir)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      integer nmat
      doubleprecision elab(3,miso,3*miso),uresp(3,nzch,miso,5), sbar(3,
     &   miso+1), sbar0(3*(6)), ubar0(3*(6)), zi(miso,*),amat(nmat,nmat)
     &   ,denmass(miso,0:nzch)
      doubleprecision den(miso,0:nzch), nurec(miso,nzch)
      doubleprecision usum(26), bmat(3*(6)*3*(6))
      integer nrow(3*(6)), z1
      integer i, j
      save nrow, bmat, sbar0, ubar0
cSpace for acci = acceleration force
      macc = miso+1
cFlow
      mflow = 1
      z1 = 1
cNorm for AI force
      fanorm = one / (totmass * anorm)
c
c	COMPUTE ZI,DENMASS-WEIGHTED AVERAGES OF RESPONSE FUNCTIONS
c	AND FORM INTER-ISOTOPIC COUPLING MATRIX
c	NOTE: FOR MISA = 1 (ELECTRONS), M = 1 (FLOW), REPLACE
c	WITH NO NET FLOW CONDITION SUM M(ALPHA)*DEN(ALPHA,Z)U(ALPHA,Z) = 0
c	TO AVOID SINGULAR MATRIX (IN REF. FRAME OF MASS FLOW)
c
c	AUGMENT (FOR MISA=MACC, K=1) SYSTEM WITH EQUATIONS FOR MEAN
c	ACCELERATION TERM AI [=ubar(1,macc)]
c
c	RHO*AI + SUM( M N NUrec U(1,Z=1,alpha) ) = NEUTRAL SOURCE
c	AND U(1,1,alpha) MUST BE EXPRESSED IN TERMS OF AI, UBAR
c
c	JPAR = SUM( DENZ * U(1,Z,alpha) )
c
c
c	NOTE THAT U(m,Z,alpha) = -BIGLAM(m,Z,alpha;mp,beta)*ubar(mp,beta)
c	WHERE BIGLAM = SUM(over kp) elab(kp,alpha,mp,beta)*uresp(m,Z,alpha;kp)
c
      j = 3*(macc-1)
      do 23000 mmisb = 1,nmat
c electron "isotope"
         amat(mflow,mmisb) = zero
         amat(1+j,mmisb) = zero
         amat(2+j,mmisb) = zero
         amat(3+j,mmisb) = zero
23000 continue
      sbar(mflow,mise) = zero
      sbar(mflow,macc) = sumforce * fanorm
      sbar(2,macc) = zero
      sbar(3,macc) = zero
ctotmass*anorm * fanorm
      amat(1+j,1+j) = one
cNOT USED FOR ANYTHING PHYSICAL
      amat(2+j,2+j) = one
cNOT USED FOR ANYTHING PHYSICAL
      amat(3+j,3+j) = one
      do 10 misa = 1,miso
         nz = natom(misa)
         dnur1 = (fanorm*denmass(misa,z1))*nurec(misa,z1)
c
c	COMPUTE ACCELERATION SOURCE, MATRIX ELEMENTS
c
         sbar(1,macc) = sbar(1,macc) - dnur1* uresp(mflow,z1,misa,iforc)
         amat(1+j,1+j) = amat(1+j,1+j) + dnur1* uresp(mflow,z1,misa,
     &      iacci)
         do 23003 nzsum = 1,nz
c
c     	REPLACE ELECTRON MOMENTUM WITH NO NET FLOW CONDITION
c     	(IN REFERENCE FRAME MOVING WITH MASS FLOW)
c
            rhomass = denmass(misa,nzsum)/totmass
            sbar(mflow,mise) = sbar(mflow,mise) + rhomass*uresp(mflow,
     &         nzsum,misa,iforc)
            amat(mflow,1+j) = amat(mflow,1+j) - rhomass*uresp(mflow,
     &         nzsum,misa,iacci)
23003    continue
         i = 3*(misa-1)
         do 10 m = 1,3
            if ( (misa.ne.mise) .or. (m.ne.mflow) )then
               sbar(m,misa) = ddot_u(nz,zi(misa,1),miso,uresp(m,z1,misa,
     &            iforc),3)
               amat(m+i,1+j) = -ddot_u(nz,zi(misa,1),miso,uresp(m,z1,
     &            misa,iacci),3)
            endif
            do 10 mpmisb = 1,3*miso
               do 23007 nzb = 1,nz
                  usum(nzb) = uresp(m,nzb,misa,ilam1)*elab(ilam1,misa,
     &               mpmisb) + uresp(m,nzb,misa,ilam2)*elab(ilam2,misa,
     &               mpmisb) + uresp(m,nzb,misa,ilam3)*elab(ilam3,misa,
     &               mpmisb)
23007          continue
               if ( (misa.ne.mise) .or. (m.ne.mflow) ) amat(m+i,mpmisb) 
     &               = ddot_u(nz,zi(misa,z1),miso,usum,1)
c
c	PERFORM SUMS OVER MISA (ISOTOPE MASS A)
c
               if ( m.eq.mflow )then
                  amat(1+j,mpmisb) = amat(1+j,mpmisb) - dnur1*usum(z1)
                  do 23009 nzsum = 1,nz
                     amat(mflow,mpmisb) = amat(mflow,mpmisb) + (denmass(
     &                  misa,nzsum)/totmass)*usum(nzsum)
23009             continue
               endif
   10          continue
c
c	ADD DIAGONAL ELEMENTS
c
cIgnore electron momentum balance here
      mmin = 1
      do 20 mmisa = mmin+1,3*miso
         amat(mmisa,mmisa) = amat(mmisa,mmisa) + one
   20    continue
c
c	INVERT MATRIX TO OBTAIN REDUCED FLOWS
c
      if ( ldir.gt.1 )then
         call dgefa_u(amat,nmat,nmat,nrow,info)
         nmat2 = nmat*nmat
         call dcopy_u(nmat2,amat,1,bmat,1)
         call dcopy_u(nmat,sbar,1,sbar0,1)
         if ( info.ne.0 )then
            call xerrab('mrespond:  Condition No. = 0 in Solver')
         endif
      else
         do 23012 i = 1,nmat
            sbar(i,1) = sbar(i,1) + sbar0(i) - ddot_u(nmat,amat(i,1),
     &         nmat,ubar0,1)
23012    continue
      endif
      call dgesl_u(bmat,nmat,nmat,nrow,sbar,0)
      if ( ldir.gt.1 )call dcopy_u(nmat,sbar,1,ubar0,1)
      return
      end
c---- End of subroutine mrespond ---------------------------------------
c-----------------------------------------------------------------------
      subroutine mzrespond(elab,uresp,ubar,caplam,caplams,usol, usave,
     &   den,denz,parcurrent,qcond,ucond,tempa,umass,ldir)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision elab(3*miso,3*miso),uresp(3*nzch,miso,5), ubar(3,
     &   miso+1), usol(3*nzch,miso), denz(miso,nzch), den(miso,0:nzch), 
     &   qcond(miso,nzch), ucond(miso,nzch)
      doubleprecision caplam(3,miso), caplams(3*miso), usave(*), tempa(
     &   miso)
      integer m,misa
      acci1 = ubar(1,miso+1)
      parcurrent = zero
c/csnorm
      uscale = one
c/(csnorm * tempnorm * dennorm)
      qscale = one
      mtotal = 3*miso
      do 23000 mmisa = 1,mtotal
         misa = 1 + (mmisa-1)/3
         m = mmisa - (misa-1)*3
         caplam(m,misa) = ddot_u(mtotal,ubar,1,elab(mmisa,1),mtotal)
23000 continue

      do 23002 misa = 1,miso
         do 23004 knz = 1,3*natom(misa)
            usol(knz,misa) = uresp(knz,misa,iforc) - uresp(knz,misa,1)*
     &         caplam(1,misa) - uresp(knz,misa,2)*caplam(2,misa) - uresp
     &         (knz,misa,3)*caplam(3,misa) + uresp(knz,misa,iacci)*acci1
23004    continue
c
c	CONVERT BACK TO ABSOLUTE (NOT RELATIVE TO UMASS) FLOW
c	CONVERT TO RANDOM HEAT FLUX (MULT BY -2.5) FOR K=2
c	AND STORE NORMED FORM FOR EXTERNAL USE
c
         k1 = 1
         do 23006 nz = 1,natom(misa)
            k2 = k1+1
            ucond(misa,nz) = (usol(k1,misa) + umass) * uscale
            qcond(misa,nz) = -2.5d0*usol(k2,misa)*den(misa,nz) *tempa(
     &         misa) * qscale
            parcurrent = parcurrent + denz(misa,nz)*ucond(misa,nz)
            k1 = k1 + 3
23006    continue
23002 continue
c
c	STORE SOLUTION FOR INCREMENTAL MODE
c
      if ( ldir.gt.1 )then
         mtot2 = mtotal*nzch
         call dcopy_u(mtot2,usol,1,usave,1)
         call dcopy_u(mtotal,caplam,1,caplams,1)
         acci0 = acci1
      endif
      return
      end
c---- End of subroutine mzrespond --------------------------------------
c-----------------------------------------------------------------------
      subroutine neolab(mntau,capm,capn,ela,elab)
cProlog
c*****	******************************************************************
c*****	NEOLAB calculates the neoclassical friction coefficients.        *
c*****	References:                                                      *
c*****	Hirshman, Sigmar, Nucl Fusion 21 (1981) 1079 (H&S).              *
c*****	Last Revision: 5/94 W.A.Houlberg and S.P.Hirshman ORNL.          *
c*****	Input:                                                           *
c*****	miso-number of isotopes.                                         *
c*****	mntau(misb)-ma<<na/tauab>>-kg/m**3/s.                           *
c*****	     -Eqn 5.25 of H&S.                                    *
c*****	capm(3,miso,3,miso)-matrix of test particle elements.            *
c*****	capn(3,miso,3,miso)-matrix of field particle elements.           *
c*****	Output:                                                          *
c*****	ela(3,3,misa)-test particle component-kg/m**3/s.                 *
c*****	elab(3,misa,3,misb)-field particle component-kg/m**3/s.           *
c*****	******************************************************************
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision mntau(miso,miso)
      doubleprecision ela(3,3,miso), elab(3,miso,3,miso)
      doubleprecision capm(3,miso,3,miso), capn(3,miso,3,miso)

c ... Initialize ela array.
      do 23000 i=1,3
         do 23002 j=1,3
            do 23004 k=1,miso
               ela(i,j,k)=zero
23004       continue
23002    continue
23000 continue

      do 40 misb=1,miso
         do 30 misa=1,miso
            do 20 k=1,3
               do 10 j=1,3
c*****	Sum over isotopes misb for test particle component.
                  ela(j,k,misa)=ela(j,k,misa) +mntau(misa,misb)*capm(j,
     &               misa,k,misb)
c*****	Field particle component.
                  elab(j,misa,k,misb)=mntau(misa,misb)*capn(j,misa,k,
     &               misb)
   10             continue
   20          continue
   30       continue
   40    continue
      return
      end
c---- End of subroutine neolab -----------------------------------------
c-----------------------------------------------------------------------
      subroutine neomn(amu,capm,capn,tempa)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

c*****	******************************************************************
c*****	NEOMN calculates the test particle (M) and field particle (N)    *
c*****	matrix elements of the collision operator using the Laguerre    *
c*****	polynomials of order 3/2 as basis functions for each isotopic   *
c*****	species combination.                                            *
c*****	References:                                                      *
c*****	Hirshman, Sigmar, Nucl Fusion 21 (1981) 1079 (H&S).              *
c*****	Hirshman, Phys Fluids 20 (1977) 589.                             *
c*****	Last Revision: 3/94 W.A.Houlberg and S.E.Attenberger ORNL.       *
c*****	Input:                                                           *
c*****	miso-number of isotopes.                                         *
c*****	amu(miso)-atomic mass of isotopes-arbitrary.                     *
c*****	tempa(miso)-temperature of isotopes-arbitrary.                      *
c*****	Output:                                                          *
c*****	capm(3,miso,3,miso)-matrix of test particle elements.            *
c*****	capn(3,miso,3,miso)-matrix of field particle elements.           *
c*****	Comments:                                                        *
c*****	The indices on the matrices are one greater than the notation in *
c*****	the review article so as to avoid 0 as an index.                *
c*****	******************************************************************
      doubleprecision capm(3,miso,3,miso), capn(3,miso,3,miso)
      doubleprecision amu(miso), tempa(miso)
c*****	Loop over isotope a.
      do 20 misa=1,miso
c*****	Loop over isotope b.
         do 10 misb=1,miso
c*****	Ratio of masses.
            xmab=amu(misa)/amu(misb)
c*****	Ratio of temperatures.
            xtab=tempa(misa)/tempa(misb)
c*****	Ratio of thermal velocities, vtb/vta.
            xab=sqrt(xmab/xtab)
c*****	Elements of M.
            xab2=xab**2
            yab32=(one+xab2)*sqrt(one+xab2)
            yab52=(one+xab2)*yab32
            yab72=(one+xab2)*yab52
            yab92=(one+xab2)*yab72
c*****	Eqn 4.11 for M00 H&S.
            capm(1,misa,1,misb)=-(one+xmab)/yab32
c*****	Eqn 4.12 for M01 H&S.
            capm(1,misa,2,misb)=-(3.0d0/2.0d0)*(one+xmab)/yab52
c*****	Eqn 4.15 for M02 H&S.
            capm(1,misa,3,misb)=-(15.0d0/8.0d0)*(one+xmab)/yab72
c*****	Eqn 4.8 for M10 H&S.
            capm(2,misa,1,misb)=capm(1,misa,2,misb)
c*****	Eqn 4.13 for M11 H&S.
            capm(2,misa,2,misb)=-(13.0d0/4.0d0+4.0d0*xab2+(15.0d0/2.0d0)
     &         *xab2**2) /yab52
c*****	Eqn 4.16 for M12 H&S.
            capm(2,misa,3,misb)=-(69.0d0/16.0d0+6.0d0*xab2+(63.0d0/4.0d0
     &         )*xab2**2) /yab72
c*****	Eqn 4.8 for M20 H&S.
            capm(3,misa,1,misb)=capm(1,misa,3,misb)
c*****	Eqn 4.8 for M21 H&S.
            capm(3,misa,2,misb)=capm(2,misa,3,misb)
c*****	Eqn 5.21 for M22 H&S.
            capm(3,misa,3,misb)=-(433.0d0/64.0d0+17.0d0*xab2+(459.0d0/
     &         8.0d0)*xab2**2 +28.0d0*xab2**3+(175.0d0/8.0d0)*xab2**4)/
     &         yab92
c*****	Elements of N.
c*****	Momentum conservation, Eqn 4.11 for N00 H&S.
            capn(1,misa,1,misb)=-capm(1,misa,1,misb)
c*****	Eqn 4.9 and 4.12 for N01 H&S.
            capn(1,misa,2,misb)=-xab2*capm(1,misa,2,misb)
c*****	Eqn 4.15 for N02 H&S - corrected by multiplying rhs by (Ta/Tb)
            capn(1,misa,3,misb)=-xab2**2*capm(1,misa,3,misb)
c*****	Momentum conservation, Eqn 4.12 for N10 H&S.
            capn(2,misa,1,misb)=-capm(2,misa,1,misb)
c*****	Eqn 4.14 for N11 H&S.
            capn(2,misa,2,misb)=(27.0d0/4.0d0)*xtab*xab2/yab52
c*****	Eqn 4.17 for N12 H&S.
            capn(2,misa,3,misb)=(225.0d0/16.0d0)*xtab*xab2**2/yab72
c*****	Momentum conservation for N20.
            capn(3,misa,1,misb)=-capm(3,misa,1,misb)
c*****	Eqn 4.9 and 4.17 for N21 H&S.
            capn(3,misa,2,misb)=(225.0d0/16.0d0)*xab2/yab72
c*****	Eqn 5.22 for N22 H&S.
            capn(3,misa,3,misb)=(2625.0d0/64.0d0)*xtab*xab2**2/yab92
   10       continue
   20    continue
      return
      end
c---- End of subroutine neomn ------------------------------------------
c-----------------------------------------------------------------------
      subroutine printit(amu,den,epar,zi,ela, caplam,sbar,usol,fmom,
     &   denmass,nuion,nurec, gradp,gradt,parcurrent,xirl,tempa,uneut,
     &   umass)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision sbar(3,miso+1), usol(3,nzch,miso)
      doubleprecision den(miso,0:nzch), caplam(3,miso)
      doubleprecision denmass(miso,0:nzch)
      doubleprecision nuion(miso,0:nzch), nurec(miso,nzch), gradp(miso,*
     &   ), gradt(miso,*), ela(3,3,miso), zi(miso,nzch), fmom(3,nzch,
     &   miso), amu(miso), tempa(miso), uneut(miso)

c*****	Print out average-ion quantities
      write(*,490)xirl,umass
  490 format(' XI(IGRID) = ',1pe10.3,' UMASS = ',1pe10.3,/, 
     &   ' NOTE: RESULTS ARE PHYSICALLY VALID IF |UBAR| < VTHERM AND', 
     &   ' |QBAR/P| < VTHERM')
      acci = acci0*anorm
      sumflow = 0.d0
      sumaflow= 0.d0
      do 55 misa = 1,miso
         vtherm=sqrt(2.0d0*tempa(misa)/amu(misa)/promas)
cOnly look at flow, heat flow
         do 55 m = 1,2
            if ( m.eq.1 )then
               write(*,500)m,amu(misa),sbar(m,misa), 1000.d0*tempa(misa)
     &            /xj7kv,vtherm,caplam(m,misa)
               write(*,510)
               if ( misa.ne.1 ) write(*,520)0,uneut(misa),den(misa,0),
     &               nuion(misa,0)
            elseif (m.eq.2) then
               write(*,505)m,amu(misa),sbar(m,misa)
               write(*,530)
            endif
            nzmax = natom(misa)
            do 55 nz = 1,nzmax
               force = fmom(m,nz,misa)
               friction = zi(misa,nz) * ( ela(m,1,misa)*usol(1,nz,misa) 
     &            + ela(m,2,misa)*usol(2,nz,misa) + ela(m,3,misa)*usol(3
     &            ,nz,misa) + caplam(m,misa) )
               friction = friction - denmass(misa,nz)*usol(m,nz,misa)* (
     &            nuion(misa,nz) + nurec(misa,nz))*al32(m)
               if ( nz.gt.1 )friction = friction + usol(m,nz-1,misa) *
     &               denmass(misa,nz-1) * nuion(misa,nz-1) * al32(m)
               if ( nz.lt.nzmax )friction = friction + usol(m,nz+1,misa) 
     &               *denmass(misa,nz+1) * nurec(misa,nz+1) * al32(m)
               if ( m.eq.1 )then
                  force = force + denmass(misa,nz)*acci
                  sumflow = sumflow + denmass(misa,nz)*usol(1,nz,misa)
                  sumaflow= sumaflow+ denmass(misa,nz)*abs(usol(1,nz,
     &               misa))
                  write(*,550)nz,usol(m,nz,misa),force,friction, den(
     &               misa,nz),zi(misa,nz),nuion(misa,nz),nurec(misa,nz)
               elseif ( m.eq.2 ) then
                  pres = den(misa,nz)*tempa(misa)
                  write(*,550)nz,-2.5d0*usol(m,nz,misa)*pres, force,
     &               friction,gradp(misa,nz),den(misa,nz)*gradt(misa,nz)
               endif
   55          continue
      sumaflow = max(sumaflow,totmass*abs(umass))
  500 format(/' UBAR (m=',i1,', mass=',1pe9.2,') = ',1pe10.3, 
     &   ' (m/sec)  TEMP = ',1pe10.3,' (eV)  VTHERM = ',1pe10.3, 
     &   ' (m/sec)','  LAMBDA =',1pe10.3)
  505 format(/' QBAR/P(m=',i1,', mass=',1pe9.2,') = ',1pe10.3, 
     &   ' (m/sec)')
  510 format('  Z  U||-UMASS', '     FORCE    FRICTION', 
     &   '       DEN         ZI     NU-ION     NU-REC')
  520 format(i3,1pe11.3,2(11x),1pe11.3,11x,1pe11.3)
  530 format('  Z      Q||', '       FORCE    FRICTION', 
     &   '   GRAD||P   N*GRAD||T')
  550 format(i3,1p8e11.3)
      write(*,560)sumflow/sumaflow,parcurrent, totmass*acci,epar
  560 format(/' NORMALIZED NET MASS FLOW, SUM(RHO*U)/SUM(RHO*|U|)', 
     &   ' -> 0 (U = U||-UMASS) = ',1pe11.3, /' J||(calc) = ',1pe11.3,/, 
     &   ' MEAN INERTIAL TERM RHO*AI   = ',1pe11.3,/, ' E||     = ',1
     &   pe11.3/)
      return
      end
c---- End of subroutine printit ----------------------------------------
c-----------------------------------------------------------------------
      subroutine setden(amu,den,denmass,denz,denz2,zi)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision amu(miso), denz2(miso)
      doubleprecision den(miso,0:nzch), denmass(miso,0:nzch), denz(miso,
     &   *)
      doubleprecision zi(miso,*)
c*****	Sum over isotopes for electron density-isotope 1.
      do 23000 misa = 2,miso
         do 23002 nza = 1,natom(misa)
            denz(misa,nza) = den(misa,nza)*dble(nza)*coulom
23002    continue
23000 continue
      denz(1,1) = -den(1,1)*coulom
c*****	Compute mass-density, ZI, SUM(ZI), and total mass density
      totmass = zero
      do 23004 misa = 1,miso
         bmass = amu(misa)*promas
         denz2(misa)=zero
         do 23006 nza = 1,natom(misa)
            denmass(misa,nza) = bmass*den(misa,nza)
            zi(misa,nza) = den(misa,nza)*dble(nza)**2
            denz2(misa)=denz2(misa) + zi(misa,nza)
            totmass = totmass + denmass(misa,nza)
23006    continue
23004 continue
c*****	Compute neutral mass-density
      do 23008 misa = 2,miso
         denmass(misa,0) = amu(misa)*promas*den(misa,0)
23008 continue
c*****	Provide pedestal for zi to avoid matrix inversion singularity
      ziped = 1.d-4
      do 23010 misa=1,miso
         zisum = zero
         do 23012 nza=1,natom(misa)
            zi(misa,nza)=zi(misa,nza)/denz2(misa) + ziped
            zisum = zisum + zi(misa,nza)
23012    continue
czi normed to 1
         do 23014 nza = 1,natom(misa)
            zi(misa,nza) = zi(misa,nza)/zisum
23014    continue
23010 continue
      return
      end
c---- End of subroutine setden -----------------------------------------
c-----------------------------------------------------------------------
      subroutine setforce(den,denz,denmass,epar,gradp,gradt, tempa,uneut
     &   ,qneut,umass,fmom,nuion)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision gradp(miso,*), gradt(miso,*), nuion(miso,0:nzch), 
     &   denmass(miso,0:nzch), den(miso,0:nzch), denz(miso,nzch), fmom(3
     &   ,nzch,miso), tempa(miso), uneut(miso), qneut(miso)
c
c	COMPUTE FORCES PROPORTIONAL TO GRAD(P), GRAD(T)
c
c	FMOMENTA(1,ALPHA) = GRAD(P sub alpha) -e*N*E|| - M N NU(ion)( UN - U ) delta(Z,1)
c	FMOMENTA(2,ALPHA) =-2.5 N GRAD T
c	FMOMENTA(3,ALPHA) = 0
c
      sumforce = zero
      do 23000 misa = 1,miso
         do 23002 nz = 1,natom(misa)
            fmom(1,nz,misa) = gradp(misa,nz) - denz(misa,nz)*epar
            fmom(2,nz,misa) = -2.5d0*den(misa,nz)*gradt(misa,nz)
            fmom(3,nz,misa) = 0.d0
            if ( nz.eq.1 .and. misa.ne.mise )then
               fmom(1,nz,misa) = fmom(1,nz,misa) - al32(1)*denmass(misa,
c(Neutral mass-density)
     &            0)*
     &           nuion(misa,0)*(uneut(misa) - umass)
               presa = den(misa,nz)*tempa(misa)
               fmom(2,nz,misa) = fmom(2,nz,misa) - al32(2)*denmass(misa,
c(Neutral mass-density)
     &            0)*
     &           nuion(misa,0)*(-2.d0*qneut(misa)/(5.d0*presa))
            endif
            sumforce = sumforce - fmom(1,nz,misa)
23002    continue
23000 continue
      return
      end
c---- End of subroutine setforce ---------------------------------------
c-----------------------------------------------------------------------
      subroutine uinvm2(k,n,a,b,x,nrow,scas,lss,msbs, nbrt,istore,iflag)
cProlog
c	ALSO, BE SURE TO LINK IN BLAS LIBRARY (-LBLAS)
      implicit doubleprecision (a-h,o-z), integer(i-n)
c*****	******************************************************************
c*****	UINVM2 performs the matrix inversion for a system of k equations *
c*****	each having n points.                                           *
c*****	Previous Last Revision: 3/90 W.A.Houlberg ORNL.                  *
c*****	Last Revision: 5/94 S.P.Hirshman ORNL (multiple right sides)     *
c*****	        and BLAS routines                                 *
c*****	Input:                                                           *
c*****	k-number of equations per block.                                 *
c*****	n-number of nodes in each equation (number of blocks)            *
c*****	nbrt-number of right hand sides (independent source terms)       *
c*****	a(n*k*(3*k))-coefficient array.                                  *
c*****	b(n*k,nbrt)-right sides (sources) loaded as 1-D vector b(k,n,nbrt)   *
c*****	loaded as one dimensional x(n,k,nbrt).                           *
c*****	iflag: if non-zero, routine is being called with previously
c*****	istore: if non-zero, store for restart scas,lss,msb vectors
c*****	       computed values of nrow, a
c*****	       use iflag != 0 for incremental update
c*****	Output:                                                          *
c*****	x(n*k,nbrt)-solution array loaded as one dimensional x(k,n,nbrt).*
c*****	nrow(i)-record of row permutations for i-th row of matrix a      *
c*****	 during the gaussian elimination with partial pivoting.   *
c*****	 dimension in calling routine must be >= n*k              *
c*****	iflag-error flag for solution.                                   *
c*****	=0 normal solution.                                         *
c*****	=1 singular matrix found in inverting a.                    *
c*****	Comments:                                                        *
c*****	We wish to approximate the solution of the system of linear     *
c*****	equations fx=b where f is a block tridiagonal matrix of order n *
c*****	and each block is of order k. thus there n*k equations in the   *
c*****	system. Let f(i,j) represent the (i,j) block of the matrix f.   *
c*****	Let b(i) denote the corresponding k by 1 block of the vector b. *
c*****	Then the 3k X n*k array a contains on entry into UINVM the   *
c*****	nontrivial information to describe the coefficient matrix f.    *
c*****	The matrix "A"           is described more easily by displaying *
c*****	the transpose of "A" which follows (note: "A" is stacked            *
c*****	so that the diagonal elements are aligned in the same column)   *
c*****	0 block    f(1,1)      f(1,2)   b(1)   1st k eqns..             *
c*****	f(2,1)     f(2,2)     f(2,3)    b(2)   next k eqns..            *
c*****	...        ...        ...      ...    ...                       *
c*****	f(n-1,n-2) f(n-1,n-1) f(n-1,n)  b(n-1) next to last k eqns..    *
c*****	f(n,n-1)   f(n,n)     0 block   b(n)   last k eqns..            *
c	INDEXING OF MATRIX A
c	F(I,J,M,N)*X(N,J) = B(M,I)    ,   AMAT(L) = LMAT(I,J,M,N) strung out
c
c	HERE, 1 <= (M,N) <= J,  1 <= I <= N,  I-1 <= J <= I+1
c
c	THUS, A(L) = LMAT(I,J,M,N) FOR
c
c	L = N + (M-1)*KX3 + (J-I+1)*K + (I-1)*KSQ3
c
c	WHERE KX3 = 3*K (OR 3*K+1 for original version), KSQ3 = K * KX3
c
c*****	Partial pivoting is within a subblock of k rows.                *
c*****	For full partial pivoting we would have to search over 2k rows  *
c*****	for the pivot element.                                          *
c*****	Double precision may be required for s,sca,anor,raia,raig,x,a.  *
c*****	******************************************************************
      doubleprecision a(3*n*k*k), b(n*k,nbrt), x(n*k,nbrt), scas(*)
      integer lss(*), msbs(*)
      integer nrow(n*k)
      nk=n*k
      km1=k-1
      k2m1=k+km1
      k2=k+k
      k3=k2+k
c*****	Previously computed a-matrix inversion
      if ( iflag.ne.0 )goto 1000
c*****	Shift first row blocks 1 block to left (on input, 1st block = 0)
      na=0
      do 30 j=1,k
         napk=na+k
         call dcopy_u(k2,a(napk+1),1,a(na+1),1)
         napk2=na+k2
         do 23001 i=1,k
            a(napk2+i)=0.0d0
23001    continue
         na=na+k3
   30    continue
      na=0
      do 23003 i=1,nk
         nrow(i)=na
         na=na + k3
23003 continue
 1000 continue
c*****	Begin loop through n blocks.
c*****	nl=(iblock-1)*k+1,  nh=(iblock+1)*k  for iblock=1,...,n-1.
      nl=1
      icount = 0
      do 50 iblock = 1,n
         nh=nl+k2m1
         nhs=nl+km1
         kblock = k
         krow = k3
         if ( iblock.eq.n )then
            nh = nk
            nhs= nk
            kblock = km1
            krow = k
         endif
         do 90 j=1,kblock
c*****	Determine element of maximum modulus in next column.
c*****	Only allow permutations within blocks of k rows.
            if ( iflag.ne.0 )goto 1010
            s=0.0d0
            do 23007 l=nl,nhs
               sa=a(nrow(l)+j)
               if (sa.lt.0.0d0) sa=-sa
               if (s.lt.sa) then
cPivot row
                  ni=l
                  s=sa
               endif
23007       continue
            if (s.eq.0.0d0) then
c*****	Singular matrix found.
               iflag=1
               return
            endif
c*****	Row exchange (pivot)
            ms=nrow(ni)
            nrow(ni)=nrow(nl)
            nrow(nl)=ms
            anor=a(ms+j)
            jp1=j+1
 1010       continue
            nl=nl+1
c*****	Gaussian elimination within block
            do 23009 l=nl,nh
               icount = icount+1
               if ( iflag.eq.0 )then
                  sca=a(nrow(l)+j)
                  if (sca.ne.0.0d0) then
                     sca=sca/anor
c*****	  Subtract pivot row elements (ms) from row (l) elements
                     call daxpy_u(krow-jp1+1,-sca,a(ms+jp1),1, a(nrow(l)
     &                  +jp1),1)
                  endif
                  ls = nrow(l)/k3 + 1
                  msb= ms/k3 + 1
                  if ( istore.ne.0 )then
                     lss(icount) = ls
                     msbs(icount) = msb
                     scas(icount) = sca
                  endif
               else
                  ls = lss(icount)
                  msb= msbs(icount)
                  sca = scas(icount)
               endif
c*****	  Subtract pivot row right side from other right-hand side(s)
               if (sca.ne.0.0d0)call daxpy_u(nbrt,-sca,b(msb,1),nk,b(ls,
     &               1),nk)
23009       continue
   90       continue
c*****	Move block 2 to 1, block 3 to 2, 0 out block 3 of rows used in
c*****	this stage that will also be used in next.
         if ( iblock.ne.n .and. iflag.eq.0 )then
            do 23011 l=nl,nh
               call dcopy_u(k2,a(nrow(l)+k+1),1,a(nrow(l)+1),1)
               do 23013 j=1,k
                  a(nrow(l)+j+k2)=0.0d0
23013          continue
23011       continue
         endif
         if (nh.gt.nk) call xerrab('uinvm2:  nh > nk')
   50    continue
      if ( icount .gt. 2*k*k*n ) call xerrab('uinvm2:  icount > 2*k*k*n'
     &      )
c*****	Process back substitution in blocks of k equations.  1st 2 blocks
c*****	are special, but have special coding only for the 1st block.
      if (a(nrow(nk)+k).eq.0.0d0) then
c*****	Singular matrix found.
         iflag=1
         return
      endif
      do 100 lb = 1,nbrt
         nkb = nrow(nk)/k3 + 1
         x(nk,lb)=b(nkb,lb)/a(nrow(nk)+k)
         neq=nk-1
         if (k.ne.1) then
            ntrm=1
            do 23016 lk=km1,1,-1
               neqb = nrow(neq)/k3 + 1
               s = b(neqb,lb) - ddot_u(ntrm,x(neq+1,lb),1,a(nrow(neq)+lk
     &            +1),1)
               x(neq,lb)=s/a(nrow(neq)+lk)
               ntrm=ntrm+1
               neq=neq-1
23016       continue
         endif
         if ( neq.le.0 )goto 100
  180    ntrm=k
         do 23018 lk=k,1,-1
            neqb = nrow(neq)/k3 + 1
            s = b(neqb,lb) - ddot_u(ntrm,x(neq+1,lb),1,a(nrow(neq)+lk+1)
     &         ,1)
            x(neq,lb)=s/a(nrow(neq)+lk)
            ntrm=ntrm+1
            neq=neq-1
23018    continue
         if (neq.gt.0) goto 180
  100    continue
      iflag=0
      return
      end
c---- End of subroutine uinvm2 -----------------------------------------
c-----------------------------------------------------------------------
      subroutine zrespond(den,denmass,zi,ela,nuion,nurec, uresp,usave,
     &   caplams,fmom,ldir)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      parameter( NSIZE = 2*3*3*26 )
      doubleprecision zmat(702,5), source(3*26,5)
      doubleprecision amat(702), asource(3*26*5)
      doubleprecision den(miso,0:nzch), zi(miso,nzch), ela(3,3,miso)
      doubleprecision nuion(miso,0:nzch), nurec(miso,nzch)
      doubleprecision uresp(3,nzch,miso,5), usave(3,nzch,miso)
      doubleprecision fmom(3,nzch,miso),denmass(miso,0:nzch)
      doubleprecision caplams(3,miso), xsol(5*3*26)
      doubleprecision scaz(NSIZE,5)
      integer nrowz(3*26,5), lsz(NSIZE,5), msz(NSIZE,5)
      save zmat, source, scaz, lsz, msz, nrowz
c
c	FOR LDIR > 1, DO COMPLETE NEW MATRIX INVERSION
c	FOR LDIR <=1, DO INCREMENTAL MATRIX INVERSION, USING
c
c	[ ZMAT(old) + del-ZMAT ][USOL(old) + del-U] = SOURCE + del-SOURCE
c
c	==>   ZMAT(old)*USOL(new) = S(new) + [S(old) - ZMAT(new)*USOL(old)]
c
c	HERE, ZMAT(new)*USOL(old) = ZMAT*USAVE - S(IACCI)*ACCI(old) -
c
c	 - S(1)*CAPLAM(1) - S(2)*CAPLAM(2) - S(3)*CAPLAM(3)
c
c
c	COMPUTE NORMS FOR AI
c	AI = ANORM * aI, WHERE
c	ANORM = SUM(ela(1,1,a))/SUM(DENMASS)
c
      elsum = zero
      do 23000 misa = 1,miso
         elsum = elsum + ela(1,1,misa)
23000 continue
      anorm = elsum / totmass
c
c	FOR EACH FIXED ISOTOPE, COMPUTE RESPONSE FUNCTIONS WHICH SOLVE
c	THE EQUATION (FOR ALPHA FIXED)
c
c	ZMAT(m,Z,mm,ZZ) u(mm,ZZ;k) = SOURCE(m,Z;k)
c
c	WHERE FOR
c
c	k = 1, 2, 3 [ uresp(m,Z;k) == ULAMk ]
c
c	SOURCE(m,Z;k)  = +ZI(alpha,Z) delta(m,k)
c
c	k = 4 [uresp(m,Z;k) == UACCI] SOURCE = DEN(alpha,Z)*MASS(alpha) delta(m,1)
c
c	k = 5 [uresp(m,Z;k) == UFORC] SOURCE = FORCE(alpha,m,Z)   (see paper...)
c
c	THEN, THE SOLUTION (IN TERMS OF THE INTER-SPECIES COUPLING TERMS
c	LAMBDA AND OTHER DRIVING TERMS) IS:
c
c	u(alpha,m,Z) =  SUM(k=1,2,3) [-ULAMk * LAMBDA(alpha,k) ]
c
c	          + UACCI * AI + UFORC
c
c	NOTE THAT THE ORDERING (STACKING) OF SOURCE AND URESP IS THE
c	SAME (SEE SUBROUTINE ZSOURCE FOR DETAILS)
c
      kx3 = 3*3
      kxsq3 = kx3 * 3
      do 100 misa = 1,miso
         nz = natom(misa)
         nkz = nz * 3
cNumber of response array elements per isotope
         nresp = 5*nkz
         nknz = kxsq3*nz
c
c	SET UP SOURCE TERMS: SOURCE(M,Z,k=1,NBA)
c	NOTE: Z = 1,NATOM IS DIFFERENT SIZE FOR EACH ISOTOPE
c

c ... Initalize asource array.
         do 23003 i=1,nresp
            asource(i)=zero
23003    continue

         call zsource(asource,zi,den,fmom(1,1,misa),denmass,misa,nz)
         nforc = nkz*(iforc-1)
         nacci = nkz*(iacci-1)
         if ( ldir.le.1 )then
            do 23005 i = 1,nkz
               asource(i+nforc) = asource(i+nforc) + ( source(i,misa) + 
     &            asource(i+nacci)*acci0 - (asource(i)*caplams(1,misa) + 
     &            asource(i+nkz)*caplams(2,misa) +asource(i+2*nkz)*
     &            caplams(3,misa)) )
23005       continue
         endif
c
c	SET UP Z-MATRIX ARRAY ELEMENTS
c

c ... Initialize amat array.
         do 23007 i=1,nknz
            amat(i)=zero
23007    continue

         do 10 m = 1,3
            do 10 mp= 1,3
               i1 = mp + kx3*(m-1)
               i2 = m + nforc
               do 10 jz= 1,nz
cconsecutive block-by-block index
                  index = i1 + (jz-1)*kxsq3
                  is = i2 + (jz-1)*3
c
c	LOWER DIAGONAL ELEMENTS (IONIZATION FROM LOWER CHARGE STATE)
c
                  ozi = al32(m)/zi(misa,jz)
                  if (jz.gt.1)then
                     jp = jz-1
                     if ( (m.eq.mp) )then
                        amat(index) = ozi*denmass(misa,jp)*nuion(misa,jp
     &                     )
                        if ( ldir.le.1 ) asource(is) = asource(is) - 
     &                        amat(index)*usave(mp,jp,misa)
                     endif
                  endif
c
c	DIAGONAL ELEMENTS
c
                  index = index + 3
                  amat(index) = ela(m,mp,misa)
                  if ( (m.eq.mp) ) amat(index) = amat(index) - denmass(
     &                  misa,jz)* ( nuion(misa,jz) + nurec(misa,jz) )*
     &                  ozi
                  if ( ldir.le.1 ) asource(is) = asource(is) - amat(
     &                  index)*usave(mp,jz,misa)
c
c	UPPER DIAGONAL ELEMENTS (RECOMBINATION FROM HIGHER CHARGE STATE)
c
                  if (jz.lt.nz)then
                     index = index + 3
                     jp = jz+1
                     if ( (m.eq.mp) )then
                        amat(index) = ozi*denmass(misa,jp)*nurec(misa,jp
     &                     )
                        if ( ldir.le.1 ) asource(is) = asource(is) - 
     &                        amat(index)*usave(mp,jp,misa)
                     endif
                  endif
   10             continue
c
c	SOLVE TRIDIAGONAL SYSTEM WITH NBA RIGHT SIDES STORED IN SOURCE
c	STORE FOR FAST (INCREMENTAL) RECALCULATION (LDIR = 0,1)
c
         noff = 1 + nforc
         istore = 1
         if ( ldir.gt.1 )then
            call dcopy_u(nkz,asource(noff),1,source(1,misa),1)
            lflag = 1
            noff = 1
            nr = 5
            iflag = 0
         else
            lflag = iforc
            nr = 1
            iflag = 1
            call dcopy_u(nknz,zmat(1,misa),1,amat,1)
         endif
         call uinvm2(3,nz,amat,asource(noff),xsol(noff), nrowz(1,misa),
     &      scaz(1,misa),lsz(1,misa),msz(1,misa), nr,istore,iflag)
         if ( ldir.gt.1 )call dcopy_u(nknz,amat,1,zmat(1,misa),1)
         if ( iflag.ne.0 )then
            call xerrab(" CALL TO UINVM2 FAILED! ")
         endif
c
c	STORE SOLUTION VECTOR IN RESPONSE ARRAY URESP FOR EACH ISOTOPE
c	URESP(KXA=1,2,3,NATOM,n=1,..,NBA).
c	Note response arrays are arranged consecutively
c
         do 23012 ntype = lflag,5
            noff = 1 + nkz*(ntype-1)
            call dcopy_u(nkz,xsol(noff),1,uresp(1,1,misa,ntype),1)
23012    continue
  100    continue
      return
      end
c---- End of subroutine zrespond ---------------------------------------
c-----------------------------------------------------------------------
      subroutine zsource(source,zi,den,fmom,denmass,misa,nz)
cProlog
      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group Reduced_ion_constants
      double precision coulom, epsilo, promas, xj7kv, one, pi0, zero
      integer miso, nzch, mise, ilam1, ilam2, ilam3, iacci, iforc
      double precision sumforce, totmass, anorm, acci, acci0, al32(3)
      integer natom(5)
      common /api150/ miso, nzch, mise, ilam1, ilam2, ilam3, iacci
      common /api150/ iforc, natom
      common /api153/ coulom, epsilo, promas, xj7kv, one, pi0, zero
      common /api153/ sumforce, totmass, anorm, acci, acci0, al32
c End of Reduced_ion_constants

      doubleprecision zi(miso,*), den(miso,0:nz), source(3,nz,5), fmom(3
     &   ,*)
      doubleprecision denmass(miso,0:nz)
      do 20 jz= 1,nz
         do 20 m = 1,3
            if ( m.eq.1 )then
               source(m,jz,ilam1) = one
               source(m,jz,iacci) = denmass(misa,jz) * anorm / zi(misa,
     &            jz)
            elseif ( (m.eq.ilam2) .or. (m.eq.ilam3) ) then
               source(m,jz,m) = one
            endif
            source(m,jz,iforc) = fmom(m,jz)/zi(misa,jz)
   20       continue
      return
      end
c---- End of subroutine zsource ----------------------------------------
c-----------------------------------------------------------------------
