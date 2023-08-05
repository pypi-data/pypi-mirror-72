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
c     ./../convert.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c






















































































































































c-----------------------------------------------------------------------
      subroutine convert
cProlog

c     CONVERT changes from fluid variables inteo variables by solvers.
c     It also calculates the tolerances and the indexes for the cuts.

      implicit none

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nisp,nusp,ngsp
c Group Math_problem_size
      integer neqmx, numvar, numvarbwpad
      common /bbb10/ neqmx, numvar, numvarbwpad
c End of Math_problem_size
c neqmx
c Group UEpar
      double precision csfaclb(31,2), csfacrb(31,2)
      integer methe, methu, methn, methi, methg, methp, isgxvon
      double precision csfacti, cslim, dcslim, lnlam, cfaccony, isvylog
      double precision cniatol, cngatol, cupatol, cteatol, ctiatol
      integer ishavisy, isintlog, concap, convis, icnuiz, icnucx
      double precision cphiatol, tolbf, tadj, cnuiz, cnucx, cfrecom
      double precision ngbackg(6), cflbg, facngbackg2ngs(6)
      double precision nzbackg(31), facnzbackg2nis(31)
      double precision upclng(31), facupclng2ups(31), tebg, tibg
      double precision temin, temin2, pwrbkg_c, pwribkg_c, cfwjdotelim
      double precision nlimix(31), nlimiy(31), nlimgx, nlimgy
      double precision xgbx, agdc, pcolwid, eion, ediss, ebind, tfcx
      integer isrecmon, igas, ingb, inflbg, inzb, iteb, is1D_gbx, ixgb
      double precision tfcy, afix, coef, ce, ci, dp1, qfl, csh, qsh, mfl
      double precision msh, ro, cs, fxe, ctaue, fxi, ctaui, zcoef, coef1
      double precision cnurn, cnuru, cnure, cnuri, cnurg, cnurp, nurlxn
      character*72 label
      double precision nurlxu, nurlxe, nurlxi, nurlxg, nurlxp, rnewpot
      character*8 svrpkg
      character*80 petscoptfile
      character*2048 petscopts
      integer ncrhs, istep, iter, ishymol, isfqpave, isgpye, iigsp
      integer itrap_negni, itrap_negt, itrap_negng, isybdryog, isybdrywd
      double precision r0slab, te_s_dis, fnnuiz, thetar, iseesorave
      integer isxmpog, iexclnxc1, ineudif, isbcwdt, ishosor, issyvxpt0
      integer isrrvave, isdtsfscal, isplflxl, isplflxlv, isplflxlgx
      integer isplflxlgxy, iswflxlgy, isplflxlvgx, isplflxlvgxy
      double precision ispsorave, fsprd, rr_fac, rrmin, frfqpn, cffqpsat
      integer iswflxlvgy, isplflxltgx, isplflxltgxy, iswflxltgy
      integer isfeexpl0, isfeixpl0, isofric, iskaboom, isnglf, isngrf
      double precision flalfipl, flalfepl, del_te_ro, nglfix, ngrfix
      integer isnion(31), isupon(31), isup1up2, isupgon(6)
      integer isteon, istion, isngon(6), istgon(6), isphion
      integer isphiofft, isnewpot, isugfm1side, isnupdot1sd, isphicore0
      double precision rup21, z0_imp_const
      integer is_z0_imp_const

      integer isnionxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisnionxy,isnionxy)

      integer isuponxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisuponxy,isuponxy)

      integer isteonxy ( 0:nx+1,0:ny+1)
      pointer(pisteonxy,isteonxy)

      integer istionxy ( 0:nx+1,0:ny+1)
      pointer(pistionxy,istionxy)

      integer isngonxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pisngonxy,isngonxy)

      integer istgonxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pistgonxy,istgonxy)

      integer isphionxy ( 0:nx+1,0:ny+1)
      pointer(pisphionxy,isphionxy)

      integer isnioffxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisnioffxy,isnioffxy)

      integer isupoffxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisupoffxy,isupoffxy)

      integer isteoffxy ( 0:nx+1,0:ny+1)
      pointer(pisteoffxy,isteoffxy)

      integer istioffxy ( 0:nx+1,0:ny+1)
      pointer(pistioffxy,istioffxy)

      integer isngoffxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pisngoffxy,isngoffxy)

      integer istgoffxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pistgoffxy,istgoffxy)

      integer isphioffxy ( 0:nx+1,0:ny+1)
      pointer(pisphioffxy,isphioffxy)

      double precision fdtnixy ( 0:nx+1,0:ny+1,nisp)
      pointer(pfdtnixy,fdtnixy)

      double precision fdtupxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pfdtupxy,fdtupxy)

      double precision fdttexy ( 0:nx+1,0:ny+1)
      pointer(pfdttexy,fdttexy)

      double precision fdttixy ( 0:nx+1,0:ny+1)
      pointer(pfdttixy,fdttixy)

      double precision fdtngxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pfdtngxy,fdtngxy)

      double precision fdttgxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pfdttgxy,fdttgxy)

      double precision fdtphixy ( 0:nx+1,0:ny+1)
      pointer(pfdtphixy,fdtphixy)
      common /bbb10000/ label
      common /bbb10001/ svrpkg
      common /bbb10002/ petscoptfile
      common /bbb10003/ petscopts
      common /bbb20/ methe, methu, methn, methi, methg, methp, isgxvon
      common /bbb20/ ishavisy, isintlog, concap, convis, icnuiz, icnucx
      common /bbb20/ isrecmon, igas, ingb, inflbg, inzb, iteb, is1D_gbx
      common /bbb20/ ixgb, ncrhs, istep, iter, ishymol, isfqpave, isgpye
      common /bbb20/ iigsp, itrap_negni, itrap_negt, itrap_negng
      common /bbb20/ isybdryog, isybdrywd, isxmpog, iexclnxc1, ineudif
      common /bbb20/ isbcwdt, ishosor, issyvxpt0, isrrvave, isdtsfscal
      common /bbb20/ isplflxl, isplflxlv, isplflxlgx, isplflxlgxy
      common /bbb20/ iswflxlgy, isplflxlvgx, isplflxlvgxy, iswflxlvgy
      common /bbb20/ isplflxltgx, isplflxltgxy, iswflxltgy, isfeexpl0
      common /bbb20/ isfeixpl0, isofric, iskaboom, isnglf, isngrf
      common /bbb20/ isnion, isupon, isup1up2, isupgon, isteon, istion
      common /bbb20/ isngon, istgon, isphion, isphiofft, isnewpot
      common /bbb20/ isugfm1side, isnupdot1sd, isphicore0
      common /bbb20/ is_z0_imp_const
      common /bbb23/ csfaclb, csfacrb, csfacti, cslim, dcslim, lnlam
      common /bbb23/ cfaccony, isvylog, cniatol, cngatol, cupatol
      common /bbb23/ cteatol, ctiatol, cphiatol, tolbf, tadj, cnuiz
      common /bbb23/ cnucx, cfrecom, ngbackg, cflbg, facngbackg2ngs
      common /bbb23/ nzbackg, facnzbackg2nis, upclng, facupclng2ups
      common /bbb23/ tebg, tibg, temin, temin2, pwrbkg_c, pwribkg_c
      common /bbb23/ cfwjdotelim, nlimix, nlimiy, nlimgx, nlimgy, xgbx
      common /bbb23/ agdc, pcolwid, eion, ediss, ebind, tfcx, tfcy, afix
      common /bbb23/ coef, ce, ci, dp1, qfl, csh, qsh, mfl, msh, ro, cs
      common /bbb23/ fxe, ctaue, fxi, ctaui, zcoef, coef1, cnurn, cnuru
      common /bbb23/ cnure, cnuri, cnurg, cnurp, nurlxn, nurlxu, nurlxe
      common /bbb23/ nurlxi, nurlxg, nurlxp, rnewpot, r0slab, te_s_dis
      common /bbb23/ fnnuiz, thetar, iseesorave, ispsorave, fsprd
      common /bbb23/ rr_fac, rrmin, frfqpn, cffqpsat, flalfipl, flalfepl
      common /bbb23/ del_te_ro, nglfix, ngrfix, rup21, z0_imp_const
      common /bbb26/ pisnionxy, pisuponxy, pisteonxy
      common /bbb26/ pistionxy, pisngonxy, pistgonxy
      common /bbb26/ pisphionxy, pisnioffxy
      common /bbb26/ pisupoffxy, pisteoffxy
      common /bbb26/ pistioffxy, pisngoffxy
      common /bbb26/ pistgoffxy, pisphioffxy, pfdtnixy
      common /bbb26/ pfdtupxy, pfdttexy, pfdttixy
      common /bbb26/ pfdtngxy, pfdttgxy, pfdtphixy
c End of UEpar
c cniatol,cngatol,cupatol,cteatol,ctiatol,cphiatol,
c tolbf,isnionxy,isuponxy,isteonxy,istionxy,isngonxy,
c isphionxy
c Group Aux
      integer ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3, ix4, ix5
      double precision tv, t0, t1, t2, a
      integer ix6, ixmp
      common /bbb100/ ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3
      common /bbb100/ ix4, ix5, ix6, ixmp
      common /bbb103/ tv, t0, t1, t2, a
c End of Aux
c ix,iy,igsp,iv,ix1,ix2
c Group Lsode
      integer neq, jacflg, jpre, itol, itask, istate, iopts, mf, idid
      double precision runtim, trange, rtolv(30), ts, tout, dtmax
      double precision dtinit, rpar(1), eplidpk, epnldpk, srtolpk, efacn
      integer ires, maxpoly, ipar(3), iextra(5), info(20), iterm, mdif
      double precision ftol, stptol, epscon1, epscon2, stepmx, del2nksol
      integer ipflag, mfnksol, iprint, itermx, incpset, ismmaxuc, mmaxu
      double precision taunksol
      integer icntnunk

      double precision rtol ( neqmx)
      pointer(prtol,rtol)

      double precision atol ( neqmx)
      pointer(patol,atol)

      double precision yl ( neqmx)
      pointer(pyl,yl)

      double precision yldot ( neqmx)
      pointer(pyldot,yldot)

      double precision delta ( neqmx)
      pointer(pdelta,delta)
      common /bbb130/ neq, jacflg, jpre, itol, itask, istate, iopts, mf
      common /bbb130/ idid, ires, maxpoly, ipar, iextra, info, iterm
      common /bbb130/ mdif, ipflag, mfnksol, iprint, itermx, incpset
      common /bbb130/ ismmaxuc, mmaxu, icntnunk
      common /bbb133/ runtim, trange, rtolv, ts, tout, dtmax, dtinit
      common /bbb133/ rpar, eplidpk, epnldpk, srtolpk, efacn, ftol
      common /bbb133/ stptol, epscon1, epscon2, stepmx, del2nksol
      common /bbb133/ taunksol
      common /bbb136/ prtol, patol, pyl, pyldot
      common /bbb136/ pdelta
c End of Lsode
c rtolv,rtol,atol,yl
c Group Compla
      double precision facmg(1:31), istgcon(6), rtauxfac
      double precision rtauyfac, rt_scal, fracvgpgp

      double precision mi ( 1:nisp)
      pointer(pmi,mi)

      double precision zi ( 1:nisp)
      pointer(pzi,zi)

      double precision mg ( 1:ngsp)
      pointer(pmg,mg)

      integer znucl ( 1:nisp)
      pointer(pznucl,znucl)

      double precision ni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pni,ni)

      double precision lni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(plni,lni)

      double precision nm ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnm,nm)

      double precision nz2 ( 0:nx+1,0:ny+1)
      pointer(pnz2,nz2)

      double precision uu ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puu,uu)

      double precision uup ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puup,uup)

      double precision up ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pup,up)

      double precision upi ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupi,upi)

      double precision upifmb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupifmb,upifmb)

      double precision uz ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puz,uz)

      double precision v2 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2,v2)

      double precision v2xgp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2xgp,v2xgp)

      double precision v2ce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2ce,v2ce)

      double precision v2cb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cb,v2cb)

      double precision ve2cb ( 0:nx+1,0:ny+1)
      pointer(pve2cb,ve2cb)

      double precision v2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cd,v2cd)

      double precision ve2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pve2cd,ve2cd)

      double precision q2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pq2cd,q2cd)

      double precision v2rd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2rd,v2rd)

      double precision v2dd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2dd,v2dd)

      double precision vy ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvy,vy)

      double precision vygp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvygp,vygp)

      double precision vytan ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvytan,vytan)

      double precision vygtan ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvygtan,vygtan)

      double precision vyce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyce,vyce)

      double precision vycb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycb,vycb)

      double precision veycb ( 0:nx+1,0:ny+1)
      pointer(pveycb,veycb)

      double precision vycp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycp,vycp)

      double precision veycp ( 0:nx+1,0:ny+1)
      pointer(pveycp,veycp)

      double precision vyrd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyrd,vyrd)

      double precision vydd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvydd,vydd)

      double precision vyavis ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyavis,vyavis)

      double precision vex ( 0:nx+1,0:ny+1)
      pointer(pvex,vex)

      double precision upe ( 0:nx+1,0:ny+1)
      pointer(pupe,upe)

      double precision vep ( 0:nx+1,0:ny+1)
      pointer(pvep,vep)

      double precision ve2 ( 0:nx+1,0:ny+1)
      pointer(pve2,ve2)

      double precision vey ( 0:nx+1,0:ny+1)
      pointer(pvey,vey)

      double precision vycf ( 0:nx+1,0:ny+1)
      pointer(pvycf,vycf)

      double precision vycr ( 0:nx+1,0:ny+1)
      pointer(pvycr,vycr)

      double precision te ( 0:nx+1,0:ny+1)
      pointer(pte,te)

      double precision ti ( 0:nx+1,0:ny+1)
      pointer(pti,ti)

      double precision ng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(png,ng)

      double precision lng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(plng,lng)

      double precision uug ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(puug,uug)

      double precision vyg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvyg,vyg)

      double precision tg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptg,tg)

      double precision tev ( 0:nx+1,0:ny+1)
      pointer(ptev,tev)

      double precision niv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniv,niv)

      double precision upv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupv,upv)

      double precision ngv ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngv,ngv)

      double precision tiv ( 0:nx+1,0:ny+1)
      pointer(ptiv,tiv)

      double precision niy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0,niy0)

      double precision niy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1,niy1)

      double precision niy0s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0s,niy0s)

      double precision niy1s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1s,niy1s)

      double precision ney0 ( 0:nx+1,0:ny+1)
      pointer(pney0,ney0)

      double precision ney1 ( 0:nx+1,0:ny+1)
      pointer(pney1,ney1)

      double precision nity0 ( 0:nx+1,0:ny+1)
      pointer(pnity0,nity0)

      double precision nity1 ( 0:nx+1,0:ny+1)
      pointer(pnity1,nity1)

      double precision tey0 ( 0:nx+1,0:ny+1)
      pointer(ptey0,tey0)

      double precision tey1 ( 0:nx+1,0:ny+1)
      pointer(ptey1,tey1)

      double precision tiy0 ( 0:nx+1,0:ny+1)
      pointer(ptiy0,tiy0)

      double precision tiy1 ( 0:nx+1,0:ny+1)
      pointer(ptiy1,tiy1)

      double precision tiy0s ( 0:nx+1,0:ny+1)
      pointer(ptiy0s,tiy0s)

      double precision tiy1s ( 0:nx+1,0:ny+1)
      pointer(ptiy1s,tiy1s)

      double precision tgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy0,tgy0)

      double precision tgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy1,tgy1)

      double precision ngy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy0,ngy0)

      double precision ngy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy1,ngy1)

      double precision pgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy0,pgy0)

      double precision pgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy1,pgy1)

      double precision pg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppg,pg)

      double precision phiy0 ( 0:nx+1,0:ny+1)
      pointer(pphiy0,phiy0)

      double precision phiy1 ( 0:nx+1,0:ny+1)
      pointer(pphiy1,phiy1)

      double precision phiy0s ( 0:nx+1,0:ny+1)
      pointer(pphiy0s,phiy0s)

      double precision phiy1s ( 0:nx+1,0:ny+1)
      pointer(pphiy1s,phiy1s)

      double precision pr ( 0:nx+1,0:ny+1)
      pointer(ppr,pr)

      double precision prev ( 0:nx+1,0:ny+1)
      pointer(pprev,prev)

      double precision prtv ( 0:nx+1,0:ny+1)
      pointer(pprtv,prtv)

      double precision pri ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppri,pri)

      double precision priv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriv,priv)

      double precision priy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy0,priy0)

      double precision priy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy1,priy1)

      double precision pre ( 0:nx+1,0:ny+1)
      pointer(ppre,pre)

      double precision ne ( 0:nx+1,0:ny+1)
      pointer(pne,ne)

      double precision nit ( 0:nx+1,0:ny+1)
      pointer(pnit,nit)

      double precision nginit ( 0:nx+1,0:ny+1)
      pointer(pnginit,nginit)

      double precision phi ( 0:nx+1,0:ny+1)
      pointer(pphi,phi)

      double precision phiv ( 0:nx+1,0:ny+1)
      pointer(pphiv,phiv)

      double precision zeff ( 0:nx+1,0:ny+1)
      pointer(pzeff,zeff)

      double precision netap ( 0:nx+1,0:ny+1)
      pointer(pnetap,netap)

      double precision znot ( 0:nx+1,0:ny+1)
      pointer(pznot,znot)

      double precision zimpc ( 0:nx+1,0:ny+1)
      pointer(pzimpc,zimpc)

      double precision nil ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnil,nil)

      double precision upl ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupl,upl)

      double precision tel ( 0:nx+1,0:ny+1)
      pointer(ptel,tel)

      double precision til ( 0:nx+1,0:ny+1)
      pointer(ptil,til)

      double precision ngl ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngl,ngl)

      double precision phil ( 0:nx+1,0:ny+1)
      pointer(pphil,phil)

      double precision upxpt ( 1:nusp,1:nxpt)
      pointer(pupxpt,upxpt)

      double precision nixpt ( 1:nusp,1:nxpt)
      pointer(pnixpt,nixpt)

      double precision visyxpt ( 1:nusp,1:nxpt)
      pointer(pvisyxpt,visyxpt)

      double precision vyhxpt ( 1:nusp,1:nxpt)
      pointer(pvyhxpt,vyhxpt)

      double precision vyvxpt ( 1:nusp,1:nxpt)
      pointer(pvyvxpt,vyvxpt)

      double precision fmihxpt ( 1:nusp,1:nxpt)
      pointer(pfmihxpt,fmihxpt)

      double precision fmivxpt ( 1:nusp,1:nxpt)
      pointer(pfmivxpt,fmivxpt)

      double precision rtaux ( 0:nx+1,0:ny+1)
      pointer(prtaux,rtaux)

      double precision rtauy ( 0:nx+1,0:ny+1)
      pointer(prtauy,rtauy)

      double precision rtau ( 0:nx+1,0:ny+1)
      pointer(prtau,rtau)

      double precision betap ( 0:nx+1,0:ny+1)
      pointer(pbetap,betap)
      common /bbb243/ facmg, istgcon, rtauxfac, rtauyfac, rt_scal
      common /bbb243/ fracvgpgp
      common /bbb246/ pmi, pzi, pmg, pznucl
      common /bbb246/ pni, plni, pnm, pnz2
      common /bbb246/ puu, puup, pup, pupi
      common /bbb246/ pupifmb, puz, pv2, pv2xgp
      common /bbb246/ pv2ce, pv2cb, pve2cb
      common /bbb246/ pv2cd, pve2cd, pq2cd
      common /bbb246/ pv2rd, pv2dd, pvy, pvygp
      common /bbb246/ pvytan, pvygtan, pvyce
      common /bbb246/ pvycb, pveycb, pvycp
      common /bbb246/ pveycp, pvyrd, pvydd
      common /bbb246/ pvyavis, pvex, pupe, pvep
      common /bbb246/ pve2, pvey, pvycf, pvycr
      common /bbb246/ pte, pti, png, plng
      common /bbb246/ puug, pvyg, ptg, ptev
      common /bbb246/ pniv, pupv, pngv, ptiv
      common /bbb246/ pniy0, pniy1, pniy0s
      common /bbb246/ pniy1s, pney0, pney1
      common /bbb246/ pnity0, pnity1, ptey0
      common /bbb246/ ptey1, ptiy0, ptiy1
      common /bbb246/ ptiy0s, ptiy1s, ptgy0
      common /bbb246/ ptgy1, pngy0, pngy1, ppgy0
      common /bbb246/ ppgy1, ppg, pphiy0, pphiy1
      common /bbb246/ pphiy0s, pphiy1s, ppr
      common /bbb246/ pprev, pprtv, ppri, ppriv
      common /bbb246/ ppriy0, ppriy1, ppre, pne
      common /bbb246/ pnit, pnginit, pphi, pphiv
      common /bbb246/ pzeff, pnetap, pznot
      common /bbb246/ pzimpc, pnil, pupl, ptel
      common /bbb246/ ptil, pngl, pphil, pupxpt
      common /bbb246/ pnixpt, pvisyxpt, pvyhxpt
      common /bbb246/ pvyvxpt, pfmihxpt, pfmivxpt
      common /bbb246/ prtaux, prtauy, prtau
      common /bbb246/ pbetap
c End of Compla

c Group Indexes

      integer idxn ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pidxn,idxn)

      integer idxg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pidxg,idxg)

      integer idxtg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pidxtg,idxtg)

      integer idxu ( 0:nx+1,0:ny+1,1:nusp)
      pointer(pidxu,idxu)

      integer idxti ( 0:nx+1,0:ny+1)
      pointer(pidxti,idxti)

      integer idxte ( 0:nx+1,0:ny+1)
      pointer(pidxte,idxte)

      integer idxphi ( 0:nx+1,0:ny+1)
      pointer(pidxphi,idxphi)

      integer ivfirst ( 0:nx+1,0:ny+1)
      pointer(pivfirst,ivfirst)

      integer igyl ( neqmx,2)
      pointer(pigyl,igyl)

      integer iseqalg ( neqmx)
      pointer(piseqalg,iseqalg)

      integer isvarup ( numvar)
      pointer(pisvarup,isvarup)

      integer isvarphi ( numvar)
      pointer(pisvarphi,isvarphi)
      common /bbb306/ pidxn, pidxg, pidxtg
      common /bbb306/ pidxu, pidxti, pidxte
      common /bbb306/ pidxphi, pivfirst, pigyl
      common /bbb306/ piseqalg, pisvarup, pisvarphi
c End of Indexes
c igyl
c Group Selec
      integer i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2, j3, j4
      integer j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p, ixs1, ixf6, iys1
      integer iyf6, xlinc, xrinc, yinc, isjaccorall

      integer ixm1 ( 0:nx+1,0:ny+1)
      pointer(pixm1,ixm1)

      integer ixp1 ( 0:nx+1,0:ny+1)
      pointer(pixp1,ixp1)

      integer iym1a ( 0:nx+1,0:ny+1)
      pointer(piym1a,iym1a)

      integer iyp1a ( 0:nx+1,0:ny+1)
      pointer(piyp1a,iyp1a)

      double precision stretcx ( 0:nx+1,0:ny+1)
      pointer(pstretcx,stretcx)
      common /bbb90/ i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2
      common /bbb90/ j3, j4, j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p
      common /bbb90/ ixs1, ixf6, iys1, iyf6, xlinc, xrinc, yinc
      common /bbb90/ isjaccorall
      common /bbb96/ pixm1, pixp1, piym1a
      common /bbb96/ piyp1a, pstretcx
