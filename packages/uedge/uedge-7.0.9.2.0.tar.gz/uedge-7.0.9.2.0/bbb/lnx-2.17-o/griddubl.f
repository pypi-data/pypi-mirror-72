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
c     ./../griddubl.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c






















































































































































c-----------------------------------------------------------------------
      subroutine gridseq
cProlog

c     GRIDSEQ provides saving of variables for grid interp. and restart

      implicit none

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nhsp,nisp,ngsp,nxpt
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
c ixlb,ixpt1,ixpt2,ixrb,iysptrx
c Group Aux
      integer ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3, ix4, ix5
      double precision tv, t0, t1, t2, a
      integer ix6, ixmp
      common /bbb100/ ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3
      common /bbb100/ ix4, ix5, ix6, ixmp
      common /bbb103/ tv, t0, t1, t2, a
c End of Aux
c igsp
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
c ixlbo,ixpt1o,ixpt2o,ixrbo,iysptrxo
c xnrmo,xvnrmo,ynrmo,yvnrmo,
c nis,tes,tis,tgs,ups,phis,ngs,isimesh,afracs,
c ixst,ixend,ixsto,ixendo
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
c afrac,isimpon
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
c ni,up,ng,te,ti,phi
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
c xnrm,xvnrm,ynrm,yvnrm
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
c nyomitmx
c Group Npes_mpi
      integer npes, mype, ismpion, hascomm, isparmultdt
      common /bbb630/ npes, mype, ismpion, hascomm, isparmultdt
c End of Npes_mpi
c ismpion
c Group Cut_indices
      integer ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2, iycut3
      integer iycut4
      common /com100/ ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2
      common /com100/ iycut3, iycut4
c End of Cut_indices
c ixcut1,iycut1,ixcut2,iycut2,ixcut3,iycut3
c ixcut4,iycut4

      integer ifld,jx,ir

cturn-off switch; at least one mesh calc
      if (ismpion .eq. 0) isimesh = 0

      iysptrxo = iysptrx
      do 23000 jx=1,nxpt
         ixlbo(jx) = ixlb(jx)
         ixpt1o(jx) = ixpt1(jx)
         ixpt2o(jx) = ixpt2(jx)
         ixrbo(jx) = ixrb(jx)
23000 continue

c...  Order poloidal regions from old mesh (as new mesh in ueinit)
      ixsto(1) = ixlb(1)
      ixendo(1) = ixcut1
      if (ixlb(1) .eq. 0 .and. ixcut1 .eq. 0) then
c no inner leg
         ixsto(2) = 0
      else
         ixsto(2) = max(ixlb(1), ixcut1+1)
      endif
      ixendo(2) = ixcut2
      if (nyomitmx .ge. nysol(1)) then
c no inner/outer leg region
         ixsto(2) = 0
         ixendo(2) = nx+1
      endif
      if (nx .eq. 1) then
cspecial case: 1D in radial direction
         ixendo(2) = 2
      endif
c..   Now need to check if ixrb is > or < ixcut3
      ixsto(3) = ixcut2+1
      if (ixcut3 .gt. ixrb(1) .or. nxpt.eq.1) then
c3 regions in first domain
         ixendo(3) = ixrb(1)+1
c 4 regions in 1st domain, end on ixcut3
      else
         ixendo(3) = ixcut3
      endif

c..   Continue ordering if double null or snowflake
      if (nxpt .eq. 2) then
         if (ixcut3 .gt. ixrb(1)) then
c do 3-region 2nd domain
            ixsto(4) = ixlb(2)
            ixendo(4) = ixcut3
            ixsto(5) = ixcut3+1
c 4 regions in 1st domain, compl & do 2-region 2nd domain
         else
            ixsto(4) = ixcut3+1
            ixendo(4) = ixrb(1)+1
            ixsto(5) = ixlb(2)
         endif
c remain indices are the same
         ixendo(5) = ixcut4
         ixsto(6) = ixcut4+1
         ixendo(6) = ixrb(2)+1
      endif
c if-test on nxpt

      call s2copy (nx+2, ny+2, xnrm, 1, nx+2, xnrmo, 1, nx+2)
      call s2copy (nx+2, ny+2, xvnrm, 1, nx+2, xvnrmo, 1, nx+2)
      call s2copy (nx+2, ny+2, ynrm, 1, nx+2, ynrmo, 1, nx+2)
      call s2copy (nx+2, ny+2, yvnrm, 1, nx+2, yvnrmo, 1, nx+2)

      do 705 ifld = 1, nisp
         if (nyomitmx .ge. nysol(1)+nyout(1)) then
c           # fill dead guard cells with adjacent values
            do 23003 iy = 0, ny+1
               ni(0,iy,ifld) = ni(1,iy,ifld)
               ni(nx+1,iy,ifld) = ni(nx,iy,ifld)
23003       continue
         endif
         call s2copy (nx+2, ny+2, ni(0,0,ifld), 1, nx+2, nis(0,0,ifld), 
     &      1, nx+2)
  705    continue
      do 706 ifld = 1, nusp
         if (nyomitmx .ge. nysol(1)+nyout(1)) then
c           # fill dead guard cells with adjacent values
            do 23006 iy = 0, ny+1
               up(0,iy,ifld) = up(1,iy,ifld)
               up(nx+1,iy,ifld) = up(nx,iy,ifld)
23006       continue
         endif
         call s2copy (nx+2, ny+2, up(0,0,ifld), 1, nx+2, ups(0,0,ifld), 
     &      1, nx+2)
  706    continue

      do 707 igsp = 1, ngsp
         if (nyomitmx .ge. nysol(1)+nyout(1)) then
c           # fill dead guard cells with adjacent values
            do 23009 iy = 0, ny+1
               ng(0,iy,igsp) = ng(1,iy,igsp)
               ng(nx+1,iy,igsp) = ng(nx,iy,igsp)
23009       continue
         endif
         call s2copy (nx+2, ny+2, ng(0,0,igsp), 1, nx+2, ngs(0,0,igsp), 
     &      1, nx+2)
         call s2copy (nx+2, ny+2, tg(0,0,igsp), 1, nx+2, tgs(0,0,igsp), 
     &      1, nx+2)
  707    continue

      if (nyomitmx .ge.nysol(1)+nyout(1)) then
c           # fill dead guard cells with adjacent values
         do 23011 iy = 0, ny+1
            te(0,iy) = te(1,iy)
            te(nx+1,iy) = te(nx,iy)
            ti(0,iy) = ti(1,iy)
            ti(nx+1,iy) = ti(nx,iy)
            phi(0,iy) = phi(1,iy)
            phi(nx+1,iy) = phi(nx,iy)
23011    continue
      endif
      call s2copy (nx+2, ny+2, te, 1, nx+2, tes, 1, nx+2)
      call s2copy (nx+2, ny+2, ti, 1, nx+2, tis, 1, nx+2)
      call s2copy (nx+2, ny+2, tg, 1, nx+2, tgs, 1, nx+2)
      call s2copy (nx+2, ny+2, phi, 1, nx+2, phis, 1, nx+2)
      if (isimpon.gt.0) call s2copy (nx+2, ny+2, afrac, 1, nx+2, afracs, 
     &      1, nx+2)

      return
      end
c****** end of subroutine gridseq ***
c************************************
c-----------------------------------------------------------------------
      subroutine refpla
cProlog

c     REFPLA interpolates the plasma variables onto a grid which is
c     twice as fine as the preceding one

      implicit none

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
c geometry,nxc
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nhsp,nisp,ngsp
c Group Aux
      integer ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3, ix4, ix5
      double precision tv, t0, t1, t2, a
      integer ix6, ixmp
      common /bbb100/ ix, iy, igsp, iv, iv1, iv2, iv3, ix1, ix2, ix3
      common /bbb100/ ix4, ix5, ix6, ixmp
      common /bbb103/ tv, t0, t1, t2, a
c End of Aux
c ix,iy,igsp,ix2
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
c nxold,nyold,nis,tes,tis,tgs,phis,ups,ngs
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


c...  local variables
      integer ifld
      integer ix2p, ix2m, ip1, im1, ixn, iy2, iy2p
c.... note: ix2 is already defined in Aux, but we can use it since it is
c.... meant to be a work variable, i.e., its value can change


c.... This is for doubling the grid in both x and y
      do 704 iy = 1, nyold-1
         iy2 = 2*iy
         iy2p = iy2 + 1
         do 703 ix = 1, nxold
            ix2 = 2*ix
            ix2p = ix2 + 1
            ix2m = max(ix2 - 1,0)
            ip1 = (ixp1(ix2,iy2) + 1) / 2
            im1 = ixm1(ix2m,iy2) / 2
            ixn = ixm1(ix2p,iy2) / 2
            do 23002 ifld = 1, nisp
               ni(ix2,iy2,ifld) = 9*nis(ix,iy,ifld)/16 + 3*(nis(ip1,iy,
     &            ifld)+nis(ix,iy+1,ifld))/16 + nis(ip1,iy+1,ifld)/16
               ni(ix2p,iy2,ifld) = 9*nis(ix+1,iy,ifld)/16 + 3*(nis(ixn,
     &            iy,ifld)+nis(ix+1,iy+1,ifld))/16+ nis(ixn,iy+1,ifld)/
     &            16
               ni(ix2,iy2p,ifld) = 9*nis(ix,iy+1,ifld)/16 + 3*(nis(ix,iy
     &            ,ifld)+nis(ip1,iy+1,ifld))/16 + nis(ip1,iy,ifld)/16
               ni(ix2p,iy2p,ifld) = 9*nis(ix+1,iy+1,ifld)/16 + 3*(nis(
     &            ixn,iy+1,ifld)+nis(ix+1,iy,ifld))/16+ nis(ixn,iy,ifld)
     &            /16
