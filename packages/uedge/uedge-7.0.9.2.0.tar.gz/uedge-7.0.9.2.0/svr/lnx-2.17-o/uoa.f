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
c     ./../uoa.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c












































c newuoa.m,v 1.6 2006/08/12 18:27:06 bulmer Exp

      subroutine xnewuoa(n,npt,x,rhobeg,rhoend,maxfun,iprint)
cProlog

      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group UOA
      double precision rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      integer n_uoa, npt_uoa, m_uoa

      double precision x_uoa ( n_uoa)
      pointer(px_uoa,x_uoa)

      double precision w_uoa ( m_uoa)
      pointer(pw_uoa,w_uoa)
      common /svr10/ n_uoa, npt_uoa, m_uoa
      common /svr13/ rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      common /svr16/ px_uoa, pw_uoa
c End of UOA

      dimension x(*)

c This subroutine seeks the least value of a function of many variables,
c by a trust region method that forms quadratic models by interpolation.
c There can be some freedom in the interpolation conditions, which is
c taken up by minimizing the Frobenius norm of the change to the second
c derivative of the quadratic model, beginning with a zero matrix. The
c arguments of the subroutine are as follows.
c
c N must be set to the number of variables and must be at least two.
c NPT is the number of interpolation conditions. Its value must be in the
c   interval [N+2,(N+1)(N+2)/2].
c Initial values of the variables must be set in X(1),X(2),...,X(N). They
c   will be changed to the values that give the least calculated F.
c RHOBEG and RHOEND must be set to the initial and final values of a trust
c   region radius, so both must be positive with RHOEND<=RHOBEG. Typically
c   RHOBEG should be about one tenth of the greatest expected change to a
c   variable, and RHOEND should indicate the accuracy that is required in
c   the final values of the variables.
c MAXFUN must be set to an upper bound on the number of calls of CALFUN.
c The value of IPRINT should be set to 0, 1, 2 or 3, which controls the
c   amount of printing. Specifically, there is no output if IPRINT=0 and
c   there is output only at the return if IPRINT=1. Otherwise, each new
c   value of RHO is printed, with the best vector of variables so far and
c   the corresponding value of the objective function. Further, each new
c   value of F with its variables are output if IPRINT=3.
c
c SUBROUTINE CALFUN (N,X,F) must be provided by the user. It must set F to
c the value of the objective function for the variables X(1),X(2),...,X(N).
c
c Partition the working space array, so that different parts of it can be
c treated separately by the subroutine that performs the main calculation.

      np=n+1
      nptm=npt-np

c Allocate workspace
      n_uoa=n
      npt_uoa=npt
      m_uoa=(npt+13)*(npt+n)+3*n*(n+3)/2
      call gchange("UOA",0)

c Provide a partition of W for subroutine NEWUOB.
c The partition requires the first NPT*(NPT+N)+5*N*(N+3)/2 elements of
c W plus the space that is needed by the last array of NEWUOB.
      ndim=npt+n
      ixb=1
      ixo=ixb+n
      ixn=ixo+n
      ixp=ixn+n
      ifv=ixp+n*npt
      igq=ifv+npt
      ihq=igq+n
      ipq=ihq+(n*np)/2
      ibmat=ipq+npt
      izmat=ibmat+ndim*n
      id=izmat+npt*nptm
      ivl=id+n
      iw=ivl+ndim

      call newuob(n, npt, x, rhobeg, rhoend, iprint, maxfun, w_uoa(ixb), 
     &   w_uoa(ixo), w_uoa(ixn), w_uoa(ixp), w_uoa(ifv), w_uoa(igq), 
     &   w_uoa(ihq), w_uoa(ipq), w_uoa(ibmat), w_uoa(izmat), ndim, w_uoa
     &   (id), w_uoa(ivl), w_uoa(iw))

      return

c newuoa
      end

c----------------------------------------------------------------------
c newuob.m,v 1.4 2006/08/12 18:27:06 bulmer Exp

      subroutine newuob(n,npt,x,rhobeg,rhoend,iprint,maxfun,xbase, xopt,
     &   xnew,xpt,fval,gq,hq,pq,bmat,zmat,ndim,d,vlag,w)
cProlog

      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group UOA
      double precision rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      integer n_uoa, npt_uoa, m_uoa

      double precision x_uoa ( n_uoa)
      pointer(px_uoa,x_uoa)

      double precision w_uoa ( m_uoa)
      pointer(pw_uoa,w_uoa)
      common /svr10/ n_uoa, npt_uoa, m_uoa
      common /svr13/ rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      common /svr16/ px_uoa, pw_uoa
c End of UOA

      dimension x(*),xbase(*),xopt(*),xnew(*),xpt(npt,*),fval(*)
      dimension gq(*),hq(*),pq(*),bmat(ndim,*),zmat(npt,*),d(*),vlag(*),
     &   w(*)

c The arguments N, NPT, X, RHOBEG, RHOEND, IPRINT and MAXFUN are identical
c   to the corresponding arguments in SUBROUTINE NEWUOA.
c XBASE will hold a shift of origin that should reduce the contributions
c   from rounding errors to values of the model and Lagrange functions.
c XOPT will be set to the displacement from XBASE of the vector of
c   variables that provides the least calculated F so far.
c XNEW will be set to the displacement from XBASE of the vector of
c   variables for the current calculation of F.
c XPT will contain the interpolation point coordinates relative to XBASE.
c FVAL will hold the values of F at the interpolation points.
c GQ will hold the gradient of the quadratic model at XBASE.
c HQ will hold the explicit second derivatives of the quadratic model.
c PQ will contain the parameters of the implicit second derivatives of
c   the quadratic model.
c BMAT will hold the last N columns of H.
c ZMAT will hold the factorization of the leading NPT by NPT submatrix of
c   H, this factorization being ZMAT times Diag(DZ) times ZMAT^T, where
c   the elements of DZ are plus or minus one, as specified by IDZ.
c NDIM is the first dimension of BMAT and has the value NPT+N.
c D is reserved for trial steps from XOPT.
c VLAG will contain the values of the Lagrange functions at a new point X.
c   They are part of a product that requires VLAG to be of length NDIM.
c The array W will be used for working space. Its length must be at least
c   10*NDIM = 10*(NPT+N).

      half=0.5d0
      one=1.0d0
      tenth=0.1d0
      zero=0.0d0
      np=n+1
      nh=(n*np)/2
      nptm=npt-np
      nftest=max0(maxfun,1)

c Set the initial elements of XPT, BMAT, HQ, PQ and ZMAT to zero.

      do 23000 j=1,n
         xbase(j)=x(j)
         do 23002 k=1,npt
            xpt(k,j)=zero
23002    continue
         do 23004 i=1,ndim
            bmat(i,j)=zero
23004    continue
23000 continue
      do 23006 ih=1,nh
         hq(ih)=zero
23006 continue
      do 23008 k=1,npt
         pq(k)=zero
         do 23010 j=1,nptm
            zmat(k,j)=zero
23010    continue
23008 continue

