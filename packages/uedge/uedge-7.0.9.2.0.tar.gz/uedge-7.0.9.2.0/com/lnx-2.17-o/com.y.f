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
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/aph.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/api_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/bbb_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/grd_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/flx_basis.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/wdf.d
c     /mfe/workspace/meyer8/cvsstuff/pyUedge/uedge/dev/lnx-2.17-o/include/com.d
c     ./com.y.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c


























































































































































































































      subroutine cominit0
cProlog
c initializes a Package
      integer drtdm
      common /comrtdm/ drtdm
      character*(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("com")
      if (glbstat(drtdm) .ne. 0) return
      call glblngn(drtdm,lngn)
      if (izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call comdata
      call comwake
c set our status
      call glbsstat(drtdm,2)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end

      block data comiyiyi
c Replace pointer statements with Address types


c Group OMFIT
      integer iomfit
      common /com00/ iomfit
c End of OMFIT

c Group COMroutines
c End of COMroutines

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd

c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis
      integer*8 pxold
      integer*8 pyold
      integer*8 pfold
      integer*8 pworkk
      integer*8 pfpol
      integer*8 ppres
      integer*8 pqpsi
      integer*8 prbdry
      integer*8 pzbdry
      integer*8 pxlim
      integer*8 pylim
      integer*8 pbscoef
      integer*8 pxknot
      integer*8 pyknot
      integer*8 pwork
      integer*8 pxcurve
      integer*8 pycurve
      integer*8 pnpoint
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd

c Group Aeqflxgrd
      double precision etime, rseps, zseps, rseps1, zseps1, rseps2
      integer vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop, magpri
      character*128 aeqdskfname
      double precision zseps2, rvsin, zvsin, rvsout, zvsout
      integer nfcoil, nesum
      integer*8 prco2v
      integer*8 pdco2v
      integer*8 prco2r
      integer*8 pdco2r
      integer*8 pcsilop
      integer*8 pcmpr2
      integer*8 pccbrsp
      integer*8 peccurt
      common /com10002/ aeqdskfname
      common /com50/ vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop
      common /com50/ magpri, nfcoil, nesum
      common /com53/ etime, rseps, zseps, rseps1, zseps1, rseps2, zseps2
      common /com53/ rvsin, zvsin, rvsout, zvsout
      common /com56/ prco2v, pdco2v, prco2r
      common /com56/ pdco2r, pcsilop, pcmpr2
      common /com56/ pccbrsp, peccurt
c End of Aeqflxgrd

c Group RZ_grid_info
      integer*8 prm
      integer*8 pzm
      integer*8 prmt
      integer*8 pzmt
      integer*8 prv
      integer*8 pzv
      integer*8 ppsi
      integer*8 pbr
      integer*8 pbz
      integer*8 pbpol
      integer*8 pbphi
      integer*8 pb
      integer*8 pbsqr
      integer*8 pb12
      integer*8 pb12ctr
      integer*8 pb32
      common /com66/ prm, pzm, prmt, pzmt
      common /com66/ prv, pzv, ppsi, pbr
      common /com66/ pbz, pbpol, pbphi, pb
      common /com66/ pbsqr, pb12, pb12ctr, pb32
c End of RZ_grid_info

c Group RZ_grid_global
      integer*8 prmg
      integer*8 pzmg
      integer*8 ppsig
      integer*8 pbrg
      integer*8 pbzg
      integer*8 pbpolg
      integer*8 pbphig
      integer*8 pbg
      common /com76/ prmg, pzmg, ppsig, pbrg
      common /com76/ pbzg, pbpolg, pbphig, pbg
c End of RZ_grid_global

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

c Group Xpoint_indices
      integer iysptrx
      integer*8 pixlb
      integer*8 pixpt1
      integer*8 pixmdp
      integer*8 pixpt2
      integer*8 pixrb
      integer*8 piysptrx1
      integer*8 piysptrx2
      common /com90/ iysptrx
      common /com96/ pixlb, pixpt1, pixmdp
      common /com96/ pixpt2, pixrb, piysptrx1
      common /com96/ piysptrx2
c End of Xpoint_indices

c Group Cut_indices
      integer ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2, iycut3
      integer iycut4
      common /com100/ ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2
      common /com100/ iycut3, iycut4
c End of Cut_indices

c Group Comgeo
      double precision sygytotc, area_core, ghxpt, gvxpt, sxyxpt
      double precision ghxpt_lower, gvxpt_lower, sxyxpt_lower
      double precision ghxpt_upper, gvxpt_upper, sxyxpt_upper, linelen
      double precision dxmin
      integer*8 pvol
      integer*8 pgx
      integer*8 pgy
      integer*8 pdx
      integer*8 pdxvf
      integer*8 pdy
      integer*8 pgxf
      integer*8 pgxfn
      integer*8 pgyf
      integer*8 pgxc
      integer*8 pgyc
      integer*8 pxnrm
      integer*8 pxvnrm
      integer*8 pynrm
      integer*8 pyvnrm
      integer*8 psx
      integer*8 psxnp
      integer*8 psy
      integer*8 prr
      integer*8 pxcs
      integer*8 pxfs
      integer*8 pxcwi
      integer*8 pxfwi
      integer*8 pxfpf
      integer*8 pxcpf
      integer*8 pxcwo
      integer*8 pxfwo
      integer*8 pyyc
      integer*8 pyyf
      integer*8 pyylb
      integer*8 pyyrb
      integer*8 pxcv
      integer*8 pxfv
      integer*8 ppsinormc
      integer*8 ppsinormf
      integer*8 prrv
      integer*8 pvolv
      integer*8 phxv
      integer*8 psyv
      integer*8 pisxptx
      integer*8 pisxpty
      integer*8 plcon
      integer*8 plconi
      integer*8 plcone
      integer*8 plconneo
      integer*8 pepsneo
      integer*8 pisixcore
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

c Group Comgeo_g
      integer*8 plcong
      integer*8 plconig
      integer*8 plconeg
      common /com126/ plcong, plconig, plconeg
c End of Comgeo_g

c Group Noggeo
      integer*8 pvtag
      integer*8 pangfx
      integer*8 pfxm
      integer*8 pfx0
      integer*8 pfxp
      integer*8 pfym
      integer*8 pfy0
      integer*8 pfyp
      integer*8 pfxmy
      integer*8 pfxpy
      integer*8 pfymx
      integer*8 pfypx
      integer*8 pfxmv
      integer*8 pfx0v
      integer*8 pfxpv
      integer*8 pfymv
      integer*8 pfy0v
      integer*8 pfypv
      integer*8 pfxmyv
      integer*8 pfxpyv
      integer*8 pfymxv
      integer*8 pfypxv
      common /com136/ pvtag, pangfx, pfxm, pfx0
      common /com136/ pfxp, pfym, pfy0, pfyp
      common /com136/ pfxmy, pfxpy, pfymx, pfypx
      common /com136/ pfxmv, pfx0v, pfxpv, pfymv
      common /com136/ pfy0v, pfypv, pfxmyv
      common /com136/ pfxpyv, pfymxv, pfypxv
c End of Noggeo

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

c Group Linkbbb
      integer nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb, nxcore1bbb
      character*8 geometrybbb
      integer nxleg2bbb, nxcore2bbb
      integer*8 pnibbb
      integer*8 ptibbb
      integer*8 pnebbb
      integer*8 ptebbb
      integer*8 pvflowxbbb
      integer*8 pvflowybbb
      integer*8 pvflowzbbb
      integer*8 pfnixbbb
      integer*8 pfngysibbb
      integer*8 pfngysobbb
      common /com10007/ geometrybbb
      common /com150/ nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb
      common /com150/ nxcore1bbb, nxleg2bbb, nxcore2bbb
      common /com156/ pnibbb, ptibbb, pnebbb
      common /com156/ ptebbb, pvflowxbbb, pvflowybbb
      common /com156/ pvflowzbbb, pfnixbbb, pfngysibbb
      common /com156/ pfngysobbb
c End of Linkbbb

c Group Timespl
      double precision totb2val, totintrv
      common /com163/ totb2val, totintrv
c End of Timespl

c Group Limiter
      double precision rptnma, zptnma, dslims
      integer nlimu, nptnma, nsplit1, nsplit2
      integer*8 prlimu
      integer*8 pzlimu
      integer*8 prsplit1
      integer*8 pzsplit1
      integer*8 prsplit2
      integer*8 pzsplit2
      common /com170/ nlimu, nptnma, nsplit1, nsplit2
      common /com173/ rptnma, zptnma, dslims
      common /com176/ prlimu, pzlimu, prsplit1
      common /com176/ pzsplit1, prsplit2, pzsplit2
c End of Limiter

c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap
      integer*8 ptevb
      integer*8 prsi
      integer*8 prre
      integer*8 prpwr
      integer*8 prrcx
      integer*8 prtza
      integer*8 prtzn
      integer*8 prtza2
      integer*8 prtt
      integer*8 prtn
      integer*8 prtlt
      integer*8 prtln
      integer*8 prtlsa
      integer*8 prtlra
      integer*8 prtlqa
      integer*8 prtlcx
      integer*8 pchgstate_format
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge

c Group Fitdata
      integer isprof_coef, ncoefne_tanh, ncoefte_tanh, numt_bs, numc_bs
      character*8 fit_paramne_tanh
      character*8 fit_paramte_tanh
      double precision fitfrac1, psishift, tim_interval_fit
      double precision tim_chng_max
      integer numk_bs, isdatfmtnew, isdndtfitdat, ifitset, isprofvspsi
      integer*8 pfcoefne_tanh
      integer*8 pfcoefte_tanh
      integer*8 pfit_t_bs
      integer*8 pfcoef_bs
      integer*8 pnefit
      integer*8 ptefit
      integer*8 ptifit
      integer*8 pnefituse
      integer*8 ptefituse
      integer*8 ptifituse
      integer*8 pdumfit
      integer*8 ptaudndt
      integer*8 ptaudeedt
      integer*8 ptaudeidt
      integer*8 pepsi_fit
      integer*8 ppsi_s
      integer*8 pyyc_fit
      integer*8 peprofile_fit
      common /com10009/ fit_paramne_tanh
      common /com10010/ fit_paramte_tanh
      common /com190/ isprof_coef, ncoefne_tanh, ncoefte_tanh, numt_bs
      common /com190/ numc_bs, numk_bs, isdatfmtnew, isdndtfitdat
      common /com190/ ifitset, isprofvspsi
      common /com193/ fitfrac1, psishift, tim_interval_fit, tim_chng_max
      common /com196/ pfcoefne_tanh, pfcoefte_tanh
      common /com196/ pfit_t_bs, pfcoef_bs, pnefit
      common /com196/ ptefit, ptifit, pnefituse
      common /com196/ ptefituse, ptifituse, pdumfit
      common /com196/ ptaudndt, ptaudeedt, ptaudeidt
      common /com196/ pepsi_fit, ppsi_s, pyyc_fit
      common /com196/ peprofile_fit
c End of Fitdata

c Group Subs2
c End of Subs2


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
      data iy_lims/9999/,theta_split/1.570796326794896d0/,isnonog/0/
      data ismmon/0/,isoldgrid/0/,isgrdsym/0/,cutlo/1.d-300/
      data epslon/1d-6/,spheromak/0/,isfrc/0/,ishalfm/0/,isbphicon/0/
      data nhdf/1/,hdfilename/12*'b2frates'/,nzdf/1/
      data mcfilename/12*'b2frates'/,coronalimpfname/'mist.dat'/
      data istabon/7/,reset_core_og/0/
      data dxmin/1.d-20/
      data istimingon/1/,iprinttim/0/,ttotfe/0.d0/,ttimpfe/0.d0/,ttotjf/
     &   0.d0/
      data ttimpjf/0.d0/,ttmatfac/0.d0/,ttmatsol/0.d0/,ttjstor/0.d0/
      data ttjrnorm/0.d0/,ttjreorder/0.d0/,ttimpc/0.d0/,tstart/0.d0/,
     &   tend/0.d0/
      data ttnpg/0.d0/,ttngxlog/0.d0/,ttngylog/0.d0/,ttngfd2/0.d0/,
     &   ttngfxy/0.d0/
      data totb2val/0.d0/,totintrv/0.d0/
      data dslims/.0001d0/
      data ntev/101/,nz/2/,iscxfit/1.d0/,isrtndep/1/,mcfformat/12*0/
      data ispradextrap/0/
      data isprof_coef/0/,ncoefne_tanh/1/,ncoefte_tanh/1/,numt_bs/1/
      data numc_bs/1/,numk_bs/1/,fitfrac1/1.d0/,isdatfmtnew/1/
      data psishift/0.d0/,isdndtfitdat/0/,ifitset/1/
      data tim_interval_fit/3.d-2/,tim_chng_max/1.d0/,isprofvspsi/1/

      end
c restore definition from mppl.BASIS

      subroutine comdata
cProlog

c Group OMFIT
      integer iomfit
      common /com00/ iomfit
c End of OMFIT

c Group COMroutines
c End of COMroutines

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd

c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis
      double precision xold ( nxefit)
      pointer(pxold,xold)
      double precision yold ( nyefit)
      pointer(pyold,yold)
      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)
      double precision workk ( nxefit)
      pointer(pworkk,workk)
      double precision fpol ( nxefit)
      pointer(pfpol,fpol)
      double precision pres ( nxefit)
      pointer(ppres,pres)
      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)
      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)
      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)
      double precision xlim ( nlim)
      pointer(pxlim,xlim)
      double precision ylim ( nlim)
      pointer(pylim,ylim)
      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)
      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)
      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)
      double precision work ( nwork)
      pointer(pwork,work)
      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)
      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)
      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd

