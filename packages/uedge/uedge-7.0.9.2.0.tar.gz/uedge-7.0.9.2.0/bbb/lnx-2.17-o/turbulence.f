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
c     ./../turbulence.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c






















































































































































c!include "../mppl.h"
c-----------------------------------------------------------------------
      subroutine turb_diffus (btotyf, lte, lpi, teyf, tiyf, neyf, ted, 
     &   tid, densd, mhyd, zavg, linelen, chi, lmodechin, hmodechin)
cProlog
c ... Calculate anomalous radial diffusivity caused by turbulence.

      implicit none

c ... Input arguments:
c total B at y-face
      doubleprecision btotyf
c radial scale lengths of Te and ion pressure
      doubleprecision lte, lpi
c Te, Ti, and ne at y-face
      doubleprecision teyf, tiyf, neyf
c Te, Ti, and ne at divertor plate
      doubleprecision ted, tid, densd
c mass of hydrogenic ions
      doubleprecision mhyd
c mean ion charge
      doubleprecision zavg
c field-line length typical of SOL
      doubleprecision linelen

c ... Output arguments:
c diffusivity (SI units)
      doubleprecision chi
c normalized diffusivities
      doubleprecision lmodechin, hmodechin

c ... Common blocks:
c Group Phyvar
      double precision pi, me, mp, ev, qe, mu0, eps0, rt8opi
      common /bbb173/ pi, me, mp, ev, qe, mu0, eps0, rt8opi
c End of Phyvar
c ev
c Group Turbulence
      double precision kappabar, lambdan, lambdat, gammasi, lambdap
      double precision maxmag_lmode, kybeg, kyend, kya, kyb, tol_lmode
      integer suppress_lmode, nky, iprint_lmode, isturbnloc, isturbcons
      double precision diffusrange, diffuswgts(-9:9), gradvconst
      integer diffuslimit, islmodebeta
      common /bbb200/ suppress_lmode, nky, iprint_lmode, isturbnloc
      common /bbb200/ isturbcons, diffuslimit, islmodebeta
      common /bbb203/ kappabar, lambdan, lambdat, gammasi, lambdap
      common /bbb203/ maxmag_lmode, kybeg, kyend, kya, kyb, tol_lmode
      common /bbb203/ diffusrange, diffuswgts, gradvconst
c End of Turbulence
c gammasi,kappabar,lambdap,
c suppress_lmode,maxmag_lmode,
c nky,kybeg,kyend,kya,kyb,
c iprint_lmode,tol_lmode,islmodebeta,
c gradvconst

c ... Local variables:
      doubleprecision rhos
      doubleprecision cubrtnu, epsilon, csed
      doubleprecision betad, kt
      doubleprecision gammamax, kymax

c ... Calculate quantities dependent on variables at plates.
      rhos = sqrt(mhyd * ted) / (ev * btotyf)
      cubrtnu = (2.d0 * densd * (1.d0 + gammasi) * sqrt(1.d0 + (tid / 
     &   ted)) * zavg * lte / (neyf * lambdap * linelen)) ** 
     &   0.333333333333333d0
c ... The 1.e-7 factor below accounts for use of MKS rather than cgs
      betad = 8.d-7 * 3.14159265358979323d0 * densd * (ted + tid) / 
     &   btotyf**2
      kt = (1.d0 + gammasi) * zavg * sqrt(0.5d0 * betad * lambdan) / 
     &   cubrtnu**2

c ... Calculate normalized L-mode diffusivity lmodechin.
      if (suppress_lmode .eq. 1) then
         lmodechin = 0.d0
         gammamax = 0.d0
         kymax = 0.d0
      else
         call lmode_chi_norm (kappabar, lte, rhos, cubrtnu, tiyf/ev, ted
     &      /ev, zavg, lpi, lambdap, maxmag_lmode, nky, kybeg, kyend, 
     &      kya, kyb, tol_lmode, iprint_lmode, islmodebeta, kt, 
     &      lmodechin, gammamax, kymax)
      endif

c ... Calculate normalized H-mode diffusivity hmodechin.
      epsilon = rhos / lte
      call hmode_chi_norm (gradvconst, cubrtnu, epsilon, lambdap, 
     &   hmodechin)

c ... Convert from normalized to dimensional diffusivity chi.
      csed = sqrt(ted / mhyd)
      call turb_chi (lmodechin, hmodechin, rhos, csed, lte, lambdap, 
     &   cubrtnu, chi)

      return
      end
c****** end of subroutine turb_diffus ************
c-----------------------------------------------------------------------
      subroutine lmode_chi_norm (kappabar, lte, rhos, cubrtnuarg, ti0, 
     &   ted, zavg, lpi, lambdap, maxmag, nky, kybeg, kyend, kya, kyb, 
     &   tol, iprint, islmodebeta, kt, lmodechin, gammamax, kymax)
