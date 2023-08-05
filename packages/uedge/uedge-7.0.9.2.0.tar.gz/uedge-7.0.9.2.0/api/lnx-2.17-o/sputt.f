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
c     ./../sputt.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































      SUBROUTINE SYLD96(MATT,MATP,CION,CIZB,CRMB)
      IMPLICIT none
      INTEGER MATT,MATP,CION,CIZB
      doubleprecision CRMB

c############################################################################
c ** - modifications by TDR 2/20/98
c
c ** - Coding received from David Elder, Feb. 6, 1998; reduced argument
c ** - list for subroutine (deleted cneutd,cbombf,cbombz,cebd); deleted
c ** - params, Use statement for cyield instead of include statement
c ** - REAL -> real for mppl; ALOG10 -> log10
c
c ** -Input variables:
c     cion  # integer atomic number of impurity, e.g., for carbon, cion=6
c     cizb  # integer max charge state of plasma ions; hydrogen cizb=1
c     crmb  # real mass number of plasma ions; =2 for deut., =3 for tritium
c
c ** -Output variables:
c     matt  # integer flag giving target material
c     matp  # integer flag giving plasma material
c
c###########################################################################
c
c  *********************************************************************
c  *                                                                   *
c  *  SYLD96:  SETS UP SPUTTERING YIELD DATA IN COMMON AREA CYIELD.    *
c  *  THE DATA IS TAKEN FROM ECKSTEIN IPP 9/82 (FEB 1993)              *
c  *                                                                   *
c  *  ARGUMENTS :-                                                     *
c  *  MATT : CODE INTEGER GIVING MATERIAL USED IN TARGET               *
c  *  MATP : CODE INTEGER GIVING BACKGROUND MATERIAL                   *
c  *  CNEUTD : NEUT SPUTTER OPTION - deleted from this version 2/20/98 *
c  *                                                                   *
c  *********************************************************************
c
c     INCLUDE "PARAMS"
ctdr      include    'params'
c     INCLUDE "CYIELD"
cdtr      include    'cyield'

c Group Cyield
      double precision ceth(7,12), cetf(7,12), cq(7,12), redf_haas
      integer ntars
      logical cidata(7,12)
      common /api170/ ntars
      common /api171/ cidata
      common /api173/ ceth, cetf, cq, redf_haas
c End of Cyield
c ceth,cetf,cq,ntars,cidata

      doubleprecision ETH(7,12), ETF(7,12), Q(7,12), EBD(12)
      LOGICAL IDATA(7,12)
      INTEGER I,J,NSPEC
      CHARACTER*18 TARMAT(19)
      CHARACTER*6 PLAMAT(7)
c
      NSPEC=7
      NTARS=12
c
c  NSPEC = NUMBER OF IMPURITY SPECIES IN PLASMA.
c  NTARS = NUMBER OF TARGET MATERIALS.
c   CETH = THRESHOLD ENERGY FOR TARGET-ION INTERACTION CONSIDERED (EV)
c   CETF = THOMAS-FERMI INTERACTION POTENTIAL (EV)
c     CQ = YIELD FACTOR (ATOMS/ION)
c CIDATA = LOGICAL FLAG INDICATING WHETHER DATA IS AVAILABLE (T OR F)
c
c     DATA FROM ECKSTEINS LATEST REPORT IPP 9/82 HAS BEEN USED.
c     THE TWO COMPOUNDS (TITANIUM CARBIDE AND SILICON CARBIDE)
c     IN THE ORIGINAL REFERENCE ARE NOT AVAILABLE IN THE LATEST
c     REPORT AND HAVE BEEN REPLACED WITH LITHIUM AND CHROMIUM.
c     NOTE ALSO THAT ECKSTEIN HAS CHANGED THE DEFINITION OF HIS
c     NUCLEAR STOPPING CROSS SECTION.  HE HAS ALSO RECOMMENDED
c     THAT WE USE FITS TO EXPERIMENTAL DATA, WHERE AVAILABLE, IN
c     PREFERENCE TO THE CALCULATIONS BASED ON EMPIRICAL FORMULAE
c     (PP 335-338, WHICH ARE AVAILABLE FOR A LARGE RANGE OF
c     PROJECTILE-TARGET COMBINATIONS).  FOR THE TIME BEING I HAVE
c     REPLACED THE GENERAL TABLES WITH FITS TO EXPERIMENTAL DATA
c     ONLY FOR H, D, AND HE ON BE.  THIS RESULTS IN HIGHER YIELDS
c     (APPROX 2X).
c                       LORNE HORTON MAY 93
c

      DATA TARMAT/ ' ALUMINIUM       ',' BERYLLIUM       ',
     &   ' COPPER          ', ' GRAPHITE        ',' TITANIUM        ',
     &   ' IRON            ', ' NICKEL          ',' MOLYBDENUM      ',
     &   ' TUNGSTEN        ', ' BORON           ',' LITHIUM         ',
     &   ' CHROMIUM        ', ' "DEUTERIUM"     ',' "HELIUM"        ',
     &   ' "NEON"          ', ' "ARGON"         ',' "OXYGEN"        ',
     &   ' "CHLORINE"      ', ' "NITROGEN"      ' /

      DATA PLAMAT/ ' H    ',' D    ',' T    ',' HE4  ',' C    ',' SELF '
     &   ,' O    '/

      DATA ETH/ 23.87d0, 14.86d0, 12.91d0, 12.51d0, 16.32d0, 24.02d0, 
     &   18.55d0, 12.2d0 , 10.0d0 , 14.69d0, 13.9d0 , 28.08d0, 24.17d0, 
     &   32.71d0, 57.25d0, 28.90d0, 20.64d0, 17.07d0, 13.27d0, 25.17d0, 
     &   14.01d0, 31.00d0, 27.00d0, 29.00d0, 32.15d0, 52.98d0, 52.98d0, 
     &   61.54d0, 59.49d0, 31.51d0, 23.71d0, 20.56d0, 19.45d0, 34.96d0, 
     &   21.23d0, 61.39d0, 31.63d0, 23.12d0, 19.54d0, 16.70d0, 31.03d0, 
     &   17.95d0, 66.80d0, 34.12d0, 24.69d0, 20.67d0, 17.00d0, 31.89d0, 
     &   18.14d0, 172.36d0, 83.30d0, 56.47d0, 44.28d0, 25.75d0, 48.83d0, 
     &   25.47d0, 447.02d0,209.37d0,136.26d0,102.07d0, 41.20d0, 62.06d0, 
     &   35.92d0, 23.14d0, 21.56d0, 23.46d0, 25.83d0, 43.25d0, 40.97d0, 
     &   50.30d0, 6.22d0, 6.92d0, 8.03d0, 9.10d0, 15.94d0, 11.94d0, 
     &   18.61d0, 54.47d0, 28.39d0, 21.01d0, 17.96d0, 16.07d0, 29.46d0, 
     &   17.40d0/