c Group Aeqflxgrd
      double precision etime, rseps, zseps, rseps1, zseps1, rseps2
      integer vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop, magpri
      character*128 aeqdskfname
      double precision zseps2, rvsin, zvsin, rvsout, zvsout
      integer nfcoil, nesum
      double precision rco2v ( mco2v)
      pointer(prco2v,rco2v)
      double precision dco2v ( mco2v)
      pointer(pdco2v,dco2v)
      double precision rco2r ( mco2r)
      pointer(prco2r,rco2r)
      double precision dco2r ( mco2r)
      pointer(pdco2r,dco2r)
      double precision csilop ( nsilop)
      pointer(pcsilop,csilop)
      double precision cmpr2 ( magpri)
      pointer(pcmpr2,cmpr2)
      double precision ccbrsp ( nfcoil)
      pointer(pccbrsp,ccbrsp)
      double precision eccurt ( nesum)
      pointer(peccurt,eccurt)
      common /com10002/ aeqdskfname
      common /com50/ vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop
      common /com50/ magpri, nfcoil, nesum
      common /com53/ etime, rseps, zseps, rseps1, zseps1, rseps2, zseps2
      common /com53/ rvsin, zvsin, rvsout, zvsout
      common /com56/ prco2v, pdco2v, prco2r
      common /com56/ pdco2r, pcsilop, pcmpr2
      common /com56/ pccbrsp, peccurt
c End of Aeqflxgrd

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

c Group RZ_grid_global
      double precision rmg ( 0:nxm+1,0:nym+1,0:4)
      pointer(prmg,rmg)
      double precision zmg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pzmg,zmg)
      double precision psig ( 0:nxm+1,0:nym+1,0:4)
      pointer(ppsig,psig)
      double precision brg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbrg,brg)
      double precision bzg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbzg,bzg)
      double precision bpolg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbpolg,bpolg)
      double precision bphig ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbphig,bphig)
      double precision bg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbg,bg)
      common /com76/ prmg, pzmg, ppsig, pbrg
      common /com76/ pbzg, pbpolg, pbphig, pbg
c End of RZ_grid_global

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

c Group Cut_indices
      integer ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2, iycut3
      integer iycut4
      common /com100/ ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2
      common /com100/ iycut3, iycut4
c End of Cut_indices

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

c Group Comgeo_g
      double precision lcong ( 0:nx+1,0:ny+1)
      pointer(plcong,lcong)
      double precision lconig ( 0:nx+1,0:ny+1)
      pointer(plconig,lconig)
      double precision lconeg ( 0:nx+1,0:ny+1)
      pointer(plconeg,lconeg)
      common /com126/ plcong, plconig, plconeg
c End of Comgeo_g

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

c Group Linkbbb
      integer nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb, nxcore1bbb
      character*8 geometrybbb
      integer nxleg2bbb, nxcore2bbb
      double precision nibbb ( 0:nx+1,0:ny+1)
      pointer(pnibbb,nibbb)
      double precision tibbb ( 0:nx+1,0:ny+1)
      pointer(ptibbb,tibbb)
      double precision nebbb ( 0:nx+1,0:ny+1)
      pointer(pnebbb,nebbb)
      double precision tebbb ( 0:nx+1,0:ny+1)
      pointer(ptebbb,tebbb)
      double precision vflowxbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowxbbb,vflowxbbb)
      double precision vflowybbb ( 0:nx+1,0:ny+1)
      pointer(pvflowybbb,vflowybbb)
      double precision vflowzbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowzbbb,vflowzbbb)
      double precision fnixbbb ( 0:nx+1,0:ny+1)
      pointer(pfnixbbb,fnixbbb)
      double precision fngysibbb ( 0:nx+1)
      pointer(pfngysibbb,fngysibbb)
      double precision fngysobbb ( 0:nx+1)
      pointer(pfngysobbb,fngysobbb)
      common /com10007/ geometrybbb
      common /com150/ nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb
      common /com150/ nxcore1bbb, nxleg2bbb, nxcore2bbb
      common /com156/ pnibbb, ptibbb, pnebbb
      common /com156/ ptebbb, pvflowxbbb, pvflowybbb
      common /com156/ pvflowzbbb, pfnixbbb, pfngysibbb
      common /com156/ pfngysobbb
c End of Linkbbb

c Group Timespl
      double precision totb2val, totintrv
      common /com163/ totb2val, totintrv
c End of Timespl

c Group Limiter
      double precision rptnma, zptnma, dslims
      integer nlimu, nptnma, nsplit1, nsplit2
      double precision rlimu ( 1:nlimu)
      pointer(prlimu,rlimu)
      double precision zlimu ( 1:nlimu)
      pointer(pzlimu,zlimu)
      double precision rsplit1 ( nsplit1)
      pointer(prsplit1,rsplit1)
      double precision zsplit1 ( nsplit1)
      pointer(pzsplit1,zsplit1)
      double precision rsplit2 ( nsplit2)
      pointer(prsplit2,rsplit2)
      double precision zsplit2 ( nsplit2)
      pointer(pzsplit2,zsplit2)
      common /com170/ nlimu, nptnma, nsplit1, nsplit2
      common /com173/ rptnma, zptnma, dslims
      common /com176/ prlimu, pzlimu, prsplit1
      common /com176/ pzsplit1, prsplit2, pzsplit2