23002       continue

            do 23004 ifld = 1, nusp
               up(ix2,iy2,ifld) = .75d0*ups(ix,iy,ifld) + .25d0*ups(ix,
     &            iy+1,ifld)
               up(ix2,iy2p,ifld) = .75d0*ups(ix,iy+1,ifld) + .25d0*ups(
     &            ix,iy,ifld)
               up(ix2m,iy2,ifld) = 3*(ups(ix,iy,ifld)+ups(im1,iy,ifld))/
     &            8 + (ups(ix,iy+1,ifld)+ups(im1,iy+1,ifld))/8
               up(ix2m,iy2p,ifld) = 3*(ups(ix,iy+1,ifld) + ups(im1,iy+1,
     &            ifld))/8 + (ups(ix,iy,ifld)+ups(im1,iy,ifld))/8
23004       continue

            te(ix2,iy2) = 9*tes(ix,iy)/16 + 3*(tes(ip1,iy)+tes(ix,iy+1))
     &         /16 + tes(ip1,iy+1)/16
            te(ix2p,iy2) = 9*tes(ix+1,iy)/16 + 3*(tes(ixn,iy)+tes(ix+1,
     &         iy+1))/16 + tes(ixn,iy+1)/16
            te(ix2,iy2p) = 9*tes(ix,iy+1)/16 + 3*(tes(ix,iy)+tes(ip1,iy+
     &         1))/16 + tes(ip1,iy)/16
            te(ix2p,iy2p) = 9*tes(ix+1,iy+1)/16 + 3*(tes(ixn,iy+1)+tes(
     &         ix+1,iy))/16 + tes(ixn,iy)/16

            ti(ix2,iy2) = 9*tis(ix,iy)/16 + 3*(tis(ip1,iy)+tis(ix,iy+1))
     &         /16 + tis(ip1,iy+1)/16
            ti(ix2p,iy2) = 9*tis(ix+1,iy)/16 + 3*(tis(ixn,iy)+tis(ix+1,
     &         iy+1))/16 + tis(ixn,iy+1)/16
            ti(ix2,iy2p) = 9*tis(ix,iy+1)/16 + 3*(tis(ix,iy)+tis(ip1,iy+
     &         1))/16 + tis(ip1,iy)/16
            ti(ix2p,iy2p) = 9*tis(ix+1,iy+1)/16 + 3*(tis(ixn,iy+1)+tis(
     &         ix+1,iy))/16 + tis(ixn,iy)/16

            phi(ix2,iy2) = 9*phis(ix,iy)/16 + 3*(phis(ip1,iy)+phis(ix,iy
     &         +1))/16 + phis(ip1,iy+1)/16
            phi(ix2p,iy2) = 9*phis(ix+1,iy)/16 + 3*(phis(ixn,iy)+phis(ix
     &         +1,iy+1))/16 + phis(ixn,iy+1)/16
            phi(ix2,iy2p) = 9*phis(ix,iy+1)/16 + 3*(phis(ix,iy)+phis(ip1
     &         ,iy+1))/16 + phis(ip1,iy)/16
            phi(ix2p,iy2p) = 9*phis(ix+1,iy+1)/16 + 3*(phis(ixn,iy+1)+
     &         phis(ix+1,iy))/16 + phis(ixn,iy)/16

            do 23006 igsp = 1, ngsp

               ng(ix2,iy2,igsp) = 9*ngs(ix,iy,igsp)/16 + 3*(ngs(ip1,iy,
     &            igsp)+ngs(ix,iy+1,igsp))/16 + ngs(ip1,iy+1,igsp)/16
               ng(ix2p,iy2,igsp) = 9*ngs(ix+1,iy,igsp)/16 + 3*(ngs(ixn,
     &            iy,igsp)+ngs(ix+1,iy+1,igsp))/16+ ngs(ixn,iy+1,igsp)/
     &            16
               ng(ix2,iy2p,igsp) = 9*ngs(ix,iy+1,igsp)/16 + 3*(ngs(ix,iy
     &            ,igsp)+ngs(ip1,iy+1,igsp))/16 + ngs(ip1,iy,igsp)/16
               ng(ix2p,iy2p,igsp) = 9*ngs(ix+1,iy+1,igsp)/16 + 3*(ngs(
     &            ixn,iy+1,igsp)+ngs(ix+1,iy,igsp))/16+ ngs(ixn,iy,igsp)
     &            /16
23006       continue

            do 23008 igsp = 1, ngsp

               tg(ix2,iy2,igsp) = 9*tgs(ix,iy,igsp)/16 + 3*(tgs(ip1,iy,
     &            igsp)+tgs(ix,iy+1,igsp))/16 + tgs(ip1,iy+1,igsp)/16
               tg(ix2p,iy2,igsp) = 9*tgs(ix+1,iy,igsp)/16 + 3*(tgs(ixn,
     &            iy,igsp)+tgs(ix+1,iy+1,igsp))/16+ tgs(ixn,iy+1,igsp)/
     &            16
               tg(ix2,iy2p,igsp) = 9*tgs(ix,iy+1,igsp)/16 + 3*(tgs(ix,iy
     &            ,igsp)+tgs(ip1,iy+1,igsp))/16 + tgs(ip1,iy,igsp)/16
               tg(ix2p,iy2p,igsp) = 9*tgs(ix+1,iy+1,igsp)/16 + 3*(tgs(
     &            ixn,iy+1,igsp)+tgs(ix+1,iy,igsp))/16+ tgs(ixn,iy,igsp)
     &            /16
23008       continue


  703       continue

         do 23010 ifld = 1, nisp
            ni(0,iy2,ifld) = .75d0*nis(0,iy,ifld)+.25d0*nis(0,iy+1,ifld)
            ni(1,iy2,ifld) = 3*(nis(0,iy ,ifld)+nis(1,iy ,ifld))/8 + (
     &         nis(0,iy+1,ifld)+nis(1,iy+1,ifld))/8
            ni(nx+1,iy2,ifld) = .75d0*nis(nxold+1,iy,ifld)+ .25d0*nis(
     &         nxold+1,iy+1,ifld)
            ni(nx,iy2,ifld) = 3*(nis(nxold,iy ,ifld)+ nis(nxold+1,iy ,
     &         ifld))/8 + (nis(nxold,iy+1,ifld)+ nis(nxold+1,iy+1,ifld))
     &         /8
23010    continue
         do 23012 ifld = 1, nusp
            up(0,iy2,ifld) = .75d0*ups(0,iy,ifld)+.25d0*ups(0,iy+1,ifld)
            up(1,iy2,ifld) = 3*(ups(0,iy ,ifld)+ups(1,iy ,ifld))/8 + (
     &         ups(0,iy+1,ifld)+ups(1,iy+1,ifld))/8
            up(nx+1,iy2,ifld) = .75d0*ups(nxold+1,iy,ifld)+ .25d0*ups(
     &         nxold+1,iy+1,ifld)
            up(nx,iy2,ifld) = .75d0*ups(nxold+1,iy,ifld)+ .25d0*ups(
     &         nxold+1,iy+1,ifld)
23012    continue
         te(0,iy2) = .75d0*tes(0,iy)+.25d0*tes(0,iy+1)
         te(1,iy2) = 3*(tes(0,iy ) + tes(1,iy ))/8 + (tes(0,iy+1) + tes(
     &      1,iy+1))/8
         te(nx+1,iy2) = .75d0*tes(nxold+1,iy)+.25d0*tes(nxold+1,iy+1)
         te(nx,iy2) = 3*(tes(nxold,iy ) + tes(nxold+1,iy ))/8 + (tes(
     &      nxold,iy+1) + tes(nxold+1,iy+1))/8
         ti(0,iy2) = .75d0* tis(0,iy)+.25d0*tis(0,iy+1)
         ti(1,iy2) = 3*(tis(0,iy ) + tis(1,iy ))/8 + (tis(0,iy+1) + tis(
     &      1,iy+1))/8
         ti(nx+1,iy2) = .75d0*tis(nxold+1,iy)+.25d0*tis(nxold+1,iy+1)
         ti(nx,iy2) = 3*(tis(nxold,iy ) + tis(nxold+1,iy ))/8 + (tis(
     &      nxold,iy+1) + tis(nxold+1,iy+1))/8
         phi(0,iy2) = .75d0* phis(0,iy)+.25d0*phis(0,iy+1)
         phi(1,iy2) = 3*(phis(0,iy ) + phis(1,iy ))/8 + (phis(0,iy+1) + 
     &      phis(1,iy+1))/8
         phi(nx+1,iy2) = .75d0*phis(nxold+1,iy)+.25d0*phis(nxold+1,iy+1)
         phi(nx,iy2) = 3*(phis(nxold,iy ) + phis(nxold+1,iy ))/8 + (phis
     &      (nxold,iy+1) + phis(nxold+1,iy+1))/8

         do 23014 igsp = 1, ngsp
            ng(0,iy2,igsp) = .75d0*ngs(0,iy,igsp)+.25d0*ngs(0,iy+1,igsp)
            ng(1,iy2,igsp) = 3*(ngs(0,iy ,igsp)+ngs(1,iy, igsp))/8 + (
     &         ngs(0,iy+1,igsp)+ngs(1,iy+1,igsp))/8
            ng(nx+1,iy2,igsp) = .75d0*ngs(nxold+1,iy ,igsp)+ .25d0*ngs(
     &         nxold+1,iy+1,igsp)
            ng(nx,iy2,igsp) = 3*(ngs(nxold ,iy ,igsp)+ ngs(nxold+1,iy ,
     &         igsp))/8 + (ngs(nxold,iy+1,igsp)+ngs(nxold+1,iy+1,igsp))/
     &         8