c End of Selec
c ixm1,ixp1
c Group Ynorm
      double precision var_scale_floor, vsf_up, vsf_phi, n0(31)
      double precision n0g(6), temp0, dx0, nnorm, ennorm, sigbar0
      double precision vpnorm, rdoff
      integer iscolnorm, isflxvar, isrscalf, isyloext

      double precision norm_cons ( numvar)
      pointer(pnorm_cons,norm_cons)

      double precision floor_cons ( numvar)
      pointer(pfloor_cons,floor_cons)

      double precision fnorm ( 1:nusp)
      pointer(pfnorm,fnorm)

      double precision suscal ( neqmx)
      pointer(psuscal,suscal)

      double precision sfscal ( neqmx)
      pointer(psfscal,sfscal)

      double precision yloext ( neqmx)
      pointer(pyloext,yloext)
      common /bbb160/ iscolnorm, isflxvar, isrscalf, isyloext
      common /bbb163/ var_scale_floor, vsf_up, vsf_phi, n0, n0g, temp0
      common /bbb163/ dx0, nnorm, ennorm, sigbar0, vpnorm, rdoff
      common /bbb166/ pnorm_cons, pfloor_cons, pfnorm
      common /bbb166/ psuscal, psfscal, pyloext
c End of Ynorm
c isflxvar,nnorm,ennorm,fnorm,temp0,n0,n0g
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
c igrid
c Group Coefeq
      double precision cnfx, cnfy, cnsor, cfneut, cfnidh, cfupcx, cfticx
      double precision cfupimpg, cftiimpg, cmneut, cnflux(6)
      double precision chradi, chradr, chioniz, cne_sgvi, ctsor, ceisor
      double precision ccoldsor, cngfx(6), cngfy(6)
      double precision cngmom(31), cmwall(31), cngtgx(6)
      double precision cngtgy(6), sxgsol, sxgpr, xstscal
      double precision rld2dxg(6), rld2dyg(6), cngflox(6)
      double precision cngfloy(6), cngniflox(31,6)
      double precision cngnifloy(31,6), cngsor, cdifg(6)
      double precision lgmax(6), lgtmax(6), lgvmax
      double precision rtg2ti(6), tgas(6), cmfx, cmfy, cpgx
      double precision cfvisx, cfvisy, cfanomvisxg, cfanomvisyg, cfvisxn
      double precision cfvisxy(1:31), cfvxnrr, cfvisyn
      double precision cfvcsx(1:31), cfvcsy(1:31), vboost, cvgp
      double precision cfvgpx(1:31), cfvgpy(1:31), cfbgt, cfjhf
      double precision cf2ef, cfyef, cftef, cf2bf, cfybf, cfcbti, cfcurv
      double precision cfgradb, cfq2bf, cfqybf, cfqyn, cfqym, cfqydt
      double precision cf2dd, cfydd, cftdd, cfrd, cfvisxneov, cfvisxneoq
      double precision cfvycr, cfvycf, cfvyavis, cfjve, cfjp2, cfjpy
      double precision cfnfmiy, cnimp, fac2sp, cftnm, cfupjr, cfcximp1
      double precision cfcximp2, cfnetap, fcdif, cfmsor, cpiup(31)
      double precision cfloyi, cfloye, cfcvte, cfcvti, cfcvtg, cfloxiplt
      double precision cfloygwall, cftgdiss(6), exjbdry, cfgpijr
      double precision zeffcon, alftng, cfqya, cfqyao, cfqyae, cfqyai
      double precision cfhcxgc(6), cfhcygc(6), cftgcond
      double precision cftgeqp
      integer ifxnsgi, isvisxn_old, jhswitch, isnfmiy, iszeffcon
      common /bbb40/ ifxnsgi, isvisxn_old, jhswitch, isnfmiy, iszeffcon
      common /bbb43/ cnfx, cnfy, cnsor, cfneut, cfnidh, cfupcx, cfticx
      common /bbb43/ cfupimpg, cftiimpg, cmneut, cnflux, chradi, chradr
      common /bbb43/ chioniz, cne_sgvi, ctsor, ceisor, ccoldsor, cngfx
      common /bbb43/ cngfy, cngmom, cmwall, cngtgx, cngtgy, sxgsol
      common /bbb43/ sxgpr, xstscal, rld2dxg, rld2dyg, cngflox, cngfloy
      common /bbb43/ cngniflox, cngnifloy, cngsor, cdifg, lgmax, lgtmax
      common /bbb43/ lgvmax, rtg2ti, tgas, cmfx, cmfy, cpgx, cfvisx
      common /bbb43/ cfvisy, cfanomvisxg, cfanomvisyg, cfvisxn, cfvisxy
      common /bbb43/ cfvxnrr, cfvisyn, cfvcsx, cfvcsy, vboost, cvgp
      common /bbb43/ cfvgpx, cfvgpy, cfbgt, cfjhf, cf2ef, cfyef, cftef
      common /bbb43/ cf2bf, cfybf, cfcbti, cfcurv, cfgradb, cfq2bf
      common /bbb43/ cfqybf, cfqyn, cfqym, cfqydt, cf2dd, cfydd, cftdd
      common /bbb43/ cfrd, cfvisxneov, cfvisxneoq, cfvycr, cfvycf
      common /bbb43/ cfvyavis, cfjve, cfjp2, cfjpy, cfnfmiy, cnimp
      common /bbb43/ fac2sp, cftnm, cfupjr, cfcximp1, cfcximp2, cfnetap
      common /bbb43/ fcdif, cfmsor, cpiup, cfloyi, cfloye, cfcvte
      common /bbb43/ cfcvti, cfcvtg, cfloxiplt, cfloygwall, cftgdiss
      common /bbb43/ exjbdry, cfgpijr, zeffcon, alftng, cfqya, cfqyao
      common /bbb43/ cfqyae, cfqyai, cfhcxgc, cfhcygc, cftgcond, cftgeqp
c End of Coefeq
c cngtgx,cngtgy
c Group Constraints
      double precision rlx, rlxv, adjf1
      integer icflag

      integer icnstr ( neqmx)
      pointer(picnstr,icnstr)

      double precision constr ( neqmx)
      pointer(pconstr,constr)

      double precision ylprevc ( neqmx)
      pointer(pylprevc,ylprevc)

      double precision ylchng ( neqmx)
      pointer(pylchng,ylchng)
      common /bbb150/ icflag
      common /bbb153/ rlx, rlxv, adjf1
      common /bbb156/ picnstr, pconstr, pylprevc
      common /bbb156/ pylchng
c End of Constraints
c icnstr
c Group Indices_domain_dcl
      integer nx_loc, ny_loc, nvrsendl, nvisendl, ixmnbcl, ixmxbcl
      integer iymnbcl, iymxbcl, idxp1, idxm1, idyp1, idym1, idcorn(1:4)
      integer iv_totbdy(1:8), typebdyi(1:4), typecni(1:4), typebdy(1:4)
      integer typecn(1:4), neq_locl, numvarl, ispwrbcl, ixpt1l, ixpt2l
      integer iysptrx1l, ixlbl, ixrbl

      double precision vrsendl ( nvrsendl)
      pointer(pvrsendl,vrsendl)

      integer visendl ( nvisendl)
      pointer(pvisendl,visendl)

      integer ivloc2sdgl ( nvisendl)
      pointer(pivloc2sdgl,ivloc2sdgl)

      integer ivloc2mdgl ( nvisendl)
      pointer(pivloc2mdgl,ivloc2mdgl)

      integer ivl2gstnll ( neq_locl,9*numvarl)
      pointer(pivl2gstnll,ivl2gstnll)
      common /bbb660/ nx_loc, ny_loc, nvrsendl, nvisendl, ixmnbcl
      common /bbb660/ ixmxbcl, iymnbcl, iymxbcl, idxp1, idxm1, idyp1
      common /bbb660/ idym1, idcorn, iv_totbdy, typebdyi, typecni
      common /bbb660/ typebdy, typecn, neq_locl, numvarl, ispwrbcl
      common /bbb660/ ixpt1l, ixpt2l, iysptrx1l, ixlbl, ixrbl
      common /bbb666/ pvrsendl, pvisendl, pivloc2sdgl
      common /bbb666/ pivloc2mdgl, pivl2gstnll
c End of Indices_domain_dcl
cixmxbcl,ixmnbcl,iymxbcl,iymnbcl
c Group Phyvar
      double precision pi, me, mp, ev, qe, mu0, eps0, rt8opi
      common /bbb173/ pi, me, mp, ev, qe, mu0, eps0, rt8opi
c End of Phyvar
c ev

c...  local variables
      doubleprecision bfac, ntemp
      integer ifld,isfirstvar

cflag signals first var at ix,iy found
      isfirstvar = 0
      iv = 0
      do 8 iy = 1-iymnbcl, ny+iymxbcl
         do 6 ix = 1-ixmnbcl, nx+ixmxbcl
            bfac = 1.d0
            if (ix.eq.0 .or. iy.eq.0 .or. iy.eq.ny+1) bfac = tolbf
            ix1 = ixp1(ix,iy)
cflag signals first var at ix,iy found
            isfirstvar = 0
            do 23002 ifld = 1, nisp
               if (isnionxy(ix,iy,ifld) .eq. 1) then
                  iv = iv + 1
                  yl(iv) = ni(ix,iy,ifld)/n0(ifld)
                  if (zi(ifld).eq.0.d0 .and. ineudif.eq.3) then
                     yl(iv) = log(ni(ix,iy,ifld))
                  endif
                  rtol(iv) = rtolv(igrid)*bfac
                  atol(iv) = cniatol*rtol(iv)*bfac*abs(yl(iv))
                  idxn(ix,iy,ifld) = iv
                  if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
                  isfirstvar = 1
                  igyl(iv,1) = ix
                  igyl(iv,2) = iy
                  icnstr(iv) = 1
               endif
23002       continue
            do 23004 ifld = 1, nusp
               if (isuponxy(ix,iy,ifld) .eq. 1) then
                  iv = iv + 1
                  ntemp =0.5d0*( nm(ix,iy,ifld) + nm(ix1,iy,ifld) )
                  if (isflxvar.eq.0 .or. isflxvar.eq.2) ntemp = mi(ifld)
     &                  * n0(ifld)
                  yl(iv) = up(ix,iy,ifld)*ntemp/fnorm(ifld)
                  rtol(iv) = rtolv(igrid)*bfac
                  atol(iv) = cupatol*rtol(iv)*bfac*sqrt(te(ix,iy)/ mi(
     &               ifld))*ntemp/fnorm(ifld)
                  idxu(ix,iy,ifld) = iv
                  if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
                  isfirstvar = 1
                  igyl(iv,1) = ix
                  igyl(iv,2) = iy
                  icnstr(iv) = 0
               endif
23004       continue
            if (isteonxy(ix,iy) .eq. 1) then
               iv = iv + 1
               ntemp = ne(ix,iy)
               if (isflxvar .eq. 0) ntemp = nnorm
               yl(iv) = 1.5d0*ntemp*te(ix,iy)/ennorm
               rtol(iv) = rtolv(igrid)*bfac
               atol(iv) = cteatol*rtol(iv)*bfac*abs(yl(iv))
               idxte(ix,iy) = iv
               if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
               isfirstvar = 1
               igyl(iv,1) = ix
               igyl(iv,2) = iy
               icnstr(iv) = 1
            endif
            if (istionxy(ix,iy) .eq. 1) then
               iv = iv + 1
               ntemp = nit(ix,iy) + cngtgx(1)*ng(ix,iy,1)
               if (isflxvar .eq. 0) ntemp = nnorm
               yl(iv) = 1.5d0*ntemp*ti(ix,iy)/ennorm
               rtol(iv) = rtolv(igrid)*bfac
               atol(iv) = ctiatol*rtol(iv)*bfac*abs(yl(iv))
               idxti(ix,iy) = iv
               if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
               isfirstvar = 1
               igyl(iv,1) = ix
               igyl(iv,2) = iy
               icnstr(iv) = 1
c...  Omit constraint check on x-boundaries for Ti - ckinfl problem
               if (ix.eq.0 .or. ix.eq.nx+1) icnstr(iv) = 0
            endif
            do 23006 igsp = 1, ngsp
               if (isngonxy(ix,iy,igsp) .eq. 1) then
                  iv = iv + 1
                  if (ineudif .ne. 3) then
                     yl(iv) = ng(ix,iy,igsp)/n0g(igsp)
                  elseif (ineudif .eq. 3) then
                     yl(iv) = lng(ix,iy,igsp)
                  endif
                  rtol(iv) = rtolv(igrid)*bfac
                  atol(iv) = cngatol*rtol(iv)*bfac*abs(yl(iv))
                  idxg(ix,iy,igsp) = iv
                  if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
                  isfirstvar = 1
                  igyl(iv,1) = ix
                  igyl(iv,2) = iy
                  icnstr(iv) = 1
               endif
23006       continue
            do 23008 igsp = 1, ngsp
               if (istgonxy(ix,iy,igsp) .eq. 1) then
                  iv = iv + 1
                  ntemp = ng(ix,iy,igsp)
                  if (isflxvar .eq. 0) ntemp=n0g(igsp)
                  yl(iv) = 1.5d0*ntemp*tg(ix,iy,igsp)/ennorm
                  rtol(iv) = rtolv(igrid)*bfac
                  atol(iv) = cngatol*rtol(iv)*bfac*abs(yl(iv))
                  idxtg(ix,iy,igsp) = iv
                  if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
                  isfirstvar = 1
                  igyl(iv,1) = ix
                  igyl(iv,2) = iy
                  icnstr(iv) = 1
               endif
23008       continue
            if (isphionxy(ix,iy) .eq. 1) then
               iv = iv + 1
               yl(iv) = phi(ix,iy)/temp0
               rtol(iv) = rtolv(igrid)*bfac
               atol(iv) = cphiatol*rtol(iv)*bfac*abs(yl(iv))
               idxphi(ix,iy) = iv
               if (isfirstvar.eq.0) ivfirst(ix,iy) = iv
               isfirstvar = 1
               igyl(iv,1) = ix
               igyl(iv,2) = iy
               icnstr(iv) = 0
            endif
    6       continue
    8    continue

      return
      end
c ***** end of subroutine convert ***********
c-----------------------------------------------------------------------
      subroutine convsr_vo (ixl, iyl, yl)
cProlog

c ... Converts the yl variables into plasma variables over a restricted
c ... range of indices
c ... This routine only unloads the yl variables into ni, up, etc.,
c ... The other variables are added in the routine convr_auxo


      implicit none

c  -- input arguments
      integer ixl, iyl, inc
      doubleprecision yl(*)

c  -- local variables
      doubleprecision ntemp
      integer is, ie, js, je
      integer ifld, id
      integer inegt, inegng, inegni, ixneg, iyneg, ifldneg, igspneg

c_mpi      Use(MpiVars)  #module defined in com/mpivarsmod.F.in
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nhsp,nzsp,nisp,nusp,ngsp
c Group Xpoint_indices
      integer iysptrx

      integer ixlb ( 1:nxpt)
      pointer(pixlb,ixlb)

      integer ixpt1 ( 1:nxpt)
      pointer(pixpt1,ixpt1)

      integer ixmdp ( 1:nxpt)
      pointer(pixmdp,ixmdp)

      integer ixpt2 ( 1:nxpt)
      pointer(pixpt2,ixpt2)

      integer ixrb ( 1:nxpt)
      pointer(pixrb,ixrb)

      integer iysptrx1 ( 1:nxpt)
      pointer(piysptrx1,iysptrx1)

      integer iysptrx2 ( 1:nxpt)
      pointer(piysptrx2,iysptrx2)
      common /com90/ iysptrx
      common /com96/ pixlb, pixpt1, pixmdp
      common /com96/ pixpt2, pixrb, piysptrx1
      common /com96/ piysptrx2
c End of Xpoint_indices
c ixpt1,ixpt2
c Group Math_problem_size
      integer neqmx, numvar, numvarbwpad
      common /bbb10/ neqmx, numvar, numvarbwpad
c End of Math_problem_size
c neqmx
c Group Compla
      double precision facmg(1:31), istgcon(6), rtauxfac
      double precision rtauyfac, rt_scal, fracvgpgp

      double precision mi ( 1:nisp)
      pointer(pmi,mi)

      double precision zi ( 1:nisp)
      pointer(pzi,zi)

      double precision mg ( 1:ngsp)
      pointer(pmg,mg)

      integer znucl ( 1:nisp)
      pointer(pznucl,znucl)

      double precision ni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pni,ni)

      double precision lni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(plni,lni)

      double precision nm ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnm,nm)

      double precision nz2 ( 0:nx+1,0:ny+1)
      pointer(pnz2,nz2)

      double precision uu ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puu,uu)

      double precision uup ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puup,uup)

      double precision up ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pup,up)

      double precision upi ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupi,upi)

      double precision upifmb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupifmb,upifmb)

      double precision uz ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puz,uz)

      double precision v2 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2,v2)

      double precision v2xgp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2xgp,v2xgp)

      double precision v2ce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2ce,v2ce)

      double precision v2cb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cb,v2cb)

      double precision ve2cb ( 0:nx+1,0:ny+1)
      pointer(pve2cb,ve2cb)

      double precision v2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cd,v2cd)

      double precision ve2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pve2cd,ve2cd)

      double precision q2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pq2cd,q2cd)

      double precision v2rd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2rd,v2rd)

      double precision v2dd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2dd,v2dd)

      double precision vy ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvy,vy)

      double precision vygp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvygp,vygp)

      double precision vytan ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvytan,vytan)

      double precision vygtan ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvygtan,vygtan)

      double precision vyce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyce,vyce)

      double precision vycb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycb,vycb)

      double precision veycb ( 0:nx+1,0:ny+1)
      pointer(pveycb,veycb)

      double precision vycp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycp,vycp)

      double precision veycp ( 0:nx+1,0:ny+1)
      pointer(pveycp,veycp)

      double precision vyrd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyrd,vyrd)

      double precision vydd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvydd,vydd)

      double precision vyavis ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyavis,vyavis)

      double precision vex ( 0:nx+1,0:ny+1)
      pointer(pvex,vex)

      double precision upe ( 0:nx+1,0:ny+1)
      pointer(pupe,upe)

      double precision vep ( 0:nx+1,0:ny+1)
      pointer(pvep,vep)

      double precision ve2 ( 0:nx+1,0:ny+1)
      pointer(pve2,ve2)

      double precision vey ( 0:nx+1,0:ny+1)
      pointer(pvey,vey)

      double precision vycf ( 0:nx+1,0:ny+1)
      pointer(pvycf,vycf)

      double precision vycr ( 0:nx+1,0:ny+1)
      pointer(pvycr,vycr)

      double precision te ( 0:nx+1,0:ny+1)
      pointer(pte,te)

      double precision ti ( 0:nx+1,0:ny+1)
      pointer(pti,ti)

      double precision ng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(png,ng)

      double precision lng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(plng,lng)

      double precision uug ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(puug,uug)

      double precision vyg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvyg,vyg)

      double precision tg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptg,tg)

      double precision tev ( 0:nx+1,0:ny+1)
      pointer(ptev,tev)

      double precision niv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniv,niv)

      double precision upv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupv,upv)

      double precision ngv ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngv,ngv)

      double precision tiv ( 0:nx+1,0:ny+1)
      pointer(ptiv,tiv)

      double precision niy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0,niy0)

      double precision niy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1,niy1)

      double precision niy0s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0s,niy0s)

      double precision niy1s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1s,niy1s)

      double precision ney0 ( 0:nx+1,0:ny+1)
      pointer(pney0,ney0)

      double precision ney1 ( 0:nx+1,0:ny+1)
      pointer(pney1,ney1)

      double precision nity0 ( 0:nx+1,0:ny+1)
      pointer(pnity0,nity0)

      double precision nity1 ( 0:nx+1,0:ny+1)
      pointer(pnity1,nity1)

      double precision tey0 ( 0:nx+1,0:ny+1)
      pointer(ptey0,tey0)

      double precision tey1 ( 0:nx+1,0:ny+1)
      pointer(ptey1,tey1)

      double precision tiy0 ( 0:nx+1,0:ny+1)
      pointer(ptiy0,tiy0)

      double precision tiy1 ( 0:nx+1,0:ny+1)
      pointer(ptiy1,tiy1)

      double precision tiy0s ( 0:nx+1,0:ny+1)
      pointer(ptiy0s,tiy0s)

      double precision tiy1s ( 0:nx+1,0:ny+1)
      pointer(ptiy1s,tiy1s)

      double precision tgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy0,tgy0)

      double precision tgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy1,tgy1)

      double precision ngy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy0,ngy0)

      double precision ngy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy1,ngy1)

      double precision pgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy0,pgy0)

      double precision pgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy1,pgy1)

      double precision pg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppg,pg)

      double precision phiy0 ( 0:nx+1,0:ny+1)
      pointer(pphiy0,phiy0)

      double precision phiy1 ( 0:nx+1,0:ny+1)
      pointer(pphiy1,phiy1)

      double precision phiy0s ( 0:nx+1,0:ny+1)
      pointer(pphiy0s,phiy0s)

      double precision phiy1s ( 0:nx+1,0:ny+1)
      pointer(pphiy1s,phiy1s)

      double precision pr ( 0:nx+1,0:ny+1)
      pointer(ppr,pr)

      double precision prev ( 0:nx+1,0:ny+1)
      pointer(pprev,prev)

      double precision prtv ( 0:nx+1,0:ny+1)
      pointer(pprtv,prtv)

      double precision pri ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppri,pri)

      double precision priv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriv,priv)

      double precision priy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy0,priy0)

      double precision priy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy1,priy1)

      double precision pre ( 0:nx+1,0:ny+1)
      pointer(ppre,pre)

      double precision ne ( 0:nx+1,0:ny+1)
      pointer(pne,ne)

      double precision nit ( 0:nx+1,0:ny+1)
      pointer(pnit,nit)

      double precision nginit ( 0:nx+1,0:ny+1)
      pointer(pnginit,nginit)

      double precision phi ( 0:nx+1,0:ny+1)
      pointer(pphi,phi)

      double precision phiv ( 0:nx+1,0:ny+1)
      pointer(pphiv,phiv)

      double precision zeff ( 0:nx+1,0:ny+1)
      pointer(pzeff,zeff)

      double precision netap ( 0:nx+1,0:ny+1)
      pointer(pnetap,netap)

      double precision znot ( 0:nx+1,0:ny+1)
      pointer(pznot,znot)

      double precision zimpc ( 0:nx+1,0:ny+1)
      pointer(pzimpc,zimpc)

      double precision nil ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnil,nil)

      double precision upl ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupl,upl)

      double precision tel ( 0:nx+1,0:ny+1)
      pointer(ptel,tel)

      double precision til ( 0:nx+1,0:ny+1)
      pointer(ptil,til)

      double precision ngl ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngl,ngl)

      double precision phil ( 0:nx+1,0:ny+1)
      pointer(pphil,phil)

      double precision upxpt ( 1:nusp,1:nxpt)
      pointer(pupxpt,upxpt)

      double precision nixpt ( 1:nusp,1:nxpt)
      pointer(pnixpt,nixpt)

      double precision visyxpt ( 1:nusp,1:nxpt)
      pointer(pvisyxpt,visyxpt)

      double precision vyhxpt ( 1:nusp,1:nxpt)
      pointer(pvyhxpt,vyhxpt)

      double precision vyvxpt ( 1:nusp,1:nxpt)
      pointer(pvyvxpt,vyvxpt)

      double precision fmihxpt ( 1:nusp,1:nxpt)
      pointer(pfmihxpt,fmihxpt)

      double precision fmivxpt ( 1:nusp,1:nxpt)
      pointer(pfmivxpt,fmivxpt)

      double precision rtaux ( 0:nx+1,0:ny+1)
      pointer(prtaux,rtaux)

      double precision rtauy ( 0:nx+1,0:ny+1)
      pointer(prtauy,rtauy)

      double precision rtau ( 0:nx+1,0:ny+1)
      pointer(prtau,rtau)

      double precision betap ( 0:nx+1,0:ny+1)
      pointer(pbetap,betap)
      common /bbb243/ facmg, istgcon, rtauxfac, rtauyfac, rt_scal
      common /bbb243/ fracvgpgp
      common /bbb246/ pmi, pzi, pmg, pznucl
      common /bbb246/ pni, plni, pnm, pnz2
      common /bbb246/ puu, puup, pup, pupi
      common /bbb246/ pupifmb, puz, pv2, pv2xgp
      common /bbb246/ pv2ce, pv2cb, pve2cb
      common /bbb246/ pv2cd, pve2cd, pq2cd
      common /bbb246/ pv2rd, pv2dd, pvy, pvygp
      common /bbb246/ pvytan, pvygtan, pvyce
      common /bbb246/ pvycb, pveycb, pvycp
      common /bbb246/ pveycp, pvyrd, pvydd
      common /bbb246/ pvyavis, pvex, pupe, pvep
      common /bbb246/ pve2, pvey, pvycf, pvycr
      common /bbb246/ pte, pti, png, plng
      common /bbb246/ puug, pvyg, ptg, ptev
      common /bbb246/ pniv, pupv, pngv, ptiv
      common /bbb246/ pniy0, pniy1, pniy0s
      common /bbb246/ pniy1s, pney0, pney1
      common /bbb246/ pnity0, pnity1, ptey0
      common /bbb246/ ptey1, ptiy0, ptiy1
      common /bbb246/ ptiy0s, ptiy1s, ptgy0
      common /bbb246/ ptgy1, pngy0, pngy1, ppgy0
      common /bbb246/ ppgy1, ppg, pphiy0, pphiy1
      common /bbb246/ pphiy0s, pphiy1s, ppr
      common /bbb246/ pprev, pprtv, ppri, ppriv
      common /bbb246/ ppriy0, ppriy1, ppre, pne
      common /bbb246/ pnit, pnginit, pphi, pphiv
      common /bbb246/ pzeff, pnetap, pznot
      common /bbb246/ pzimpc, pnil, pupl, ptel
      common /bbb246/ ptil, pngl, pphil, pupxpt
      common /bbb246/ pnixpt, pvisyxpt, pvyhxpt
      common /bbb246/ pvyvxpt, pfmihxpt, pfmivxpt
      common /bbb246/ prtaux, prtauy, prtau
      common /bbb246/ pbetap