cProlog

c ... Calculate normalized L-mode transport coefficient chi by
c     maximizing growth rate as a function of ky.

      implicit none

c ... Input arguments:
c field-line-averaged curvature [1/m]
      doubleprecision kappabar
c L_Te = Ted / (dTed / dr0) [m]
      doubleprecision lte
c ion gyroradius at Ted [m]
      doubleprecision rhos
c cube root of collisionality nu
      doubleprecision cubrtnuarg
c Ti at "mid-plane" [eV]
      doubleprecision ti0
c Te at divertor plate [eV]
      doubleprecision ted
c average Z
      doubleprecision zavg
c Pi / (dPi / dr) at "mid-plane" [m]
      doubleprecision lpi
c e (dPhi0 / dr0) / (dTed / dr0)
      doubleprecision lambdap
c max magnitude of parab. step in bracketing ky
      doubleprecision maxmag
c number of ky's used in maximizing growth rate
      integer nky
c lower limit of acceptable kymax [none]
      doubleprecision kybeg
c upper limit of acceptable kymax [none]
      doubleprecision kyend
c one initial point in search for kymax [none]
      doubleprecision kya
c other initial point in search for kymax [none]
      doubleprecision kyb
c abs & rel tolerance in search for kymax
      doubleprecision tol
      integer iprint
c =1 to turn on finite-beta correction
      integer islmodebeta
c parameter in finite-beta correction [none]
      doubleprecision kt

c ... Output arguments:
      doubleprecision lmodechin
c maximum growth rate
      doubleprecision gammamax
c ky at maximum growth rate
      doubleprecision kymax

c ... Common block:
c Group Turbulence_comm
      double precision epsilon, turbdelta, ssqthsqavg, kxconst, cubrtnu
      double complex bcoef0, ccoef1
      double precision ccoef2, ccoef3
      common /bbb213/ epsilon, turbdelta, ssqthsqavg, kxconst, cubrtnu
      common /bbb213/ ccoef2, ccoef3
      common /bbb214/ bcoef0, ccoef1
c End of Turbulence_comm
c ssqthsqavg,kxconst,epsilon,turbdelta,
c cubrtnu,bcoef0,ccoef1,ccoef2,ccoef3

c ... Local variables:
      doubleprecision third, fivo6
      double complex ci
      doubleprecision kappa, kxsq
      doubleprecision a, b, c, fa, fb, fc
      integer gcona, gconb, gn

c ... External function:
      external brent, lmode_funct
      doubleprecision brent, lmode_funct

c ... Set constants.
      third = 1.d0/3.d0
      fivo6 = third + 0.5d0
      ci = dcmplx(0.d0, 1.d0)

c ... Copy an argument to the common block for communication to the
c     minimization routine.
      cubrtnu = cubrtnuarg

c ... Calculate variables that are independent of ky.
      kappa = 2.d0 * (2.d0 * ti0 / ted) * kappabar * lte
      epsilon = rhos / lte
      turbdelta = (ti0 / ted) * lte / (zavg * lpi * lambdap)

c ... Calculate terms and factors that enter coefficients in normalized
c     dispersion relation for L-mode turbulence.
      bcoef0 = third * ci * (lambdap * cubrtnu)**2
      ccoef1 = 2.d0 * bcoef0 * turbdelta
      ccoef2 = fivo6 * lambdap * cubrtnu**2
      ccoef3 = kappa / (cubrtnu * lambdap)**2

c ... Find maximum growth rate by varying ky using Numerical Recipes
c     routines.
      a = kya
      b = kyb
      call mnbrak (iprint, maxmag, a, b, c, fa, fb, fc, lmode_funct)
      gammamax = -brent (iprint, nky, a, b, c, lmode_funct, tol, kymax)
      if (kymax .lt. kybeg) then
         write(*,90) '*** Max. growth rate for L-mode turbulence', 
     &      ' found at ky < kybeg = ', kybeg
         call xerrab("")
      endif
      if (kymax .gt. kyend) then
         write(*,90) '*** Max. growth rate for L-mode turbulence', 
     &      ' found at ky > kyend = ', kyend
         call xerrab("")
      endif
   90 format(a,a,f6.3)

c ... Compute normalized L-mode chi.
      kxsq = ssqthsqavg * kymax**2 + kxconst * (epsilon / cubrtnu)**2
      lmodechin = max(0.d0, gammamax) / kxsq

c ... Apply finite-k_parallel (finite-beta) correction, if selected.
      if (islmodebeta .eq. 1) then
         gcona = 0.346203d0
         gconb = 0.0008d0
         if (kt .lt. 3.d0) then
            gn = exp(-gcona * kt**2 / (1.d0 + gconb * kt**4))
         else
            gn = 0.d0
         endif
         lmodechin = lmodechin * gn
      endif

      return
      end
