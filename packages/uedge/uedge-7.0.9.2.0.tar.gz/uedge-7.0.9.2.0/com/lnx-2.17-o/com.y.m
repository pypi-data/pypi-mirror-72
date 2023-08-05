      subroutine cominit0
c initializes a Package
      integer drtdm
      common /comrtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("com")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call comdata
      call comwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_com],[
Use(OMFIT)
Use(COMroutines)
Use(Dim)
Use(Dimflxgrd)
Use(Comflxgrd)
Use(Aeqflxgrd)
Use(RZ_grid_info)
Use(RZ_grid_global)
Use(Share)
Use(Xpoint_indices)
Use(Cut_indices)
Use(Comgeo)
Use(Comgeo_g)
Use(Noggeo)
Use(Timing)
Use(Linkbbb)
Use(Timespl)
Use(Limiter)
Use(Multicharge)
Use(Fitdata)
Use(Subs2)
])
      block data comiyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_com
      data iomfit/1/
      data nx/8/,ny/4/,nxm/8/,nym/4/,nxpt/1/,nhsp/1/,nzsp/5*0/
      data nzspmx/10/,nisp/1/,ngsp/1/,nhgsp/1/,imx/50/,imy/40/,lnst/43/
      data num_elem/0/
      data noregs/2/
      data isfw/0/,kxord/4/,kyord/4/,geqdskfname/'neqdsk'/
      data mco2v/3/,mco2r/1/,nsilop/41/,magpri/60/,nfcoil/18/,nesum/2/
      data aeqdskfname/'aeqdsk'/
      data nycore/30*0/,nysol/30*2/,nyout/30*0/,nxleg/0,59*2/
      data nxcore/0,59*4/,nxomit/0/,nyomitmx/0/,igrid/1/
      data geometry/"snull"/,nxc/4/,ismpsym/0/,isudsym/0/,islimon/0/
      data iy_lims/9999/,theta_split/1.570796326794896/,isnonog/0/
      data ismmon/0/,isoldgrid/0/,isgrdsym/0/,cutlo/1.e-300/
      data epslon/1e-6/,spheromak/0/,isfrc/0/,ishalfm/0/,isbphicon/0/
      data nhdf/1/,hdfilename/12*'b2frates'/,nzdf/1/
      data mcfilename/12*'b2frates'/,coronalimpfname/'mist.dat'/
      data istabon/7/,reset_core_og/0/
      data dxmin/1.e-20/
      data istimingon/1/,iprinttim/0/,ttotfe/0./,ttimpfe/0./,ttotjf/0./
      data ttimpjf/0./,ttmatfac/0./,ttmatsol/0./,ttjstor/0./
      data ttjrnorm/0./,ttjreorder/0./,ttimpc/0./,tstart/0./,tend/0./
      data ttnpg/0./,ttngxlog/0./,ttngylog/0./,ttngfd2/0./,ttngfxy/0./
      data totb2val/0./,totintrv/0./
      data dslims/.0001/
      data ntev/101/,nz/2/,iscxfit/1./,isrtndep/1/,mcfformat/12*0/
      data ispradextrap/0/
      data isprof_coef/0/,ncoefne_tanh/1/,ncoefte_tanh/1/,numt_bs/1/
      data numc_bs/1/,numk_bs/1/,fitfrac1/1./,isdatfmtnew/1/
      data psishift/0./,isdndtfitdat/0/,ifitset/1/
      data tim_interval_fit/3.e-2/,tim_chng_max/1./,isprofvspsi/1/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine comdata