c
      DATA ETF/ 1059.d0, 1097.d0, 1135.d0, 2448.d0, 10297.d0, 34550.d0, 
     &   15720.d0, 256.d0, 282.d0, 308.d0, 720.d0, 4153.d0, 2208.d0, 
     &   6971.d0, 2926.d0, 2972.d0, 3017.d0, 6293.d0, 22701.d0, 
     &   224652.d0, 32727.d0, 415.d0, 447.d0, 479.d0, 1087.d0, 5688.d0, 
     &   5688.d0, 9298.d0, 2054.d0, 2097.d0, 2139.d0, 4503.d0, 16949.d0, 
     &   117915.d0, 24846.d0, 2544.d0, 2590.d0, 2635.d0, 5517.d0, 
     &   20270.d0, 174122.d0, 29437.d0, 2799.d0, 2846.d0, 2893.d0, 
     &   6045.d0, 22014.d0, 206991.d0, 31860.d0, 4719.d0, 4768.d0, 
     &   4817.d0, 9945.d0, 34188.d0, 533127.d0, 48329.d0, 9871.d0, 
     &   9925.d0, 9978.d0, 20376.d0, 66517.d0,1998893.d0, 91993.d0, 
     &   333.d0, 361.d0, 389.d0, 894.d0, 4856.d0, 3717.d0, 8021.d0, 
     &   185.d0, 209.d0, 232.d0, 557.d0, 3506.d0, 1129.d0, 6014.d0, 
     &   2296.d0, 2340.d0, 2383.d0, 5002.d0, 18577.d0, 144458.d0, 
     &   27091.d0/
c
      DATA Q/ 0.08d0, 0.14d0, 0.19d0, 0.37d0, 1.65d0, 4.21d0, 2.36d0, 
     &   0.128d0, 0.220d0, 0.14d0, 0.707d0, 1.00d0, 0.67d0, 1.35d0, 
     &   0.08d0, 0.14d0, 0.19d0, 0.38d0, 1.83d0, 14.23d0, 2.73d0, 
     &   0.035d0, 0.10d0, 0.12d0, 0.20d0, 0.75d0, 0.75d0, 1.02d0, 0.06d0
     &   , 0.11d0, 0.15d0, 0.30d0, 1.41d0, 7.44d0, 2.07d0, 0.07d0, 
     &   0.12d0, 0.16d0, 0.33d0, 1.59d0, 10.44d0, 2.36d0, 0.07d0, 0.12d0
     &   , 0.16d0, 0.33d0, 1.60d0, 11.51d0, 2.38d0, 0.05d0, 0.09d0, 
     &   0.12d0, 0.24d0, 1.20d0, 16.27d0, 1.81d0, 0.04d0, 0.07d0, 0.10d0
     &   , 0.20d0, 1.02d0, 33.47d0, 1.55d0, 0.05d0, 0.08d0, 0.11d0, 
     &   0.21d0, 0.80d0, 0.67d0, 1.08d0, 0.10d0, 0.16d0, 0.21d0, 0.40d0, 
     &   1.37d0, 0.69d0, 1.82d0, 0.07d0, 0.12d0, 0.17d0, 0.34d0, 1.61d0, 
     &   9.54d0, 2.38d0/