c Begin the initialization procedure. NF becomes one more than the number
c of function values so far. The coordinates of the displacement of the
c next initial interpolation point from XBASE are set in XPT(NF,.).

      rhosq=rhobeg*rhobeg
      recip=one/rhosq
      reciq=sqrt(half)/rhosq
      nf=0
   50 nfm=nf
      nfmm=nf-n
      nf=nf+1
      if (nfm .le. 2*n) then
         if (nfm .ge. 1 .and. nfm .le. n) then
            xpt(nf,nfm)=rhobeg
         elseif (nfm .gt. n) then
            xpt(nf,nfmm)=-rhobeg
         endif
      else
         itemp=(nfmm-1)/n
         jpt=nfm-itemp*n-n
         ipt=jpt+itemp
         if (ipt .gt. n) then
            itemp=jpt
            jpt=ipt-n
            ipt=itemp
         endif
         xipt=rhobeg
         if (fval(ipt+np) .lt. fval(ipt+1)) xipt=-xipt
         xjpt=rhobeg
         if (fval(jpt+np) .lt. fval(jpt+1)) xjpt=-xjpt
         xpt(nf,ipt)=xipt
         xpt(nf,jpt)=xjpt
      endif

c Calculate the next value of F, label 70 being reached immediately
c after this calculation. The least function value so far and its index
c are required.

      do 23012 j=1,n
         x(j)=xpt(nf,j)+xbase(j)
23012 continue
      goto 310
   70 fval(nf)=f
      if (nf .eq. 1) then
         fbeg=f
         fopt=f
         kopt=1
      elseif (f .lt. fopt) then
         fopt=f
         kopt=nf
      endif

c Set the nonzero initial elements of BMAT and the quadratic model in
c the cases when NF is at most 2*N+1.

      if (nfm .le. 2*n) then
         if (nfm .ge. 1 .and. nfm .le. n) then
            gq(nfm)=(f-fbeg)/rhobeg
            if (npt .lt. nf+n) then
               bmat(1,nfm)=-one/rhobeg
               bmat(nf,nfm)=one/rhobeg
               bmat(npt+nfm,nfm)=-half*rhosq
            endif
         elseif (nfm .gt. n) then
            bmat(nf-n,nfmm)=half/rhobeg
            bmat(nf,nfmm)=-half/rhobeg
            zmat(1,nfmm)=-reciq-reciq
            zmat(nf-n,nfmm)=reciq
            zmat(nf,nfmm)=reciq
            ih=(nfmm*(nfmm+1))/2
            temp=(fbeg-f)/rhobeg
            hq(ih)=(gq(nfmm)-temp)/rhobeg
            gq(nfmm)=half*(gq(nfmm)+temp)
         endif

      else
c Set the off-diagonal second derivatives of the Lagrange functions and
c the initial quadratic model.
         ih=(ipt*(ipt-1))/2+jpt
         if (xipt .lt. zero) ipt=ipt+n
         if (xjpt .lt. zero) jpt=jpt+n
         zmat(1,nfmm)=recip
         zmat(nf,nfmm)=recip
         zmat(ipt+1,nfmm)=-recip
         zmat(jpt+1,nfmm)=-recip
         hq(ih)=(fbeg-fval(ipt+1)-fval(jpt+1)+f)/(xipt*xjpt)
      endif
      if (nf .lt. npt) goto 50

c Begin the iterative procedure, because the initial model is complete.

      rho=rhobeg
      rho_uoa=rho
      delta=rho
      idz=1
      diffa=zero
      diffb=zero
      itest=0
      xoptsq=zero
      do 23014 i=1,n
         xopt(i)=xpt(kopt,i)
         xoptsq=xoptsq+xopt(i)**2
23014 continue
   90 nfsav=nf

c Generate the next trust region step and test its length. Set KNEW
c to -1 if the purpose of the next F will be to improve the model.

  100 knew=0
      call trsapp(n,npt,xopt,xpt,gq,hq,pq,delta,d,w,w(np), w(np+n),w(np+
     &   2*n),crvmin)
      dsq=zero
      do 23016 i=1,n
         dsq=dsq+d(i)**2
23016 continue
      dnorm=min(delta,sqrt(dsq))
      if (dnorm .lt. half*rho) then
         knew=-1
         delta=tenth*delta
         ratio=-1.0d0
         if (delta .le. 1.5d0*rho) delta=rho
         if (nf .le. nfsav+2) goto 460
         temp=0.125d0*crvmin*rho*rho
         if (temp .le. max(diffa,diffb,diffc)) goto 460
         goto 490
      endif

c Shift XBASE if XOPT may be too far from XBASE. First make the changes
c to BMAT that do not depend on ZMAT.

  120 if (dsq .le. 1.0d-3*xoptsq) then
         tempq=0.25d0*xoptsq
         do 23018 k=1,npt
            sum=zero
            do 23020 i=1,n
               sum=sum+xpt(k,i)*xopt(i)
23020       continue
            temp=pq(k)*sum
            sum=sum-half*xoptsq
            w(npt+k)=sum
            do 23022 i=1,n
               gq(i)=gq(i)+temp*xpt(k,i)
               xpt(k,i)=xpt(k,i)-half*xopt(i)
               vlag(i)=bmat(k,i)
               w(i)=sum*xpt(k,i)+tempq*xopt(i)
               ip=npt+i
               do 23024 j=1,i
                  bmat(ip,j)=bmat(ip,j)+vlag(i)*w(j)+w(i)*vlag(j)
23024          continue
23022       continue
23018    continue

c Then the revisions of BMAT that depend on ZMAT are calculated.

         do 23026 k=1,nptm
            sumz=zero
            do 23028 i=1,npt
               sumz=sumz+zmat(i,k)
               w(i)=w(npt+i)*zmat(i,k)
23028       continue
            do 23030 j=1,n
               sum=tempq*sumz*xopt(j)
               do 23032 i=1,npt
                  sum=sum+w(i)*xpt(i,j)
23032          continue
               vlag(j)=sum
               if (k .lt. idz) sum=-sum
               do 23034 i=1,npt
                  bmat(i,j)=bmat(i,j)+sum*zmat(i,k)
23034          continue
23030       continue
            do 23036 i=1,n
               ip=i+npt
               temp=vlag(i)
               if (k .lt. idz) temp=-temp
               do 23038 j=1,i
                  bmat(ip,j)=bmat(ip,j)+temp*vlag(j)
23038          continue
23036       continue
23026    continue

c The following instructions complete the shift of XBASE, including
c the changes to the parameters of the quadratic model.

         ih=0
         do 23040 j=1,n
            w(j)=zero
            do 23042 k=1,npt
               w(j)=w(j)+pq(k)*xpt(k,j)
               xpt(k,j)=xpt(k,j)-half*xopt(j)
23042       continue
            do 23044 i=1,j
               ih=ih+1
               if (i .lt. j) gq(j)=gq(j)+hq(ih)*xopt(i)
               gq(i)=gq(i)+hq(ih)*xopt(j)
               hq(ih)=hq(ih)+w(i)*xopt(j)+xopt(i)*w(j)
               bmat(npt+i,j)=bmat(npt+j,i)
23044       continue
23040    continue
         do 23046 j=1,n
            xbase(j)=xbase(j)+xopt(j)
            xopt(j)=zero
23046    continue
         xoptsq=zero
      endif

c Pick the model step if KNEW is positive. A different choice of D
c may be made later, if the choice of D by BIGLAG causes substantial
c cancellation in DENOM.

      if (knew .gt. 0) then
         call biglag(n,npt,xopt,xpt,bmat,zmat,idz,ndim,knew,dstep, d,
     &      alpha,vlag,vlag(npt+1),w,w(np),w(np+n))
      endif