c End of Limiter

c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap
      double precision tevb ( ntev)
      pointer(ptevb,tevb)
      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)
      double precision rre ( ntev,1:nz)
      pointer(prre,rre)
      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)
      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)
      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)
      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)
      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)
      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)
      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)
      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)
      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)
      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)
      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)
      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)
      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)
      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge

c Group Fitdata
      integer isprof_coef, ncoefne_tanh, ncoefte_tanh, numt_bs, numc_bs
      character*8 fit_paramne_tanh
      character*8 fit_paramte_tanh
      double precision fitfrac1, psishift, tim_interval_fit
      double precision tim_chng_max
      integer numk_bs, isdatfmtnew, isdndtfitdat, ifitset, isprofvspsi
      double precision fcoefne_tanh ( ncoefne_tanh)
      pointer(pfcoefne_tanh,fcoefne_tanh)
      double precision fcoefte_tanh ( ncoefte_tanh)
      pointer(pfcoefte_tanh,fcoefte_tanh)
      double precision fit_t_bs ( numt_bs)
      pointer(pfit_t_bs,fit_t_bs)
      double precision fcoef_bs ( numc_bs)
      pointer(pfcoef_bs,fcoef_bs)
      double precision nefit ( 0:ny+1,2)
      pointer(pnefit,nefit)
      double precision tefit ( 0:ny+1,2)
      pointer(ptefit,tefit)
      double precision tifit ( 0:ny+1,2)
      pointer(ptifit,tifit)
      double precision nefituse ( 0:ny+1)
      pointer(pnefituse,nefituse)
      double precision tefituse ( 0:ny+1)
      pointer(ptefituse,tefituse)
      double precision tifituse ( 0:ny+1)
      pointer(ptifituse,tifituse)
      double precision dumfit ( 0:ny+1)
      pointer(pdumfit,dumfit)
      double precision taudndt ( 0:ny+1)
      pointer(ptaudndt,taudndt)
      double precision taudeedt ( 0:ny+1)
      pointer(ptaudeedt,taudeedt)
      double precision taudeidt ( 0:ny+1)
      pointer(ptaudeidt,taudeidt)
      double precision epsi_fit ( num_elem)
      pointer(pepsi_fit,epsi_fit)
      double precision psi_s ( num_elem)
      pointer(ppsi_s,psi_s)
      double precision yyc_fit ( num_elem)
      pointer(pyyc_fit,yyc_fit)
      double precision eprofile_fit ( num_elem)
      pointer(peprofile_fit,eprofile_fit)
      common /com10009/ fit_paramne_tanh
      common /com10010/ fit_paramte_tanh
      common /com190/ isprof_coef, ncoefne_tanh, ncoefte_tanh, numt_bs
      common /com190/ numc_bs, numk_bs, isdatfmtnew, isdndtfitdat
      common /com190/ ifitset, isprofvspsi
      common /com193/ fitfrac1, psishift, tim_interval_fit, tim_chng_max
      common /com196/ pfcoefne_tanh, pfcoefte_tanh
      common /com196/ pfit_t_bs, pfcoef_bs, pnefit
      common /com196/ ptefit, ptifit, pnefituse
      common /com196/ ptefituse, ptifituse, pdumfit
      common /com196/ ptaudndt, ptaudeedt, ptaudeidt
      common /com196/ pepsi_fit, ppsi_s, pyyc_fit
      common /com196/ peprofile_fit
c End of Fitdata

c Group Subs2
c End of Subs2


      external comiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(pxold)
      call clraddr(pyold)
      call clraddr(pfold)
      call clraddr(pworkk)
      call clraddr(pfpol)
      call clraddr(ppres)
      call clraddr(pqpsi)
      call clraddr(prbdry)
      call clraddr(pzbdry)
      call clraddr(pxlim)
      call clraddr(pylim)
      call clraddr(pbscoef)
      call clraddr(pxknot)
      call clraddr(pyknot)
      call clraddr(pwork)
      call clraddr(pxcurve)
      call clraddr(pycurve)
      call clraddr(pnpoint)
      call clraddr(prco2v)
      call clraddr(pdco2v)
      call clraddr(prco2r)
      call clraddr(pdco2r)
      call clraddr(pcsilop)
      call clraddr(pcmpr2)
      call clraddr(pccbrsp)
      call clraddr(peccurt)
      call clraddr(prm)
      call clraddr(pzm)
      call clraddr(prmt)
      call clraddr(pzmt)
      call clraddr(prv)
      call clraddr(pzv)
      call clraddr(ppsi)
      call clraddr(pbr)
      call clraddr(pbz)
      call clraddr(pbpol)
      call clraddr(pbphi)
      call clraddr(pb)
      call clraddr(pbsqr)
      call clraddr(pb12)
      call clraddr(pb12ctr)
      call clraddr(pb32)
      call clraddr(prmg)
      call clraddr(pzmg)
      call clraddr(ppsig)
      call clraddr(pbrg)
      call clraddr(pbzg)
      call clraddr(pbpolg)
      call clraddr(pbphig)
      call clraddr(pbg)
      call clraddr(pixlb)
      call clraddr(pixpt1)
      call clraddr(pixmdp)
      call clraddr(pixpt2)
      call clraddr(pixrb)
      call clraddr(piysptrx1)
      call clraddr(piysptrx2)
      call clraddr(pvol)
      call clraddr(pgx)
      call clraddr(pgy)
      call clraddr(pdx)
      call clraddr(pdxvf)
      call clraddr(pdy)
      call clraddr(pgxf)
      call clraddr(pgxfn)
      call clraddr(pgyf)
      call clraddr(pgxc)
      call clraddr(pgyc)
      call clraddr(pxnrm)
      call clraddr(pxvnrm)
      call clraddr(pynrm)
      call clraddr(pyvnrm)
      call clraddr(psx)
      call clraddr(psxnp)
      call clraddr(psy)
      call clraddr(prr)
      call clraddr(pxcs)
      call clraddr(pxfs)
      call clraddr(pxcwi)
      call clraddr(pxfwi)
      call clraddr(pxfpf)
      call clraddr(pxcpf)
      call clraddr(pxcwo)
      call clraddr(pxfwo)
      call clraddr(pyyc)
      call clraddr(pyyf)
      call clraddr(pyylb)
      call clraddr(pyyrb)
      call clraddr(pxcv)
      call clraddr(pxfv)
      call clraddr(ppsinormc)
      call clraddr(ppsinormf)
      call clraddr(prrv)
      call clraddr(pvolv)
      call clraddr(phxv)
      call clraddr(psyv)
      call clraddr(pisxptx)
      call clraddr(pisxpty)
      call clraddr(plcon)
      call clraddr(plconi)
      call clraddr(plcone)
      call clraddr(plconneo)
      call clraddr(pepsneo)
      call clraddr(pisixcore)
      call clraddr(plcong)
      call clraddr(plconig)
      call clraddr(plconeg)
      call clraddr(pvtag)
      call clraddr(pangfx)
      call clraddr(pfxm)
      call clraddr(pfx0)
      call clraddr(pfxp)
      call clraddr(pfym)
      call clraddr(pfy0)
      call clraddr(pfyp)
      call clraddr(pfxmy)
      call clraddr(pfxpy)
      call clraddr(pfymx)
      call clraddr(pfypx)
      call clraddr(pfxmv)
      call clraddr(pfx0v)
      call clraddr(pfxpv)
      call clraddr(pfymv)
      call clraddr(pfy0v)
      call clraddr(pfypv)
      call clraddr(pfxmyv)
      call clraddr(pfxpyv)
      call clraddr(pfymxv)
      call clraddr(pfypxv)
      call clraddr(pnibbb)
      call clraddr(ptibbb)
      call clraddr(pnebbb)
      call clraddr(ptebbb)
      call clraddr(pvflowxbbb)
      call clraddr(pvflowybbb)
      call clraddr(pvflowzbbb)
      call clraddr(pfnixbbb)
      call clraddr(pfngysibbb)
      call clraddr(pfngysobbb)
      call clraddr(prlimu)
      call clraddr(pzlimu)
      call clraddr(prsplit1)
      call clraddr(pzsplit1)
      call clraddr(prsplit2)
      call clraddr(pzsplit2)
      call clraddr(ptevb)
      call clraddr(prsi)
      call clraddr(prre)
      call clraddr(prpwr)
      call clraddr(prrcx)
      call clraddr(prtza)
      call clraddr(prtzn)
      call clraddr(prtza2)
      call clraddr(prtt)
      call clraddr(prtn)
      call clraddr(prtlt)
      call clraddr(prtln)
      call clraddr(prtlsa)
      call clraddr(prtlra)
      call clraddr(prtlqa)
      call clraddr(prtlcx)
      call clraddr(pchgstate_format)
      call clraddr(pfcoefne_tanh)
      call clraddr(pfcoefte_tanh)
      call clraddr(pfit_t_bs)
      call clraddr(pfcoef_bs)
      call clraddr(pnefit)
      call clraddr(ptefit)
      call clraddr(ptifit)
      call clraddr(pnefituse)
      call clraddr(ptefituse)
      call clraddr(ptifituse)
      call clraddr(pdumfit)
      call clraddr(ptaudndt)
      call clraddr(ptaudeedt)
      call clraddr(ptaudeidt)
      call clraddr(pepsi_fit)
      call clraddr(ppsi_s)
      call clraddr(pyyc_fit)
      call clraddr(peprofile_fit)

      return
      end
      subroutine comdbcr(drtdm)