Use_All_Groups_com
      external comiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(xold))
      call clraddr(Point(yold))
      call clraddr(Point(fold))
      call clraddr(Point(workk))
      call clraddr(Point(fpol))
      call clraddr(Point(pres))
      call clraddr(Point(qpsi))
      call clraddr(Point(rbdry))
      call clraddr(Point(zbdry))
      call clraddr(Point(xlim))
      call clraddr(Point(ylim))
      call clraddr(Point(bscoef))
      call clraddr(Point(xknot))
      call clraddr(Point(yknot))
      call clraddr(Point(work))
      call clraddr(Point(xcurve))
      call clraddr(Point(ycurve))
      call clraddr(Point(npoint))
      call clraddr(Point(rco2v))
      call clraddr(Point(dco2v))
      call clraddr(Point(rco2r))
      call clraddr(Point(dco2r))
      call clraddr(Point(csilop))
      call clraddr(Point(cmpr2))
      call clraddr(Point(ccbrsp))
      call clraddr(Point(eccurt))
      call clraddr(Point(rm))
      call clraddr(Point(zm))
      call clraddr(Point(rmt))
      call clraddr(Point(zmt))
      call clraddr(Point(rv))
      call clraddr(Point(zv))
      call clraddr(Point(psi))
      call clraddr(Point(br))
      call clraddr(Point(bz))
      call clraddr(Point(bpol))
      call clraddr(Point(bphi))
      call clraddr(Point(b))
      call clraddr(Point(bsqr))
      call clraddr(Point(b12))
      call clraddr(Point(b12ctr))
      call clraddr(Point(b32))
      call clraddr(Point(rmg))
      call clraddr(Point(zmg))
      call clraddr(Point(psig))
      call clraddr(Point(brg))
      call clraddr(Point(bzg))
      call clraddr(Point(bpolg))
      call clraddr(Point(bphig))
      call clraddr(Point(bg))
      call clraddr(Point(ixlb))
      call clraddr(Point(ixpt1))
      call clraddr(Point(ixmdp))
      call clraddr(Point(ixpt2))
      call clraddr(Point(ixrb))
      call clraddr(Point(iysptrx1))
      call clraddr(Point(iysptrx2))
      call clraddr(Point(vol))
      call clraddr(Point(gx))
      call clraddr(Point(gy))
      call clraddr(Point(dx))
      call clraddr(Point(dxvf))
      call clraddr(Point(dy))
      call clraddr(Point(gxf))
      call clraddr(Point(gxfn))
      call clraddr(Point(gyf))
      call clraddr(Point(gxc))
      call clraddr(Point(gyc))
      call clraddr(Point(xnrm))
      call clraddr(Point(xvnrm))
      call clraddr(Point(ynrm))
      call clraddr(Point(yvnrm))
      call clraddr(Point(sx))
      call clraddr(Point(sxnp))
      call clraddr(Point(sy))
      call clraddr(Point(rr))
      call clraddr(Point(xcs))
      call clraddr(Point(xfs))
      call clraddr(Point(xcwi))
      call clraddr(Point(xfwi))
      call clraddr(Point(xfpf))
      call clraddr(Point(xcpf))
      call clraddr(Point(xcwo))
      call clraddr(Point(xfwo))
      call clraddr(Point(yyc))
      call clraddr(Point(yyf))
      call clraddr(Point(yylb))
      call clraddr(Point(yyrb))
      call clraddr(Point(xcv))
      call clraddr(Point(xfv))
      call clraddr(Point(psinormc))
      call clraddr(Point(psinormf))
      call clraddr(Point(rrv))
      call clraddr(Point(volv))
      call clraddr(Point(hxv))
      call clraddr(Point(syv))
      call clraddr(Point(isxptx))
      call clraddr(Point(isxpty))
      call clraddr(Point(lcon))
      call clraddr(Point(lconi))
      call clraddr(Point(lcone))
      call clraddr(Point(lconneo))
      call clraddr(Point(epsneo))
      call clraddr(Point(isixcore))
      call clraddr(Point(lcong))
      call clraddr(Point(lconig))
      call clraddr(Point(lconeg))
      call clraddr(Point(vtag))
      call clraddr(Point(angfx))
      call clraddr(Point(fxm))
      call clraddr(Point(fx0))
      call clraddr(Point(fxp))
      call clraddr(Point(fym))
      call clraddr(Point(fy0))
      call clraddr(Point(fyp))
      call clraddr(Point(fxmy))
      call clraddr(Point(fxpy))
      call clraddr(Point(fymx))
      call clraddr(Point(fypx))
      call clraddr(Point(fxmv))
      call clraddr(Point(fx0v))
      call clraddr(Point(fxpv))
      call clraddr(Point(fymv))
      call clraddr(Point(fy0v))
      call clraddr(Point(fypv))
      call clraddr(Point(fxmyv))
      call clraddr(Point(fxpyv))
      call clraddr(Point(fymxv))
      call clraddr(Point(fypxv))
      call clraddr(Point(nibbb))
      call clraddr(Point(tibbb))
      call clraddr(Point(nebbb))
      call clraddr(Point(tebbb))
      call clraddr(Point(vflowxbbb))
      call clraddr(Point(vflowybbb))
      call clraddr(Point(vflowzbbb))
      call clraddr(Point(fnixbbb))
      call clraddr(Point(fngysibbb))
      call clraddr(Point(fngysobbb))
      call clraddr(Point(rlimu))
      call clraddr(Point(zlimu))
      call clraddr(Point(rsplit1))
      call clraddr(Point(zsplit1))
      call clraddr(Point(rsplit2))
      call clraddr(Point(zsplit2))
      call clraddr(Point(tevb))
      call clraddr(Point(rsi))
      call clraddr(Point(rre))
      call clraddr(Point(rpwr))
      call clraddr(Point(rrcx))
      call clraddr(Point(rtza))
      call clraddr(Point(rtzn))
      call clraddr(Point(rtza2))
      call clraddr(Point(rtt))
      call clraddr(Point(rtn))
      call clraddr(Point(rtlt))
      call clraddr(Point(rtln))
      call clraddr(Point(rtlsa))
      call clraddr(Point(rtlra))
      call clraddr(Point(rtlqa))
      call clraddr(Point(rtlcx))
      call clraddr(Point(chgstate_format))
      call clraddr(Point(fcoefne_tanh))
      call clraddr(Point(fcoefte_tanh))
      call clraddr(Point(fit_t_bs))
      call clraddr(Point(fcoef_bs))
      call clraddr(Point(nefit))
      call clraddr(Point(tefit))
      call clraddr(Point(tifit))
      call clraddr(Point(nefituse))
      call clraddr(Point(tefituse))
      call clraddr(Point(tifituse))
      call clraddr(Point(dumfit))
      call clraddr(Point(taudndt))
      call clraddr(Point(taudeedt))
      call clraddr(Point(taudeidt))
      call clraddr(Point(epsi_fit))
      call clraddr(Point(psi_s))
      call clraddr(Point(yyc_fit))
      call clraddr(Point(eprofile_fit))

      return
       end
      subroutine comdbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,21,387)
      return
       end
      subroutine comwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /comrtdm/ drtdm