c Calculate VLAG and BETA for the current choice of D. The first NPT
c components of W_check will be held in W.

      do 23048 k=1,npt
         suma=zero
         sumb=zero
         sum=zero
         do 23050 j=1,n
            suma=suma+xpt(k,j)*d(j)
            sumb=sumb+xpt(k,j)*xopt(j)
            sum=sum+bmat(k,j)*d(j)
23050    continue
         w(k)=suma*(half*suma+sumb)
         vlag(k)=sum
23048 continue
      beta=zero
      do 23052 k=1,nptm
         sum=zero
         do 23054 i=1,npt
            sum=sum+zmat(i,k)*w(i)
23054    continue
         if (k .lt. idz) then
            beta=beta+sum*sum
            sum=-sum
         else
            beta=beta-sum*sum
         endif
         do 23056 i=1,npt
            vlag(i)=vlag(i)+sum*zmat(i,k)
23056    continue
23052 continue
      bsum=zero
      dx=zero
      do 23058 j=1,n
         sum=zero
         do 23060 i=1,npt
            sum=sum+w(i)*bmat(i,j)
23060    continue
         bsum=bsum+sum*d(j)
         jp=npt+j
         do 23062 k=1,n
            sum=sum+bmat(jp,k)*d(k)
23062    continue
         vlag(jp)=sum
         bsum=bsum+sum*d(j)
         dx=dx+d(j)*xopt(j)
23058 continue
      beta=dx*dx+dsq*(xoptsq+dx+dx+half*dsq)+beta-bsum
      vlag(kopt)=vlag(kopt)+one

c If KNEW is positive and if the cancellation in DENOM is unacceptable,
c then BIGDEN calculates an alternative model step, XNEW being used for
c working space.

      if (knew .gt. 0) then
         temp=one+alpha*beta/vlag(knew)**2
         if (abs(temp) .le. 0.8d0) then
            call bigden(n,npt,xopt,xpt,bmat,zmat,idz,ndim,kopt, knew,d,w
     &         ,vlag,beta,xnew,w(ndim+1),w(6*ndim+1))
         endif
      endif

c Calculate the next value of the objective function.

  290 do 23064 i=1,n
         xnew(i)=xopt(i)+d(i)
         x(i)=xbase(i)+xnew(i)
23064 continue
      nf=nf+1
  310 if (nf .gt. nftest) then
         nf=nf-1
         if (iprint .gt. 0) then
            call remark("newuoa: CALFUN has been called MAXFUN times.")
         endif
         goto 530
      endif
      call calfun(n,x,f)
      if (iprint .eq. 3) then
         print 330, nf,f,(x(i),i=1,n)
  330    format (/4x,'Function number',i6,'    F =',1pd18.10, 
     &      '    The corresponding X is:'/(2x,5d15.6))
      endif
      if (nf .le. npt) goto 70
      if (knew .eq. -1) goto 530

c Use the quadratic model to predict the change in F due to the step D,
c and set DIFF to the error of this prediction.

      vquad=zero
      ih=0
      do 23066 j=1,n
         vquad=vquad+d(j)*gq(j)
         do 23068 i=1,j
            ih=ih+1
            temp=d(i)*xnew(j)+d(j)*xopt(i)
            if (i .eq. j) temp=half*temp
            vquad=vquad+temp*hq(ih)
23068    continue
23066 continue
      do 23070 k=1,npt
         vquad=vquad+pq(k)*w(k)
23070 continue
      diff=f-fopt-vquad
      diffc=diffb
      diffb=diffa
      diffa=abs(diff)
      if (dnorm .gt. rho) nfsav=nf

c Update FOPT and XOPT if the new F is the least value of the objective
c function so far. The branch when KNEW is positive occurs if D is not
c a trust region step.

      fsave=fopt
      if (f .lt. fopt) then
         fopt=f
         xoptsq=zero
         do 23072 i=1,n
            xopt(i)=xnew(i)
            xoptsq=xoptsq+xopt(i)**2
23072    continue
      endif
      ksave=knew
      if (knew .gt. 0) goto 410

c Pick the next value of DELTA after a trust region step.

      if (vquad .ge. zero) then
         if (iprint .gt. 0) then
            call remark(
     &         "newuoa: a trust region step has failed to reduce Q.")
         endif
         goto 530
      endif
      ratio=(f-fsave)/vquad
      if (ratio .le. tenth) then
         delta=half*dnorm
      elseif (ratio .le. 0.7d0) then
         delta=max(half*delta,dnorm)
      else
         delta=max(half*delta,dnorm+dnorm)
      endif
      if (delta .le. 1.5d0*rho) delta=rho

c Set KNEW to the index of the next interpolation point to be deleted.

      rhosq=max(tenth*delta,rho)**2
      ktemp=0
      detrat=zero
      if (f .ge. fsave) then
         ktemp=kopt
         detrat=one
      endif
      do 23074 k=1,npt
         hdiag=zero
         do 23076 j=1,nptm
            temp=one
            if (j .lt. idz) temp=-one
            hdiag=hdiag+temp*zmat(k,j)**2
23076    continue
         temp=abs(beta*hdiag+vlag(k)**2)
         distsq=zero
         do 23078 j=1,n
            distsq=distsq+(xpt(k,j)-xopt(j))**2
23078    continue
         if (distsq .gt. rhosq) temp=temp*(distsq/rhosq)**3
         if (temp .gt. detrat .and. k .ne. ktemp) then
            detrat=temp
            knew=k
         endif
23074 continue
      if (knew .eq. 0) goto 460

c Update BMAT, ZMAT and IDZ, so that the KNEW-th interpolation point
c can be moved. Begin the updating of the quadratic model, starting
c with the explicit second derivative term.

  410 call update(n,npt,bmat,zmat,idz,ndim,vlag,beta,knew,w)
      fval(knew)=f
      ih=0
      do 23080 i=1,n
         temp=pq(knew)*xpt(knew,i)
         do 23082 j=1,i
            ih=ih+1
            hq(ih)=hq(ih)+temp*xpt(knew,j)
23082    continue
23080 continue
      pq(knew)=zero

c Update the other second derivative parameters, and then the gradient
c vector of the model. Also include the new interpolation point.

      do 23084 j=1,nptm
         temp=diff*zmat(knew,j)
         if (j .lt. idz) temp=-temp
         do 23086 k=1,npt
            pq(k)=pq(k)+temp*zmat(k,j)
23086    continue
23084 continue
      gqsq=zero
      do 23088 i=1,n
         gq(i)=gq(i)+diff*bmat(knew,i)
         gqsq=gqsq+gq(i)**2
         xpt(knew,i)=xnew(i)
23088 continue

c If a trust region step makes a small change to the objective function,
c then calculate the gradient of the least Frobenius norm interpolant at
c XBASE, and store it in W, using VLAG for a vector of right hand sides.

      if (ksave .eq. 0 .and. delta .eq. rho) then
         if (abs(ratio) .gt. 1.0d-2) then
            itest=0
         else
            do 23090 k=1,npt
               vlag(k)=fval(k)-fval(kopt)
23090       continue
            gisq=zero
            do 23092 i=1,n
               sum=zero
               do 23094 k=1,npt
                  sum=sum+bmat(k,i)*vlag(k)
23094          continue
               gisq=gisq+sum*sum
               w(i)=sum
23092       continue