cProlog
      integer drtdm
      call rtdbcr(drtdm,21,387)
      return
      end
      subroutine comwake
cProlog
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, 
     &   setlimit
      common /comrtdm/ drtdm

c Group OMFIT
      integer iomfit
      common /com00/ iomfit
c End of OMFIT

c Group COMroutines
c End of COMroutines

c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim

c Group Dimflxgrd
      integer jdim, npts, noregs, nxefit, nyefit, nlim, nbdry, nwork
      common /com30/ jdim, npts, noregs, nxefit, nyefit, nlim, nbdry
      common /com30/ nwork
c End of Dimflxgrd

c Group Comflxgrd
      character*60 runid
      double precision bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      double precision sibdry1, sibdry2, xdim, zdim, zmid, zshift
      integer isfw, kxord, kyord, ldf, iflag, jmin(2), jmax(2)
      character*128 geqdskfname
      double precision rgrid1, cpasma, xlbnd, xubnd, ylbnd, yubnd
      integer jsptrx(2), jaxis
      double precision xold ( nxefit)
      pointer(pxold,xold)
      double precision yold ( nyefit)
      pointer(pyold,yold)
      double precision fold ( nxefit,nyefit)
      pointer(pfold,fold)
      double precision workk ( nxefit)
      pointer(pworkk,workk)
      double precision fpol ( nxefit)
      pointer(pfpol,fpol)
      double precision pres ( nxefit)
      pointer(ppres,pres)
      double precision qpsi ( nxefit)
      pointer(pqpsi,qpsi)
      double precision rbdry ( nbdry)
      pointer(prbdry,rbdry)
      double precision zbdry ( nbdry)
      pointer(pzbdry,zbdry)
      double precision xlim ( nlim)
      pointer(pxlim,xlim)
      double precision ylim ( nlim)
      pointer(pylim,ylim)
      double precision bscoef ( nxefit,nyefit)
      pointer(pbscoef,bscoef)
      double precision xknot ( nxefit+kxord)
      pointer(pxknot,xknot)
      double precision yknot ( nyefit+kyord)
      pointer(pyknot,yknot)
      double precision work ( nwork)
      pointer(pwork,work)
      double precision xcurve ( npts,jdim)
      pointer(pxcurve,xcurve)
      double precision ycurve ( npts,jdim)
      pointer(pycurve,ycurve)
      integer npoint ( jdim)
      pointer(pnpoint,npoint)
      common /com10000/ runid
      common /com10001/ geqdskfname
      common /com40/ isfw, kxord, kyord, ldf, iflag, jmin, jmax, jsptrx
      common /com40/ jaxis
      common /com43/ bcentr, rcentr, rmagx, zmagx, simagx, sibdry
      common /com43/ sibdry1, sibdry2, xdim, zdim, zmid, zshift, rgrid1
      common /com43/ cpasma, xlbnd, xubnd, ylbnd, yubnd
      common /com46/ pxold, pyold, pfold, pworkk
      common /com46/ pfpol, ppres, pqpsi, prbdry
      common /com46/ pzbdry, pxlim, pylim
      common /com46/ pbscoef, pxknot, pyknot
      common /com46/ pwork, pxcurve, pycurve
      common /com46/ pnpoint
c End of Comflxgrd

c Group Aeqflxgrd
      double precision etime, rseps, zseps, rseps1, zseps1, rseps2
      integer vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop, magpri
      character*128 aeqdskfname
      double precision zseps2, rvsin, zvsin, rvsout, zvsout
      integer nfcoil, nesum
      double precision rco2v ( mco2v)
      pointer(prco2v,rco2v)
      double precision dco2v ( mco2v)
      pointer(pdco2v,dco2v)
      double precision rco2r ( mco2r)
      pointer(prco2r,rco2r)
      double precision dco2r ( mco2r)
      pointer(pdco2r,dco2r)
      double precision csilop ( nsilop)
      pointer(pcsilop,csilop)
      double precision cmpr2 ( magpri)
      pointer(pcmpr2,cmpr2)
      double precision ccbrsp ( nfcoil)
      pointer(pccbrsp,ccbrsp)
      double precision eccurt ( nesum)
      pointer(peccurt,eccurt)
      common /com10002/ aeqdskfname
      common /com50/ vmonth, vday, vyear, eshot, mco2v, mco2r, nsilop
      common /com50/ magpri, nfcoil, nesum
      common /com53/ etime, rseps, zseps, rseps1, zseps1, rseps2, zseps2
      common /com53/ rvsin, zvsin, rvsout, zvsout
      common /com56/ prco2v, pdco2v, prco2r
      common /com56/ pdco2r, pcsilop, pcmpr2
      common /com56/ pccbrsp, peccurt
c End of Aeqflxgrd

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

c Group RZ_grid_global
      double precision rmg ( 0:nxm+1,0:nym+1,0:4)
      pointer(prmg,rmg)
      double precision zmg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pzmg,zmg)
      double precision psig ( 0:nxm+1,0:nym+1,0:4)
      pointer(ppsig,psig)
      double precision brg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbrg,brg)
      double precision bzg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbzg,bzg)
      double precision bpolg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbpolg,bpolg)
      double precision bphig ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbphig,bphig)
      double precision bg ( 0:nxm+1,0:nym+1,0:4)
      pointer(pbg,bg)
      common /com76/ prmg, pzmg, ppsig, pbrg
      common /com76/ pbzg, pbpolg, pbphig, pbg
c End of RZ_grid_global

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

c Group Cut_indices
      integer ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2, iycut3
      integer iycut4
      common /com100/ ixcut1, ixcut2, ixcut3, ixcut4, iycut1, iycut2
      common /com100/ iycut3, iycut4
c End of Cut_indices

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

c Group Comgeo_g
      double precision lcong ( 0:nx+1,0:ny+1)
      pointer(plcong,lcong)
      double precision lconig ( 0:nx+1,0:ny+1)
      pointer(plconig,lconig)
      double precision lconeg ( 0:nx+1,0:ny+1)
      pointer(plconeg,lconeg)
      common /com126/ plcong, plconig, plconeg
c End of Comgeo_g

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

c Group Linkbbb
      integer nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb, nxcore1bbb
      character*8 geometrybbb
      integer nxleg2bbb, nxcore2bbb
      double precision nibbb ( 0:nx+1,0:ny+1)
      pointer(pnibbb,nibbb)
      double precision tibbb ( 0:nx+1,0:ny+1)
      pointer(ptibbb,tibbb)
      double precision nebbb ( 0:nx+1,0:ny+1)
      pointer(pnebbb,nebbb)
      double precision tebbb ( 0:nx+1,0:ny+1)
      pointer(ptebbb,tebbb)
      double precision vflowxbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowxbbb,vflowxbbb)
      double precision vflowybbb ( 0:nx+1,0:ny+1)
      pointer(pvflowybbb,vflowybbb)
      double precision vflowzbbb ( 0:nx+1,0:ny+1)
      pointer(pvflowzbbb,vflowzbbb)
      double precision fnixbbb ( 0:nx+1,0:ny+1)
      pointer(pfnixbbb,fnixbbb)
      double precision fngysibbb ( 0:nx+1)
      pointer(pfngysibbb,fngysibbb)
      double precision fngysobbb ( 0:nx+1)
      pointer(pfngysobbb,fngysobbb)
      common /com10007/ geometrybbb
      common /com150/ nxbbb, nybbb, nycorebbb, nysolbbb, nxleg1bbb
      common /com150/ nxcore1bbb, nxleg2bbb, nxcore2bbb
      common /com156/ pnibbb, ptibbb, pnebbb
      common /com156/ ptebbb, pvflowxbbb, pvflowybbb
      common /com156/ pvflowzbbb, pfnixbbb, pfngysibbb
      common /com156/ pfngysobbb
c End of Linkbbb

c Group Timespl
      double precision totb2val, totintrv
      common /com163/ totb2val, totintrv
c End of Timespl

c Group Limiter
      double precision rptnma, zptnma, dslims
      integer nlimu, nptnma, nsplit1, nsplit2
      double precision rlimu ( 1:nlimu)
      pointer(prlimu,rlimu)
      double precision zlimu ( 1:nlimu)
      pointer(pzlimu,zlimu)
      double precision rsplit1 ( nsplit1)
      pointer(prsplit1,rsplit1)
      double precision zsplit1 ( nsplit1)
      pointer(pzsplit1,zsplit1)
      double precision rsplit2 ( nsplit2)
      pointer(prsplit2,rsplit2)
      double precision zsplit2 ( nsplit2)
      pointer(pzsplit2,zsplit2)
      common /com170/ nlimu, nptnma, nsplit1, nsplit2
      common /com173/ rptnma, zptnma, dslims
      common /com176/ prlimu, pzlimu, prsplit1
      common /com176/ pzsplit1, prsplit2, pzsplit2
c End of Limiter