23014    continue

         do 23016 igsp = 1, ngsp
            tg(0,iy2,igsp) = .75d0*tgs(0,iy,igsp)+.25d0*tgs(0,iy+1,igsp)
            tg(1,iy2,igsp) = 3*(tgs(0,iy ,igsp)+tgs(1,iy, igsp))/8 + (
     &         tgs(0,iy+1,igsp)+tgs(1,iy+1,igsp))/8
            tg(nx+1,iy2,igsp) = .75d0*tgs(nxold+1,iy ,igsp)+ .25d0*tgs(
     &         nxold+1,iy+1,igsp)
            tg(nx,iy2,igsp) = 3*(tgs(nxold ,iy ,igsp)+ tgs(nxold+1,iy ,
     &         igsp))/8 + (tgs(nxold,iy+1,igsp)+tgs(nxold+1,iy+1,igsp))/
     &         8
23016    continue

         do 23018 ifld = 1, nisp
            ni(0,iy2p,ifld) = .25d0*nis(0,iy,ifld)+.75d0*nis(0,iy+1,ifld
     &         )
            ni(1,iy2p,ifld) = (nis(0,iy ,ifld)+nis(1,iy ,ifld))/8 + 3*(
     &         nis(0,iy+1,ifld)+nis(1,iy+1,ifld))/8
            ni(nx+1,iy2p,ifld) = .25d0*nis(nxold+1,iy,ifld)+ .75d0*nis(
     &         nxold+1,iy+1,ifld)
            ni(nx,iy2p,ifld) = (nis(nxold,iy ,ifld)+ nis(nxold+1,iy ,
     &         ifld))/8 + 3*(nis(nxold,iy+1,ifld)+ nis(nxold+1,iy+1,ifld
     &         ))/8
23018    continue
         do 23020 ifld = 1, nusp
            up(0,iy2p,ifld) = .25d0*ups(0,iy,ifld)+.75d0*ups(0,iy+1,ifld
     &         )
            up(1,iy2p,ifld) = (ups(0,iy ,ifld)+ups(1,iy ,ifld))/8 + 3*(
     &         ups(0,iy+1,ifld)+ups(1,iy+1,ifld))/8
            up(nx+1,iy2p,ifld) = .25d0*ups(nxold+1,iy ,ifld) + .75d0*ups
     &         (nxold+1,iy+1,ifld)
            up(nx,iy2p,ifld) = .25d0*ups(nxold+1,iy ,ifld) + .75d0*ups(
     &         nxold+1,iy+1,ifld)
23020    continue
         te(0,iy2p) = .25d0*tes(0,iy)+.75d0*tes(0,iy+1)
         te(1,iy2p) = (tes(0,iy ) + tes(1,iy ))/8 + 3*(tes(0,iy+1) + tes
     &      (1,iy+1))/8
         te(nx+1,iy2p) = .25d0*tes(nxold+1,iy)+.75d0*tes(nxold+1,iy+1)
         te(nx,iy2p) = (tes(nxold,iy ) + tes(nxold+1,iy ))/8 + 3*(tes(
     &      nxold,iy+1) + tes(nxold+1,iy+1))/8
         ti(0,iy2p) = .25d0* tis(0,iy)+.75d0*tis(0,iy+1)
         ti(1,iy2p) = (tis(0,iy ) + tis(1,iy ))/8 + 3*(tis(0,iy+1) + tis
     &      (1,iy+1))/8
         ti(nx+1,iy2p) = .25d0*tis(nxold+1,iy)+.75d0*tis(nxold+1,iy+1)
         ti(nx,iy2p) = (tis(nxold,iy ) + tis(nxold+1,iy ))/8 + 3*(tis(
     &      nxold,iy+1) + tis(nxold+1,iy+1))/8
         phi(0,iy2p) = .25d0* phis(0,iy)+.75d0*phis(0,iy+1)
         phi(1,iy2p) = (phis(0,iy ) + phis(1,iy ))/8 + 3*(phis(0,iy+1) + 
     &      phis(1,iy+1))/8
         phi(nx+1,iy2p) = .25d0*phis(nxold+1,iy)+.75d0*phis(nxold+1,iy+1
     &      )
         phi(nx,iy2p) = (phis(nxold,iy ) + phis(nxold+1,iy ))/8 + 3*(
     &      phis(nxold,iy+1) + phis(nxold+1,iy+1))/8

         do 23022 igsp = 1, ngsp
            ng(0,iy2p,igsp) = .25d0*ngs(0,iy,igsp)+.75d0*ngs(0,iy+1,igsp
     &         )
            ng(1,iy2p,igsp) = (ngs(0,iy ,igsp)+ngs(1,iy ,igsp))/8 + 3*(
     &         ngs(0,iy+1,igsp)+ngs(1,iy+1,igsp))/8
            ng(nx+1,iy2p,igsp) = .25d0*ngs(nxold+1,iy ,igsp)+ .75d0*ngs(
     &         nxold+1,iy+1,igsp)
            ng(nx,iy2p,igsp) = (ngs(nxold ,iy ,igsp)+ ngs(nxold+1,iy ,
     &         igsp))/8 + 3*(ngs(nxold ,iy+1,igsp)+ ngs(nxold+1,iy+1,
     &         igsp))/8
23022    continue
         do 23024 igsp = 1, ngsp
            tg(0,iy2p,igsp) = .25d0*tgs(0,iy,igsp)+.75d0*tgs(0,iy+1,igsp
     &         )
            tg(1,iy2p,igsp) = (tgs(0,iy ,igsp)+tgs(1,iy ,igsp))/8 + 3*(
     &         tgs(0,iy+1,igsp)+tgs(1,iy+1,igsp))/8
            tg(nx+1,iy2p,igsp) = .25d0*tgs(nxold+1,iy ,igsp)+ .75d0*tgs(
     &         nxold+1,iy+1,igsp)
            tg(nx,iy2p,igsp) = (tgs(nxold ,iy ,igsp)+ tgs(nxold+1,iy ,
     &         igsp))/8 + 3*(tgs(nxold ,iy+1,igsp)+ tgs(nxold+1,iy+1,
     &         igsp))/8
23024    continue

  704    continue

c.... Do the iy=0,1 and iy=ny+,ny1 points
      do 706 ix = 1 , nxold-1
         ix2 = 2*ix
         ix2p = ix2 + 1
         ix2m = max(ix2 - 1,0)
         ip1 = (ixp1(ix2,0) + 1) / 2
         im1 = ixm1(ix2m,0) / 2
         ixn = ixm1(ix2p,0) / 2
c....    the special ip1, im1, ixn are not done for ny+1 as the cuts are
c....    assumed not to extend there
         do 23027 ifld = 1, nisp
            ni(ix2,0,ifld) = .75d0*nis(ix,0,ifld)+.25d0*nis(ip1,0,ifld)
            ni(ix2,1,ifld) = 3*(nis(ix ,0,ifld)+nis(ix ,1,ifld))/8 + (
     &         nis(ip1,0,ifld)+nis(ip1,1,ifld))/8
            ni(ix2,ny+1,ifld) = .75d0*nis(ix,nyold+1,ifld) + .25d0*nis(
     &         ix+1,nyold+1,ifld)
            ni(ix2,ny,ifld) = 3*(nis(ix ,nyold+1,ifld)+ nis(ix ,nyold,
     &         ifld))/8+ (nis(ix+1,nyold+1,ifld)+ nis(ix+1,nyold,ifld))/
     &         8
23027    continue
         do 23029 ifld = 1, nusp
            up(ix2,0,ifld) = ups(ix,0,ifld)
            up(ix2,1,ifld) = 0.5d0*(ups(ix,0,ifld)+ups(ix,1,ifld))
            up(ix2,ny+1,ifld) = ups(ix,nyold+1,ifld)
            up(ix2,ny,ifld) = 0.5d0*(ups(ix,nyold+1,ifld)+ ups(ix,nyold 
     &         ,ifld))