Use_All_Groups_com

      Address i000addr
      external varadr
      Address varadr


      call comdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"OMFIT")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"iomfit",varadr(iomfit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"COMroutines")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "glbwrlog",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ioun:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Dim")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nx",varadr(nx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ny",varadr(ny),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxm",varadr(nxm),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nym",varadr(nym),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxpt",varadr(nxpt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nhsp",varadr(nhsp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( nzsp )
      i0001234=rtvare(drtdm,"nzsp",i000addr,0,Quote(integer),
Quote((1:ngspmx-1)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzspt",varadr(nzspt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzspmx",varadr(nzspmx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nisp",varadr(nisp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nusp",varadr(nusp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nfsp",varadr(nfsp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ngsp",varadr(ngsp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+restart))
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"nhgsp",varadr(nhgsp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"imx",varadr(imx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"imy",varadr(imy),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"lnst",varadr(lnst),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"num_elem",varadr(num_elem),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Dimflxgrd")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"jdim",varadr(jdim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"npts",varadr(npts),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"noregs",varadr(noregs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxefit",varadr(nxefit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nyefit",varadr(nyefit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nlim",varadr(nlim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nbdry",varadr(nbdry),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nwork",varadr(nwork),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Comflxgrd")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"isfw",varadr(isfw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"runid",varadr(runid),0,Quote(character*60),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xold) )
      i0001234=rtvare(drtdm,"xold",i000addr,1,Quote(_double precision),
Quote((nxefit)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yold) )
      i0001234=rtvare(drtdm,"yold",i000addr,1,Quote(_double precision),
Quote((nyefit)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fold) )
      i0001234=rtvare(drtdm,"fold",i000addr,1,Quote(_double precision),
Quote((nxefit,nyefit)), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"bcentr",varadr(bcentr),0,Quote(double precision),
Quote(scalar), "Tesla")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rcentr",varadr(rcentr),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rmagx",varadr(rmagx),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zmagx",varadr(zmagx),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"simagx",varadr(simagx),0,Quote(double precision),
Quote(scalar), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sibdry",varadr(sibdry),0,Quote(double precision),
Quote(scalar), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sibdry1",varadr(sibdry1),0,Quote(double precision),
Quote(scalar), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sibdry2",varadr(sibdry2),0,Quote(double precision),
Quote(scalar), "volt-sec/radian")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xdim",varadr(xdim),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zdim",varadr(zdim),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zmid",varadr(zmid),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zshift",varadr(zshift),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(workk) )
      i0001234=rtvare(drtdm,"workk",i000addr,1,Quote(_double precision),
Quote((nxefit)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fpol) )
      i0001234=rtvare(drtdm,"fpol",i000addr,1,Quote(_double precision),
Quote((nxefit)), "m-T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(pres) )
      i0001234=rtvare(drtdm,"pres",i000addr,1,Quote(_double precision),
Quote((nxefit)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(qpsi) )
      i0001234=rtvare(drtdm,"qpsi",i000addr,1,Quote(_double precision),
Quote((nxefit)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rgrid1",varadr(rgrid1),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"cpasma",varadr(cpasma),0,Quote(double precision),
Quote(scalar), "Amps")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rbdry) )
      i0001234=rtvare(drtdm,"rbdry",i000addr,1,Quote(_double precision),
Quote((nbdry)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zbdry) )
      i0001234=rtvare(drtdm,"zbdry",i000addr,1,Quote(_double precision),
Quote((nbdry)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xlim) )
      i0001234=rtvare(drtdm,"xlim",i000addr,1,Quote(_double precision),
Quote((nlim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ylim) )
      i0001234=rtvare(drtdm,"ylim",i000addr,1,Quote(_double precision),
Quote((nlim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bscoef) )
      i0001234=rtvare(drtdm,"bscoef",i000addr,1,Quote(_double precision),
Quote((nxefit,nyefit)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kxord",varadr(kxord),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kyord",varadr(kyord),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xknot) )
      i0001234=rtvare(drtdm,"xknot",i000addr,1,Quote(_double precision),
Quote((nxefit+kxord)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yknot) )
      i0001234=rtvare(drtdm,"yknot",i000addr,1,Quote(_double precision),
Quote((nyefit+kyord)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ldf",varadr(ldf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iflag",varadr(iflag),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(work) )
      i0001234=rtvare(drtdm,"work",i000addr,1,Quote(_double precision),
Quote((nwork)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( jmin )
      i0001234=rtvare(drtdm,"jmin",i000addr,0,Quote(integer),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( jmax )
      i0001234=rtvare(drtdm,"jmax",i000addr,0,Quote(integer),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( jsptrx )
      i0001234=rtvare(drtdm,"jsptrx",i000addr,0,Quote(integer),
Quote((2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"jaxis",varadr(jaxis),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xlbnd",varadr(xlbnd),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xubnd",varadr(xubnd),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ylbnd",varadr(ylbnd),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"yubnd",varadr(yubnd),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcurve) )
      i0001234=rtvare(drtdm,"xcurve",i000addr,1,Quote(_double precision),
Quote((npts,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ycurve) )
      i0001234=rtvare(drtdm,"ycurve",i000addr,1,Quote(_double precision),
Quote((npts,jdim)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(npoint) )
      i0001234=rtvare(drtdm,"npoint",i000addr,1,Quote(_integer),
Quote((jdim)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"geqdskfname",varadr(geqdskfname),0,Quote(character*128),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Aeqflxgrd")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"vmonth",varadr(vmonth),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"vday",varadr(vday),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"vyear",varadr(vyear),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"eshot",varadr(eshot),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"etime",varadr(etime),0,Quote(double precision),
Quote(scalar), "msec")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rseps",varadr(rseps),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zseps",varadr(zseps),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rseps1",varadr(rseps1),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zseps1",varadr(zseps1),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rseps2",varadr(rseps2),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zseps2",varadr(zseps2),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rvsin",varadr(rvsin),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zvsin",varadr(zvsin),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rvsout",varadr(rvsout),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zvsout",varadr(zvsout),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mco2v",varadr(mco2v),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mco2r",varadr(mco2r),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rco2v) )
      i0001234=rtvare(drtdm,"rco2v",i000addr,1,Quote(_double precision),
Quote((mco2v)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dco2v) )
      i0001234=rtvare(drtdm,"dco2v",i000addr,1,Quote(_double precision),
Quote((mco2v)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rco2r) )
      i0001234=rtvare(drtdm,"rco2r",i000addr,1,Quote(_double precision),
Quote((mco2r)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dco2r) )
      i0001234=rtvare(drtdm,"dco2r",i000addr,1,Quote(_double precision),
Quote((mco2r)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nsilop",varadr(nsilop),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(csilop) )
      i0001234=rtvare(drtdm,"csilop",i000addr,1,Quote(_double precision),
Quote((nsilop)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"magpri",varadr(magpri),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(cmpr2) )
      i0001234=rtvare(drtdm,"cmpr2",i000addr,1,Quote(_double precision),
Quote((magpri)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nfcoil",varadr(nfcoil),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ccbrsp) )
      i0001234=rtvare(drtdm,"ccbrsp",i000addr,1,Quote(_double precision),
Quote((nfcoil)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nesum",varadr(nesum),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(eccurt) )
      i0001234=rtvare(drtdm,"eccurt",i000addr,1,Quote(_double precision),
Quote((nesum)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"aeqdskfname",varadr(aeqdskfname),0,Quote(character*128),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"RZ_grid_info")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(rm) )
      i0001234=rtvare(drtdm,"rm",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zm) )
      i0001234=rtvare(drtdm,"zm",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rmt) )
      i0001234=rtvare(drtdm,"rmt",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zmt) )
      i0001234=rtvare(drtdm,"zmt",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rv) )
      i0001234=rtvare(drtdm,"rv",i000addr,1,Quote(_double precision),
Quote((0:nxm+2,-1:nym+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zv) )
      i0001234=rtvare(drtdm,"zv",i000addr,1,Quote(_double precision),
Quote((0:nxm+2,-1:nym+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psi) )
      i0001234=rtvare(drtdm,"psi",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "Tm^2")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(br) )
      i0001234=rtvare(drtdm,"br",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bz) )
      i0001234=rtvare(drtdm,"bz",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bpol) )
      i0001234=rtvare(drtdm,"bpol",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bphi) )
      i0001234=rtvare(drtdm,"bphi",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(b) )
      i0001234=rtvare(drtdm,"b",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bsqr) )
      i0001234=rtvare(drtdm,"bsqr",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(b12) )
      i0001234=rtvare(drtdm,"b12",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(b12ctr) )
      i0001234=rtvare(drtdm,"b12ctr",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(b32) )
      i0001234=rtvare(drtdm,"b32",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1)), "T")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"RZ_grid_global")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(rmg) )
      i0001234=rtvare(drtdm,"rmg",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zmg) )
      i0001234=rtvare(drtdm,"zmg",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psig) )
      i0001234=rtvare(drtdm,"psig",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "Tm^2")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(brg) )
      i0001234=rtvare(drtdm,"brg",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bzg) )
      i0001234=rtvare(drtdm,"bzg",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bpolg) )
      i0001234=rtvare(drtdm,"bpolg",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bphig) )
      i0001234=rtvare(drtdm,"bphig",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(bg) )
      i0001234=rtvare(drtdm,"bg",i000addr,1,Quote(_double precision),
Quote((0:nxm+1,0:nym+1,0:4)), "T")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Share")
      if(jgrp = 0) go to 999
      i000addr = varadr ( nycore )
      i0001234=rtvare(drtdm,"nycore",i000addr,0,Quote(integer),
Quote((30)), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i000addr = varadr ( nysol )
      i0001234=rtvare(drtdm,"nysol",i000addr,0,Quote(integer),
Quote((30)), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i000addr = varadr ( nyout )
      i0001234=rtvare(drtdm,"nyout",i000addr,0,Quote(integer),
Quote((30)), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i000addr = varadr ( nxleg )
      i0001234=rtvare(drtdm,"nxleg",i000addr,0,Quote(integer),
Quote((30,2)), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i000addr = varadr ( nxcore )
      i0001234=rtvare(drtdm,"nxcore",i000addr,0,Quote(integer),
Quote((30,2)), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+regrid))
      i0001234=rtvare(drtdm,"nxomit",varadr(nxomit),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxxpt",varadr(nxxpt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nyomitmx",varadr(nyomitmx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"igrid",varadr(igrid),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"geometry",varadr(geometry),0,Quote(character*16),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxc",varadr(nxc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"simagxs",varadr(simagxs),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sibdrys",varadr(sibdrys),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ismpsym",varadr(ismpsym),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isudsym",varadr(isudsym),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"islimon",varadr(islimon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ix_lim",varadr(ix_lim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iy_lims",varadr(iy_lims),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"theta_split",varadr(theta_split),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isnonog",varadr(isnonog),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ismmon",varadr(ismmon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isoldgrid",varadr(isoldgrid),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isgrdsym",varadr(isgrdsym),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"cutlo",varadr(cutlo),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"epslon",varadr(epslon),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"spheromak",varadr(spheromak),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isfrc",varadr(isfrc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ishalfm",varadr(ishalfm),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isbphicon",varadr(isbphicon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nhdf",varadr(nhdf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( hdfilename )
      i0001234=rtvare(drtdm,"hdfilename",i000addr,0,Quote(Filename),
Quote((1:12)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzdf",varadr(nzdf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( mcfilename )
      i0001234=rtvare(drtdm,"mcfilename",i000addr,0,Quote(Filename),
Quote((1:12)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"coronalimpfname",varadr(coronalimpfname),0,Quote(character*120),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"istabon",varadr(istabon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      call rtvattre(i0001234,drtdm,Quote(+restart))
      i0001234=rtvare(drtdm,"reset_core_og",varadr(reset_core_og),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Xpoint_indices")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(ixlb) )
      i0001234=rtvare(drtdm,"ixlb",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixpt1) )
      i0001234=rtvare(drtdm,"ixpt1",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixmdp) )
      i0001234=rtvare(drtdm,"ixmdp",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixpt2) )
      i0001234=rtvare(drtdm,"ixpt2",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixrb) )
      i0001234=rtvare(drtdm,"ixrb",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iysptrx1) )
      i0001234=rtvare(drtdm,"iysptrx1",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iysptrx2) )
      i0001234=rtvare(drtdm,"iysptrx2",i000addr,1,Quote(_integer),
Quote((1:nxpt)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iysptrx",varadr(iysptrx),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Cut_indices")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ixcut1",varadr(ixcut1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixcut2",varadr(ixcut2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixcut3",varadr(ixcut3),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ixcut4",varadr(ixcut4),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iycut1",varadr(iycut1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iycut2",varadr(iycut2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iycut3",varadr(iycut3),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iycut4",varadr(iycut4),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Comgeo")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(vol) )
      i0001234=rtvare(drtdm,"vol",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gx) )
      i0001234=rtvare(drtdm,"gx",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gy) )
      i0001234=rtvare(drtdm,"gy",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dx) )
      i0001234=rtvare(drtdm,"dx",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dxvf) )
      i0001234=rtvare(drtdm,"dxvf",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dy) )
      i0001234=rtvare(drtdm,"dy",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gxf) )
      i0001234=rtvare(drtdm,"gxf",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gxfn) )
      i0001234=rtvare(drtdm,"gxfn",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gyf) )
      i0001234=rtvare(drtdm,"gyf",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gxc) )
      i0001234=rtvare(drtdm,"gxc",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(gyc) )
      i0001234=rtvare(drtdm,"gyc",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^-1")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xnrm) )
      i0001234=rtvare(drtdm,"xnrm",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xvnrm) )
      i0001234=rtvare(drtdm,"xvnrm",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ynrm) )
      i0001234=rtvare(drtdm,"ynrm",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yvnrm) )
      i0001234=rtvare(drtdm,"yvnrm",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(sx) )
      i0001234=rtvare(drtdm,"sx",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^2")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(sxnp) )
      i0001234=rtvare(drtdm,"sxnp",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^2")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(sy) )
      i0001234=rtvare(drtdm,"sy",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m^2")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rr) )
      i0001234=rtvare(drtdm,"rr",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcs) )
      i0001234=rtvare(drtdm,"xcs",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xfs) )
      i0001234=rtvare(drtdm,"xfs",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcwi) )
      i0001234=rtvare(drtdm,"xcwi",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xfwi) )
      i0001234=rtvare(drtdm,"xfwi",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xfpf) )
      i0001234=rtvare(drtdm,"xfpf",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcpf) )
      i0001234=rtvare(drtdm,"xcpf",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcwo) )
      i0001234=rtvare(drtdm,"xcwo",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xfwo) )
      i0001234=rtvare(drtdm,"xfwo",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yyc) )
      i0001234=rtvare(drtdm,"yyc",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yyf) )
      i0001234=rtvare(drtdm,"yyf",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yylb) )
      i0001234=rtvare(drtdm,"yylb",i000addr,1,Quote(_double precision),
Quote((0:ny+1,1:nxpt)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yyrb) )
      i0001234=rtvare(drtdm,"yyrb",i000addr,1,Quote(_double precision),
Quote((0:ny+1,1:nxpt)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xcv) )
      i0001234=rtvare(drtdm,"xcv",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xfv) )
      i0001234=rtvare(drtdm,"xfv",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psinormc) )
      i0001234=rtvare(drtdm,"psinormc",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(psinormf) )
      i0001234=rtvare(drtdm,"psinormf",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rrv) )
      i0001234=rtvare(drtdm,"rrv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(volv) )
      i0001234=rtvare(drtdm,"volv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(hxv) )
      i0001234=rtvare(drtdm,"hxv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "1/m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(syv) )
      i0001234=rtvare(drtdm,"syv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sygytotc",varadr(sygytotc),0,Quote(double precision),
Quote(scalar), "1/m**3")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"area_core",varadr(area_core),0,Quote(double precision),
Quote(scalar), "1/m**3")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ghxpt",varadr(ghxpt),0,Quote(double precision),
Quote(scalar), "m^-1")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"gvxpt",varadr(gvxpt),0,Quote(double precision),
Quote(scalar), "m^-1")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sxyxpt",varadr(sxyxpt),0,Quote(double precision),
Quote(scalar), "m^2")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ghxpt_lower",varadr(ghxpt_lower),0,Quote(double precision),
Quote(scalar), "m^-1")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"gvxpt_lower",varadr(gvxpt_lower),0,Quote(double precision),
Quote(scalar), "m^-1")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sxyxpt_lower",varadr(sxyxpt_lower),0,Quote(double precision),
Quote(scalar), "m^2")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ghxpt_upper",varadr(ghxpt_upper),0,Quote(double precision),
Quote(scalar), "m^-1")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"gvxpt_upper",varadr(gvxpt_upper),0,Quote(double precision),
Quote(scalar), "m^-1")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sxyxpt_upper",varadr(sxyxpt_upper),0,Quote(double precision),
Quote(scalar), "m^2")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"linelen",varadr(linelen),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(isxptx) )
      i0001234=rtvare(drtdm,"isxptx",i000addr,1,Quote(_integer),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(isxpty) )
      i0001234=rtvare(drtdm,"isxpty",i000addr,1,Quote(_integer),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lcon) )
      i0001234=rtvare(drtdm,"lcon",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lconi) )
      i0001234=rtvare(drtdm,"lconi",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lcone) )
      i0001234=rtvare(drtdm,"lcone",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lconneo) )
      i0001234=rtvare(drtdm,"lconneo",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(epsneo) )
      i0001234=rtvare(drtdm,"epsneo",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(isixcore) )
      i0001234=rtvare(drtdm,"isixcore",i000addr,1,Quote(_integer),
Quote((0:nx+1)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dxmin",varadr(dxmin),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Comgeo_g")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(lcong) )
      i0001234=rtvare(drtdm,"lcong",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lconig) )
      i0001234=rtvare(drtdm,"lconig",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lconeg) )
      i0001234=rtvare(drtdm,"lconeg",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Noggeo")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(vtag) )
      i0001234=rtvare(drtdm,"vtag",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(angfx) )
      i0001234=rtvare(drtdm,"angfx",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxm) )
      i0001234=rtvare(drtdm,"fxm",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fx0) )
      i0001234=rtvare(drtdm,"fx0",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxp) )
      i0001234=rtvare(drtdm,"fxp",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fym) )
      i0001234=rtvare(drtdm,"fym",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fy0) )
      i0001234=rtvare(drtdm,"fy0",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fyp) )
      i0001234=rtvare(drtdm,"fyp",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxmy) )
      i0001234=rtvare(drtdm,"fxmy",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxpy) )
      i0001234=rtvare(drtdm,"fxpy",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fymx) )
      i0001234=rtvare(drtdm,"fymx",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fypx) )
      i0001234=rtvare(drtdm,"fypx",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxmv) )
      i0001234=rtvare(drtdm,"fxmv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fx0v) )
      i0001234=rtvare(drtdm,"fx0v",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxpv) )
      i0001234=rtvare(drtdm,"fxpv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fymv) )
      i0001234=rtvare(drtdm,"fymv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fy0v) )
      i0001234=rtvare(drtdm,"fy0v",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fypv) )
      i0001234=rtvare(drtdm,"fypv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxmyv) )
      i0001234=rtvare(drtdm,"fxmyv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fxpyv) )
      i0001234=rtvare(drtdm,"fxpyv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fymxv) )
      i0001234=rtvare(drtdm,"fymxv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fypxv) )
      i0001234=rtvare(drtdm,"fypxv",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1,0:1)), " ")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Timing")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"istimingon",varadr(istimingon),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iprinttim",varadr(iprinttim),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttotfe",varadr(ttotfe),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttimpfe",varadr(ttimpfe),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttotjf",varadr(ttotjf),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttimpjf",varadr(ttimpjf),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttmatfac",varadr(ttmatfac),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttmatsol",varadr(ttmatsol),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttjstor",varadr(ttjstor),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttjrnorm",varadr(ttjrnorm),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttjreorder",varadr(ttjreorder),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttimpc",varadr(ttimpc),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tstart",varadr(tstart),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tend",varadr(tend),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttnpg",varadr(ttnpg),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttngxlog",varadr(ttngxlog),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttngylog",varadr(ttngylog),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttngfd2",varadr(ttngfd2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ttngfxy",varadr(ttngfxy),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Linkbbb")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nxbbb",varadr(nxbbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nybbb",varadr(nybbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nycorebbb",varadr(nycorebbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nysolbbb",varadr(nysolbbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxleg1bbb",varadr(nxleg1bbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxcore1bbb",varadr(nxcore1bbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxleg2bbb",varadr(nxleg2bbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nxcore2bbb",varadr(nxcore2bbb),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"geometrybbb",varadr(geometrybbb),0,Quote(character*8),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nibbb) )
      i0001234=rtvare(drtdm,"nibbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tibbb) )
      i0001234=rtvare(drtdm,"tibbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nebbb) )
      i0001234=rtvare(drtdm,"nebbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tebbb) )
      i0001234=rtvare(drtdm,"tebbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(vflowxbbb) )
      i0001234=rtvare(drtdm,"vflowxbbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(vflowybbb) )
      i0001234=rtvare(drtdm,"vflowybbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(vflowzbbb) )
      i0001234=rtvare(drtdm,"vflowzbbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fnixbbb) )
      i0001234=rtvare(drtdm,"fnixbbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1,0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fngysibbb) )
      i0001234=rtvare(drtdm,"fngysibbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fngysobbb) )
      i0001234=rtvare(drtdm,"fngysobbb",i000addr,1,Quote(_double precision),
Quote((0:nx+1)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Timespl")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"totb2val",varadr(totb2val),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"totintrv",varadr(totintrv),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Limiter")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nlimu",varadr(nlimu),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rlimu) )
      i0001234=rtvare(drtdm,"rlimu",i000addr,1,Quote(_double precision),
Quote((1:nlimu)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zlimu) )
      i0001234=rtvare(drtdm,"zlimu",i000addr,1,Quote(_double precision),
Quote((1:nlimu)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nptnma",varadr(nptnma),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rptnma",varadr(rptnma),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zptnma",varadr(zptnma),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dslims",varadr(dslims),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nsplit1",varadr(nsplit1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rsplit1) )
      i0001234=rtvare(drtdm,"rsplit1",i000addr,1,Quote(_double precision),
Quote((nsplit1)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zsplit1) )
      i0001234=rtvare(drtdm,"zsplit1",i000addr,1,Quote(_double precision),
Quote((nsplit1)), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nsplit2",varadr(nsplit2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rsplit2) )
      i0001234=rtvare(drtdm,"rsplit2",i000addr,1,Quote(_double precision),
Quote((nsplit2)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zsplit2) )
      i0001234=rtvare(drtdm,"zsplit2",i000addr,1,Quote(_double precision),
Quote((nsplit2)), "m")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Multicharge")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ntev",varadr(ntev),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nz",varadr(nz),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tevb) )
      i0001234=rtvare(drtdm,"tevb",i000addr,1,Quote(_double precision),
Quote((ntev)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rsi) )
      i0001234=rtvare(drtdm,"rsi",i000addr,1,Quote(_double precision),
Quote((ntev,0:nz-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rre) )
      i0001234=rtvare(drtdm,"rre",i000addr,1,Quote(_double precision),
Quote((ntev,1:nz)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rpwr) )
      i0001234=rtvare(drtdm,"rpwr",i000addr,1,Quote(_double precision),
Quote((ntev,0:nz)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rrcx) )
      i0001234=rtvare(drtdm,"rrcx",i000addr,1,Quote(_double precision),
Quote((ntev,1:nz)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( labelrt )
      i0001234=rtvare(drtdm,"labelrt",i000addr,0,Quote(character*120),
Quote((1:12)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rtnt",varadr(rtnt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rtnn",varadr(rtnn),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rtns",varadr(rtns),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rtnsd",varadr(rtnsd),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtza) )
      i0001234=rtvare(drtdm,"rtza",i000addr,1,Quote(_double precision),
Quote((0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtzn) )
      i0001234=rtvare(drtdm,"rtzn",i000addr,1,Quote(_double precision),
Quote((0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtza2) )
      i0001234=rtvare(drtdm,"rtza2",i000addr,1,Quote(_double precision),
Quote((0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtt) )
      i0001234=rtvare(drtdm,"rtt",i000addr,1,Quote(_double precision),
Quote((0:rtnt)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtn) )
      i0001234=rtvare(drtdm,"rtn",i000addr,1,Quote(_double precision),
Quote((0:rtnn)), "/m**3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtlt) )
      i0001234=rtvare(drtdm,"rtlt",i000addr,1,Quote(_double precision),
Quote((0:rtnt)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtln) )
      i0001234=rtvare(drtdm,"rtln",i000addr,1,Quote(_double precision),
Quote((0:rtnn)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtlsa) )
      i0001234=rtvare(drtdm,"rtlsa",i000addr,1,Quote(_double precision),
Quote((0:rtnt,0:rtnn,0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtlra) )
      i0001234=rtvare(drtdm,"rtlra",i000addr,1,Quote(_double precision),
Quote((0:rtnt,0:rtnn,0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtlqa) )
      i0001234=rtvare(drtdm,"rtlqa",i000addr,1,Quote(_double precision),
Quote((0:rtnt,0:rtnn,0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rtlcx) )
      i0001234=rtvare(drtdm,"rtlcx",i000addr,1,Quote(_double precision),
Quote((0:rtnt,0:rtnn,0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iscxfit",varadr(iscxfit),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isrtndep",varadr(isrtndep),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( mcfformat )
      i0001234=rtvare(drtdm,"mcfformat",i000addr,0,Quote(integer),
Quote((1:12)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(chgstate_format) )
      i0001234=rtvare(drtdm,"chgstate_format",i000addr,1,Quote(_integer),
Quote((0:rtnsd-1)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ispradextrap",varadr(ispradextrap),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Fitdata")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"isprof_coef",varadr(isprof_coef),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncoefne_tanh",varadr(ncoefne_tanh),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncoefte_tanh",varadr(ncoefte_tanh),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"numt_bs",varadr(numt_bs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"numc_bs",varadr(numc_bs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"numk_bs",varadr(numk_bs),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fcoefne_tanh) )
      i0001234=rtvare(drtdm,"fcoefne_tanh",i000addr,1,Quote(_double precision),
Quote((ncoefne_tanh)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fcoefte_tanh) )
      i0001234=rtvare(drtdm,"fcoefte_tanh",i000addr,1,Quote(_double precision),
Quote((ncoefte_tanh)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"fit_paramne_tanh",varadr(fit_paramne_tanh),0,Quote(character*8),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"fit_paramte_tanh",varadr(fit_paramte_tanh),0,Quote(character*8),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fit_t_bs) )
      i0001234=rtvare(drtdm,"fit_t_bs",i000addr,1,Quote(_double precision),
Quote((numt_bs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fcoef_bs) )
      i0001234=rtvare(drtdm,"fcoef_bs",i000addr,1,Quote(_double precision),
Quote((numc_bs)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(nefit) )
      i0001234=rtvare(drtdm,"nefit",i000addr,1,Quote(_double precision),
Quote((0:ny+1,2)), "m**-3")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( Point(tefit) )
      i0001234=rtvare(drtdm,"tefit",i000addr,1,Quote(_double precision),
Quote((0:ny+1,2)), "keV")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( Point(tifit) )
      i0001234=rtvare(drtdm,"tifit",i000addr,1,Quote(_double precision),
Quote((0:ny+1,2)), "keV")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( Point(nefituse) )
      i0001234=rtvare(drtdm,"nefituse",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( Point(tefituse) )
      i0001234=rtvare(drtdm,"tefituse",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( Point(tifituse) )
      i0001234=rtvare(drtdm,"tifituse",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i0001234=rtvare(drtdm,"fitfrac1",varadr(fitfrac1),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(dumfit) )
      i0001234=rtvare(drtdm,"dumfit",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i0001234=rtvare(drtdm,"isdatfmtnew",varadr(isdatfmtnew),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"psishift",varadr(psishift),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"isdndtfitdat",varadr(isdndtfitdat),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ifitset",varadr(ifitset),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tim_interval_fit",varadr(tim_interval_fit),0,Quote(double precision),
Quote(scalar), "s")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"tim_chng_max",varadr(tim_chng_max),0,Quote(double precision),
Quote(scalar), "s")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(taudndt) )
      i0001234=rtvare(drtdm,"taudndt",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "s")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,1.e50)
      i000addr = varadr ( Point(taudeedt) )
      i0001234=rtvare(drtdm,"taudeedt",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "s")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,1.e50)
      i000addr = varadr ( Point(taudeidt) )
      i0001234=rtvare(drtdm,"taudeidt",i000addr,1,Quote(_double precision),
Quote((0:ny+1)), "s")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,1.e50)
      i0001234=rtvare(drtdm,"isprofvspsi",varadr(isprofvspsi),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(epsi_fit) )
      i0001234=rtvare(drtdm,"epsi_fit",i000addr,1,Quote(_double precision),
Quote((num_elem)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(psi_s) )
      i0001234=rtvare(drtdm,"psi_s",i000addr,1,Quote(_double precision),
Quote((num_elem)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(yyc_fit) )
      i0001234=rtvare(drtdm,"yyc_fit",i000addr,1,Quote(_double precision),
Quote((num_elem)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(eprofile_fit) )
      i0001234=rtvare(drtdm,"eprofile_fit",i000addr,1,Quote(_double precision),
Quote((num_elem)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      jgrp=rtgrpe(drtdm,"Subs2")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "xerrab",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(msg:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_msg_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readne_dat",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readte_dat",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "readti_dat",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "fit_neteti",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "tanh_multi",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(i:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(a:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(j:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(b:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(fname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_fname_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(d:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      call rtsetdoc(drtdm,"com.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine comxpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.2) then
         call comxp2(name1234)
      elseif(iseg.eq.21) then
         call comxp21(name1234)
      else
         call baderr('comxpf: impossible event')
      endif
      return
      end
      subroutine comxp2(name1234)
      character*(*) name1234
      external com_handler
      external [glbwrlog]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'glbwrlog') then
         call parexecf(com_handler, 0, [glbwrlog])
      else
         call baderr('comxp2: impossible event: '//name5678)
      endif
      return
      end
      subroutine comxp21(name1234)
      character*(*) name1234
      external com_handler
      external [xerrab]
      external [readne_dat]
      external [readte_dat]
      external [readti_dat]
      external [fit_neteti]
      external [tanh_multi]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'xerrab') then
         call parexecf(com_handler, 1, [xerrab])
      elseif(name1234 = 'readne_dat') then
         call parexecf(com_handler, 2, [readne_dat])
      elseif(name1234 = 'readte_dat') then
         call parexecf(com_handler, 3, [readte_dat])
      elseif(name1234 = 'readti_dat') then
         call parexecf(com_handler, 4, [readti_dat])
      elseif(name1234 = 'fit_neteti') then
         call parexecf(com_handler, 5, [fit_neteti])
      elseif(name1234 = 'tanh_multi') then
         call parexecf(com_handler, 6, [tanh_multi])
      else
         call baderr('comxp21: impossible event: '//name5678)
      endif
      return
      end
      function combfcn(ss,sp,nargs,name1234,sx)
      integer combfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in com')
      call baderr(name1234)
      return(ERR)
      end