c Group Multicharge
      character*120 labelrt(1:12)
      integer ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      double precision iscxfit
      integer mcfformat(1:12), ispradextrap
      double precision tevb ( ntev)
      pointer(ptevb,tevb)
      double precision rsi ( ntev,0:nz-1)
      pointer(prsi,rsi)
      double precision rre ( ntev,1:nz)
      pointer(prre,rre)
      double precision rpwr ( ntev,0:nz)
      pointer(prpwr,rpwr)
      double precision rrcx ( ntev,1:nz)
      pointer(prrcx,rrcx)
      double precision rtza ( 0:rtnsd-1)
      pointer(prtza,rtza)
      double precision rtzn ( 0:rtnsd-1)
      pointer(prtzn,rtzn)
      double precision rtza2 ( 0:rtnsd-1)
      pointer(prtza2,rtza2)
      double precision rtt ( 0:rtnt)
      pointer(prtt,rtt)
      double precision rtn ( 0:rtnn)
      pointer(prtn,rtn)
      double precision rtlt ( 0:rtnt)
      pointer(prtlt,rtlt)
      double precision rtln ( 0:rtnn)
      pointer(prtln,rtln)
      double precision rtlsa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlsa,rtlsa)
      double precision rtlra ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlra,rtlra)
      double precision rtlqa ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlqa,rtlqa)
      double precision rtlcx ( 0:rtnt,0:rtnn,0:rtnsd-1)
      pointer(prtlcx,rtlcx)
      integer chgstate_format ( 0:rtnsd-1)
      pointer(pchgstate_format,chgstate_format)
      common /com10008/ labelrt
      common /com180/ ntev, nz, rtnt, rtnn, rtns, rtnsd, isrtndep
      common /com180/ mcfformat, ispradextrap
      common /com183/ iscxfit
      common /com186/ ptevb, prsi, prre, prpwr
      common /com186/ prrcx, prtza, prtzn
      common /com186/ prtza2, prtt, prtn, prtlt
      common /com186/ prtln, prtlsa, prtlra
      common /com186/ prtlqa, prtlcx, pchgstate_format
c End of Multicharge

c Group Fitdata
      integer isprof_coef, ncoefne_tanh, ncoefte_tanh, numt_bs, numc_bs
      character*8 fit_paramne_tanh
      character*8 fit_paramte_tanh
      double precision fitfrac1, psishift, tim_interval_fit
      double precision tim_chng_max
      integer numk_bs, isdatfmtnew, isdndtfitdat, ifitset, isprofvspsi
      double precision fcoefne_tanh ( ncoefne_tanh)
      pointer(pfcoefne_tanh,fcoefne_tanh)
      double precision fcoefte_tanh ( ncoefte_tanh)
      pointer(pfcoefte_tanh,fcoefte_tanh)
      double precision fit_t_bs ( numt_bs)
      pointer(pfit_t_bs,fit_t_bs)
      double precision fcoef_bs ( numc_bs)
      pointer(pfcoef_bs,fcoef_bs)
      double precision nefit ( 0:ny+1,2)
      pointer(pnefit,nefit)
      double precision tefit ( 0:ny+1,2)
      pointer(ptefit,tefit)
      double precision tifit ( 0:ny+1,2)
      pointer(ptifit,tifit)
      double precision nefituse ( 0:ny+1)
      pointer(pnefituse,nefituse)
      double precision tefituse ( 0:ny+1)
      pointer(ptefituse,tefituse)
      double precision tifituse ( 0:ny+1)
      pointer(ptifituse,tifituse)
      double precision dumfit ( 0:ny+1)
      pointer(pdumfit,dumfit)
      double precision taudndt ( 0:ny+1)
      pointer(ptaudndt,taudndt)
      double precision taudeedt ( 0:ny+1)
      pointer(ptaudeedt,taudeedt)
      double precision taudeidt ( 0:ny+1)
      pointer(ptaudeidt,taudeidt)
      double precision epsi_fit ( num_elem)
      pointer(pepsi_fit,epsi_fit)
      double precision psi_s ( num_elem)
      pointer(ppsi_s,psi_s)
      double precision yyc_fit ( num_elem)
      pointer(pyyc_fit,yyc_fit)
      double precision eprofile_fit ( num_elem)
      pointer(peprofile_fit,eprofile_fit)
      common /com10009/ fit_paramne_tanh
      common /com10010/ fit_paramte_tanh
      common /com190/ isprof_coef, ncoefne_tanh, ncoefte_tanh, numt_bs
      common /com190/ numc_bs, numk_bs, isdatfmtnew, isdndtfitdat
      common /com190/ ifitset, isprofvspsi
      common /com193/ fitfrac1, psishift, tim_interval_fit, tim_chng_max
      common /com196/ pfcoefne_tanh, pfcoefte_tanh
      common /com196/ pfit_t_bs, pfcoef_bs, pnefit
      common /com196/ ptefit, ptifit, pnefituse
      common /com196/ ptefituse, ptifituse, pdumfit
      common /com196/ ptaudndt, ptaudeedt, ptaudeidt
      common /com196/ pepsi_fit, ppsi_s, pyyc_fit
      common /com196/ peprofile_fit
c End of Fitdata