23029    continue
         te(ix2,0) = .75d0*tes(ix,0) + .25d0*tes(ip1,0)
         te(ix2,1) = 3*(tes(ix ,0)+tes(ix ,1))/8 + (tes(ip1,0)+tes(ip1,1
     &      ))/8
         te(ix2,ny+1) = .75d0*tes(ix,nyold+1) + .25d0*tes(ix+1,nyold+1)
         te(ix2,ny) = 3*(tes(ix ,nyold+1)+tes(ix ,nyold))/8 + (tes(ix+1,
     &      nyold+1)+tes(ix+1,nyold))/8
         ti(ix2,0) = .75d0*tis(ix,0) + .25d0*tis(ip1,0)
         ti(ix2,1) = 3*(tis(ix ,0)+tis(ix ,1))/8 + (tis(ip1,0)+tis(ip1,1
     &      ))/8
         ti(ix2,ny+1) = .75d0*tis(ix,nyold+1) + .25d0*tis(ix+1,nyold+1)
         ti(ix2,ny) = 3*(tis(ix ,nyold+1)+tis(ix ,nyold))/8 + (tis(ix+1,
     &      nyold+1)+tis(ix+1,nyold))/8
         phi(ix2,0) = .75d0*phis(ix,0) + .25d0*phis(ip1,0)
         phi(ix2,1) = 3*(phis(ix ,0)+phis(ix ,1))/8 + (phis(ip1,0)+phis(
     &      ip1,1))/8
         phi(ix2,ny+1) = .75d0*phis(ix,nyold+1) + .25d0*phis(ix+1,nyold+
     &      1)
         phi(ix2,ny) = 3*(phis(ix ,nyold+1)+phis(ix ,nyold))/8 + (phis(
     &      ix+1,nyold+1)+phis(ix+1,nyold))/8

         do 23031 igsp = 1, ngsp
            ng(ix2,0,igsp) = .75d0*ngs(ix,0,igsp)+.25d0*ngs(ip1,0,igsp)
            ng(ix2,1,igsp) = 3*(ngs(ix ,0,igsp)+ngs(ix ,1,igsp))/8 + (
     &         ngs(ip1,0,igsp)+ngs(ip1,1,igsp))/8
            ng(ix2,ny+1,igsp) = .75d0*ngs(ix,nyold+1,igsp)+ .25d0*ngs(ix
     &         +1,nyold+1,igsp)
            ng(ix2,ny,igsp) = 3*(ngs(ix ,nyold+1,igsp)+ ngs(ix ,nyold ,
     &         igsp))/8+ (ngs(ix+1,nyold+1,igsp)+ ngs(ix+1,nyold ,igsp))
     &         /8
23031    continue

         do 23033 igsp = 1, ngsp
            tg(ix2,0,igsp) = .75d0*tgs(ix,0,igsp)+.25d0*tgs(ip1,0,igsp)
            tg(ix2,1,igsp) = 3*(tgs(ix ,0,igsp)+tgs(ix ,1,igsp))/8 + (
     &         tgs(ip1,0,igsp)+tgs(ip1,1,igsp))/8
            tg(ix2,ny+1,igsp) = .75d0*tgs(ix,nyold+1,igsp)+ .25d0*tgs(ix
     &         +1,nyold+1,igsp)
            tg(ix2,ny,igsp) = 3*(tgs(ix ,nyold+1,igsp)+ tgs(ix ,nyold ,
     &         igsp))/8+ (tgs(ix+1,nyold+1,igsp)+ tgs(ix+1,nyold ,igsp))
     &         /8
23033    continue

         do 23035 ifld = 1, nisp
            ni(ix2p,0,ifld) = .25d0*nis(ixn,0,ifld)+.75d0*nis(ix+1,0,
     &         ifld)
            ni(ix2p,1,ifld) = (nis(ixn ,0,ifld)+nis(ixn ,1,ifld))/8 + 3*
     &         (nis(ix+1,0,ifld)+nis(ix+1,1,ifld))/8
            ni(ix2p,ny+1,ifld) = .25d0*nis(ixn,nyold+1,ifld) + .75d0*nis
     &         (ix+1,nyold+1,ifld)
            ni(ix2p,ny,ifld) = (nis(ixn ,nyold+1,ifld)+ nis(ixn ,nyold,
     &         ifld))/8+ 3*(nis(ix+1,nyold+1,ifld)+ nis(ix+1,nyold,ifld)
     &         )/8
23035    continue
         do 23037 ifld = 1, nusp
            up(ix2m,0,ifld) = .5d0*(ups(ix,0,ifld)+ups(im1,0,ifld))
            up(ix2m,1,ifld) = .25d0*(ups(ix,0,ifld)+ups(im1,0,ifld)+ ups
     &         (ix,1,ifld)+ups(im1,1,ifld))
            up(ix2m,ny+1,ifld) = .5d0*(ups(ix,nyold+1,ifld) + ups(ix-1,
     &         nyold+1,ifld))
            up(ix2m,ny,ifld) = .25d0*(ups(ix ,nyold+1,ifld)+ ups(ix ,
     &         nyold ,ifld)+ ups(ix-1,nyold+1,ifld)+ ups(ix-1,nyold ,
     &         ifld))
23037    continue
         te(ix2p,0) = .25d0*tes(ixn,0) + .75d0*tes(ix+1,0)
         te(ix2p,1) = (tes(ixn ,0)+tes(ixn ,1))/8 + 3*(tes(ix+1,0)+tes(
     &      ix+1,1))/8
         te(ix2p,ny+1) = .25d0*tes(ixn,nyold+1) + .75d0*tes(ix+1,nyold+1
     &      )
         te(ix2p,ny) = (tes(ixn ,nyold+1)+tes(ixn ,nyold))/8 + 3*(tes(ix
     &      +1,nyold+1)+tes(ix+1,nyold))/8
         ti(ix2p,0) = .25d0*tis(ixn,0) + .75d0*tis(ix+1,0)
         ti(ix2p,1) = (tis(ixn ,0)+tis(ixn ,1))/8 + 3*(tis(ix+1,0)+tis(
     &      ix+1,1))/8
         ti(ix2p,ny+1) = .25d0*tis(ixn,nyold+1) + .75d0*tis(ix+1,nyold+1
     &      )
         ti(ix2p,ny) = (tis(ixn ,nyold+1)+tis(ixn ,nyold))/8 + 3*(tis(ix
     &      +1,nyold+1)+tis(ix+1,nyold))/8
         phi(ix2p,0) = .25d0*phis(ixn,0) + .75d0*phis(ix+1,0)
         phi(ix2p,1) = (phis(ixn ,0)+phis(ixn ,1))/8 + 3*(phis(ix+1,0)+
     &      phis(ix+1,1))/8
         phi(ix2p,ny+1) = .25d0*phis(ixn,nyold+1) + .75d0*phis(ix+1,
     &      nyold+1)
         phi(ix2p,ny) = (phis(ixn ,nyold+1)+phis(ixn ,nyold))/8 + 3*(
     &      phis(ix+1,nyold+1)+phis(ix+1,nyold))/8

         do 23039 igsp = 1, ngsp
            ng(ix2p,0,igsp) = .25d0*ngs(ixn,0,igsp)+.75d0*ngs(ix+1,0,
     &         igsp)
            ng(ix2p,1,igsp) = (ngs(ixn ,0,igsp)+ngs(ixn ,1,igsp))/8 + 3*
     &         (ngs(ix+1,0,igsp)+ngs(ix+1,1,igsp))/8
            ng(ix2p,ny+1,igsp) = .25d0*ngs(ixn ,nyold+1,igsp)+ .75d0*ngs
     &         (ix+1,nyold+1,igsp)
            ng(ix2p,ny,igsp) = (ngs(ixn ,nyold+1,igsp)+ ngs(ixn ,nyold ,
     &         igsp))/8+ 3*(ngs(ix+1,nyold+1,igsp)+ ngs(ix+1,nyold ,igsp
     &         ))/8
23039    continue

         do 23041 igsp = 1, ngsp
            tg(ix2p,0,igsp) = .25d0*tgs(ixn,0,igsp)+.75d0*tgs(ix+1,0,
     &         igsp)
            tg(ix2p,1,igsp) = (tgs(ixn ,0,igsp)+tgs(ixn ,1,igsp))/8 + 3*
     &         (tgs(ix+1,0,igsp)+tgs(ix+1,1,igsp))/8
            tg(ix2p,ny+1,igsp) = .25d0*tgs(ixn ,nyold+1,igsp)+ .75d0*tgs
     &         (ix+1,nyold+1,igsp)
            tg(ix2p,ny,igsp) = (tgs(ixn ,nyold+1,igsp)+ tgs(ixn ,nyold ,
     &         igsp))/8+ 3*(tgs(ix+1,nyold+1,igsp)+ tgs(ix+1,nyold ,igsp
     &         ))/8
23041    continue

  706    continue