c End of Compla
c ,zi,zeff,zimpc
c Group Ynorm
      double precision var_scale_floor, vsf_up, vsf_phi, n0(31)
      double precision n0g(6), temp0, dx0, nnorm, ennorm, sigbar0
      double precision vpnorm, rdoff
      integer iscolnorm, isflxvar, isrscalf, isyloext

      double precision norm_cons ( numvar)
      pointer(pnorm_cons,norm_cons)

      double precision floor_cons ( numvar)
      pointer(pfloor_cons,floor_cons)

      double precision fnorm ( 1:nusp)
      pointer(pfnorm,fnorm)

      double precision suscal ( neqmx)
      pointer(psuscal,suscal)

      double precision sfscal ( neqmx)
      pointer(psfscal,sfscal)

      double precision yloext ( neqmx)
      pointer(pyloext,yloext)
      common /bbb160/ iscolnorm, isflxvar, isrscalf, isyloext
      common /bbb163/ var_scale_floor, vsf_up, vsf_phi, n0, n0g, temp0
      common /bbb163/ dx0, nnorm, ennorm, sigbar0, vpnorm, rdoff
      common /bbb166/ pnorm_cons, pfloor_cons, pfnorm
      common /bbb166/ psuscal, psfscal, pyloext
c End of Ynorm
c isflxvar,temp0,nnorm,ennorm,fnorm,n0,n0g
c Group UEpar
      double precision csfaclb(31,2), csfacrb(31,2)
      integer methe, methu, methn, methi, methg, methp, isgxvon
      double precision csfacti, cslim, dcslim, lnlam, cfaccony, isvylog
      double precision cniatol, cngatol, cupatol, cteatol, ctiatol
      integer ishavisy, isintlog, concap, convis, icnuiz, icnucx
      double precision cphiatol, tolbf, tadj, cnuiz, cnucx, cfrecom
      double precision ngbackg(6), cflbg, facngbackg2ngs(6)
      double precision nzbackg(31), facnzbackg2nis(31)
      double precision upclng(31), facupclng2ups(31), tebg, tibg
      double precision temin, temin2, pwrbkg_c, pwribkg_c, cfwjdotelim
      double precision nlimix(31), nlimiy(31), nlimgx, nlimgy
      double precision xgbx, agdc, pcolwid, eion, ediss, ebind, tfcx
      integer isrecmon, igas, ingb, inflbg, inzb, iteb, is1D_gbx, ixgb
      double precision tfcy, afix, coef, ce, ci, dp1, qfl, csh, qsh, mfl
      double precision msh, ro, cs, fxe, ctaue, fxi, ctaui, zcoef, coef1
      double precision cnurn, cnuru, cnure, cnuri, cnurg, cnurp, nurlxn
      character*72 label
      double precision nurlxu, nurlxe, nurlxi, nurlxg, nurlxp, rnewpot
      character*8 svrpkg
      character*80 petscoptfile
      character*2048 petscopts
      integer ncrhs, istep, iter, ishymol, isfqpave, isgpye, iigsp
      integer itrap_negni, itrap_negt, itrap_negng, isybdryog, isybdrywd
      double precision r0slab, te_s_dis, fnnuiz, thetar, iseesorave
      integer isxmpog, iexclnxc1, ineudif, isbcwdt, ishosor, issyvxpt0
      integer isrrvave, isdtsfscal, isplflxl, isplflxlv, isplflxlgx
      integer isplflxlgxy, iswflxlgy, isplflxlvgx, isplflxlvgxy
      double precision ispsorave, fsprd, rr_fac, rrmin, frfqpn, cffqpsat
      integer iswflxlvgy, isplflxltgx, isplflxltgxy, iswflxltgy
      integer isfeexpl0, isfeixpl0, isofric, iskaboom, isnglf, isngrf
      double precision flalfipl, flalfepl, del_te_ro, nglfix, ngrfix
      integer isnion(31), isupon(31), isup1up2, isupgon(6)
      integer isteon, istion, isngon(6), istgon(6), isphion
      integer isphiofft, isnewpot, isugfm1side, isnupdot1sd, isphicore0
      double precision rup21, z0_imp_const
      integer is_z0_imp_const

      integer isnionxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisnionxy,isnionxy)

      integer isuponxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisuponxy,isuponxy)

      integer isteonxy ( 0:nx+1,0:ny+1)
      pointer(pisteonxy,isteonxy)

      integer istionxy ( 0:nx+1,0:ny+1)
      pointer(pistionxy,istionxy)

      integer isngonxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pisngonxy,isngonxy)

      integer istgonxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pistgonxy,istgonxy)

      integer isphionxy ( 0:nx+1,0:ny+1)
      pointer(pisphionxy,isphionxy)

      integer isnioffxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisnioffxy,isnioffxy)

      integer isupoffxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisupoffxy,isupoffxy)

      integer isteoffxy ( 0:nx+1,0:ny+1)
      pointer(pisteoffxy,isteoffxy)

      integer istioffxy ( 0:nx+1,0:ny+1)
      pointer(pistioffxy,istioffxy)

      integer isngoffxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pisngoffxy,isngoffxy)

      integer istgoffxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pistgoffxy,istgoffxy)

      integer isphioffxy ( 0:nx+1,0:ny+1)
      pointer(pisphioffxy,isphioffxy)

      double precision fdtnixy ( 0:nx+1,0:ny+1,nisp)
      pointer(pfdtnixy,fdtnixy)

      double precision fdtupxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pfdtupxy,fdtupxy)

      double precision fdttexy ( 0:nx+1,0:ny+1)
      pointer(pfdttexy,fdttexy)

      double precision fdttixy ( 0:nx+1,0:ny+1)
      pointer(pfdttixy,fdttixy)

      double precision fdtngxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pfdtngxy,fdtngxy)

      double precision fdttgxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pfdttgxy,fdttgxy)

      double precision fdtphixy ( 0:nx+1,0:ny+1)
      pointer(pfdtphixy,fdtphixy)
      common /bbb10000/ label
      common /bbb10001/ svrpkg
      common /bbb10002/ petscoptfile
      common /bbb10003/ petscopts
      common /bbb20/ methe, methu, methn, methi, methg, methp, isgxvon
      common /bbb20/ ishavisy, isintlog, concap, convis, icnuiz, icnucx
      common /bbb20/ isrecmon, igas, ingb, inflbg, inzb, iteb, is1D_gbx
      common /bbb20/ ixgb, ncrhs, istep, iter, ishymol, isfqpave, isgpye
      common /bbb20/ iigsp, itrap_negni, itrap_negt, itrap_negng
      common /bbb20/ isybdryog, isybdrywd, isxmpog, iexclnxc1, ineudif
      common /bbb20/ isbcwdt, ishosor, issyvxpt0, isrrvave, isdtsfscal
      common /bbb20/ isplflxl, isplflxlv, isplflxlgx, isplflxlgxy
      common /bbb20/ iswflxlgy, isplflxlvgx, isplflxlvgxy, iswflxlvgy
      common /bbb20/ isplflxltgx, isplflxltgxy, iswflxltgy, isfeexpl0
      common /bbb20/ isfeixpl0, isofric, iskaboom, isnglf, isngrf
      common /bbb20/ isnion, isupon, isup1up2, isupgon, isteon, istion
      common /bbb20/ isngon, istgon, isphion, isphiofft, isnewpot
      common /bbb20/ isugfm1side, isnupdot1sd, isphicore0
      common /bbb20/ is_z0_imp_const
      common /bbb23/ csfaclb, csfacrb, csfacti, cslim, dcslim, lnlam
      common /bbb23/ cfaccony, isvylog, cniatol, cngatol, cupatol
      common /bbb23/ cteatol, ctiatol, cphiatol, tolbf, tadj, cnuiz
      common /bbb23/ cnucx, cfrecom, ngbackg, cflbg, facngbackg2ngs
      common /bbb23/ nzbackg, facnzbackg2nis, upclng, facupclng2ups
      common /bbb23/ tebg, tibg, temin, temin2, pwrbkg_c, pwribkg_c
      common /bbb23/ cfwjdotelim, nlimix, nlimiy, nlimgx, nlimgy, xgbx
      common /bbb23/ agdc, pcolwid, eion, ediss, ebind, tfcx, tfcy, afix
      common /bbb23/ coef, ce, ci, dp1, qfl, csh, qsh, mfl, msh, ro, cs
      common /bbb23/ fxe, ctaue, fxi, ctaui, zcoef, coef1, cnurn, cnuru
      common /bbb23/ cnure, cnuri, cnurg, cnurp, nurlxn, nurlxu, nurlxe
      common /bbb23/ nurlxi, nurlxg, nurlxp, rnewpot, r0slab, te_s_dis
      common /bbb23/ fnnuiz, thetar, iseesorave, ispsorave, fsprd
      common /bbb23/ rr_fac, rrmin, frfqpn, cffqpsat, flalfipl, flalfepl
      common /bbb23/ del_te_ro, nglfix, ngrfix, rup21, z0_imp_const
      common /bbb26/ pisnionxy, pisuponxy, pisteonxy
      common /bbb26/ pistionxy, pisngonxy, pistgonxy
      common /bbb26/ pisphionxy, pisnioffxy
      common /bbb26/ pisupoffxy, pisteoffxy
      common /bbb26/ pistioffxy, pisngoffxy
      common /bbb26/ pistgoffxy, pisphioffxy, pfdtnixy
      common /bbb26/ pfdtupxy, pfdttexy, pfdttixy
      common /bbb26/ pfdtngxy, pfdttgxy, pfdtphixy
c End of UEpar
c itrap_negt,itrap_negng,
c isnionxy,isuponxy,isteonxy,istionxy,
c isngonxy,isphionxy
c Group Aux
      integer ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3, ix4, ix5
      double precision tv, t0, t1, t2, a
      integer ix6, ixmp
      common /bbb100/ ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3
      common /bbb100/ ix4, ix5, ix6, ixmp
      common /bbb103/ tv, t0, t1, t2, a
c End of Aux
c ix,iy,igsp,ix1,ix2,t1,t2
c Group Selec
      integer i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2, j3, j4
      integer j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p, ixs1, ixf6, iys1
      integer iyf6, xlinc, xrinc, yinc, isjaccorall

      integer ixm1 ( 0:nx+1,0:ny+1)
      pointer(pixm1,ixm1)

      integer ixp1 ( 0:nx+1,0:ny+1)
      pointer(pixp1,ixp1)

      integer iym1a ( 0:nx+1,0:ny+1)
      pointer(piym1a,iym1a)

      integer iyp1a ( 0:nx+1,0:ny+1)
      pointer(piyp1a,iyp1a)

      double precision stretcx ( 0:nx+1,0:ny+1)
      pointer(pstretcx,stretcx)
      common /bbb90/ i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2
      common /bbb90/ j3, j4, j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p
      common /bbb90/ ixs1, ixf6, iys1, iyf6, xlinc, xrinc, yinc
      common /bbb90/ isjaccorall
      common /bbb96/ pixm1, pixp1, piym1a
      common /bbb96/ piyp1a, pstretcx
c End of Selec
c yinc,ixm1,ixp1
c Group Indexes

      integer idxn ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pidxn,idxn)

      integer idxg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pidxg,idxg)

      integer idxtg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pidxtg,idxtg)

      integer idxu ( 0:nx+1,0:ny+1,1:nusp)
      pointer(pidxu,idxu)

      integer idxti ( 0:nx+1,0:ny+1)
      pointer(pidxti,idxti)

      integer idxte ( 0:nx+1,0:ny+1)
      pointer(pidxte,idxte)

      integer idxphi ( 0:nx+1,0:ny+1)
      pointer(pidxphi,idxphi)

      integer ivfirst ( 0:nx+1,0:ny+1)
      pointer(pivfirst,ivfirst)

      integer igyl ( neqmx,2)
      pointer(pigyl,igyl)

      integer iseqalg ( neqmx)
      pointer(piseqalg,iseqalg)

      integer isvarup ( numvar)
      pointer(pisvarup,isvarup)

      integer isvarphi ( numvar)
      pointer(pisvarphi,isvarphi)
      common /bbb306/ pidxn, pidxg, pidxtg
      common /bbb306/ pidxu, pidxti, pidxte
      common /bbb306/ pidxphi, pivfirst, pigyl
      common /bbb306/ piseqalg, pisvarup, pisvarphi
c End of Indexes

c Group Comgeo
      double precision sygytotc, area_core, ghxpt, gvxpt, sxyxpt
      double precision ghxpt_lower, gvxpt_lower, sxyxpt_lower
      double precision ghxpt_upper, gvxpt_upper, sxyxpt_upper, linelen
      double precision dxmin

      double precision vol ( 0:nx+1,0:ny+1)
      pointer(pvol,vol)

      double precision gx ( 0:nx+1,0:ny+1)
      pointer(pgx,gx)

      double precision gy ( 0:nx+1,0:ny+1)
      pointer(pgy,gy)

      double precision dx ( 0:nx+1,0:ny+1)
      pointer(pdx,dx)

      double precision dxvf ( 0:nx+1,0:ny+1)
      pointer(pdxvf,dxvf)

      double precision dy ( 0:nx+1,0:ny+1)
      pointer(pdy,dy)

      double precision gxf ( 0:nx+1,0:ny+1)
      pointer(pgxf,gxf)

      double precision gxfn ( 0:nx+1,0:ny+1)
      pointer(pgxfn,gxfn)

      double precision gyf ( 0:nx+1,0:ny+1)
      pointer(pgyf,gyf)

      double precision gxc ( 0:nx+1,0:ny+1)
      pointer(pgxc,gxc)

      double precision gyc ( 0:nx+1,0:ny+1)
      pointer(pgyc,gyc)

      double precision xnrm ( 0:nx+1,0:ny+1)
      pointer(pxnrm,xnrm)

      double precision xvnrm ( 0:nx+1,0:ny+1)
      pointer(pxvnrm,xvnrm)

      double precision ynrm ( 0:nx+1,0:ny+1)
      pointer(pynrm,ynrm)

      double precision yvnrm ( 0:nx+1,0:ny+1)
      pointer(pyvnrm,yvnrm)

      double precision sx ( 0:nx+1,0:ny+1)
      pointer(psx,sx)

      double precision sxnp ( 0:nx+1,0:ny+1)
      pointer(psxnp,sxnp)

      double precision sy ( 0:nx+1,0:ny+1)
      pointer(psy,sy)

      double precision rr ( 0:nx+1,0:ny+1)
      pointer(prr,rr)

      double precision xcs ( 0:nx+1)
      pointer(pxcs,xcs)

      double precision xfs ( 0:nx+1)
      pointer(pxfs,xfs)

      double precision xcwi ( 0:nx+1)
      pointer(pxcwi,xcwi)

      double precision xfwi ( 0:nx+1)
      pointer(pxfwi,xfwi)

      double precision xfpf ( 0:nx+1)
      pointer(pxfpf,xfpf)

      double precision xcpf ( 0:nx+1)
      pointer(pxcpf,xcpf)

      double precision xcwo ( 0:nx+1)
      pointer(pxcwo,xcwo)

      double precision xfwo ( 0:nx+1)
      pointer(pxfwo,xfwo)

      double precision yyc ( 0:ny+1)
      pointer(pyyc,yyc)

      double precision yyf ( 0:ny+1)
      pointer(pyyf,yyf)

      double precision yylb ( 0:ny+1,1:nxpt)
      pointer(pyylb,yylb)

      double precision yyrb ( 0:ny+1,1:nxpt)
      pointer(pyyrb,yyrb)

      double precision xcv ( 0:nx+1)
      pointer(pxcv,xcv)

      double precision xfv ( 0:nx+1)
      pointer(pxfv,xfv)

      double precision psinormc ( 0:ny+1)
      pointer(ppsinormc,psinormc)

      double precision psinormf ( 0:ny+1)
      pointer(ppsinormf,psinormf)

      double precision rrv ( 0:nx+1,0:ny+1)
      pointer(prrv,rrv)

      double precision volv ( 0:nx+1,0:ny+1)
      pointer(pvolv,volv)

      double precision hxv ( 0:nx+1,0:ny+1)
      pointer(phxv,hxv)

      double precision syv ( 0:nx+1,0:ny+1)
      pointer(psyv,syv)

      integer isxptx ( 0:nx+1,0:ny+1)
      pointer(pisxptx,isxptx)

      integer isxpty ( 0:nx+1,0:ny+1)
      pointer(pisxpty,isxpty)

      double precision lcon ( 0:nx+1,0:ny+1)
      pointer(plcon,lcon)

      double precision lconi ( 0:nx+1,0:ny+1)
      pointer(plconi,lconi)

      double precision lcone ( 0:nx+1,0:ny+1)
      pointer(plcone,lcone)

      double precision lconneo ( 0:nx+1,0:ny+1)
      pointer(plconneo,lconneo)

      double precision epsneo ( 0:nx+1,0:ny+1)
      pointer(pepsneo,epsneo)

      integer isixcore ( 0:nx+1)
      pointer(pisixcore,isixcore)
      common /com113/ sygytotc, area_core, ghxpt, gvxpt, sxyxpt
      common /com113/ ghxpt_lower, gvxpt_lower, sxyxpt_lower
      common /com113/ ghxpt_upper, gvxpt_upper, sxyxpt_upper, linelen
      common /com113/ dxmin
      common /com116/ pvol, pgx, pgy, pdx
      common /com116/ pdxvf, pdy, pgxf, pgxfn
      common /com116/ pgyf, pgxc, pgyc, pxnrm
      common /com116/ pxvnrm, pynrm, pyvnrm, psx
      common /com116/ psxnp, psy, prr, pxcs
      common /com116/ pxfs, pxcwi, pxfwi, pxfpf
      common /com116/ pxcpf, pxcwo, pxfwo, pyyc
      common /com116/ pyyf, pyylb, pyyrb, pxcv
      common /com116/ pxfv, ppsinormc, ppsinormf
      common /com116/ prrv, pvolv, phxv, psyv
      common /com116/ pisxptx, pisxpty, plcon
      common /com116/ plconi, plcone, plconneo
      common /com116/ pepsneo, pisixcore
c End of Comgeo

c Group Noggeo

      double precision vtag ( 0:nx+1,0:ny+1)
      pointer(pvtag,vtag)

      double precision angfx ( 0:nx+1,0:ny+1)
      pointer(pangfx,angfx)

      double precision fxm ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxm,fxm)

      double precision fx0 ( 0:nx+1,0:ny+1,0:1)
      pointer(pfx0,fx0)

      double precision fxp ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxp,fxp)

      double precision fym ( 0:nx+1,0:ny+1,0:1)
      pointer(pfym,fym)

      double precision fy0 ( 0:nx+1,0:ny+1,0:1)
      pointer(pfy0,fy0)

      double precision fyp ( 0:nx+1,0:ny+1,0:1)
      pointer(pfyp,fyp)

      double precision fxmy ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmy,fxmy)

      double precision fxpy ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpy,fxpy)

      double precision fymx ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymx,fymx)

      double precision fypx ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypx,fypx)

      double precision fxmv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmv,fxmv)

      double precision fx0v ( 0:nx+1,0:ny+1,0:1)
      pointer(pfx0v,fx0v)

      double precision fxpv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpv,fxpv)

      double precision fymv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymv,fymv)

      double precision fy0v ( 0:nx+1,0:ny+1,0:1)
      pointer(pfy0v,fy0v)

      double precision fypv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypv,fypv)

      double precision fxmyv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmyv,fxmyv)

      double precision fxpyv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpyv,fxpyv)

      double precision fymxv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymxv,fymxv)

      double precision fypxv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypxv,fypxv)
      common /com136/ pvtag, pangfx, pfxm, pfx0
      common /com136/ pfxp, pfym, pfy0, pfyp
      common /com136/ pfxmy, pfxpy, pfymx, pfypx
      common /com136/ pfxmv, pfx0v, pfxpv, pfymv
      common /com136/ pfy0v, pfypv, pfxmyv
      common /com136/ pfxpyv, pfymxv, pfypxv
