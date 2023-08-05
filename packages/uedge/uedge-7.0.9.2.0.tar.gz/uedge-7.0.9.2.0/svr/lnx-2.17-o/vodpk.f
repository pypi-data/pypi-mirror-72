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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/svr.d
c     ./../vodpk.m
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
      SUBROUTINE VODPK (F, NEQ, Y, T, TOUT, ITOL, RTOL, ATOL, ITASK, 
     &   ISTATE, IOPT, RWORK, LRW, IWORK, LIW, JAC, PSOL, MF, RPAR, IPAR
     &   , scalpk, efacnin)
      EXTERNAL F, JAC, PSOL
      doubleprecision Y, T, TOUT, RTOL, ATOL, RWORK, RPAR, scalpk, 
     &   efacnin
      INTEGER NEQ, ITOL, ITASK, ISTATE, IOPT, LRW, IWORK, LIW, MF, IPAR
      DIMENSION Y(*), RTOL(*), ATOL(*), RWORK(LRW), IWORK(LIW), RPAR(*), 
     &   IPAR(*)
c-----------------------------------------------------------------------
c This is the 30 November 1993 version of
c VODPK.. variable-coefficient ordinary differential equation solver
c         with the preconditioned Krylov method GMRES for the solution
c         of linear systems.
c
c Modified for use in LEDGE and UEDGE by T. Rognlien et al.
c
c Modified by A. C. Hindmarsh: added failure flag in F routine.
c
c This version is in single precision.
c
c VODPK solves the initial value problem for stiff or nonstiff
c systems of first order ode-s,
c     dy/dt = f(t,y) ,  or, in component form,
c     dy(i)/dt = f(i) = f(i,t,y(1),y(2),...,y(neq)) (i = 1,...,neq).
c VODPK is a package based on the VODE and LSODPK packages, and on
c the October 23, 1978 version of the ODEPACK user interface
c standard, with minor modifications.
c-----------------------------------------------------------------------
c Note to LLNL Cray users..
c For maximum efficiency, appropriate compiler optimization directives
c have been inserted for Cray compilers (but not CIVIC).
c-----------------------------------------------------------------------
c References..
c 1. P. N. Brown, G. D. Byrne, and A. C. Hindmarsh, "VODE, A Variable-
c    Coefficient ODE Solver," SIAM J. Sci. Stat. Comput., 10  (1989),
c    pp., 1038-1051.  Also LLNL report UCRL-98412, June 1988.
c 2. P. N. Brown and A. C. Hindmarsh, "Reduced Storage Matrix Methods
c    in Stiff ODE Systems," J. Appl. Math. & Comp., 31 (1989), pp.40-91.
c    Also LLNL report UCRL-95088, Rev. 1, June 1987.
c 3. G. D. Byrne, "Pragmatic Experiments with Krylov Methods in the
c    Stiff ODE Setting," Numerical ODEs, J. Cash and I. Duff, eds.,
c    Oxford Univ. Press, London, to appear.
c-----------------------------------------------------------------------
c Authors..
c               George D. Byrne
c               Technical Computing Division
c               Exxon Research and Engineering Co.
c               P. O. Box 998
c               Annandale, NJ 08801-0998
c and
c               Alan C. Hindmarsh and Peter N. Brown
c               Computing and Mathematics Research Division, L-316
c               Lawrence Livermore National Laboratory
c               Livermore, CA 94550
c-----------------------------------------------------------------------
c Introduction.
c
c This is a modification of the VODE package which incorporates
c the preconditioned Krylov subspace iterative method SPIGMR for the
c linear algebraic systems that arise in the case of stiff systems.
c SPIGMR denotes a scaled preconditioned incomplete version of the
c GMRES (Generalized Minimum Residual) method.
c
c The linear systems that are solved have the form
c   A * x  = b ,  where  A = I - hrl1 * (df/dy) .
c here hrl1 is a scalar, I is the identity matrix, and df/dy is the
c Jacobian matrix of partial derivatives of f with respect to y
c (an NEQ by NEQ matrix).
c
c The particular Krylov method is chosen by setting the second digit,
c MITER, in the method flag MF.
c Currently, the values of MITER have the following meanings..
c
c          1 means SPIGMR, a scaled, preconditioned, incomplete version
c            of GMRES, a generalized minimum residual method.
c            This is the best choice in general.
c
c          9 means that only a user-supplied matrix P (approximating A)
c            will be used, with no Krylov iteration done internally to
c            VODPK.  This option allows the user to provide the complete
c            linear system solution algorithm, if desired.
c
c The user can apply preconditioning to the linear system A*x = b,
c by means of arbitrary matrices (the preconditioners).
c
c     In the case of SPIGMR, one can apply left and right
c preconditioners P1 and P2, and the basic iterative method is then
c applied to the matrix (P1-inverse)*A*(P2-inverse) instead of to the
c matrix A.  The product P1*P2 should be an approximation to A
c such that linear systems with P1 or P2 are easier to solve than with
c A alone.  Preconditioning from the left only or right only means using
c P2 = I  or  P1 = I, respectively.
c
c     If the Jacobian  J = df/dy  splits in a natural way into a sum
c J = J1 + J2, then one possible choice of preconditioners is
c            P1 = I - hrl1 * J1  and  P2 = I - hrl1 * J2
c provided each of these is easy to solve (or to approximately solve).
c
c NOTE:  To achieve an efficient solution, the preconditioned Krylov
c methods in VODPK generally require a thoughtful choice of
c preconditioners.  If the ODE system produces linear systems that are
c not amenable to solution by such iterative methods, the cost can be
c higher than with a solver that uses sparse direct methods.  However,
c for many systems, careful use of VODPK can be highly effective.
c
c See Ref. 2 for more details on the methods and applications.
c-----------------------------------------------------------------------
c Summary of usage.
c
c Communication between the user and the VODPK package, for normal
c situations, is summarized here.  This summary describes only a subset
c of the full set of options available.  See full description (below)
c for details, including optional communication, nonstandard options,
c and instructions for special situations.  See also the example
c program embedded in the comments below.
c
c A. First provide a subroutine of the form..
c     SUBROUTINE F (NEQ, T, Y, YDOT, RPAR, IPAR, IFAIL)
c     DIMENSION Y(NEQ), YDOT(NEQ), RPAR(*), IPAR(*)
c which supplies the vector function f by loading YDOT(i) with f(i).
c It should set IFAIL .ne. 0 if unable to evaluate this function.
c
c B. Next determine (or guess) whether or not the problem is stiff.
c Stiffness occurs when the Jacobian matrix df/dy has an eigenvalue
c whose real part is negative and large in magnitude, compared to the
c reciprocal of the t span of interest.  If the problem is nonstiff,
c use method flag MF = 10.  If it is stiff, MF should be 21.
c
c The following four parameters must also be set.
c  IWORK(1) = LWP  = length of real array WP for preconditioning.
c  IWORK(2) = LIWP = length of integer array IWP for preconditioning.
c  IWORK(3) = JPRE = preconditioner type flag..
c                  = 0 for no preconditioning (P1 = P2 = I)
c                  = 1 for left-only preconditioning (P2 = I)
c                  = 2 for right-only preconditioning (P1 = I)
c                  = 3 for two-sided preconditioning
c  IWORK(4) = JACFLG = flag for whether JAC is called.
c                    = 0 if JAC is not to be called,
c                    = 1 if JAC is to be called.
c  Use JACFLG = 1 if JAC computes any nonconstant data for use in
c  preconditioning, such as Jacobian elements.  See next paragraph.
c  The arrays WP and IWP are work arrays under the user-s control,
c  for use in the routines that perform preconditioning operations.
c
c C. If the problem is stiff, you must supply two routines that deal
c with the preconditioning of the linear systems to be solved.
c These are as follows..
c
c     SUBROUTINE JAC (F, NEQ, T, Y, YSV, REWT, FTY, V, HRL1, WP, IWP,
c                     IER, RPAR, IPAR)
c     DIMENSION Y(NEQ), YSV(NEQ), REWT(NEQ), FTY(NEQ), V(NEQ),
c               WP(*), IWP(*), RPAR(*), IPAR(*)
c
c        This routine is optional, and is to evaluate and preprocess
c     any parts of the Jacobian matrix df/dy involved in the
c     preconditioners P1 and P2.
c     The Y and FTY arrays contain the current values of y and f(t,y),
c     respectively, and YSV also contains the current value of y.
c     The array V is work space of length NEQ.
c     JAC must multiply all computed Jacobian elements by the scalar
c     -hrl1, add the identity matrix I, and do any factorization
c     operations called for, in preparation for solving linear systems
c     with a coefficient matrix of P1 or P2.  The matrix P1*P2
c     should be an approximation to  I - hrl1 * (df/dy), where hrl1 is a
c     scalar stored in HRL1.
c     JAC should return IER = 0 if successful, and IER .ne. 0 if not.
c     (If IER .ne. 0, a smaller time step will be tried.)
c
c     SUBROUTINE PSOL (NEQ, T, Y, FTY, WK, HRL1, WP, IWP, B, LR,
c                      IER, RPAR, IPAR)
c     DIMENSION Y(NEQ), FTY(NEQ), WK(NEQ), WP(*), IWP(*), B(NEQ),
c               RPAR(*), IPAR(*)
c
c        This routine must solve a linear system with b (stored in B)
c     as right-hand side and one of the preconditioning matrices, P1 or
c     P2, as coefficient matrix, and return the solution vector in B.
c     LR is a flag concerning left vs. right preconditioning, input
c     to PSOL.  PSOL is to use P1 if LR = 1, and P2 if LR = 2.
c
c        PSOL can use data generated in the JAC routine and stored in
c     WP and IWP.  WK is a work array of length NEQ.
c     The argument HRL1 is the current value of the scalar appearing
c     in the linear system.  If the old value, at the time of the last
c     JAC call, is needed, it must have been saved by JAC in WP.
c     on return, PSOL should set the error flag  IER as follows..
c        IER = 0 if PSOL was successful,
c        IER .gt. 0 if a recoverable error occurred, meaning that the
c              time step will be retried,
c        IER .lt. 0 if an unrecoverable error occurred, meaning that the
c              solver is to stop immediately.
c
c D. Write a main program which calls subroutine VODPK once for
c each point at which answers are desired.  This should also provide
c for possible use of logical unit 6 for output of error messages
c by VODPK.  on the first call to VODPK, supply arguments as follows..
c F      = name of subroutine for right-hand side vector f.
c          This name must be declared EXTERNAL in calling program.
c NEQ    = number of first order ODE-s.
c Y      = array of initial values, of length NEQ.
c T      = the initial value of the independent variable.
c TOUT   = first point where output is desired (.ne. T).
c ITOL   = 1 or 2 according as ATOL (below) is a scalar or array.
c RTOL   = relative tolerance parameter (scalar).
c ATOL   = absolute tolerance parameter (scalar or array).
c          The estimated local error in Y(i) will be controlled so as
c          to be roughly less (in magnitude) than
c             EWT(i) = RTOL*abs(Y(i)) + ATOL     if ITOL = 1, or
c             EWT(i) = RTOL*abs(Y(i)) + ATOL(i)  if ITOL = 2.
c          Thus the local error test passes if, in each component,
c          either the absolute error is less than ATOL (or ATOL(i)),
c          or the relative error is less than RTOL.
c          Use RTOL = 0.0 for pure absolute error control, and
c          use ATOL = 0.0 (or ATOL(i) = 0.0) for pure relative error
c          control.  Caution.. Actual (global) errors may exceed these
c          local tolerances, so choose them conservatively.
c ITASK  = 1 for normal computation of output values of Y at t = TOUT.
c ISTATE = integer flag (input and output).  Set ISTATE = 1.
c IOPT   = 0 to indicate no optional input used.
c RWORK  = real work array of length at least..
c             20 + 16*NEQ           for MF = 10,
c             61 + 17*NEQ + LWP     for MF = 21.
c LRW    = declared length of RWORK (in user-s DIMENSION statement).
c IWORK  = integer work array of length at least..
c             30            for MF = 10,
c             35 + LIWP     for MF = 21.
c LIW    = declared length of IWORK (in user-s DIMENSION statement).
c JAC,PSOL = names of subroutines for preconditioning.  These names
c            must be declared EXTERNAL in the user-s calling program.
c MF     = method flag.  Standard values are..
c          10 for nonstiff (Adams) method.
c          21 for stiff (BDF) method, with SPIGMR.
c
c RPAR, IPAR  User-specified arrays used to communicate real and integer
c             parameters (respectively) to user-supplied subroutines.
c             to user-supplied subroutines.  If RPAR is a vector, then
c             it must be dimensioned in the user's main program.  If it
c             is unused or it is a scalar, then it need not be
c             dimensioned.
c
c IPAR     User-specified array used to communicate integer parameter
c          to user-supplied subroutines.  The comments on dimensioning
c          RPAR apply to IPAR.
c
c Note that the user-s main (calling) program must declare arrays
c Y, RWORK, IWORK, and possibly ATOL, RPAR, and IPAR.
c
c E. The output from the first call (or any call) is..
c      Y = array of computed values of y(t) vector.
c      T = corresponding value of independent variable (normally TOUT).
c ISTATE = 2  if VODPK was successful, negative otherwise.
c          -1 means excess work done on this call (perhaps wrong MF).
c          -2 means excess accuracy requested (tolerances too small).
c          -3 means illegal input detected (see printed message).
c          -4 means repeated error test failures (check all input).
c          -5 means repeated convergence failures (perhaps bad JAC
c             or PSOL routine supplied or wrong choice of MF or
c             tolerances, or this solver is inappropriate).
c          -6 means error weight became zero during problem. (Solution
c             component i vanished, and ATOL or ATOL(i) = 0.)
c          -7 means an unrecoverable error occurred in JAC or PSOL.
c          -8 means f returned IFAIL .ne. 0 and VODPK was unable to
c             avoid this condition.
c
c F. To continue the integration after a successful return, simply
c reset TOUT and call VODPK again.  No other parameters need be reset.
c
c-----------------------------------------------------------------------
c Example problem.
c An ODE system is generated from the following 2-species diurnal
c kinetics advection-diffusion PDE system in 2 space dimensions:
c
c dc(i)/dt = Kh*(d/dx)**2 c(i) + V*dc(i)/dx + (d/dz)(Kv(z)*dc(i)/dz)
c                 + Ri(c1,c2,t)      for i = 1,2,   where
c   R1(c1,c2,t) = -q1*c1*c3 - q2*c1*c2 + 2*q3(t)*c3 + q4(t)*c2 ,
c   R2(c1,c2,t) =  q1*c1*c3 - q2*c1*c2 - q4(t)*c2 ,
c   Kv(z) = Kv0*exp(z/5) ,
c Kh, V, Kv0, q1, q2, and c3 are constants, and q3(t) and q4(t)
c vary diurnally.   The problem is posed on the square
c   0 .le. x .le. 20,    30 .le. z .le. 50   (all in km),
c with homogeneous Neumann boundary conditions, and for time t in
c   0 .le. t .le. 86400 sec (1 day).
c The PDE system is treated by central differences on a uniform
c 10 x 10 mesh, with simple polynomial initial profiles.
c The problem is solved with VODPK, with the BDF/GMRES method and
c the block-diagonal part of the Jacobian as a left preconditioner.
c-----------------------------------------------------------------------
c      EXTERNAL FEX, JACBD, SOLBD
c      COMMON /PCOM/ MX,MZ,MM,Q1,Q2,Q3,Q4,A3,A4,OM,C3,DZ,HDCO,VDCO,HACO
c      DIMENSION Y(2, 10, 10), RWORK(3861), IWORK(230)
c      DATA DKH/4.0E-6/, VEL/0.001E0/, DKV0/1.0E-8/, HALFDA/4.32E4/,
c     1  PI/3.1415926535898E0/, TWOHR/7200.0E0/, RTOL/1.0E-5/,
c     2  FLOOR/100.0E0/, LRW/3861/, LIW/230/, MF/21/, JPRE/1/, JACFLG/1/
c
c Load Common block of problem parameters.
c      MX = 10
c      MZ = 10
c      MM = MX*MZ
c      Q1 = 1.63E-16
c      Q2 = 4.66E-16
c      A3 = 22.62E0
c      A4 = 7.601E0
c      OM = PI/HALFDA
c      C3 = 3.7E16
c      DX = 20.0E0/(MX - 1.0E0)
c      DZ = 20.0E0/(MZ - 1.0E0)
c      HDCO = DKH/DX**2
c      HACO = VEL/(2.0E0*DX)
c      VDCO = (1.0E0/DZ**2)*DKV0
c Set other input arguments.
c      ATOL = RTOL*FLOOR
c      NEQ = 2*MX*MZ
c      IWORK(1) = 4*MX*MZ
c      IWORK(2) = NEQ
c      IWORK(3) = JPRE
c      IWORK(4) = JACFLG
c      T = 0.0E0
c      TOUT = TWOHR
c      ISTATE = 1
c Set initial profiles.
c      DO 20 JZ = 1,MZ
c        Z = 30.0E0 + (JZ - 1.0E0)*DZ
c        CZ = (0.1E0*(Z - 40.0E0))**2
c        CZ = 1.0E0 - CZ + 0.5E0*CZ**2
c        DO 10 JX = 1,MX
c          X = (JX - 1.0E0)*DX
c          CX = (0.1E0*(X - 10.0E0))**2
c          CX = 1.0E0 - CX + 0.5E0*CX**2
c          Y(1,JX,JZ) = 1.0E6*CX*CZ
c          Y(2,JX,JZ) = 1.0E12*CX*CZ
c 10       CONTINUE
c 20     CONTINUE
c
c Loop over output points, call VODPK, print sample solution values.
c      DO 70 IOUT = 1,12
c        CALL VODPK (FEX, NEQ, Y, T, TOUT, 1, RTOL, ATOL, 1, ISTATE, 0,
c     1            RWORK, LRW, IWORK, LIW, JACBD, SOLBD, MF, RPAR, IPAR)
c        WRITE(6,50) T,IWORK(11),IWORK(14),RWORK(11)
c 50     FORMAT(/' t =',E10.2,5X,'no. steps =',I5,
c     1                      '   order =',I3,'   stepsize =',E10.2)
c        WRITE(6,60) Y(1,1,1), Y(1,5,5), Y(1,10,10),
c     1              Y(2,1,1), Y(2,5,5), Y(2,10,10)
c 60     FORMAT('  c1 (bot.left/middle/top rt.) =',3E12.3/
c     1         '  c2 (bot.left/middle/top rt.) =',3E12.3)
c        IF (ISTATE .NE. 2) STOP
c        TOUT = TOUT + TWOHR
c 70     CONTINUE
c
c Print final statististics.
c      LENRW = IWORK(17)
c      LENIW = IWORK(18)
c      NST = IWORK(11)
c      NFE = IWORK(12)
c      NPE = IWORK(13)
c      NPS = IWORK(24)
c      NNI = IWORK(20)
c      NLI = IWORK(23)
c      AVDIM = FLOAT(NLI)/FLOAT(NNI)
c      NCFN = IWORK(21)
c      NCFL = IWORK(25)
c      WRITE (6,80) LENRW,LENIW,NST,NFE,NPE,NPS,NNI,NLI,AVDIM,NCFN,NCFL
c 80   FORMAT(//' final statistics..'/
c     1 ' RWORK size =',I5,5X,' IWORK size =',I4/
c     2 ' number of steps        =',I5,5X,'number of f evals.     =',I5/
c     3 ' number of prec. evals. =',I5,5X,'number of prec. solves =',I5/
c     4 ' number of nonl. iters. =',I5,5X,'number of lin. iters.  =',I5/
c     5 ' average Krylov subspace dimension (NLI/NNI)  =',F8.4/
c     6 ' number of conv. failures..  nonlinear =',I3,'  linear =',I3)
c      STOP
c      END
c
c      SUBROUTINE FEX (NEQ, T, Y, YDOT, RPAR, IPAR, IFAIL)
c      DIMENSION Y(2,*), YDOT(2,*)
c      COMMON /PCOM/ MX,MZ,MM,Q1,Q2,Q3,Q4,A3,A4,OM,C3,DZ,HDCO,VDCO,HACO
c
c Set diurnal rate coefficients.
c      S = SIN(OM*T)
c      IF (S .GT. 0.0E0) THEN
c        Q3 = EXP(-A3/S)
c        Q4 = EXP(-A4/S)
c      ELSE
c        Q3 = 0.0E0
c        Q4 = 0.0E0
c      ENDIF
c Loop over all grid points.
c      DO 20 JZ = 1,MZ
c        ZDN = 30.0E0 + (JZ - 1.5E0)*DZ
c        ZUP = ZDN + DZ
c        CZDN = VDCO*EXP(0.2E0*ZDN)
c        CZUP = VDCO*EXP(0.2E0*ZUP)
c        IBLOK0 = (JZ-1)*MX
c        IDN = -MX
c        IF (JZ .EQ. 1) IDN = MX
c        IUP = MX
c        IF (JZ .EQ. MZ) IUP = -MX
c        DO 10 JX = 1,MX
c          IBLOK = IBLOK0 + JX
c          C1 = Y(1,IBLOK)
c          C2 = Y(2,IBLOK)
c Set kinetic rate terms.
c          QQ1 = Q1*C1*C3
c          QQ2 = Q2*C1*C2
c          QQ3 = Q3*C3
c          QQ4 = Q4*C2
c          RKIN1 = -QQ1 - QQ2 + 2.0E0*QQ3 + QQ4
c          RKIN2 = QQ1 - QQ2 - QQ4
c Set vertical diffusion terms.
c          C1DN = Y(1,IBLOK+IDN)
c          C2DN = Y(2,IBLOK+IDN)
c          C1UP = Y(1,IBLOK+IUP)
c          C2UP = Y(2,IBLOK+IUP)
c          VERTD1 = CZUP*(C1UP - C1) - CZDN*(C1 - C1DN)
c          VERTD2 = CZUP*(C2UP - C2) - CZDN*(C2 - C2DN)
c Set horizontal diffusion and advection terms.
c          ILEFT = -1
c          IF (JX .EQ. 1) ILEFT = 1
c          IRIGHT = 1
c          IF (JX .EQ. MX) IRIGHT = -1
c          C1LT = Y(1,IBLOK+ILEFT)
c          C2LT = Y(2,IBLOK+ILEFT)
c          C1RT = Y(1,IBLOK+IRIGHT)
c          C2RT = Y(2,IBLOK+IRIGHT)
c          HORD1 = HDCO*(C1RT - 2.0E0*C1 + C1LT)
c          HORD2 = HDCO*(C2RT - 2.0E0*C2 + C2LT)
c          HORAD1 = HACO*(C1RT - C1LT)
c          HORAD2 = HACO*(C2RT - C2LT)
c Load all terms into YDOT.
c          YDOT(1,IBLOK) = VERTD1 + HORD1 + HORAD1 + RKIN1
c          YDOT(2,IBLOK) = VERTD2 + HORD2 + HORAD2 + RKIN2
c 10       CONTINUE
c 20     CONTINUE
c      RETURN
c      END
c
c      SUBROUTINE JACBD (F, NEQ, T, Y, YSV, REWT, F0, F1, HRL1,
c     1    BD, IPBD, IER, RPAR, IPAR)
c      EXTERNAL F
c      DIMENSION Y(2, *), YSV(*), REWT(*), F0(*), F1(*), BD(2, 2, *),
c     1          IPBD(2, *)
c      COMMON /PCOM/ MX,MZ,MM,Q1,Q2,Q3,Q4,A3,A4,OM,C3,DZ,HDCO,VDCO,HACO
c
c Compute diagonal Jacobian blocks, multiplied by -HRL1
c   (using q3 and q4 values computed on last F call).
c      DO 20 JZ = 1,MZ
c        ZDN = 30.0E0 + (JZ - 1.5E0)*DZ
c        ZUP = ZDN + DZ
c        CZDN = VDCO*EXP(0.2E0*ZDN)
c        CZUP = VDCO*EXP(0.2E0*ZUP)
c        DIAG = -(CZDN + CZUP + 2.0E0*HDCO)
c        IBLOK0 = (JZ-1)*MX
c        DO 10 JX = 1,MX
c          IBLOK = IBLOK0 + JX
c          C1 = Y(1,IBLOK)
c          C2 = Y(2,IBLOK)
c          BD(1,1,IBLOK) = -HRL1*( (-Q1*C3 - Q2*C2) + DIAG )
c          BD(1,2,IBLOK) = -HRL1*( -Q2*C1 + Q4 )
c          BD(2,1,IBLOK) = -HRL1*( Q1*C3 - Q2*C2 )
c          BD(2,2,IBLOK) = -HRL1*( (-Q2*C1 - Q4) + DIAG )
c 10       CONTINUE
c 20     CONTINUE
c Add identity matrix and do LU decompositions on blocks.
c      DO 40 IBLOK = 1,MM
c        BD(1,1,IBLOK) = BD(1,1,IBLOK) + 1.0E0
c        BD(2,2,IBLOK) = BD(2,2,IBLOK) + 1.0E0
c        CALL SGEFA (BD(1,1,IBLOK), 2, 2, IPBD(1,IBLOK), IER)
c        IF (IER .NE. 0) RETURN
c 40     CONTINUE
c      RETURN
c      END
c
c      SUBROUTINE SOLBD (NEQ, T, Y, F0, WK, HRL1, BD, IPBD, V, LR, IER,
c     1    RPAR, IPAR)
c      DIMENSION BD(2,2,*), IPBD(2,*), V(2,*)
c      COMMON /PCOM/ MX,MZ,MM,Q1,Q2,Q3,Q4,A3,A4,OM,C3,DZ,HDCO,VDCO,HACO
c Solve the block-diagonal system Px = v using LU factors stored in BD
c and pivot data in IPBD, and return the solution in V.
c      IER = 0
c      DO 10 I = 1,MM
c        CALL SGESL (BD(1,1,I), 2, 2, IPBD(1,I), V(1,I), 0)
c 10     CONTINUE
c      RETURN
c      END
c
c The output of this program, on a Cray-1 in single precision,
c is as follows:
c
c t =  7.20e+03     no. steps =  194   order =  5   stepsize =  1.17e+02
c  c1 (bot.left/middle/top rt.) =   1.047e+04   2.964e+04   1.119e+04
c  c2 (bot.left/middle/top rt.) =   2.527e+11   7.154e+11   2.700e+11
c
c t =  1.44e+04     no. steps =  227   order =  5   stepsize =  2.73e+02
c  c1 (bot.left/middle/top rt.) =   6.659e+06   5.316e+06   7.301e+06
c  c2 (bot.left/middle/top rt.) =   2.582e+11   2.057e+11   2.833e+11
c
c t =  2.16e+04     no. steps =  252   order =  5   stepsize =  4.21e+02
c  c1 (bot.left/middle/top rt.) =   2.665e+07   1.036e+07   2.931e+07
c  c2 (bot.left/middle/top rt.) =   2.993e+11   1.028e+11   3.313e+11
c
c t =  2.88e+04     no. steps =  291   order =  4   stepsize =  2.13e+02
c  c1 (bot.left/middle/top rt.) =   8.702e+06   1.292e+07   9.650e+06
c  c2 (bot.left/middle/top rt.) =   3.380e+11   5.029e+11   3.751e+11
c
c t =  3.60e+04     no. steps =  321   order =  5   stepsize =  9.90e+01
c  c1 (bot.left/middle/top rt.) =   1.404e+04   2.029e+04   1.561e+04
c  c2 (bot.left/middle/top rt.) =   3.387e+11   4.894e+11   3.765e+11
c
c t =  4.32e+04     no. steps =  374   order =  4   stepsize =  4.44e+02
c  c1 (bot.left/middle/top rt.) =  -5.457e-09  -4.365e-09  -6.182e-09
c  c2 (bot.left/middle/top rt.) =   3.382e+11   1.355e+11   3.804e+11
c
c t =  5.04e+04     no. steps =  393   order =  5   stepsize =  5.22e+02
c  c1 (bot.left/middle/top rt.) =   3.396e-12   2.798e-12   3.789e-12
c  c2 (bot.left/middle/top rt.) =   3.358e+11   4.930e+11   3.864e+11
c
c t =  5.76e+04     no. steps =  407   order =  5   stepsize =  3.54e+02
c  c1 (bot.left/middle/top rt.) =   7.738e-12   6.455e-12   8.598e-12
c  c2 (bot.left/middle/top rt.) =   3.320e+11   9.650e+11   3.909e+11
c
c t =  6.48e+04     no. steps =  419   order =  5   stepsize =  5.90e+02
c  c1 (bot.left/middle/top rt.) =  -2.018e-11  -1.680e-11  -2.243e-11
c  c2 (bot.left/middle/top rt.) =   3.313e+11   8.922e+11   3.963e+11
c
c t =  7.20e+04     no. steps =  432   order =  5   stepsize =  5.90e+02
c  c1 (bot.left/middle/top rt.) =  -2.837e-11  -2.345e-11  -3.166e-11
c  c2 (bot.left/middle/top rt.) =   3.330e+11   6.186e+11   4.039e+11
c
c t =  7.92e+04     no. steps =  444   order =  5   stepsize =  5.90e+02
c  c1 (bot.left/middle/top rt.) =  -4.861e-14  -4.433e-14  -5.162e-14
c  c2 (bot.left/middle/top rt.) =   3.334e+11   6.669e+11   4.120e+11
c
c t =  8.64e+04     no. steps =  456   order =  5   stepsize =  5.90e+02
c  c1 (bot.left/middle/top rt.) =   2.511e-15   2.071e-15   2.802e-15
c  c2 (bot.left/middle/top rt.) =   3.352e+11   9.107e+11   4.163e+11
c
c
c final statistics..
c RWORK size = 3861      IWORK size = 230
c number of steps        =  456     number of f evals.     = 1317
c number of prec. evals. =   82     number of prec. solves = 1226
c number of nonl. iters. =  571     number of lin. iters.  =  743
c average Krylov subspace dimension (NLI/NNI)  =  1.3012
c number of conv. failures..  nonlinear =  0  linear =  0
c-----------------------------------------------------------------------
c Full description of user interface to VODPK.
c
c The user interface to VODPK consists of the following parts.
c
c i.   The call sequence to subroutine VODPK, which is a driver
c      routine for the solver.  This includes descriptions of both
c      the call sequence arguments and of user-supplied routines.
c      Following these descriptions are
c        * a description of optional input available through the
c          call sequence,
c        * a description of optional output (in the work arrays), and
c        * instructions for interrupting and restarting a solution.
c
c ii.  Descriptions of other routines in the VODPK package that may be
c      (optionally) called by the user.  These provide the ability to
c      alter error message handling, save and restore the internal
c      COMMON, and obtain specified derivatives of the solution y(t).
c
c iii. Descriptions of COMMON blocks to be declared in overlay
c      or similar environments.
c
c iv.  Description of two routines in the VODPK package, either of
c      which the user may replace with the user-s own version, if
c      desired.  These relate to the measurement of errors.
c
c-----------------------------------------------------------------------
c Part i.  Call Sequence.
c
c The call sequence parameters used for input only are
c     F, NEQ, TOUT, ITOL, RTOL, ATOL, ITASK, IOPT, LRW, LIW,
c     JAC, PSOL, MF,
c and those used for both input and output are
c     Y, T, ISTATE.
c The work arrays RWORK and IWORK are also used for conditional and
c optional input and optional output.  (The term output here refers
c to the return from subroutine VODPK to the user's calling program.)
c
c The legality of input parameters will be thoroughly checked on the
c initial call for the problem, but not checked thereafter unless a
c change in input parameters is flagged by ISTATE = 3 in the input.
c
c The descriptions of the call arguments are as follows.
c
c F      = The name of the user-supplied subroutine defining the
c          ODE system.  The system must be put in the first-order
c          form dy/dt = f(t,y), where f is a vector-valued function
c          of the scalar t and the vector y.  Subroutine F is to
c          compute the function f.  It is to have the form
c               SUBROUTINE F (NEQ, T, Y, YDOT, RPAR, IPAR, IFAIL)
c               DIMENSION Y(NEQ), YDOT(NEQ), RPAR(*), IPAR(*)
c          where NEQ, T, and Y are input, and the array YDOT = f(t,y)
c          is output.  Y and YDOT are arrays of length NEQ.
c          (In the DIMENSION statement above, NEQ  can be replaced by
c          *  to make  Y  and  YDOT  assumed size arrays.)
c
c          The IFAIL argument is an output flag to indicate whether
c          f(t,y) could not be evaluated for the given arguments.
c          The input value of IFAIL is 0 and a return value of 0
c          indicates success.  The F routine should set IFAIL .ne. 0
c          if it failed to evaluate this function.
c
c          Subroutine F should not alter Y or T.
c          F must be declared EXTERNAL in the calling program.
c
c          Subroutine F may access user-defined real and integer
c          work arrays RPAR and IPAR, which are to be dimensioned
c          in the user-s calling (main) program.
c
c          If quantities computed in the F routine are needed
c          externally to VODPK, an extra call to F should be made
c          for this purpose, for consistent and accurate results.
c          If only the derivative dy/dt is needed, use VINDY instead.
c
c NEQ    = The size of the ODE system (number of first order
c          ordinary differential equations).  Used only for input.
c          NEQ may not be increased during the problem, but
c          can be decreased (with ISTATE = 3 in the input).
c
c Y      = A real array for the vector of dependent variables, of
c          length NEQ or more.  Used for both input and output on the
c          first call (ISTATE = 1), and only for output on other calls.
c          On the first call, Y must contain the vector of initial
c          values.  In the output, Y contains the computed solution
c          evaluated at T.  If desired, the Y array may be used
c          for other purposes between calls to the solver.
c
c          This array is passed as the Y argument in all calls to
c          F, JAC, and PSOL.
c
c T      = The independent variable.  In the input, T is used only on
c          the first call, as the initial point of the integration.
c          In the output, after each call, T is the value at which a
c          computed solution Y is evaluated (usually the same as TOUT).
c          On an error return, T is the farthest point reached.
c
c TOUT   = The next value of t at which a computed solution is desired.
c          Used only for input.
c
c          When starting the problem (ISTATE = 1), TOUT may be equal
c          to T for one call, then should .ne. T for the next call.
c          For the initial T, an input value of TOUT .ne. T is used
c          in order to determine the direction of the integration
c          (i.e. the algebraic sign of the step sizes) and the rough
c          scale of the problem.  Integration in either direction
c          (forward or backward in t) is permitted.
c
c          If ITASK = 2 or 5 (one-step modes), TOUT is ignored after
c          the first call (i.e. the first call with TOUT .ne. T).
c          Otherwise, TOUT is required on every call.
c
c          If ITASK = 1, 3, or 4, the values of TOUT need not be
c          monotone, but a value of TOUT which backs up is limited
c          to the current internal t interval, whose endpoints are
c          TCUR - HU and TCUR.  (See optional output, below, for
c          TCUR and HU.)
c
c ITOL   = An indicator for the type of error control.  See
c          description below under ATOL.  Used only for input.
c
c RTOL   = A relative error tolerance parameter, either a scalar or
c          an array of length NEQ.  See description below under ATOL.
c          Input only.
c
c ATOL   = An absolute error tolerance parameter, either a scalar or
c          an array of length NEQ.  Input only.
c
c          The input parameters ITOL, RTOL, and ATOL determine
c          the error control performed by the solver.  The solver will
c          control the vector e = (e(i)) of estimated local errors
c          in Y, according to an inequality of the form
c                      rms-norm of ( e(i)/EWT(i) )   .le.   1,
c          where       EWT(i) = RTOL(i)*abs(Y(i)) + ATOL(i),
c          and the rms-norm (root-mean-square norm) here is
c          rms-norm(v) = sqrt(sum v(i)**2 / NEQ).  Here EWT = (EWT(i))
c          is a vector of weights which must always be positive, and
c          the values of RTOL and ATOL should all be non-negative.
c          The following table gives the types (scalar/array) of
c          RTOL and ATOL, and the corresponding form of EWT(i).
c
c             ITOL    RTOL       ATOL          EWT(i)
c              1     scalar     scalar     RTOL*ABS(Y(i)) + ATOL
c              2     scalar     array      RTOL*ABS(Y(i)) + ATOL(i)
c              3     array      scalar     RTOL(i)*ABS(Y(i)) + ATOL
c              4     array      array      RTOL(i)*ABS(Y(i)) + ATOL(i)
c
c          When either of these parameters is a scalar, it need not
c          be dimensioned in the user's calling program.
c
c          If none of the above choices (with ITOL, RTOL, and ATOL
c          fixed throughout the problem) is suitable, more general
c          error controls can be obtained by substituting
c          user-supplied routines for the setting of EWT and/or for
c          the norm calculation.  See Part iv below.
c
c          If global errors are to be estimated by making a repeated
c          run on the same problem with smaller tolerances, then all
c          components of RTOL and ATOL (i.e. of EWT) should be scaled
c          down uniformly.
c
c ITASK  = An index specifying the task to be performed.
c          Input only.  ITASK has the following values and meanings.
c          1  means normal computation of output values of y(t) at
c             t = TOUT (by overshooting and interpolating).
c          2  means take one step only and return.
c          3  means stop at the first internal mesh point at or
c             beyond t = TOUT and return.
c          4  means normal computation of output values of y(t) at
c             t = TOUT but without overshooting t = TCRIT.
c             TCRIT must be input as RWORK(1).  TCRIT may be equal to
c             or beyond TOUT, but not behind it in the direction of
c             integration.  This option is useful if the problem
c             has a singularity at or beyond t = TCRIT.
c          5  means take one step, without passing TCRIT, and return.
c             TCRIT must be input as RWORK(1).
c
c          Note..  If ITASK = 4 or 5 and the solver reaches TCRIT
c          (within roundoff), it will return T = TCRIT (exactly) to
c          indicate this (unless ITASK = 4 and TOUT comes before TCRIT,
c          in which case answers at T = TOUT are returned first).
c
c ISTATE = an index used for input and output to specify the
c          the state of the calculation.
c
c          In the input, the values of ISTATE are as follows.
c          1  means this is the first call for the problem
c             (initializations will be done).  See note below.
c          2  means this is not the first call, and the calculation
c             is to continue normally, with no change in any input
c             parameters except possibly TOUT and ITASK.
c             (If ITOL, RTOL, and/or ATOL are changed between calls
c             with ISTATE = 2, the new values will be used but not
c             tested for legality.)
c          3  means this is not the first call, and the
c             calculation is to continue normally, but with
c             a change in input parameters other than
c             TOUT and ITASK.  Changes are allowed in
c             NEQ, ITOL, RTOL, ATOL, IOPT, LRW, LIW, MF,
c             and any of the optional input except H0.
c
c          Note..  A preliminary call with TOUT = T is not counted
c          as a first call here, as no initialization or checking of
c          input is done.  (Such a call is sometimes useful to include
c          the initial conditions in the output.)
c          Thus the first call for which TOUT .ne. T requires
c          ISTATE = 1 in the input.
c
c          In the output, ISTATE has the following values and meanings.
c           1  means nothing was done, as TOUT was equal to T with
c              ISTATE = 1 in the input.
c           2  means the integration was performed successfully.
c          -1  means an excessive amount of work (more than MXSTEP
c              steps) was done on this call, before completing the
c              requested task, but the integration was otherwise
c              successful as far as T.  (MXSTEP is an optional input
c              and is normally 500.)  To continue, the user may
c              simply reset ISTATE to a value .gt. 1 and call again.
c              (The excess work step counter will be reset to 0.)
c              In addition, the user may increase MXSTEP to avoid
c              this error return.  (See optional input below.)
c          -2  means too much accuracy was requested for the precision
c              of the machine being used.  This was detected before
c              completing the requested task, but the integration
c              was successful as far as T.  To continue, the tolerance
c              parameters must be reset, and ISTATE must be set
c              to 3.  The optional output TOLSF may be used for this
c              purpose.  (Note.. If this condition is detected before
c              taking any steps, then an illegal input return
c              (ISTATE = -3) occurs instead.)
c          -3  means illegal input was detected, before taking any
c              integration steps.  See written message for details.
c              Note..  If the solver detects an infinite loop of calls
c              to the solver with illegal input, it will cause
c              the run to stop.
c          -4  means there were repeated error test failures on
c              one attempted step, before completing the requested
c              task, but the integration was successful as far as T.
c              The problem may have a singularity, or the input
c              may be inappropriate.
c          -5  means there were repeated convergence test failures on
c              one attempted step, before completing the requested
c              task, but the integration was successful as far as T.
c              This may be caused by a poor preconditioner matrix.
c          -6  means EWT(i) became zero for some i during the
c              integration.  Pure relative error control (ATOL(i)=0.0)
c              was requested on a variable which has now vanished.
c              The integration was successful as far as T.
c          -7  means an unrecoverable error occurred in JAC or PSOL.
c              Either JAC returned IER .ne. 0, or PSOL returned
c              IER .lt. 0.
c          -8  means the F routine returned IFAIL .ne. 0, and the
c              integrator was unable to avoid this condition.
c              The integration was successful as far as T.
c
c          Note..  Since the normal output value of ISTATE is 2,
c          it does not need to be reset for normal continuation.
c          Also, since a negative input value of ISTATE will be
c          regarded as illegal, a negative output value requires the
c          user to change it, and possibly other input, before
c          calling the solver again.
c
c IOPT   = An integer flag to specify whether or not any optional
c          input is being used on this call.  Input only.
c          The optional input is listed separately below.
c          IOPT = 0 means no optional input is being used.
c                   Default values will be used in all cases.
c          IOPT = 1 means optional input is being used.
c
c RWORK  = A real working array (single precision).
c          The length of RWORK must be at least
c             20 + NYH*(MAXORD + 1) + 3*NEQ + LENK + LWP   where
c          NYH    = the initial value of NEQ,
c          MAXORD = 12 (if METH = 1) or 5 (if METH = 2) (unless a
c                   smaller value is given as an optional input),
c          LENK = length of work space for Krylov-related data..
c          LENK = 0                                 if MITER = 0,
c          LENK = NEQ*(MAXL+3+MIN(1,MAXL-KMP))
c                  + (MAXL+3)*MAXL + 1              if MITER = 1,
c          LENK = 3*NEQ                             if MITER = 9.
c          LWP = length of real user work space for preconditioning.
c          (See JAC/PSOL.)
c          (See the MF description for METH and MITER.)
c          Thus if MAXORD has its default value and NEQ is constant,
c          this length is..
c             20 + 16*NEQ                    for MF = 10,
c             61 + 24*NEQ + LWP              for MF = 11,
c             20 + 19*NEQ + LWP              for MF = 19,
c             20 + 9*NEQ                     for MF = 20,
c             61 + 17*NEQ + LWP              for MF = 21,
c             20 + 12*NEQ + LWP              for MF = 29
c          The first 20 words of RWORK are reserved for conditional
c          and optional input and optional output.
c
c          The following word in RWORK is a conditional input..
c            RWORK(1) = TCRIT = critical value of t which the solver
c                       is not to overshoot.  Required if ITASK is
c                       4 or 5, and ignored otherwise.  (See ITASK.)
c
c LRW    = The length of the array RWORK, as declared by the user.
c          (This will be checked by the solver.)
c
c IWORK  = An integer work array.  The length of IWORK must be at least
c             30        if MITER = 0  (MF = 10, 20), or
c             30 + LIWP  otherwise (MF = 11, 21, 19, 29).
c          LIWP = length of integer user work space for preconditioning.
c          (See conditional input list following).
c
c          The first 30 words of IWORK are reserved for conditional and
c          optional input and optional output.
c
c          The following 4 words in IWORK are conditional input,
c          required if MITER .ge. 1..
c
c          IWORK(1) = LWP  = length of real array WP for use in
c                     preconditioning (part of RWORK array).
c          IWORK(2) = LIWP = length of integer array IWP for use in
c                     preconditioning (part of IWORK array).
c                     The arrays WP and IWP are work arrays under the
c                     user-s control, for use in the routines that
c                     perform preconditioning operations (JAC and PSOL).
c          IWORK(3) = JPRE = preconditioner type flag..
c                   = 0 for no preconditioning (P1 = P2 = I
c                   = 1 for left-only preconditioning (P2 = I)
c                   = 2 for right-only preconditioning (P1 = I)
c                   = 3 for two-sided preconditioning
c          IWORK(4) = JACFLG = flag for whether JAC is called.
c                   = 0 if JAC is not to be called,
c                   = 1 if JAC is to be called.
c                     Use JACFLG = 1 if JAC computes any nonconstant
c                     data needed in preconditioning operations,
c                     such as some of the Jacobian elements.
c
c
c LIW    = the length of the array IWORK, as declared by the user.
c          (This will be checked by the solver.)
c
c Note..  The work arrays must not be altered between calls to VODPK
c for the same problem, except possibly for the conditional and
c optional input, and except for the last 3*NEQ words of RWORK.
c The latter space is used for internal scratch space, and so is
c available for use by the user outside VODPK between calls, if
c desired (but not for use by F or JAC).
c
c JAC    = The name of the user-supplied routine (MITER = 1 or 4) to
c          compute the Jacobian matrix, df/dy, as a function of
c          the scalar t and the vector y.  It is to have the form
c
c               SUBROUTINE JAC (F, NEQ, T, Y, YSV, REWT, FTY, V, HRL1,
c                               WP, IWP, IER, RPAR, IPAR)
c               EXTERNAL F
c               DIMENSION Y(NEQ), YSV(NEQ), REWT(NEQ), FTY(NEQ),
c                         V(NEQ), WP(*), IWP(*), RPAR(*), IPAR(*)
c
c          This routine must evaluate and preprocess any parts of the
c          Jacobian matrix df/dy used in the preconditioners P1, P2 .
c          The Y and FTY arrays contain the current values of y and
c          f(t,y), respectively, and YSV also contains the current
c          value of y.  The array V is work space of length
c          NEQ for use by JAC.  REWT is the array of reciprocal error
c          weights (1/ewt).  JAC must multiply all computed Jacobian
c          elements by the scalar -hrl1, add the identity matrix I and
c          do any factorization operations called for, in preparation
c          for solving linear systems with a coefficient matrix of
c          P1 or P2.  The matrix P1*P2 should be an approximation to
c          I - hrl1 * (df/dy), where hrl1 is stored in HRL1.  JAC should
c          return IER = 0 if successful, and IER .ne. 0 if not.
c          (If IER .ne. 0, a smaller time step will be tried.)
c          The arrays WP (of length LWP) and IWP (of length LIWP)
c          are for use by JAC and PSOL for work space and for storage
c          of data needed for the solution of the preconditioner
c          linear systems.  Their lengths and contents are under the
c          user-s control.
c          The JAC routine may save relevant Jacobian elements (or
c          approximations) used in the preconditioners, along with the
c          value of hrl1, and use these to reconstruct preconditioner
c          matrices later without reevaluationg those elements.
c          This may be cost-effective if JAC is called with hrl1
c          considerably different from its earlier value, indicating
c          that a corrector convergence failure has occurred because
c          of the change in hrl1, not because of changes in the
c          value of the Jacobian.  In doing this, use the saved and
c          current values of hrl1 to decide whether to use saved
c          or reevaluated elements.
c          JAC may alter V, but not Y, YSV, REWT, FTY, or HRL1.
c          JAC must be declared external in the calling program.
c
c PSOL   = the name of the user-supplied routine for the
c          solution of preconditioner linear systems.
c          It is to have the form
c            SUBROUTINE PSOL (NEQ, T, Y, FTY, WK, HRL1, WP, IWP, B, LR,
c                             IER, RPAR, IPAR)
c            DIMENSION Y(NEQ), FTY(NEQ), WK(NEQ), WP(*), IWP(*),
c                      B(NEQ), RPAR(*), IPAR(*)
c          This routine must solve a linear system with b (stored in B)
c          as right-hand side and one of the preconditioning matrices,
c          P1 or P2, as coefficient matrix, and return the solution
c          vector in B.  LR is a flag concerning left vs. right
c          preconditioning, input to PSOL.  PSOL is to use P1 if LR = 1
c          and P2 if LR = 2.  In the case miter = 9 (no Krylov
c          iteration), LR will be 0, and PSOL is to return in B the
c          desired approximate solution to A * x = b, where
c          A = I - hrl1 * (df/dy).  (hrl1 is stored in HRL1.)  PSOL can
c          use data generated in the JAC routine and stored in WP and
c          IWP.  The Y and FTY arrays contain the current values of y
c          and f(t,y), respectively.  The array WK is work space of
c          length NEQ for use by PSOL.
c          The argument HRL1 is the current value of the scalar appear-
c          ing in the linear system.  If the old value, as of the last
c          JAC call, is needed, it must have been saved by JAC in WP.
c          On return, PSOL should set the error flag IER as follows..
c            IER = 0 if PSOL was successful,
c            IER .gt. 0 on a recoverable error, meaning that the
c                   time step will be retried,
c            IER .lt. 0 on an unrecoverable error, meaning that the
c                   solver is to stop immediately.
c          PSOL may not alter Y, FTY, or HRL1.
c          PSOL must be declared external in the calling program.
c
c MF     = The method flag.  Used only for input.  The legal values of
c          MF are 10, 11, 19, 20, 21, 29 .
c          MF is a two-digit integer, MF = 10*METH + MITER .
c          METH indicates the basic linear multistep method..
c            METH = 1 means the implicit Adams method.
c            METH = 2 means the method based on backward
c                     differentiation formulas (BDF-s).
c          MITER indicates the corrector iteration method.  Currently,
c            the values of MITER have the following meanings..
c
c          0 means functional iteration is used (no Jacobian matrix
c            is involved).
c
c          1 means SPIGMR, a scaled, preconditioned, incomplete version
c            of GMRES, a generalized minimum residual method, is used.
c            This is the best choice in general.
c
c          9 means that only a user-supplied matrix P (approximating A)
c            will be used, with no Krylov iteration done internally to
c            VODPK.  This option allows the user to provide the complete
c            linear system solution algorithm, if desired.
c
c The user can apply preconditioning to the linear system A*x = b,
c by means of arbitrary matrices (the preconditioners).
c
c RPAR     User-specified array used to communicate real parameters
c          to user-supplied subroutines.  If RPAR is a vector, then
c          it must be dimensioned in the user's main program.  If it
c          is unused or it is a scalar, then it need not be
c          dimensioned.
c
c IPAR     User-specified array used to communicate integer parameter
c          to user-supplied subroutines.  The comments on dimensioning
c          RPAR apply to IPAR.
c-----------------------------------------------------------------------
c Optional Input.
c
c The following is a list of the optional input provided for in the
c call sequence.  (See also Part ii.)  For each such input variable,
c this table lists its name as used in this documentation, its
c location in the call sequence, its meaning, and the default value.
c The use of any of this input requires IOPT = 1, and in that
c case all of this input is examined.  A value of zero for any
c of these optional input variables will cause the default value to be
c used.  Thus to use a subset of the optional input, simply preload
c locations 5 to 10 in RWORK and IWORK to 0.0 and 0 respectively, and
c then set those of interest to nonzero values.
c
c NAME    LOCATION      MEANING AND DEFAULT VALUE
c
c H0      RWORK(5)  The step size to be attempted on the first step.
c                   The default value is determined by the solver.
c
c HMAX    RWORK(6)  The maximum absolute step size allowed.
c                   The default value is infinite.
c
c HMIN    RWORK(7)  The minimum absolute step size allowed.
c                   The default value is 0.  (This lower bound is not
c                   enforced on the final step before reaching TCRIT
c                   when ITASK = 4 or 5.)
c
c MAXORD  IWORK(5)  The maximum order to be allowed.  The default
c                   value is 12 if METH = 1, and 5 if METH = 2.
c                   If MAXORD exceeds the default value, it will
c                   be reduced to the default value.
c                   If MAXORD is changed during the problem, it may
c                   cause the current order to be reduced.
c
c MXSTEP  IWORK(6)  Maximum number of (internally defined) steps
c                   allowed during one call to the solver.
c                   The default value is 500.
c
c MXHNIL  IWORK(7)  Maximum number of messages printed (per problem)
c                   warning that T + H = T on a step (H = step size).
c                   This must be positive to result in a non-default
c                   value.  The default value is 10.
c
c MAXL    IWORK(8)  maximum number of iterations in the SPIGMR
c                   algorithm (.le. NEQ).  The default is
c                   MAXL = min(5, NEQ).
c
c KMP     IWORK(9)  number of vectors on which orthogonalization
c                   is done in the SPIGMR algorithm (.le. MAXL).
c                   The default is KMP = MAXL (complete GMRES method).
c                   See Ref. 2 for details on incomplete GMRES.
c                   Note:  When KMP .lt. MAXL and MITER = 1, the length
c                          of RWORK must be defined accordingly.  See
c                          the definition of RWORK above.
c-----------------------------------------------------------------------
c Optional Output.
c
c As optional additional output from VODPK, the variables listed
c below are quantities related to the performance of VODPK
c which are available to the user.  These are communicated by way of
c the work arrays, but also have internal mnemonic names as shown.
c Except where stated otherwise, all of this output is defined
c on any successful return from VODPK, and on any return with
c ISTATE = -1, -2, -4, -5, ..., -8.  On an illegal input return
c (ISTATE = -3), they will be unchanged from their existing values
c (if any), except possibly for TOLSF, LENRW, and LENIW.
c On any error return, output relevant to the error will be defined,
c as noted below.
c
c NAME    LOCATION      MEANING
c
c HU      RWORK(11) The step size in t last used (successfully).
c
c HCUR    RWORK(12) The step size to be attempted on the next step.
c
c TCUR    RWORK(13) The current value of the independent variable
c                   which the solver has actually reached, i.e. the
c                   current internal mesh point in t.  In the output,
c                   TCUR will always be at least as far from the
c                   initial value of t as the current argument T,
c                   but may be farther (if interpolation was done).
c
c TOLSF   RWORK(14) A tolerance scale factor, greater than 1.0,
c                   computed when a request for too much accuracy was
c                   detected (ISTATE = -3 if detected at the start of
c                   the problem, ISTATE = -2 otherwise).  If ITOL is
c                   left unaltered but RTOL and ATOL are uniformly
c                   scaled up by a factor of TOLSF for the next call,
c                   then the solver is deemed likely to succeed.
c                   (The user may also ignore TOLSF and alter the
c                   tolerance parameters in any other way appropriate.)
c
c NST     IWORK(11) The number of steps taken for the problem so far.
c
c NFE     IWORK(12) The number of f evaluations for the problem so far.
c
c NPE     IWORK(13) The number of preconditioner evaluations (JAC calls)
c                   so far.
c
c NQU     IWORK(14) The method order last used (successfully).
c
c NQCUR   IWORK(15) The order to be attempted on the next step.
c
c IMXER   IWORK(16) The index of the component of largest magnitude in
c                   the weighted local error vector ( e(i)/EWT(i) ),
c                   on an error return with ISTATE = -4 or -5.
c
c LENRW   IWORK(17) The length of RWORK actually required.
c                   This is defined on normal returns and on an illegal
c                   input return for insufficient storage.
c
c LENIW   IWORK(18) The length of IWORK actually required.
c                   This is defined on normal returns and on an illegal
c                   input return for insufficient storage.
c
c NNI     IWORK(20) The number of nonlinear iterations so far (each of
c                   which calls the Krylov iterative linear solver).
c
c NCFN    IWORK(21) The number of convergence failures of the nonlinear
c                   (Newton) iteration so far.
c                   Note.. A measure of success is the overall
c                   rate of nonlinear convergence failures, NCFN/NST.
c
c NETF    IWORK(22) The number of error test failures of the integrator
c                   so far.
c
c
c NLI     IWORK(23) The number of linear iterations so far.
c                   Note.. a measure of the success of algorithm is
c                   the average number of linear iterations per
c                   nonlinear iteration, given by NLI/NNI.
c                   If this is close to MAXL, MAXL may be too small.
c
c NPS     IWORK(24) The number of preconditioning solve operations
c                   (PSOL calls) so far.
c
c
c NCFL    IWORK(25) The number of convergence failures of the linear
c                   iteration so far.
c                   Note.. A measure of success is the overall
c                   rate of linear convergence failures, NCFL/NNI.
c
c The following two arrays are segments of the RWORK array which
c may also be of interest to the user as optional output.
c For each array, the table below gives its internal name,
c its base address in RWORK, and its description.
c
c NAME    BASE ADDRESS      DESCRIPTION
c
c YH      21             The Nordsieck history array, of size NYH by
c                        (NQCUR + 1), where NYH is the initial value
c                        of NEQ.  For j = 0,1,...,NQCUR, column j+1
c                        of YH contains HCUR**j/factorial(j) times
c                        the j-th derivative of the interpolating
c                        polynomial currently representing the
c                        solution, evaluated at t = TCUR.
c
c ACOR     LENRW-NEQ+1   Array of size NEQ used for the accumulated
c                        corrections on each step, scaled in the output
c                        to represent the estimated local error in Y
c                        on the last step.  This is the vector e in
c                        the description of the error control.  It is
c                        defined only on a successful return from VODPK.
c
c-----------------------------------------------------------------------
c Interrupting and Restarting
c
c If the integration of a given problem by VODPK is to be
c interrrupted and then later continued, such as when restarting
c an interrupted run or alternating between two or more ODE problems,
c the user should save, following the return from the last VODPK call
c prior to the interruption, the contents of the call sequence
c variables and internal COMMON blocks, and later restore these
c values before the next VODPK call for that problem.  To save
c and restore the COMMON blocks, use subroutine VKSRC, as
c described below in part ii.
c
c-----------------------------------------------------------------------
c Part ii.  Other Routines Callable.
c
c The following are optional calls which the user may make to
c gain additional capabilities in conjunction with VODPK.
c
c     FORM OF CALL                  FUNCTION
c
c  CALL VKSRC(RSAV,ISAV,JOB) Saves and restores the contents of
c                             the internal COMMON blocks used by
c                             VODPK. (See Part iii below.)
c                             RSAV must be a real array of length 52
c                             or more, and ISAV must be an integer
c                             array of length 52 or more.
c                             JOB=1 means save COMMON into RSAV/ISAV.
c                             JOB=2 means restore COMMON from RSAV/ISAV.
c
c                                VKSRC is useful if one is
c                             interrupting a run and restarting
c                             later, or alternating between two or
c                             more problems solved with VODPK.
c
c  CALL VINDY(,,,,,)         Provide derivatives of y, of various
c        (See below.)         orders, at a specified point T, if
c                             desired.  It may be called only after
c                             a successful return from VODPK.
c
c The detailed instructions for using VINDY are as follows.
c The form of the call is..
c
c  CALL VINDY (T, K, RWORK(21), NYH, DKY, IFLAG)
c
c The input parameters are..
c
c T         = Value of independent variable where answers are desired
c             (normally the same as the T last returned by VODPK).
c             For valid results, T must lie between TCUR - HU and TCUR.
c             (See optional output for TCUR and HU.)
c K         = Integer order of the derivative desired.  K must satisfy
c             0 .le. K .le. NQCUR, where NQCUR is the current order
c             (see optional output).  The capability corresponding
c             to K = 0, i.e. computing y(T), is already provided
c             by VODPK directly.  Since NQCUR .ge. 1, the first
c             derivative dy/dt is always available with VINDY.
c RWORK(21) = The base address of the history array YH.
c NYH       = Column length of YH, equal to the initial value of NEQ.
c
c The output parameters are..
c
c DKY       = A real array of length NEQ containing the computed value
c             of the K-th derivative of y(t).
c IFLAG     = Integer flag, returned as 0 if K and T were legal,
c             -1 if K was illegal, and -2 if T was illegal.
c             On an error return, a message is also written.
c-----------------------------------------------------------------------
c Part iii.  COMMON Blocks.
c If VODPK is to be used in an overlay situation, the user
c must declare, in the primary overlay, the variables in..
c   (1) the call sequence to VODPK,
c   (2) the two internal COMMON blocks
c         /VOD001/  of length  81  (48 single precision words
c                         followed by 33 integer words),
c         /VOD002/  of length  9  (1 single precision word
c                         followed by 8 integer words),
c
c         /VPK001/  of length 14 (3 single precision words
c                         followed by 11 integer words)
c
c If VODPK is used on a system in which the contents of internal
c COMMON blocks are not preserved between calls, the user should
c declare the above three COMMON blocks in the calling (main) program
c to insure that their contents are preserved.
c
c-----------------------------------------------------------------------
c Part iv.  Optionally Replaceable Solver Routines.
c
c Below are descriptions of two routines in the VODPK package which
c relate to the measurement of errors.  Either routine can be
c replaced by a user-supplied version, if desired.  However, since such
c a replacement may have a major impact on performance, it should be
c done only when absolutely necessary, and only with great caution.
c (Note.. The means by which the package version of a routine is
c superseded by the user's version may be system-dependent.)
c
c (a) EWSET.
c The following subroutine is called just before each internal
c integration step, and sets the array of error weights, EWT, as
c described under ITOL/RTOL/ATOL above..
c     SUBROUTINE EWSET (NEQ, ITOL, RTOL, ATOL, YCUR, EWT)
c where NEQ, ITOL, RTOL, and ATOL are as in the VODPK call sequence,
c YCUR contains the current dependent variable vector, and
c EWT is the array of weights set by EWSET.
c
c If the user supplies this subroutine, it must return in EWT(i)
c (i = 1,...,NEQ) a positive quantity suitable for comparison with
c errors in Y(i).  The EWT array returned by EWSET is passed to the
c VNORML routine (see below), and also used by VODPK in the computation
c of the optional output IMXER, the diagonal Jacobian approximation,
c and the increments for difference quotient Jacobians.
c
c In the user-supplied version of EWSET, it may be desirable to use
c the current values of derivatives of y.  Derivatives up to order NQ
c are available from the history array YH, described above under
c Optional Output.  In EWSET, YH is identical to the YCUR array,
c extended to NQ + 1 columns with a column length of NYH and scale
c factors of h**j/factorial(j).  On the first call for the problem,
c given by NST = 0, NQ is 1 and H is temporarily set to 1.0.
c NYH is the initial value of NEQ.  The quantities NQ, H, and NST
c can be obtained by including in EWSET the statements..
c     COMMON /VOD001/ RVOD(48), IVOD(33)
c     COMMON /VOD002/ HU, NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
c     NQ = IVOD(28)
c     H = RVOD(21)
c Thus, for example, the current value of dy/dt can be obtained as
c YCUR(NYH+i)/H  (i=1,...,NEQ)  (and the division by H is
c unnecessary when NST = 0).
c
c (b) VNORML.
c The following is a real function routine which computes the weighted
c root-mean-square norm of a vector v..
c     D = VNORML (N, V, W)
c where..
c   N = the length of the vector,
c   V = real array of length N containing the vector,
c   W = real array of length N containing weights,
c   D = sqrt( (1/N) * sum(V(i)*W(i))**2 ).
c VNORML is called with N = NEQ and with W(i) = 1.0/EWT(i), where
c EWT is as set by subroutine EWSET.
c
c If the user supplies this function, it should return a non-negative
c value of VNORML suitable for use in the error control in VODPK.
c None of the arguments should be altered by VNORML.
c For example, a user-supplied VNORML routine might..
c   -substitute a max-norm of (V(i)*W(i)) for the RMS-norm, or
c   -ignore some components of V in the norm, with the effect of
c    suppressing the error control on those components of Y.
c-----------------------------------------------------------------------
c Other Routines in the VODPK Package.
c
c In addition to subroutine VODPK, the VODPK package includes the
c following subroutines and function routines..
c  VHIN     computes an approximate step size for the initial step.
c  VINDY    computes an interpolated value of the y vector at t = TOUT.
c  VSTEP    is the core integrator, which does one step of the
c           integration and the associated error control.
c  VSET     sets all method coefficients and test constants.
c  VJUST    adjusts the history array on a change of order.
c  VNLSK    solves the underlying nonlinear system -- the corrector.
c  VSOLPK   manages solution of linear system in chord iteration.
c  VSPIG    performs the SPIGMR algorithm.
c  VATV     computes a scaled, preconditioned product (I-hrl1*J)*v.
c  SVRORTHOG   orthogonalizes a vector against previous basis vectors.
c  SHEQR    generates a QR factorization of a Hessenberg matrix.
c  SHELS    finds the least squares solution of a Hessenberg system.
c  VUSOL    interfaces to the user-s PSOL routine (MITER = 9).
c  EWSET    sets the error weight vector EWT before each step.
c  VNORML    computes the weighted r.m.s. norm of a vector.
c  VKSRC    is a user-callable routine to save and restore
c           the contents of the internal COMMON blocks.
c  SAXPY, SSCAL, SCOPY, SDOT, and SNRM2 are basic linear
c           algebra modules (BLAS) used by this package.
c  R1MACH9   computes the unit roundoff in a machine-independent manner.
c  XERRWV   handles the printing of all error messages and warnings.
c           XERRWV is machine-dependent.

c Note..  VNORML, SDOT, SNRM2, and R1MACH9 are
c function routines.  All the others are subroutines.
c
c The intrinsic and external routines used by the VODPK package are..
c ABS, float, max, min, SIGN, SQRT, ijmgetmr, xerrab, and write.
c
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for labeled COMMON block VOD002 --------------------
c
      doubleprecision HU
      INTEGER NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
c
c Type declarations for labeled COMMON block VPK001 --------------------
c
      doubleprecision DELT, SQRTN, RSQRTN
      INTEGER JPRE, JACFLG, LOCWP, LOCIWP, LVSAV, KMP, MAXL, MNEWT, NLI, 
     &   NPS, NCFL
c Type declarations for local variables --------------------------------
c
      EXTERNAL VNLSK
      LOGICAL IHIT, LAVD, LCFN, LCFL, LWARN
      doubleprecision ATOLI, AVDIM, BIG, EWTI, FOUR, H0, HMAX, HMX, HUN, 
     &   ONE, PT05, PT2, PT9, RCFL, RCFN, RH, RTOLI, SIZE, TCRIT, TNEXT, 
     &   TOLSF, TP, TWO, ZERO
      INTEGER I, IER, IFLAG, IMXER, KGO, LENIW, LENIWK, LENRW, LENWK, 
     &   LENWM, LF0, LIWP, LWP, MORD, MXHNL0, MXSTP0, NCFL0, NCFN0, 
     &   NITER, NLI0, NNI0, NNID, NSTD, NSLAST, NWARN, IFAIL
      CHARACTER*80 MSG
c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision R1MACH9, VNORML
c
      DIMENSION MORD(2)
c-----------------------------------------------------------------------
c The following Fortran-77 declarations are to cause the values of the
c listed (local) variables to be saved between calls to VODPK.
c-----------------------------------------------------------------------
      SAVE MORD, MXHNL0, MXSTP0
      SAVE ZERO, ONE, TWO, FOUR, HUN, PT05, PT2, PT9
c-----------------------------------------------------------------------
c The following internal COMMON blocks contain variables which are
c communicated between subroutines in the VODPK package, or which are
c to be saved between calls to VODPK.
c In each block, real variables precede integers.
c The block /VOD001/ appears in subroutines VODPK, VINDY, VSTEP, VSET,
c VJUST, VNLSK, VSOLPK, VATV, and VKSRC.
c The block /VOD002/ appears in subroutines VODPK, VINDY, VSTEP, VNLSK,
c VSOLPK, VATV, and VKSRC.
c The block /VPK001/ appears in subroutines VODPK, VNLSK, VSOLPK,
c and VKSRC.
c
c The variables stored in the internal COMMON blocks are as follows..
c
c ACNRM  = Weighted r.m.s. norm of accumulated correction vectors.
c CCMXJ  = Threshhold on DRC for updating the Jacobian. (See DRC.)
c CONP   = The saved value of TQ(5).
c CRATE  = Estimated corrector convergence rate constant.
c DRC    = Relative change in H*RL1 since last VJAC call.
c EL     = Real array of integration coefficients.  See VSET.
c ETA    = Saved tentative ratio of new to old H.
c ETAMAX = Saved maximum value of ETA to be allowed.
c H      = The step size.
c HMIN   = The minimum absolute value of the step size H to be used.
c HMXI   = Inverse of the maximum absolute value of H to be used.
c          HMXI = 0.0 is allowed and corresponds to an infinite HMAX.
c HNEW   = The step size to be attempted on the next step.
c HSCAL  = Stepsize in scaling of YH array.
c PRL1   = The saved value of RL1.
c RC     = Ratio of current H*RL1 to value on last VJAC call.
c RL1    = The reciprocal of the coefficient EL(1).
c TAU    = Real vector of past NQ step sizes, length 13.
c TQ     = A real vector of length 5 in which VSET stores constants
c          used for the convergence test, the error test, and the
c          selection of H at a new order.
c TN     = The independent variable, updated on each step taken.
c UROUND = The machine unit roundoff.  The smallest positive real number
c          such that  1.0 + UROUND .ne. 1.0
c ICF    = Integer flag for convergence failure in VNLSK..
c            0 means no failures.
c            1 means convergence failure with out of date Jacobian
c                   (recoverable error).
c            2 means convergence failure with current Jacobian or
c                   singular matrix (unrecoverable error).
c INIT   = Saved integer flag indicating whether initialization of the
c          problem has been done (INIT = 1) or not.
c IPUP   = Saved flag to signal updating of Newton matrix.
c JCUR   = Output flag from VJAC showing Jacobian status..
c            JCUR = 0 means J is not current.
c            JCUR = 1 means J is current.
c JSTART = Integer flag used as input to VSTEP..
c            0  means perform the first step.
c            1  means take a new step continuing from the last.
c            -1 means take the next step with a new value of MAXORD,
c                  HMIN, HMXI, N, METH, MITER, and/or matrix parameters.
c          On return, VSTEP sets JSTART = 1.
c JSV    = Integer flag for Jacobian saving, = sign(MF).
c KFLAG  = A completion code from VSTEP with the following meanings..
c               0      the step was succesful.
c              -1      the requested error could not be achieved.
c              -2      corrector convergence could not be achieved.
c              -3, -4  fatal error in VNLS (can not occur here).
c              -5      corrector loop unable to avoid failure in F.
c KUTH   = Input flag to VSTEP showing whether H was reduced by the
c          driver.  KUTH = 1 if H was reduced, = 0 otherwise.
c L      = Integer variable, NQ + 1, current order plus one.
c LMAX   = MAXORD + 1 (used for dimensioning).
c LOCJS  = A pointer to the saved Jacobian, whose storage starts at
c          WM(LOCJS), if JSV = 1.
c LYH, LEWT, LACOR, LSAVF, LWM, LIWM = Saved integer pointers
c          to segments of RWORK and IWORK.
c MAXORD = The maximum order of integration method to be allowed.
c METH/MITER = The method flags.  See MF.
c MSBJ   = The maximum number of steps between J evaluations, = 50.
c MXHNIL = Saved value of optional input MXHNIL.
c MXSTEP = Saved value of optional input MXSTEP.
c N      = The number of first-order ODEs, = NEQ.
c NEWH   = Saved integer to flag change of H.
c NEWQ   = The method order to be used on the next step.
c NHNIL  = Saved counter for occurrences of T + H = T.
c NQ     = Integer variable, the current integration method order.
c NQNYH  = Saved value of NQ*NYH.
c NQWAIT = A counter controlling the frequency of order changes.
c          An order change is about to be considered if NQWAIT = 1.
c NSLJ   = The number of steps taken as of the last Jacobian update.
c NSLP   = Saved value of NST as of last Newton matrix update.
c NYH    = Saved value of the initial value of NEQ.
c
c HU     = The step size in t last used.
c NCFN   = Number of nonlinear convergence failures so far.
c NETF   = The number of error test failures of the integrator so far.
c NFE    = The number of f evaluations for the problem so far.
c NPE    = The number of preconditioner evaluations (JAC calls) so far.
c NLU    = The number of matrix LU decompositions so far.
c NNI    = Number of nonlinear iterations so far.
c NQU    = The method order last used.
c NST    = The number of steps taken for the problem so far.
c
c DELT   = Convergence test constant in Krylov iterations.
c SQRTN  = SQRT(NEQ), for use in weights in Krylov convergence tests.
c RSQRTN = 1.0/SQRTN, also for use in convergence weights.
c JPRE   = Preconditioner type flag.
c JACFLG = Indicator for presence of user-supplied JAC routine.
c LOCWP  = Location of start of user-s WP array in WM work array.
c LOCIWP = Location of start of user-s IWP array in IWM work array.
c LVSAV  = Saved pointer to VSAV array in RWORK.
c KMP    = Number of vectors on which orthogonalization is done in
c          Krylov iteration.
c MAXL   = Maximum dimension of Krylov subspace used.
c MNEWT  = Newton iteration index.
c NLI    = Number of linear (Krylov) iterations done.
c NPS    = Number of preconditioner solvers (PSOL calls) done.
c NCFL   = Number of convergence failures in Krylov iteration.
c-----------------------------------------------------------------------
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
      COMMON /VOD002/ HU, NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
      COMMON /VPK001/ DELT, SQRTN, RSQRTN, JPRE, JACFLG, LOCIWP, LOCWP, 
     &   LVSAV, KMP, MAXL, MNEWT, NLI, NPS, NCFL
c
      DATA MORD(1),MORD(2)/12,5/, MXSTP0/500/, MXHNL0/10/
      DATA ZERO/0.0d0/, ONE/1.0d0/, TWO/2.0d0/, FOUR/4.0d0/, PT05/0.05d0
     &   /, PT2/0.2d0/, PT9/0.9d0/, HUN/100.0d0/
      doubleprecision scaleps
      common /comvatv/ scaleps
c
c     Special scaling factor for Newton iteration error TDR 11/19/93
      doubleprecision EFACN
      COMMON /TDR1/ EFACN
c
      scaleps = scalpk
      EFACN = efacnin
c
c-----------------------------------------------------------------------
c Block A.
c This code block is executed on every call.
c It tests ISTATE and ITASK for legality and branches appropriately.
c If ISTATE .gt. 1 but the flag INIT shows that initialization has
c not yet been done, an error return occurs.
c If ISTATE = 1 and TOUT = T, jump to Block G and return immediately.
c-----------------------------------------------------------------------
      IF (ISTATE .LT. 1 .OR. ISTATE .GT. 3) GO TO 601
      IF (ITASK .LT. 1 .OR. ITASK .GT. 5) GO TO 602
      IF (ISTATE .EQ. 1) GO TO 10
      IF (INIT .EQ. 0) GO TO 603
      IF (ISTATE .EQ. 2) GO TO 200
      GO TO 20
   10 INIT = 0
      IF (TOUT .EQ. T) RETURN
c-----------------------------------------------------------------------
c Block B.
c The next code block is executed for the initial call (ISTATE = 1),
c or for a continuation call with parameter changes (ISTATE = 3).
c It contains checking of all inputs and various initializations.
c
c First check legality of the non-optional inputs NEQ, ITOL, IOPT, MF.
c-----------------------------------------------------------------------
   20 IF (NEQ .LE. 0) GO TO 604
      IF (ISTATE .EQ. 1) GO TO 25
      IF (NEQ .GT. N) GO TO 605
   25 N = NEQ
      IF (ITOL .LT. 1 .OR. ITOL .GT. 4) GO TO 606
      IF (IOPT .LT. 0 .OR. IOPT .GT. 1) GO TO 607
      JSV = 0
      METH = MF/10
      MITER = MF - 10*METH
      IF (METH .LT. 1 .OR. METH .GT. 2) GO TO 608
      IF (MITER .LT. 0) GO TO 608
      IF (MITER .GT. 1 .AND. MITER .LT. 9) GO TO 608
      IF (MITER .GE. 1) JPRE = IWORK(3)
      JACFLG = 0
      IF (MITER .GE. 1) JACFLG = IWORK(4)
      IF (MITER .GE. 1 .AND. MITER .NE. 9 .AND. JPRE .EQ. 0) JACFLG = 0
c Next process and check the optional inputs. --------------------------
      IF (IOPT .EQ. 1) GO TO 40
      MAXORD = MORD(METH)
      MXSTEP = MXSTP0
      MXHNIL = MXHNL0
      IF (ISTATE .EQ. 1) H0 = ZERO
      HMXI = ZERO
      HMIN = ZERO
      MAXL = min(5,N)
      KMP = MAXL
      DELT = PT05
      GO TO 60
   40 MAXORD = IWORK(5)
      IF (MAXORD .LT. 0) GO TO 611
      IF (MAXORD .EQ. 0) MAXORD = 100
      MAXORD = min(MAXORD,MORD(METH))
      MXSTEP = IWORK(6)
      IF (MXSTEP .LT. 0) GO TO 612
      IF (MXSTEP .EQ. 0) MXSTEP = MXSTP0
      MXHNIL = IWORK(7)
      IF (MXHNIL .LT. 0) GO TO 613
      IF (MXHNIL .EQ. 0) MXHNIL = MXHNL0
      IF (ISTATE .NE. 1) GO TO 50
      H0 = RWORK(5)
      IF ((TOUT - T)*H0 .LT. ZERO) GO TO 614
   50 HMAX = RWORK(6)
      IF (HMAX .LT. ZERO) GO TO 615
      HMXI = ZERO
      IF (HMAX .GT. ZERO) HMXI = ONE/HMAX
      HMIN = RWORK(7)
      IF (HMIN .LT. ZERO) GO TO 616
      MAXL = IWORK(8)
      IF (MAXL .EQ. 0) MAXL = 5
      MAXL = min(MAXL,N)
      KMP = IWORK(9)
      IF (KMP .EQ. 0 .OR. KMP .GT. MAXL) KMP = MAXL
      DELT = RWORK(8)
      IF (DELT .EQ. 0.0d0) DELT = PT05
c-----------------------------------------------------------------------
c Set work array pointers and check lengths lrw and liw.
c Pointers to segments of RWORK and iwork are named by prefixing l to
c the name of the segment.  e.g., the segment YH starts at RWORK(LYH).
c Segments of RWORK (in order) are  YH, WM, EWT, SAVF, VSAV, ACOR.
c Within WM, LOCWP is the location of the WP work array,
c and within IWM, LOCIWP is the location of the IWP work array.
c-----------------------------------------------------------------------
   60 LYH = 21
      IF (ISTATE .EQ. 1) NYH = N
      LWM = LYH + (MAXORD + 1)*NYH
      IF (MITER .EQ. 0) LENWK = 0
      IF (MITER .EQ. 1) LENWK = N*(MAXL+2+min(1,MAXL-KMP)) + (MAXL+3)*
     &   MAXL + 1
      IF (MITER .EQ. 9) LENWK = 2*N
      LWP = 0
      IF (MITER .GE. 1) LWP = IWORK(1)
      LENWM = LENWK + LWP
      LOCWP = LENWK + 1
      LEWT = LWM + LENWM
      LSAVF = LEWT + N
      LVSAV = LSAVF + N
      LACOR = LVSAV + N
      IF (MITER .EQ. 0) LACOR = LVSAV
      LENRW = LACOR + N - 1
      IWORK(17) = LENRW
      LIWM = 31
      LENIWK = 0
      LIWP = 0
      IF (MITER .GE. 1) LIWP = IWORK(2)
      LENIW = 30 + LENIWK + LIWP
      LOCIWP = LENIWK + 1
      IWORK(18) = LENIW
      IF (LENRW .GT. LRW) GO TO 617
      IF (LENIW .GT. LIW) GO TO 618
c Check RTOL and ATOL for legality. ------------------------------------
      RTOLI = RTOL(1)
      ATOLI = ATOL(1)
      DO 70 I = 1, N
      IF (ITOL .GE. 3) RTOLI = RTOL(I)
      IF (ITOL .EQ. 2 .OR. ITOL .EQ. 4) ATOLI = ATOL(I)
      IF (RTOLI .LT. ZERO) GO TO 619
      IF (ATOLI .LT. ZERO) GO TO 620
   70 CONTINUE
c Load SQRT(N) and its reciprocal in common. ---------------------------
      SQRTN = SQRT(dble(N))
      RSQRTN = ONE/SQRTN
      IF (ISTATE .EQ. 1) GO TO 100
c If ISTATE = 3, set flag to signal parameter changes to VSTEP. --------
      JSTART = -1
      IF (NQ .LE. MAXORD) GO TO 100
c MAXORD was reduced below NQ.  Copy YH(*,MAXORD+2) into SAVF. ---------
      CALL dcopy_u(N, RWORK(LWM), 1, RWORK(LSAVF), 1)
c-----------------------------------------------------------------------
c Block C.
c The next block is for the initial call only (ISTATE = 1).
c It contains all remaining initializations, the initial call to F,
c and the calculation of the initial step size.
c The error weights in EWT are inverted after being loaded.
c-----------------------------------------------------------------------
  100 UROUND = R1MACH9(4)
      TN = T
      IF (ITASK .NE. 4 .AND. ITASK .NE. 5) GO TO 110
      TCRIT = RWORK(1)
      IF ((TCRIT - TOUT)*(TOUT - T) .LT. ZERO) GO TO 625
      IF (H0 .NE. ZERO .AND. (T + H0 - TCRIT)*H0 .GT. ZERO) H0 = TCRIT - 
     &   T
  110 JSTART = 0
      CCMXJ = PT2
      MSBJ = 50
      NHNIL = 0
      NST = 0
      NSLAST = 0
      HU = ZERO
      NQU = 0
      NPE = 0
      NLI0 = 0
      NNI0 = 0
      NCFN0 = 0
      NCFL0 = 0
      NWARN = 0
      NNI = 0
      NLI = 0
      NPS = 0
      NETF = 0
      NCFN = 0
      NCFL = 0
c Initial call to F.  (LF0 points to YH(*,2).) -------------------------
      LF0 = LYH + NYH
      IFAIL = 0
      CALL F (N, T, Y, RWORK(LF0), RPAR, IPAR, IFAIL)
      NFE = 1
      IF (IFAIL .NE. 0) THEN
      MSG = 'VODPK-- Initial call to F failed.       '
      CALL dxerrwv_u(MSG, 40, 251, 0, 0, 0, 0, 0, ZERO, ZERO)
      ISTATE = -8
      GO TO 580
      ENDIF
c Load the initial value vector in YH. ---------------------------------
      CALL dcopy_u(N, Y, 1, RWORK(LYH), 1)
c Load and invert the EWT array.  (H is temporarily set to 1.0.) -------
      NQ = 1
      H = ONE
      CALL dewset_u(N, ITOL, RTOL, ATOL, RWORK(LYH), RWORK(LEWT))
      DO 120 I = 1, N
      IF (RWORK(I+LEWT-1) .LE. ZERO) GO TO 621
  120 RWORK(I+LEWT-1) = ONE/RWORK(I+LEWT-1)
      IF (H0 .NE. ZERO) GO TO 180
c Call VHIN to set initial step size H0 to be attempted. ---------------
      CALL VHIN (N, T, RWORK(LYH), RWORK(LF0), F, RPAR, IPAR, TOUT, 
     &   UROUND, RWORK(LEWT), ITOL, ATOL, Y, RWORK(LACOR), H0, NITER, 
     &   IER)
      NFE = NFE + NITER
      IF (IER .EQ. -1) GO TO 622
      IF (IER .EQ. -2) THEN
      MSG = 'VODPK--  calls to F failed repeatedly in initial H calc.'
      CALL dxerrwv_u(MSG, 56, 251, 0, 0, 0, 0, 0, ZERO, ZERO)
      ISTATE = -8
      GO TO 580
      ENDIF
c Adjust H0 if necessary to meet HMAX bound. ---------------------------
  180 RH = ABS(H0)*HMXI
      IF (RH .GT. ONE) H0 = H0/RH
c Load H with H0 and scale YH(*,2) by H0. ------------------------------
      H = H0
      CALL dscal_u(N, H0, RWORK(LF0), 1)
      GO TO 270
c-----------------------------------------------------------------------
c Block D.
c The next code block is for continuation calls only (ISTATE = 2 or 3)
c and is to check stop conditions before taking a step.
c-----------------------------------------------------------------------
  200 NSLAST = NST
      KUTH = 0
      NLI0 = NLI
      NNI0 = NNI
      NCFN0 = NCFN
      NCFL0 = NCFL
      NWARN = 0
      GO TO (210, 250, 220, 230, 240), ITASK
  210 IF ((TN - TOUT)*H .LT. ZERO) GO TO 250
      CALL VINDY (TOUT, 0, RWORK(LYH), NYH, Y, IFLAG)
      IF (IFLAG .NE. 0) GO TO 627
      T = TOUT
      GO TO 420
  220 TP = TN - HU*(ONE + HUN*UROUND)
      IF ((TP - TOUT)*H .GT. ZERO) GO TO 623
      IF ((TN - TOUT)*H .LT. ZERO) GO TO 250
      GO TO 400
  230 TCRIT = RWORK(1)
      IF ((TN - TCRIT)*H .GT. ZERO) GO TO 624
      IF ((TCRIT - TOUT)*H .LT. ZERO) GO TO 625
      IF ((TN - TOUT)*H .LT. ZERO) GO TO 245
      CALL VINDY (TOUT, 0, RWORK(LYH), NYH, Y, IFLAG)
      IF (IFLAG .NE. 0) GO TO 627
      T = TOUT
      GO TO 420
  240 TCRIT = RWORK(1)
      IF ((TN - TCRIT)*H .GT. ZERO) GO TO 624
  245 HMX = ABS(TN) + ABS(H)
      IHIT = ABS(TN - TCRIT) .LE. HUN*UROUND*HMX
      IF (IHIT) GO TO 400
      TNEXT = TN + HNEW*(ONE + FOUR*UROUND)
      IF ((TNEXT - TCRIT)*H .LE. ZERO) GO TO 250
      H = (TCRIT - TN)*(ONE - FOUR*UROUND)
      KUTH = 1
c-----------------------------------------------------------------------
c Block E.
c The next block is normally executed for all calls and contains
c the call to the one-step core integrator VSTEP.
c
c This is a looping point for the integration steps.
c
c First check for too many steps being taken,
c check for poor Newton/Krylov performance, update EWT (if not at
c start of problem), check for too much accuracy being requested, and
c check for H below the roundoff level in T.
c-----------------------------------------------------------------------
  250 CONTINUE
      IF ((NST-NSLAST) .GE. MXSTEP) GO TO 500
      CALL dewset_u(N, ITOL, RTOL, ATOL, RWORK(LYH), RWORK(LEWT))
      NSTD = NST - NSLAST
      NNID = NNI - NNI0
      IF (NSTD .LT. 10 .OR. NNID .EQ. 0) GO TO 255
      AVDIM = dble(NLI - NLI0)/dble(NNID)
      RCFN = dble(NCFN - NCFN0)/dble(NSTD)
      RCFL = dble(NCFL - NCFL0)/dble(NNID)
      LAVD = AVDIM .GT. (dble(MAXL) - PT05)
      LCFN = RCFN .GT. PT9
      LCFL = RCFL .GT. PT9
      LWARN = LAVD .OR. LCFN .OR. LCFL
      IF (.NOT.LWARN) GO TO 255
      NWARN = NWARN + 1
      IF (NWARN .GT. 10) GO TO 255
      IF (LAVD) THEN
      MSG = 'VODPK-- Warning. Poor iterative algorithm performance   '
      CALL dxerrwv_u(MSG, 56, 111, 0, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      at T = R1. Average no. of linear iterations = R2  '
      CALL dxerrwv_u(MSG, 56, 111, 0, 0, 0, 0, 2, TN, AVDIM)
      ENDIF
      IF (LCFN) THEN
      MSG = 'VODPK-- Warning. Poor iterative algorithm performance   '
      CALL dxerrwv_u(MSG, 56, 112, 0, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      at T = R1. Nonlinear convergence failure rate = R2'
      CALL dxerrwv_u(MSG, 56, 112, 0, 0, 0, 0, 2, TN, RCFN)
      ENDIF
      IF (LCFL) THEN
      MSG = 'VODPK-- Warning. Poor iterative algorithm performance   '
      CALL dxerrwv_u(MSG, 56, 113, 0, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      at T = R1. Linear convergence failure rate = R2   '
      CALL dxerrwv_u(MSG, 56, 113, 0, 0, 0, 0, 2, TN, RCFL)
      ENDIF
  255 CONTINUE
      DO 260 I = 1, N
      IF (RWORK(I+LEWT-1) .LE. ZERO) GO TO 510
  260 RWORK(I+LEWT-1) = ONE/RWORK(I+LEWT-1)
  270 TOLSF = UROUND*VNORML (N, RWORK(LYH), RWORK(LEWT))
      IF (TOLSF .LE. ONE) GO TO 280
      TOLSF = TOLSF*TWO
      IF (NST .EQ. 0) GO TO 626
      GO TO 520
  280 IF ((TN + H) .NE. TN) GO TO 290
      NHNIL = NHNIL + 1
      IF (NHNIL .GT. MXHNIL) GO TO 290
      MSG = 'VODPK--  Warning..internal T (=R1) and H (=R2) are'
      CALL dxerrwv_u(MSG, 50, 101, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG='      such that in the machine, T + H = T on the next step  '
      CALL dxerrwv_u(MSG, 60, 101, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      (H = step size). solver will continue anyway'
      CALL dxerrwv_u(MSG, 50, 101, 1, 0, 0, 0, 2, TN, H)
      IF (NHNIL .LT. MXHNIL) GO TO 290
      MSG = 'VODPK--  Above warning has been issued I1 times.  '
      CALL dxerrwv_u(MSG, 50, 102, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      it will not be issued again for this problem'
      CALL dxerrwv_u(MSG, 50, 102, 1, 1, MXHNIL, 0, 0, ZERO, ZERO)
  290 CONTINUE
c-----------------------------------------------------------------------
c  CALL VSTEP (Y, YH, NYH, YH, EWT, SAVF, VSAV, ACOR, WM, IWM,
c                                     F, JAC, PSOL, VNLSK, RPAR, IPAR)
c-----------------------------------------------------------------------
      CALL VSTEP (Y, RWORK(LYH), NYH, RWORK(LYH), RWORK(LEWT), RWORK(
     &   LSAVF), RWORK(LVSAV), RWORK(LACOR), RWORK(LWM), IWORK(LIWM), F, 
     &   JAC, PSOL, VNLSK, RPAR, IPAR)
      KGO = 1 - KFLAG
      GO TO (300, 530, 540, 550, 552, 555), KGO
c-----------------------------------------------------------------------
c Block F.
c The following block handles the case of a successful return from the
c core integrator (KFLAG = 0).  Test for stop conditions.
c-----------------------------------------------------------------------
  300 INIT = 1
      KUTH = 0
      GO TO (310, 400, 330, 340, 350), ITASK
c ITASK = 1.  if TOUT has been reached, interpolate. -------------------
  310 IF ((TN - TOUT)*H .LT. ZERO) GO TO 250
      CALL VINDY (TOUT, 0, RWORK(LYH), NYH, Y, IFLAG)
      T = TOUT
      GO TO 420
c ITASK = 3.  Jump to exit if TOUT was reached. ------------------------
  330 IF ((TN - TOUT)*H .GE. ZERO) GO TO 400
      GO TO 250
c ITASK = 4.  See if TOUT or TCRIT was reached.  Adjust H if necessary.
  340 IF ((TN - TOUT)*H .LT. ZERO) GO TO 345
      CALL VINDY (TOUT, 0, RWORK(LYH), NYH, Y, IFLAG)
      T = TOUT
      GO TO 420
  345 HMX = ABS(TN) + ABS(H)
      IHIT = ABS(TN - TCRIT) .LE. HUN*UROUND*HMX
      IF (IHIT) GO TO 400
      TNEXT = TN + H*(ONE + FOUR*UROUND)
      IF ((TNEXT - TCRIT)*H .LE. ZERO) GO TO 250
      H = (TCRIT - TN)*(ONE - FOUR*UROUND)
      KUTH = 1
      GO TO 250
c ITASK = 5.  See if TCRIT was reached and jump to exit. ---------------
  350 HMX = ABS(TN) + ABS(H)
      IHIT = ABS(TN - TCRIT) .LE. HUN*UROUND*HMX
c-----------------------------------------------------------------------
c Block G.
c The following block handles all successful returns from VODPK.
c If ITASK .ne. 1, Y is loaded from YH and T is set accordingly.
c ISTATE is set to 2, and the optional outputs are loaded into the
c work arrays before returning.
c-----------------------------------------------------------------------
  400 CONTINUE
      CALL dcopy_u(N, RWORK(LYH), 1, Y, 1)
      T = TN
      IF (ITASK .NE. 4 .AND. ITASK .NE. 5) GO TO 420
      IF (IHIT) T = TCRIT
  420 ISTATE = 2
      RWORK(11) = HU
      RWORK(12) = H
      RWORK(13) = TN
      IWORK(11) = NST
      IWORK(12) = NFE
      IWORK(13) = NPE
      IWORK(14) = NQU
      IWORK(15) = NQ
      IWORK(20) = NNI
      IWORK(21) = NCFN
      IWORK(22) = NETF
      IWORK(23) = NLI
      IWORK(24) = NPS
      IWORK(25) = NCFL
      RETURN
c-----------------------------------------------------------------------
c Block H.
c The following block handles all unsuccessful returns other than
c those for illegal input.  First the error message routine is called.
c if there was an error test or convergence test failure, IMXER is set.
c Then Y is loaded from YH, and T is set to TN.  The optional outputs
c are loaded into the work arrays before returning.
c-----------------------------------------------------------------------
c The maximum number of steps was taken before reaching TOUT. ----------
  500 MSG = 'VODPK--  At current T (=R1), MXSTEP (=I1) steps   '
      CALL dxerrwv_u(MSG, 50, 201, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      taken on this call before reaching TOUT     '
      CALL dxerrwv_u(MSG, 50, 201, 1, 1, MXSTEP, 0, 1, TN, ZERO)
      ISTATE = -1
      GO TO 580
c EWT(i) .le. 0.0 for some i (not at start of problem). ----------------
  510 EWTI = RWORK(LEWT+I-1)
      MSG = 'VODPK--  At T (=R1), EWT(I1) has become R2 .le. 0.'
      CALL dxerrwv_u(MSG, 50, 202, 1, 1, I, 0, 2, TN, EWTI)
      ISTATE = -6
      GO TO 580
c Too much accuracy requested for machine precision. -------------------
  520 MSG = 'VODPK--  At T (=R1), too much accuracy requested  '
      CALL dxerrwv_u(MSG, 50, 203, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      for precision of machine..  See TOLSF (=R2) '
      CALL dxerrwv_u(MSG, 50, 203, 1, 0, 0, 0, 2, TN, TOLSF)
      RWORK(14) = TOLSF
      ISTATE = -2
      GO TO 580
c KFLAG = -1.  Error test failed repeatedly or with ABS(H) = HMIN. -----
  530 MSG = 'VODPK--  At T(=R1) and step size H(=R2), the error'
      CALL dxerrwv_u(MSG, 50, 204, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      test failed repeatedly or with abs(H) = HMIN'
      CALL dxerrwv_u(MSG, 50, 204, 1, 0, 0, 0, 2, TN, H)
      ISTATE = -4
      GO TO 560
c KFLAG = -2.  Convergence failed repeatedly or with abs(H) = HMIN. ----
  540 MSG = 'VODPK--  At T (=R1) and step size H (=R2), the    '
      CALL dxerrwv_u(MSG, 50, 205, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      corrector convergence failed repeatedly     '
      CALL dxerrwv_u(MSG, 50, 205, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      or with abs(H) = HMIN   '
      CALL dxerrwv_u(MSG, 30, 205, 1, 0, 0, 0, 2, TN, H)
      ISTATE = -5
      GO TO 560
c KFLAG = -3.  Unrecoverable error from JAC. ---------------------------
  550 MSG = 'VODPK--  at T (=R1) an unrecoverable error return '
      CALL dxerrwv_u(MSG, 50, 206, 0, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      was made from subroutine JAC      '
      CALL dxerrwv_u(MSG, 40, 206, 0, 0, 0, 0, 1, TN, ZERO)
      ISTATE = -7
      GO TO 580
c KFLAG = -4.  Unrecoverable error from PSOL. --------------------------
  552 MSG = 'VODPK--  at T (=R1) an unrecoverable error return '
      CALL dxerrwv_u(MSG, 50, 207, 0, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      was made from subroutine PSOL     '
      CALL dxerrwv_u(MSG, 40, 207, 0, 0, 0, 0, 1, TN, ZERO)
      ISTATE = -7
      GO TO 580
c KFLAG = -5.  F returned IFAIL .ne. 0 repeatedly in corrector loop. ---
  555 MSG = 'VODPK--  at T (=R1) and step size H (=R2), F      '
      CALL dxerrwv_u(MSG, 50, 208, 0, 0, 0, 0, 0, ZERO, ZERO)
      MSG = '      failed repeatedly in the corrector loop.    '
      CALL dxerrwv_u(MSG, 50, 208, 0, 0, 0, 0, 2, TN, H)
      ISTATE = -8
      GO TO 580
c Compute IMXER if relevant. -------------------------------------------
  560 BIG = ZERO
      IMXER = 1
      DO 570 I = 1, N
      SIZE = ABS(RWORK(I+LACOR-1)*RWORK(I+LEWT-1))
      IF (BIG .GE. SIZE) GO TO 570
      BIG = SIZE
      IMXER = I
  570 CONTINUE
      IWORK(16) = IMXER
c Set Y vector, T, and optional outputs. -------------------------------
  580 CONTINUE
      CALL dcopy_u(N, RWORK(LYH), 1, Y, 1)
      T = TN
      RWORK(11) = HU
      RWORK(12) = H
      RWORK(13) = TN
      IWORK(11) = NST
      IWORK(12) = NFE
      IWORK(13) = NPE
      IWORK(14) = NQU
      IWORK(15) = NQ
      IWORK(20) = NNI
      IWORK(21) = NCFN
      IWORK(22) = NETF
      IWORK(23) = NLI
      IWORK(24) = NPS
      IWORK(25) = NCFL
      RETURN
c-----------------------------------------------------------------------
c Block I.
c The following block handles all error returns due to illegal input
c (ISTATE = -3), as detected before calling the core integrator.
c Call the error message routine and then return.
c-----------------------------------------------------------------------
  601 MSG = 'VODPK--  ISTATE (=I1) illegal '
      CALL dxerrwv_u(MSG, 30, 1, 1, 1, ISTATE, 0, 0, ZERO, ZERO)
      IF (ISTATE .LT. 0) GO TO 800
      GO TO 700
  602 MSG = 'VODPK--  ITASK (=I1) illegal  '
      CALL dxerrwv_u(MSG, 30, 2, 1, 1, ITASK, 0, 0, ZERO, ZERO)
      GO TO 700
  603 MSG='VODPK--   ISTATE (=I1) .gt. 1 but VODPK not initialized     '
      CALL dxerrwv_u(MSG, 60, 3, 1, 1, ISTATE, 0, 0, ZERO, ZERO)
      GO TO 700
  604 MSG = 'VODPK--  NEQ (=I1) .lt. 1     '
      CALL dxerrwv_u(MSG, 30, 4, 1, 1, NEQ, 0, 0, ZERO, ZERO)
      GO TO 700
  605 MSG = 'VODPK--  ISTATE = 3 and NEQ increased (I1 to I2)  '
      CALL dxerrwv_u(MSG, 50, 5, 1, 2, N, NEQ, 0, ZERO, ZERO)
      GO TO 700
  606 MSG = 'VODPK--  ITOL (=I1) illegal   '
      CALL dxerrwv_u(MSG, 30, 6, 1, 1, ITOL, 0, 0, ZERO, ZERO)
      GO TO 700
  607 MSG = 'VODPK--  IOPT (=I1) illegal   '
      CALL dxerrwv_u(MSG, 30, 7, 1, 1, IOPT, 0, 0, ZERO, ZERO)
      GO TO 700
  608 MSG = 'VODPK--  MF (=I1) illegal     '
      CALL dxerrwv_u(MSG, 30, 8, 1, 1, MF, 0, 0, ZERO, ZERO)
      GO TO 700
  611 MSG = 'VODPK--  MAXORD (=I1) .lt. 0  '
      CALL dxerrwv_u(MSG, 30, 11, 1, 1, MAXORD, 0, 0, ZERO, ZERO)
      GO TO 700
  612 MSG = 'VODPK--  MXSTEP (=I1) .lt. 0  '
      CALL dxerrwv_u(MSG, 30, 12, 1, 1, MXSTEP, 0, 0, ZERO, ZERO)
      GO TO 700
  613 MSG = 'VODPK--  MXHNIL (=I1) .lt. 0  '
      CALL dxerrwv_u(MSG, 30, 13, 1, 1, MXHNIL, 0, 0, ZERO, ZERO)
      GO TO 700
  614 MSG = 'VODPK--  TOUT (=R1) behind T (=R2)      '
      CALL dxerrwv_u(MSG, 40, 14, 1, 0, 0, 0, 2, TOUT, T)
      MSG = '      integration direction is given by H0 (=R1)  '
      CALL dxerrwv_u(MSG, 50, 14, 1, 0, 0, 0, 1, H0, ZERO)
      GO TO 700
  615 MSG = 'VODPK--  HMAX (=R1) .lt. 0.0  '
      CALL dxerrwv_u(MSG, 30, 15, 1, 0, 0, 0, 1, HMAX, ZERO)
      GO TO 700
  616 MSG = 'VODPK--  HMIN (=R1) .lt. 0.0  '
      CALL dxerrwv_u(MSG, 30, 16, 1, 0, 0, 0, 1, HMIN, ZERO)
      GO TO 700
  617 CONTINUE
      MSG='VODPK--  RWORK length needed, LENRW (=I1), exceeds LRW (=I2)'
      CALL dxerrwv_u(MSG, 60, 17, 1, 2, LENRW, LRW, 0, ZERO, ZERO)
      GO TO 700
  618 CONTINUE
      MSG='VODPK--  IWORK length needed, LENIW (=I1), exceeds LIW (=I2)'
      CALL dxerrwv_u(MSG, 60, 18, 1, 2, LENIW, LIW, 0, ZERO, ZERO)
      GO TO 700
  619 MSG = 'VODPK--  RTOL(I1) is R1 .lt. 0.0        '
      CALL dxerrwv_u(MSG, 40, 19, 1, 1, I, 0, 1, RTOLI, ZERO)
      GO TO 700
  620 MSG = 'VODPK--  ATOL(I1) is R1 .lt. 0.0        '
      CALL dxerrwv_u(MSG, 40, 20, 1, 1, I, 0, 1, ATOLI, ZERO)
      GO TO 700
  621 EWTI = RWORK(LEWT+I-1)
      MSG = 'VODPK--  EWT(I1) is R1 .le. 0.0         '
      CALL dxerrwv_u(MSG, 40, 21, 1, 1, I, 0, 1, EWTI, ZERO)
      GO TO 700
  622 CONTINUE
      MSG='VODPK--  TOUT (=R1) too close to T(=R2) to start integration'
      CALL dxerrwv_u(MSG, 60, 22, 1, 0, 0, 0, 2, TOUT, T)
      GO TO 700
  623 CONTINUE
      MSG='VODPK--  ITASK = I1 and TOUT (=R1) behind TCUR - HU (= R2)  '
      CALL dxerrwv_u(MSG, 60, 23, 1, 1, ITASK, 0, 2, TOUT, TP)
      GO TO 700
  624 CONTINUE
      MSG='VODPK--  ITASK = 4 or 5 and TCRIT (=R1) behind TCUR (=R2)   '
      CALL dxerrwv_u(MSG, 60, 24, 1, 0, 0, 0, 2, TCRIT, TN)
      GO TO 700
  625 CONTINUE
      MSG='VODPK--  ITASK = 4 or 5 and TCRIT (=R1) behind TOUT (=R2)   '
      CALL dxerrwv_u(MSG, 60, 25, 1, 0, 0, 0, 2, TCRIT, TOUT)
      GO TO 700
  626 MSG = 'VODPK--  At start of problem, too much accuracy   '
      CALL dxerrwv_u(MSG, 50, 26, 1, 0, 0, 0, 0, ZERO, ZERO)
      MSG='      requested for precision of machine..  See TOLSF (=R1) '
      CALL dxerrwv_u(MSG, 60, 26, 1, 0, 0, 0, 1, TOLSF, ZERO)
      RWORK(14) = TOLSF
      GO TO 700
  627 MSG = 'VODPK--  Trouble from VINDY. ITASK = I1, TOUT = R1'
      CALL dxerrwv_u(MSG, 50, 27, 1, 1, ITASK, 0, 1, TOUT, ZERO)
c
  700 CONTINUE
      ISTATE = -3
      RETURN
c
  800 MSG = 'VODPK--  Run aborted.. apparent infinite loop     '
ccc      CALL XERRWV (MSG, 50, 303, 2, 0, 0, 0, 0, ZERO, ZERO)
      call xerrab('*** PROBABLY YOU NEED TO SET ts = 0. AND istate = 1')
      RETURN
c----------------------- End of Subroutine VODPK -----------------------
      END
      SUBROUTINE VNLSK (Y, YH, LDYH, VSAV, SAVF, EWT, ACOR, IWM, WM, F, 
     &   JAC, PSOL, NFLAG, RPAR, IPAR)
c
      EXTERNAL F, JAC, PSOL
      doubleprecision Y, YH, VSAV, SAVF, EWT, ACOR, WM, RPAR
      INTEGER IWM, LDYH, NFLAG, IPAR
      DIMENSION Y(*), YH(LDYH, *), SAVF(*), VSAV(*), EWT(*), ACOR(*), 
     &   IWM(*), WM(*), RPAR(*), IPAR(*)
c-----------------------------------------------------------------------
c Call sequence input -- YH, LDYH, F, JAC, EWT, ACOR, IWM, WM,
c                        NFLAG, RPAR, IPAR
c Call sequence output -- Y, YH, VSAV, SAVF, ACOR, IWM, WM, NFLAG
c COMMON block variables accessed..
c        /VOD001/  ACNRM, CRATE, DRC, H, ICF, IPUP, JCUR, JSTART,
c                  METH, MITER, N, NSLP, RC, RL1, TN, TQ
c        /VOD002/  NFE, NNI, NPE, NST
c        /VPK001/  JACFLG, LOCIWP, LOCWP, MNEWT
c Subroutines called.. F, JAC, PSOL, SAXPY, SCOPY, SSCAL, VSOLPK
c Function subroutines called.. VNORML
c-----------------------------------------------------------------------
c Subroutine VNLSK is a nonlinear system solver, which uses either
c functional iteration (MITER = 0), or a combination of an inexact
c Newton method and preconditioned Krylov iteration (MITER .gt. 0)
c to solve the implicit system for the corrector y vector.
c It calls Subroutine JAC (user-supplied) for preprocessing the
c preconditioner, and Subroutine VSOLPK for the Krylov iteration.
c
c In addition to variables described elsewhere, communication with
c VNLSK uses the following variables..
c
c Y          = The dependent variable, a vector of length N, input.
c YH         = The Nordsieck (Taylor) array, LDYH by LMAX, input
c              and output.  On input, it contains predicted values.
c LDYH       = A constant .ge. N, the first dimension of YH, input.
c VSAV       = A work array of length N.
c SAVF       = A work array of length N.
c EWT        = An error weight vector of length N, input.
c ACOR       = A work array of length N, used for the accumulated
c              corrections to the predicted y vector.
c WM,IWM     = Real and integer work arrays associated with matrix
c              operations in Newton iteration (MITER .ne. 0).
c F          = Dummy name for user-supplied routine for f.
c JAC        = Dummy name for user-supplied routine for Jacobian data
c              and associated preconditioner matrix.
c PSOL       = Dummy name for user-supplied subroutine to solve
c              preconditioner linear system.
c NFLAG      = Input/output flag, with values and meanings as follows..
c              INPUT
c                  0 first call for this time step.
c                 -1 convergence failure in previous call to VNLSK.
c                 -2 error test failure in VSTEP.
c              OUTPUT
c                  0 successful completion of nonlinear solver.
c                 -1 convergence failure or failure in JAC.
c                 -2 unrecoverable error in matrix preprocessing
c                    (cannot occur here).
c                 -3 unrecoverable error in PSOL.
c                 -4 IFAIL .ne. 0 from F repeatedly.
c RPAR, IPAR = Dummy names for user's real and integer work arrays.
c
c IPUP       = Own variable flag with values and meanings as follows..
c              0,            do not update preconditioner.
c              MITER .ne. 0, update the preconditioner, because it is
c                            the initial step, user input changed,
c                            there was an error test failure, or an
c                            update is indicated by a change in the
c                            scalar RC or step counter NST.
c
c For more details, see comments in driver subroutine.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for labeled COMMON block VOD002 --------------------
c
      doubleprecision HU
      INTEGER NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
c
c Type declarations for labeled COMMON block VPK001 --------------------
c
      doubleprecision DELT, SQRTN, RSQRTN
      INTEGER JPRE, JACFLG, LOCWP, LOCIWP, LVSAV, KMP, MAXL, MNEWT, NLI, 
     &   NPS, NCFL
c
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
      COMMON /VOD002/ HU, NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
      COMMON /VPK001/ DELT, SQRTN, RSQRTN, JPRE, JACFLG, LOCIWP, LOCWP, 
     &   LVSAV, KMP, MAXL, MNEWT, NLI, NPS, NCFL
c
c     Special scaling factor for Newton iteration error TDR 11/19/93
      doubleprecision EFACN
      COMMON /TDR1/ EFACN
c
c
c Type declarations for local variables --------------------------------
c
      doubleprecision CCMAX, CRDOWN, CSCALE, DEL, DCON, DELP, HRL1,RDIV
      doubleprecision ONE, TWO, ZERO
      INTEGER I, IERPJ, IERSL, M, MAXCOR, MSBP, IFAIL
c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision VNORML
c-----------------------------------------------------------------------
c The following Fortran-77 declarations are to cause the values of the
c listed (local) variables to be saved between calls to VODPK.
      SAVE CCMAX, CRDOWN, MAXCOR, MSBP, RDIV
      SAVE ONE, TWO, ZERO
c-----------------------------------------------------------------------
      DATA CCMAX /0.3d0/, CRDOWN /0.3d0/, MAXCOR /3/, MSBP /20/, RDIV /
     &   2.0d0/
      DATA ONE /1.0d0/, TWO /2.0d0/, ZERO /0.0d0/
c-----------------------------------------------------------------------
c Up to MAXCOR corrector iterations are taken.  A convergence test is
c made on the RMS norm of each correction, weighted by the error
c weight vector EWT.  The sum of the corrections is accumulated in the
c vector ACOR(*).  The YH array is not altered in the corrector loop.
c-----------------------------------------------------------------------
      IF (JSTART .EQ. 0) NSLP = 0
      IF (NFLAG .EQ. 0) ICF = 0
      IF (NFLAG .EQ. -2) IPUP = MITER
      IF ( (JSTART .EQ. 0) .OR. (JSTART .EQ. -1) ) IPUP = MITER
      IF (JACFLG .EQ. 0) THEN
      IPUP = 0
      CRATE = ONE
      GO TO 220
      ENDIF
      DRC = ABS(RC-ONE)
      IF (DRC .GT. CCMAX .OR. NST .GE. NSLP+MSBP) IPUP = MITER
  220 M = 0
      HRL1 = H*RL1
      DELP = ZERO
      MNEWT = 0
      CALL dcopy_u(N, YH(1,1), 1, Y, 1 )
      IFAIL = 0
      CALL F (N, TN, Y, SAVF, RPAR, IPAR, IFAIL)
      NFE = NFE + 1
      IF (IFAIL .NE. 0) GO TO 420
      IF (IPUP .LE. 0) GO TO 250
c-----------------------------------------------------------------------
c If indicated, the preconditioner matrix is reevaluated and
c preprocessed before starting the corrector iteration.  IPUP is set
c to 0 as an indicator that this has been done.
c-----------------------------------------------------------------------
      JCUR = 1
      IERPJ = 0
      CALL JAC (F, N, TN, Y, YH, EWT, SAVF, ACOR, HRL1, WM(LOCWP), IWM(
     &   LOCIWP), IERPJ, RPAR, IPAR)
      NPE = NPE + 1
      IPUP = 0
      RC = ONE
      DRC = ZERO
      CRATE = ONE
      NSLP = NST
      IF (IERPJ .NE. 0) GO TO 420
  250 DO 260 I = 1, N
  260 ACOR(I) = ZERO
  270 IF (MITER .NE. 0) GO TO 350
c-----------------------------------------------------------------------
c In the case of functional iteration, update Y directly from
c the result of the last function evaluation.
c-----------------------------------------------------------------------
      DO 290 I = 1, N
      SAVF(I) = RL1*(H*SAVF(I) - YH(I,2))
  290 Y(I) = SAVF(I) - ACOR(I)
      DEL = VNORML (N, Y, EWT)
      DO 300 I = 1, N
  300 Y(I) = YH(I,1) + SAVF(I)
      CALL dcopy_u(N, SAVF, 1, ACOR, 1)
      GO TO 400
c-----------------------------------------------------------------------
c In the case of the Newton method, compute the corrector error,
c and solve the linear system with that as right-hand side and
c A as coefficient matrix.  The correction is scaled by the factor
c 2/(1+RC) to account for changes in H*RL1 since the last JAC call.
c-----------------------------------------------------------------------
  350 DO 360 I = 1, N
  360 VSAV(I) = HRL1*SAVF(I) - (RL1*YH(I,2) + ACOR(I))
      CALL VSOLPK (Y, SAVF, VSAV, EWT, WM, IWM, F, PSOL, IERSL, RPAR, 
     &   IPAR)
      NNI = NNI + 1
      IF (METH .EQ. 2 .AND. JACFLG .EQ. 1 .AND. MITER .EQ. 9 .AND. RC 
     &   .NE. ONE) THEN
      CSCALE = TWO/(ONE + RC)
      CALL dscal_u(N, CSCALE, VSAV, 1)
      ENDIF
      IF (IERSL .LT. 0) GO TO 440
      IF (IERSL .GT. 0) GO TO 410
      DEL = VNORML (N, VSAV, EWT)
      CALL daxpy_u(N, ONE, VSAV, 1, ACOR, 1)
      DO 380 I = 1, N
  380 Y(I) = YH(I,1) + ACOR(I)
c-----------------------------------------------------------------------
c Test for convergence.  If M.gt.0, an estimate of the convergence
c rate constant is stored in CRATE, and this is used in the test.
c-----------------------------------------------------------------------
  400 IF (M .NE. 0) CRATE = max(CRDOWN*CRATE,DEL/DELP)
      DCON = DEL*min(ONE,CRATE)/TQ(4)
      IF (DCON .LE. ONE*EFACN) GO TO 450
      M = M + 1
      IF (M .EQ. MAXCOR) GO TO 410
      IF (M .GE. 2 .AND. DEL .GT. RDIV*DELP) GO TO 410
      MNEWT = M
      DELP = DEL
      IFAIL = 0
      CALL F (N, TN, Y, SAVF, RPAR, IPAR, IFAIL)
      NFE = NFE + 1
      IF (IFAIL .EQ. 0) GO TO 270
c
  410 IF (MITER .EQ. 0 .OR. JCUR .EQ. 1 .OR. JACFLG .EQ. 0) GO TO 420
      ICF = 1
      IPUP = MITER
      GO TO 220
c
  420 CONTINUE
      ICF = 2
      NFLAG = -1
      RETURN
  440 CONTINUE
      NFLAG = -3
      RETURN
c Return for successful step. ------------------------------------------
  450 NFLAG = 0
      JCUR = 0
      ICF = 0
      IF (M .EQ. 0) ACNRM = DEL
      IF (M .GT. 0) ACNRM = VNORML (N, ACOR, EWT)
      RETURN
c----------------------- End of Subroutine VNLSK -----------------------
      END
      SUBROUTINE VSOLPK (Y, SAVF, X, EWT, WM, IWM, F, PSOL, IERSL, RPAR, 
     &   IPAR)
      EXTERNAL F, PSOL
      doubleprecision Y, SAVF, X, EWT, WM, RPAR
      INTEGER IWM, IERSL, IPAR
      DIMENSION Y(*), SAVF(*), X(*), EWT(*), WM(*), IWM(*), RPAR(*), 
     &   IPAR(*)
c-----------------------------------------------------------------------
c Call sequence input -- Y, SAVF, X, EWT, F, PSOL, RPAR, IPAR
c Call sequence output -- Y, SAVF, X, WM, IWM, IERSL
c COMMON block variables accessed..
c        /VOD001/  H, RL1, TQ, TN, MITER, N
c        /VPK001/  DELT, SQRTN, RSQRTN, JPRE, LOCIWP, LOCWP,
c                  KMP, MAXL, MNEWT, NLI, NPS, NCFL
c Subroutines called.. F, PSOL, SCOPY, SSCAL, VSPIG, VUSOL
c-----------------------------------------------------------------------
c This routine interfaces with  VSPIG  or  VUSOL  for the solution of
c the linear system arising from a Newton iteration (MITER .ne. 0).
c
c In addition to variables described elsewhere, communication with
c VSOLPK uses the following variables..
c WM    = real work space containing data for the algorithm
c         (Krylov basis vectors, Hessenberg matrix, etc.)
c IWM   = integer work space containing data for the algorithm
c X     = the right-hand side vector on input, and the solution vector
c         on output, of length N.
c IERSL = output flag (in COMMON)..
c         IERSL =  0 means no trouble occurred.
c         IERSL =  1 means the iterative method failed to converge.
c                    If the preconditioner is out of date, the step
c                    is repeated with a new preconditioner.  Otherwise,
c                    the stepsize is reduced (forcing a new evalua-
c                    tion of the preconditioner) and the step is
c                    repeated.
c         IERSL = -1 means there was a nonrecoverable error in the
c                    iterative solver.  The stepsize is reduced in
c                    VSTEP and the step is repeated.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for labeled COMMON block VPK001 --------------------
c
      doubleprecision DELT, SQRTN, RSQRTN
      INTEGER JPRE, JACFLG, LOCWP, LOCIWP, LVSAV, KMP, MAXL, MNEWT, NLI, 
     &   NPS, NCFL
c
c Type declarations for local variables --------------------------------
c
      doubleprecision DELTA, HRL1
      INTEGER IFLAG, LB, LDL, LGMR, LHES, LQ, LV, LWK, MAXLP1, NPSL
c-----------------------------------------------------------------------
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
      COMMON /VPK001/ DELT, SQRTN, RSQRTN, JPRE, JACFLG, LOCIWP, LOCWP, 
     &   LVSAV, KMP, MAXL, MNEWT, NLI, NPS, NCFL
c-----------------------------------------------------------------------
c
      IERSL = 0
      HRL1 = H*RL1
      DELTA = DELT*TQ(4)
      IF (MITER .EQ. 1) THEN
c-----------------------------------------------------------------------
c Use the VSPIG algorithm to solve the linear system A*x = -f.
c-----------------------------------------------------------------------
      MAXLP1 = MAXL + 1
      LV = 1
      LB = LV + N*MAXL
      LHES = LB + N + 1
      LQ = LHES + MAXL*MAXLP1
      LWK = LQ + 2*MAXL
      LDL = LWK + min(1,MAXL-KMP)*N
      CALL dcopy_u(N, X, 1, WM(LB), 1)
      CALL dscal_u(N, RSQRTN, EWT, 1)
      CALL VSPIG (TN, Y, SAVF, WM(LB), EWT, N, MAXL, MAXLP1, KMP, DELTA, 
     &   HRL1, JPRE, MNEWT, F, PSOL, NPSL, X, WM(LV), WM(LHES), WM(LQ), 
     &   LGMR, WM(LOCWP), IWM(LOCIWP), WM(LWK), WM(LDL), RPAR, IPAR, 
     &   IFLAG)
      NLI = NLI + LGMR
      NPS = NPS + NPSL
      CALL dscal_u(N, SQRTN, EWT, 1)
      IF (IFLAG .NE. 0) NCFL = NCFL + 1
      IF (IFLAG .GE. 2) IERSL = 1
      IF (IFLAG .LT. 0) IERSL = -1
      RETURN
      ELSE IF (MITER .EQ. 9) THEN
c-----------------------------------------------------------------------
c Use VUSOL, which interfaces to PSOL, to solve the linear system
c (No Krylov iteration).
c-----------------------------------------------------------------------
      LB = 1
      LWK = LB + N
      CALL dcopy_u(N, X, 1, WM(LB), 1)
      CALL VUSOL (N, TN, Y, SAVF, WM(LB), EWT, DELTA, HRL1, JPRE, MNEWT, 
     &   PSOL, NPSL, X, WM(LOCWP), IWM(LOCIWP), WM(LWK), RPAR, IPAR, 
     &   IFLAG)
      NPS = NPS + NPSL
      IF (IFLAG .NE. 0) NCFL = NCFL + 1
      IF (IFLAG .EQ. 3) IERSL = 1
      IF (IFLAG .LT. 0) IERSL = -1
      RETURN
      ENDIF
c----------------------- End of Subroutine VSOLPK ----------------------
      END
      SUBROUTINE VSPIG (TN, Y, SAVF, B, WGHT, N, MAXL, MAXLP1, KMP, 
     &   DELTA, HB0, JPRE, MNEWT, F, PSOL, NPSL, X, V, HES, Q, LGMR, WP, 
     &   IWP, WK, DL, RPAR, IPAR, IFLAG)
      EXTERNAL F, PSOL
      doubleprecision TN, Y, SAVF, B, WGHT, DELTA, HB0, X, V, HES, Q, WP
     &   , WK, DL, RPAR
      INTEGER N, MAXL, MAXLP1, KMP, JPRE, MNEWT, NPSL, LGMR, IWP, IFLAG, 
     &   IPAR
      DIMENSION Y(*), SAVF(*), B(*), WGHT(*), X(*), V(N,*), HES(MAXLP1,*
     &   ), Q(*), WP(*), IWP(*), WK(*), DL(*), RPAR(*), IPAR(*)
c-----------------------------------------------------------------------
c Call sequence input --  TN, Y, SAVF, B, WGHT, N, MAXL, MAXLP1, DELTA,
c                         HB0, JPRE, MNEWT, F, PSOL, RPAR, IPAR
c Call sequence output -- B, KMP, DELTA, NPSL, X, V, HES, Q, LGMR, WP,
c                         IWP, WK, DL, RPAR, IPAR, IFLAG
c COMMON block variables accessed.. None
c Subroutines called.. F, SVRORTHOG, PSOL, SAXPY, SCOPY, SHELS, SHEQR,
c                      SSCAL, VATV
c Function subroutines called.. SNRM2
c-----------------------------------------------------------------------
c This routine solves the linear system  A * x = b using SPIGMR,
c a scaled preconditioned incomplete version of the generalized
c minimum residual method GMRES.
c An initial guess of x = 0 is assumed.
c-----------------------------------------------------------------------
c
c      On entry
c
c          NEQ = problem size, passed to F and PSOL (NEQ(1) = N).
c
c           TN = current value of t.
c
c            Y = array containing current dependent variable vector.
c
c         SAVF = array containing current value of f(t,y).
c
c            B = the right hand side of the system A*x = b.
c                B is also used as work space when computing
c                the final approximation.
c                (B is the same as V(*,MAXL+1) in the call to VSPIG.)
c
c         WGHT = the vector of length N containing the nonzero
c                elements of the diagonal scaling matrix.
c
c            N = the order of the matrix A, and the lengths
c                of the vectors WGHT, B and X.
c
c         MAXL = the maximum allowable order of the matrix H.
c
c       MAXLP1 = MAXL + 1, used for dynamic dimensioning of HES .
c
c          KMP = the number of previous vectors the new vector VNEW
c                must be made orthogonal to.  KMP .le. MAXL.
c
c        DELTA = tolerance on residuals  b - A*x  in weighted RMS norm.
c
c          HB0 = current value of (step size h) * (coefficient beta0).
c
c         JPRE = preconditioner type flag.
c
c        MNEWT = Newton iteration counter (.ge. 0).
c
c           WK = real work array used by routine VATV and PSOL.
c
c           DL = real work array used for calculation of the residual
c                norm rho when the method is incomplete (KMP.lt.MAXL).
c
c           WP = real work array used by preconditioner PSOL.
c
c          IWP = integer work array used by preconditioner PSOL.
c
c      On return
c
c         X    = the final computed approximation to the solution
c                of the system A*x = b.
c
c         LGMR = the number of iterations performed and
c                the current order of the upper Hessenberg
c                matrix HES .
c
c         NPSL = the number of calls to PSOL.
c
c         V    = the N by (LGMR+1) array containing the LGMR
c                orthogonal vectors V(*,1) to V(*,LGMR).
c
c         HES  = the upper triangular factor of the QR decomposition
c                of the (LGMR+1) by LGMR upper Hessenberg matrix whose
c                entries are the scaled inner-products of A*V(*,i)
c                and V(*,k).
c
c         Q    = real array of length 2*MAXL containing the components
c                of the Givens rotations used in the QR decomposition
c                of HES.  It is loaded in SHEQR and used in SHELS.
c
c        IFLAG = integer error flag..
c                0 means convergence in LGMR iterations, LGMR.le.MAXL.
c                1 means the convergence test did not pass in MAXL
c                  iterations, but the residual norm is .lt. 1,
c                  or .lt. norm(b) if MNEWT = 0, and so x is computed.
c                2 means the convergence test did not pass in MAXL
c                  iterations, residual .gt. 1, and x is undefined.
c                3 means there was a recoverable error in PSOL
c                  caused by the preconditioner being out of date.
c                4 means ATV failed with repeated failures of F.
c               -1 means there was a nonrecoverable error in PSOL.
c
c-----------------------------------------------------------------------
c
c Type declarations for local variables --------------------------------
c
      doubleprecision BNRM, BNRM0, C, DLNRM, PROD, RHO, S, SNORMW, TEM
      INTEGER I, IER, INFO, IP1, I2, J, K, LL, LLP1
c
c Type declarations for function subroutines called --------------------
c
      doubleprecision dnrm2_u
c
      IFLAG = 0
      LGMR = 0
      NPSL = 0
c-----------------------------------------------------------------------
c The initial residual is the vector b.  Apply scaling to b, and test
c for an immediate return with x = 0 or x = b.
c-----------------------------------------------------------------------
      DO 10 I = 1, N
   10 V(I,1) = B(I)*WGHT(I)
      BNRM0 = dnrm2_u(N, V, 1)
      BNRM = BNRM0
      IF (BNRM0 .GT. DELTA) GO TO 30
      IF (MNEWT .GT. 0) GO TO 20
      CALL dcopy_u(N, B, 1, X, 1)
      RETURN
   20 DO 25 I = 1, N
   25 X(I) = 0.0d0
      RETURN
   30 CONTINUE
c Apply inverse of left preconditioner to vector b. --------------------
      IER = 0
      IF (JPRE .EQ. 0 .OR. JPRE .EQ. 2) GO TO 40
      CALL PSOL (N, TN, Y, SAVF, WK, HB0, WP, IWP, B, 1, IER, RPAR, IPAR
     &   )
      NPSL = 1
      IF (IER .NE. 0) GO TO 300
   40 IF (JPRE .EQ. 0 .OR. JPRE .EQ. 2) GO TO 55
c Calculate norm of scaled vector V(*, 1) and normalize it. ------------
      DO 50 I = 1, N
   50 V(I,1) = B(I)*WGHT(I)
      BNRM = dnrm2_u(N, V, 1)
      DELTA = DELTA*(BNRM/BNRM0)
   55 TEM = 1.0d0/BNRM
      CALL dscal_u(N, TEM, V(1,1), 1)
c Zero out the HES array. ----------------------------------------------
      DO 65 J = 1, MAXL
      DO 60 I = 1, MAXLP1
   60 HES (I,J) = 0.0d0
   65 CONTINUE
c-----------------------------------------------------------------------
c Main loop to compute the vectors V(*,2) to V(*,MAXL).
c The running product PROD is needed for the convergence test.
c-----------------------------------------------------------------------
      PROD = 1.0d0
      DO 90 LL = 1, MAXL
      LGMR = LL
c-----------------------------------------------------------------------
c Call routine VATV to compute VNEW = Abar*v(ll), where Abar is
c the matrix A with scaling and inverse preconditioner factors applied.
c Call routine SVRORTHOG to orthogonalize the new vector VNEW = V(*,LL+1).
c Call routine SHEQR to update the factors of HES .
c-----------------------------------------------------------------------
      CALL VATV (Y, SAVF, V(1,LL), WGHT, X, F, PSOL, RPAR, IPAR, V(1,LL+
     &   1), WK, WP, IWP, HB0, JPRE, IER, NPSL)
      IF (IER .NE. 0) GO TO 310
      CALL SVRORTHOG (V(1, LL+1), V, HES , N, LL, MAXLP1, KMP, SNORMW)
      HES (LL+1, LL) = SNORMW
      CALL SHEQR (HES , MAXLP1, LL, Q, INFO, LL)
      IF (INFO .EQ. LL) GO TO 120
c-----------------------------------------------------------------------
c Update RHO, the estimate of the norm of the residual b - A*xl.
c If KMP .lt. MAXL, then the vectors V(*,1),...,V(*,LL+1) are not
c necessarily orthogonal for LL .gt. KMP.  The vector DL must then
c be computed, and its norm used in the calculation of RHO
c-----------------------------------------------------------------------
      PROD = PROD*Q(2*LL)
      RHO = ABS(PROD*BNRM)
      IF ((LL.GT.KMP) .AND. (KMP.LT.MAXL)) THEN
      IF (LL .EQ. KMP+1) THEN
      CALL dcopy_u(N, V(1,1), 1, DL, 1)
      DO 75 I = 1, KMP
      IP1 = I + 1
      I2 = I*2
      S = Q(I2)
      C = Q(I2-1)
      DO 70 K = 1, N
   70 DL(K) = S*DL(K) + C*V(K,IP1)
   75 CONTINUE
      ENDIF
      S = Q(2*LL)
      C = Q(2*LL-1)/SNORMW
      LLP1 = LL + 1
      DO 80 K = 1, N
   80 DL(K) = S*DL(K) + C*V(K,LLP1)
      DLNRM = dnrm2_u(N, DL, 1)
      RHO = RHO*DLNRM
      ENDIF
c-----------------------------------------------------------------------
c Test for convergence.  If passed, compute approximation xl.
c If failed and LL .lt. MAXL, then continue iterating.
c-----------------------------------------------------------------------
      IF (RHO .LE. DELTA) GO TO 200
      IF (LL .EQ. MAXL) GO TO 100
c-----------------------------------------------------------------------
c Rescale so that the norm of V(1,LL+1) is one.
c-----------------------------------------------------------------------
      TEM = 1.0d0/SNORMW
      CALL dscal_u(N, TEM, V(1,LL+1), 1)
   90 CONTINUE
  100 CONTINUE
      IF (RHO .LE. 1.0d0) GO TO 150
      IF (RHO .LE. BNRM .AND. MNEWT .EQ. 0) GO TO 150
  120 CONTINUE
      IFLAG = 2
      RETURN
  150 IFLAG = 1
c-----------------------------------------------------------------------
c Compute the approximation xl to the solution.
c Since the vector X was used as work space, and the initial guess
c of the Newton correction is zero, x must be reset to zero.
c-----------------------------------------------------------------------
  200 CONTINUE
      LL = LGMR
      LLP1 = LL + 1
      DO 210 K = 1, LLP1
  210 B(K) = 0.0d0
      B(1) = BNRM
      CALL SHELS (HES , MAXLP1, LL, Q, B)
      DO 220 K = 1, N
  220 X(K) = 0.0d0
      DO 230 I = 1, LL
      CALL daxpy_u(N, B(I), V(1,I), 1, X, 1)
  230 CONTINUE
      DO 240 I = 1, N
  240 X(I) = X(I)/WGHT(I)
      IF (JPRE .LE. 1) RETURN
      CALL PSOL (N, TN, Y, SAVF, WK, HB0, WP, IWP, X, 2, IER, RPAR, IPAR
     &   )
      NPSL = NPSL + 1
      IF (IER .NE. 0) GO TO 300
      RETURN
c Error returns forced by routine PSOL. --------------------------------
  300 CONTINUE
      IF (IER .LT. 0) IFLAG = -1
      IF (IER .GT. 0) IFLAG = 3
      RETURN
c Error returns forced by ATV (by failure of PSOL or F). ---------------
  310 CONTINUE
      IF (IER .EQ. -1) IFLAG = -1
      IF (IER .EQ. 1) IFLAG = 3
      IF (IER .EQ. 2) IFLAG = 4
      RETURN
c----------------------- End of Subroutine VSPIG -----------------------
      END
      SUBROUTINE VATV (Y, SAVF, V, WGHT, FTEM, F, PSOL, RPAR, IPAR, Z, 
     &   VTEM, WP, IWP, HB0, JPRE, IER, NPSL)
      EXTERNAL F, PSOL
      doubleprecision Y, SAVF, V, WGHT, FTEM, RPAR, Z, VTEM, WP, HB0
      INTEGER IPAR, IWP, JPRE, IER, NPSL
      DIMENSION Y(*), SAVF(*), V(*), WGHT(*), FTEM(*), Z(*), VTEM(*), WP
     &   (*), IWP(*), RPAR(*), IPAR(*)
c-----------------------------------------------------------------------
c Call sequence input -- Y, SAVF, V, WGHT, F, PSOL, RPAR, IPAR,
c                        WP, IWP, HB0, NPSL
c Call sequence output --Z, IER, NPSL
c COMMON block variables accessed..
c        /VOD001/  TN, N
c        /VOD002/  NFE
c Subroutines called.. F, PSOL, SCOPY
c Function subroutines called.. SNRM2
c-----------------------------------------------------------------------
c This routine computes the product
c
c   (D-inverse)*(P1-inverse)*(I - hb0*df/dy)*(P2-inverse)*(D*v),
c
c where D is a diagonal scaling matrix, and P1 and P2 are the
c left and right preconditioning matrices, respectively.
c v is assumed to have WRMS norm equal to 1.
c The product is stored in Z.  This is computed by a
c difference quotient, a call to F, and two calls to PSOL.
c If the F call fails, up to 4 more tries are made with a smaller
c value for the increment.
c-----------------------------------------------------------------------
c
c      On entry
c
c            Y = array containing current dependent variable vector.
c
c         SAVF = array containing current value of f(t,y).
c
c            V = real array of length N (can be the same array as Z).
c
c         WGHT = array of length N containing scale factors.
c                1/WGHT(i) are the diagonal elements of the matrix D.
c
c         FTEM = work array of length N.
c
c         VTEM = work array of length N used to store the
c                unscaled version of v.
c
c           WP = real work array used by preconditioner PSOL.
c
c          IWP = integer work array used by preconditioner PSOL.
c
c          HB0 = current value of (step size h) * (coefficient beta0).
c
c         JPRE = preconditioner type flag.
c
c
c      On return
c
c            Z = array of length N containing desired scaled
c                matrix-vector product.
c
c          IER = error flag.
c                IER =  1 means PSOL failed recoverably.
c                IER = -1 means PSOL failed unrecoverably.
c                IER =  2 means calls to F failed repeatedly.
c
c         NPSL = the number of calls to PSOL.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for labeled COMMON block VOD002 --------------------
c
      doubleprecision HU
      INTEGER NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
c
c Type declarations for local variables --------------------------------
c
      doubleprecision FAC, SIG, RSIG
      INTEGER I, IERP, NFAIL, IFAIL

c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision dnrm2_u
c
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
      COMMON /VOD002/ HU, NCFN, NETF, NFE, NPE, NLU, NNI, NQU, NST
      doubleprecision scaleps
      common /comvatv/ scaleps
c-----------------------------------------------------------------------
      NFAIL = 0
c Set vtem = D * v. ----------------------------------------------------
      DO 10 I = 1, N
   10 VTEM(I) = V(I)/WGHT(I)
      IF (JPRE .GE. 2) GO TO 30
c
c JPRE = 0 or 1.  Save y in Z and increment Y by VTEM. -----------------
      CALL dcopy_u(N, Y, 1, Z, 1)
      DO 20 I = 1, N
   20 Y(I) = Z(I) + VTEM(I)*scaleps
      SIG = scaleps
      RSIG = 1.0d0/scaleps
      FAC = HB0*RSIG
      GO TO 60
c
c JPRE = 2 or 3.  Apply inverse of right preconditioner to VTEM. -------
   30 CONTINUE
      CALL PSOL (N, TN, Y, SAVF, FTEM, HB0, WP, IWP, VTEM, 2, IERP, RPAR
     &   , IPAR)
      NPSL = NPSL + 1
      IF (IERP .NE. 0) GO TO 100
c Calculate l-2 norm of (D-inverse) * VTEM. ----------------------------
      DO 40 I = 1, N
   40 Z(I) = VTEM(I)*WGHT(I)
      RSIG = dnrm2_u(N, Z, 1)/scaleps
      SIG = 1.0d0/RSIG
c Save y in Z and increment Y by VTEM/norm. ----------------------------
      CALL dcopy_u(N, Y, 1, Z, 1)
   45 DO 50 I = 1, N
   50 Y(I) = Z(I) + VTEM(I)*SIG
      FAC = HB0*RSIG
c
c For all JPRE, call F with incremented Y argument, and restore Y. -----
   60 CONTINUE
      IFAIL = 0
      CALL F (N, TN, Y, FTEM, RPAR, IPAR, IFAIL)
      NFE = NFE + 1
      IF (IFAIL .NE. 0) THEN
      NFAIL = NFAIL + 1
      IF (NFAIL .GT. 5) GO TO 110
      SIG = 0.25d0*SIG
      RSIG = 4.0d0*RSIG
      GO TO 45
      ENDIF
      CALL dcopy_u(N, Z, 1, Y, 1)
c Set Z = (I - HB0*Jacobian) * VTEM, using difference quotient. --------
      DO 70 I = 1, N
   70 Z(I) = FTEM(I) - SAVF(I)
      DO 80 I = 1, N
   80 Z(I) = VTEM(I) - FAC*Z(I)
c Apply inverse of left preconditioner to Z, if nontrivial. ------------
      IF (JPRE .EQ. 0 .OR. JPRE .EQ. 2) GO TO 85
      CALL PSOL (N, TN, Y, SAVF, FTEM, HB0, WP, IWP, Z, 1, IERP, RPAR, 
     &   IPAR)
      NPSL = NPSL + 1
      IF (IERP .NE. 0) GO TO 100
   85 CONTINUE
c Apply D-inverse to Z and return. -------------------------------------
      DO 90 I = 1, N
   90 Z(I) = Z(I)*WGHT(I)
      IER = 0
      RETURN
c
  100 IER = 1
      IF (IERP .LT. 0) IER = -1
      RETURN
  110 IER = 2
      RETURN
c----------------------- End of Subroutine VATV ------------------------
      END
      SUBROUTINE VUSOL (N, TN, Y, SAVF, B, WGHT, DELTA, HB0, JPRE, MNEWT
     &   , PSOL, NPSL, X, WP, IWP, WK, RPAR, IPAR, IFLAG)
      EXTERNAL PSOL
      doubleprecision TN, Y, SAVF, B, WGHT, DELTA, HB0, X, WP, WK, RPAR
      INTEGER N, JPRE, MNEWT, NPSL, IWP, IPAR, IFLAG
      DIMENSION Y(*), SAVF(*), B(*), WGHT(*), X(*), WP(*), IWP(*), WK(*)
     &   , RPAR(*), IPAR(*)
c-----------------------------------------------------------------------
c This routine solves the linear system A * x = b using only
c calls to the user-supplied routine PSOL (no Krylov iteration).
c If the norm of the right-hand side vector b is smaller than DELTA,
c the vector x returned is x = b (if MNEWT = 0) or x = 0 otherwise.
c PSOL is called with an LR argument of 1 (if JPRE = 1 or 3),
c then 2 (if JPRE = 2 or 3).
c-----------------------------------------------------------------------
c
c      On entry
c
c          NEQ = problem size, passed to F and PSOL (NEQ(1) = N).
c
c           TN = current value of t.
c
c            Y = array containing current dependent variable vector.
c
c         SAVF = array containing current value of f(t,y).
c
c            B = the right hand side of the system A*x = b.
c
c         WGHT = the vector of length N containing the nonzero
c                elements of the diagonal scaling matrix.
c
c            N = the order of the matrix A, and the lengths
c                of the vectors WGHT, b and x.
c
c        DELTA = tolerance on residuals  b - A*x  in weighted RMS norm.
c
c          HB0 = current value of (step size h) * (coefficient beta0).
c
c         JPRE = preconditioner type flag.
c
c        MNEWT = Newton iteration counter (.ge. 0).
c
c           WK = real work array used by PSOL.
c
c           WP = real work array used by preconditioner PSOL.
c
c          IWP = integer work array used by preconditioner PSOL.
c
c      On return
c
c         X    = the final computed approximation to the solution
c                of the system A*x = b.
c
c         NPSL = the number of calls to PSOL.
c
c        IFLAG = integer error flag..
c                0 means no trouble occurred.
c                3 means there was a recoverable error in PSOL
c                  caused by the preconditioner being out of date.
c               -1 means there was a nonrecoverable error in PSOL.
c
c-----------------------------------------------------------------------
c
c Type declarations for local variables --------------------------------
c
      doubleprecision BNRM
      INTEGER I, IER
c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision VNORML
c
      IFLAG = 0
      NPSL = 0
c-----------------------------------------------------------------------
c Test for an immediate return with x = 0 or x = b.
c-----------------------------------------------------------------------
      BNRM = VNORML (N, B, WGHT)
      IF (BNRM .GT. DELTA) GO TO 30
      IF (MNEWT .GT. 0) GO TO 10
      CALL dcopy_u(N, B, 1, X, 1)
      RETURN
   10 DO 20 I = 1, N
   20 X(I) = 0.0d0
      RETURN
c Apply inverse of left preconditioner to vector b. --------------------
   30 IER = 0
      IF (JPRE .EQ. 0 .OR. JPRE .EQ. 2) GO TO 40
      CALL PSOL (N, TN, Y, SAVF, WK, HB0, WP, IWP, B, 1, IER, RPAR,IPAR)
      NPSL = 1
      IF (IER .NE. 0) GO TO 100
c Apply inverse of right preconditioner to result, and copy to X. ------
   40 IF (JPRE .LE. 1) GO TO 50
      CALL PSOL (N, TN, Y, SAVF, WK, HB0, WP, IWP, B, 2, IER, RPAR, IPAR
     &   )
      NPSL = NPSL + 1
      IF (IER .NE. 0) GO TO 100
   50 CALL dcopy_u(N, B, 1, X, 1)
      RETURN
c-----------------------------------------------------------------------
c This block handles error returns forced by routine PSOL.
c-----------------------------------------------------------------------
  100 CONTINUE
      IF (IER .LT. 0) IFLAG = -1
      IF (IER .GT. 0) IFLAG = 3
      RETURN
c----------------------- End of Subroutine VUSOL -----------------------
      END
      SUBROUTINE VKSRC (RSAV, ISAV, JOB)
      doubleprecision RSAV
      INTEGER ISAV, JOB
      DIMENSION RSAV(*), ISAV(*)
c-----------------------------------------------------------------------
c Call sequence input -- RSAV, ISAV, JOB
c Call sequence output -- RSAV, ISAV
c COMMON block variables accessed -- All of /VOD001/, /VOD002/, /VODPK1/
c
c Subroutines/functions called by VKSRC.. None
c-----------------------------------------------------------------------
c This routine saves or restores (depending on JOB) the contents of the
c COMMON blocks VOD001, VOD002, VPK001, used internally by VODPK.
c
c RSAV = real array of length 52 or more.
c ISAV = integer array of length 52 or more.
c JOB  = flag indicating to save or restore the COMMON blocks..
c        JOB  = 1 if COMMON is to be saved (written to RSAV/ISAV).
c        JOB  = 2 if COMMON is to be restored (read from RSAV/ISAV).
c        A call with JOB = 2 presumes a prior call with JOB = 1.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision RVOD1
      INTEGER IVOD1
c
c Type declarations for labeled COMMON block VOD002 --------------------
c
      doubleprecision RVOD2
      INTEGER IVOD2
c
c Type declarations for labeled COMMON block VPK001 --------------------
c
      doubleprecision RVPK1
      INTEGER IVPK1
c
c Type declarations for local variables --------------------------------
c
c
      INTEGER I, IOFF, LENIV1, LENIV2, LENRV1, LENRV2, LRVK1, LIVK1
c-----------------------------------------------------------------------
c The following Fortran-77 declaration is to cause the values of the
c listed (local) variables to be saved between calls to this integrator.
c-----------------------------------------------------------------------
      SAVE LENRV1, LENIV1, LENRV2, LENIV2, LRVK1, LIVK1
c-----------------------------------------------------------------------
      COMMON /VOD001/ RVOD1(48), IVOD1(33)
      COMMON /VOD002/ RVOD2(1), IVOD2(8)
      COMMON /VPK001/ RVPK1(3), IVPK1(11)
      DATA LENRV1 /48/, LENIV1 /33/, LENRV2 /1/, LENIV2 /8/, LRVK1 /3/, 
     &   LIVK1 /11/
c
      IF (JOB .EQ. 2) GO TO 100
      DO 10 I = 1, LENRV1
   10 RSAV(I) = RVOD1(I)
      DO 12 I = 1, LENRV2
   12 RSAV(LENRV1+I) = RVOD2(I)
      IOFF = LENRV1 + LENRV2
      DO 14 I = 1, LRVK1
   14 RSAV(IOFF+I) = RVPK1(I)
c
      DO 20 I = 1, LENIV1
   20 ISAV(I) = IVOD1(I)
      DO 22 I = 1, LENIV2
   22 ISAV(LENIV1+I) = IVOD2(I)
      IOFF = LENIV1 + LENIV2
      DO 24 I = 1, LIVK1
   24 ISAV(IOFF+I) = IVPK1(I)
c
      RETURN
c
  100 CONTINUE
      DO 110 I = 1, LENRV1
  110 RVOD1(I) = RSAV(I)
      DO 112 I = 1, LENRV2
  112 RVOD2(I) = RSAV(LENRV1+I)
      IOFF = LENRV1 + LENRV2
      DO 114 I = 1, LRVK1
  114 RVPK1(I) = RSAV(IOFF+I)
c
      DO 120 I = 1, LENIV1
  120 IVOD1(I) = ISAV(I)
      DO 122 I = 1, LENIV2
  122 IVOD2(I) = ISAV(LENIV1+I)
      IOFF = LENIV1 + LENIV2
      DO 124 I = 1, LIVK1
  124 IVPK1(I) = ISAV(IOFF+I)
c
      RETURN
c----------------------- End of Subroutine VKSRC -----------------------
      END
      SUBROUTINE VHIN (N, T0, Y0, YDOT, F, RPAR, IPAR, TOUT, UROUND, EWT
     &   , ITOL, ATOL, Y, TEMP, H0, NITER, IER)
      EXTERNAL F
      doubleprecision T0, Y0, YDOT, RPAR, TOUT, UROUND, EWT, ATOL, Y, 
     &   TEMP, H0
      INTEGER N, IPAR, ITOL, NITER, IER
      DIMENSION Y0(*), YDOT(*), EWT(*), ATOL(*), Y(*), TEMP(*), RPAR(*), 
     &   IPAR(*)
c-----------------------------------------------------------------------
c Call sequence input -- N, T0, Y0, YDOT, F, RPAR, IPAR, TOUT, UROUND,
c                        EWT, ITOL, ATOL, Y, TEMP
c Call sequence output -- H0, NITER, IER
c COMMON block variables accessed -- None
c
c Subroutines called by VHIN.. F
c Function routines called by VHIN.. VNORML
c-----------------------------------------------------------------------
c This routine computes the step size, H0, to be attempted on the
c first step, when the user has not supplied a value for this.
c
c First we check that TOUT - T0 differs significantly from zero.  Then
c an iteration is done to approximate the initial second derivative
c and this is used to define h from w.r.m.s.norm(h**2 * yddot / 2) = 1.
c A bias factor of 1/2 is applied to the resulting h.
c The sign of H0 is inferred from the initial values of TOUT and T0.
c
c Communication with VHIN is done with the following variables..
c
c N      = Size of ODE system, input.
c T0     = Initial value of independent variable, input.
c Y0     = Vector of initial conditions, input.
c YDOT   = Vector of initial first derivatives, input.
c F      = Name of subroutine for right-hand side f(t,y), input.
c RPAR, IPAR = Dummy names for user's real and integer work arrays.
c TOUT   = First output value of independent variable
c UROUND = Machine unit roundoff
c EWT, ITOL, ATOL = Error weights and tolerance parameters
c                   as described in the driver routine, input.
c Y, TEMP = Work arrays of length N.
c H0     = Step size to be attempted, output.
c NITER  = Number of iterations (and of f evaluations) to compute H0,
c          output.
c IER    = The error flag, returned with the value
c          IER = 0  if no trouble occurred, or
c          IER = -1 if TOUT and T0 are considered too close to proceed.
c          IER = -2 if F returned IFAIL .ne. 0, after 5 attempts to
c                   avoid this condition.
c-----------------------------------------------------------------------
c
c Type declarations for local variables --------------------------------
c
      doubleprecision AFI, ATOLI, DELYI, HALF, HG, HLB, HNEW, HRAT, HUB, 
     &   HUN, PT1, PT2, T1, TDIST, TROUND, TWO, YDDNRM
      INTEGER I, ITER, IFAIL
c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision VNORML
c-----------------------------------------------------------------------
c The following Fortran-77 declaration is to cause the values of the
c listed (local) variables to be saved between calls to this integrator.
c-----------------------------------------------------------------------
      SAVE HALF, HUN, PT1, TWO
      DATA HALF /0.5d0/, HUN /100.0d0/, PT1 /0.1d0/, PT2 /0.2d0/, TWO /
     &   2.0d0/
c
      NITER = 0
      TDIST = ABS(TOUT - T0)
      TROUND = UROUND*max(ABS(T0),ABS(TOUT))
      IF (TDIST .LT. TWO*TROUND) GO TO 100
c
c Set a lower bound on h based on the roundoff level in T0 and TOUT. ---
      HLB = HUN*TROUND
c Set an upper bound on h based on TOUT-T0 and the initial Y and YDOT. -
      HUB = PT1*TDIST
      ATOLI = ATOL(1)
      DO 10 I = 1, N
      IF (ITOL .EQ. 2 .OR. ITOL .EQ. 4) ATOLI = ATOL(I)
      DELYI = PT1*ABS(Y0(I)) + ATOLI
      AFI = ABS(YDOT(I))
      IF (AFI*HUB .GT. DELYI) HUB = DELYI/AFI
   10 CONTINUE
c
c Set initial guess for h as geometric mean of upper and lower bounds. -
      ITER = 0
      HG = SQRT(HLB*HUB)
c If the bounds have crossed, exit with the mean value. ----------------
      IF (HUB .LT. HLB) THEN
      H0 = HG
      GO TO 90
      ENDIF
c
c Looping point for iteration. -----------------------------------------
   50 CONTINUE
c Estimate the second derivative as a difference quotient in f. --------
      T1 = T0 + HG
      DO 60 I = 1, N
   60 Y(I) = Y0(I) + HG*YDOT(I)
      IFAIL = 0
      CALL F (N, T1, Y, TEMP, RPAR, IPAR, IFAIL)
      IF (IFAIL .NE. 0) THEN
      HNEW = PT2*HG
      GO TO 75
      ENDIF
      DO 70 I = 1, N
   70 TEMP(I) = (TEMP(I) - YDOT(I))/HG
      YDDNRM = VNORML (N, TEMP, EWT)
c Get the corresponding new value of h. --------------------------------
      IF (YDDNRM*HUB*HUB .GT. TWO) THEN
      HNEW = SQRT(TWO/YDDNRM)
      ELSE
      HNEW = SQRT(HG*HUB)
      ENDIF
   75 ITER = ITER + 1
c-----------------------------------------------------------------------
c Test the stopping conditions.
c Stop if the new and previous h values differ by a factor of .lt. 2.
c Stop if four iterations have been done.  Also, stop with previous h
c if HNEW/HG .gt. 2 after first iteration, as this probably means that
c the second derivative value is bad because of cancellation error.
c-----------------------------------------------------------------------
      IF (ITER .GE. 4) GO TO 80
      HRAT = HNEW/HG
      IF ( (HRAT .GT. HALF) .AND. (HRAT .LT. TWO) ) GO TO 80
      IF ( (ITER .GE. 2) .AND. (HNEW .GT. TWO*HG) ) THEN
      HNEW = HG
      GO TO 80
      ENDIF
      HG = HNEW
      GO TO 50
c
c Iteration done.  Apply bounds, bias factor, and sign.  Then exit. ----
   80 IF (IFAIL .NE. 0) GO TO 110
      H0 = HNEW*HALF
      IF (H0 .LT. HLB) H0 = HLB
      IF (H0 .GT. HUB) H0 = HUB
   90 H0 = SIGN(H0, TOUT - T0)
      NITER = ITER
      IER = 0
      RETURN
c Error return for TOUT - T0 too small. --------------------------------
  100 IER = -1
      RETURN
c Error return for IFAIL .ne. 0 from F. --------------------------------
  110 IER = -2
      RETURN
c----------------------- End of Subroutine VHIN ------------------------
      END
      SUBROUTINE VINDY (T, K, YH, LDYH, DKY, IFLAG)
      doubleprecision T, YH, DKY
      INTEGER K, LDYH, IFLAG
      DIMENSION YH(LDYH,*), DKY(*)
c-----------------------------------------------------------------------
c Call sequence input -- T, K, YH, LDYH
c Call sequence output -- DKY, IFLAG
c COMMON block variables accessed..
c     /VOD001/ --  H, TN, UROUND, L, N, NQ
c     /VOD002/ --  HU
c
c Subroutines called by VINDY.. SSCAL, XERRWV
c Function routines called by VINDY.. None
c-----------------------------------------------------------------------
c VINDY computes interpolated values of the K-th derivative of the
c dependent variable vector y, and stores it in DKY.  This routine
c is called within the package with K = 0 and T = TOUT, but may
c also be called by the user for any K up to the current order.
c (See detailed instructions in the usage documentation.)
c-----------------------------------------------------------------------
c The computed values in DKY are gotten by interpolation using the
c Nordsieck history array YH.  This array corresponds uniquely to a
c vector-valued polynomial of degree NQCUR or less, and DKY is set
c to the K-th derivative of this polynomial at T.
c The formula for DKY is..
c              q
c  DKY(i)  =  sum  c(j,K) * (T - TN)**(j-K) * H**(-j) * YH(i,j+1)
c             j=K
c where  c(j,K) = j*(j-1)*...*(j-K+1), q = NQCUR, TN = TCUR, H = HCUR.
c The quantities  NQ = NQCUR, L = NQ+1, N, TN, and H are
c communicated by COMMON.  The above sum is done in reverse order.
c IFLAG is returned negative if either K or T is out of bounds.
c
c Discussion above and comments in driver explain all variables.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for labeled COMMON block VOD002 --------------------
c
      doubleprecision HU
      INTEGER NCFN, NETF, NFE, NJE, NLU, NNI, NQU, NST
c
c Type declarations for local variables --------------------------------
c
      doubleprecision C, HUN, R, S, TFUZZ, TN1, TP, ZERO
      INTEGER I, IC, J, JB, JB2, JJ, JJ1, JP1
      CHARACTER*80 MSG
c-----------------------------------------------------------------------
c The following Fortran-77 declaration is to cause the values of the
c listed (local) variables to be saved between calls to this integrator.
c-----------------------------------------------------------------------
      SAVE HUN, ZERO
c
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
      COMMON /VOD002/ HU, NCFN, NETF, NFE, NJE, NLU, NNI, NQU, NST
c
      DATA HUN /100.0d0/, ZERO /0.0d0/
c
      IFLAG = 0
      IF (K .LT. 0 .OR. K .GT. NQ) GO TO 80
      TFUZZ = HUN*UROUND*(TN + HU)
      TP = TN - HU - TFUZZ
      TN1 = TN + TFUZZ
      IF ((T-TP)*(T-TN1) .GT. ZERO) GO TO 90
c
      S = (T - TN)/H
      IC = 1
      IF (K .EQ. 0) GO TO 15
      JJ1 = L - K
      DO 10 JJ = JJ1, NQ
   10 IC = IC*JJ
   15 C = dble(IC)
      DO 20 I = 1, N
   20 DKY(I) = C*YH(I,L)
      IF (K .EQ. NQ) GO TO 55
      JB2 = NQ - K
      DO 50 JB = 1, JB2
      J = NQ - JB
      JP1 = J + 1
      IC = 1
      IF (K .EQ. 0) GO TO 35
      JJ1 = JP1 - K
      DO 30 JJ = JJ1, J
   30 IC = IC*JJ
   35 C = dble(IC)
      DO 40 I = 1, N
   40 DKY(I) = C*YH(I,JP1) + S*DKY(I)
   50 CONTINUE
      IF (K .EQ. 0) RETURN
   55 R = H**(-K)
      CALL dscal_u(N, R, DKY, 1)
      RETURN
c
   80 MSG = 'VINDY--  K (=I1) illegal      '
      CALL dxerrwv_u(MSG, 30, 51, 1, 1, K, 0, 0, ZERO, ZERO)
      IFLAG = -1
      RETURN
   90 MSG = 'VINDY--  T (=R1) illegal      '
      CALL dxerrwv_u(MSG, 30, 52, 1, 0, 0, 0, 1, T, ZERO)
      MSG='      T not in interval TCUR - HU (= R1) to TCUR (=R2)      '
      CALL dxerrwv_u(MSG, 60, 52, 1, 0, 0, 0, 2, TP, TN)
      IFLAG = -2
      RETURN
c----------------------- End of Subroutine VINDY -----------------------
      END
      SUBROUTINE VSTEP (Y, YH, LDYH, YH1, EWT, SAVF, VSAV, ACOR, WM, IWM
     &   , F, JAC, PSOL, VNLS, RPAR, IPAR)
      EXTERNAL F, JAC, PSOL, VNLS
      doubleprecision Y, YH, YH1, EWT, SAVF, VSAV, ACOR, WM, RPAR
      INTEGER LDYH, IWM, IPAR
      DIMENSION Y(*), YH(LDYH,*), YH1(*), EWT(*), SAVF(*), VSAV(*), ACOR
     &   (*), WM(*), IWM(*), RPAR(*), IPAR(*)
c-----------------------------------------------------------------------
c Call sequence input -- Y, YH, LDYH, YH1, EWT, SAVF, VSAV,
c                        ACOR, WM, IWM, F, JAC, PSOL, VNLS, RPAR, IPAR
c Call sequence output -- YH, ACOR, WM, IWM
c COMMON block variables accessed..
c     /VOD001/  ACNRM, EL(13), H, HMIN, HMXI, HNEW, HSCAL, RC, TAU(13),
c               TQ(5), TN, JCUR, JSTART, KFLAG, KUTH,
c               L, LMAX, MAXORD, MITER, N, NEWQ, NQ, NQWAIT
c     /VOD002/  HU, NCFN, NETF, NFE, NQU, NST
c
c Subroutines called by VSTEP.. F, SAXPY, SCOPY, SSCAL,
c                               VJUST, VNLS, VSET
c Function routines called by VSTEP.. VNORML
c-----------------------------------------------------------------------
c VSTEP performs one step of the integration of an initial value
c problem for a system of ordinary differential equations.
c VSTEP calls subroutine VNLS for the solution of the nonlinear system
c arising in the time step.  Thus it is independent of the problem
c Jacobian structure and the type of nonlinear system solution method.
c VSTEP returns a completion flag KFLAG (in COMMON).
c A return with KFLAG = -1, -2, or -5 means either ABS(H) = HMIN or 10
c consecutive failures occurred.  On a return with KFLAG negative,
c the values of TN and the YH array are as of the beginning of the last
c step, and H is the last step size attempted.
c
c Communication with VSTEP is done with the following variables..
c
c Y      = An array of length N used for the dependent variable vector.
c YH     = An LDYH by LMAX array containing the dependent variables
c          and their approximate scaled derivatives, where
c          LMAX = MAXORD + 1.  YH(i,j+1) contains the approximate
c          j-th derivative of y(i), scaled by H**j/factorial(j)
c          (j = 0,1,...,NQ).  On entry for the first step, the first
c          two columns of YH must be set from the initial values.
c LDYH   = A constant integer .ge. N, the first dimension of YH.
c          N is the number of ODEs in the system.
c YH1    = A one-dimensional array occupying the same space as YH.
c EWT    = An array of length N containing multiplicative weights
c          for local error measurements.  Local errors in y(i) are
c          compared to 1.0/EWT(i) in various error tests.
c SAVF   = An array of working storage, of length N.
c          also used for input of YH(*,MAXORD+2) when JSTART = -1
c          and MAXORD .lt. the current order NQ.
c VSAV   = A work array of length N passed to subroutine VNLS.
c ACOR   = A work array of length N, used for the accumulated
c          corrections.  On a successful return, ACOR(i) contains
c          the estimated one-step local error in y(i).
c WM,IWM = Real and integer work arrays associated with matrix
c          operations in VNLS.
c F      = Dummy name for the user supplied subroutine for f.
c JAC    = Dummy name for the user supplied Jacobian subroutine.
c PSOL   = Dummy name for the subroutine passed to VNLS, for
c          possible use there.
c VNLS   = Dummy name for the nonlinear system solving subroutine,
c          whose real name is dependent on the method used.
c RPAR, IPAR = Dummy names for user's real and integer work arrays.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for labeled COMMON block VOD002 --------------------
c
      doubleprecision HU
      INTEGER NCFN, NETF, NFE, NJE, NLU, NNI, NQU, NST
c
c Type declarations for local variables --------------------------------
c
      doubleprecision ADDON, BIAS1,BIAS2,BIAS3, CNQUOT, DDN, DSM, DUP, 
     &   ETACF, ETAMIN, ETAMX1, ETAMX2, ETAMX3, ETAMXF, ETAQ, ETAQM1, 
     &   ETAQP1, FLOTL, ONE, ONEPSM, R, THRESH, TOLD, ZERO
      INTEGER I, I1, I2, IBACK, J, JB, KFC, KFH, MXNCF, NCF, NFLAG
      INTEGER IFAIL
c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision VNORML
c
c Type declaration for the additional diagnostics set up to inquire ----
c during the running of vodpk. -----------------------------------------
c
      character*80 msgjm
      integer nrcv, ierrjm, ijmgetmr, imxer2, imxer3
      doubleprecision big2, big3, size2
c-----------------------------------------------------------------------
c The following Fortran-77 declaration is to cause the values of the
c listed (local) variables to be saved between calls to this integrator.
c-----------------------------------------------------------------------
      SAVE ADDON, BIAS1, BIAS2, BIAS3, ETACF, ETAMIN, ETAMX1, ETAMX2, 
     &   ETAMX3, ETAMXF, KFC, KFH, MXNCF, ONEPSM, THRESH, ONE, ZERO, 
     &   ETAQ, ETAQM1
c-----------------------------------------------------------------------
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
      COMMON /VOD002/ HU, NCFN, NETF, NFE, NJE, NLU, NNI, NQU, NST
c
      DATA KFC/-3/, KFH/-7/, MXNCF/10/
      DATA ADDON /1.0d-6/, BIAS1 /6.0d0/, BIAS2 /6.0d0/, BIAS3 /10.0d0/, 
     &   ETACF /0.25d0/, ETAMIN /0.1d0/, ETAMXF /0.2d0/, ETAMX1 /1.0d4/, 
     &   ETAMX2 /10.0d0/, ETAMX3 /10.0d0/, ONEPSM /1.00001d0/, THRESH /
     &   1.5d0/
      DATA ONE/1.0d0/, ZERO/0.0d0/
c
      KFLAG = 0
      TOLD = TN
      NCF = 0
      JCUR = 0
      NFLAG = 0
      IF (JSTART .GT. 0) GO TO 20
      IF (JSTART .EQ. -1) GO TO 100
c-----------------------------------------------------------------------
c On the first call, the order is set to 1, and other variables are
c initialized.  ETAMAX is the maximum ratio by which H can be increased
c in a single step.  It is normally 1.5, but is larger during the
c first 10 steps to compensate for the small initial H.  If a failure
c occurs (in corrector convergence or error test), ETAMAX is set to 1
c for the next increase.
c-----------------------------------------------------------------------
      LMAX = MAXORD + 1
      NQ = 1
      L = 2
      NQNYH = NQ*LDYH
      TAU(1) = H
      PRL1 = ONE
      RC = ZERO
      ETAMAX = ETAMX1
      NQWAIT = 2
      HSCAL = H
      IFAIL = 0
      GO TO 200
c-----------------------------------------------------------------------
c Take preliminary actions on a normal continuation step (JSTART.GT.0).
c If the driver changed H, then ETA must be reset and NEWH set to 1.
c If a change of order was dictated on the previous step, then
c it is done here and appropriate adjustments in the history are made.
c On an order decrease, the history array is adjusted by VJUST.
c On an order increase, the history array is augmented by a column.
c On a change of step size H, the history array YH is rescaled.
c-----------------------------------------------------------------------
   20 CONTINUE
      IF (KUTH .EQ. 1) THEN
      ETA = min(ETA,H/HSCAL)
      NEWH = 1
      ENDIF
   50 IF (NEWH .EQ. 0) GO TO 200
      IF (NEWQ .EQ. NQ) GO TO 150
      IF (NEWQ .LT. NQ) THEN
      CALL VJUST (YH, LDYH, -1)
      NQ = NEWQ
      L = NQ + 1
      NQWAIT = L
      GO TO 150
      ENDIF
      IF (NEWQ .GT. NQ) THEN
      CALL VJUST (YH, LDYH, 1)
      NQ = NEWQ
      L = NQ + 1
      NQWAIT = L
      GO TO 150
      ENDIF
c-----------------------------------------------------------------------
c The following block handles preliminaries needed when JSTART = -1.
c If N was reduced, zero out part of YH to avoid undefined references.
c If MAXORD was reduced to a value less than the tentative order NEWQ,
c then NQ is set to MAXORD, and a new H ratio ETA is chosen.
c Otherwise, we take the same preliminary actions as for JSTART .gt. 0.
c In any case, NQWAIT is reset to L = NQ + 1 to prevent further
c changes in order for that many steps.
c The new H ratio ETA is limited by the input H if KUTH = 1,
c by HMIN if KUTH = 0, and by HMXI in any case.
c Finally, the history array YH is rescaled.
c-----------------------------------------------------------------------
  100 CONTINUE
      LMAX = MAXORD + 1
      IF (N .EQ. LDYH) GO TO 120
      I1 = 1 + (NEWQ + 1)*LDYH
      I2 = (MAXORD + 1)*LDYH
      IF (I1 .GT. I2) GO TO 120
      DO 110 I = I1, I2
  110 YH1(I) = ZERO
  120 IF (NEWQ .LE. MAXORD) GO TO 140
      FLOTL = dble(LMAX)
      IF (MAXORD .LT. NQ-1) THEN
      DDN = VNORML (N, SAVF, EWT)/TQ(1)
      ETA = ONE/((BIAS1*DDN)**(ONE/FLOTL) + ADDON)
      ENDIF
      IF (MAXORD .EQ. NQ .AND. NEWQ .EQ. NQ+1) ETA = ETAQ
      IF (MAXORD .EQ. NQ-1 .AND. NEWQ .EQ. NQ+1) THEN
      ETA = ETAQM1
      CALL VJUST (YH, LDYH, -1)
      ENDIF
      IF (MAXORD .EQ. NQ-1 .AND. NEWQ .EQ. NQ) THEN
      DDN = VNORML (N, SAVF, EWT)/TQ(1)
      ETA = ONE/((BIAS1*DDN)**(ONE/FLOTL) + ADDON)
      CALL VJUST (YH, LDYH, -1)
      ENDIF
      ETA = min(ETA,ONE)
      NQ = MAXORD
      L = LMAX
  140 IF (KUTH .EQ. 1) ETA = min(ETA,ABS(H/HSCAL))
      IF (KUTH .EQ. 0) ETA = max(ETA,HMIN/ABS(HSCAL))
      ETA = ETA/max(ONE,ABS(HSCAL)*HMXI*ETA)
      NEWH = 1
      NQWAIT = L
      IF (NEWQ .LE. MAXORD) GO TO 50
c Rescale the history array for a change in H by a factor of ETA. ------
  150 R = ONE
      DO 180 J = 2, L
      R = R*ETA
      CALL dscal_u(N, R, YH(1,J), 1 )
  180 CONTINUE
      H = HSCAL*ETA
      HSCAL = H
      RC = RC*ETA
      NQNYH = NQ*LDYH
c-----------------------------------------------------------------------
c This section computes the predicted values by effectively
c multiplying the YH array by the Pascal triangle matrix.
c VSET is called to calculate all integration coefficients.
c RC is the ratio of new to old values of the coefficient H/EL(2)=h/l1.
c-----------------------------------------------------------------------
  200 TN = TN + H
      I1 = NQNYH + 1
      DO 220 JB = 1, NQ
      I1 = I1 - LDYH
      DO 210 I = I1, NQNYH
  210 YH1(I) = YH1(I) + YH1(I+LDYH)
  220 CONTINUE
      CALL VSET
      RL1 = ONE/EL(2)
      RC = RC*(RL1/PRL1)
      PRL1 = RL1
c
c Call the nonlinear system solver. ------------------------------------
c
      CALL VNLS (Y, YH, LDYH, VSAV, SAVF, EWT, ACOR, IWM, WM, F, JAC, 
     &   PSOL, NFLAG, RPAR, IPAR)
c
      IF (NFLAG .EQ. 0) GO TO 450
c-----------------------------------------------------------------------
c The VNLS routine failed to achieve convergence (NFLAG .NE. 0).
c The YH array is retracted to its values before prediction.
c The step size H is reduced and the step is retried, if possible.
c Otherwise, an error exit is taken.
c-----------------------------------------------------------------------
      NCF = NCF + 1
      NCFN = NCFN + 1
      ETAMAX = ONE
      TN = TOLD
      I1 = NQNYH + 1
      DO 430 JB = 1, NQ
      I1 = I1 - LDYH
      DO 420 I = I1, NQNYH
  420 YH1(I) = YH1(I) - YH1(I+LDYH)
  430 CONTINUE
      IF (NFLAG .LT. -1) GO TO 680
      IF (ABS(H) .LE. HMIN*ONEPSM) GO TO 670
      IF (NCF .EQ. MXNCF) GO TO 670
      ETA = ETACF
      ETA = max(ETA,HMIN/ABS(H))
      NFLAG = -1
      GO TO 150
c-----------------------------------------------------------------------
c The corrector has converged (NFLAG = 0).  The local error test is
c made and control passes to statement 500 if it fails.
c-----------------------------------------------------------------------
  450 CONTINUE
      DSM = ACNRM/TQ(2)
c-----------------------------------------------------------------------
c This section is here to obtain information while the integrator ------
c is running,  The keywords are:
c              s       give information about the status
c              kaboom  returns to the user prompt, this option is useful
c                      when the solution failes to converge.
c This section was added by JLM 3/7/92
c-----------------------------------------------------------------------
ccTDR  Disable because PYTHON versions get stuck looking for signal 12/3/03?
ccTDR      ierrjm = ijmgetmr(msgjm,80,1,nrcv)
ccTDR      if (ierrjm .eq. 0) then
ccTDR         if (msgjm(1:nrcv).eq.'status' .or. msgjm(1:nrcv).eq.'s' ) then
ccTDR           big2 = 0.0e0
ccTDR           imxer2 = 1
ccTDR           do 452 i = 1,n
ccTDR              size2 = abs( acor(i)*ewt(i) )
ccTDR              if (big2 .ge. size2) go to 452
ccTDR              big2 = size2
ccTDR              imxer2 = i
ccTDR 452       continue
ccTDR           big3 = 0.0e0
ccTDR           imxer3 = 1
ccTDR           do 453 i = 1,n
ccTDR              size2 = abs( vsav(i)*ewt(i) )
ccTDR              if (big2 .ge. size2) go to 453
ccTDR              big3 = size2
ccTDR              imxer3 = i
ccTDR 453       continue
ccTDR            write(*,*) 'nfe = ', nfe, '   npe = ', nje, '   imxtstep = '
ccTDR     .           , imxer2,'   imxnewt = ', imxer3
ccTDR            write(*,*) 'time = ', tn-h, '   dt = ', h
ccTDR            write(*,*) 'bigts = ', big2, '   dsm = ', dsm
ccTDR         elseif(msgjm(1:nrcv).eq.'kaboom' .or. msgjm(1:nrcv).eq.'k')then
ccTDR            call xerrab("")
ccTDR         endif
ccTDR      endif
c-----------------------------------------------------------------------
      IF (DSM .GT. ONE) GO TO 500
c-----------------------------------------------------------------------
c After a successful step, update the YH and TAU arrays and decrement
c NQWAIT.  If NQWAIT is then 1 and NQ .lt. MAXORD, then ACOR is saved
c for use in a possible order increase on the next step.
c If ETAMAX = 1 (a failure occurred this step), keep NQWAIT .ge. 2.
c-----------------------------------------------------------------------
      KFLAG = 0
      NST = NST + 1
      HU = H
      NQU = NQ
      DO 470 IBACK = 1, NQ
      I = L - IBACK
  470 TAU(I+1) = TAU(I)
      TAU(1) = H
      DO 480 J = 1, L
      CALL daxpy_u(N, EL(J), ACOR, 1, YH(1,J), 1 )
  480 CONTINUE
      NQWAIT = NQWAIT - 1
      IF ((L .EQ. LMAX) .OR. (NQWAIT .NE. 1)) GO TO 490
      CALL dcopy_u(N, ACOR, 1, YH(1,LMAX), 1 )
      CONP = TQ(5)
  490 IF (ETAMAX .NE. ONE) GO TO 560
      IF (NQWAIT .LT. 2) NQWAIT = 2
      NEWQ = NQ
      NEWH = 0
      ETA = ONE
      HNEW = H
      GO TO 690
c-----------------------------------------------------------------------
c The error test failed.  KFLAG keeps track of multiple failures.
c Restore TN and the YH array to their previous values, and prepare
c to try the step again.  Compute the optimum step size for the
c same order.  After repeated failures, H is forced to decrease
c more rapidly.
c-----------------------------------------------------------------------
  500 KFLAG = KFLAG - 1
      NETF = NETF + 1
      NFLAG = -2
      TN = TOLD
      I1 = NQNYH + 1
      DO 520 JB = 1, NQ
      I1 = I1 - LDYH
      DO 510 I = I1, NQNYH
  510 YH1(I) = YH1(I) - YH1(I+LDYH)
  520 CONTINUE
      IF (ABS(H) .LE. HMIN*ONEPSM) GO TO 660
      ETAMAX = ONE
      IF (KFLAG .LE. KFC) GO TO 530
c Compute ratio of new H to current H at the current order. ------------
      FLOTL = dble(L)
      ETA = ONE/((BIAS2*DSM)**(ONE/FLOTL) + ADDON)
      ETA = max(ETA,HMIN/ABS(H),ETAMIN)
      IF ((KFLAG .LE. -2) .AND. (ETA .GT. ETAMXF)) ETA = ETAMXF
      GO TO 150
c-----------------------------------------------------------------------
c Control reaches this section if 3 or more consecutive failures
c have occurred.  It is assumed that the elements of the YH array
c have accumulated errors of the wrong order.  The order is reduced
c by one, if possible.  Then H is reduced by a factor of 0.1 and
c the step is retried.  After a total of 7 consecutive failures,
c an exit is taken with KFLAG = -1.
c-----------------------------------------------------------------------
  530 IF (KFLAG .EQ. KFH) GO TO 660
      IF (NQ .EQ. 1) GO TO 540
      ETA = max(ETAMIN,HMIN/ABS(H))
      CALL VJUST (YH, LDYH, -1)
      L = NQ
      NQ = NQ - 1
      NQWAIT = L
      GO TO 150
  540 ETA = max(ETAMIN,HMIN/ABS(H))
      H = H*ETA
      HSCAL = H
      TAU(1) = H
      IFAIL = 0
      CALL F (N, TN, Y, SAVF, RPAR, IPAR, IFAIL)
      NFE = NFE + 1
      IF (IFAIL .NE. 0) GO TO 670
      DO 550 I = 1, N
  550 YH(I,2) = H*SAVF(I)
      NQWAIT = 10
      GO TO 200
c-----------------------------------------------------------------------
c If NQWAIT = 0, an increase or decrease in order by one is considered.
c Factors ETAQ, ETAQM1, ETAQP1 are computed by which H could
c be multiplied at order q, q-1, or q+1, respectively.
c The largest of these is determined, and the new order and
c step size set accordingly.
c A change of H or NQ is made only if H increases by at least a
c factor of THRESH.  If an order change is considered and rejected,
c then NQWAIT is set to 2 (reconsider it after 2 steps).
c-----------------------------------------------------------------------
c Compute ratio of new H to current H at the current order. ------------
  560 FLOTL = dble(L)
      ETAQ = ONE/((BIAS2*DSM)**(ONE/FLOTL) + ADDON)
      IF (NQWAIT .NE. 0) GO TO 600
      NQWAIT = 2
      ETAQM1 = ZERO
      IF (NQ .EQ. 1) GO TO 570
c Compute ratio of new H to current H at the current order less one. ---
      DDN = VNORML (N, YH(1,L), EWT)/TQ(1)
      ETAQM1 = ONE/((BIAS1*DDN)**(ONE/(FLOTL - ONE)) + ADDON)
  570 ETAQP1 = ZERO
      IF (L .EQ. LMAX) GO TO 580
c Compute ratio of new H to current H at current order plus one. -------
      CNQUOT = (TQ(5)/CONP)*(H/TAU(2))**L
      DO 575 I = 1, N
  575 SAVF(I) = ACOR(I) - CNQUOT*YH(I,LMAX)
      DUP = VNORML (N, SAVF, EWT)/TQ(3)
      ETAQP1 = ONE/((BIAS3*DUP)**(ONE/(FLOTL + ONE)) + ADDON)
  580 IF (ETAQ .GE. ETAQP1) GO TO 590
      IF (ETAQP1 .GT. ETAQM1) GO TO 620
      GO TO 610
  590 IF (ETAQ .LT. ETAQM1) GO TO 610
  600 ETA = ETAQ
      NEWQ = NQ
      GO TO 630
  610 ETA = ETAQM1
      NEWQ = NQ - 1
      GO TO 630
  620 ETA = ETAQP1
      NEWQ = NQ + 1
      CALL dcopy_u(N, ACOR, 1, YH(1,LMAX), 1)
c Test tentative new H against THRESH, ETAMAX, and HMXI, then exit. ----
  630 IF (ETA .LT. THRESH .OR. ETAMAX .EQ. ONE) GO TO 640
      ETA = min(ETA,ETAMAX)
      ETA = ETA/max(ONE,ABS(H)*HMXI*ETA)
      NEWH = 1
      HNEW = H*ETA
      GO TO 690
  640 NEWQ = NQ
      NEWH = 0
      ETA = ONE
      HNEW = H
      GO TO 690
c-----------------------------------------------------------------------
c All returns are made through this section.
c On a successful return, ETAMAX is reset and ACOR is scaled.
c-----------------------------------------------------------------------
  660 KFLAG = -1
      GO TO 720
  670 KFLAG = -2
      IF (IFAIL .NE. 0) KFLAG = -5
      GO TO 720
  680 IF (NFLAG .EQ. -2) KFLAG = -3
      IF (NFLAG .EQ. -3) KFLAG = -4
      IF (NFLAG .EQ. -4) KFLAG = -5
      GO TO 720
  690 ETAMAX = ETAMX3
      IF (NST .LE. 10) ETAMAX = ETAMX2
  700 R = ONE/TQ(2)
      CALL dscal_u(N, R, ACOR, 1)
  720 JSTART = 1
      RETURN
c----------------------- End of Subroutine VSTEP -----------------------
      END
      SUBROUTINE VSET
c-----------------------------------------------------------------------
c Call sequence communication.. None
c COMMON block variables accessed..
c     /VOD001/ -- EL(13), H, TAU(13), TQ(5), L(= NQ + 1),
c                 METH, NQ, NQWAIT
c
c Subroutines called by VSET.. None
c Function routines called by VSET.. None
c-----------------------------------------------------------------------
c VSET is called by VSTEP and sets coefficients for use there.
c
c For each order NQ, the coefficients in EL are calculated by use of
c  the generating polynomial lambda(x), with coefficients EL(i).
c      lambda(x) = EL(1) + EL(2)*x + ... + EL(NQ+1)*(x**NQ).
c For the backward differentiation formulas,
c                                     NQ-1
c      lambda(x) = (1 + x/xi*(NQ)) * product (1 + x/xi(i) ) .
c                                     i = 1
c For the Adams formulas,
c                              NQ-1
c      (d/dx) lambda(x) = c * product (1 + x/xi(i) ) ,
c                              i = 1
c      lambda(-1) = 0,    lambda(0) = 1,
c where c is a normalization constant.
c In both cases, xi(i) is defined by
c      H*xi(i) = t sub n  -  t sub (n-i)
c              = H + TAU(1) + TAU(2) + ... TAU(i-1).
c
c
c In addition to variables described previously, communication
c with VSET uses the following..
c   TAU    = A vector of length 13 containing the past NQ values
c            of H.
c   EL     = A vector of length 13 in which vset stores the
c            coefficients for the corrector formula.
c   TQ     = A vector of length 5 in which vset stores constants
c            used for the convergence test, the error test, and the
c            selection of H at a new order.
c   METH   = The basic method indicator.
c   NQ     = The current order.
c   L      = NQ + 1, the length of the vector stored in EL, and
c            the number of columns of the YH array being used.
c   NQWAIT = A counter controlling the frequency of order changes.
c            An order change is about to be considered if NQWAIT = 1.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for local variables --------------------------------
c
      doubleprecision AHATN0, ALPH0, CNQM1, CORTES, CSUM, ELP, EM, EM0, 
     &   FLOTI, FLOTL, FLOTNQ, HSUM, ONE, RXI, RXIS, S, SIX, T1, T2, T3, 
     &   T4, T5, T6, TWO, XI, ZERO
      INTEGER I, IBACK, J, JP1, NQM1, NQM2
c
      DIMENSION EM(13)
c-----------------------------------------------------------------------
c The following Fortran-77 declaration is to cause the values of the
c listed (local) variables to be saved between calls to this integrator.
c-----------------------------------------------------------------------
      SAVE CORTES, ONE, SIX, TWO, ZERO
c
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
c
      DATA CORTES /0.1d0/
      DATA ONE /1.0d0/, SIX /6.0d0/, TWO /2.0d0/, ZERO /0.0d0/
c
      FLOTL = dble(L)
      NQM1 = NQ - 1
      NQM2 = NQ - 2
      GO TO (100, 200), METH
c
c Set coefficients for Adams methods. ----------------------------------
  100 IF (NQ .NE. 1) GO TO 110
      EL(1) = ONE
      EL(2) = ONE
      TQ(1) = ONE
      TQ(2) = TWO
      TQ(3) = SIX*TQ(2)
      TQ(5) = ONE
      GO TO 300
  110 HSUM = H
      EM(1) = ONE
      FLOTNQ = FLOTL - ONE
      DO 115 I = 2, L
  115 EM(I) = ZERO
      DO 150 J = 1, NQM1
      IF ((J .NE. NQM1) .OR. (NQWAIT .NE. 1)) GO TO 130
      S = ONE
      CSUM = ZERO
      DO 120 I = 1, NQM1
      CSUM = CSUM + S*EM(I)/dble(I+1)
  120 S = -S
      TQ(1) = EM(NQM1)/(FLOTNQ*CSUM)
  130 RXI = H/HSUM
      DO 140 IBACK = 1, J
      I = (J + 2) - IBACK
  140 EM(I) = EM(I) + EM(I-1)*RXI
      HSUM = HSUM + TAU(J)
  150 CONTINUE
c Compute integral from -1 to 0 of polynomial and of x times it. -------
      S = ONE
      EM0 = ZERO
      CSUM = ZERO
      DO 160 I = 1, NQ
      FLOTI = dble(I)
      EM0 = EM0 + S*EM(I)/FLOTI
      CSUM = CSUM + S*EM(I)/(FLOTI+ONE)
  160 S = -S
c In EL, form coefficients of normalized integrated polynomial. --------
      S = ONE/EM0
      EL(1) = ONE
      DO 170 I = 1, NQ
  170 EL(I+1) = S*EM(I)/dble(I)
      XI = HSUM/H
      TQ(2) = XI*EM0/CSUM
      TQ(5) = XI/EL(L)
      IF (NQWAIT .NE. 1) GO TO 300
c For higher order control constant, multiply polynomial by 1+x/xi(q). -
      RXI = ONE/XI
      DO 180 IBACK = 1, NQ
      I = (L + 1) - IBACK
  180 EM(I) = EM(I) + EM(I-1)*RXI
c Compute integral of polynomial. --------------------------------------
      S = ONE
      CSUM = ZERO
      DO 190 I = 1, L
      CSUM = CSUM + S*EM(I)/dble(I+1)
  190 S = -S
      TQ(3) = FLOTL*EM0/CSUM
      GO TO 300
c
c Set coefficients for BDF methods. ------------------------------------
  200 DO 210 I = 3, L
  210 EL(I) = ZERO
      EL(1) = ONE
      EL(2) = ONE
      ALPH0 = -ONE
      AHATN0 = -ONE
      HSUM = H
      RXI = ONE
      RXIS = ONE
      IF (NQ .EQ. 1) GO TO 240
      DO 230 J = 1, NQM2
c In EL, construct coefficients of (1+x/xi(1))*...*(1+x/xi(j+1)). ------
      HSUM = HSUM + TAU(J)
      RXI = H/HSUM
      JP1 = J + 1
      ALPH0 = ALPH0 - ONE/dble(JP1)
      DO 220 IBACK = 1, JP1
      I = (J + 3) - IBACK
  220 EL(I) = EL(I) + EL(I-1)*RXI
  230 CONTINUE
      ALPH0 = ALPH0 - ONE/dble(NQ)
      RXIS = -EL(2) - ALPH0
      HSUM = HSUM + TAU(NQM1)
      RXI = H/HSUM
      AHATN0 = -EL(2) - RXI
      DO 235 IBACK = 1, NQ
      I = (NQ + 2) - IBACK
  235 EL(I) = EL(I) + EL(I-1)*RXIS
  240 T1 = ONE - AHATN0 + ALPH0
      T2 = ONE + dble(NQ)*T1
      TQ(2) = ABS(ALPH0*T2/T1)
      TQ(5) = ABS(T2/(EL(L)*RXI/RXIS))
      IF (NQWAIT .NE. 1) GO TO 300
      CNQM1 = RXIS/EL(L)
      T3 = ALPH0 + ONE/dble(NQ)
      T4 = AHATN0 + RXI
      ELP = T3/(ONE - T4 + T3)
      TQ(1) = ABS(ELP/CNQM1)
      HSUM = HSUM + TAU(NQ)
      RXI = H/HSUM
      T5 = ALPH0 - ONE/dble(NQ+1)
      T6 = AHATN0 - RXI
      ELP = T2/(ONE - T6 + T5)
      TQ(3) = ABS(ELP*RXI*(FLOTL + ONE)*T5)
  300 TQ(4) = CORTES*TQ(2)
      RETURN
c----------------------- End of Subroutine VSET ------------------------
      END
      SUBROUTINE VJUST (YH, LDYH, IORD)
      doubleprecision YH
      INTEGER LDYH, IORD
      DIMENSION YH(LDYH,*)
c-----------------------------------------------------------------------
c Call sequence input -- YH, LDYH, IORD
c Call sequence output -- YH
c COMMON block input -- NQ, METH, LMAX, HSCAL, TAU(13), N
c COMMON block variables accessed..
c     /VOD001/ -- HSCAL, TAU(13), LMAX, METH, N, NQ,
c
c Subroutines called by VJUST.. SAXPY
c Function routines called by VJUST.. None
c-----------------------------------------------------------------------
c This subroutine adjusts the YH array on reduction of order,
c and also when the order is increased for the stiff option (METH = 2).
c Communication with VJUST uses the following..
c IORD  = An integer flag used when METH = 2 to indicate an order
c         increase (IORD = +1) or an order decrease (IORD = -1).
c HSCAL = Step size H used in scaling of Nordsieck array YH.
c         (If IORD = +1, VJUST assumes that HSCAL = TAU(1).)
c See References 1 and 2 for details.
c-----------------------------------------------------------------------
c
c Type declarations for labeled COMMON block VOD001 --------------------
c
      doubleprecision ACNRM, CCMXJ, CONP, CRATE, DRC, EL, ETA, ETAMAX, H
     &   , HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU, TQ, TN, UROUND
      INTEGER ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH, L, LMAX, 
     &   LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, METH, MITER, 
     &   MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, NQNYH, NQWAIT, 
     &   NSLJ, NSLP, NYH
c
c Type declarations for local variables --------------------------------
c
      doubleprecision ALPH0,ALPH1, HSUM, ONE, PROD, T1, XI,XIOLD, ZERO
      INTEGER I, IBACK, J, JP1, LP1, NQM1, NQM2, NQP1
c-----------------------------------------------------------------------
c The following Fortran-77 declaration is to cause the values of the
c listed (local) variables to be saved between calls to this integrator.
c-----------------------------------------------------------------------
      SAVE ONE, ZERO
c
      COMMON /VOD001/ ACNRM, CCMXJ, CONP, CRATE, DRC, EL(13), ETA, 
     &   ETAMAX, H, HMIN, HMXI, HNEW, HSCAL, PRL1, RC, RL1, TAU(13), TQ(
     &   5), TN, UROUND, ICF, INIT, IPUP, JCUR, JSTART, JSV, KFLAG, KUTH
     &   , L, LMAX, LYH, LEWT, LACOR, LSAVF, LWM, LIWM, LOCJS, MAXORD, 
     &   METH, MITER, MSBJ, MXHNIL, MXSTEP, N, NEWH, NEWQ, NHNIL, NQ, 
     &   NQNYH, NQWAIT, NSLJ, NSLP, NYH
c
      DATA ONE /1.0d0/, ZERO /0.0d0/
c
      IF ((NQ .EQ. 2) .AND. (IORD .NE. 1)) RETURN
      NQM1 = NQ - 1
      NQM2 = NQ - 2
      GO TO (100, 200), METH
c-----------------------------------------------------------------------
c Nonstiff option...
c Check to see if the order is being increased or decreased.
c-----------------------------------------------------------------------
  100 CONTINUE
      IF (IORD .EQ. 1) GO TO 180
c Order decrease. ------------------------------------------------------
      DO 110 J = 1, LMAX
  110 EL(J) = ZERO
      EL(2) = ONE
      HSUM = ZERO
      DO 130 J = 1, NQM2
c Construct coefficients of x*(x+xi(1))*...*(x+xi(j)). -----------------
      HSUM = HSUM + TAU(J)
      XI = HSUM/HSCAL
      JP1 = J + 1
      DO 120 IBACK = 1, JP1
      I = (J + 3) - IBACK
  120 EL(I) = EL(I)*XI + EL(I-1)
  130 CONTINUE
c Construct coefficients of integrated polynomial. ---------------------
      DO 140 J = 2, NQM1
  140 EL(J+1) = dble(NQ)*EL(J)/dble(J)
c Subtract correction terms from YH array. -----------------------------
      DO 170 J = 3, NQ
      DO 160 I = 1, N
  160 YH(I,J) = YH(I,J) - YH(I,L)*EL(J)
  170 CONTINUE
      RETURN
c Order increase. ------------------------------------------------------
c Zero out next column in YH array. ------------------------------------
  180 CONTINUE
      LP1 = L + 1
      DO 190 I = 1, N
  190 YH(I,LP1) = ZERO
      RETURN
c-----------------------------------------------------------------------
c Stiff option...
c Check to see if the order is being increased or decreased.
c-----------------------------------------------------------------------
  200 CONTINUE
      IF (IORD .EQ. 1) GO TO 300
c Order decrease. ------------------------------------------------------
      DO 210 J = 1, LMAX
  210 EL(J) = ZERO
      EL(3) = ONE
      HSUM = ZERO
      DO 230 J = 1, NQM2
c Construct coefficients of x*x*(x+xi(1))*...*(x+xi(j)). ---------------
      HSUM = HSUM + TAU(J)
      XI = HSUM/HSCAL
      JP1 = J + 1
      DO 220 IBACK = 1, JP1
      I = (J + 4) - IBACK
  220 EL(I) = EL(I)*XI + EL(I-1)
  230 CONTINUE
c Subtract correction terms from YH array. -----------------------------
      DO 250 J = 3, NQ
      DO 240 I = 1, N
  240 YH(I,J) = YH(I,J) - YH(I,L)*EL(J)
  250 CONTINUE
      RETURN
c Order increase. ------------------------------------------------------
  300 DO 310 J = 1, LMAX
  310 EL(J) = ZERO
      EL(3) = ONE
      ALPH0 = -ONE
      ALPH1 = ONE
      PROD = ONE
      XIOLD = ONE
      HSUM = HSCAL
      IF (NQ .EQ. 1) GO TO 340
      DO 330 J = 1, NQM1
c Construct coefficients of x*x*(x+xi(1))*...*(x+xi(j)). ---------------
      JP1 = J + 1
      HSUM = HSUM + TAU(JP1)
      XI = HSUM/HSCAL
      PROD = PROD*XI
      ALPH0 = ALPH0 - ONE/dble(JP1)
      ALPH1 = ALPH1 + ONE/XI
      DO 320 IBACK = 1, JP1
      I = (J + 4) - IBACK
  320 EL(I) = EL(I)*XIOLD + EL(I-1)
      XIOLD = XI
  330 CONTINUE
  340 CONTINUE
      T1 = (-ALPH0 - ALPH1)/PROD
c Load column L + 1 in YH array. ---------------------------------------
      LP1 = L + 1
      DO 350 I = 1, N
  350 YH(I,LP1) = T1*YH(I,LMAX)
c Add correction terms to YH array. ------------------------------------
      NQP1 = NQ + 1
      DO 370 J = 3, NQP1
      CALL daxpy_u(N, EL(J), YH(1,LP1), 1, YH(1,J), 1 )
  370 CONTINUE
      RETURN
c----------------------- End of Subroutine VJUST -----------------------
      END
      doubleprecision FUNCTION VNORML (N, V, W)
      doubleprecision V, W
      INTEGER N
      DIMENSION V(N), W(N)
c-----------------------------------------------------------------------
c Call sequence input -- N, V, W
c Call sequence output -- None
c COMMON block variables accessed -- None
c
c Subroutines/functions called by VNORML.. None
c-----------------------------------------------------------------------
c This function routine computes the weighted root-mean-square norm
c of the vector of length N contained in the array V, with weights
c contained in the array W of length N..
c     VNORML = sqrt( (1/N) * sum( V(i)*W(i) )**2 )
cCC commented section can calculate the maximum of V(i)*W(i)  TDR 05/27/92
c-----------------------------------------------------------------------
      doubleprecision SUM, big, size
      INTEGER I
      big = 0.0d0
      do 10 I = 1, N
         size = abs( V(I)*W(I) )
         if (big .ge. size) go to 10
         big = size
   10    continue
      VNORML = big
c
ccc      SUM = 0.0E0
ccc         DO 10 I = 1, N
ccc  10     SUM = SUM + (V(I)*W(I))**2
ccc      VNORML = SQRT(SUM/float(N))
      RETURN
c----------------------- End of Function VNORML -------------------------
      END