c
      DATA IDATA/ 7*.true., 7*.true., 7*.true., 7*.true., 7*.true., 7*
     &   .true., 7*.true., 7*.true., 7*.true., 7*.true., 7*.true., 7*
     &   .true./
c
c  TABLE OF BINDING ENERGIES TO BE USED AS DEFAULT WHEN ZERO IS
c  SPECIFIED IN THE INPUT FILE.  FOR THE GASEOUS IMPURITIES I HAVE
c  SET EBD = 0
c
      DATA EBD/3.36d0,3.38d0,3.52d0,7.42d0,4.89d0,4.34d0, 4.46d0,6.83d0,
     &   8.68d0,5.73d0,1.67d0,4.12d0/
c
c-----------------------------------------------------------------------
c INITIALISE COMMON BLOCK CYIELD.
c-----------------------------------------------------------------------
c
      DO 10 I=1,NTARS
      DO 20 J=1,NSPEC
      CETH(J,I) = ETH(J,I)
      CETF(J,I) = ETF(J,I)
      CQ(J,I) = Q(J,I)
      CIDATA(J,I) = IDATA(J,I)
   20 CONTINUE
   10 CONTINUE
c
c-----------------------------------------------------------------------
c  ASSIGN TARGET AND BACKGROUND ION MATERIALS.
c  MATERIALS 13-18 ARE SPECIAL "GAS" TARGET CASES, WHERE THE YIELD IS
c  ALWAYS 1.0
c-----------------------------------------------------------------------
c
      MATT = 4
      IF (CION.EQ.13) MATT = 1
      IF (CION.EQ.4) MATT = 2
      IF (CION.EQ.29) MATT = 3
      IF (CION.EQ.6) MATT = 4
      IF (CION.EQ.22) MATT = 5
      IF (CION.EQ.26) MATT = 6
      IF (CION.EQ.28) MATT = 7
      IF (CION.EQ.42) MATT = 8
      IF (CION.EQ.74) MATT = 9
      IF (CION.EQ.5) MATT = 10
      IF (CION.EQ.3) MATT = 11
      IF (CION.EQ.24) MATT = 12
      IF (CION.EQ.1) MATT = 13
      IF (CION.EQ.2) MATT = 14
      IF (CION.EQ.10) MATT = 15
      IF (CION.EQ.18) MATT = 16
      IF (CION.EQ.8) MATT = 17
      IF (CION.EQ.17) MATT = 18
      IF (CION.EQ.7) MATT = 19
c
c---- TARGET BINDING ENERGY FROM INTERNAL DATA IF EXTERNAL INPUT ZERO
c
ctdr      IF (CEBD.EQ.0.0 .AND. MATT.LE.12) CEBD = EBD(MATT)
c
c---- PLASMA MATERIAL.  CAN BE SET EXPLICITLY FROM INPUT DATA
c
      MATP = 6
      IF (NINT(CRMB).LE.4) MATP = NINT (CRMB)
      IF (CIZB.EQ.6) MATP = 5
      IF (CIZB.EQ.8) MATP = 7
cdtr      IF (CNEUTD.EQ.1) MATP = CBOMBF
      WRITE (*,*) 'TARGET MATERIAL IS     ' , TARMAT(MATT)
      WRITE (*,*) 'BOMBARDING IONS ARE    ' , PLAMAT(MATP)
cdtr      IF (CNEUTD.EQ.1) CALL PRI ('         WITH ZIMP', CBOMBZ)
      RETURN
      END
c
c
c
c ------------------------------------------------------------------------c
      doubleprecision FUNCTION YLD96(MATP,MATT,ENERGY)
      IMPLICIT none
      doubleprecision ENERGY,X1,X12,X2
      INTEGER MATP,MATT
c
c  *********************************************************************
c  *                                                                   *
c  *  YLD96:   CALCULATES YIELD OF MATERIAL "MATP" HITTING TARGET      *
c  *  MADE OF MATERIAL "MATT" WITH AN ENERGY "ENERGY".                 *
c  *                                                                   *
c  *  ARGUMENTS :-                                                     *
c  *  MATP : CODE INTEGER GIVING MATERIAL OF IMPACTING PARTICLE        *
c  *  MATT : CODE INTEGER GIVING MATERIAL USED IN TARGET               *
c  *  ENERGY : ENERGY OF IMPACTING PARTICLE                            *
c  *                                                                   *
c  *********************************************************************
c
c     INCLUDE "CYIELD"
cdtr      include    'cyield'
c Group Cyield
      double precision ceth(7,12), cetf(7,12), cq(7,12), redf_haas
      integer ntars
      logical cidata(7,12)
      common /api170/ ntars
      common /api171/ cidata
      common /api173/ ceth, cetf, cq, redf_haas