c Test whether to replace the new quadratic model by the
c least Frobenius norm interpolant, making the replacement
c if the test is satisfied.

            itest=itest+1
            if (gqsq .lt. 1.0d+2*gisq) itest=0
            if (itest .ge. 3) then
               do 23096 i=1,n
                  gq(i)=w(i)
23096          continue
               do 23098 ih=1,nh
                  hq(ih)=zero
23098          continue
               do 23100 j=1,nptm
                  w(j)=zero
                  do 23102 k=1,npt
                     w(j)=w(j)+vlag(k)*zmat(k,j)
23102             continue
                  if (j .lt. idz) w(j)=-w(j)
23100          continue
               do 23104 k=1,npt
                  pq(k)=zero
                  do 23106 j=1,nptm
                     pq(k)=pq(k)+zmat(k,j)*w(j)
23106             continue
23104          continue
               itest=0
            endif
         endif
      endif
      if (f .lt. fsave) kopt=knew

c If a trust region step has provided a sufficient decrease in F, then
c branch for another trust region calculation. The case KSAVE>0 occurs
c when the new function value was calculated by a model step.

      if (f .le. fsave+tenth*vquad) goto 100
      if (ksave .gt. 0) goto 100

c Alternatively, find out if the interpolation points are close enough
c to the best point so far.

      knew=0
  460 distsq=4.0d0*delta*delta
      do 23108 k=1,npt
         sum=zero
         do 23110 j=1,n
            sum=sum+(xpt(k,j)-xopt(j))**2
23110    continue
         if (sum .gt. distsq) then
            knew=k
            distsq=sum
         endif
23108 continue

c If KNEW is positive, then set DSTEP, and branch back for the next
c iteration, which will generate a "model step".

      if (knew .gt. 0) then
         dstep=max(min(tenth*sqrt(distsq),half*delta),rho)
         dsq=dstep*dstep
         goto 120
      endif
      if (ratio .gt. zero) goto 100
      if (max(delta,dnorm) .gt. rho) goto 100

c The calculations with the current value of RHO are complete. Pick the
c next values of RHO and DELTA.

  490 if (rho .gt. rhoend) then
         delta=half*rho
         ratio=rho/rhoend
         if (ratio .le. 16.0d0) then
            rho=rhoend
         elseif (ratio .le. 250.0d0) then
            rho=sqrt(ratio)*rhoend
         else
            rho=tenth*rho
         endif
         rho_uoa=rho
         delta=max(delta,rho)
         if (iprint .ge. 2) then
            if (iprint .ge. 3) print 500
  500       format (5x)
            print 510, rho,nf
  510       format (/4x,'New RHO =',1pd11.4,5x,'Number of', 
     &         ' function values =',i6)
            print 520, fopt,(xbase(i)+xopt(i),i=1,n)
  520       format (4x,'Least value of F =',1pd23.15,9x, 
     &         'The corresponding X is:'/(2x,5d15.6))
         endif
         goto 90
      endif

c Return from the calculation, after another Newton-Raphson step, if
c it is too short to have been tried before.

      if (knew .eq. -1) goto 290
  530 if (fopt .le. f) then
         do 23112 i=1,n
            x(i)=xbase(i)+xopt(i)
23112    continue
         f=fopt
      endif
      if (iprint .ge. 1) then
         print 550, nf
  550    format (/4x,'At the return from NEWUOA',5x, 
     &      'Number of function values =',i6)
         print 520, f,(x(i),i=1,n)
      endif
      return

c newuob
      end

c----------------------------------------------------------------------
c bigden.m,v 1.3 2006/08/12 18:27:06 bulmer Exp

      subroutine bigden (n,npt,xopt,xpt,bmat,zmat,idz,ndim,kopt, knew,d,
     &   w,vlag,beta,s,wvec,prod)
cProlog

      implicit real*8 (a-h,o-z), integer (i-n)

      dimension xopt(*),xpt(npt,*),bmat(ndim,*),zmat(npt,*),d(*)
      dimension w(*),vlag(*),s(*),wvec(ndim,*),prod(ndim,*)
      dimension den(9),denex(9),par(9)

c N is the number of variables.
c NPT is the number of interpolation equations.
c XOPT is the best interpolation point so far.
c XPT contains the coordinates of the current interpolation points.
c BMAT provides the last N columns of H.
c ZMAT and IDZ give a factorization of the first NPT by NPT submatrix of H.
c NDIM is the first dimension of BMAT and has the value NPT+N.
c KOPT is the index of the optimal interpolation point.
c KNEW is the index of the interpolation point that is going to be moved.
c D will be set to the step from XOPT to the new point, and on entry it
c   should be the D that was calculated by the last call of BIGLAG. The
c   length of the initial D provides a trust region bound on the final D.
c W will be set to Wcheck for the final choice of D.
c VLAG will be set to Theta*Wcheck+e_b for the final choice of D.
c BETA will be set to the value that will occur in the updating formula
c   when the KNEW-th interpolation point is moved to its new position.
c S, WVEC, PROD and the private arrays DEN, DENEX and PAR will be used
c   for working space.
c
c D is calculated in a way that should provide a denominator with a large
c modulus in the updating formula when the KNEW-th interpolation point is
c shifted to the new position XOPT+D.

      half=0.5d0
      one=1.0d0
      quart=0.25d0
      two=2.0d0
      zero=0.0d0
      twopi=8.0d0*atan(one)
      nptm=npt-n-1

c Store the first NPT elements of the KNEW-th column of H in W(N+1)
c to W(N+NPT).

      do 23000 k=1,npt
         w(n+k)=zero
23000 continue
      do 23002 j=1,nptm
         temp=zmat(knew,j)
         if (j .lt. idz) temp=-temp
         do 23004 k=1,npt
            w(n+k)=w(n+k)+temp*zmat(k,j)
23004    continue
23002 continue
      alpha=w(n+knew)

c The initial search direction D is taken from the last call of BIGLAG,
c and the initial S is set below, usually to the direction from X_OPT
c to X_KNEW, but a different direction to an interpolation point may
c be chosen, in order to prevent S from being nearly parallel to D.

      dd=zero
      ds=zero
      ss=zero
      xoptsq=zero
      do 23006 i=1,n
         dd=dd+d(i)**2
         s(i)=xpt(knew,i)-xopt(i)
         ds=ds+d(i)*s(i)
         ss=ss+s(i)**2
         xoptsq=xoptsq+xopt(i)**2
23006 continue
      if (ds*ds .gt. 0.99d0*dd*ss) then
         ksav=knew
         dtest=ds*ds/ss
         do 23008 k=1,npt
            if (k .ne. kopt) then
               dstemp=zero
               sstemp=zero
               do 23010 i=1,n
                  diff=xpt(k,i)-xopt(i)
                  dstemp=dstemp+d(i)*diff
                  sstemp=sstemp+diff*diff
23010          continue
               if (dstemp*dstemp/sstemp .lt. dtest) then
                  ksav=k
                  dtest=dstemp*dstemp/sstemp
                  ds=dstemp
                  ss=sstemp
               endif
            endif
23008    continue
         do 23012 i=1,n
            s(i)=xpt(ksav,i)-xopt(i)
23012    continue
      endif
      ssden=dd*ss-ds*ds
      iterc=0
      densav=zero

c Begin the iteration by overwriting S with a vector that has the
c required length and direction.

   70 iterc=iterc+1
      temp=one/sqrt(ssden)
      xoptd=zero
      xopts=zero
      do 23014 i=1,n
         s(i)=temp*(dd*s(i)-ds*d(i))
         xoptd=xoptd+xopt(i)*d(i)
         xopts=xopts+xopt(i)*s(i)