c.... finally, reset the corners

      do 23043 ifld = 1, nisp
         ni(0,0,ifld) = nis(0,0,ifld)
         ni(0,ny+1,ifld) = nis(0,nyold+1,ifld)
         ni(nx+1,0,ifld) = nis(nxold+1,0,ifld)
         ni(nx+1,ny+1,ifld) = nis(nxold+1,nyold+1,ifld)
         ni(1,1,ifld) = 0.25d0*(nis(0,0,ifld)+nis(1,0,ifld)+ nis(0,1,
     &      ifld)+nis(1,1,ifld))
         ni(1,ny,ifld) = 0.25d0*(nis(0,nyold+1,ifld)+nis(1,nyold+1,ifld)
     &      + nis(0,nyold ,ifld)+nis(1,nyold ,ifld))
         ni(nx,1,ifld) = 0.25d0*(nis(nxold+1,0,ifld)+nis(nxold,0,ifld)+ 
     &      nis(nxold+1,1,ifld)+nis(nxold,1,ifld))
         ni(nx,ny,ifld) = 0.25d0*(nis(nxold+1,nyold+1,ifld)+ nis(nxold,
     &      nyold+1,ifld)+ nis(nxold+1,nyold ,ifld)+ nis(nxold,nyold ,
     &      ifld))
         ni(1,0,ifld) = 0.5d0*(nis(0,0,ifld)+nis(1,0,ifld))
         ni(0,1,ifld) = 0.5d0*(nis(0,0,ifld)+nis(0,1,ifld))
         ni(nx,0,ifld) = 0.5d0*(nis(nxold+1,0,ifld)+nis(nxold,0,ifld))
         ni(nx+1,1,ifld) = 0.5d0*(nis(nxold+1,0,ifld)+nis(nxold+1,1,ifld
     &      ))
         ni(0,ny,ifld) = 0.5d0*(nis(0,nyold+1,ifld)+nis(0,nyold,ifld))
         ni(1,ny+1,ifld) = 0.5d0*(nis(0,nyold+1,ifld)+nis(1,nyold+1,ifld
     &      ))
         ni(nx,ny+1,ifld) = 0.5d0*(nis(nxold+1,nyold+1,ifld)+ nis(nxold,
     &      nyold+1,ifld))
         ni(nx+1,ny,ifld) = 0.5d0*(nis(nxold+1,nyold+1,ifld)+ nis(nxold+
     &      1,nyold,ifld))
23043 continue
      do 23045 ifld = 1, nusp
         up(0,0,ifld) = ups(0,0,ifld)
         up(0,ny+1,ifld) = ups(0,nyold+1,ifld)
         up(nx+1,0,ifld) = ups(nxold+1,0,ifld)
         up(nx+1,ny+1,ifld) = ups(nxold+1,nyold+1,ifld)
         up(1,1,ifld) = 0.25d0*(ups(0,0,ifld)+ups(1,0,ifld)+ ups(0,1,
     &      ifld)+ups(1,1,ifld))
         up(1,ny,ifld) = 0.25d0*(ups(0,nyold+1,ifld)+ups(1,nyold+1,ifld)
     &      + ups(0,nyold ,ifld)+ups(1,nyold ,ifld))
         up(nx,1,ifld) = .5d0*(ups(nxold,0,ifld)+ups(nxold,1,ifld))
         up(nx,ny,ifld) = .5d0*(ups(nxold,nyold+1,ifld)+ups(nxold,nyold,
     &      ifld))
         up(1,0,ifld) = 0.5d0*(ups(0,0,ifld)+ups(1,0,ifld))
         up(0,1,ifld) = 0.5d0*(ups(0,0,ifld)+ups(0,1,ifld))
         up(nx,0,ifld) = 0.5d0*(ups(nxold+1,0,ifld)+ups(nxold,0,ifld))
         up(nx+1,1,ifld) = 0.5d0*(ups(nxold+1,0,ifld)+ups(nxold+1,1,ifld
     &      ))
         up(0,ny,ifld) = 0.5d0*(ups(0,nyold+1,ifld)+ups(0,nyold,ifld))
         up(1,ny+1,ifld) = 0.5d0*(ups(0,nyold+1,ifld)+ups(1,nyold+1,ifld
     &      ))
         up(nx,ny+1,ifld) = 0.5d0*(ups(nxold+1,nyold+1,ifld)+ ups(nxold,
     &      nyold+1,ifld))
         up(nx+1,ny,ifld) = 0.5d0*(ups(nxold+1,nyold+1,ifld)+ ups(nxold+
     &      1,nyold,ifld))
         up(nx-1,0,ifld) = 0.5d0*(ups(nxold,0,ifld)+ups(nxold-1,0,ifld))
         up(nx-1,1,ifld) = 0.25d0*(ups(nxold,0,ifld)+ups(nxold-1,0,ifld)
     &      + ups(nxold,1,ifld)+ups(nxold-1,1,ifld))
         up(nx-1,ny+1,ifld) = .5d0*(ups(nxold ,nyold+1,ifld) + ups(nxold
     &      -1,nyold+1,ifld))
         up(nx-1,ny,ifld) = .25d0*(ups(nxold ,nyold+1,ifld) + ups(nxold-
     &      1,nyold+1,ifld) + ups(nxold ,nyold ,ifld) + ups(nxold-1,
     &      nyold ,ifld))
23045 continue
      te(0,0) = tes(0,0)
      te(0,ny+1) = tes(0,nyold+1)
      te(nx+1,0) = tes(nxold+1,0)
      te(nx+1,ny+1) = tes(nxold+1,nyold+1)
      te(1,1) = 0.25d0*(tes(0,0)+tes(1,0)+tes(0,1)+tes(1,1))
      te(1,ny) = 0.25d0*(tes(0,nyold+1)+tes(1,nyold+1)+ tes(0,nyold )+
     &   tes(1,nyold ))
      te(nx,1) = 0.25d0*(tes(nxold+1,0)+tes(nxold,0)+ tes(nxold+1,1)+tes
     &   (nxold,1))
      te(nx,ny) = 0.25d0*(tes(nxold+1,nyold+1)+tes(nxold,nyold+1)+ tes(
     &   nxold+1,nyold )+tes(nxold,nyold ))
      te(1,0) = 0.5d0*(tes(0,0)+tes(1,0))
      te(0,1) = 0.5d0*(tes(0,0)+tes(0,1))
      te(nx,0) = 0.5d0*(tes(nxold+1,0)+tes(nxold,0))
      te(nx+1,1) = 0.5d0*(tes(nxold+1,0)+tes(nxold+1,1))
      te(0,ny) = 0.5d0*(tes(0,nyold+1)+tes(0,nyold))
      te(1,ny+1) = 0.5d0*(tes(0,nyold+1)+tes(1,nyold+1))
      te(nx,ny+1) = 0.5d0*(tes(nxold+1,nyold+1)+tes(nxold,nyold+1))
      te(nx+1,ny) = 0.5d0*(tes(nxold+1,nyold+1)+tes(nxold+1,nyold))
      ti(0,0) = tis(0,0)
      ti(0,ny+1) = tis(0,nyold+1)
      ti(nx+1,0) = tis(nxold+1,0)
      ti(nx+1,ny+1) = tis(nxold+1,nyold+1)
      ti(1,1) = 0.25d0*(tis(0,0)+tis(1,0)+tis(0,1)+tis(1,1))
      ti(1,ny) = 0.25d0*(tis(0,nyold+1)+tis(1,nyold+1)+ tis(0,nyold )+
     &   tis(1,nyold ))
      ti(nx,1) = 0.25d0*(tis(nxold+1,0)+tis(nxold,0)+ tis(nxold+1,1)+tis
     &   (nxold,1))
      ti(nx,ny) = 0.25d0*(tis(nxold+1,nyold+1)+tis(nxold,nyold+1)+ tis(
     &   nxold+1,nyold )+tis(nxold,nyold ))
      ti(1,0) = 0.5d0*(tis(0,0)+tis(1,0))
      ti(0,1) = 0.5d0*(tis(0,0)+tis(0,1))
      ti(nx,0) = 0.5d0*(tis(nxold+1,0)+tis(nxold,0))
      ti(nx+1,1) = 0.5d0*(tis(nxold+1,0)+tis(nxold+1,1))
      ti(0,ny) = 0.5d0*(tis(0,nyold+1)+tis(0,nyold))
      ti(1,ny+1) = 0.5d0*(tis(0,nyold+1)+tis(1,nyold+1))
      ti(nx,ny+1) = 0.5d0*(tis(nxold+1,nyold+1)+tis(nxold,nyold+1))
      ti(nx+1,ny) = 0.5d0*(tis(nxold+1,nyold+1)+tis(nxold+1,nyold))
      phi(0,0) = phis(0,0)
      phi(0,ny+1) = phis(0,nyold+1)
      phi(nx+1,0) = phis(nxold+1,0)
      phi(nx+1,ny+1) = phis(nxold+1,nyold+1)
      phi(1,1) = 0.25d0*(phis(0,0)+phis(1,0)+phis(0,1)+phis(1,1))
      phi(1,ny) = 0.25d0*(phis(0,nyold+1)+phis(1,nyold+1)+ phis(0,nyold 
     &   )+phis(1,nyold ))
      phi(nx,1) = 0.25d0*(phis(nxold+1,0)+phis(nxold,0)+ phis(nxold+1,1)
     &   +phis(nxold,1))
      phi(nx,ny) = 0.25d0*(phis(nxold+1,nyold+1)+phis(nxold,nyold+1)+ 
     &   phis(nxold+1,nyold )+phis(nxold,nyold ))
      phi(1,0) = 0.5d0*(phis(0,0)+phis(1,0))
      phi(0,1) = 0.5d0*(phis(0,0)+phis(0,1))
      phi(nx,0) = 0.5d0*(phis(nxold+1,0)+phis(nxold,0))
      phi(nx+1,1) = 0.5d0*(phis(nxold+1,0)+phis(nxold+1,1))
      phi(0,ny) = 0.5d0*(phis(0,nyold+1)+phis(0,nyold))
      phi(1,ny+1) = 0.5d0*(phis(0,nyold+1)+phis(1,nyold+1))
      phi(nx,ny+1) = 0.5d0*(phis(nxold+1,nyold+1)+phis(nxold,nyold+1))
      phi(nx+1,ny) = 0.5d0*(phis(nxold+1,nyold+1)+phis(nxold+1,nyold))

      do 23047 igsp = 1, ngsp
         ng(0,0,igsp) = ngs(0,0,igsp)
         ng(0,ny+1,igsp) = ngs(0,nyold+1,igsp)
         ng(nx+1,0,igsp) = ngs(nxold+1,0,igsp)
         ng(nx+1,ny+1,igsp) = ngs(nxold+1,nyold+1,igsp)
         ng(1,1,igsp) = 0.25d0*(ngs(0,0,igsp)+ngs(1,0,igsp)+ ngs(0,1,
     &      igsp)+ngs(1,1,igsp))
         ng(1,ny,igsp) = 0.25d0*(ngs(0,nyold+1,igsp)+ngs(1,nyold+1,igsp)
     &      + ngs(0,nyold ,igsp)+ngs(1,nyold ,igsp))
         ng(nx,1,igsp) = 0.25d0*(ngs(nxold+1,0,igsp)+ngs(nxold,0,igsp)+ 
     &      ngs(nxold+1,1,igsp)+ngs(nxold,1,igsp))
         ng(nx,ny,igsp) = 0.25d0*(ngs(nxold+1,nyold+1,igsp)+ ngs(nxold,
     &      nyold+1,igsp)+ ngs(nxold+1,nyold ,igsp)+ ngs(nxold,nyold ,
     &      igsp))
         ng(1,0,igsp) = 0.5d0*(ngs(0,0,igsp)+ngs(1,0,igsp))
         ng(0,1,igsp) = 0.5d0*(ngs(0,0,igsp)+ngs(0,1,igsp))
         ng(nx,0,igsp) = 0.5d0*(ngs(nxold+1,0,igsp)+ngs(nxold,0,igsp))
         ng(nx+1,1,igsp) = 0.5d0*(ngs(nxold+1,0,igsp)+ngs(nxold+1,1,igsp
     &      ))
         ng(0,ny,igsp) = 0.5d0*(ngs(0,nyold+1,igsp)+ngs(0,nyold,igsp))
         ng(1,ny+1,igsp) = 0.5d0*(ngs(0,nyold+1,igsp)+ngs(1,nyold+1,igsp
     &      ))
         ng(nx,ny+1,igsp) = 0.5d0*(ngs(nxold+1,nyold+1,igsp)+ ngs(nxold,
     &      nyold+1,igsp))
         ng(nx+1,ny,igsp) = 0.5d0*(ngs(nxold+1,nyold+1,igsp)+ ngs(nxold+
     &      1,nyold,igsp))