c End of Noggeo
c fxm,fx0,fxp,fxmy,fxpy
c Group Gradients
      double precision einduc

      double precision ex ( 0:nx+1,0:ny+1)
      pointer(pex,ex)

      double precision ey ( 0:nx+1,0:ny+1)
      pointer(pey,ey)

      double precision gpix ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pgpix,gpix)

      double precision gpiy ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pgpiy,gpiy)

      double precision gpex ( 0:nx+1,0:ny+1)
      pointer(pgpex,gpex)

      double precision gpey ( 0:nx+1,0:ny+1)
      pointer(pgpey,gpey)

      double precision gprx ( 0:nx+1,0:ny+1)
      pointer(pgprx,gprx)

      double precision gpry ( 0:nx+1,0:ny+1)
      pointer(pgpry,gpry)

      double precision gtex ( 0:nx+1,0:ny+1)
      pointer(pgtex,gtex)

      double precision gtey ( 0:nx+1,0:ny+1)
      pointer(pgtey,gtey)

      double precision gtix ( 0:nx+1,0:ny+1)
      pointer(pgtix,gtix)

      double precision gtiy ( 0:nx+1,0:ny+1)
      pointer(pgtiy,gtiy)
      common /bbb333/ einduc
      common /bbb336/ pex, pey, pgpix, pgpiy
      common /bbb336/ pgpex, pgpey, pgprx, pgpry
      common /bbb336/ pgtex, pgtey, pgtix, pgtiy
c End of Gradients

c Group Phyvar
      double precision pi, me, mp, ev, qe, mu0, eps0, rt8opi
      common /bbb173/ pi, me, mp, ev, qe, mu0, eps0, rt8opi
c End of Phyvar
c pi,ev
c Group Coefeq
      double precision cnfx, cnfy, cnsor, cfneut, cfnidh, cfupcx, cfticx
      double precision cfupimpg, cftiimpg, cmneut, cnflux(6)
      double precision chradi, chradr, chioniz, cne_sgvi, ctsor, ceisor
      double precision ccoldsor, cngfx(6), cngfy(6)
      double precision cngmom(31), cmwall(31), cngtgx(6)
      double precision cngtgy(6), sxgsol, sxgpr, xstscal
      double precision rld2dxg(6), rld2dyg(6), cngflox(6)
      double precision cngfloy(6), cngniflox(31,6)
      double precision cngnifloy(31,6), cngsor, cdifg(6)
      double precision lgmax(6), lgtmax(6), lgvmax
      double precision rtg2ti(6), tgas(6), cmfx, cmfy, cpgx
      double precision cfvisx, cfvisy, cfanomvisxg, cfanomvisyg, cfvisxn
      double precision cfvisxy(1:31), cfvxnrr, cfvisyn
      double precision cfvcsx(1:31), cfvcsy(1:31), vboost, cvgp
      double precision cfvgpx(1:31), cfvgpy(1:31), cfbgt, cfjhf
      double precision cf2ef, cfyef, cftef, cf2bf, cfybf, cfcbti, cfcurv
      double precision cfgradb, cfq2bf, cfqybf, cfqyn, cfqym, cfqydt
      double precision cf2dd, cfydd, cftdd, cfrd, cfvisxneov, cfvisxneoq
      double precision cfvycr, cfvycf, cfvyavis, cfjve, cfjp2, cfjpy
      double precision cfnfmiy, cnimp, fac2sp, cftnm, cfupjr, cfcximp1
      double precision cfcximp2, cfnetap, fcdif, cfmsor, cpiup(31)
      double precision cfloyi, cfloye, cfcvte, cfcvti, cfcvtg, cfloxiplt
      double precision cfloygwall, cftgdiss(6), exjbdry, cfgpijr
      double precision zeffcon, alftng, cfqya, cfqyao, cfqyae, cfqyai
      double precision cfhcxgc(6), cfhcygc(6), cftgcond
      double precision cftgeqp
      integer ifxnsgi, isvisxn_old, jhswitch, isnfmiy, iszeffcon
      common /bbb40/ ifxnsgi, isvisxn_old, jhswitch, isnfmiy, iszeffcon
      common /bbb43/ cnfx, cnfy, cnsor, cfneut, cfnidh, cfupcx, cfticx
      common /bbb43/ cfupimpg, cftiimpg, cmneut, cnflux, chradi, chradr
      common /bbb43/ chioniz, cne_sgvi, ctsor, ceisor, ccoldsor, cngfx
      common /bbb43/ cngfy, cngmom, cmwall, cngtgx, cngtgy, sxgsol
      common /bbb43/ sxgpr, xstscal, rld2dxg, rld2dyg, cngflox, cngfloy
      common /bbb43/ cngniflox, cngnifloy, cngsor, cdifg, lgmax, lgtmax
      common /bbb43/ lgvmax, rtg2ti, tgas, cmfx, cmfy, cpgx, cfvisx
      common /bbb43/ cfvisy, cfanomvisxg, cfanomvisyg, cfvisxn, cfvisxy
      common /bbb43/ cfvxnrr, cfvisyn, cfvcsx, cfvcsy, vboost, cvgp
      common /bbb43/ cfvgpx, cfvgpy, cfbgt, cfjhf, cf2ef, cfyef, cftef
      common /bbb43/ cf2bf, cfybf, cfcbti, cfcurv, cfgradb, cfq2bf
      common /bbb43/ cfqybf, cfqyn, cfqym, cfqydt, cf2dd, cfydd, cftdd
      common /bbb43/ cfrd, cfvisxneov, cfvisxneoq, cfvycr, cfvycf
      common /bbb43/ cfvyavis, cfjve, cfjp2, cfjpy, cfnfmiy, cnimp
      common /bbb43/ fac2sp, cftnm, cfupjr, cfcximp1, cfcximp2, cfnetap
      common /bbb43/ fcdif, cfmsor, cpiup, cfloyi, cfloye, cfcvte
      common /bbb43/ cfcvti, cfcvtg, cfloxiplt, cfloygwall, cftgdiss
      common /bbb43/ exjbdry, cfgpijr, zeffcon, alftng, cfqya, cfqyao
      common /bbb43/ cfqyae, cfqyai, cfhcxgc, cfhcygc, cftgcond, cftgeqp
c End of Coefeq
c cngtgx
c Group Imprad
      integer isimpon, nusp_imp, isupimpap, ismctab

      double precision nzloc ( 0:nzspmx)
      pointer(pnzloc,nzloc)

      double precision impradloc ( 0:nzspmx)
      pointer(pimpradloc,impradloc)

      double precision pwrzec ( 0:nx+1,0:ny+1)
      pointer(ppwrzec,pwrzec)

      double precision pwrze ( 0:nx+1,0:ny+1)
      pointer(ppwrze,pwrze)

      double precision pradc ( 0:nx+1,0:ny+1)
      pointer(ppradc,pradc)

      double precision pradcff ( 0:nx+1,0:ny+1)
      pointer(ppradcff,pradcff)

      double precision prad ( 0:nx+1,0:ny+1)
      pointer(pprad,prad)

      double precision pradzc ( 0:nx+1,0:ny+1,0:nzspmx,1:ngsp-1)
      pointer(ppradzc,pradzc)

      double precision pradz ( 0:nx+1,0:ny+1,0:nzspmx,1:ngsp-1)
      pointer(ppradz,pradz)

      double precision na ( 0:nx+1,0:ny+1)
      pointer(pna,na)

      double precision ntau ( 0:nx+1,0:ny+1)
      pointer(pntau,ntau)

      double precision nratio ( 0:nx+1,0:ny+1)
      pointer(pnratio,nratio)

      double precision afrac ( 0:nx+1,0:ny+1)
      pointer(pafrac,afrac)

      double precision atau ( 0:nx+1,0:ny+1)
      pointer(patau,atau)

      double precision tau1 ( 0:nx+1,0:ny+1)
      pointer(ptau1,tau1)

      double precision tau2 ( 0:nx+1,0:ny+1)
      pointer(ptau2,tau2)
      common /bbb740/ isimpon, nusp_imp, isupimpap, ismctab
      common /bbb746/ pnzloc, pimpradloc, ppwrzec
      common /bbb746/ ppwrze, ppradc, ppradcff
      common /bbb746/ pprad, ppradzc, ppradz
      common /bbb746/ pna, pntau, pnratio
      common /bbb746/ pafrac, patau, ptau1
      common /bbb746/ ptau2
c End of Imprad
c isimpon
c Group Indices_domain_dcl
      integer nx_loc, ny_loc, nvrsendl, nvisendl, ixmnbcl, ixmxbcl
      integer iymnbcl, iymxbcl, idxp1, idxm1, idyp1, idym1, idcorn(1:4)
      integer iv_totbdy(1:8), typebdyi(1:4), typecni(1:4), typebdy(1:4)
      integer typecn(1:4), neq_locl, numvarl, ispwrbcl, ixpt1l, ixpt2l
      integer iysptrx1l, ixlbl, ixrbl

      double precision vrsendl ( nvrsendl)
      pointer(pvrsendl,vrsendl)

      integer visendl ( nvisendl)
      pointer(pvisendl,visendl)

      integer ivloc2sdgl ( nvisendl)
      pointer(pivloc2sdgl,ivloc2sdgl)

      integer ivloc2mdgl ( nvisendl)
      pointer(pivloc2mdgl,ivloc2mdgl)

      integer ivl2gstnll ( neq_locl,9*numvarl)
      pointer(pivl2gstnll,ivl2gstnll)
      common /bbb660/ nx_loc, ny_loc, nvrsendl, nvisendl, ixmnbcl
      common /bbb660/ ixmxbcl, iymnbcl, iymxbcl, idxp1, idxm1, idyp1
      common /bbb660/ idym1, idcorn, iv_totbdy, typebdyi, typecni
      common /bbb660/ typebdy, typecn, neq_locl, numvarl, ispwrbcl
      common /bbb660/ ixpt1l, ixpt2l, iysptrx1l, ixlbl, ixrbl
      common /bbb666/ pvrsendl, pvisendl, pivloc2sdgl
      common /bbb666/ pivloc2mdgl, pivl2gstnll
c End of Indices_domain_dcl
cixmxbcl,ixmnbcl,iymxbcl,iymnbcl
ctypebdy,typecn,iv_totbdy
c Group Indices_domain_dcg
      integer isddcon, ndleg(1:10,1:2), ndxcore(1:10), ndycore(1:10)
      integer ndysol(1:10), idxpt(1:2), ndxt, ndyt, ndomain
      integer ndomain_orig, nvrsend, nvisend, ixmin(32)
      integer ixmax(32), iymin(32), iymax(32)
      integer ixmnbcg(32), ixmxbcg(32), iymnbcg(32)
      integer iymxbcg(32), ncell(32), idxp1g(32)
      integer idxm1g(32), idyp1g(32), idym1g(32)
      integer idcorng(32,1:4), ixpt1g(32)
      integer ixpt2g(32), iysptrxg(32), neq_locgmx
      integer ispwrbc(32)

      double precision vrsend ( nvrsend)
      pointer(pvrsend,vrsend)

      integer visend ( nvisend)
      pointer(pvisend,visend)

      integer neq_locg ( 32)
      pointer(pneq_locg,neq_locg)
      common /bbb640/ isddcon, ndleg, ndxcore, ndycore, ndysol, idxpt
      common /bbb640/ ndxt, ndyt, ndomain, ndomain_orig, nvrsend
      common /bbb640/ nvisend, ixmin, ixmax, iymin, iymax, ixmnbcg
      common /bbb640/ ixmxbcg, iymnbcg, iymxbcg, ncell, idxp1g, idxm1g
      common /bbb640/ idyp1g, idym1g, idcorng, ixpt1g, ixpt2g, iysptrxg
      common /bbb640/ neq_locgmx, ispwrbc
      common /bbb646/ pvrsend, pvisend, pneq_locg
c End of Indices_domain_dcg
cisddcon
c Group Npes_mpi
      integer npes, mype, ismpion, hascomm, isparmultdt
      common /bbb630/ npes, mype, ismpion, hascomm, isparmultdt
c End of Npes_mpi
cmype

cforces Forthon scripts to put implicit none above here
      integer ifake

c ... Set mpi indices, etc
cC c_mpi      include 'mpif.h'
c_mpi      integer status(MPI_STATUS_SIZE)
c_mpi      integer ierr

      id = 1
      if (ixl .lt. 0 .or. yinc .ge. 6) then
         is = 1-ixmnbcl
         ie = nx+ixmxbcl
      else
         is = ixl
         ie = ixl
      endif

      if (iyl .lt. 0 .or. yinc .ge. 6) then
         js = 1-iymnbcl
         je = ny+iymxbcl
      else
         js = iyl
         je = iyl
      endif

      do 20 iy = js, je
c was nx+1
         do 19 ix = is, ie
            ne(ix,iy) = 0.0d0
            nit(ix,iy) = 0.0d0
            nm(ix,iy,1) = 0.0d0
            nz2(ix,iy) = 0.0d0
   19       continue
   20    continue

c not used since te & ti have temin eV floor
      inegt = 0
      inegng = 0
      inegni = 0

c use full loop even if some isnionxyy=0;
      do 50 ifld = 1, nisp
         do 40 iy = js, je
c was nx+1
            do 30 ix = is, ie
               if (isnionxy(ix,iy,ifld).eq.1) then
                  ni(ix,iy,ifld) = yl(idxn(ix,iy,ifld))*n0(ifld)
                  if (ni(ix,iy,ifld) .lt. 0) then
                     inegni = 1
                     ixneg = ix
                     iyneg = iy
                     ifldneg = ifld
                  endif
                  if (zi(ifld).eq.0 .and. ineudif.eq.3) then
                     ni(ix,iy,ifld) = exp(yl(idxn(ix,iy,ifld)))
                  endif
               endif
               ne(ix,iy) = ne(ix,iy) + zi(ifld)*ni(ix,iy,ifld)
               if (isupgon(1).eq.1 .and. zi(ifld).eq.0) then
                  ng(ix,iy,1) = ni(ix,iy,ifld)
                  if (ineudif .eq. 3) lng(ix,iy,1)=log(ng(ix,iy,1))
               else
                  nit(ix,iy) = nit(ix,iy) + ni(ix,iy,ifld)
                  if (isimpon.ge.5 .and. nusp_imp.eq.0) nm(ix,iy,1)=nm(
     &                  ix,iy,1)+ni(ix,iy,ifld)*mi(ifld)
                  nz2(ix,iy) = nz2(ix,iy) + ni(ix,iy,ifld)*zi(ifld)**2
               endif
               nm(ix,iy,ifld) = ni(ix,iy,ifld)*mi(ifld)
   30          continue
   40       continue
   50    continue

      do 7 iy = js, je
         do 6 ix = is, ie
            ntemp = ne(ix,iy)
            if (isflxvar .eq. 0) ntemp = nnorm
            if (isteonxy(ix,iy) .eq. 1) then
               te(ix,iy)=yl(idxte(ix,iy))*ennorm/(1.5d0*ntemp)
cNEW Feb4,2018
               te(ix,iy) = max(te(ix,iy), temin*ev)
            endif
            do 65 igsp =1, ngsp
               if (isngonxy(ix,iy,igsp) .eq. 1) then
                  if (ineudif .ne. 3) then
                     ng(ix,iy,igsp) = yl(idxg(ix,iy,igsp))*n0g(igsp)
                     if (ng(ix,iy,igsp) .lt. 0) then
                        inegng = 1
                        ixneg = ix
                        iyneg = iy
                        igspneg = igsp
                     endif
                  elseif (ineudif .eq. 3) then
                     lng(ix,iy,igsp) = yl(idxg(ix,iy,igsp))
                     ng(ix,iy,igsp) = exp(lng(ix,iy,igsp))
                  endif
               endif
               if (istgonxy(ix,iy,igsp) .eq. 1) then
                  ntemp = ng(ix,iy,igsp)
                  if (isflxvar .eq. 0) ntemp = n0g(igsp)
                  tg(ix,iy,igsp) = yl(idxtg(ix,iy,igsp))*ennorm/ (1.5d0*
     &               ntemp)
                  tg(ix,iy,igsp) = max(tg(ix,iy,igsp), temin*ev)
               endif
   65          continue
            ntemp = nit(ix,iy) + cngtgx(1)*ng(ix,iy,1)
            if (isflxvar .eq. 0) ntemp = nnorm
            if (istionxy(ix,iy) .eq. 1) then
               ti(ix,iy)=yl(idxti(ix,iy))*ennorm/(1.5d0*ntemp)
               ti(ix,iy) = max(ti(ix,iy), temin*ev)
            endif
            if (isphionxy(ix,iy) .eq. 1) phi(ix,iy) = yl(idxphi(ix,iy))*
     &            temp0
    6       continue
    7    continue

      if (inegni .gt. 0 .and. itrap_negni.eq.1) then
         call remark("***  ni is negative - calculation stopped")
         write(*,*) 'At  ix =', ixneg, ' iy =', iyneg, ' ifld =', 
     &      ifldneg
         call xerrab("")
      endif
      if (inegng .gt. 0 .and. itrap_negng.eq.1) then
         call remark("***  ng is negative - calculation stopped")
         write(*,*) 'At  ix =', ixneg, ' iy =', iyneg, ' igsp =', 
     &      igspneg
         call xerrab("")
      endif
cc Since Te and Ti have temin eV floors, this not used
cc      if (inegt .gt. 0 .and. itrap_negt.eq.1) then
cc         call xerrab("***  Te or Ti is negative - calculation stopped")
cc      endif

c the message passing is done twice here to get nm for up - very inefficient
c *** Mpi message passing if this is a parallel calculation - only need for
c *** isflxvar.ne.0
c++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (isddcon .ge. 1 .and. ixl .lt. 0) then
         call sendbdry(mype+1)
         call recvbdry(mype+1)
      endif
c++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      do 10 ifld = 1, nusp
         do 9 iy = js, je
            do 8 ix = is, ie
               if (isuponxy(ix,iy,ifld) .eq. 1) then
                  ix1 = ixp1(ix,iy)
                  ix2 = max(1-ixmnbcl, ixm1(ix,iy))
                  t1 = 0.5d0*( nm(ix2,iy,ifld)+nm(ix, iy,ifld) )
                  t2 = 0.5d0*( nm(ix, iy,ifld)+nm(ix1,iy,ifld) )
                  if (isflxvar .eq. 0 .or. isflxvar .eq. 2) then
                     t1 = mi(ifld)*n0(ifld)
                     t2 = mi(ifld)*n0(ifld)
                  endif
                  up(ix2,iy,ifld) = yl(idxu(ix2,iy,ifld))*fnorm(ifld)/t1
                  up(ix,iy,ifld) = yl(idxu(ix,iy,ifld))*fnorm(ifld)/t2
                  if (isup1up2.eq.1) then
ctemp model for up2 if isupon(2)=0
                     up(ix2,iy,2) = rup21*up(ix2,iy,1)
                     up(ix,iy,2) = rup21*up(ix,iy,1)
                  endif
               endif
    8          continue
    9       continue
   10    continue

c *** Mpi message passing if this is a parallel calculation; should only do up here
c++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (isddcon .ge. 1 .and. ixl .lt. 0) then
         call sendbdry(mype+1)
         call recvbdry(mype+1)
      endif
c++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      return
      end

c ***** end of subroutines convsr_vo ********
c-----------------------------------------------------------------------
      subroutine convsr_aux (ixl, iyl, yl)
cProlog

c...  Calculates various plasmas quantities used repeatedly in pandf

      implicit none

c  -- input arguments
      integer ixl, iyl, inc
      doubleprecision yl(1)
c  -- local variables
      doubleprecision ntemp
      integer is, ie, js, je, k, l
      integer ifld, id
      integer impflag, inegt, inegng
      integer jx,ixlp1,ixlp2,ixrm1
c  -- external functions
      doubleprecision zimp, rnec, zeffc, intpnog

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nhsp,nzsp,nisp,nusp,ngsp
c Group Xpoint_indices
      integer iysptrx

      integer ixlb ( 1:nxpt)
      pointer(pixlb,ixlb)

      integer ixpt1 ( 1:nxpt)
      pointer(pixpt1,ixpt1)

      integer ixmdp ( 1:nxpt)
      pointer(pixmdp,ixmdp)

      integer ixpt2 ( 1:nxpt)
      pointer(pixpt2,ixpt2)

      integer ixrb ( 1:nxpt)
      pointer(pixrb,ixrb)

      integer iysptrx1 ( 1:nxpt)
      pointer(piysptrx1,iysptrx1)

      integer iysptrx2 ( 1:nxpt)
      pointer(piysptrx2,iysptrx2)
      common /com90/ iysptrx
      common /com96/ pixlb, pixpt1, pixmdp
      common /com96/ pixpt2, pixrb, piysptrx1
      common /com96/ piysptrx2
c End of Xpoint_indices
c ixpt1,ixpt2,iysptrx1,iysptrx2,ixlb,ixrb
c Group Math_problem_size
      integer neqmx, numvar, numvarbwpad
      common /bbb10/ neqmx, numvar, numvarbwpad