c-----------------------------------------------------------------------
      doubleprecision function lmode_funct (ky)
cProlog

c ... Return -1 times the growth rate, given ky.

      implicit none

c ... Input variable:
c normalized poloidal wave number
      doubleprecision ky

c ... Common block:
c Group Turbulence_comm
      double precision epsilon, turbdelta, ssqthsqavg, kxconst, cubrtnu
      double complex bcoef0, ccoef1
      double precision ccoef2, ccoef3
      common /bbb213/ epsilon, turbdelta, ssqthsqavg, kxconst, cubrtnu
      common /bbb213/ ccoef2, ccoef3
      common /bbb214/ bcoef0, ccoef1
c End of Turbulence_comm
c ssqthsqavg,kxconst,epsilon,turbdelta,
c cubrtnu,bcoef0,ccoef1,ccoef2,ccoef3

c ... Local variables:
      doubleprecision kysq, kxsq, ksq
      double complex ci
      double complex bcoef, ccoef
      double complex omega(2)

c ... Set constant.
      ci = dcmplx(0.d0, 1.d0)

c ... Calculate local variables that are dependent on ky.
      kysq = ky**2
      kxsq = ssqthsqavg * kysq + kxconst * (epsilon / cubrtnu)**2
      ksq = kxsq + kysq

c ... Calculate coefficients in normalized dispersion relation for
c     L-mode turbulence.
      bcoef = bcoef0 + 0.5d0 * (turbdelta * ky + ci / ksq)
      ccoef = ccoef1 * ky - (ccoef2 + ci * ky - ccoef3 * kysq) / ksq

c ... Calculate normalized roots of the L-mode dispersion relation
      call lmode_roots (bcoef, ccoef, omega)

c ... Return -1 times growth rate.
      lmode_funct = -dimag(omega(1))

      return
      end
c-----------------------------------------------------------------------
      subroutine lmode_roots (bcoef, ccoef, omega)
cProlog

c ... Calculate normalized roots of the L-mode dispersion relation,
c     given the coefficients.  Root with larger growth rate is returned
c     in omega(1).

      implicit none

c ... Input arguments:
      double complex bcoef, ccoef

c ... Output argument:
      double complex omega(2)

c ... Local variable:
      double complex discrim

c ... Use quadratic formula to evaluate roots for quadratic of the form
c        omega**2 + 2*b*omega + c = 0
      discrim = sqrt(bcoef**2 - ccoef)
      omega(1) = -bcoef + discrim
      omega(2) = -bcoef - discrim

c ... Interchange roots if necessary to get faster growing root in
c     omega(1).
      if (dimag(omega(1)) .lt. dimag(omega(2))) then
         discrim = omega(1)
         omega(1) = omega(2)
         omega(2) = discrim
      endif

      return
      end
c-----------------------------------------------------------------------
      subroutine hmode_chi_norm (gradvconst, cubrtnu, epsilon, lambdap, 
     &   hmodechin)
cProlog

c ... Calculate normalized H-mode transport coefficient chi.

      implicit none

c ... Input arguments:
c factor involving rad. grad. of v(parallel)
      doubleprecision gradvconst
c cube root of collisionality nu
      doubleprecision cubrtnu
c rhos / L_Te
      doubleprecision epsilon
c e (dPhi0 / dr0) / (dTed / dr0)
      doubleprecision lambdap

c ... Output argument:
c normalized chi for H-mode turbulence
      doubleprecision hmodechin

      hmodechin = gradvconst * cubrtnu / (epsilon * lambdap)

      return
      end
c-----------------------------------------------------------------------
      subroutine turb_chi (lmodechin, hmodechin, rhos, csed, lte, 
     &   lambdap, cubrtnu, chi)
cProlog

c ... Calculate turbulent transport coefficient chi by multiplying
c     normalization constants by sum of normalized chi's from turbulence
c     presumed to dominate in L and H modes.

      implicit none

c ... Input arguments:
c normalized chi for L-mode turbulence
      doubleprecision lmodechin
c normalized chi for H-mode turbulence
      doubleprecision hmodechin
c ion gyroradius at Ted [m]
      doubleprecision rhos
c sound speed cs at divertor plate [m/s]
      doubleprecision csed
c Ted / (dTed / dr0) [m]
      doubleprecision lte
c e (dPhi0 / dr0) / (dTed / dr0)
      doubleprecision lambdap
c cube root of collisionality nu
      doubleprecision cubrtnu

c ... Output argument:
c turbulent transport coefficient chi (SI units)
      doubleprecision chi

      chi = rhos**2 * (csed / lte) * (lambdap / cubrtnu) * (lmodechin + 
     &   hmodechin)

      return
      end