23047 continue

      do 23049 igsp = 1, ngsp
         tg(0,0,igsp) = tgs(0,0,igsp)
         tg(0,ny+1,igsp) = tgs(0,nyold+1,igsp)
         tg(nx+1,0,igsp) = tgs(nxold+1,0,igsp)
         tg(nx+1,ny+1,igsp) = tgs(nxold+1,nyold+1,igsp)
         tg(1,1,igsp) = 0.25d0*(tgs(0,0,igsp)+tgs(1,0,igsp)+ tgs(0,1,
     &      igsp)+tgs(1,1,igsp))
         tg(1,ny,igsp) = 0.25d0*(tgs(0,nyold+1,igsp)+tgs(1,nyold+1,igsp)
     &      + tgs(0,nyold ,igsp)+tgs(1,nyold ,igsp))
         tg(nx,1,igsp) = 0.25d0*(tgs(nxold+1,0,igsp)+tgs(nxold,0,igsp)+ 
     &      tgs(nxold+1,1,igsp)+tgs(nxold,1,igsp))
         tg(nx,ny,igsp) = 0.25d0*(tgs(nxold+1,nyold+1,igsp)+ tgs(nxold,
     &      nyold+1,igsp)+ tgs(nxold+1,nyold ,igsp)+ tgs(nxold,nyold ,
     &      igsp))
         tg(1,0,igsp) = 0.5d0*(tgs(0,0,igsp)+tgs(1,0,igsp))
         tg(0,1,igsp) = 0.5d0*(tgs(0,0,igsp)+tgs(0,1,igsp))
         tg(nx,0,igsp) = 0.5d0*(tgs(nxold+1,0,igsp)+tgs(nxold,0,igsp))
         tg(nx+1,1,igsp) = 0.5d0*(tgs(nxold+1,0,igsp)+tgs(nxold+1,1,igsp
     &      ))
         tg(0,ny,igsp) = 0.5d0*(tgs(0,nyold+1,igsp)+tgs(0,nyold,igsp))
         tg(1,ny+1,igsp) = 0.5d0*(tgs(0,nyold+1,igsp)+tgs(1,nyold+1,igsp
     &      ))
         tg(nx,ny+1,igsp) = 0.5d0*(tgs(nxold+1,nyold+1,igsp)+ tgs(nxold,
     &      nyold+1,igsp))
         tg(nx+1,ny,igsp) = 0.5d0*(tgs(nxold+1,nyold+1,igsp)+ tgs(nxold+
     &      1,nyold,igsp))
23049 continue

c...  If this is a double-null case, we must adjust the values across
c...  the cut at nxc

      if (((geometry.eq.'dnbot').or.(geometry.eq.'dnXtarget')) .and. nxc
     &   .gt.0) then


         ix2 = nxc
         ix2p = ix2 + 1
         ix2m = max(ix2-1,0)
         do 910 iy = 0, ny+1
            do 902 ifld = 1, nisp
               ni(ix2 ,iy,ifld) = ni(ix2m ,iy,ifld)
               ni(ix2p,iy,ifld) = ni(ix2p+1,iy,ifld)
  902          continue
            do 903 ifld = 1, nusp
               up(ix2m,iy,ifld) = 0.d0
               up(ix2 ,iy,ifld) = 0.d0
               up(ix2p,iy,ifld) = 0.d0
  903          continue

            te(ix2 ,iy) = te(ix2m ,iy)
            te(ix2p,iy) = te(ix2p+1,iy)
            ti(ix2 ,iy) = ti(ix2m ,iy)
            ti(ix2p,iy) = ti(ix2p+1,iy)
            phi(ix2 ,iy) = phi(ix2m ,iy)
            phi(ix2p,iy) = phi(ix2p+1,iy)

            do 904 igsp = 1, ngsp
               ng(ix2,iy,igsp) = ng(ix2m,iy,igsp)
               ng(ix2p,iy,igsp) = ng(ix2p+1,iy,igsp)
  904          continue
            do 23055 igsp = 1, ngsp
               tg(ix2,iy,igsp) = tg(ix2m,iy,igsp)
               tg(ix2p,iy,igsp) = tg(ix2p+1,iy,igsp)
23055       continue
  910       continue

      endif

      return
      end
c****** end of subroutine refpla ***
c***********************************
c -----------------------------------------------------------------------
      subroutine grdintpy (ixs,ixf,ixos,ixof,iys,iyf,iyos,iyof,nx,ny, 
     &   nxold,nyold,xn,yn,xno,yno,xny,yny,indxx,indxy)
cProlog

c...  This subroutine calculates the "intermediate" mesh that has nxold
c...  poloidal points and ny radial points. Linear interpolation is used
c...  to find the intersections of the old mesh radial lines with the
c...  new mesh poloidal lines. This intermediate mesh is then used to
c...  interpolate variables in the radial direction to the new mesh, but at
c...  the old poloidal points. Subsequently, a poloidal interpolation it done.

c...  The input variables:
c...  ixs    -- initial poloidal index for new mesh
c...  ixf    -- final poloidal index for new mesh
c...  ixos   -- initial poloidal index for old mesh
c...  ixof   -- final poloidal index for old mesh
c...  iys    -- initial radial index for new mesh
c...  iyf    -- final radial index for new mesh
c...  iyos   -- initial radial index for old mesh
c...  iyof   -- final radial index for old mesh
c...  nx     -- total poloidal mesh size for new mesh
c...  ny     -- total radial mesh size for new mesh
c...  nxold  -- total poloidal mesh size for old mesh
c...  nyold  -- total radial mesh size for old mesh
c...  xn     -- normalized poloidal location for new mesh (nx,ny)
c...  yn     -- normalized radial location for new mesh (nx,ny)
c...  xno    -- normalized poloidal location for old mesh (nxold,nyold)
c...  yno    -- normalized radial location for old mesh (nxold,nyold)