c End of Math_problem_size
c neqmx
c Group Compla
      double precision facmg(1:31), istgcon(6), rtauxfac
      double precision rtauyfac, rt_scal, fracvgpgp

      double precision mi ( 1:nisp)
      pointer(pmi,mi)

      double precision zi ( 1:nisp)
      pointer(pzi,zi)

      double precision mg ( 1:ngsp)
      pointer(pmg,mg)

      integer znucl ( 1:nisp)
      pointer(pznucl,znucl)

      double precision ni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pni,ni)

      double precision lni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(plni,lni)

      double precision nm ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnm,nm)

      double precision nz2 ( 0:nx+1,0:ny+1)
      pointer(pnz2,nz2)

      double precision uu ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puu,uu)

      double precision uup ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puup,uup)

      double precision up ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pup,up)

      double precision upi ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupi,upi)

      double precision upifmb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupifmb,upifmb)

      double precision uz ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puz,uz)

      double precision v2 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2,v2)

      double precision v2xgp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2xgp,v2xgp)

      double precision v2ce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2ce,v2ce)

      double precision v2cb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cb,v2cb)

      double precision ve2cb ( 0:nx+1,0:ny+1)
      pointer(pve2cb,ve2cb)

      double precision v2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cd,v2cd)

      double precision ve2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pve2cd,ve2cd)

      double precision q2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pq2cd,q2cd)

      double precision v2rd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2rd,v2rd)

      double precision v2dd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2dd,v2dd)

      double precision vy ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvy,vy)

      double precision vygp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvygp,vygp)

      double precision vytan ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvytan,vytan)

      double precision vygtan ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvygtan,vygtan)

      double precision vyce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyce,vyce)

      double precision vycb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycb,vycb)

      double precision veycb ( 0:nx+1,0:ny+1)
      pointer(pveycb,veycb)

      double precision vycp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycp,vycp)

      double precision veycp ( 0:nx+1,0:ny+1)
      pointer(pveycp,veycp)

      double precision vyrd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyrd,vyrd)

      double precision vydd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvydd,vydd)

      double precision vyavis ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyavis,vyavis)

      double precision vex ( 0:nx+1,0:ny+1)
      pointer(pvex,vex)

      double precision upe ( 0:nx+1,0:ny+1)
      pointer(pupe,upe)

      double precision vep ( 0:nx+1,0:ny+1)
      pointer(pvep,vep)

      double precision ve2 ( 0:nx+1,0:ny+1)
      pointer(pve2,ve2)

      double precision vey ( 0:nx+1,0:ny+1)
      pointer(pvey,vey)

      double precision vycf ( 0:nx+1,0:ny+1)
      pointer(pvycf,vycf)

      double precision vycr ( 0:nx+1,0:ny+1)
      pointer(pvycr,vycr)

      double precision te ( 0:nx+1,0:ny+1)
      pointer(pte,te)

      double precision ti ( 0:nx+1,0:ny+1)
      pointer(pti,ti)

      double precision ng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(png,ng)

      double precision lng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(plng,lng)

      double precision uug ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(puug,uug)

      double precision vyg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvyg,vyg)

      double precision tg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptg,tg)

      double precision tev ( 0:nx+1,0:ny+1)
      pointer(ptev,tev)

      double precision niv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniv,niv)

      double precision upv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupv,upv)

      double precision ngv ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngv,ngv)

      double precision tiv ( 0:nx+1,0:ny+1)
      pointer(ptiv,tiv)

      double precision niy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0,niy0)

      double precision niy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1,niy1)

      double precision niy0s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0s,niy0s)

      double precision niy1s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1s,niy1s)

      double precision ney0 ( 0:nx+1,0:ny+1)
      pointer(pney0,ney0)

      double precision ney1 ( 0:nx+1,0:ny+1)
      pointer(pney1,ney1)

      double precision nity0 ( 0:nx+1,0:ny+1)
      pointer(pnity0,nity0)

      double precision nity1 ( 0:nx+1,0:ny+1)
      pointer(pnity1,nity1)

      double precision tey0 ( 0:nx+1,0:ny+1)
      pointer(ptey0,tey0)

      double precision tey1 ( 0:nx+1,0:ny+1)
      pointer(ptey1,tey1)

      double precision tiy0 ( 0:nx+1,0:ny+1)
      pointer(ptiy0,tiy0)

      double precision tiy1 ( 0:nx+1,0:ny+1)
      pointer(ptiy1,tiy1)

      double precision tiy0s ( 0:nx+1,0:ny+1)
      pointer(ptiy0s,tiy0s)

      double precision tiy1s ( 0:nx+1,0:ny+1)
      pointer(ptiy1s,tiy1s)

      double precision tgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy0,tgy0)

      double precision tgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy1,tgy1)

      double precision ngy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy0,ngy0)

      double precision ngy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy1,ngy1)

      double precision pgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy0,pgy0)

      double precision pgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy1,pgy1)

      double precision pg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppg,pg)

      double precision phiy0 ( 0:nx+1,0:ny+1)
      pointer(pphiy0,phiy0)

      double precision phiy1 ( 0:nx+1,0:ny+1)
      pointer(pphiy1,phiy1)

      double precision phiy0s ( 0:nx+1,0:ny+1)
      pointer(pphiy0s,phiy0s)

      double precision phiy1s ( 0:nx+1,0:ny+1)
      pointer(pphiy1s,phiy1s)

      double precision pr ( 0:nx+1,0:ny+1)
      pointer(ppr,pr)

      double precision prev ( 0:nx+1,0:ny+1)
      pointer(pprev,prev)

      double precision prtv ( 0:nx+1,0:ny+1)
      pointer(pprtv,prtv)

      double precision pri ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppri,pri)

      double precision priv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriv,priv)

      double precision priy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy0,priy0)

      double precision priy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy1,priy1)

      double precision pre ( 0:nx+1,0:ny+1)
      pointer(ppre,pre)

      double precision ne ( 0:nx+1,0:ny+1)
      pointer(pne,ne)

      double precision nit ( 0:nx+1,0:ny+1)
      pointer(pnit,nit)

      double precision nginit ( 0:nx+1,0:ny+1)
      pointer(pnginit,nginit)

      double precision phi ( 0:nx+1,0:ny+1)
      pointer(pphi,phi)

      double precision phiv ( 0:nx+1,0:ny+1)
      pointer(pphiv,phiv)

      double precision zeff ( 0:nx+1,0:ny+1)
      pointer(pzeff,zeff)

      double precision netap ( 0:nx+1,0:ny+1)
      pointer(pnetap,netap)

      double precision znot ( 0:nx+1,0:ny+1)
      pointer(pznot,znot)

      double precision zimpc ( 0:nx+1,0:ny+1)
      pointer(pzimpc,zimpc)

      double precision nil ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnil,nil)

      double precision upl ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupl,upl)

      double precision tel ( 0:nx+1,0:ny+1)
      pointer(ptel,tel)

      double precision til ( 0:nx+1,0:ny+1)
      pointer(ptil,til)

      double precision ngl ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngl,ngl)

      double precision phil ( 0:nx+1,0:ny+1)
      pointer(pphil,phil)

      double precision upxpt ( 1:nusp,1:nxpt)
      pointer(pupxpt,upxpt)

      double precision nixpt ( 1:nusp,1:nxpt)
      pointer(pnixpt,nixpt)

      double precision visyxpt ( 1:nusp,1:nxpt)
      pointer(pvisyxpt,visyxpt)

      double precision vyhxpt ( 1:nusp,1:nxpt)
      pointer(pvyhxpt,vyhxpt)

      double precision vyvxpt ( 1:nusp,1:nxpt)
      pointer(pvyvxpt,vyvxpt)

      double precision fmihxpt ( 1:nusp,1:nxpt)
      pointer(pfmihxpt,fmihxpt)

      double precision fmivxpt ( 1:nusp,1:nxpt)
      pointer(pfmivxpt,fmivxpt)

      double precision rtaux ( 0:nx+1,0:ny+1)
      pointer(prtaux,rtaux)

      double precision rtauy ( 0:nx+1,0:ny+1)
      pointer(prtauy,rtauy)

      double precision rtau ( 0:nx+1,0:ny+1)
      pointer(prtau,rtau)

      double precision betap ( 0:nx+1,0:ny+1)
      pointer(pbetap,betap)
      common /bbb243/ facmg, istgcon, rtauxfac, rtauyfac, rt_scal
      common /bbb243/ fracvgpgp
      common /bbb246/ pmi, pzi, pmg, pznucl
      common /bbb246/ pni, plni, pnm, pnz2
      common /bbb246/ puu, puup, pup, pupi
      common /bbb246/ pupifmb, puz, pv2, pv2xgp
      common /bbb246/ pv2ce, pv2cb, pve2cb
      common /bbb246/ pv2cd, pve2cd, pq2cd
      common /bbb246/ pv2rd, pv2dd, pvy, pvygp
      common /bbb246/ pvytan, pvygtan, pvyce
      common /bbb246/ pvycb, pveycb, pvycp
      common /bbb246/ pveycp, pvyrd, pvydd
      common /bbb246/ pvyavis, pvex, pupe, pvep
      common /bbb246/ pve2, pvey, pvycf, pvycr
      common /bbb246/ pte, pti, png, plng
      common /bbb246/ puug, pvyg, ptg, ptev
      common /bbb246/ pniv, pupv, pngv, ptiv
      common /bbb246/ pniy0, pniy1, pniy0s
      common /bbb246/ pniy1s, pney0, pney1
      common /bbb246/ pnity0, pnity1, ptey0
      common /bbb246/ ptey1, ptiy0, ptiy1
      common /bbb246/ ptiy0s, ptiy1s, ptgy0
      common /bbb246/ ptgy1, pngy0, pngy1, ppgy0
      common /bbb246/ ppgy1, ppg, pphiy0, pphiy1
      common /bbb246/ pphiy0s, pphiy1s, ppr
      common /bbb246/ pprev, pprtv, ppri, ppriv
      common /bbb246/ ppriy0, ppriy1, ppre, pne
      common /bbb246/ pnit, pnginit, pphi, pphiv
      common /bbb246/ pzeff, pnetap, pznot
      common /bbb246/ pzimpc, pnil, pupl, ptel
      common /bbb246/ ptil, pngl, pphil, pupxpt
      common /bbb246/ pnixpt, pvisyxpt, pvyhxpt
      common /bbb246/ pvyvxpt, pfmihxpt, pfmivxpt
      common /bbb246/ prtaux, prtauy, prtau
      common /bbb246/ pbetap
c End of Compla
c ,zi,zeff,zimpc
c Group Ynorm
      double precision var_scale_floor, vsf_up, vsf_phi, n0(31)
      double precision n0g(6), temp0, dx0, nnorm, ennorm, sigbar0
      double precision vpnorm, rdoff
      integer iscolnorm, isflxvar, isrscalf, isyloext

      double precision norm_cons ( numvar)
      pointer(pnorm_cons,norm_cons)

      double precision floor_cons ( numvar)
      pointer(pfloor_cons,floor_cons)

      double precision fnorm ( 1:nusp)
      pointer(pfnorm,fnorm)

      double precision suscal ( neqmx)
      pointer(psuscal,suscal)

      double precision sfscal ( neqmx)
      pointer(psfscal,sfscal)

      double precision yloext ( neqmx)
      pointer(pyloext,yloext)
      common /bbb160/ iscolnorm, isflxvar, isrscalf, isyloext
      common /bbb163/ var_scale_floor, vsf_up, vsf_phi, n0, n0g, temp0
      common /bbb163/ dx0, nnorm, ennorm, sigbar0, vpnorm, rdoff
      common /bbb166/ pnorm_cons, pfloor_cons, pfnorm
      common /bbb166/ psuscal, psfscal, pyloext
c End of Ynorm
c isflxvar,temp0,nnorm,ennorm,fnorm,n0,n0g
c Group UEpar
      double precision csfaclb(31,2), csfacrb(31,2)
      integer methe, methu, methn, methi, methg, methp, isgxvon
      double precision csfacti, cslim, dcslim, lnlam, cfaccony, isvylog
      double precision cniatol, cngatol, cupatol, cteatol, ctiatol
      integer ishavisy, isintlog, concap, convis, icnuiz, icnucx
      double precision cphiatol, tolbf, tadj, cnuiz, cnucx, cfrecom
      double precision ngbackg(6), cflbg, facngbackg2ngs(6)
      double precision nzbackg(31), facnzbackg2nis(31)
      double precision upclng(31), facupclng2ups(31), tebg, tibg
      double precision temin, temin2, pwrbkg_c, pwribkg_c, cfwjdotelim
      double precision nlimix(31), nlimiy(31), nlimgx, nlimgy
      double precision xgbx, agdc, pcolwid, eion, ediss, ebind, tfcx
      integer isrecmon, igas, ingb, inflbg, inzb, iteb, is1D_gbx, ixgb
      double precision tfcy, afix, coef, ce, ci, dp1, qfl, csh, qsh, mfl
      double precision msh, ro, cs, fxe, ctaue, fxi, ctaui, zcoef, coef1
      double precision cnurn, cnuru, cnure, cnuri, cnurg, cnurp, nurlxn
      character*72 label
      double precision nurlxu, nurlxe, nurlxi, nurlxg, nurlxp, rnewpot
      character*8 svrpkg
      character*80 petscoptfile
      character*2048 petscopts
      integer ncrhs, istep, iter, ishymol, isfqpave, isgpye, iigsp
      integer itrap_negni, itrap_negt, itrap_negng, isybdryog, isybdrywd
      double precision r0slab, te_s_dis, fnnuiz, thetar, iseesorave
      integer isxmpog, iexclnxc1, ineudif, isbcwdt, ishosor, issyvxpt0
      integer isrrvave, isdtsfscal, isplflxl, isplflxlv, isplflxlgx
      integer isplflxlgxy, iswflxlgy, isplflxlvgx, isplflxlvgxy
      double precision ispsorave, fsprd, rr_fac, rrmin, frfqpn, cffqpsat
      integer iswflxlvgy, isplflxltgx, isplflxltgxy, iswflxltgy
      integer isfeexpl0, isfeixpl0, isofric, iskaboom, isnglf, isngrf
      double precision flalfipl, flalfepl, del_te_ro, nglfix, ngrfix
      integer isnion(31), isupon(31), isup1up2, isupgon(6)
      integer isteon, istion, isngon(6), istgon(6), isphion
      integer isphiofft, isnewpot, isugfm1side, isnupdot1sd, isphicore0
      double precision rup21, z0_imp_const
      integer is_z0_imp_const

      integer isnionxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisnionxy,isnionxy)

      integer isuponxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisuponxy,isuponxy)

      integer isteonxy ( 0:nx+1,0:ny+1)
      pointer(pisteonxy,isteonxy)

      integer istionxy ( 0:nx+1,0:ny+1)
      pointer(pistionxy,istionxy)

      integer isngonxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pisngonxy,isngonxy)

      integer istgonxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pistgonxy,istgonxy)

      integer isphionxy ( 0:nx+1,0:ny+1)
      pointer(pisphionxy,isphionxy)

      integer isnioffxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisnioffxy,isnioffxy)

      integer isupoffxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pisupoffxy,isupoffxy)

      integer isteoffxy ( 0:nx+1,0:ny+1)
      pointer(pisteoffxy,isteoffxy)

      integer istioffxy ( 0:nx+1,0:ny+1)
      pointer(pistioffxy,istioffxy)

      integer isngoffxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pisngoffxy,isngoffxy)

      integer istgoffxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pistgoffxy,istgoffxy)

      integer isphioffxy ( 0:nx+1,0:ny+1)
      pointer(pisphioffxy,isphioffxy)

      double precision fdtnixy ( 0:nx+1,0:ny+1,nisp)
      pointer(pfdtnixy,fdtnixy)

      double precision fdtupxy ( 0:nx+1,0:ny+1,nisp)
      pointer(pfdtupxy,fdtupxy)

      double precision fdttexy ( 0:nx+1,0:ny+1)
      pointer(pfdttexy,fdttexy)

      double precision fdttixy ( 0:nx+1,0:ny+1)
      pointer(pfdttixy,fdttixy)

      double precision fdtngxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pfdtngxy,fdtngxy)

      double precision fdttgxy ( 0:nx+1,0:ny+1,ngsp)
      pointer(pfdttgxy,fdttgxy)

      double precision fdtphixy ( 0:nx+1,0:ny+1)
      pointer(pfdtphixy,fdtphixy)
      common /bbb10000/ label
      common /bbb10001/ svrpkg
      common /bbb10002/ petscoptfile
      common /bbb10003/ petscopts
      common /bbb20/ methe, methu, methn, methi, methg, methp, isgxvon
      common /bbb20/ ishavisy, isintlog, concap, convis, icnuiz, icnucx
      common /bbb20/ isrecmon, igas, ingb, inflbg, inzb, iteb, is1D_gbx
      common /bbb20/ ixgb, ncrhs, istep, iter, ishymol, isfqpave, isgpye
      common /bbb20/ iigsp, itrap_negni, itrap_negt, itrap_negng
      common /bbb20/ isybdryog, isybdrywd, isxmpog, iexclnxc1, ineudif
      common /bbb20/ isbcwdt, ishosor, issyvxpt0, isrrvave, isdtsfscal
      common /bbb20/ isplflxl, isplflxlv, isplflxlgx, isplflxlgxy
      common /bbb20/ iswflxlgy, isplflxlvgx, isplflxlvgxy, iswflxlvgy
      common /bbb20/ isplflxltgx, isplflxltgxy, iswflxltgy, isfeexpl0
      common /bbb20/ isfeixpl0, isofric, iskaboom, isnglf, isngrf
      common /bbb20/ isnion, isupon, isup1up2, isupgon, isteon, istion
      common /bbb20/ isngon, istgon, isphion, isphiofft, isnewpot
      common /bbb20/ isugfm1side, isnupdot1sd, isphicore0
      common /bbb20/ is_z0_imp_const
      common /bbb23/ csfaclb, csfacrb, csfacti, cslim, dcslim, lnlam
      common /bbb23/ cfaccony, isvylog, cniatol, cngatol, cupatol
      common /bbb23/ cteatol, ctiatol, cphiatol, tolbf, tadj, cnuiz
      common /bbb23/ cnucx, cfrecom, ngbackg, cflbg, facngbackg2ngs
      common /bbb23/ nzbackg, facnzbackg2nis, upclng, facupclng2ups
      common /bbb23/ tebg, tibg, temin, temin2, pwrbkg_c, pwribkg_c
      common /bbb23/ cfwjdotelim, nlimix, nlimiy, nlimgx, nlimgy, xgbx
      common /bbb23/ agdc, pcolwid, eion, ediss, ebind, tfcx, tfcy, afix
      common /bbb23/ coef, ce, ci, dp1, qfl, csh, qsh, mfl, msh, ro, cs
      common /bbb23/ fxe, ctaue, fxi, ctaui, zcoef, coef1, cnurn, cnuru
      common /bbb23/ cnure, cnuri, cnurg, cnurp, nurlxn, nurlxu, nurlxe
      common /bbb23/ nurlxi, nurlxg, nurlxp, rnewpot, r0slab, te_s_dis
      common /bbb23/ fnnuiz, thetar, iseesorave, ispsorave, fsprd
      common /bbb23/ rr_fac, rrmin, frfqpn, cffqpsat, flalfipl, flalfepl
      common /bbb23/ del_te_ro, nglfix, ngrfix, rup21, z0_imp_const
      common /bbb26/ pisnionxy, pisuponxy, pisteonxy
      common /bbb26/ pistionxy, pisngonxy, pistgonxy
      common /bbb26/ pisphionxy, pisnioffxy
      common /bbb26/ pisupoffxy, pisteoffxy
      common /bbb26/ pistioffxy, pisngoffxy
      common /bbb26/ pistgoffxy, pisphioffxy, pfdtnixy
      common /bbb26/ pfdtupxy, pfdttexy, pfdttixy
      common /bbb26/ pfdtngxy, pfdttgxy, pfdtphixy
c End of UEpar
c itrap_negt,itrap_negng
c Group Aux
      integer ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3, ix4, ix5
      double precision tv, t0, t1, t2, a
      integer ix6, ixmp
      common /bbb100/ ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3
      common /bbb100/ ix4, ix5, ix6, ixmp
      common /bbb103/ tv, t0, t1, t2, a
c End of Aux
c ix,iy,igsp,ix1,ix2,t1,t2
c Group Selec
      integer i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2, j3, j4
      integer j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p, ixs1, ixf6, iys1
      integer iyf6, xlinc, xrinc, yinc, isjaccorall

      integer ixm1 ( 0:nx+1,0:ny+1)
      pointer(pixm1,ixm1)

      integer ixp1 ( 0:nx+1,0:ny+1)
      pointer(pixp1,ixp1)

      integer iym1a ( 0:nx+1,0:ny+1)
      pointer(piym1a,iym1a)

      integer iyp1a ( 0:nx+1,0:ny+1)
      pointer(piyp1a,iyp1a)

      double precision stretcx ( 0:nx+1,0:ny+1)
      pointer(pstretcx,stretcx)
      common /bbb90/ i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2
      common /bbb90/ j3, j4, j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p
      common /bbb90/ ixs1, ixf6, iys1, iyf6, xlinc, xrinc, yinc
      common /bbb90/ isjaccorall
      common /bbb96/ pixm1, pixp1, piym1a
      common /bbb96/ piyp1a, pstretcx
c End of Selec
c yinc,ixm1,ixp1
c Group Indexes

      integer idxn ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pidxn,idxn)

      integer idxg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pidxg,idxg)

      integer idxtg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pidxtg,idxtg)

      integer idxu ( 0:nx+1,0:ny+1,1:nusp)
      pointer(pidxu,idxu)

      integer idxti ( 0:nx+1,0:ny+1)
      pointer(pidxti,idxti)

      integer idxte ( 0:nx+1,0:ny+1)
      pointer(pidxte,idxte)

      integer idxphi ( 0:nx+1,0:ny+1)
      pointer(pidxphi,idxphi)

      integer ivfirst ( 0:nx+1,0:ny+1)
      pointer(pivfirst,ivfirst)

      integer igyl ( neqmx,2)
      pointer(pigyl,igyl)

      integer iseqalg ( neqmx)
      pointer(piseqalg,iseqalg)

      integer isvarup ( numvar)
      pointer(pisvarup,isvarup)

      integer isvarphi ( numvar)
      pointer(pisvarphi,isvarphi)
      common /bbb306/ pidxn, pidxg, pidxtg
      common /bbb306/ pidxu, pidxti, pidxte
      common /bbb306/ pidxphi, pivfirst, pigyl
      common /bbb306/ piseqalg, pisvarup, pisvarphi
c End of Indexes

c Group Comgeo
      double precision sygytotc, area_core, ghxpt, gvxpt, sxyxpt
      double precision ghxpt_lower, gvxpt_lower, sxyxpt_lower
      double precision ghxpt_upper, gvxpt_upper, sxyxpt_upper, linelen
      double precision dxmin

      double precision vol ( 0:nx+1,0:ny+1)
      pointer(pvol,vol)

      double precision gx ( 0:nx+1,0:ny+1)
      pointer(pgx,gx)

      double precision gy ( 0:nx+1,0:ny+1)
      pointer(pgy,gy)

      double precision dx ( 0:nx+1,0:ny+1)
      pointer(pdx,dx)

      double precision dxvf ( 0:nx+1,0:ny+1)
      pointer(pdxvf,dxvf)

      double precision dy ( 0:nx+1,0:ny+1)
      pointer(pdy,dy)

      double precision gxf ( 0:nx+1,0:ny+1)
      pointer(pgxf,gxf)

      double precision gxfn ( 0:nx+1,0:ny+1)
      pointer(pgxfn,gxfn)

      double precision gyf ( 0:nx+1,0:ny+1)
      pointer(pgyf,gyf)

      double precision gxc ( 0:nx+1,0:ny+1)
      pointer(pgxc,gxc)

      double precision gyc ( 0:nx+1,0:ny+1)
      pointer(pgyc,gyc)

      double precision xnrm ( 0:nx+1,0:ny+1)
      pointer(pxnrm,xnrm)

      double precision xvnrm ( 0:nx+1,0:ny+1)
      pointer(pxvnrm,xvnrm)

      double precision ynrm ( 0:nx+1,0:ny+1)
      pointer(pynrm,ynrm)

      double precision yvnrm ( 0:nx+1,0:ny+1)
      pointer(pyvnrm,yvnrm)

      double precision sx ( 0:nx+1,0:ny+1)
      pointer(psx,sx)

      double precision sxnp ( 0:nx+1,0:ny+1)
      pointer(psxnp,sxnp)

      double precision sy ( 0:nx+1,0:ny+1)
      pointer(psy,sy)

      double precision rr ( 0:nx+1,0:ny+1)
      pointer(prr,rr)

      double precision xcs ( 0:nx+1)
      pointer(pxcs,xcs)

      double precision xfs ( 0:nx+1)
      pointer(pxfs,xfs)

      double precision xcwi ( 0:nx+1)
      pointer(pxcwi,xcwi)

      double precision xfwi ( 0:nx+1)
      pointer(pxfwi,xfwi)

      double precision xfpf ( 0:nx+1)
      pointer(pxfpf,xfpf)

      double precision xcpf ( 0:nx+1)
      pointer(pxcpf,xcpf)

      double precision xcwo ( 0:nx+1)
      pointer(pxcwo,xcwo)

      double precision xfwo ( 0:nx+1)
      pointer(pxfwo,xfwo)

      double precision yyc ( 0:ny+1)
      pointer(pyyc,yyc)

      double precision yyf ( 0:ny+1)
      pointer(pyyf,yyf)

      double precision yylb ( 0:ny+1,1:nxpt)
      pointer(pyylb,yylb)

      double precision yyrb ( 0:ny+1,1:nxpt)
      pointer(pyyrb,yyrb)

      double precision xcv ( 0:nx+1)
      pointer(pxcv,xcv)

      double precision xfv ( 0:nx+1)
      pointer(pxfv,xfv)

      double precision psinormc ( 0:ny+1)
      pointer(ppsinormc,psinormc)

      double precision psinormf ( 0:ny+1)
      pointer(ppsinormf,psinormf)

      double precision rrv ( 0:nx+1,0:ny+1)
      pointer(prrv,rrv)

      double precision volv ( 0:nx+1,0:ny+1)
      pointer(pvolv,volv)

      double precision hxv ( 0:nx+1,0:ny+1)
      pointer(phxv,hxv)

      double precision syv ( 0:nx+1,0:ny+1)
      pointer(psyv,syv)

      integer isxptx ( 0:nx+1,0:ny+1)
      pointer(pisxptx,isxptx)

      integer isxpty ( 0:nx+1,0:ny+1)
      pointer(pisxpty,isxpty)

      double precision lcon ( 0:nx+1,0:ny+1)
      pointer(plcon,lcon)

      double precision lconi ( 0:nx+1,0:ny+1)
      pointer(plconi,lconi)

      double precision lcone ( 0:nx+1,0:ny+1)
      pointer(plcone,lcone)

      double precision lconneo ( 0:nx+1,0:ny+1)
      pointer(plconneo,lconneo)

      double precision epsneo ( 0:nx+1,0:ny+1)
      pointer(pepsneo,epsneo)

      integer isixcore ( 0:nx+1)
      pointer(pisixcore,isixcore)
      common /com113/ sygytotc, area_core, ghxpt, gvxpt, sxyxpt
      common /com113/ ghxpt_lower, gvxpt_lower, sxyxpt_lower
      common /com113/ ghxpt_upper, gvxpt_upper, sxyxpt_upper, linelen
      common /com113/ dxmin
      common /com116/ pvol, pgx, pgy, pdx
      common /com116/ pdxvf, pdy, pgxf, pgxfn
      common /com116/ pgyf, pgxc, pgyc, pxnrm
      common /com116/ pxvnrm, pynrm, pyvnrm, psx
      common /com116/ psxnp, psy, prr, pxcs
      common /com116/ pxfs, pxcwi, pxfwi, pxfpf
      common /com116/ pxcpf, pxcwo, pxfwo, pyyc
      common /com116/ pyyf, pyylb, pyyrb, pxcv
      common /com116/ pxfv, ppsinormc, ppsinormf
      common /com116/ prrv, pvolv, phxv, psyv
      common /com116/ pisxptx, pisxpty, plcon
      common /com116/ plconi, plcone, plconneo
      common /com116/ pepsneo, pisixcore