23014 continue

c Set the coefficients of the first two terms of BETA.

      tempa=half*xoptd*xoptd
      tempb=half*xopts*xopts
      den(1)=dd*(xoptsq+half*dd)+tempa+tempb
      den(2)=two*xoptd*dd
      den(3)=two*xopts*dd
      den(4)=tempa-tempb
      den(5)=xoptd*xopts
      do 23016 i=6,9
         den(i)=zero
23016 continue

c Put the coefficients of Wcheck in WVEC.

      do 23018 k=1,npt
         tempa=zero
         tempb=zero
         tempc=zero
         do 23020 i=1,n
            tempa=tempa+xpt(k,i)*d(i)
            tempb=tempb+xpt(k,i)*s(i)
            tempc=tempc+xpt(k,i)*xopt(i)
23020    continue
         wvec(k,1)=quart*(tempa*tempa+tempb*tempb)
         wvec(k,2)=tempa*tempc
         wvec(k,3)=tempb*tempc
         wvec(k,4)=quart*(tempa*tempa-tempb*tempb)
         wvec(k,5)=half*tempa*tempb
23018 continue
      do 23022 i=1,n
         ip=i+npt
         wvec(ip,1)=zero
         wvec(ip,2)=d(i)
         wvec(ip,3)=s(i)
         wvec(ip,4)=zero
         wvec(ip,5)=zero
23022 continue

c Put the coefficents of THETA*Wcheck in PROD.

      do 23024 jc=1,5
         nw=npt
         if (jc .eq. 2 .or. jc .eq. 3) nw=ndim
         do 23026 k=1,npt
            prod(k,jc)=zero
23026    continue
         do 23028 j=1,nptm
            sum=zero
            do 23030 k=1,npt
               sum=sum+zmat(k,j)*wvec(k,jc)
23030       continue
            if (j .lt. idz) sum=-sum
            do 23032 k=1,npt
               prod(k,jc)=prod(k,jc)+sum*zmat(k,j)
23032       continue
23028    continue
         if (nw .eq. ndim) then
            do 23034 k=1,npt
               sum=zero
               do 23036 j=1,n
                  sum=sum+bmat(k,j)*wvec(npt+j,jc)
23036          continue
               prod(k,jc)=prod(k,jc)+sum
23034       continue
         endif
         do 23038 j=1,n
            sum=zero
            do 23040 i=1,nw
               sum=sum+bmat(i,j)*wvec(i,jc)
23040       continue
            prod(npt+j,jc)=sum
23038    continue
23024 continue

c Include in DEN the part of BETA that depends on THETA.

      do 23042 k=1,ndim
         sum=zero
         do 23044 i=1,5
            par(i)=half*prod(k,i)*wvec(k,i)
            sum=sum+par(i)
23044    continue
         den(1)=den(1)-par(1)-sum
         tempa=prod(k,1)*wvec(k,2)+prod(k,2)*wvec(k,1)
         tempb=prod(k,2)*wvec(k,4)+prod(k,4)*wvec(k,2)
         tempc=prod(k,3)*wvec(k,5)+prod(k,5)*wvec(k,3)
         den(2)=den(2)-tempa-half*(tempb+tempc)
         den(6)=den(6)-half*(tempb-tempc)
         tempa=prod(k,1)*wvec(k,3)+prod(k,3)*wvec(k,1)
         tempb=prod(k,2)*wvec(k,5)+prod(k,5)*wvec(k,2)
         tempc=prod(k,3)*wvec(k,4)+prod(k,4)*wvec(k,3)
         den(3)=den(3)-tempa-half*(tempb-tempc)
         den(7)=den(7)-half*(tempb+tempc)
         tempa=prod(k,1)*wvec(k,4)+prod(k,4)*wvec(k,1)
         den(4)=den(4)-tempa-par(2)+par(3)
         tempa=prod(k,1)*wvec(k,5)+prod(k,5)*wvec(k,1)
         tempb=prod(k,2)*wvec(k,3)+prod(k,3)*wvec(k,2)
         den(5)=den(5)-tempa-half*tempb
         den(8)=den(8)-par(4)+par(5)
         tempa=prod(k,4)*wvec(k,5)+prod(k,5)*wvec(k,4)
         den(9)=den(9)-half*tempa
23042 continue

c Extend DEN so that it holds all the coefficients of DENOM.

      sum=zero
      do 23046 i=1,5
         par(i)=half*prod(knew,i)**2
         sum=sum+par(i)
23046 continue
      denex(1)=alpha*den(1)+par(1)+sum
      tempa=two*prod(knew,1)*prod(knew,2)
      tempb=prod(knew,2)*prod(knew,4)
      tempc=prod(knew,3)*prod(knew,5)
      denex(2)=alpha*den(2)+tempa+tempb+tempc
      denex(6)=alpha*den(6)+tempb-tempc
      tempa=two*prod(knew,1)*prod(knew,3)
      tempb=prod(knew,2)*prod(knew,5)
      tempc=prod(knew,3)*prod(knew,4)
      denex(3)=alpha*den(3)+tempa+tempb-tempc
      denex(7)=alpha*den(7)+tempb+tempc
      tempa=two*prod(knew,1)*prod(knew,4)
      denex(4)=alpha*den(4)+tempa+par(2)-par(3)
      tempa=two*prod(knew,1)*prod(knew,5)
      denex(5)=alpha*den(5)+tempa+prod(knew,2)*prod(knew,3)
      denex(8)=alpha*den(8)+par(4)-par(5)
      denex(9)=alpha*den(9)+prod(knew,4)*prod(knew,5)

c Seek the value of the angle that maximizes the modulus of DENOM.

      sum=denex(1)+denex(2)+denex(4)+denex(6)+denex(8)
      denold=sum
      denmax=sum
      isave=0
      iu=49
      temp=twopi/dble(iu+1)
      par(1)=one
      do 23048 i=1,iu
         angle=dble(i)*temp
         par(2)=cos(angle)
         par(3)=sin(angle)
         do 23050 j=4,8,2
            par(j)=par(2)*par(j-2)-par(3)*par(j-1)
            par(j+1)=par(2)*par(j-1)+par(3)*par(j-2)
23050    continue
         sumold=sum
         sum=zero
         do 23052 j=1,9
            sum=sum+denex(j)*par(j)
23052    continue
         if (abs(sum) .gt. abs(denmax)) then
            denmax=sum
            isave=i
            tempa=sumold
         elseif (i .eq. isave+1) then
            tempb=sum
         endif
23048 continue
      if (isave .eq. 0) tempa=sum
      if (isave .eq. iu) tempb=denold
      step=zero
      if (tempa .ne. tempb) then
         tempa=tempa-denmax
         tempb=tempb-denmax
         step=half*(tempa-tempb)/(tempa+tempb)
      endif
      angle=temp*(dble(isave)+step)

c Calculate the new parameters of the denominator, the new VLAG vector
c and the new D. Then test for convergence.

      par(2)=cos(angle)
      par(3)=sin(angle)
      do 23054 j=4,8,2
         par(j)=par(2)*par(j-2)-par(3)*par(j-1)
         par(j+1)=par(2)*par(j-1)+par(3)*par(j-2)