c...  The output variables:
c...  xny    -- calculated poloidal location for intermediate mesh (nxold,ny)
c...  yny    -- calculated radial location for intermediate mesh (nxold,ny)
c...  indxx  -- poloidal index ixo used in constructing intermediate mesh
c...  indxy  -- radial index iy used in constructing intermediate mesh

      implicit none

c --  Input variables
      integer ixs,ixf,ixos,ixof,iys,iyf,iyos,iyof,nx,ny,nxold,nyold
      doubleprecision xn(0:nx+1,0:ny+1), yn(0:nx+1,0:ny+1), xno(0:nxold+
     &   1,0:nyold+1), yno(0:nxold+1,0:nyold+1)

c --  Output variables
      doubleprecision xny(0:nxold+1,0:ny+1), yny(0:nxold+1,0:ny+1)
      integer indxx(0:nxold+1,0:ny+1), indxy(0:nxold+1,0:ny+1)

c --  Local variables
ccc   integer ix,iyo
ccc   real d2
      integer iy,ixo,ixm,ixmp,iyom,iyomp,icount
      doubleprecision spn,spo,xxn,yyn,d2min,smalln,almost1,delerr,ferr
      data smalln /1.d-07/, almost1 /9.9999d-01/, delerr /1.d-02/

c...  This routine searchs for the (ix,iyo) indice pair the gives a point
c...  on the new grid (xn,yn) that is closest to the old grid point
c...  (xno,yno) for a give (ixo,iy), i.e., the intermediate grid indices

      iyom = iyos
      do 90 iy = iys, iyf
         ixm = ixs
         do 80 ixo = ixos, ixof
            d2min = 1.d20

c...  Search for the closest point of old and new mesh for specific ixo,iy
c...  After the closest point, we must search for the points that straddle
cc            do 70 iyo = iyos, iyof
cc               do 60 ix = ixs, ixf
cc                  d2 = (xno(ixo,iyo) - xn(ix,iy))**2 +
cc     .                 (yno(ixo,iyo) - yn(ix,iy))**2
cc                  if (d2 .lt. d2min) then
cc                     d2min = d2
cc                     ixm = ix
cc                     iyom = iyo
cc                  endif
cc  60           continue
cc  70        continue
            if (ixm .eq. ixs) then
               ixmp = ixm + 1
            elseif (ixm .eq. ixf) then
               ixmp = ixm
               ixm = ixm - 1
            elseif (xn(ixm,iy) .ge. xno(ixo,iyom)) then
               ixmp = ixm
               ixm = ixm - 1
            else
               ixmp = ixm + 1
            endif
            if (iyom .eq. iyos) then
               iyomp = iyom + 1
            elseif (iyom .eq. iyof) then
               iyomp = iyom
               iyom = iyom - 1
            elseif (yno(ixo,iyom) .ge. yn(ixm,iy)) then
               iyomp = iyom
               iyom = iyom - 1
            else
               iyomp = iyom + 1
            endif

c...  Special case for xno = 0,1; yyn could be more general if xn.ne.0,1
            icount = 0
   72       continue
            icount = icount + 1
            if (icount .gt. 500) then
               call remark(
     &            '***** grdinty cannot find straddling gridpoints, chec
     &k vel. grd at nx')
               write(*,*) 'ixo,iy,ixm,iyom = ',ixo,iy,ixm,iyom, 
     &            '  ixf,ixof,iyf,iyof = ',ixf,ixof,iyf,iyof
               call xerrab("")
            endif
            if (abs(xno(ixo,iyomp)-xno(ixo,iyom)) .lt. smalln) then
               xxn = xno(ixo,iyom)
               yyn = ( yn(ixm ,iy)*( xn(ixmp,iy )-xno(ixo,iyom)) + yn(
     &            ixmp,iy)*(xno(ixo ,iyom)- xn(ixm,iy )) ) / (xn(ixmp,iy
     &            )-xn(ixm,iy))
c...  Special if test prevents prob for vel. grid for nx pt.
               if (xxn.gt.almost1 .and. ixm.eq.ixf-1) yyn = yn(ixmp,iy)
            else
               spo = (yno(ixo,iyomp) - yno(ixo,iyom)) / (xno(ixo,iyomp) 
     &            - xno(ixo,iyom))
               spn = (yn(ixmp,iy) - yn(ixm,iy)) / (xn(ixmp,iy) - xn(ixm,
     &            iy))
               xxn = (spn*xn(ixm,iy) - spo*xno(ixo,iyom) + yno(ixo,iyom) 
     &            - yn(ixm,iy)) / (spn - spo +1d-200)
               yyn = yno(ixo,iyom) + spo*(xxn - xno(ixo,iyom))
            endif
c...  Verify that old grid pts nearly straddle new grd pt, or try again
            ferr = delerr*( yno(ixo,iyomp)-yno(ixo,iyom) )
            if (yyn.ge.yno(ixo,iyom)-ferr .and. yyn.le.yno(ixo,iyomp)+
     &         ferr) goto 74
            if (yyn .lt. yno(ixo,iyom)) then
               if (iyom .eq. iyos) goto 74
               iyom = iyom - 1
               iyomp = iyom + 1
            else
               if (iyom .eq. iyof-1) goto 74
               iyom = iyom + 1
               iyomp = iyom + 1
            endif
            goto 72
   74       continue
            ferr = delerr*( xn(ixmp,iy)-xn(ixm,iy) )
            if (xxn.ge.xn(ixm,iy)-ferr .and. xxn.le.xn(ixmp,iy)+ferr) 
     &            goto 76
c...  Special if test prevents prob for vel. grid for nx pt.
            if (xxn.gt.almost1 .and. ixm.eq.ixf-1) goto 76
            if (xxn .lt. xn(ixm,iy)) then
               if (ixm .eq. ixs) goto 76
               ixm = ixm - 1
               ixmp = ixm + 1
            else
               if (ixm .eq. ixf-1) goto 76
               ixm = ixm + 1
               ixmp = ixm + 1
            endif
            goto 72
   76       continue

            xny(ixo,iy) = xxn
            yny(ixo,iy) = yyn
            indxx(ixo,iy) = ixm
            indxy(ixo,iy) = iyom

   80       continue
   90    continue

      return
      end
c **** end of subroutine grdintpy ****
c ************************************
c -----------------------------------------------------------------------
      subroutine intpvar (varo, varn, ivel, nnxold, nnyold)
cProlog

c...  This subroutine does the combined radial and poloidal interpolation
c...  of the variable varo

      implicit none

c  -- Common blocks
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nx,ny,nisp,ngsp(for arrays in Interp not used)]
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
c geometry,nxc,nyomitmx
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
c xnrm,xvnrm
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
c ixlb,ixpt1,ixpt2,ixrb,iysptrx
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
c ixlbo,ixpt1o,ixpt2o,ixrbo,iysptrxo,
c xnrmox,xvnrmox,ynrmox,yvnrmox,ynrmo,yvnrmo,
c xnrmnx,xvnrmnx,ynrmnx,yvnrmnx,wrkint,wrkint2

c  -- Input variables - vel. grid switch, mesh sizes, variable on old mesh
      integer ivel, nnxold, nnyold
      doubleprecision varo(0:nnxold+1,0:nnyold+1)

c  -- Output variables - variable on new mesh
      doubleprecision varn(0:nx+1,0:ny+1)

c  -- Local variables
      integer iy, ix2, ix2p, ix2m, ixxst, ixxsto, iyst, iysto, ixxend, 
     &   ixxendo, iyend, iyendo, jx, ir

c...  Set double null indices
      ix2 = nxc
      ix2p = ix2 + 1
      ix2m = max(ix2-1,0)

c...  If ivel=0, use xnrm grid; if ivel=1, use xvnrm grid
c##########################################################
      if (ivel.eq.0) then
c Do the density mesh; very large ivel if-test
c##########################################################

c...  First we do the radial linear interpolation for two regions for
c...  first intermediate mesh (xnrmox,ynrmox)
         if (iysptrx .gt. 0) then
            iyend = iysptrx
            iyendo = iysptrxo
            if (nyomitmx .ge. nysol(1)+nyout(1)) then
               iyend = iysptrx+1
               iyendo = iysptrxo+1
            endif
            call radintp (0,iyend,0,iyendo,0,nnxold+1, nx,ny,nnxold,
     &         nnyold,ynrmox,ynrmo,varo,wrkint)
         endif
         iyst = iysptrx + 1
         iysto = iysptrxo + 1
         if (iysptrx .eq. 0) iyst = 0
         if (iysptrxo .eq. 0) iysto = 0
         if (nyomitmx .lt. nysol(1)+nyout(1)) then
            call radintp (iyst,ny+1,iysto,nnyold+1,0,nnxold+1, nx,ny,
     &         nnxold,nnyold,ynrmox,ynrmo,varo,wrkint)
         endif