c End of Comgeo
c xcs, yyc
c Group Noggeo

      double precision vtag ( 0:nx+1,0:ny+1)
      pointer(pvtag,vtag)

      double precision angfx ( 0:nx+1,0:ny+1)
      pointer(pangfx,angfx)

      double precision fxm ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxm,fxm)

      double precision fx0 ( 0:nx+1,0:ny+1,0:1)
      pointer(pfx0,fx0)

      double precision fxp ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxp,fxp)

      double precision fym ( 0:nx+1,0:ny+1,0:1)
      pointer(pfym,fym)

      double precision fy0 ( 0:nx+1,0:ny+1,0:1)
      pointer(pfy0,fy0)

      double precision fyp ( 0:nx+1,0:ny+1,0:1)
      pointer(pfyp,fyp)

      double precision fxmy ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmy,fxmy)

      double precision fxpy ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpy,fxpy)

      double precision fymx ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymx,fymx)

      double precision fypx ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypx,fypx)

      double precision fxmv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmv,fxmv)

      double precision fx0v ( 0:nx+1,0:ny+1,0:1)
      pointer(pfx0v,fx0v)

      double precision fxpv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpv,fxpv)

      double precision fymv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymv,fymv)

      double precision fy0v ( 0:nx+1,0:ny+1,0:1)
      pointer(pfy0v,fy0v)

      double precision fypv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypv,fypv)

      double precision fxmyv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmyv,fxmyv)

      double precision fxpyv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpyv,fxpyv)

      double precision fymxv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymxv,fymxv)

      double precision fypxv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypxv,fypxv)
      common /com136/ pvtag, pangfx, pfxm, pfx0
      common /com136/ pfxp, pfym, pfy0, pfyp
      common /com136/ pfxmy, pfxpy, pfymx, pfypx
      common /com136/ pfxmv, pfx0v, pfxpv, pfymv
      common /com136/ pfy0v, pfypv, pfxmyv
      common /com136/ pfxpyv, pfymxv, pfypxv
c End of Noggeo
c fxm,fx0,fxp,fxmy,fxpy
c Group Gradients
      double precision einduc

      double precision ex ( 0:nx+1,0:ny+1)
      pointer(pex,ex)

      double precision ey ( 0:nx+1,0:ny+1)
      pointer(pey,ey)

      double precision gpix ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pgpix,gpix)

      double precision gpiy ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pgpiy,gpiy)

      double precision gpex ( 0:nx+1,0:ny+1)
      pointer(pgpex,gpex)

      double precision gpey ( 0:nx+1,0:ny+1)
      pointer(pgpey,gpey)

      double precision gprx ( 0:nx+1,0:ny+1)
      pointer(pgprx,gprx)

      double precision gpry ( 0:nx+1,0:ny+1)
      pointer(pgpry,gpry)

      double precision gtex ( 0:nx+1,0:ny+1)
      pointer(pgtex,gtex)

      double precision gtey ( 0:nx+1,0:ny+1)
      pointer(pgtey,gtey)

      double precision gtix ( 0:nx+1,0:ny+1)
      pointer(pgtix,gtix)

      double precision gtiy ( 0:nx+1,0:ny+1)
      pointer(pgtiy,gtiy)
      common /bbb333/ einduc
      common /bbb336/ pex, pey, pgpix, pgpiy
      common /bbb336/ pgpex, pgpey, pgprx, pgpry
      common /bbb336/ pgtex, pgtey, pgtix, pgtiy
c End of Gradients

c Group Phyvar
      double precision pi, me, mp, ev, qe, mu0, eps0, rt8opi
      common /bbb173/ pi, me, mp, ev, qe, mu0, eps0, rt8opi
c End of Phyvar
c pi,ev
c Group Coefeq
      double precision cnfx, cnfy, cnsor, cfneut, cfnidh, cfupcx, cfticx
      double precision cfupimpg, cftiimpg, cmneut, cnflux(6)
      double precision chradi, chradr, chioniz, cne_sgvi, ctsor, ceisor
      double precision ccoldsor, cngfx(6), cngfy(6)
      double precision cngmom(31), cmwall(31), cngtgx(6)
      double precision cngtgy(6), sxgsol, sxgpr, xstscal
      double precision rld2dxg(6), rld2dyg(6), cngflox(6)
      double precision cngfloy(6), cngniflox(31,6)
      double precision cngnifloy(31,6), cngsor, cdifg(6)
      double precision lgmax(6), lgtmax(6), lgvmax
      double precision rtg2ti(6), tgas(6), cmfx, cmfy, cpgx
      double precision cfvisx, cfvisy, cfanomvisxg, cfanomvisyg, cfvisxn
      double precision cfvisxy(1:31), cfvxnrr, cfvisyn
      double precision cfvcsx(1:31), cfvcsy(1:31), vboost, cvgp
      double precision cfvgpx(1:31), cfvgpy(1:31), cfbgt, cfjhf
      double precision cf2ef, cfyef, cftef, cf2bf, cfybf, cfcbti, cfcurv
      double precision cfgradb, cfq2bf, cfqybf, cfqyn, cfqym, cfqydt
      double precision cf2dd, cfydd, cftdd, cfrd, cfvisxneov, cfvisxneoq
      double precision cfvycr, cfvycf, cfvyavis, cfjve, cfjp2, cfjpy
      double precision cfnfmiy, cnimp, fac2sp, cftnm, cfupjr, cfcximp1
      double precision cfcximp2, cfnetap, fcdif, cfmsor, cpiup(31)
      double precision cfloyi, cfloye, cfcvte, cfcvti, cfcvtg, cfloxiplt
      double precision cfloygwall, cftgdiss(6), exjbdry, cfgpijr
      double precision zeffcon, alftng, cfqya, cfqyao, cfqyae, cfqyai
      double precision cfhcxgc(6), cfhcygc(6), cftgcond
      double precision cftgeqp
      integer ifxnsgi, isvisxn_old, jhswitch, isnfmiy, iszeffcon
      common /bbb40/ ifxnsgi, isvisxn_old, jhswitch, isnfmiy, iszeffcon
      common /bbb43/ cnfx, cnfy, cnsor, cfneut, cfnidh, cfupcx, cfticx
      common /bbb43/ cfupimpg, cftiimpg, cmneut, cnflux, chradi, chradr
      common /bbb43/ chioniz, cne_sgvi, ctsor, ceisor, ccoldsor, cngfx
      common /bbb43/ cngfy, cngmom, cmwall, cngtgx, cngtgy, sxgsol
      common /bbb43/ sxgpr, xstscal, rld2dxg, rld2dyg, cngflox, cngfloy
      common /bbb43/ cngniflox, cngnifloy, cngsor, cdifg, lgmax, lgtmax
      common /bbb43/ lgvmax, rtg2ti, tgas, cmfx, cmfy, cpgx, cfvisx
      common /bbb43/ cfvisy, cfanomvisxg, cfanomvisyg, cfvisxn, cfvisxy
      common /bbb43/ cfvxnrr, cfvisyn, cfvcsx, cfvcsy, vboost, cvgp
      common /bbb43/ cfvgpx, cfvgpy, cfbgt, cfjhf, cf2ef, cfyef, cftef
      common /bbb43/ cf2bf, cfybf, cfcbti, cfcurv, cfgradb, cfq2bf
      common /bbb43/ cfqybf, cfqyn, cfqym, cfqydt, cf2dd, cfydd, cftdd
      common /bbb43/ cfrd, cfvisxneov, cfvisxneoq, cfvycr, cfvycf
      common /bbb43/ cfvyavis, cfjve, cfjp2, cfjpy, cfnfmiy, cnimp
      common /bbb43/ fac2sp, cftnm, cfupjr, cfcximp1, cfcximp2, cfnetap
      common /bbb43/ fcdif, cfmsor, cpiup, cfloyi, cfloye, cfcvte
      common /bbb43/ cfcvti, cfcvtg, cfloxiplt, cfloygwall, cftgdiss
      common /bbb43/ exjbdry, cfgpijr, zeffcon, alftng, cfqya, cfqyao
      common /bbb43/ cfqyae, cfqyai, cfhcxgc, cfhcygc, cftgcond, cftgeqp
c End of Coefeq
c cngtgx
c Group Imprad
      integer isimpon, nusp_imp, isupimpap, ismctab

      double precision nzloc ( 0:nzspmx)
      pointer(pnzloc,nzloc)

      double precision impradloc ( 0:nzspmx)
      pointer(pimpradloc,impradloc)

      double precision pwrzec ( 0:nx+1,0:ny+1)
      pointer(ppwrzec,pwrzec)

      double precision pwrze ( 0:nx+1,0:ny+1)
      pointer(ppwrze,pwrze)

      double precision pradc ( 0:nx+1,0:ny+1)
      pointer(ppradc,pradc)

      double precision pradcff ( 0:nx+1,0:ny+1)
      pointer(ppradcff,pradcff)

      double precision prad ( 0:nx+1,0:ny+1)
      pointer(pprad,prad)

      double precision pradzc ( 0:nx+1,0:ny+1,0:nzspmx,1:ngsp-1)
      pointer(ppradzc,pradzc)

      double precision pradz ( 0:nx+1,0:ny+1,0:nzspmx,1:ngsp-1)
      pointer(ppradz,pradz)

      double precision na ( 0:nx+1,0:ny+1)
      pointer(pna,na)

      double precision ntau ( 0:nx+1,0:ny+1)
      pointer(pntau,ntau)

      double precision nratio ( 0:nx+1,0:ny+1)
      pointer(pnratio,nratio)

      double precision afrac ( 0:nx+1,0:ny+1)
      pointer(pafrac,afrac)

      double precision atau ( 0:nx+1,0:ny+1)
      pointer(patau,atau)

      double precision tau1 ( 0:nx+1,0:ny+1)
      pointer(ptau1,tau1)

      double precision tau2 ( 0:nx+1,0:ny+1)
      pointer(ptau2,tau2)
      common /bbb740/ isimpon, nusp_imp, isupimpap, ismctab
      common /bbb746/ pnzloc, pimpradloc, ppwrzec
      common /bbb746/ ppwrze, ppradc, ppradcff
      common /bbb746/ pprad, ppradzc, ppradz
      common /bbb746/ pna, pntau, pnratio
      common /bbb746/ pafrac, patau, ptau1
      common /bbb746/ ptau2
c End of Imprad
c isimpon
c Group Interp
      character*64 uedge_savefile
      integer isnintp, isimesh, isumesh2, nxold, nyold, nxoldg, nyoldg
      integer iysptrxo, ixst(1:6), ixsto(1:6), ixend(1:6), ixendo(1:6)

      integer ixlbo ( 1:nxpt)
      pointer(pixlbo,ixlbo)

      integer ixpt1o ( 1:nxpt)
      pointer(pixpt1o,ixpt1o)

      integer ixpt2o ( 1:nxpt)
      pointer(pixpt2o,ixpt2o)

      integer ixrbo ( 1:nxpt)
      pointer(pixrbo,ixrbo)

      double precision xnrmo ( 0:nxold+1,0:nyold+1)
      pointer(pxnrmo,xnrmo)

      double precision xvnrmo ( 0:nxold+1,0:nyold+1)
      pointer(pxvnrmo,xvnrmo)

      double precision xnrmox ( 0:nxold+1,0:ny+1)
      pointer(pxnrmox,xnrmox)

      double precision xvnrmox ( 0:nxold+1,0:ny+1)
      pointer(pxvnrmox,xvnrmox)

      double precision xnrmnx ( 0:nx+1,0:ny+1)
      pointer(pxnrmnx,xnrmnx)

      double precision xvnrmnx ( 0:nx+1,0:ny+1)
      pointer(pxvnrmnx,xvnrmnx)

      double precision ynrmo ( 0:nxold+1,0:nyold+1)
      pointer(pynrmo,ynrmo)

      double precision yvnrmo ( 0:nxold+1,0:nyold+1)
      pointer(pyvnrmo,yvnrmo)

      double precision ynrmox ( 0:nxold+1,0:ny+1)
      pointer(pynrmox,ynrmox)

      double precision yvnrmox ( 0:nxold+1,0:ny+1)
      pointer(pyvnrmox,yvnrmox)

      double precision ynrmnx ( 0:nx+1,0:ny+1)
      pointer(pynrmnx,ynrmnx)

      double precision yvnrmnx ( 0:nx+1,0:ny+1)
      pointer(pyvnrmnx,yvnrmnx)

      double precision wrkint ( 0:nxold+1,0:ny+1)
      pointer(pwrkint,wrkint)

      double precision wrkint2 ( 0:nx+1,0:ny+1)
      pointer(pwrkint2,wrkint2)

      integer ixmg ( 0:nxold+1,0:ny+1)
      pointer(pixmg,ixmg)

      integer iyomg ( 0:nxold+1,0:ny+1)
      pointer(piyomg,iyomg)

      integer ixvmg ( 0:nxold+1,0:ny+1)
      pointer(pixvmg,ixvmg)

      integer iyvomg ( 0:nxold+1,0:ny+1)
      pointer(piyvomg,iyvomg)

      integer ix2g ( 0:nx+1,0:ny+1)
      pointer(pix2g,ix2g)

      integer iy2g ( 0:nx+1,0:ny+1)
      pointer(piy2g,iy2g)

      integer ixv2g ( 0:nx+1,0:ny+1)
      pointer(pixv2g,ixv2g)

      integer iyv2g ( 0:nx+1,0:ny+1)
      pointer(piyv2g,iyv2g)

      double precision nis ( 0:nxold+1,0:nyold+1,1:nisp)
      pointer(pnis,nis)

      double precision tes ( 0:nxold+1,0:nyold+1)
      pointer(ptes,tes)

      double precision tis ( 0:nxold+1,0:nyold+1)
      pointer(ptis,tis)

      double precision tgs ( 0:nxold+1,0:nyold+1,1:ngsp)
      pointer(ptgs,tgs)

      double precision phis ( 0:nxold+1,0:nyold+1)
      pointer(pphis,phis)

      double precision ups ( 0:nxold+1,0:nyold+1,1:nisp)
      pointer(pups,ups)

      double precision ngs ( 0:nxold+1,0:nyold+1,1:ngsp)
      pointer(pngs,ngs)

      double precision afracs ( 0:nxold+1,0:nyold+1)
      pointer(pafracs,afracs)
      common /bbb10053/ uedge_savefile
      common /bbb600/ isnintp, isimesh, isumesh2, nxold, nyold, nxoldg
      common /bbb600/ nyoldg, iysptrxo, ixst, ixsto, ixend, ixendo
      common /bbb606/ pixlbo, pixpt1o, pixpt2o
      common /bbb606/ pixrbo, pxnrmo, pxvnrmo
      common /bbb606/ pxnrmox, pxvnrmox, pxnrmnx
      common /bbb606/ pxvnrmnx, pynrmo, pyvnrmo
      common /bbb606/ pynrmox, pyvnrmox, pynrmnx
      common /bbb606/ pyvnrmnx, pwrkint, pwrkint2
      common /bbb606/ pixmg, piyomg, pixvmg
      common /bbb606/ piyvomg, pix2g, piy2g
      common /bbb606/ pixv2g, piyv2g, pnis, ptes
      common /bbb606/ ptis, ptgs, pphis, pups
      common /bbb606/ pngs, pafracs
c End of Interp
c nis,tis,phis,nxold,nyold
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
c nysol,nyomitmx
c Group RZ_grid_info

      double precision rm ( 0:nxm+1,0:nym+1,0:4)
      pointer(prm,rm)

      double precision zm ( 0:nxm+1,0:nym+1,0:4)
      pointer(pzm,zm)

      double precision rmt ( 0:nxm+1,0:nym+1,0:4)
      pointer(prmt,rmt)

      double precision zmt ( 0:nxm+1,0:nym+1,0:4)
      pointer(pzmt,zmt)

      double precision rv ( 0:nxm+2,-1:nym+1)
      pointer(prv,rv)

      double precision zv ( 0:nxm+2,-1:nym+1)
      pointer(pzv,zv)

      double precision psi ( 0:nxm+1,0:nym+1,0:4)
      pointer(ppsi,psi)

      double precision br ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbr,br)

      double precision bz ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbz,bz)

      double precision bpol ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbpol,bpol)

      double precision bphi ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbphi,bphi)

      double precision b ( 0:nxm+1,0:nym+1,0:4)
      pointer(pb,b)

      double precision bsqr ( 0:nxm+1,0:nym+1)
      pointer(pbsqr,bsqr)

      double precision b12 ( 0:nxm+1,0:nym+1)
      pointer(pb12,b12)

      double precision b12ctr ( 0:nxm+1,0:nym+1)
      pointer(pb12ctr,b12ctr)

      double precision b32 ( 0:nxm+1,0:nym+1)
      pointer(pb32,b32)
      common /com66/ prm, pzm, prmt, pzmt
      common /com66/ prv, pzv, ppsi, pbr
      common /com66/ pbz, pbpol, pbphi, pb
      common /com66/ pbsqr, pb12, pb12ctr, pb32
c End of RZ_grid_info
c rm,zm

c  -- procedures --
      doubleprecision interpte,interpti,interpphi,interpni,interppri,
     &   interpng, interpnis,interptis,interpphis,interppg,interptg
c                               # interpolate 2-D array with a 5-point stencil
      interpte(ix,iy,k) = fxm (ix,iy,k)*te(ixm1(ix,iy+k) ,iy+k ) + fx0 (
     &   ix,iy,k)*te(ix ,iy+k ) + fxp (ix,iy,k)*te(ixp1(ix,iy+k) ,iy+k ) 
     &   + fxmy(ix,iy,k)*te(ixm1(ix,iy+1-k),iy+1-k) + fxpy(ix,iy,k)*te(
     &   ixp1(ix,iy+1-k),iy+1-k)
      interpti(ix,iy,k) = fxm (ix,iy,k)*ti(ixm1(ix,iy+k) ,iy+k ) + fx0 (
     &   ix,iy,k)*ti(ix ,iy+k ) + fxp (ix,iy,k)*ti(ixp1(ix,iy+k) ,iy+k ) 
     &   + fxmy(ix,iy,k)*ti(ixm1(ix,iy+1-k),iy+1-k) + fxpy(ix,iy,k)*ti(
     &   ixp1(ix,iy+1-k),iy+1-k)
      interptis(ix,iy,k)=fxm (ix,iy,k)*tis(ixm1(ix,iy+k) ,iy+k ) + fx0 (
     &   ix,iy,k)*tis(ix ,iy+k ) + fxp (ix,iy,k)*tis(ixp1(ix,iy+k) ,iy+k 
     &   ) + fxmy(ix,iy,k)*tis(ixm1(ix,iy+1-k),iy+1-k) + fxpy(ix,iy,k)*
     &   tis(ixp1(ix,iy+1-k),iy+1-k)
      interptg(ix,iy,k,l) = ( fxm (ix,iy,k)*tg(ixm1(ix,iy+k) ,iy+k ,l) + 
     &   fx0 (ix,iy,k)*tg(ix ,iy+k ,l) + fxp (ix,iy,k)*tg(ixp1(ix,iy+k) 
     &   ,iy+k ,l) + fxmy(ix,iy,k)*tg(ixm1(ix,iy+1-k),iy+1-k,l) + fxpy(
     &   ix,iy,k)*tg(ixp1(ix,iy+1-k),iy+1-k,l) )
      interpphi(ix,iy,k)= fxm (ix,iy,k)*phi(ixm1(ix,iy+k) ,iy+k ) + fx0 
     &   (ix,iy,k)*phi(ix ,iy+k ) + fxp (ix,iy,k)*phi(ixp1(ix,iy+k) ,iy+
     &   k ) + fxmy(ix,iy,k)*phi(ixm1(ix,iy+1-k),iy+1-k) + fxpy(ix,iy,k)
     &   *phi(ixp1(ix,iy+1-k),iy+1-k)
      interpphis(ix,iy,k)=fxm (ix,iy,k)*phis(ixm1(ix,iy+k) ,iy+k ) + fx0 
     &   (ix,iy,k)*phis(ix ,iy+k ) + fxp (ix,iy,k)*phis(ixp1(ix,iy+k) ,
     &   iy+k ) + fxmy(ix,iy,k)*phis(ixm1(ix,iy+1-k),iy+1-k) + fxpy(ix,
     &   iy,k)*phis(ixp1(ix,iy+1-k),iy+1-k)
      interpni(ix,iy,k,l) = exp ( fxm (ix,iy,k)*log(ni(ixm1(ix,iy+k) ,iy
     &   +k ,l)) + fx0 (ix,iy,k)*log(ni(ix ,iy+k ,l)) + fxp (ix,iy,k)*
     &   log(ni(ixp1(ix,iy+k) ,iy+k ,l)) + fxmy(ix,iy,k)*log(ni(ixm1(ix,
     &   iy+1-k),iy+1-k,l)) + fxpy(ix,iy,k)*log(ni(ixp1(ix,iy+1-k),iy+1-
     &   k,l)) )
      interpnis(ix,iy,k,l) = exp ( fxm (ix,iy,k)*log(nis(ixm1(ix,iy+k) ,
     &   iy+k ,l)) + fx0 (ix,iy,k)*log(nis(ix ,iy+k ,l)) + fxp (ix,iy,k)
     &   *log(nis(ixp1(ix,iy+k) ,iy+k ,l)) + fxmy(ix,iy,k)*log(nis(ixm1(
     &   ix,iy+1-k),iy+1-k,l)) + fxpy(ix,iy,k)*log(nis(ixp1(ix,iy+1-k),
     &   iy+1-k,l)) )
      interppri(ix,iy,k,l) = exp ( fxm (ix,iy,k)*log(pri(ixm1(ix,iy+k) ,
     &   iy+k ,l)) + fx0 (ix,iy,k)*log(pri(ix ,iy+k ,l)) + fxp (ix,iy,k)
     &   *log(pri(ixp1(ix,iy+k) ,iy+k ,l)) + fxmy(ix,iy,k)*log(pri(ixm1(
     &   ix,iy+1-k),iy+1-k,l)) + fxpy(ix,iy,k)*log(pri(ixp1(ix,iy+1-k),
     &   iy+1-k,l)) )
      interpng(ix,iy,k,l) = exp ( fxm (ix,iy,k)*log(ng(ixm1(ix,iy+k) ,iy
     &   +k ,l)) + fx0 (ix,iy,k)*log(ng(ix ,iy+k ,l)) + fxp (ix,iy,k)*
     &   log(ng(ixp1(ix,iy+k) ,iy+k ,l)) + fxmy(ix,iy,k)*log(ng(ixm1(ix,
     &   iy+1-k),iy+1-k,l)) + fxpy(ix,iy,k)*log(ng(ixp1(ix,iy+1-k),iy+1-
     &   k,l)) )
      interppg(ix,iy,k,l) = exp ( fxm (ix,iy,k)*log(pg(ixm1(ix,iy+k) ,iy
     &   +k ,l)) + fx0 (ix,iy,k)*log(pg(ix ,iy+k ,l)) + fxp (ix,iy,k)*
     &   log(pg(ixp1(ix,iy+k) ,iy+k ,l)) + fxmy(ix,iy,k)*log(pg(ixm1(ix,
     &   iy+1-k),iy+1-k,l)) + fxpy(ix,iy,k)*log(pg(ixp1(ix,iy+1-k),iy+1-
     &   k,l)) )

      id = 1
      if (ixl .lt. 0 .or. yinc .ge. 6) then
         is = 0
         ie = nx+1
      else
         is = ixl
         ie = ixl
      endif

      if (iyl .lt. 0 .or. yinc .ge. 6) then
         js = 0
         je = ny+1
      else
         js = iyl
         je = iyl
      endif

      do 23000 iy = js, je
         do 23002 ix = is, ie
            pr(ix,iy) = 0.0d0
            zeff(ix,iy) = 0.0d0