c Group Subs2
c End of Subs2



      integer*8 i000addr
      external varadr
      integer*8 varadr


      call comdbcr(drtdm)
      jgrp=rtgrpe(drtdm,"OMFIT")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iomfit",varadr(iomfit),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"COMroutines")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "glbwrlog",jgrp,'double precision',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'ioun:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Dim")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nx",varadr(nx),0,'integer','scalar', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ny",varadr(ny),0,'integer','scalar', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxm",varadr(nxm),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nym",varadr(nym),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxpt",varadr(nxpt),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nhsp",varadr(nhsp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( nzsp )
      i0001234=rtvare(drtdm,"nzsp",i000addr,0,'integer','(1:6-1)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzspt",varadr(nzspt),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzspmx",varadr(nzspmx),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nisp",varadr(nisp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nusp",varadr(nusp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nfsp",varadr(nfsp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ngsp",varadr(ngsp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+restart')
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"nhgsp",varadr(nhgsp),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"imx",varadr(imx),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"imy",varadr(imy),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"lnst",varadr(lnst),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"num_elem",varadr(num_elem),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Dimflxgrd")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jdim",varadr(jdim),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"npts",varadr(npts),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"noregs",varadr(noregs),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxefit",varadr(nxefit),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nyefit",varadr(nyefit),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nlim",varadr(nlim),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nbdry",varadr(nbdry),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nwork",varadr(nwork),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Comflxgrd")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isfw",varadr(isfw),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"runid",varadr(runid),0,'character*60',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxold )
      i0001234=rtvare(drtdm,"xold",i000addr,1,'double precision',
     &   '(nxefit)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyold )
      i0001234=rtvare(drtdm,"yold",i000addr,1,'double precision',
     &   '(nyefit)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfold )
      i0001234=rtvare(drtdm,"fold",i000addr,1,'double precision',
     &   '(nxefit,nyefit)', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"bcentr",varadr(bcentr),0,'double precision'
     &   ,'scalar', "Tesla")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rcentr",varadr(rcentr),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rmagx",varadr(rmagx),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zmagx",varadr(zmagx),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"simagx",varadr(simagx),0,'double precision'
     &   ,'scalar', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sibdry",varadr(sibdry),0,'double precision'
     &   ,'scalar', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sibdry1",varadr(sibdry1),0,
     &   'double precision','scalar', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sibdry2",varadr(sibdry2),0,
     &   'double precision','scalar', "volt-sec/radian")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xdim",varadr(xdim),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zdim",varadr(zdim),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zmid",varadr(zmid),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zshift",varadr(zshift),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pworkk )
      i0001234=rtvare(drtdm,"workk",i000addr,1,'double precision',
     &   '(nxefit)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfpol )
      i0001234=rtvare(drtdm,"fpol",i000addr,1,'double precision',
     &   '(nxefit)', "m-T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppres )
      i0001234=rtvare(drtdm,"pres",i000addr,1,'double precision',
     &   '(nxefit)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pqpsi )
      i0001234=rtvare(drtdm,"qpsi",i000addr,1,'double precision',
     &   '(nxefit)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rgrid1",varadr(rgrid1),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"cpasma",varadr(cpasma),0,'double precision'
     &   ,'scalar', "Amps")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prbdry )
      i0001234=rtvare(drtdm,"rbdry",i000addr,1,'double precision',
     &   '(nbdry)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzbdry )
      i0001234=rtvare(drtdm,"zbdry",i000addr,1,'double precision',
     &   '(nbdry)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxlim )
      i0001234=rtvare(drtdm,"xlim",i000addr,1,'double precision',
     &   '(nlim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pylim )
      i0001234=rtvare(drtdm,"ylim",i000addr,1,'double precision',
     &   '(nlim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbscoef )
      i0001234=rtvare(drtdm,"bscoef",i000addr,1,'double precision',
     &   '(nxefit,nyefit)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kxord",varadr(kxord),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"kyord",varadr(kyord),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxknot )
      i0001234=rtvare(drtdm,"xknot",i000addr,1,'double precision',
     &   '(nxefit+kxord)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyknot )
      i0001234=rtvare(drtdm,"yknot",i000addr,1,'double precision',
     &   '(nyefit+kyord)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ldf",varadr(ldf),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iflag",varadr(iflag),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pwork )
      i0001234=rtvare(drtdm,"work",i000addr,1,'double precision',
     &   '(nwork)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( jmin )
      i0001234=rtvare(drtdm,"jmin",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( jmax )
      i0001234=rtvare(drtdm,"jmax",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( jsptrx )
      i0001234=rtvare(drtdm,"jsptrx",i000addr,0,'integer','(2)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"jaxis",varadr(jaxis),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xlbnd",varadr(xlbnd),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"xubnd",varadr(xubnd),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ylbnd",varadr(ylbnd),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"yubnd",varadr(yubnd),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcurve )
      i0001234=rtvare(drtdm,"xcurve",i000addr,1,'double precision',
     &   '(npts,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pycurve )
      i0001234=rtvare(drtdm,"ycurve",i000addr,1,'double precision',
     &   '(npts,jdim)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnpoint )
      i0001234=rtvare(drtdm,"npoint",i000addr,1,'integer','(jdim)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"geqdskfname",varadr(geqdskfname),0,
     &   'character*128','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Aeqflxgrd")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"vmonth",varadr(vmonth),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"vday",varadr(vday),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"vyear",varadr(vyear),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"eshot",varadr(eshot),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"etime",varadr(etime),0,'double precision',
     &   'scalar', "msec")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rseps",varadr(rseps),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zseps",varadr(zseps),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rseps1",varadr(rseps1),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zseps1",varadr(zseps1),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rseps2",varadr(rseps2),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zseps2",varadr(zseps2),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rvsin",varadr(rvsin),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zvsin",varadr(zvsin),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rvsout",varadr(rvsout),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zvsout",varadr(zvsout),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mco2v",varadr(mco2v),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"mco2r",varadr(mco2r),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prco2v )
      i0001234=rtvare(drtdm,"rco2v",i000addr,1,'double precision',
     &   '(mco2v)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdco2v )
      i0001234=rtvare(drtdm,"dco2v",i000addr,1,'double precision',
     &   '(mco2v)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prco2r )
      i0001234=rtvare(drtdm,"rco2r",i000addr,1,'double precision',
     &   '(mco2r)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdco2r )
      i0001234=rtvare(drtdm,"dco2r",i000addr,1,'double precision',
     &   '(mco2r)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nsilop",varadr(nsilop),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcsilop )
      i0001234=rtvare(drtdm,"csilop",i000addr,1,'double precision',
     &   '(nsilop)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"magpri",varadr(magpri),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pcmpr2 )
      i0001234=rtvare(drtdm,"cmpr2",i000addr,1,'double precision',
     &   '(magpri)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nfcoil",varadr(nfcoil),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pccbrsp )
      i0001234=rtvare(drtdm,"ccbrsp",i000addr,1,'double precision',
     &   '(nfcoil)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nesum",varadr(nesum),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( peccurt )
      i0001234=rtvare(drtdm,"eccurt",i000addr,1,'double precision',
     &   '(nesum)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"aeqdskfname",varadr(aeqdskfname),0,
     &   'character*128','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"RZ_grid_info")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( prm )
      i0001234=rtvare(drtdm,"rm",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzm )
      i0001234=rtvare(drtdm,"zm",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prmt )
      i0001234=rtvare(drtdm,"rmt",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzmt )
      i0001234=rtvare(drtdm,"zmt",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prv )
      i0001234=rtvare(drtdm,"rv",i000addr,1,'double precision',
     &   '(0:nxm+2,-1:nym+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzv )
      i0001234=rtvare(drtdm,"zv",i000addr,1,'double precision',
     &   '(0:nxm+2,-1:nym+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsi )
      i0001234=rtvare(drtdm,"psi",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "Tm^2")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbr )
      i0001234=rtvare(drtdm,"br",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbz )
      i0001234=rtvare(drtdm,"bz",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbpol )
      i0001234=rtvare(drtdm,"bpol",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbphi )
      i0001234=rtvare(drtdm,"bphi",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pb )
      i0001234=rtvare(drtdm,"b",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbsqr )
      i0001234=rtvare(drtdm,"bsqr",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pb12 )
      i0001234=rtvare(drtdm,"b12",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pb12ctr )
      i0001234=rtvare(drtdm,"b12ctr",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pb32 )
      i0001234=rtvare(drtdm,"b32",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1)', "T")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"RZ_grid_global")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( prmg )
      i0001234=rtvare(drtdm,"rmg",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzmg )
      i0001234=rtvare(drtdm,"zmg",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsig )
      i0001234=rtvare(drtdm,"psig",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "Tm^2")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbrg )
      i0001234=rtvare(drtdm,"brg",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbzg )
      i0001234=rtvare(drtdm,"bzg",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbpolg )
      i0001234=rtvare(drtdm,"bpolg",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbphig )
      i0001234=rtvare(drtdm,"bphig",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pbg )
      i0001234=rtvare(drtdm,"bg",i000addr,1,'double precision',
     &   '(0:nxm+1,0:nym+1,0:4)', "T")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Share")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( nycore )
      i0001234=rtvare(drtdm,"nycore",i000addr,0,'integer','(30)', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i000addr = varadr ( nysol )
      i0001234=rtvare(drtdm,"nysol",i000addr,0,'integer','(30)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i000addr = varadr ( nyout )
      i0001234=rtvare(drtdm,"nyout",i000addr,0,'integer','(30)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i000addr = varadr ( nxleg )
      i0001234=rtvare(drtdm,"nxleg",i000addr,0,'integer','(30,2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i000addr = varadr ( nxcore )
      i0001234=rtvare(drtdm,"nxcore",i000addr,0,'integer','(30,2)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+regrid')
      i0001234=rtvare(drtdm,"nxomit",varadr(nxomit),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxxpt",varadr(nxxpt),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nyomitmx",varadr(nyomitmx),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"igrid",varadr(igrid),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"geometry",varadr(geometry),0,'character*16'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxc",varadr(nxc),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"simagxs",varadr(simagxs),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sibdrys",varadr(sibdrys),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ismpsym",varadr(ismpsym),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isudsym",varadr(isudsym),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"islimon",varadr(islimon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ix_lim",varadr(ix_lim),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iy_lims",varadr(iy_lims),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"theta_split",varadr(theta_split),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isnonog",varadr(isnonog),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ismmon",varadr(ismmon),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isoldgrid",varadr(isoldgrid),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isgrdsym",varadr(isgrdsym),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"cutlo",varadr(cutlo),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"epslon",varadr(epslon),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"spheromak",varadr(spheromak),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isfrc",varadr(isfrc),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ishalfm",varadr(ishalfm),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isbphicon",varadr(isbphicon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nhdf",varadr(nhdf),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( hdfilename )
      i0001234=rtvare(drtdm,"hdfilename",i000addr,0,'character*(256)',
     &   '(1:12)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nzdf",varadr(nzdf),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( mcfilename )
      i0001234=rtvare(drtdm,"mcfilename",i000addr,0,'character*(256)',
     &   '(1:12)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"coronalimpfname",varadr(coronalimpfname),0,
     &   'character*120','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istabon",varadr(istabon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      call rtvattre(i0001234,drtdm,'+restart')
      i0001234=rtvare(drtdm,"reset_core_og",varadr(reset_core_og),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Xpoint_indices")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pixlb )
      i0001234=rtvare(drtdm,"ixlb",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixpt1 )
      i0001234=rtvare(drtdm,"ixpt1",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixmdp )
      i0001234=rtvare(drtdm,"ixmdp",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixpt2 )
      i0001234=rtvare(drtdm,"ixpt2",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pixrb )
      i0001234=rtvare(drtdm,"ixrb",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piysptrx1 )
      i0001234=rtvare(drtdm,"iysptrx1",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( piysptrx2 )
      i0001234=rtvare(drtdm,"iysptrx2",i000addr,1,'integer','(1:nxpt)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iysptrx",varadr(iysptrx),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Cut_indices")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixcut1",varadr(ixcut1),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixcut2",varadr(ixcut2),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixcut3",varadr(ixcut3),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ixcut4",varadr(ixcut4),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iycut1",varadr(iycut1),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iycut2",varadr(iycut2),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iycut3",varadr(iycut3),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iycut4",varadr(iycut4),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Comgeo")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pvol )
      i0001234=rtvare(drtdm,"vol",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgx )
      i0001234=rtvare(drtdm,"gx",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgy )
      i0001234=rtvare(drtdm,"gy",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdx )
      i0001234=rtvare(drtdm,"dx",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdxvf )
      i0001234=rtvare(drtdm,"dxvf",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdy )
      i0001234=rtvare(drtdm,"dy",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgxf )
      i0001234=rtvare(drtdm,"gxf",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgxfn )
      i0001234=rtvare(drtdm,"gxfn",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgyf )
      i0001234=rtvare(drtdm,"gyf",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgxc )
      i0001234=rtvare(drtdm,"gxc",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pgyc )
      i0001234=rtvare(drtdm,"gyc",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxnrm )
      i0001234=rtvare(drtdm,"xnrm",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxvnrm )
      i0001234=rtvare(drtdm,"xvnrm",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pynrm )
      i0001234=rtvare(drtdm,"ynrm",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyvnrm )
      i0001234=rtvare(drtdm,"yvnrm",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psx )
      i0001234=rtvare(drtdm,"sx",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^2")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psxnp )
      i0001234=rtvare(drtdm,"sxnp",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^2")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psy )
      i0001234=rtvare(drtdm,"sy",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m^2")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prr )
      i0001234=rtvare(drtdm,"rr",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcs )
      i0001234=rtvare(drtdm,"xcs",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxfs )
      i0001234=rtvare(drtdm,"xfs",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcwi )
      i0001234=rtvare(drtdm,"xcwi",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxfwi )
      i0001234=rtvare(drtdm,"xfwi",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxfpf )
      i0001234=rtvare(drtdm,"xfpf",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcpf )
      i0001234=rtvare(drtdm,"xcpf",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcwo )
      i0001234=rtvare(drtdm,"xcwo",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxfwo )
      i0001234=rtvare(drtdm,"xfwo",i000addr,1,'double precision',
     &   '(0:nx+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyyc )
      i0001234=rtvare(drtdm,"yyc",i000addr,1,'double precision',
     &   '(0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyyf )
      i0001234=rtvare(drtdm,"yyf",i000addr,1,'double precision',
     &   '(0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyylb )
      i0001234=rtvare(drtdm,"yylb",i000addr,1,'double precision',
     &   '(0:ny+1,1:nxpt)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pyyrb )
      i0001234=rtvare(drtdm,"yyrb",i000addr,1,'double precision',
     &   '(0:ny+1,1:nxpt)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxcv )
      i0001234=rtvare(drtdm,"xcv",i000addr,1,'double precision',
     &   '(0:nx+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pxfv )
      i0001234=rtvare(drtdm,"xfv",i000addr,1,'double precision',
     &   '(0:nx+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsinormc )
      i0001234=rtvare(drtdm,"psinormc",i000addr,1,'double precision',
     &   '(0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ppsinormf )
      i0001234=rtvare(drtdm,"psinormf",i000addr,1,'double precision',
     &   '(0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prrv )
      i0001234=rtvare(drtdm,"rrv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pvolv )
      i0001234=rtvare(drtdm,"volv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( phxv )
      i0001234=rtvare(drtdm,"hxv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "1/m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( psyv )
      i0001234=rtvare(drtdm,"syv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sygytotc",varadr(sygytotc),0,
     &   'double precision','scalar', "1/m**3")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"area_core",varadr(area_core),0,
     &   'double precision','scalar', "1/m**3")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ghxpt",varadr(ghxpt),0,'double precision',
     &   'scalar', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"gvxpt",varadr(gvxpt),0,'double precision',
     &   'scalar', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sxyxpt",varadr(sxyxpt),0,'double precision'
     &   ,'scalar', "m^2")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ghxpt_lower",varadr(ghxpt_lower),0,
     &   'double precision','scalar', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"gvxpt_lower",varadr(gvxpt_lower),0,
     &   'double precision','scalar', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sxyxpt_lower",varadr(sxyxpt_lower),0,
     &   'double precision','scalar', "m^2")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ghxpt_upper",varadr(ghxpt_upper),0,
     &   'double precision','scalar', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"gvxpt_upper",varadr(gvxpt_upper),0,
     &   'double precision','scalar', "m^-1")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"sxyxpt_upper",varadr(sxyxpt_upper),0,
     &   'double precision','scalar', "m^2")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"linelen",varadr(linelen),0,
     &   'double precision','scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pisxptx )
      i0001234=rtvare(drtdm,"isxptx",i000addr,1,'integer',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pisxpty )
      i0001234=rtvare(drtdm,"isxpty",i000addr,1,'integer',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plcon )
      i0001234=rtvare(drtdm,"lcon",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plconi )
      i0001234=rtvare(drtdm,"lconi",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plcone )
      i0001234=rtvare(drtdm,"lcone",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plconneo )
      i0001234=rtvare(drtdm,"lconneo",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pepsneo )
      i0001234=rtvare(drtdm,"epsneo",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pisixcore )
      i0001234=rtvare(drtdm,"isixcore",i000addr,1,'integer','(0:nx+1)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dxmin",varadr(dxmin),0,'double precision',
     &   'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Comgeo_g")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( plcong )
      i0001234=rtvare(drtdm,"lcong",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plconig )
      i0001234=rtvare(drtdm,"lconig",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( plconeg )
      i0001234=rtvare(drtdm,"lconeg",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Noggeo")
      if (jgrp .eq. 0) go to 999
      i000addr = varadr ( pvtag )
      i0001234=rtvare(drtdm,"vtag",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pangfx )
      i0001234=rtvare(drtdm,"angfx",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxm )
      i0001234=rtvare(drtdm,"fxm",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfx0 )
      i0001234=rtvare(drtdm,"fx0",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxp )
      i0001234=rtvare(drtdm,"fxp",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfym )
      i0001234=rtvare(drtdm,"fym",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfy0 )
      i0001234=rtvare(drtdm,"fy0",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfyp )
      i0001234=rtvare(drtdm,"fyp",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxmy )
      i0001234=rtvare(drtdm,"fxmy",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxpy )
      i0001234=rtvare(drtdm,"fxpy",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfymx )
      i0001234=rtvare(drtdm,"fymx",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfypx )
      i0001234=rtvare(drtdm,"fypx",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxmv )
      i0001234=rtvare(drtdm,"fxmv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfx0v )
      i0001234=rtvare(drtdm,"fx0v",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxpv )
      i0001234=rtvare(drtdm,"fxpv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfymv )
      i0001234=rtvare(drtdm,"fymv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfy0v )
      i0001234=rtvare(drtdm,"fy0v",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfypv )
      i0001234=rtvare(drtdm,"fypv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxmyv )
      i0001234=rtvare(drtdm,"fxmyv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfxpyv )
      i0001234=rtvare(drtdm,"fxpyv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfymxv )
      i0001234=rtvare(drtdm,"fymxv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfypxv )
      i0001234=rtvare(drtdm,"fypxv",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1,0:1)', " ")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Timing")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"istimingon",varadr(istimingon),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iprinttim",varadr(iprinttim),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttotfe",varadr(ttotfe),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttimpfe",varadr(ttimpfe),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttotjf",varadr(ttotjf),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttimpjf",varadr(ttimpjf),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttmatfac",varadr(ttmatfac),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttmatsol",varadr(ttmatsol),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttjstor",varadr(ttjstor),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttjrnorm",varadr(ttjrnorm),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttjreorder",varadr(ttjreorder),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttimpc",varadr(ttimpc),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tstart",varadr(tstart),0,'double precision'
     &   ,'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tend",varadr(tend),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttnpg",varadr(ttnpg),0,'double precision',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttngxlog",varadr(ttngxlog),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttngylog",varadr(ttngylog),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttngfd2",varadr(ttngfd2),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ttngfxy",varadr(ttngfxy),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Linkbbb")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxbbb",varadr(nxbbb),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nybbb",varadr(nybbb),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nycorebbb",varadr(nycorebbb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nysolbbb",varadr(nysolbbb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxleg1bbb",varadr(nxleg1bbb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxcore1bbb",varadr(nxcore1bbb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxleg2bbb",varadr(nxleg2bbb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nxcore2bbb",varadr(nxcore2bbb),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"geometrybbb",varadr(geometrybbb),0,
     &   'character*8','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnibbb )
      i0001234=rtvare(drtdm,"nibbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptibbb )
      i0001234=rtvare(drtdm,"tibbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnebbb )
      i0001234=rtvare(drtdm,"nebbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptebbb )
      i0001234=rtvare(drtdm,"tebbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pvflowxbbb )
      i0001234=rtvare(drtdm,"vflowxbbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pvflowybbb )
      i0001234=rtvare(drtdm,"vflowybbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pvflowzbbb )
      i0001234=rtvare(drtdm,"vflowzbbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfnixbbb )
      i0001234=rtvare(drtdm,"fnixbbb",i000addr,1,'double precision',
     &   '(0:nx+1,0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfngysibbb )
      i0001234=rtvare(drtdm,"fngysibbb",i000addr,1,'double precision',
     &   '(0:nx+1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfngysobbb )
      i0001234=rtvare(drtdm,"fngysobbb",i000addr,1,'double precision',
     &   '(0:nx+1)', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Timespl")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"totb2val",varadr(totb2val),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"totintrv",varadr(totintrv),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Limiter")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nlimu",varadr(nlimu),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prlimu )
      i0001234=rtvare(drtdm,"rlimu",i000addr,1,'double precision',
     &   '(1:nlimu)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzlimu )
      i0001234=rtvare(drtdm,"zlimu",i000addr,1,'double precision',
     &   '(1:nlimu)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nptnma",varadr(nptnma),0,'integer','scalar'
     &   , "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rptnma",varadr(rptnma),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"zptnma",varadr(zptnma),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"dslims",varadr(dslims),0,'double precision'
     &   ,'scalar', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nsplit1",varadr(nsplit1),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prsplit1 )
      i0001234=rtvare(drtdm,"rsplit1",i000addr,1,'double precision',
     &   '(nsplit1)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzsplit1 )
      i0001234=rtvare(drtdm,"zsplit1",i000addr,1,'double precision',
     &   '(nsplit1)', "m")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nsplit2",varadr(nsplit2),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prsplit2 )
      i0001234=rtvare(drtdm,"rsplit2",i000addr,1,'double precision',
     &   '(nsplit2)', "m")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pzsplit2 )
      i0001234=rtvare(drtdm,"zsplit2",i000addr,1,'double precision',
     &   '(nsplit2)', "m")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Multicharge")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ntev",varadr(ntev),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"nz",varadr(nz),0,'integer','scalar', "none"
     &   )
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptevb )
      i0001234=rtvare(drtdm,"tevb",i000addr,1,'double precision',
     &   '(ntev)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prsi )
      i0001234=rtvare(drtdm,"rsi",i000addr,1,'double precision',
     &   '(ntev,0:nz-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prre )
      i0001234=rtvare(drtdm,"rre",i000addr,1,'double precision',
     &   '(ntev,1:nz)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prpwr )
      i0001234=rtvare(drtdm,"rpwr",i000addr,1,'double precision',
     &   '(ntev,0:nz)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prrcx )
      i0001234=rtvare(drtdm,"rrcx",i000addr,1,'double precision',
     &   '(ntev,1:nz)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( labelrt )
      i0001234=rtvare(drtdm,"labelrt",i000addr,0,'character*120',
     &   '(1:12)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rtnt",varadr(rtnt),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rtnn",varadr(rtnn),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rtns",varadr(rtns),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"rtnsd",varadr(rtnsd),0,'integer','scalar', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtza )
      i0001234=rtvare(drtdm,"rtza",i000addr,1,'double precision',
     &   '(0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtzn )
      i0001234=rtvare(drtdm,"rtzn",i000addr,1,'double precision',
     &   '(0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtza2 )
      i0001234=rtvare(drtdm,"rtza2",i000addr,1,'double precision',
     &   '(0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtt )
      i0001234=rtvare(drtdm,"rtt",i000addr,1,'double precision',
     &   '(0:rtnt)', "eV")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtn )
      i0001234=rtvare(drtdm,"rtn",i000addr,1,'double precision',
     &   '(0:rtnn)', "/m**3")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtlt )
      i0001234=rtvare(drtdm,"rtlt",i000addr,1,'double precision',
     &   '(0:rtnt)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtln )
      i0001234=rtvare(drtdm,"rtln",i000addr,1,'double precision',
     &   '(0:rtnn)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtlsa )
      i0001234=rtvare(drtdm,"rtlsa",i000addr,1,'double precision',
     &   '(0:rtnt,0:rtnn,0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtlra )
      i0001234=rtvare(drtdm,"rtlra",i000addr,1,'double precision',
     &   '(0:rtnt,0:rtnn,0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtlqa )
      i0001234=rtvare(drtdm,"rtlqa",i000addr,1,'double precision',
     &   '(0:rtnt,0:rtnn,0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( prtlcx )
      i0001234=rtvare(drtdm,"rtlcx",i000addr,1,'double precision',
     &   '(0:rtnt,0:rtnn,0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"iscxfit",varadr(iscxfit),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isrtndep",varadr(isrtndep),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( mcfformat )
      i0001234=rtvare(drtdm,"mcfformat",i000addr,0,'integer','(1:12)', 
     &   "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pchgstate_format )
      i0001234=rtvare(drtdm,"chgstate_format",i000addr,1,'integer',
     &   '(0:rtnsd-1)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ispradextrap",varadr(ispradextrap),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      jgrp=rtgrpe(drtdm,"Fitdata")
      if (jgrp .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isprof_coef",varadr(isprof_coef),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncoefne_tanh",varadr(ncoefne_tanh),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ncoefte_tanh",varadr(ncoefte_tanh),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"numt_bs",varadr(numt_bs),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"numc_bs",varadr(numc_bs),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"numk_bs",varadr(numk_bs),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfcoefne_tanh )
      i0001234=rtvare(drtdm,"fcoefne_tanh",i000addr,1,'double precision'
     &   ,'(ncoefne_tanh)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfcoefte_tanh )
      i0001234=rtvare(drtdm,"fcoefte_tanh",i000addr,1,'double precision'
     &   ,'(ncoefte_tanh)', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"fit_paramne_tanh",varadr(fit_paramne_tanh),
     &   0,'character*8','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"fit_paramte_tanh",varadr(fit_paramte_tanh),
     &   0,'character*8','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfit_t_bs )
      i0001234=rtvare(drtdm,"fit_t_bs",i000addr,1,'double precision',
     &   '(numt_bs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pfcoef_bs )
      i0001234=rtvare(drtdm,"fcoef_bs",i000addr,1,'double precision',
     &   '(numc_bs)', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pnefit )
      i0001234=rtvare(drtdm,"nefit",i000addr,1,'double precision',
     &   '(0:ny+1,2)', "m**-3")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( ptefit )
      i0001234=rtvare(drtdm,"tefit",i000addr,1,'double precision',
     &   '(0:ny+1,2)', "keV")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( ptifit )
      i0001234=rtvare(drtdm,"tifit",i000addr,1,'double precision',
     &   '(0:ny+1,2)', "keV")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( pnefituse )
      i0001234=rtvare(drtdm,"nefituse",i000addr,1,'double precision',
     &   '(0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( ptefituse )
      i0001234=rtvare(drtdm,"tefituse",i000addr,1,'double precision',
     &   '(0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( ptifituse )
      i0001234=rtvare(drtdm,"tifituse",i000addr,1,'double precision',
     &   '(0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i0001234=rtvare(drtdm,"fitfrac1",varadr(fitfrac1),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pdumfit )
      i0001234=rtvare(drtdm,"dumfit",i000addr,1,'double precision',
     &   '(0:ny+1)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i0001234=rtvare(drtdm,"isdatfmtnew",varadr(isdatfmtnew),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"psishift",varadr(psishift),0,
     &   'double precision','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"isdndtfitdat",varadr(isdndtfitdat),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"ifitset",varadr(ifitset),0,'integer',
     &   'scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tim_interval_fit",varadr(tim_interval_fit),
     &   0,'double precision','scalar', "s")
      if (i0001234 .eq. 0) go to 999
      i0001234=rtvare(drtdm,"tim_chng_max",varadr(tim_chng_max),0,
     &   'double precision','scalar', "s")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( ptaudndt )
      i0001234=rtvare(drtdm,"taudndt",i000addr,1,'double precision',
     &   '(0:ny+1)', "s")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,1.d50)
      i000addr = varadr ( ptaudeedt )
      i0001234=rtvare(drtdm,"taudeedt",i000addr,1,'double precision',
     &   '(0:ny+1)', "s")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,1.d50)
      i000addr = varadr ( ptaudeidt )
      i0001234=rtvare(drtdm,"taudeidt",i000addr,1,'double precision',
     &   '(0:ny+1)', "s")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,1.d50)
      i0001234=rtvare(drtdm,"isprofvspsi",varadr(isprofvspsi),0,
     &   'integer','scalar', "none")
      if (i0001234 .eq. 0) go to 999
      i000addr = varadr ( pepsi_fit )
      i0001234=rtvare(drtdm,"epsi_fit",i000addr,1,'double precision',
     &   '(num_elem)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( ppsi_s )
      i0001234=rtvare(drtdm,"psi_s",i000addr,1,'double precision',
     &   '(num_elem)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( pyyc_fit )
      i0001234=rtvare(drtdm,"yyc_fit",i000addr,1,'double precision',
     &   '(num_elem)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      i000addr = varadr ( peprofile_fit )
      i0001234=rtvare(drtdm,"eprofile_fit",i000addr,1,'double precision'
     &   ,'(num_elem)', "none")
      if (i0001234 .eq. 0) go to 999
      call rtdynset(i0001234,drtdm,0.d0)
      jgrp=rtgrpe(drtdm,"Subs2")
      if (jgrp .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "xerrab",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'msg:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_msg_:integer')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "readne_dat",jgrp,'null',"none")
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
      jvar = rtfcne1(drtdm, "readte_dat",jgrp,'null',"none")
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
      jvar = rtfcne1(drtdm, "readti_dat",jgrp,'null',"none")
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
      jvar = rtfcne1(drtdm, "fit_neteti",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      jvar = rtfcne1(drtdm, "tanh_multi",jgrp,'null',"none")
      if (jvar .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'i:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'a:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'j:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'b:double precision,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'fname:String,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'l_fname_:integer,')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , 'd:double precision')
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if (i0001234 .eq. 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if (i0001234 .eq. 0) go to 999
      call rtsetdoc(drtdm,"com.cmt")
      return
  999 continue
      call baderr("Error initializing variable in database")
      end
      subroutine comxpf(iseg,name1234)
cProlog
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if (iseg.eq.2) then
         call comxp2(name1234)
      elseif (iseg.eq.21) then
         call comxp21(name1234)
      else
         call baderr('comxpf: impossible event')
      endif
      return
      end
      subroutine comxp2(name1234)
cProlog
      character*(*) name1234
      external com_handler
      external glbwrlog
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'glbwrlog') then
         call parexecf(com_handler, 0, glbwrlog)
      else
         call baderr('comxp2: impossible event: '//name5678)
      endif
      return
      end
      subroutine comxp21(name1234)
cProlog
      character*(*) name1234
      external com_handler
      external xerrab
      external readne_dat
      external readte_dat
      external readti_dat
      external fit_neteti
      external tanh_multi
      character*8 name5678
      name5678=name1234
      if (name1234 .eq. 'xerrab') then
         call parexecf(com_handler, 1, xerrab)
      elseif (name1234 .eq. 'readne_dat') then
         call parexecf(com_handler, 2, readne_dat)
      elseif (name1234 .eq. 'readte_dat') then
         call parexecf(com_handler, 3, readte_dat)
      elseif (name1234 .eq. 'readti_dat') then
         call parexecf(com_handler, 4, readti_dat)
      elseif (name1234 .eq. 'fit_neteti') then
         call parexecf(com_handler, 5, fit_neteti)
      elseif (name1234 .eq. 'tanh_multi') then
         call parexecf(com_handler, 6, tanh_multi)
      else
         call baderr('comxp21: impossible event: '//name5678)
      endif
      return
      end
      function combfcn(ss,sp,nargs,name1234,sx)
cProlog
      integer combfcn,ss(26,1),sp,nargs
      integer sx(26)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in com')
      call baderr(name1234)
      combfcn = -1
      return
      end