23054 continue
      beta=zero
      denmax=zero
      do 23056 j=1,9
         beta=beta+den(j)*par(j)
         denmax=denmax+denex(j)*par(j)
23056 continue
      do 23058 k=1,ndim
         vlag(k)=zero
         do 23060 j=1,5
            vlag(k)=vlag(k)+prod(k,j)*par(j)
23060    continue
23058 continue
      tau=vlag(knew)
      dd=zero
      tempa=zero
      tempb=zero
      do 23062 i=1,n
         d(i)=par(2)*d(i)+par(3)*s(i)
         w(i)=xopt(i)+d(i)
         dd=dd+d(i)**2
         tempa=tempa+d(i)*w(i)
         tempb=tempb+w(i)*w(i)
23062 continue
      if (iterc .ge. n) goto 340
      if (iterc .gt. 1) densav=max(densav,denold)
      if (abs(denmax) .le. 1.1d0*abs(densav)) goto 340
      densav=denmax

c Set S to half the gradient of the denominator with respect to D.
c Then branch for the next iteration.

      do 23064 i=1,n
         temp=tempa*xopt(i)+tempb*d(i)-vlag(npt+i)
         s(i)=tau*bmat(knew,i)+alpha*temp
23064 continue
      do 23066 k=1,npt
         sum=zero
         do 23068 j=1,n
            sum=sum+xpt(k,j)*w(j)
23068    continue
         temp=(tau*w(n+k)-alpha*vlag(k))*sum
         do 23070 i=1,n
            s(i)=s(i)+temp*xpt(k,i)
23070    continue
23066 continue
      ss=zero
      ds=zero
      do 23072 i=1,n
         ss=ss+s(i)**2
         ds=ds+d(i)*s(i)
23072 continue
      ssden=dd*ss-ds*ds
      if (ssden .ge. 1.0d-8*dd*ss) goto 70

c Set the vector W before the RETURN from the subroutine.

  340 do 23074 k=1,ndim
         w(k)=zero
         do 23076 j=1,5
            w(k)=w(k)+wvec(k,j)*par(j)
23076    continue
23074 continue
      vlag(kopt)=vlag(kopt)+one

      return

c bigden
      end

c----------------------------------------------------------------------
c biglag.m,v 1.3 2006/08/12 18:27:06 bulmer Exp

      subroutine biglag(n,npt,xopt,xpt,bmat,zmat,idz,ndim,knew, delta,d,
     &   alpha,hcol,gc,gd,s,w)
cProlog

      implicit doubleprecision (a-h,o-z), integer (i-n)
      dimension xopt(*),xpt(npt,*),bmat(ndim,*),zmat(npt,*),d(*)
      dimension hcol(*),gc(*),gd(*),s(*),w(*)

c N is the number of variables.
c NPT is the number of interpolation equations.
c XOPT is the best interpolation point so far.
c XPT contains the coordinates of the current interpolation points.
c BMAT provides the last N columns of H.
c ZMAT and IDZ give a factorization of the first NPT by NPT submatrix of H.
c NDIM is the first dimension of BMAT and has the value NPT+N.
c KNEW is the index of the interpolation point that is going to be moved.
c DELTA is the current trust region bound.
c D will be set to the step from XOPT to the new point.
c ALPHA will be set to the KNEW-th diagonal element of the H matrix.
c HCOL, GC, GD, S and W will be used for working space.
c
c The step D is calculated in a way that attempts to maximize the modulus
c of LFUNC(XOPT+D), subject to the bound ||D|| <= DELTA, where LFUNC is
c the KNEW-th Lagrange function.

      half=0.5d0
      one=1.0d0
      zero=0.0d0
      twopi=8.0d0*atan(one)
      delsq=delta*delta
      nptm=npt-n-1

c Set the first NPT components of HCOL to the leading elements of the
c KNEW-th column of H.

      iterc=0
      do 23000 k=1,npt
         hcol(k)=zero
23000 continue
      do 23002 j=1,nptm
         temp=zmat(knew,j)
         if (j .lt. idz) temp=-temp
         do 23004 k=1,npt
            hcol(k)=hcol(k)+temp*zmat(k,j)
23004    continue
23002 continue
      alpha=hcol(knew)

c Set the unscaled initial direction D. Form the gradient of LFUNC at
c XOPT, and multiply D by the second derivative matrix of LFUNC.

      dd=zero
      do 23006 i=1,n
         d(i)=xpt(knew,i)-xopt(i)
         gc(i)=bmat(knew,i)
         gd(i)=zero
         dd=dd+d(i)**2
23006 continue
      do 23008 k=1,npt
         temp=zero
         sum=zero
         do 23010 j=1,n
            temp=temp+xpt(k,j)*xopt(j)
            sum=sum+xpt(k,j)*d(j)
23010    continue
         temp=hcol(k)*temp
         sum=hcol(k)*sum
         do 23012 i=1,n
            gc(i)=gc(i)+temp*xpt(k,i)
            gd(i)=gd(i)+sum*xpt(k,i)
23012    continue
23008 continue

c Scale D and GD, with a sign change if required. Set S to another
c vector in the initial two dimensional subspace.

      gg=zero
      sp=zero
      dhd=zero
      do 23014 i=1,n
         gg=gg+gc(i)**2
         sp=sp+d(i)*gc(i)
         dhd=dhd+d(i)*gd(i)
23014 continue
      scale=delta/dsqrt(dd)
      if (sp*dhd .lt. zero) scale=-scale
      temp=zero
      if (sp*sp .gt. 0.99d0*dd*gg) temp=one
      tau=scale*(abs(sp)+half*scale*abs(dhd))
      if (gg*delsq .lt. 0.01d0*tau*tau) temp=one
      do 23016 i=1,n
         d(i)=scale*d(i)
         gd(i)=scale*gd(i)
         s(i)=gc(i)+temp*gd(i)
23016 continue

c Begin the iteration by overwriting S with a vector that has the
c required length and direction, except that termination occurs if
c the given D and S are nearly parallel.

   80 iterc=iterc+1
      dd=zero
      sp=zero
      ss=zero
      do 23018 i=1,n
         dd=dd+d(i)**2
         sp=sp+d(i)*s(i)
         ss=ss+s(i)**2
23018 continue
      temp=dd*ss-sp*sp
      if (temp .le. 1.0d-8*dd*ss) goto 160
      denom=sqrt(temp)
      do 23020 i=1,n
         s(i)=(dd*s(i)-sp*d(i))/denom
         w(i)=zero
23020 continue

c Calculate the coefficients of the objective function on the circle,
c beginning with the multiplication of S by the second derivative matrix.

      do 23022 k=1,npt
         sum=zero
         do 23024 j=1,n
            sum=sum+xpt(k,j)*s(j)
23024    continue
         sum=hcol(k)*sum
         do 23026 i=1,n
            w(i)=w(i)+sum*xpt(k,i)
23026    continue
23022 continue
      cf1=zero
      cf2=zero
      cf3=zero
      cf4=zero
      cf5=zero
      do 23028 i=1,n
         cf1=cf1+s(i)*w(i)
         cf2=cf2+d(i)*gc(i)
         cf3=cf3+s(i)*gc(i)
         cf4=cf4+d(i)*gd(i)
         cf5=cf5+s(i)*gd(i)
23028 continue
      cf1=half*cf1
      cf4=half*cf4-cf1