23002    continue
23000 continue

      do 14 ifld = 1, nisp
         do 12 iy = js, je
            do 11 ix = is, ie
               pri(ix,iy,ifld) = ni(ix,iy,ifld) * ti(ix,iy)
               if (zi(ifld).ne.0.d0) then
                  pr(ix,iy) = pr(ix,iy) + pri(ix,iy,ifld)
                  zeff(ix,iy)=zeff(ix,iy)+zi(ifld)**2*ni(ix,iy,ifld)
               endif
   11          continue
   12       continue
   14    continue

c ... Replace values of ne calculated above by values consistent
c     with those of the INEL average-ion impurity model, if it is
c     being used.  Note that zi(2) passed to rnec will not be used.
      if (isimpon .eq. 3) then
         call xerrab("**** Ave-ion model with isimpon=3 disabled")
ccc         impflag = 1
ccc         do iy = js, je
ccc            do ix = is, ie
ccc               zimpc(ix,iy) = zimp(te(ix,iy))
ccc               ne(ix,iy) = rnec (ni(ix,iy,1), nzsp, ni(ix,iy,nhsp+1),
ccc     .                           te(ix,iy), zi(2), impflag,
ccc     .                           zimpc(ix,iy))
ccc            enddo
ccc         enddo
      endif

      do 16 iy = js, je
         do 15 ix = is, ie
            pre(ix,iy) = ne(ix,iy) * te(ix,iy)
            pr(ix,iy) = pr(ix,iy) + pre(ix,iy)
            zeff(ix,iy) = zeff(ix,iy) / ne(ix,iy)
            znot(ix,iy) = ne(ix,iy)*zeff(ix,iy)/ni(ix,iy,1) - 1
            do 23009 igsp = 1, ngsp
               if (istgcon(igsp) .gt. -1.d-20) tg(ix,iy,igsp) = (1-
     &               istgcon(igsp))*rtg2ti(igsp)*ti(ix,iy) + istgcon(
     &               igsp)*tgas(igsp)*ev
               pg(ix,iy,igsp) = ng(ix,iy,igsp)*tg(ix,iy,igsp)
23009       continue
   15       continue
   16    continue

c ... Set zeff=constant if iszeffcon=1
      if (iszeffcon .eq. 1) then
         do 23011 iy = js, je
            do 23013 ix = is, ie
               zeff(ix,iy) = zeffcon
23013       continue
23011    continue
      endif

cccc ... Replace values of zeff calculated above by values consistent
cccc     with those of the INEL average-ion impurity model, if it is
cccc     being used.  Note that zi(2) passed to zeffc will not be used.
ccc      if (isimpon .eq. 3) then
ccc         impflag = 1
ccc         do iy = js, je
ccc            do ix = is, ie
ccc               zeff(ix,iy) = zeffc (nzsp, ni(ix,iy,1), ni(ix,iy,nhsp+1),
ccc     .                              te(ix,iy), zi(2), impflag,
ccc     .                              zimpc(ix,iy))
ccc            enddo
ccc         enddo
ccc      endif

      do 18 iy = js, je
         inc = isign(max(1,iabs(ie-ixm1(ie,iy))),ie-ixm1(ie,iy))
         do 17 ix = ixm1(is,iy), min(nx,ie), inc
            gprx(ix,iy) = 0.0d0
   17       continue
   18    continue

c Tom:  add comments here to explain the indices used on do 20 and 19
      do 20 iy = max(js-1,0), min(ny,je)
         inc = isign(max(1,iabs(ie-ixm1(ie,js))),ie-ixm1(ie,js))
         do 19 ix = ixm1(is,js), min(nx,ie), inc
            ney0(ix,iy) = 0.0d0
            ney1(ix,iy) = 0.0d0
            nity0(ix,iy) = 0.0d0
            nity1(ix,iy) = 0.0d0
            gpry(ix,iy) = 0.0d0
   19       continue
         ix = ixp1(ie,iy)
         ney0(ix,iy) = 0.0d0
         ney1(ix,iy) = 0.0d0
         nity0(ix,iy) = 0.0d0
         nity1(ix,iy) = 0.0d0
         gpry(ix,iy) = 0.0d0
   20    continue

c Tom:  add comments here to explain the indices used on do 21
      do 23 ifld = 1, nisp
         do 22 iy = js, je
            inc = isign(max(1,iabs(ie-ixm1(ie,iy))),ie-ixm1(ie,iy))
            do 21 ix = ixm1(is,iy), min(nx,ie), inc
               ix1 = ixp1(ix,iy)
               gpix(ix,iy,ifld) = (pri(ix1,iy,ifld)-pri(ix,iy,ifld))*gxf
     &            (ix,iy)
               if (zi(ifld).ne.0.d0) gprx(ix,iy) = gprx(ix,iy) + gpix(ix
     &               ,iy,ifld)
   21          continue
   22       continue
c...  fix the corners for smooth vycd diamagnetic drifts
cc      gpix(0,0,ifld) = gpix(1,0,ifld)
cc      gpix(0,ny+1,ifld) = gpix(1,ny+1,ifld)
cc      gpix(nx+1,0,ifld) = gpix(nx,0,ifld)
cc      gpix(nx+1,ny+1,ifld) = gpix(nx,ny+1,ifld)
   23    continue

c Tom:  add comments here to explain the indices used on do 25 and 24
      do 26 ifld = 1, nisp
         do 25 iy = max(js-1,0), min(je,ny)
            inc = isign(max(1,iabs(ie-ixm1(ie,js))),ie-ixm1(ie,js))
            do 24 ix = ixm1(is,js), min(nx,ie), inc
               niy0(ix,iy,ifld) = interpni(ix,iy,0,ifld)
               niy1(ix,iy,ifld) = interpni(ix,iy,1,ifld)
               if (nx.eq.nxold .and. ny.eq.nyold .and. nis(1,1,1).ne.
     &            0.d0) then
                  niy0s(ix,iy,ifld) = interpnis(ix,iy,0,ifld)
                  niy1s(ix,iy,ifld) = interpnis(ix,iy,1,ifld)
               endif
               nity0(ix,iy) = nity0(ix,iy) + niy0(ix,iy,ifld)
               nity1(ix,iy) = nity1(ix,iy) + niy1(ix,iy,ifld)
               ney0(ix,iy) = ney0(ix,iy) + zi(ifld)*niy0(ix,iy,ifld)
               ney1(ix,iy) = ney1(ix,iy) + zi(ifld)*niy1(ix,iy,ifld)
               priy0(ix,iy,ifld) = interppri(ix,iy,0,ifld)
               priy1(ix,iy,ifld) = interppri(ix,iy,1,ifld)
               gpiy(ix,iy,ifld) = (priy1(ix,iy,ifld) - priy0(ix,iy,ifld)
     &            ) * gyf(ix,iy)
               if (zi(ifld).ne.0.d0) gpry(ix,iy) = gpry(ix,iy) + gpiy(ix
     &               ,iy,ifld)
   24          continue
            ix = ixp1(ie,iy)
            niy0(ix,iy,ifld) = interpni(ix,iy,0,ifld)
            niy1(ix,iy,ifld) = interpni(ix,iy,1,ifld)
            if (nx.eq.nxold .and. ny.eq.nyold .and. nis(1,1,1).ne.0.d0) 
     &            then
               niy0s(ix,iy,ifld) = interpnis(ix,iy,0,ifld)
               niy1s(ix,iy,ifld) = interpnis(ix,iy,1,ifld)
            endif
            nity0(ix,iy) = nity0(ix,iy) + niy0(ix,iy,ifld)
            nity1(ix,iy) = nity1(ix,iy) + niy1(ix,iy,ifld)
            ney0(ix,iy) = ney0(ix,iy) + zi(ifld)*niy0(ix,iy,ifld)
            ney1(ix,iy) = ney1(ix,iy) + zi(ifld)*niy1(ix,iy,ifld)
            priy0(ix,iy,ifld) = interppri(ix,iy,0,ifld)
            priy1(ix,iy,ifld) = interppri(ix,iy,1,ifld)
            gpiy(ix,iy,ifld) = (priy1(ix,iy,ifld) - priy0(ix,iy,ifld)) * 
     &         gyf(ix,iy)
            if (zi(ifld).ne.0.d0) gpry(ix,iy) = gpry(ix,iy) + gpiy(ix,iy
     &            ,ifld)
   25       continue
   26    continue

c Tom:  add comments here to explain the indices used on do 264 and 263
      do 264 iy = max(0,js-1), min(je,ny)
         inc = isign(max(1,iabs(ie-ixm1(ie,js))),ie-ixm1(ie,js))
         do 263 ix = ixm1(is,js), min(nx,ie), inc
            tey0(ix,iy) = interpte(ix,iy,0)
            tey1(ix,iy) = interpte(ix,iy,1)
            tiy0(ix,iy) = interpti(ix,iy,0)
            tiy1(ix,iy) = interpti(ix,iy,1)
            phiy0(ix,iy) =interpphi(ix,iy,0)
            phiy1(ix,iy) =interpphi(ix,iy,1)
            if (nx.eq.nxold .and. ny.eq.nyold) then
               tiy0s(ix,iy) =interptis(ix,iy,0)
               tiy1s(ix,iy) =interptis(ix,iy,1)
               phiy0s(ix,iy) =interpphis(ix,iy,0)
               phiy1s(ix,iy) =interpphis(ix,iy,1)
            endif
  263       continue
         ix = ixp1(ie,iy)
         tey0(ix,iy) = interpte(ix,iy,0)
         tey1(ix,iy) = interpte(ix,iy,1)
         tiy0(ix,iy) = interpti(ix,iy,0)
         tiy1(ix,iy) = interpti(ix,iy,1)
         phiy0(ix,iy) =interpphi(ix,iy,0)
         phiy1(ix,iy) =interpphi(ix,iy,1)
         if (nx.eq.nxold .and. ny.eq.nyold) then
            tiy0s(ix,iy) = interptis(ix,iy,0)
            tiy1s(ix,iy) = interptis(ix,iy,1)
            phiy0s(ix,iy) =interpphis(ix,iy,0)
            phiy1s(ix,iy) =interpphis(ix,iy,1)
         endif
  264    continue

c Tom:  add comments here to explain the indices used on do 266 and 265
      do 267 igsp = 1, ngsp
         do 266 iy = max(js-1,0), min(je,ny)
            inc = isign(max(1,iabs(ie-ixm1(ie,js))),ie-ixm1(ie,js))
            do 265 ix = ixm1(is,js), min(nx,ie), inc
               ngy0(ix,iy,igsp) = interpng(ix,iy,0,igsp)
               ngy1(ix,iy,igsp) = interpng(ix,iy,1,igsp)
               tgy0(ix,iy,igsp) = interptg(ix,iy,0,igsp)
               tgy1(ix,iy,igsp) = interptg(ix,iy,1,igsp)
  265          continue
            ix = ixp1(ie,iy)
            ngy0(ix,iy,igsp) = interpng(ix,iy,0,igsp)
            ngy1(ix,iy,igsp) = interpng(ix,iy,1,igsp)
            tgy0(ix,iy,igsp) = interptg(ix,iy,0,igsp)
            tgy1(ix,iy,igsp) = interptg(ix,iy,1,igsp)
  266       continue
  267    continue

c ... Calculate pgy0,1 only if ineudif=2, i.e. grad_pg option
      if (ineudif .eq. 2) then
         do 23030 igsp = 1, ngsp
            do 23032 iy = max(js-1,0), min(je,ny)
               inc = isign(max(1,iabs(ie-ixm1(ie,js))),ie-ixm1(ie,js))
               do 23034 ix = ixm1(is,js), min(nx,ie), inc
                  pgy0(ix,iy,igsp) = interppg(ix,iy,0,igsp)
                  pgy1(ix,iy,igsp) = interppg(ix,iy,1,igsp)
23034          continue
               ix = ixp1(ie,iy)
               pgy0(ix,iy,igsp) = interppg(ix,iy,0,igsp)
               pgy1(ix,iy,igsp) = interppg(ix,iy,1,igsp)
23032       continue
23030    continue
      endif

c inc index gives stride for jac perturb at cuts
      do 23036 iy = js, je
         inc = isign(max(1,iabs(ie-ixm1(ie,iy))),ie-ixm1(ie,iy))
         do 23038 ix = ixm1(is,iy), min(nx,ie), inc
            ix1 = ixp1(ix,iy)
            gpex(ix,iy) = (pre(ix1,iy)-pre(ix,iy))*gxf(ix,iy)
            gtex(ix,iy) = (te(ix1,iy)-te(ix,iy))*gxf(ix,iy)
            gtix(ix,iy) = (ti(ix1,iy)-ti(ix,iy))*gxf(ix,iy)
            gprx(ix,iy) = gprx(ix,iy) + gpex(ix,iy)
cccmer Replaced isphion->isphion+isphiofft below to correct Jacobian problem
            if (isphion+isphiofft .eq. 1) then
               ex(ix,iy) = (phi(ix,iy)-phi(ix1,iy))*gxf(ix,iy)
            endif
23038    continue
c#   reset ex(ixlb,), ex(ixrb,) to avoid using sheath phi(0,) & phi(nx+1,)
         if (iysptrx .lt. ny) then
c Otherwise this is core-only case w/o plates
            do 23040 jx = 1, nxpt
               ex(ixlb(jx),iy) = ex(ixlb(jx)+1,iy)
               ex(ixrb(jx),iy) = ex(ixrb(jx)-1,iy)
23040       continue
         endif
         if (islimon.ne.0 .and. iy.ge.iy_lims) then
c limiter like plate
            ex(ix_lim,iy) = 0.d0
            ex(ix_lim-1,iy) = ex(ix_lim-2,iy)
            ex(ix_lim+1,iy) = ex(ix_lim+2,iy)
         endif
23036 continue

c Tom:  add comments here to explain the indices used on do 30 and 29
      do 30 iy = max(js-1,0), min(ny,je)
         inc = isign(max(1,iabs(ie-ixm1(ie,js))),ie-ixm1(ie,js))
         do 29 ix = ixm1(is,js), min(nx,ie), inc
            gpey(ix,iy) = (ney1(ix,iy)*tey1(ix,iy) - ney0(ix,iy)*tey0(ix
     &         ,iy)) * gyf(ix,iy)
            gtey(ix,iy) = (tey1(ix,iy) - tey0(ix,iy)) * gyf(ix,iy)
            gtiy(ix,iy) = (tiy1(ix,iy) - tiy0(ix,iy)) * gyf(ix,iy)
            ey(ix,iy) = - (phiy1(ix,iy) - phiy0(ix,iy)) * gyf(ix,iy)
            gpry(ix,iy) = gpry(ix,iy) + gpey(ix,iy)
   29       continue
         ix = ixp1(ie,iy)
         gpey(ix,iy) = (ney1(ix,iy)*tey1(ix,iy) - ney0(ix,iy)*tey0(ix,iy
     &      )) * gyf(ix,iy)
         gtey(ix,iy) = (tey1(ix,iy) - tey0(ix,iy)) * gyf(ix,iy)
         gtiy(ix,iy) = (tiy1(ix,iy) - tiy0(ix,iy)) * gyf(ix,iy)
         ey(ix,iy) = - (phiy1(ix,iy) - phiy0(ix,iy)) * gyf(ix,iy)
         gpry(ix,iy) = gpry(ix,iy) + gpey(ix,iy)
   30    continue

c.... Define vertex values using linear interpolation

c,,,  Note that here we used ixm1(ix,iy) and not ixm1(ix,js) as above
c...  when the iy-loop starts at js-1; seems to work, but should check

      do 32 iy = max(0,js-1), min(ny,je)
         inc = isign(max(1,iabs(ie-ixm1(ie,iy))),ie-ixm1(ie,iy))
         do 31 ix = ixm1(is,iy), min(nx,ie), inc
            ix1 = ixp1(ix,iy)
            ix2 = ixp1(ix,iy+1)
            phiv(ix,iy) = 0.25d0*( phi(ix,iy) + phi(ix1,iy) + phi(ix,iy+
     &         1) + phi(ix2,iy+1) )
            tiv(ix,iy) = 0.25d0*( ti(ix,iy) + ti(ix1,iy) + ti(ix,iy+1) + 
     &         ti(ix2,iy+1) )
            tev(ix,iy) = 0.25d0*( te(ix,iy) + te(ix1,iy) + te(ix,iy+1) + 
     &         te(ix2,iy+1) )
c...  add electron contribution to prtv; ion contribution added below
            prev(ix,iy) = 0.25d0*( pre(ix,iy) + pre(ix1,iy) + pre(ix,iy+
     &         1) + pre(ix2,iy+1) )

            prtv(ix,iy) = prev(ix,iy)
   31       continue
   32    continue

      do 40 ifld = 1, nisp
         do 39 iy = max(0,js-1), min(ny,je)
            inc = isign(max(1,iabs(ie-ixm1(ie,iy))),ie-ixm1(ie,iy))
            do 38 ix = ixm1(is,iy), min(nx,ie), inc
               ix1 = ixp1(ix,iy)
               ix2 = ixp1(ix,iy+1)
               priv(ix,iy,ifld) = 0.25d0*( pri(ix,iy,ifld) + pri(ix1,iy,
     &            ifld) + pri(ix,iy+1,ifld) + pri(ix2,iy+1,ifld) )
               if (zi(ifld).ne.0.d0) prtv(ix,iy) = prtv(ix,iy) + priv(ix
     &               ,iy,ifld)

   38          continue
   39       continue
   40    continue

c.... reset the x-point value(s) all the time as it is easier and perhaps
c.... cheaper than checking

      if (nyomitmx .lt. nysol(1)+nyout(1)) then
c otherwise core only - skip

c loop over mesh regions
         do 23049 jx = 1, nxpt
            is = ixpt1(jx)
            js = iysptrx1(jx)
            if (jx.eq.1) then
c adjacent cells are in mesh region jx=nxpt
               ie = ixpt2(nxpt)
            else
c adjacent cells are in the previous mesh region
               ie = ixpt2(jx-1)
            endif
            if (is.lt.0 .or. ie.lt.0 .or. ie.gt.nx) goto 45
c ... Last test (ie.gt.nx) to fix parallel version with mpi - check
            phiv(is,js) = 0.125d0*( phi(is,js)+phi(is+1,js)+phi(is,js+1)
     &         +phi(is+1,js+1)+ phi(ie,js)+phi(ie+1,js)+phi(ie,js+1)+phi
     &         (ie+1,js+1) )
            phiv(ie,js) = phiv(is,js)
            tiv(is,js) = 0.125d0*( ti(is,js)+ti(is+1,js)+ti(is,js+1)+ti(
     &         is+1,js+1)+ ti(ie,js)+ti(ie+1,js)+ti(ie,js+1)+ti(ie+1,js+
     &         1) )
            tiv(ie,js) = tiv(is,js)
            tev(is,js) = 0.125d0*( te(is,js)+te(is+1,js)+te(is,js+1)+te(
     &         is+1,js+1)+ te(ie,js)+te(ie+1,js)+te(ie,js+1)+te(ie+1,js+
     &         1) )
            tev(ie,js) = tev(is,js)
            prev(is,js) = 0.125d0*( pre(is,js)+pre(is+1,js)+pre(is,js+1)
     &         +pre(is+1,js+1)+ pre(ie,js)+pre(ie+1,js)+pre(ie,js+1)+pre
     &         (ie+1,js+1) )
            prev(ie,js) = prev(is,js)
            prtv(is,js) = prev(is,js)

            do 43 ifld = 1, nisp
               priv(is,js,ifld) = 0.125d0*(pri(is,js ,ifld) + pri(is+1,
     &            js ,ifld) + pri(is,js+1,ifld) + pri(is+1,js+1,ifld) + 
     &            pri(ie,js ,ifld) + pri(ie+1,js ,ifld) + pri(ie,js+1,
     &            ifld) + pri(ie+1,js+1,ifld) )
               priv(ie,js,ifld) = priv(is,js,ifld)
               if (zi(ifld).ne.0.d0) prtv(is,js) = prtv(is,js) + priv(is
     &               ,js,ifld)
   43          continue
            prtv(ie,js) = prtv(is,js)
23049    continue
c end do-loop over nxpt mesh regions

      endif
c test on nyomit at top of do loop just above

   45 continue

      return
      end
c ***** end of subroutine convsr_aux ********
c ----------------------------------------------------------------------
c not used just now
      function intpnog (nxl,nyl,i,j,k,ary)
cProlog

c ... Interpolate a set of function values using the nonorthogonal stencil
c ... fxm, fx0, fxp, fxmy, fxpy

      implicit none

      doubleprecision intpnog
c i=ix,j=iy, and k=0/1 for lower/upper interp
      integer nxl,nyl,i,j,k