c End of Cyield
c ceth,cetf,cq,ntars,cidata

c
      IF (MATT.EQ.13.OR.MATT.EQ.14.OR.MATT.EQ.15 .OR.MATT.EQ.16.OR.MATT
     &   .EQ.17.OR.MATT.EQ.18 .or.matt.eq.19) THEN
      YLD96 = 1.0d0
      RETURN
      ENDIF
c
      IF(ENERGY.LE.0.0d0) GOTO 100
      IF(CIDATA(MATP,MATT)) THEN
      IF((CETH(MATP,MATT)/ENERGY).GT.1.0d0) GOTO 100
      X1=ENERGY/CETF(MATP,MATT)
      X12=SQRT(X1)
      X2=CETH(MATP,MATT)/ENERGY
      YLD96=CQ(MATP,MATT)*(0.5d0*LOG(1.0d0+1.2288d0*X1)) /(X1+0.1728d0*
     &   X12+0.008d0*X1**0.1504d0) *(1-X2)*(1-X2)*(1.0d0-X2**(2.0d0/
     &   3.0d0))
      ELSE
      YLD96=0.0d0
      ENDIF
      RETURN
c  ERROR TRAPPING, OUTSIDE RANGE SET YIELD=0,   E=0 OR E/E0 > 1
  100 YLD96=0.0d0
      END
c
c ------------------------------------------------------------------------c
      SUBROUTINE SPUTCHEM(IOPTCHEM,E0,TEMP,FLUX,YCHEM)

      IMPLICIT NONE
      INTEGER IOPTCHEM
      doubleprecision E0,TEMP,FLUX,YCHEM,YGARCIA,YHAASZ,YROTH96, 
     &   YHAASZ97,YHAASZ97M,FLUX_cgs
      INTRINSIC MAX
c Group Cyield
      double precision ceth(7,12), cetf(7,12), cq(7,12), redf_haas
      integer ntars
      logical cidata(7,12)
      common /api170/ ntars
      common /api171/ cidata
      common /api173/ ceth, cetf, cq, redf_haas
c End of Cyield
credf_haas