c Seek the value of the angle that maximizes the modulus of TAU.

      taubeg=cf1+cf2+cf4
      taumax=taubeg
      tauold=taubeg
      isave=0
      iu=49
      temp=twopi/dble(iu+1)
      do 23030 i=1,iu
         angle=dble(i)*temp
         cth=cos(angle)
         sth=sin(angle)
         tau=cf1+(cf2+cf4*cth)*cth+(cf3+cf5*cth)*sth
         if (abs(tau) .gt. abs(taumax)) then
            taumax=tau
            isave=i
            tempa=tauold
         elseif (i .eq. isave+1) then
            tempb=tau
         endif
         tauold=tau
23030 continue
      if (isave .eq. 0) tempa=tau
      if (isave .eq. iu) tempb=taubeg
      step=zero
      if (tempa .ne. tempb) then
         tempa=tempa-taumax
         tempb=tempb-taumax
         step=half*(tempa-tempb)/(tempa+tempb)
      endif
      angle=temp*(dble(isave)+step)

c Calculate the new D and GD. Then test for convergence.

      cth=cos(angle)
      sth=sin(angle)
      tau=cf1+(cf2+cf4*cth)*cth+(cf3+cf5*cth)*sth
      do 23032 i=1,n
         d(i)=cth*d(i)+sth*s(i)
         gd(i)=cth*gd(i)+sth*w(i)
         s(i)=gc(i)+gd(i)
23032 continue

      if (dabs(tau) .le. 1.1d0*abs(taubeg)) goto 160
      if (iterc .lt. n) goto 80
  160 return

c biglag
      end

c----------------------------------------------------------------------
c trsapp.m,v 1.5 2006/08/12 18:27:06 bulmer Exp

      subroutine trsapp(n,npt,xopt,xpt,gq,hq,pq,delta,step,d,g,hd,hs,
     &   crvmin)
cProlog

      implicit doubleprecision (a-h,o-z), integer (i-n)
      dimension xopt(*),xpt(npt,*),gq(*),hq(*),pq(*),step(*),d(*),g(*),
     &   hd(*),hs(*)

c N is the number of variables of a quadratic objective function, Q say.
c The arguments NPT, XOPT, XPT, GQ, HQ and PQ have their usual meanings,
c   in order to define the current quadratic model Q.
c DELTA is the trust region radius, and has to be positive.
c STEP will be set to the calculated trial step.
c The arrays D, G, HD and HS will be used for working space.
c CRVMIN will be set to the least curvature of H along the conjugate
c directions that occur, except that it is set to zero if STEP goes
c all the way to the trust region boundary.
c
c The calculation of STEP begins with the truncated conjugate gradient
c method. If the boundary of the trust region is reached, then further
c changes to STEP may be made, each one being in the 2D space spanned
c by the current STEP and the corresponding gradient of Q. Thus STEP
c should provide a substantial reduction to Q within the trust region.
c
c Initialization, which includes setting HD to H times XOPT.

      half=0.5d0
      zero=0.0d0
      twopi=8.0d0*atan(1.0d0)
      delsq=delta*delta
      iterc=0
      itermax=n
      itersw=itermax
      do 23000 i=1,n
         d(i)=xopt(i)
23000 continue
      goto 170

c Prepare for the first line search.

   20 qred=zero
      dd=zero
      do 23002 i=1,n
         step(i)=zero
         hs(i)=zero
         g(i)=gq(i)+hd(i)
         d(i)=-g(i)
         dd=dd+d(i)**2
23002 continue
      crvmin=zero
      if (dd .eq. zero) goto 160
      ds=zero
      ss=zero
      gg=dd
      ggbeg=gg

c Calculate the step to the trust region boundary and the product HD.

   40 iterc=iterc+1
      temp=delsq-ss
      arg=ds*ds+dd*temp
      if (arg .le. 0.0d0) then
         call xerrab(
     &      '***FATAL in UOA (trsapp: divide-by-zero, reduce rhobeg')
      endif
      bstep=temp/(ds+sqrt(ds*ds+dd*temp))
      goto 170
   50 dhd=zero
      do 23004 j=1,n
         dhd=dhd+d(j)*hd(j)
23004 continue

c Update CRVMIN and set the step-length ALPHA.

      alpha=bstep
      if (dhd .gt. zero) then
         temp=dhd/dd
         if (iterc .eq. 1) crvmin=temp
         crvmin=min(crvmin,temp)
         alpha=min(alpha,gg/dhd)
      endif
      qadd=alpha*(gg-half*alpha*dhd)
      qred=qred+qadd

c  Update STEP and HS.

      ggsav=gg
      gg=zero
      do 23006 i=1,n
         step(i)=step(i)+alpha*d(i)
         hs(i)=hs(i)+alpha*hd(i)
         gg=gg+(g(i)+hs(i))**2
23006 continue

c  Begin another conjugate direction iteration if required.

      if (alpha .lt. bstep) then
         if (qadd .le. 0.01d0*qred) goto 160
         if (gg .le. 0.0001d0*ggbeg) goto 160
         if (iterc .eq. itermax) goto 160
         temp=gg/ggsav
         dd=zero
         ds=zero
         ss=zero
         do 23008 i=1,n
            d(i)=temp*d(i)-g(i)-hs(i)
            dd=dd+d(i)**2
            ds=ds+d(i)*step(i)
            ss=ss+step(i)**2
23008    continue
         if (ds .le. zero) goto 160
         if (ss .lt. delsq) goto 40
      endif
      crvmin=zero
      itersw=iterc

c Test whether an alternative iteration is required.

   90 if (gg .le. 1.0d-4*ggbeg) goto 160
      sg=zero
      shs=zero
      do 23010 i=1,n
         sg=sg+step(i)*g(i)
         shs=shs+step(i)*hs(i)
23010 continue
      sgk=sg+shs
      angtest=sgk/sqrt(gg*delsq)
      if (angtest .le. -0.99d0) goto 160

c  Begin the alternative iteration by calculating D and HD and some
c  scalar products.

      iterc=iterc+1
      temp=sqrt(delsq*gg-sgk*sgk)
      tempa=delsq/temp
      tempb=sgk/temp
      do 23012 i=1,n
         d(i)=tempa*(g(i)+hs(i))-tempb*step(i)
23012 continue
      goto 170
  120 dg=zero
      dhd=zero
      dhs=zero
      do 23014 i=1,n
         dg=dg+d(i)*g(i)
         dhd=dhd+hd(i)*d(i)
         dhs=dhs+hd(i)*step(i)
23014 continue

c Seek the value of the angle that minimizes Q.

      cf=half*(shs-dhd)
      qbeg=sg+cf
      qsav=qbeg
      qmin=qbeg
      isave=0
      iu=49
      temp=twopi/dble(iu+1)
      do 23016 i=1,iu
         angle=dble(i)*temp
         cth=cos(angle)
         sth=sin(angle)
         qnew=(sg+cf*cth)*cth+(dg+dhs*cth)*sth
         if (qnew .lt. qmin) then
            qmin=qnew
            isave=i
            tempa=qsav
         elseif (i .eq. isave+1) then
            tempb=qnew
         endif
         qsav=qnew
23016 continue
      if (isave .eq. zero) tempa=qnew
      if (isave .eq. iu) tempb=qbeg
      angle=zero
      if (tempa .ne. tempb) then
         tempa=tempa-qmin
         tempb=tempb-qmin
         angle=half*(tempa-tempb)/(tempa+tempb)
      endif
      angle=temp*(dble(isave)+angle)

