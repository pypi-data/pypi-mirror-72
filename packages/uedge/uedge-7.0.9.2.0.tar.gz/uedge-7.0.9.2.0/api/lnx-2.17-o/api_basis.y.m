      subroutine apiinit0
c initializes a Package
      integer drtdm
      common /apirtdm/ drtdm
      Ch(32) lngn
      integer glbpknum,glbstat,izverbos
      external glbpknum,glbstat,izverbos
      drtdm = glbpknum("api")
      if (glbstat(drtdm) .ne. SLEEPING) return
      call glblngn(drtdm,lngn)
      if(izverbos(0).gt.0) call remark('Initializing '//lngn)
c initialize our run-time database manager
      call apidata
      call apiwake
c set our status
      call glbsstat(drtdm,UP)
c call user's initialization routine
      call glbinit(drtdm)
      return
      end
define([Use_All_Groups_api],[
Use(Dim_vars)
Use(Physical_constants2)
Use(Normalization_constants)
Use(Impfcn)
Use(Impurity_transport)
Use(Impurity_source)
Use(Sources_at_walls)
Use(Input)
Use(Radiation)
Use(Impdata)
Use(MC_subs)
Use(Impurity_charge)
Use(P93dat)
Use(Imslwrk)
Use(P93fcn)
Use(Reduced_ion_constants)
Use(Reduced_ion_variables)
Use(Cyield)
Use(Sputt_subs)
Use(Emissivities)
Use(Pixels)
])
      block data apiiyiyi
# Replace pointer statements with Address types
define([Dynamic],[Address Point([$1])])
Use_All_Groups_api
      data ev2/1.6022e-19/,qe2/1.6022e-19/
      data dnimp/1./,methimp/33/,csexpn/0./
      data nzsor/0/
      data inelrates/'edgrat.dat'/,inelrad/'carbavg.dat'/
      data inelmc/'carbmc.dat'/
      data ncaset/40/,ncaseno/40/,ncasent/40/
      data apidir/"."/
      data nnz/2/
      data icont/0/,kxords/4/,kyords/4/,kzords/4/
      data redf_haas/0.2/

      end
# restore definition from mppl.BASIS
define([Dynamic],[\
[$2] [$1] ifelse([$3],,,([$3]));\
pointer(Point([$1]),[$1])\
])
      subroutine apidata
Use_All_Groups_api
      external apiiyiyi
      integer iyiyiyi
      iyiyiyi = 1

      call clraddr(Point(simpfix))
      call clraddr(Point(iszsorlb))
      call clraddr(Point(jxzsori))
      call clraddr(Point(jxzsoro))
      call clraddr(Point(ixzbegi))
      call clraddr(Point(ixzendi))
      call clraddr(Point(ixzbego))
      call clraddr(Point(ixzendo))
      call clraddr(Point(ximpi))
      call clraddr(Point(ximpo))
      call clraddr(Point(wimpi))
      call clraddr(Point(wimpo))
      call clraddr(Point(impsori))
      call clraddr(Point(impsoro))
      call clraddr(Point(zq))
      call clraddr(Point(tdatm))
      call clraddr(Point(rdatm))
      call clraddr(Point(ndatm))
      call clraddr(Point(emdatm))
      call clraddr(Point(z1datm))
      call clraddr(Point(z2datm))
      call clraddr(Point(xdata))
      call clraddr(Point(ydata))
      call clraddr(Point(zdata))
      call clraddr(Point(fdata))
      call clraddr(Point(work2))
      call clraddr(Point(work3))
      call clraddr(Point(xknots))
      call clraddr(Point(yknots))
      call clraddr(Point(zknots))
      call clraddr(Point(emcoef))
      call clraddr(Point(z1coef))
      call clraddr(Point(z2coef))
      call clraddr(Point(etemp))
      call clraddr(Point(lamb))
      call clraddr(Point(eden))
      call clraddr(Point(rate))
      call clraddr(Point(emiss))
      call clraddr(Point(npd))
      call clraddr(Point(rp1))
      call clraddr(Point(zp1))
      call clraddr(Point(rp2))
      call clraddr(Point(zp2))
      call clraddr(Point(wt))

      return
       end
      subroutine apidbcr(drtdm)
      integer drtdm
      call rtdbcr(drtdm,20,152)
      return
       end
      subroutine apiwake
      integer drtdm,i0001234, jgrp , jvar
      integer rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      external rtgrpe, rtvare, rtfcne1, rtfcne2, rtfcne3, rtfcneb, setlimit
      common /apirtdm/ drtdm
Use_All_Groups_api

      Address i000addr
      external varadr
      Address varadr


      call apidbcr(drtdm)
      jgrp=rtgrpe(drtdm,"Physical_constants2")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ev2",varadr(ev2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"qe2",varadr(qe2),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Normalization_constants")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"crni",varadr(crni),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ctemp",varadr(ctemp),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Impfcn")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "getatau",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nx:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ny:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(uu:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(gx:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ixpt1:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ixpt2:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(iysptrx:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(atau:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(tau1:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(tau2:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "getprad",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nx:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ny:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ngsp:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ng:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(afrac:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(atau:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(prad:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(na:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ntau:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nratio:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Impurity_transport")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"dnimp",varadr(dnimp),0,Quote(double precision),
Quote(scalar), "m**2/s")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"methimp",varadr(methimp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"csexpn",varadr(csexpn),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Impurity_source")
      if(jgrp = 0) go to 999
      i000addr = varadr ( Point(simpfix) )
      i0001234=rtvare(drtdm,"simpfix",i000addr,1,Quote(_double precision),
Quote((nx,ny)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Sources_at_walls")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nzsor",varadr(nzsor),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(iszsorlb) )
      i0001234=rtvare(drtdm,"iszsorlb",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,1)
      i000addr = varadr ( Point(jxzsori) )
      i0001234=rtvare(drtdm,"jxzsori",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,1)
      i000addr = varadr ( Point(jxzsoro) )
      i0001234=rtvare(drtdm,"jxzsoro",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,1)
      i000addr = varadr ( Point(ixzbegi) )
      i0001234=rtvare(drtdm,"ixzbegi",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixzendi) )
      i0001234=rtvare(drtdm,"ixzendi",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixzbego) )
      i0001234=rtvare(drtdm,"ixzbego",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ixzendo) )
      i0001234=rtvare(drtdm,"ixzendo",i000addr,1,Quote(_integer),
Quote((nzspt,nzsor)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ximpi) )
      i0001234=rtvare(drtdm,"ximpi",i000addr,1,Quote(_double precision),
Quote((nzspt,nzsor)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ximpo) )
      i0001234=rtvare(drtdm,"ximpo",i000addr,1,Quote(_double precision),
Quote((nzspt,nzsor)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wimpi) )
      i0001234=rtvare(drtdm,"wimpi",i000addr,1,Quote(_double precision),
Quote((nzspt,nzsor)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(wimpo) )
      i0001234=rtvare(drtdm,"wimpo",i000addr,1,Quote(_double precision),
Quote((nzspt,nzsor)), "m")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(impsori) )
      i0001234=rtvare(drtdm,"impsori",i000addr,1,Quote(_double precision),
Quote((nzspt,nzsor)), "Amp")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(impsoro) )
      i0001234=rtvare(drtdm,"impsoro",i000addr,1,Quote(_double precision),
Quote((nzspt,nzsor)), "Amp")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Input")
      if(jgrp = 0) go to 999
      i000addr = varadr ( inelrates )
      i0001234=rtvare(drtdm,"inelrates",i000addr,0,Quote(Filename),
Quote((1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( inelrad )
      i0001234=rtvare(drtdm,"inelrad",i000addr,0,Quote(Filename),
Quote((1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( inelmc )
      i0001234=rtvare(drtdm,"inelmc",i000addr,0,Quote(Filename),
Quote((1)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Radiation")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ncaset",varadr(ncaset),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncaseno",varadr(ncaseno),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ncasent",varadr(ncasent),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( terad )
      i0001234=rtvare(drtdm,"terad",i000addr,0,Quote(double precision),
Quote((NCASET)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( xno )
      i0001234=rtvare(drtdm,"xno",i000addr,0,Quote(double precision),
Quote((NCASENO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( rntau )
      i0001234=rtvare(drtdm,"rntau",i000addr,0,Quote(double precision),
Quote((NCASENT)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( radrate )
      i0001234=rtvare(drtdm,"radrate",i000addr,0,Quote(double precision),
Quote((NCASET,NCASENO,NCASENT)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( avgz )
      i0001234=rtvare(drtdm,"avgz",i000addr,0,Quote(double precision),
Quote((NCASET,NCASENO,NCASENT)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( avgz2 )
      i0001234=rtvare(drtdm,"avgz2",i000addr,0,Quote(double precision),
Quote((NCASET,NCASENO,NCASENT)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Impdata")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"apidir",varadr(apidir),0,Quote(character*120),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"MC_subs")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "readmc",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nzdf:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(mcfilename:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_mcfilename_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "mcrates",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ti:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(za:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(zamax:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(zn:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rion:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rrec:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rcxr:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "radmc",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nz:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(znuc:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(dene:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(denz:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(radz:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "rcxr_zn6",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(tmp:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(za:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Impurity_charge")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nnz",varadr(nnz),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zq) )
      i0001234=rtvare(drtdm,"zq",i000addr,1,Quote(_double precision),
Quote((nnz)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"P93dat")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"atn",varadr(atn),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"atw",varadr(atw),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nt",varadr(nt),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nr",varadr(nr),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nn",varadr(nn),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(tdatm) )
      i0001234=rtvare(drtdm,"tdatm",i000addr,1,Quote(_double precision),
Quote((nt,nr,nn)), "J")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rdatm) )
      i0001234=rtvare(drtdm,"rdatm",i000addr,1,Quote(_double precision),
Quote((nt,nr,nn)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ndatm) )
      i0001234=rtvare(drtdm,"ndatm",i000addr,1,Quote(_double precision),
Quote((nt,nr,nn)), "sec/m**3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(emdatm) )
      i0001234=rtvare(drtdm,"emdatm",i000addr,1,Quote(_double precision),
Quote((nt,nr,nn)), "Watts-m**3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(z1datm) )
      i0001234=rtvare(drtdm,"z1datm",i000addr,1,Quote(_double precision),
Quote((nt,nr,nn)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(z2datm) )
      i0001234=rtvare(drtdm,"z2datm",i000addr,1,Quote(_double precision),
Quote((nt,nr,nn)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Imslwrk")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nxdata",varadr(nxdata),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nydata",varadr(nydata),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzdata",varadr(nzdata),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xdata) )
      i0001234=rtvare(drtdm,"xdata",i000addr,1,Quote(_double precision),
Quote((1:nxdata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(ydata) )
      i0001234=rtvare(drtdm,"ydata",i000addr,1,Quote(_double precision),
Quote((1:nydata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zdata) )
      i0001234=rtvare(drtdm,"zdata",i000addr,1,Quote(_double precision),
Quote((1:nzdata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(fdata) )
      i0001234=rtvare(drtdm,"fdata",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata,1:nzdata)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ldf",varadr(ldf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mdf",varadr(mdf),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iflagi",varadr(iflagi),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nwork2",varadr(nwork2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(work2) )
      i0001234=rtvare(drtdm,"work2",i000addr,1,Quote(_double precision),
Quote((nwork2)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nwork3",varadr(nwork3),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(work3) )
      i0001234=rtvare(drtdm,"work3",i000addr,1,Quote(_double precision),
Quote((nwork3)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( iworki )
      i0001234=rtvare(drtdm,"iworki",i000addr,0,Quote(integer),
Quote((10)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"icont",varadr(icont),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kxords",varadr(kxords),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kyords",varadr(kyords),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"kzords",varadr(kzords),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(xknots) )
      i0001234=rtvare(drtdm,"xknots",i000addr,1,Quote(_double precision),
Quote((1:nxdata+kxords)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(yknots) )
      i0001234=rtvare(drtdm,"yknots",i000addr,1,Quote(_double precision),
Quote((1:nydata+kyords)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(zknots) )
      i0001234=rtvare(drtdm,"zknots",i000addr,1,Quote(_double precision),
Quote((1:nzdata+kzords)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(emcoef) )
      i0001234=rtvare(drtdm,"emcoef",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata,1:nzdata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(z1coef) )
      i0001234=rtvare(drtdm,"z1coef",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata,1:nzdata)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(z2coef) )
      i0001234=rtvare(drtdm,"z2coef",i000addr,1,Quote(_double precision),
Quote((1:nxdata,1:nydata,1:nzdata)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"P93fcn")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "readpost",jgrp,Quote(null),"none")
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
      jvar = rtfcne1(drtdm, "splinem",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "()")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "emissbs",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nratio:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ntau:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "z1avgbs",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nratio:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ntau:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "z2avgbs",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(nratio:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ntau:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Reduced_ion_constants")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"coulom",varadr(coulom),0,Quote(double precision),
Quote(scalar), "coulomb")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"epsilo",varadr(epsilo),0,Quote(double precision),
Quote(scalar), "farad/m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"promas",varadr(promas),0,Quote(double precision),
Quote(scalar), "kg")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"xj7kv",varadr(xj7kv),0,Quote(double precision),
Quote(scalar), "J/keV")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"one",varadr(one),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"pi0",varadr(pi0),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zero",varadr(zero),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"sumforce",varadr(sumforce),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"totmass",varadr(totmass),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"anorm",varadr(anorm),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"acci",varadr(acci),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"acci0",varadr(acci0),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( al32 )
      i0001234=rtvare(drtdm,"al32",i000addr,0,Quote(double precision),
Quote((3)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"miso",varadr(miso),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzch",varadr(nzch),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"mise",varadr(mise),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ilam1",varadr(ilam1),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ilam2",varadr(ilam2),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ilam3",varadr(ilam3),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iacci",varadr(iacci),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"iforc",varadr(iforc),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( natom )
      i0001234=rtvare(drtdm,"natom",i000addr,0,Quote(integer),
Quote((MXMISO)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Reduced_ion_variables")
      if(jgrp = 0) go to 999
      i000addr = varadr ( capm )
      i0001234=rtvare(drtdm,"capm",i000addr,0,Quote(double precision),
Quote((KXA*MXMISO*KXA*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( capn )
      i0001234=rtvare(drtdm,"capn",i000addr,0,Quote(double precision),
Quote((KXA*MXMISO*KXA*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( caplam )
      i0001234=rtvare(drtdm,"caplam",i000addr,0,Quote(double precision),
Quote((KXA*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( fmomenta )
      i0001234=rtvare(drtdm,"fmomenta",i000addr,0,Quote(double precision),
Quote((KMXZ)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( denz )
      i0001234=rtvare(drtdm,"denz",i000addr,0,Quote(double precision),
Quote((MXMISO*MXNZCH)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( denmass )
      i0001234=rtvare(drtdm,"denmass",i000addr,0,Quote(double precision),
Quote((MXMISO*(MXNZCH+1))), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( ela )
      i0001234=rtvare(drtdm,"ela",i000addr,0,Quote(double precision),
Quote((KXA*KXA*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( elab )
      i0001234=rtvare(drtdm,"elab",i000addr,0,Quote(double precision),
Quote((KXA*MXMISO*KXA*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( mntau )
      i0001234=rtvare(drtdm,"mntau",i000addr,0,Quote(double precision),
Quote((MXMISO*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( usol )
      i0001234=rtvare(drtdm,"usol",i000addr,0,Quote(double precision),
Quote((KXA*MXNZCH*MXMISO)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( sbar )
      i0001234=rtvare(drtdm,"sbar",i000addr,0,Quote(double precision),
Quote((KXA*MXMISO1)), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( zi )
      i0001234=rtvare(drtdm,"zi",i000addr,0,Quote(double precision),
Quote((MXMISO*MXNZCH)), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Cyield")
      if(jgrp = 0) go to 999
      i000addr = varadr ( ceth )
      i0001234=rtvare(drtdm,"ceth",i000addr,0,Quote(double precision),
Quote((7,12)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( cetf )
      i0001234=rtvare(drtdm,"cetf",i000addr,0,Quote(double precision),
Quote((7,12)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( cq )
      i0001234=rtvare(drtdm,"cq",i000addr,0,Quote(double precision),
Quote((7,12)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"ntars",varadr(ntars),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( cidata )
      i0001234=rtvare(drtdm,"cidata",i000addr,0,Quote(logical),
Quote((7,12)), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"redf_haas",varadr(redf_haas),0,Quote(double precision),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      jgrp=rtgrpe(drtdm,"Sputt_subs")
      if(jgrp = 0) go to 999
      jvar = rtfcne1(drtdm, "syld96",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(matt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(matp:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(cion:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(cizb:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(crmb:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "yld96",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(matt:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(matp:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(energy:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "sputchem",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ioptchem:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ee0:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(temp:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(flux:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ychem:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Emissivities")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"ntemp",varadr(ntemp),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nlam",varadr(nlam),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nden",varadr(nden),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(etemp) )
      i0001234=rtvare(drtdm,"etemp",i000addr,1,Quote(_double precision),
Quote((ntemp)), "eV")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(lamb) )
      i0001234=rtvare(drtdm,"lamb",i000addr,1,Quote(_double precision),
Quote((nlam)), "Angstrom")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(eden) )
      i0001234=rtvare(drtdm,"eden",i000addr,1,Quote(_double precision),
Quote((nden)), "m^-3")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(rate) )
      i0001234=rtvare(drtdm,"rate",i000addr,1,Quote(_double precision),
Quote((nlam,ntemp,nden)), "ph/s")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(emiss) )
      i0001234=rtvare(drtdm,"emiss",i000addr,1,Quote(_double precision),
Quote((nlam,0:nx+1,0:ny+1)), "ph/m^3/s")
      if(i0001234 = 0) go to 999
      jvar = rtfcne1(drtdm, "readrates",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(apidir:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_apidir_:integer,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(impfname:String,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(l_impfname_:integer))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jvar = rtfcne1(drtdm, "calcrates",jgrp,Quote(null),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(ne:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(te:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(density:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      jgrp=rtgrpe(drtdm,"Pixels")
      if(jgrp = 0) go to 999
      i0001234=rtvare(drtdm,"nrpix",varadr(nrpix),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"nzpix",varadr(nzpix),0,Quote(integer),
Quote(scalar), "none")
      if(i0001234 = 0) go to 999
      i000addr = varadr ( Point(npd) )
      i0001234=rtvare(drtdm,"npd",i000addr,1,Quote(_integer),
Quote((nrpix,nzpix)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0)
      i000addr = varadr ( Point(rp1) )
      i0001234=rtvare(drtdm,"rp1",i000addr,1,Quote(_double precision),
Quote((nrpix,nzpix)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(zp1) )
      i0001234=rtvare(drtdm,"zp1",i000addr,1,Quote(_double precision),
Quote((nrpix,nzpix)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(rp2) )
      i0001234=rtvare(drtdm,"rp2",i000addr,1,Quote(_double precision),
Quote((nrpix,nzpix)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(zp2) )
      i0001234=rtvare(drtdm,"zp2",i000addr,1,Quote(_double precision),
Quote((nrpix,nzpix)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i000addr = varadr ( Point(wt) )
      i0001234=rtvare(drtdm,"wt",i000addr,1,Quote(_double precision),
Quote((nrpix,nzpix)), "none")
      if(i0001234 = 0) go to 999
      call rtdynset(i0001234,drtdm,0.)
      i0001234=rtvare(drtdm,"rminpix",varadr(rminpix),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"rmaxpix",varadr(rmaxpix),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zminpix",varadr(zminpix),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"zmaxpix",varadr(zmaxpix),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"drpix",varadr(drpix),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      i0001234=rtvare(drtdm,"dzpix",varadr(dzpix),0,Quote(double precision),
Quote(scalar), "m")
      if(i0001234 = 0) go to 999
      jvar = rtfcne1(drtdm, "lineintegral",jgrp,Quote(double precision),"none")
      if(jvar == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , "(")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(arg:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(rvertex:double precision,))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , Quote(zvertex:double precision))
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne2(jvar, drtdm , ")")
      if(i0001234 == 0) go to 999
      i0001234 = rtfcne3(jvar, drtdm)
      if(i0001234 == 0) go to 999
      call rtsetdoc(drtdm,"api_basis.cmt")
        return
999   continue
      call baderr("Error initializing variable in database")
        end
      subroutine apixpf(iseg,name1234)
      character*(*) name1234
      integer iseg
      character*8 name5678
      name5678=name1234
      if(iseg.eq.3) then
         call apixp3(name1234)
      elseif(iseg.eq.10) then
         call apixp10(name1234)
      elseif(iseg.eq.14) then
         call apixp14(name1234)
      elseif(iseg.eq.18) then
         call apixp18(name1234)
      elseif(iseg.eq.19) then
         call apixp19(name1234)
      elseif(iseg.eq.20) then
         call apixp20(name1234)
      else
         call baderr('apixpf: impossible event')
      endif
      return
      end
      subroutine apixp3(name1234)
      character*(*) name1234
      external api_handler
      external [getatau]
      external [getprad]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'getatau') then
         call parexecf(api_handler, 0, [getatau])
      elseif(name1234 = 'getprad') then
         call parexecf(api_handler, 1, [getprad])
      else
         call baderr('apixp3: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp10(name1234)
      character*(*) name1234
      external api_handler
      external [readmc]
      external [mcrates]
      external [radmc]
      external [rcxr_zn6]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'readmc') then
         call parexecf(api_handler, 2, [readmc])
      elseif(name1234 = 'mcrates') then
         call parexecf(api_handler, 3, [mcrates])
      elseif(name1234 = 'radmc') then
         call parexecf(api_handler, 4, [radmc])
      elseif(name1234 = 'rcxr_zn6') then
         call parexecf(api_handler, 5, [rcxr_zn6])
      else
         call baderr('apixp10: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp14(name1234)
      character*(*) name1234
      external api_handler
      external [readpost]
      external [splinem]
      external [emissbs]
      external [z1avgbs]
      external [z2avgbs]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'readpost') then
         call parexecf(api_handler, 6, [readpost])
      elseif(name1234 = 'splinem') then
         call parexecf(api_handler, 7, [splinem])
      elseif(name1234 = 'emissbs') then
         call parexecf(api_handler, 8, [emissbs])
      elseif(name1234 = 'z1avgbs') then
         call parexecf(api_handler, 9, [z1avgbs])
      elseif(name1234 = 'z2avgbs') then
         call parexecf(api_handler, 10, [z2avgbs])
      else
         call baderr('apixp14: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp18(name1234)
      character*(*) name1234
      external api_handler
      external [syld96]
      external [yld96]
      external [sputchem]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'syld96') then
         call parexecf(api_handler, 11, [syld96])
      elseif(name1234 = 'yld96') then
         call parexecf(api_handler, 12, [yld96])
      elseif(name1234 = 'sputchem') then
         call parexecf(api_handler, 13, [sputchem])
      else
         call baderr('apixp18: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp19(name1234)
      character*(*) name1234
      external api_handler
      external [readrates]
      external [calcrates]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'readrates') then
         call parexecf(api_handler, 14, [readrates])
      elseif(name1234 = 'calcrates') then
         call parexecf(api_handler, 15, [calcrates])
      else
         call baderr('apixp19: impossible event: '//name5678)
      endif
      return
      end
      subroutine apixp20(name1234)
      character*(*) name1234
      external api_handler
      external [lineintegral]
      character*8 name5678
      name5678=name1234
      if(name1234 = 'lineintegral') then
         call parexecf(api_handler, 16, [lineintegral])
      else
         call baderr('apixp20: impossible event: '//name5678)
      endif
      return
      end
      function apibfcn(ss,sp,nargs,name1234,sx)
      integer apibfcn,ss(SS_WIDTH,1),sp,nargs
      integer sx(SS_WIDTH)
      character*(*) name1234
      character*8 name5678
      name5678=name1234
      call remark('No such builtin function ('//name5678//') in api')
      call baderr(name1234)
      return(ERR)
      end