c#########################################################################
c
c ** -Modified 2/20/98 to use flux in MKS [1/m**2 s] rather than previous
c ** -[1/cm**2 s]; TDR
c
c ** -Code obtained from David Elder, 2/6/98; originally written by
c ** -Houyang Guo at JET
c
c#########################################################################
c
c  *********************************************************************
c  *                                                                   *
c  *  CHEMICAL SPUTTERING FOR D --> C                                  *
c  *                                                                   *
c  *  IOPTCHEM       -  Options for chemical sputtering:               *
c  *         1       -  Garcia-Rosales' formula (EPS94)                *
c  *         2       -  according to Pospieszczyk (EPS95)              *
c  *         3       -  Vietzke (in Physical processes of the inter-   *
c  *                    action of Fusion Plasmas with Solids)          *
c  *         4       -  Haasz (Submitted to J.Nucl.Mater.,Dec. 1995)   *
c  *         5       -  Roth & Garcia-Rosales (Submitted to Nucl.      *
c  *                    Fusion, March 1996)                            *
c  *         6       -  Haasz 1997 (Brian Mech's PhD Thesis)           *
c  *         7       -  Haasz 1997 + reduced 1/5 from 10->5 eV (Porter)*
c  *                                                                   *
c  *  E0   (eV)      -  Ion or neutral incident energy                 *
c  *  TEMP (K)       -  Temperature at target or wall                  *
c  *  FLUX (m-2s-1)  -  Ion or neutral flux  (changed to MKS 2/20/98)  *
c  *  YCHEM          -  Chemical Sputtering yield                      *
c  *                                                                   *
c  *********************************************************************
c
c
c      Change the flux from MKS to cgs units to use old cgs routines
c      conversion done on 2/20/98
      FLUX_cgs = 1d4*FLUX

      IF (IOPTCHEM.EQ.1) THEN
      YCHEM = YGARCIA(E0,TEMP,FLUX_cgs)
      ELSE IF (IOPTCHEM.EQ.2) THEN
      YCHEM = 0.04254d0*(MAX(5d18,FLUX_cgs)/5d18)**(-0.477d0)
      ELSE IF (IOPTCHEM.EQ.3) THEN
      YCHEM = 0.0215d0*(MAX(1d14,FLUX_cgs)/1d16)**(-0.1d0)
      ELSE IF (IOPTCHEM.EQ.4) THEN
      YCHEM = YHAASZ(E0,TEMP)
      ELSE IF (IOPTCHEM.EQ.5) THEN
      YCHEM = YROTH96(E0,TEMP,FLUX_cgs)
      ELSE IF (IOPTCHEM.EQ.6) THEN
      YCHEM = YHAASZ97(E0,TEMP)
      ELSE IF (IOPTCHEM.EQ.7) THEN
      YCHEM = YHAASZ97M(E0,TEMP,redf_haas)
      END IF

      RETURN
      END

c -------------
c ------------------------------------------------------------------------c
      FUNCTION YROTH96(E0,TEMP,FLUX)

      IMPLICIT NONE
      doubleprecision E0,TEMP,FLUX
      doubleprecision ETHC,ETFC,QC,SNC
      doubleprecision CSURF,CSP3
      doubleprecision YPHYS,YSURF,YTHERM,YROTH96
      INTRINSIC MIN
c
c  *********************************************************************
c  *                                                                   *
c  *  CHEMICAL SPUTTERING CALCULATED BY Garcia-Rosales FORMULA        *
c  *                                                                   *
c  *  ETHC (eV)  -  Threshold energy for D -> C physical sputtering    *
c  *  ETFC (eV)  -  Thomas-Fermi energy                                *
c  *  SNC        -  Stopping power                                     *
c  *  QC         -  Fitting parameters                                 *
c  *                                                                   *
c  *  CSURF      -  Fitting parameters                                 *
c  *  CSP3       -  Carbon at surface                                  *
c  *                                                                   *
c  *  YPHYS      -  Physical sputtering yield                          *
c  *  YSURF      -  Sputtering due to SURFACE process                  *
c  *  YTHERM     -  Sputtering due to THERMAL process                  *
c  *  YROTH96    -  Total CHEMICAL sputtering yield                    *
c  *                                                                   *
c  *********************************************************************

c ---------------------------------------------------------
c Total Chemical Sputtering Yield:
c            Ychem = Ysurf+Ytherm*(1+D*Yphys)
c ---------------------------------------------------------

c
c 1> PHYSICAL SPUTTERING YIELD
c
      ETHC = 27.0d0
      ETFC = 447.0d0
      QC = 0.1d0
c
c  - Stopping Power
c
      SNC = 0.5d0*LOG(1.d0+1.2288d0*E0/ETFC)/(E0/ETFC + 0.1728d0*SQRT(E0
     &   /ETFC) + 0.008d0*(E0/ETFC)**0.1504d0)
c
c  - Physical Sputtering Yield
c
      IF (E0.GT.ETHC) THEN
      YPHYS = QC*SNC*(1-(ETHC/E0)**(2.d0/3.d0))*(1-ETHC/E0)**2
      ELSE
      YPHYS = 0.0d0
      ENDIF
c
c 2> YSURF: Surface Process
c
      CSURF = 1/(1.d0+1d13*EXP(-2.45d0*11604/TEMP))
      CSP3 = CSURF*(2d-32*FLUX+EXP(-1.7d0*11604/TEMP)) /(2d-32*FLUX+(1
     &   +2d29/FLUX*EXP(-1.8d0*11604/TEMP)) *EXP(-1.7d0*11604/TEMP))

      IF (E0.GT.1.d0) THEN
      YSURF = CSP3*QC*SNC*(1-(1.d0/E0)**(2.d0/3.d0))*(1-1.d0/E0)**2 /(
     &   1.d0+EXP((MIN(90.0d0,E0)-90.d0)/50.d0))
      ELSE
      YSURF = 0.0d0
      ENDIF
c
c 3> YTHERM: Thermak Activated Process
c
      YTHERM = CSP3*0.033d0*EXP(-1.7d0*11604/TEMP) /(2d-32*FLUX+EXP(
     &   -1.7d0*11604/TEMP))
c
c 4> YCHEM: Total Chemical Sputtering Yield
c
      YROTH96 = YSURF + YTHERM * (1 + 125 * YPHYS)

cW    WRITE(6,*) 'YROTH96 = ',YROTH96

      RETURN
      END


c -------------
c ------------------------------------------------------------------------c
      FUNCTION YGARCIA(E0,TEMP,FLUX)

      IMPLICIT NONE
      doubleprecision E0,TEMP,FLUX
      doubleprecision ETHC,ETFC,QC,SNC
      doubleprecision YPHYS,YCHEM_TH,YCHEM_ATH,YGARCIA
c
c  *********************************************************************
c  *                                                                   *
c  *  CHEMICAL SPUTTERING CALCULATED BY Garcia-Rosales FORMULA        *
c  *                                                                   *
c  *  ETHC (eV)  -  Threshold energy for D -> C physical sputtering    *
c  *  ETFC (eV)  -  Thomas-Fermi energy                                *
c  *  SNC        -  Stopping power                                     *
c  *  QC         -  Fitting parameters                                 *
c  *                                                                   *
c  *  YPHYS      -  Physical sputtering yield                          *
c  *  YCHEM_TH   -  Thermal activated mechanism                        *
c  *  YCHEM_ATH  -  Athermal mechanism                                 *
c  *                                                                   *
c  *********************************************************************
c

      ETHC = 27.0d0
      ETFC = 447.0d0
      QC = 0.1d0
c
c Check for impact energies below threshold
c
      IF (E0.GT.ETHC) THEN
c
c Stopping Power
c
      SNC = 0.5d0*LOG(1.d0+1.2288d0*E0/ETFC)/(E0/ETFC + 0.1728d0*SQRT(E0
     &   /ETFC) + 0.008d0*(E0/ETFC)**0.1504d0)
c
c Physical Sputtering Yield
c
      YPHYS = QC*SNC*(1-(ETHC/E0)**(2.d0/3.d0))*(1-ETHC/E0)**2
c
      ELSE
      YPHYS = 0.0d0
      ENDIF
c
c Chemical Sputtering Yield
c
      YCHEM_TH = 6d19*EXP(-1.d0*11604/TEMP) /(1d15+3d27*EXP(-2.d0*11604/
     &   TEMP)) * (2.d0+200*YPHYS)*(MAX(1d16,FLUX)/1d16)**(-0.1d0)

      YCHEM_ATH = 0.05d0*EXP(E0*1d-3*(20.d0-1*11604.d0/TEMP)) / ((1.d0+
     &   EXP((E0-150.d0)/25.d0))*(1.d0+EXP((TEMP-740.d0)/25.d0)))

      YGARCIA = YCHEM_TH + YCHEM_ATH

cW    WRITE(6,*) 'YTH = ',YCHEM_TH,'YATH = ',YCHEM_ATH

      RETURN
      END


c -------------
c ------------------------------------------------------------------------c

      FUNCTION YHAASZ(E0,TEMP)
c
c  *********************************************************************
c  *                                                                   *
c  *  CHEMICAL SPUTTERING FROM Haasz NEW DATA (Dec. 1995)            *
c  *  - poly. fit: Y = a0 + a1*log(E) + a2*log(E)^2 + a3*log(E)^3      *
c  *                                                                   *
c  *********************************************************************
c
      IMPLICIT NONE

      doubleprecision E0,TEMP
      doubleprecision FITC300(4),FITC350(4),FITC400(4),FITC450(4),
     &   FITC500(4), FITC550(4),FITC600(4),FITC650(4),FITC700(4),FITC750
     &   (4), FITC800(4),FITC850(4),FITC900(4),FITC950(4),FITC1000(4), 
     &   FITC1050(4),FITC1100(4)
      doubleprecision POLY_C(4),YFIT,FITE0
      doubleprecision YHAASZ
      INTEGER I
c
c     Poly. fit c. /       a0,      a1,      a2,      a3
c
      DATA FITC300 / -0.01789d0, 0.02309d0, 0.00089d0,-0.00315d0/
      DATA FITC350 / -0.01691d0, 0.02020d0, 0.00451d0,-0.00407d0/
      DATA FITC400 / -0.01128d0, 0.01230d0, 0.00922d0,-0.00483d0/
      DATA FITC450 / -0.00401d0, 0.00453d0, 0.01226d0,-0.00493d0/
      DATA FITC500 / -0.01000d0, 0.02097d0,-0.00032d0,-0.00153d0/
      DATA FITC550 / -0.02022d0, 0.04019d0,-0.01430d0, 0.00253d0/
      DATA FITC600 / 0.00047d0,-0.00319d0, 0.00950d0,-0.00025d0/
      DATA FITC650 / 0.02921d0,-0.05657d0, 0.03467d0,-0.00226d0/
      DATA FITC700 / 0.00561d0,-0.00081d0,-0.01044d0, 0.00939d0/
      DATA FITC750 / 0.00225d0, 0.00205d0,-0.00949d0, 0.00800d0/
      DATA FITC800 / 0.00900d0,-0.02109d0, 0.01366d0, 0.00048d0/
      DATA FITC850 / 0.00483d0,-0.01691d0, 0.01513d0,-0.00152d0/
      DATA FITC900 / 0.00569d0,-0.02211d0, 0.02185d0,-0.00427d0/
      DATA FITC950 / 0.00317d0,-0.01827d0, 0.02081d0,-0.00482d0/
      DATA FITC1000/ 0.00436d0,-0.02075d0, 0.02290d0,-0.00574d0/
      DATA FITC1050/ 0.00463d0,-0.02082d0, 0.02285d0,-0.00601d0/
      DATA FITC1100/ 0.00920d0,-0.02942d0, 0.02802d0,-0.00723d0/
c
c Find right polynomial fit coefficients for a given temperature
c
      IF (TEMP.LE.300.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC300(I)
      ENDDO
      ELSE IF (TEMP.GT.300.0d0 .AND. TEMP.LE.350.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC350(I)
      ENDDO
      ELSE IF (TEMP.GT.350.0d0 .AND. TEMP.LE.400.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC400(I)
      ENDDO
      ELSE IF (TEMP.GT.400.0d0 .AND. TEMP.LE.450.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC450(I)
      ENDDO
      ELSE IF (TEMP.GT.450.0d0 .AND. TEMP.LE.500.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC500(I)
      ENDDO
      ELSE IF (TEMP.GT.500.0d0 .AND. TEMP.LE.550.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC550(I)
      ENDDO
      ELSE IF (TEMP.GT.550.0d0 .AND. TEMP.LE.600.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC600(I)
      ENDDO
      ELSE IF (TEMP.GT.600.0d0 .AND. TEMP.LE.650.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC650(I)
      ENDDO
      ELSE IF (TEMP.GT.650.0d0 .AND. TEMP.LE.700.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC700(I)
      ENDDO
      ELSE IF (TEMP.GT.700.0d0 .AND. TEMP.LE.750.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC750(I)
      ENDDO
      ELSE IF (TEMP.GT.750.0d0 .AND. TEMP.LE.800.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC800(I)
      ENDDO
      ELSE IF (TEMP.GT.800.0d0 .AND. TEMP.LE.850.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC850(I)
      ENDDO
      ELSE IF (TEMP.GT.850.0d0 .AND. TEMP.LE.900.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC900(I)
      ENDDO
      ELSE IF (TEMP.GT.900.0d0 .AND. TEMP.LE.950.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC950(I)
      ENDDO
      ELSE IF (TEMP.GT.950.0d0 .AND. TEMP.LE.1000.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC1000(I)
      ENDDO
      ELSE IF (TEMP.GT.1000.0d0 .AND. TEMP.LE.1050.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC1050(I)
      ENDDO
      ELSE
      DO I = 1,4
      POLY_C(I) = FITC1100(I)
      ENDDO
      ENDIF
c
c Calculate chemical yield according to the 3th poly. fit
c
      IF (E0.LT.10.0d0) THEN
      FITE0 = 10.d0
      ELSE IF (E0.GT.200.0d0) THEN
      FITE0 = 200.d0
      ELSE
      FITE0 = E0
      ENDIF
c
      YFIT = 0.0d0
      DO I = 1,4
      YFIT = YFIT + POLY_C(I)*log10(FITE0)**(I-1)
      ENDDO

      YHAASZ = YFIT

cW    WRITE(6,*) 'YHAASZ = ',YHAASZ

      RETURN
      END
c
c
c
c -------------
c ------------------------------------------------------------------------c

      FUNCTION YHAASZ97(E0,TEMP)
c
c  *********************************************************************
c  *                                                                   *
c  *  CHEMICAL SPUTTERING FROM Haasz NEW DATA (February 1997)        *
c  *  - poly. fit: Y = a0 + a1*log(E) + a2*log(E)^2 + a3*log(E)^3      *
c  *                                                                   *
c  *********************************************************************
c
      IMPLICIT NONE

      doubleprecision E0,TEMP
      doubleprecision FITC300(4),FITC350(4),FITC400(4),FITC450(4),
     &   FITC500(4), FITC550(4),FITC600(4),FITC650(4),FITC700(4),FITC750
     &   (4), FITC800(4),FITC850(4),FITC900(4),FITC950(4),FITC1000(4)
      doubleprecision POLY_C(4),YFIT,FITE0
      doubleprecision YHAASZ97
      INTEGER I
c
c     Poly. fit c. /       a0,      a1,      a2,      a3
c
      DATA FITC300 / -0.03882d0, 0.07432d0,-0.03470d0, 0.00486d0/
      DATA FITC350 / -0.05185d0, 0.10126d0,-0.05065d0, 0.00797d0/
      DATA FITC400 / -0.06089d0, 0.12186d0,-0.06240d0, 0.01017d0/
      DATA FITC450 / -0.08065d0, 0.16884d0,-0.09224d0, 0.01625d0/
      DATA FITC500 / -0.08872d0, 0.19424d0,-0.10858d0, 0.01988d0/
      DATA FITC550 / -0.08728d0, 0.20002d0,-0.11420d0, 0.02230d0/
      DATA FITC600 / -0.05106d0, 0.13146d0,-0.07514d0, 0.01706d0/
      DATA FITC650 / 0.07373d0,-0.13263d0, 0.09571d0,-0.01672d0/
      DATA FITC700 / 0.02722d0,-0.03599d0, 0.02064d0, 0.00282d0/
      DATA FITC750 / 0.09052d0,-0.18253d0, 0.12362d0,-0.02109d0/
      DATA FITC800 / 0.02604d0,-0.05480d0, 0.04025d0,-0.00484d0/
      DATA FITC850 / 0.03478d0,-0.08537d0, 0.06883d0,-0.01404d0/
      DATA FITC900 / 0.02173d0,-0.06399d0, 0.05862d0,-0.01380d0/
      DATA FITC950 / -0.00086d0,-0.01858d0, 0.02897d0,-0.00829d0/
      DATA FITC1000/ -0.01551d0, 0.01359d0, 0.00600d0,-0.00353d0/
c
c Find right polynomial fit coefficients for a given temperature
c
      IF (TEMP.LE.300.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC300(I)
      ENDDO
      ELSE IF (TEMP.GT.300.0d0 .AND. TEMP.LE.350.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC350(I)
      ENDDO
      ELSE IF (TEMP.GT.350.0d0 .AND. TEMP.LE.400.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC400(I)
      ENDDO
      ELSE IF (TEMP.GT.400.0d0 .AND. TEMP.LE.450.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC450(I)
      ENDDO
      ELSE IF (TEMP.GT.450.0d0 .AND. TEMP.LE.500.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC500(I)
      ENDDO
      ELSE IF (TEMP.GT.500.0d0 .AND. TEMP.LE.550.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC550(I)
      ENDDO
      ELSE IF (TEMP.GT.550.0d0 .AND. TEMP.LE.600.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC600(I)
      ENDDO
      ELSE IF (TEMP.GT.600.0d0 .AND. TEMP.LE.650.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC650(I)
      ENDDO
      ELSE IF (TEMP.GT.650.0d0 .AND. TEMP.LE.700.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC700(I)
      ENDDO
      ELSE IF (TEMP.GT.700.0d0 .AND. TEMP.LE.750.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC750(I)
      ENDDO
      ELSE IF (TEMP.GT.750.0d0 .AND. TEMP.LE.800.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC800(I)
      ENDDO
      ELSE IF (TEMP.GT.800.0d0 .AND. TEMP.LE.850.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC850(I)
      ENDDO
      ELSE IF (TEMP.GT.850.0d0 .AND. TEMP.LE.900.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC900(I)
      ENDDO
      ELSE IF (TEMP.GT.900.0d0 .AND. TEMP.LE.950.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC950(I)
      ENDDO
      ELSE IF (TEMP.GT.950.0d0) THEN
      DO I = 1,4
      POLY_C(I) = FITC1000(I)
      ENDDO
      ENDIF
c
c Calculate chemical yield according to the 3th poly. fit
c
      IF (E0.LT.10.0d0) THEN
      FITE0 = 10.d0
      ELSE IF (E0.GT.200.0d0) THEN
      FITE0 = 200.d0
      ELSE
      FITE0 = E0
      ENDIF
c
      YFIT = 0.0d0
      DO I = 1,4
      YFIT = YFIT + POLY_C(I)*log10(FITE0)**(I-1)
      ENDDO

      YHAASZ97 = YFIT

cW    WRITE(6,*) 'YHAASZ97 = ',YHAASZ97

      RETURN
      END
c
c
c
c -------------
c ------------------------------------------------------------------------c

      FUNCTION YHAASZ97M(E0,TEMP,reducf)
c
c  *********************************************************************
c  *                                                                   *
c  *  CHEMICAL SPUTTERING FROM Haasz NEW DATA (February 1997)        *
c  *  - poly. fit: Y = a0 + a1*log(E) + a2*log(E)^2 + a3*log(E)^3      *
c  *  with the addition of a new fit below 10 eV as suggested by       *
c  *  J.Davis and parameterized by G. Porter; now interpolates between *
c  *  5 and 10 eV to lower value (YDAVIS98), and is fixed below 5 eV.  *
c  *  Default value for reducf=0.2; change redf_haas                   *
c  *                                                                   *
c  *********************************************************************
c
      IMPLICIT NONE

      doubleprecision E0, TEMP, reducf
      doubleprecision YHAASZ97M, YDAVIS98, YHAASZ97
      doubleprecision m1,m2,m3,FRAC

      DATA m1/602.39d0/, m2/202.24d0/, m3/43.561d0/

      IF (E0 .GE. 10) THEN
      YHAASZ97M = YHAASZ97(E0,TEMP)
      ELSEIF (E0 .LT. 10.d0 .AND. E0 .GE. 5.d0) THEN
      FRAC = (E0-5.d0)/5.d0
      YDAVIS98 = reducf/(m2*((TEMP/m1)**2 - 1)**2 + m3)
      YHAASZ97M = FRAC*YHAASZ97(E0,TEMP)+ (1.d0-FRAC)*YDAVIS98
      ELSEIF (E0 .LT. 5.d0) THEN
      YDAVIS98 = reducf/(m2*((TEMP/m1)**2 - 1)**2 + m3)
      YHAASZ97M = YDAVIS98
      ENDIF

      RETURN
      END