c Calculate the new STEP and HS. Then test for convergence.

      cth=cos(angle)
      sth=sin(angle)
      reduc=qbeg-(sg+cf*cth)*cth-(dg+dhs*cth)*sth
      gg=zero
      do 23018 i=1,n
         step(i)=cth*step(i)+sth*d(i)
         hs(i)=cth*hs(i)+sth*hd(i)
         gg=gg+(g(i)+hs(i))**2
23018 continue
      qred=qred+reduc
      ratio=reduc/qred
      if (iterc .lt. itermax .and. ratio .gt. 0.01d0) goto 90
  160 return

c The following instructions act as a subroutine for setting the vector
c HD to the vector D multiplied by the second derivative matrix of Q.
c They are called from three different places, which are distinguished
c by the value of ITERC.

  170 do 23020 i=1,n
         hd(i)=zero
23020 continue
      do 23022 k=1,npt
         temp=zero
         do 23024 j=1,n
            temp=temp+xpt(k,j)*d(j)
23024    continue
         temp=temp*pq(k)
         do 23026 i=1,n
            hd(i)=hd(i)+temp*xpt(k,i)
23026    continue
23022 continue
      ih=0
      do 23028 j=1,n
         do 23030 i=1,j
            ih=ih+1
            if (i .lt. j) hd(j)=hd(j)+hq(ih)*d(i)
            hd(i)=hd(i)+hq(ih)*d(j)
23030    continue
23028 continue
      if (iterc .eq. 0) goto 20
      if (iterc .le. itersw) goto 50
      goto 120

c trsapp
      end

c----------------------------------------------------------------------
c update.m,v 1.3 2006/08/12 18:27:06 bulmer Exp

      subroutine update(n,npt,bmat,zmat,idz,ndim,vlag,beta,knew,w)
cProlog

      implicit doubleprecision (a-h,o-z), integer (i-n)
      dimension bmat(ndim,*),zmat(npt,*),vlag(*),w(*)

c The arrays BMAT and ZMAT with IDZ are updated, in order to shift the
c interpolation point that has index KNEW. On entry, VLAG contains the
c components of the vector Theta*Wcheck+e_b of the updating formula
c (6.11), and BETA holds the value of the parameter that has this name.
c The vector W is used for working space.
c
c Set some constants.

      one=1.0d0
      zero=0.0d0
      nptm=npt-n-1

c Apply the rotations that put zeros in the KNEW-th row of ZMAT.

      jl=1
      do 23000 j=2,nptm
         if (j .eq. idz) then
            jl=idz
         elseif (zmat(knew,j) .ne. zero) then
            temp=sqrt(zmat(knew,jl)**2+zmat(knew,j)**2)
            tempa=zmat(knew,jl)/temp
            tempb=zmat(knew,j)/temp
            do 23002 i=1,npt
               temp=tempa*zmat(i,jl)+tempb*zmat(i,j)
               zmat(i,j)=tempa*zmat(i,j)-tempb*zmat(i,jl)
               zmat(i,jl)=temp
23002       continue
            zmat(knew,j)=zero
         endif
23000 continue

c Put the first NPT components of the KNEW-th column of HLAG into W,
c and calculate the parameters of the updating formula.

      tempa=zmat(knew,1)
      if (idz .ge. 2) tempa=-tempa
      if (jl .gt. 1) tempb=zmat(knew,jl)
      do 23004 i=1,npt
         w(i)=tempa*zmat(i,1)
         if (jl .gt. 1) w(i)=w(i)+tempb*zmat(i,jl)
23004 continue
      alpha=w(knew)
      tau=vlag(knew)
      tausq=tau*tau
      denom=alpha*beta+tausq
      vlag(knew)=vlag(knew)-one

c Complete the updating of ZMAT when there is only one nonzero element
c in the KNEW-th row of the new matrix ZMAT, but, if IFLAG is set to one,
c then the first column of ZMAT will be exchanged with another one later.

      iflag=0
      if (jl .eq. 1) then
         temp=sqrt(abs(denom))
         tempb=tempa/temp
         tempa=tau/temp
         do 23006 i=1,npt
            zmat(i,1)=tempa*zmat(i,1)-tempb*vlag(i)
23006    continue
         if (idz .eq. 1 .and. temp .lt. zero) idz=2
         if (idz .ge. 2 .and. temp .ge. zero) iflag=1
      else
c Complete the updating of ZMAT in the alternative case.
         ja=1
         if (beta .ge. zero) ja=jl
         jb=jl+1-ja
         temp=zmat(knew,jb)/denom
         tempa=temp*beta
         tempb=temp*tau
         temp=zmat(knew,ja)
         scala=one/sqrt(abs(beta)*temp*temp+tausq)
         scalb=scala*sqrt(abs(denom))
         do 23008 i=1,npt
            zmat(i,ja)=scala*(tau*zmat(i,ja)-temp*vlag(i))
            zmat(i,jb)=scalb*(zmat(i,jb)-tempa*w(i)-tempb*vlag(i))
23008    continue
         if (denom .le. zero) then
            if (beta .lt. zero) idz=idz+1
            if (beta .ge. zero) iflag=1
         endif
      endif

c IDZ is reduced in the following case, and usually the first column
c of ZMAT is exchanged with a later one.

      if (iflag .eq. 1) then
         idz=idz-1
         do 23010 i=1,npt
            temp=zmat(i,1)
            zmat(i,1)=zmat(i,idz)
            zmat(i,idz)=temp
23010    continue
      endif

c Finally, update the matrix BMAT.

      do 23012 j=1,n
         jp=npt+j
         w(jp)=bmat(knew,j)
         tempa=(alpha*vlag(jp)-tau*w(jp))/denom
         tempb=(-beta*w(jp)-tau*vlag(jp))/denom
         do 23014 i=1,jp
            bmat(i,j)=bmat(i,j)+tempa*vlag(i)+tempb*w(i)
            if (i .gt. npt) bmat(jp,i-npt)=bmat(i,j)
23014    continue
23012 continue

      return

c update
      end

c----------------------------------------------------------------------
c calfun.m,v 1.2 2004/10/10 19:51:43 bulmer Exp


      subroutine calfun(n,x,f)
cProlog

      implicit doubleprecision (a-h,o-z), integer (i-n)
c Group UOA
      double precision rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      integer n_uoa, npt_uoa, m_uoa

      double precision x_uoa ( n_uoa)
      pointer(px_uoa,x_uoa)

      double precision w_uoa ( m_uoa)
      pointer(pw_uoa,w_uoa)
      common /svr10/ n_uoa, npt_uoa, m_uoa
      common /svr13/ rhobeg_uoa, rhoend_uoa, rho_uoa, f_uoa
      common /svr16/ px_uoa, pw_uoa
c End of UOA


c This routine, which was the user-supplied object function evaluator
c in the original Fortran NEWUOA, now executes a Basis script function
c which is a wrapper for the new user-supplied script (of arbitrary
c name) that evaluates the object function.

      dimension x(*)

      do 23000 i=1,n
         x_uoa(i)=x(i)
23000 continue
c_tdr      call parsestr("f_uoa=objfcn_newuoa(x_uoa)")
      call remark('***Must provide functionality just above to use')
      call remark('***parsestr does not work for c++ uedge')
      call xerrab("")
      f=f_uoa

      return

c calfun
      end