c...  Now do poloidal interpolation using radial result in wrkint from
c...  first intermediate mesh to second intermediate mesh (xnrmnx,ynrmnx)
         do 23000 ir = 1, 3*nxpt
            call polintp (ixst(ir),ixend(ir),ixsto(ir),ixendo(ir),0,ny+1
     &         , nx,ny,nnxold,nnyold,xnrmnx,xnrmox,wrkint,wrkint2)
23000    continue

c...  Next do radial interpolation using wrkint2 on second intermediate
c...  mesh to the final mesh (xnrm,ynrm); result is varn
         if (iysptrx .gt. 0) then
            iyend = iysptrx
            if (nyomitmx .ge. nysol(1)+nyout(1)) then
               iyend = iysptrx+1
            endif
            call radintp (0,iyend,0,iyend,0,nx+1, nx,ny,nx,ny,ynrm,
     &         ynrmnx,wrkint2,varn)
         endif
         iyst = iysptrx + 1
         if (iysptrx .eq. 0) iyst = 0
         if (nyomitmx .lt. nysol(1)+nyout(1)) then
            call radintp (iyst,ny+1,iyst,ny+1,0,nx+1, nx,ny,nx,ny,ynrm,
     &         ynrmnx,wrkint2,varn)
         endif

c...  Last, fix midway boundaries for double null case
         if (((geometry.eq.'dnbot').or.(geometry.eq.'dnXtarget')) .and. 
     &      nxc.gt.1) then
            do 20 iy = 0, ny+1
               varn(ix2 ,iy) = varn(ix2m ,iy)
               varn(ix2p,iy) = varn(ix2p+1,iy)
   20          continue
         endif
c     End of the density mesh calculation

c...  This next case is for ivel=1, i.e., the parallel velocity equation
c##################################################
c now if ivel=1, branch of large ivel if-test
      else
c##################################################
c...   First do the radial interpolation
         if (iysptrx .gt. 0) then
            iyend = iysptrx
            iyendo = iysptrxo
            if (nyomitmx .ge. nysol(1)+nyout(1)) then
               iyend = iysptrx+1
               iyendo = iysptrxo+1
            endif
            call radintp (0,iyend,0,iyendo,0,nnxold+1, nx,ny,nnxold,
     &         nnyold,yvnrmox,yvnrmo,varo,wrkint)
         endif
         iyst = iysptrx + 1
         iysto = iysptrxo + 1
         if (iysptrx .eq. 0) iyst = 0
         if (iysptrxo .eq. 0) iysto = 0
         if (nyomitmx .lt. nysol(1)+nyout(1)) then
            call radintp (iyst,ny+1,iysto,nnyold+1,0,nnxold+1, nx,ny,
     &         nnxold,nnyold,yvnrmox,yvnrmo,varo,wrkint)
         endif

c...  poloidal interpolation for velocity grid
         do 23003 ir = 1, 3*nxpt
            call polintp (ixst(ir),ixend(ir),ixsto(ir),ixendo(ir),0,ny+1
     &         , nx,ny,nnxold,nnyold,xvnrmnx,xvnrmox,wrkint,wrkint2)
23003    continue

c...  Next do radial interpolation using wrkint2 on second intermediate
c...  mesh to the final mesh (xvnrm,yvnrm); result is varn
         if (iysptrx .gt. 0) then
            iyend = iysptrx
            if (nyomitmx .ge. nysol(1)+nyout(1)) then
               iyend = iysptrx+1
            endif
            call radintp (0,iyend,0,iyend,0,nx+1, nx,ny,nx,ny,yvnrm,
     &         yvnrmnx,wrkint2,varn)
         endif
         iyst = iysptrx + 1
         if (iysptrx .eq. 0) iyst = 0
         if (nyomitmx .lt. nysol(1)+nyout(1)) then
            call radintp (iyst,ny+1,iyst,ny+1,0,nx+1, nx,ny,nx,ny,yvnrm,
     &         yvnrmnx,wrkint2,varn)
         endif

c...  Last, fix midway boundaries for double null case
         if (((geometry.eq.'dnbot').or.(geometry.eq.'dnXtarget')) .and. 
     &      nxc.gt.0) then
            do 40 iy = 0, ny+1
               varn(ix2m,iy) = 0.d0
               varn(ix2 ,iy) = 0.d0
               varn(ix2p,iy) = 0.d0
   40          continue
         endif

c###############################################
      endif
c end of large ivel if-test
c###############################################
      return
      end
c ***** end of subroutine intpvar ****
c ************************************
c ----------------------------------------------------------------------
      subroutine radintp (iys,iyf,iyos,iyof,ixs,ixf,nx,ny,nxold,nyold, 
     &   yn,yo,varo,varn)
cProlog

cccMER Note that argument nx is not used in subroutine radintp

c...  This subroutine does a linear interpolation in the radial direction
c...  but with the old poloidal mesh structure

      implicit none

c --  Input variables
      integer iys,iyf,iyos,iyof,ixs,ixf,nx,ny,nxold,nyold
      doubleprecision yn(0:nxold+1,0:ny+1), yo(0:nxold+1,0:nyold+1), 
     &   varo(0:nxold+1,0:nyold+1)

c --  Output variables
      doubleprecision varn(0:nxold+1,0:ny+1)

c --  Local variables
      integer ix, iy, iyo, iyl
      doubleprecision chng, avn, avo
      data chng/1.7d0/

      do 40 iy = iys, iyf
         do 30 ix = ixs, ixf
            iyl = iyos
            do 20 iyo = iyos, iyof
               if (yo(ix,iyo).gt.yn(ix,iy) .or. iyo.eq.iyof) goto 25
               iyl = iyo
   20          continue
   25       continue
            varn(ix,iy) = (varo(ix,iyl )*(yo(ix,iyl+1)-yn(ix,iy )) + 
     &         varo(ix,iyl+1)*(yn(ix,iy )-yo(ix,iyl))) / (yo(ix,iyl+1)-
     &         yo(ix,iyl))
c ...    check for extrapolation and limit change to chng
            if (yn(ix,iy) .lt. yo(ix,iyl)) then
               avn = abs(varn(ix,iy))
               avo = abs(varo(ix,iyl))
               if ( avn .lt. avo ) then
                  avn = max(avn, avo/chng)
               else
                  avn = min(avn, avo*chng)
               endif
               varn(ix,iy) = sign (avn, varo(ix,iyl))
            endif
            if (yn(ix,iy) .gt. yo(ix,iyl+1)) then
               avn = abs(varn(ix,iy))
               avo = abs(varo(ix,iyl+1))
               if ( avn .lt. avo ) then
                  avn = max(avn, avo/chng)
               else
                  avn = min(avn, avo*chng)
               endif
               varn(ix,iy) = sign (avn, varo(ix,iyl+1))
            endif
   30       continue
   40    continue

      return
      end
c **** end of subroutine radintp ****
c **********************************
c -------------------------------------------------------------------
      subroutine polintp (ixs,ixf,ixos,ixof,iys,iyf,nx,ny,nxold,nyold, 
     &   xn,xo,varo,varn)
cProlog

c...  This subroutine does the poloidal interpolation using the result
c...  of the radial interpolation on the new radial mesh

      implicit none

c --  Input variables
      integer ixs,ixf,ixos,ixof,iys,iyf,nx,ny,nxold,nyold
      doubleprecision xn(0:nx+1,0:ny+1), xo(0:nxold+1,0:ny+1), varo(0:
     &   nxold+1,0:ny+1)

c --  Output variables
      doubleprecision varn(0:nx+1,0:ny+1)

c --  Local variables
      integer ix, iy, ixo, ixl
      doubleprecision chng, avn, avo
      data chng/1.7d0/

      do 40 ix = ixs, ixf
         do 30 iy = iys, iyf
            ixl = ixos
            do 30 ixo = ixos, ixof
               if (xo(ixo,iy).gt.xn(ix,iy) .or. ixo.eq.ixof) goto 25
               ixl = ixo
   20          continue
   25          continue
               varn(ix,iy) = (varo(ixl ,iy)*(xo(ixl+1,iy)-xn(ix ,iy)) + 
     &            varo(ixl+1,iy)*(xn(ix ,iy)-xo(ixl,iy))) / (xo(ixl+1,iy
     &            )-xo(ixl,iy))
c ...    check for extrapolation and limit change to chng
               if (xn(ix,iy) .lt. xo(ixl,iy)) then
                  avn = abs(varn(ix,iy))
                  avo = abs(varo(ixl,iy))
                  if ( avn .lt. avo ) then
                     avn = max(avn, avo/chng)
                  else
                     avn = min(avn, avo*chng)
                  endif
                  varn(ix,iy) = sign (avn, varo(ixl,iy))
               endif
               if (xn(ix,iy) .gt. xo(ixl+1,iy)) then
                  avn = abs(varn(ix,iy))
                  avo = abs(varo(ixl+1,iy))
                  if ( avn .lt. avo ) then
                     avn = max(avn, avo/chng)
                  else
                     avn = min(avn, avo*chng)
                  endif
                  varn(ix,iy) = sign (avn, varo(ixl+1,iy))
               endif
   30          continue
   40    continue

      return
      end
c ***** end of subroutine polintp ****