c array to be be interpolated
      doubleprecision ary(0:nxl,0:nyl)

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny
c Group Noggeo

      double precision vtag ( 0:nx+1,0:ny+1)
      pointer(pvtag,vtag)

      double precision angfx ( 0:nx+1,0:ny+1)
      pointer(pangfx,angfx)

      double precision fxm ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxm,fxm)

      double precision fx0 ( 0:nx+1,0:ny+1,0:1)
      pointer(pfx0,fx0)

      double precision fxp ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxp,fxp)

      double precision fym ( 0:nx+1,0:ny+1,0:1)
      pointer(pfym,fym)

      double precision fy0 ( 0:nx+1,0:ny+1,0:1)
      pointer(pfy0,fy0)

      double precision fyp ( 0:nx+1,0:ny+1,0:1)
      pointer(pfyp,fyp)

      double precision fxmy ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmy,fxmy)

      double precision fxpy ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpy,fxpy)

      double precision fymx ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymx,fymx)

      double precision fypx ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypx,fypx)

      double precision fxmv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmv,fxmv)

      double precision fx0v ( 0:nx+1,0:ny+1,0:1)
      pointer(pfx0v,fx0v)

      double precision fxpv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpv,fxpv)

      double precision fymv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymv,fymv)

      double precision fy0v ( 0:nx+1,0:ny+1,0:1)
      pointer(pfy0v,fy0v)

      double precision fypv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypv,fypv)

      double precision fxmyv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxmyv,fxmyv)

      double precision fxpyv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfxpyv,fxpyv)

      double precision fymxv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfymxv,fymxv)

      double precision fypxv ( 0:nx+1,0:ny+1,0:1)
      pointer(pfypxv,fypxv)
      common /com136/ pvtag, pangfx, pfxm, pfx0
      common /com136/ pfxp, pfym, pfy0, pfyp
      common /com136/ pfxmy, pfxpy, pfymx, pfypx
      common /com136/ pfxmv, pfx0v, pfxpv, pfymv
      common /com136/ pfy0v, pfypv, pfxmyv
      common /com136/ pfxpyv, pfymxv, pfypxv
c End of Noggeo
c fxm,fx0,fxp,fxmy,fxpy
c Group Selec
      integer i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2, j3, j4
      integer j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p, ixs1, ixf6, iys1
      integer iyf6, xlinc, xrinc, yinc, isjaccorall

      integer ixm1 ( 0:nx+1,0:ny+1)
      pointer(pixm1,ixm1)

      integer ixp1 ( 0:nx+1,0:ny+1)
      pointer(pixp1,ixp1)

      integer iym1a ( 0:nx+1,0:ny+1)
      pointer(piym1a,iym1a)

      integer iyp1a ( 0:nx+1,0:ny+1)
      pointer(piyp1a,iyp1a)

      double precision stretcx ( 0:nx+1,0:ny+1)
      pointer(pstretcx,stretcx)
      common /bbb90/ i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2
      common /bbb90/ j3, j4, j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p
      common /bbb90/ ixs1, ixf6, iys1, iyf6, xlinc, xrinc, yinc
      common /bbb90/ isjaccorall
      common /bbb96/ pixm1, pixp1, piym1a
      common /bbb96/ piyp1a, pstretcx
c End of Selec
c ixp1,ixm1

      intpnog = fxm (i,j,k)*ary(ixm1(i,j+k) ,j+k ) + fx0 (i,j,k)*ary(i ,
     &   j+k ) + fxp (i,j,k)*ary(ixp1(i,j+k) ,j+k ) + fxmy(i,j,k)*ary(
     &   ixm1(i,j+1-k),j+1-k) + fxpy(i,j,k)*ary(ixp1(i,j+1-k),j+1-k)

      return
      end
c ***** end of function intpnog **************
c ----------------------------------------------------------------------

      subroutine comp_vertex_vals
cProlog

c...  Calculates plasmas quantities at cell vertices as diagnostic
c...  Simple averages are used

      implicit none

c  -- local variables
      integer is,ie,js,je,jx,ifld

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nhsp,nzsp,nisp,nusp,ngsp
c Group Xpoint_indices
      integer iysptrx

      integer ixlb ( 1:nxpt)
      pointer(pixlb,ixlb)

      integer ixpt1 ( 1:nxpt)
      pointer(pixpt1,ixpt1)

      integer ixmdp ( 1:nxpt)
      pointer(pixmdp,ixmdp)

      integer ixpt2 ( 1:nxpt)
      pointer(pixpt2,ixpt2)

      integer ixrb ( 1:nxpt)
      pointer(pixrb,ixrb)

      integer iysptrx1 ( 1:nxpt)
      pointer(piysptrx1,iysptrx1)

      integer iysptrx2 ( 1:nxpt)
      pointer(piysptrx2,iysptrx2)
      common /com90/ iysptrx
      common /com96/ pixlb, pixpt1, pixmdp
      common /com96/ pixpt2, pixrb, piysptrx1
      common /com96/ piysptrx2
c End of Xpoint_indices
c ixpt1,ixpt2,iysptrx1
c Group Compla
      double precision facmg(1:31), istgcon(6), rtauxfac
      double precision rtauyfac, rt_scal, fracvgpgp

      double precision mi ( 1:nisp)
      pointer(pmi,mi)

      double precision zi ( 1:nisp)
      pointer(pzi,zi)

      double precision mg ( 1:ngsp)
      pointer(pmg,mg)

      integer znucl ( 1:nisp)
      pointer(pznucl,znucl)

      double precision ni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pni,ni)

      double precision lni ( 0:nx+1,0:ny+1,1:nisp)
      pointer(plni,lni)

      double precision nm ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnm,nm)

      double precision nz2 ( 0:nx+1,0:ny+1)
      pointer(pnz2,nz2)

      double precision uu ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puu,uu)

      double precision uup ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puup,uup)

      double precision up ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pup,up)

      double precision upi ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupi,upi)

      double precision upifmb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupifmb,upifmb)

      double precision uz ( 0:nx+1,0:ny+1,1:nisp)
      pointer(puz,uz)

      double precision v2 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2,v2)

      double precision v2xgp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2xgp,v2xgp)

      double precision v2ce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2ce,v2ce)

      double precision v2cb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cb,v2cb)

      double precision ve2cb ( 0:nx+1,0:ny+1)
      pointer(pve2cb,ve2cb)

      double precision v2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2cd,v2cd)

      double precision ve2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pve2cd,ve2cd)

      double precision q2cd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pq2cd,q2cd)

      double precision v2rd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2rd,v2rd)

      double precision v2dd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pv2dd,v2dd)

      double precision vy ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvy,vy)

      double precision vygp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvygp,vygp)

      double precision vytan ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvytan,vytan)

      double precision vygtan ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvygtan,vygtan)

      double precision vyce ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyce,vyce)

      double precision vycb ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycb,vycb)

      double precision veycb ( 0:nx+1,0:ny+1)
      pointer(pveycb,veycb)

      double precision vycp ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvycp,vycp)

      double precision veycp ( 0:nx+1,0:ny+1)
      pointer(pveycp,veycp)

      double precision vyrd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyrd,vyrd)

      double precision vydd ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvydd,vydd)

      double precision vyavis ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pvyavis,vyavis)

      double precision vex ( 0:nx+1,0:ny+1)
      pointer(pvex,vex)

      double precision upe ( 0:nx+1,0:ny+1)
      pointer(pupe,upe)

      double precision vep ( 0:nx+1,0:ny+1)
      pointer(pvep,vep)

      double precision ve2 ( 0:nx+1,0:ny+1)
      pointer(pve2,ve2)

      double precision vey ( 0:nx+1,0:ny+1)
      pointer(pvey,vey)

      double precision vycf ( 0:nx+1,0:ny+1)
      pointer(pvycf,vycf)

      double precision vycr ( 0:nx+1,0:ny+1)
      pointer(pvycr,vycr)

      double precision te ( 0:nx+1,0:ny+1)
      pointer(pte,te)

      double precision ti ( 0:nx+1,0:ny+1)
      pointer(pti,ti)

      double precision ng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(png,ng)

      double precision lng ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(plng,lng)

      double precision uug ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(puug,uug)

      double precision vyg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pvyg,vyg)

      double precision tg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptg,tg)

      double precision tev ( 0:nx+1,0:ny+1)
      pointer(ptev,tev)

      double precision niv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniv,niv)

      double precision upv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupv,upv)

      double precision ngv ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngv,ngv)

      double precision tiv ( 0:nx+1,0:ny+1)
      pointer(ptiv,tiv)

      double precision niy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0,niy0)

      double precision niy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1,niy1)

      double precision niy0s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy0s,niy0s)

      double precision niy1s ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pniy1s,niy1s)

      double precision ney0 ( 0:nx+1,0:ny+1)
      pointer(pney0,ney0)

      double precision ney1 ( 0:nx+1,0:ny+1)
      pointer(pney1,ney1)

      double precision nity0 ( 0:nx+1,0:ny+1)
      pointer(pnity0,nity0)

      double precision nity1 ( 0:nx+1,0:ny+1)
      pointer(pnity1,nity1)

      double precision tey0 ( 0:nx+1,0:ny+1)
      pointer(ptey0,tey0)

      double precision tey1 ( 0:nx+1,0:ny+1)
      pointer(ptey1,tey1)

      double precision tiy0 ( 0:nx+1,0:ny+1)
      pointer(ptiy0,tiy0)

      double precision tiy1 ( 0:nx+1,0:ny+1)
      pointer(ptiy1,tiy1)

      double precision tiy0s ( 0:nx+1,0:ny+1)
      pointer(ptiy0s,tiy0s)

      double precision tiy1s ( 0:nx+1,0:ny+1)
      pointer(ptiy1s,tiy1s)

      double precision tgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy0,tgy0)

      double precision tgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ptgy1,tgy1)

      double precision ngy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy0,ngy0)

      double precision ngy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngy1,ngy1)

      double precision pgy0 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy0,pgy0)

      double precision pgy1 ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppgy1,pgy1)

      double precision pg ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(ppg,pg)

      double precision phiy0 ( 0:nx+1,0:ny+1)
      pointer(pphiy0,phiy0)

      double precision phiy1 ( 0:nx+1,0:ny+1)
      pointer(pphiy1,phiy1)

      double precision phiy0s ( 0:nx+1,0:ny+1)
      pointer(pphiy0s,phiy0s)

      double precision phiy1s ( 0:nx+1,0:ny+1)
      pointer(pphiy1s,phiy1s)

      double precision pr ( 0:nx+1,0:ny+1)
      pointer(ppr,pr)

      double precision prev ( 0:nx+1,0:ny+1)
      pointer(pprev,prev)

      double precision prtv ( 0:nx+1,0:ny+1)
      pointer(pprtv,prtv)

      double precision pri ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppri,pri)

      double precision priv ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriv,priv)

      double precision priy0 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy0,priy0)

      double precision priy1 ( 0:nx+1,0:ny+1,1:nisp)
      pointer(ppriy1,priy1)

      double precision pre ( 0:nx+1,0:ny+1)
      pointer(ppre,pre)

      double precision ne ( 0:nx+1,0:ny+1)
      pointer(pne,ne)

      double precision nit ( 0:nx+1,0:ny+1)
      pointer(pnit,nit)

      double precision nginit ( 0:nx+1,0:ny+1)
      pointer(pnginit,nginit)

      double precision phi ( 0:nx+1,0:ny+1)
      pointer(pphi,phi)

      double precision phiv ( 0:nx+1,0:ny+1)
      pointer(pphiv,phiv)

      double precision zeff ( 0:nx+1,0:ny+1)
      pointer(pzeff,zeff)

      double precision netap ( 0:nx+1,0:ny+1)
      pointer(pnetap,netap)

      double precision znot ( 0:nx+1,0:ny+1)
      pointer(pznot,znot)

      double precision zimpc ( 0:nx+1,0:ny+1)
      pointer(pzimpc,zimpc)

      double precision nil ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pnil,nil)

      double precision upl ( 0:nx+1,0:ny+1,1:nisp)
      pointer(pupl,upl)

      double precision tel ( 0:nx+1,0:ny+1)
      pointer(ptel,tel)

      double precision til ( 0:nx+1,0:ny+1)
      pointer(ptil,til)

      double precision ngl ( 0:nx+1,0:ny+1,1:ngsp)
      pointer(pngl,ngl)

      double precision phil ( 0:nx+1,0:ny+1)
      pointer(pphil,phil)

      double precision upxpt ( 1:nusp,1:nxpt)
      pointer(pupxpt,upxpt)

      double precision nixpt ( 1:nusp,1:nxpt)
      pointer(pnixpt,nixpt)

      double precision visyxpt ( 1:nusp,1:nxpt)
      pointer(pvisyxpt,visyxpt)

      double precision vyhxpt ( 1:nusp,1:nxpt)
      pointer(pvyhxpt,vyhxpt)

      double precision vyvxpt ( 1:nusp,1:nxpt)
      pointer(pvyvxpt,vyvxpt)

      double precision fmihxpt ( 1:nusp,1:nxpt)
      pointer(pfmihxpt,fmihxpt)

      double precision fmivxpt ( 1:nusp,1:nxpt)
      pointer(pfmivxpt,fmivxpt)

      double precision rtaux ( 0:nx+1,0:ny+1)
      pointer(prtaux,rtaux)

      double precision rtauy ( 0:nx+1,0:ny+1)
      pointer(prtauy,rtauy)

      double precision rtau ( 0:nx+1,0:ny+1)
      pointer(prtau,rtau)

      double precision betap ( 0:nx+1,0:ny+1)
      pointer(pbetap,betap)
      common /bbb243/ facmg, istgcon, rtauxfac, rtauyfac, rt_scal
      common /bbb243/ fracvgpgp
      common /bbb246/ pmi, pzi, pmg, pznucl
      common /bbb246/ pni, plni, pnm, pnz2
      common /bbb246/ puu, puup, pup, pupi
      common /bbb246/ pupifmb, puz, pv2, pv2xgp
      common /bbb246/ pv2ce, pv2cb, pve2cb
      common /bbb246/ pv2cd, pve2cd, pq2cd
      common /bbb246/ pv2rd, pv2dd, pvy, pvygp
      common /bbb246/ pvytan, pvygtan, pvyce
      common /bbb246/ pvycb, pveycb, pvycp
      common /bbb246/ pveycp, pvyrd, pvydd
      common /bbb246/ pvyavis, pvex, pupe, pvep
      common /bbb246/ pve2, pvey, pvycf, pvycr
      common /bbb246/ pte, pti, png, plng
      common /bbb246/ puug, pvyg, ptg, ptev
      common /bbb246/ pniv, pupv, pngv, ptiv
      common /bbb246/ pniy0, pniy1, pniy0s
      common /bbb246/ pniy1s, pney0, pney1
      common /bbb246/ pnity0, pnity1, ptey0
      common /bbb246/ ptey1, ptiy0, ptiy1
      common /bbb246/ ptiy0s, ptiy1s, ptgy0
      common /bbb246/ ptgy1, pngy0, pngy1, ppgy0
      common /bbb246/ ppgy1, ppg, pphiy0, pphiy1
      common /bbb246/ pphiy0s, pphiy1s, ppr
      common /bbb246/ pprev, pprtv, ppri, ppriv
      common /bbb246/ ppriy0, ppriy1, ppre, pne
      common /bbb246/ pnit, pnginit, pphi, pphiv
      common /bbb246/ pzeff, pnetap, pznot
      common /bbb246/ pzimpc, pnil, pupl, ptel
      common /bbb246/ ptil, pngl, pphil, pupxpt
      common /bbb246/ pnixpt, pvisyxpt, pvyhxpt
      common /bbb246/ pvyvxpt, pfmihxpt, pfmivxpt
      common /bbb246/ prtaux, prtauy, prtau
      common /bbb246/ pbetap
c End of Compla
c ni,up,..,niv,upv,
c Group Aux
      integer ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3, ix4, ix5
      double precision tv, t0, t1, t2, a
      integer ix6, ixmp
      common /bbb100/ ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3
      common /bbb100/ ix4, ix5, ix6, ixmp
      common /bbb103/ tv, t0, t1, t2, a
c End of Aux
c ix,iy,igsp,ix1,ix2
c Group Selec
      integer i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2, j3, j4
      integer j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p, ixs1, ixf6, iys1
      integer iyf6, xlinc, xrinc, yinc, isjaccorall

      integer ixm1 ( 0:nx+1,0:ny+1)
      pointer(pixm1,ixm1)

      integer ixp1 ( 0:nx+1,0:ny+1)
      pointer(pixp1,ixp1)

      integer iym1a ( 0:nx+1,0:ny+1)
      pointer(piym1a,iym1a)

      integer iyp1a ( 0:nx+1,0:ny+1)
      pointer(piyp1a,iyp1a)

      double precision stretcx ( 0:nx+1,0:ny+1)
      pointer(pstretcx,stretcx)
      common /bbb90/ i1, i2, i2p, i3, i4, i5, i5m, i6, i7, i8, j1, j2
      common /bbb90/ j3, j4, j5, j5m, j6, j7, j8, j1p, j2p, j5p, j6p
      common /bbb90/ ixs1, ixf6, iys1, iyf6, xlinc, xrinc, yinc
      common /bbb90/ isjaccorall
      common /bbb96/ pixm1, pixp1, piym1a
      common /bbb96/ piyp1a, pstretcx
c End of Selec
c ixp1
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
c nysol,nyomitmx

c.. Do all interior cells as 4-pt ave to upper vertex; reset X-point below
      do 23000 ix = 1, nx
         do 23002 iy = 1, ny
            ix1 = ixp1(ix,iy)
            ix2 = ixp1(ix,iy+1)
            tev(ix,iy) = 0.25d0*( te(ix,iy ) + te(ix1,iy ) + te(ix,iy+1) 
     &         + te(ix2,iy+1) )
            tiv(ix,iy) = 0.25d0*( ti(ix,iy ) + ti(ix1,iy ) + ti(ix,iy+1) 
     &         + ti(ix2,iy+1) )
            phiv(ix,iy) = 0.25d0*( phi(ix,iy ) + phi(ix1,iy ) + phi(ix,
     &         iy+1) + phi(ix2,iy+1) )

            do 23004 ifld = 1, nisp
               niv(ix,iy,ifld) =0.25d0*(ni(ix,iy, ifld) + ni(ix1,iy, 
     &            ifld) + ni(ix,iy+1,ifld) + ni(ix2,iy+1,ifld) )
               upv(ix,iy,ifld) =0.5d0*( up(ix,iy,ifld) + up(ix,iy+1,ifld
     &            ) )
23004       continue

            do 23006 igsp = 1, ngsp
               ngv(ix,iy,igsp) =0.25d0*(ng(ix,iy, igsp) + ng(ix1,iy, 
     &            igsp) + ni(ix,iy+1,igsp) + ng(ix2,iy+1,igsp) )
23006       continue

23002    continue
23000 continue

c.. Do all x-bdry cells as 2-pt y-ave to upper vertex
      do 23008 ix = 0, nx+1, nx+1
c note: corner cells relegated to y-bdry here
         do 23010 iy = 1, ny
            ix1 = ixp1(ix,iy)
            ix2 = ixp1(ix,iy+1)
            tev(ix,iy) = 0.5d0*( te(ix,iy) + te(ix,iy+1) )
            tiv(ix,iy) = 0.5d0*( ti(ix,iy) + ti(ix,iy+1) )
            phiv(ix,iy) = 0.5d0*( phi(ix,iy) + phi(ix,iy+1) )
            do 23012 ifld = 1, nisp
               niv(ix,iy,ifld) = 0.5d0*( ni(ix,iy,ifld) + ni(ix,iy+1,
     &            ifld) )
               upv(ix,iy,ifld) = 0.5d0*( up(ix,iy,ifld) + up(ix,iy+1,
     &            ifld) )
23012       continue
            do 23014 igsp = 1, ngsp
               ngv(ix,iy,igsp) = 0.5d0*( ng(ix,iy,igsp) + ng(ix,iy+1,
     &            igsp) )
23014       continue
23010    continue
23008 continue

c.. Do all y-bdry cells as 2-pt x-ave to upper vertex
      do 23016 ix = 0, nx+1
         do 23018 iy = 0, ny+1, ny+1
            ix1 = ixp1(ix,iy)
            tev(ix,iy) = 0.5d0*( te(ix,iy) + te(ix1,iy) )
            tiv(ix,iy) = 0.5d0*( ti(ix,iy) + ti(ix1,iy) )
            phiv(ix,iy) = 0.5d0*( phi(ix,iy) + phi(ix1,iy) )
            do 23020 ifld = 1, nisp
               niv(ix,iy,ifld) = 0.5d0*( ni(ix,iy,ifld) + ni(ix1,iy,ifld
     &            ) )
               upv(ix,iy,ifld) = up(ix,iy,ifld)
23020       continue
            do 23022 igsp = 1, ngsp
               ngv(ix,iy,igsp) = 0.5d0*( ng(ix,iy,igsp) + ng(ix1,iy,igsp
     &            ) )
23022       continue
23018    continue
23016 continue

c.. Now reset x-point values; mostly 8-pt ave
      if (nyomitmx .lt. nysol(1)) then
c otherwise core only - skip

c loop over mesh regions
         do 23024 jx = 1, nxpt
            is = ixpt1(jx)
            js = iysptrx1(jx)
            if (jx.eq.1) then
c adjacent cells are in mesh region jx=nxpt
               ie = ixpt2(nxpt)
            else
c adjacent cells are in the previous mesh region
               ie = ixpt2(jx-1)
            endif
            if (is.lt.0 .or. ie.lt.0 .or. ie.gt.nx) return
c ... Last test (ie.gt.nx) to fix parallel version with mpi - check
            tev(is,js) = 0.125d0*( te(is,js)+te(is+1,js)+te(is,js+1)+te(
     &         is+1,js+1)+ te(ie,js)+te(ie+1,js)+te(ie,js+1)+te(ie+1,js+
     &         1) )
            tev(ie,js) = tev(is,js)
            tiv(is,js) = 0.125d0*( ti(is,js)+ti(is+1,js)+ti(is,js+1)+ti(
     &         is+1,js+1)+ ti(ie,js)+ti(ie+1,js)+ti(ie,js+1)+ti(ie+1,js+
     &         1) )
            tiv(ie,js) = tiv(is,js)
            phiv(is,js) = 0.125d0*( phi(is,js)+phi(is+1,js)+phi(is,js+1)
     &         +phi(is+1,js+1)+ phi(ie,js)+phi(ie+1,js)+phi(ie,js+1)+phi
     &         (ie+1,js+1) )
            phiv(ie,js) = phiv(is,js)

            do 23026 ifld = 1, nisp
               niv(is,js,ifld) = 0.125d0*( ni(is,js,ifld)+ni(is+1,js,
     &            ifld)+ ni(is,js+1,ifld)+ni(is+1,js+1,ifld)+ ni(ie,js,
     &            ifld)+ni(ie+1,js,ifld)+ ni(ie,js+1,ifld)+ni(ie+1,js+1,
     &            ifld) )
               niv(ie,js,ifld) = niv(is,js,ifld)
               upv(is,js,ifld) = 0.25d0*( up(is,js,ifld)+up(is,js+1,ifld
     &            )+ up(ie,js,ifld)+up(ie+1,js+1,ifld) )
23026       continue

            do 23028 igsp = 1, ngsp
               ngv(is,js,igsp) = 0.125d0*( ng(is,js,igsp)+ng(is+1,js,
     &            igsp)+ ng(is,js+1,igsp)+ng(is+1,js+1,igsp)+ ng(ie,js,
     &            igsp)+ng(ie+1,js,igsp)+ ng(ie,js+1,igsp)+ng(ie+1,js+1,
     &            igsp) )
               ngv(ie,js,igsp) = ngv(is,js,igsp)
23028       continue

23024    continue
      endif

      return
      end
c ***** end of subroutine comp_vertex_vals **************
