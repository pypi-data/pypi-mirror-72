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
c     ./../svrut3.m
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
      SUBROUTINE SHEQR (A, LDA, N, Q, INFO, IJOB)
      doubleprecision A, Q
      INTEGER LDA, N, INFO, IJOB
      DIMENSION A(LDA, *), Q(*)
c-----------------------------------------------------------------------
c     This routine performs a QR decomposition of an upper
c     Hessenberg matrix A.  There are two options available:
c
c          (1)  Performing a fresh decomposition.
c          (2)  Updating the QR factors by adding a row and a
c               column to the matrix A.
c-----------------------------------------------------------------------
c     SHEQR decomposes an upper Hessenberg matrix by using Givens
c     rotations.
c
c     On entry
c
c        A       real(LDA, N)
c                The matrix to be decomposed.
c
c        LDA     integer
c                The leading dimension of the array  A.
c
c        N       integer
c                A is an (N+1) by N Hessenberg matrix.
c
c        IJOB    integer
c                = 1     means that a fresh decomposition of the
c                        matrix A is desired.
c                .ge. 2  means that the current decomposition of A
c                        will be updated by the addition of a row
c                        and a column.
c     On return
c
c        A       The upper triangular matrix R.
c                The factorization can be written Q*A = R, where
c                Q is a product of Givens rotations and R is upper
c                triangular.
c
c        Q       real(2*N)
c                the factors c and s of each Givens rotation used
c                in decomposing A.
c
c        INFO    integer
c                = 0  normal value.
c                = k  if  A(k,k) .eq. 0.0 .  This is not an error
c                     condition for this subroutine, but it does
c                     indicate that SHELS will divide by zero
c                     if called.
c
c     This version dated 1/13/86.
c     Peter Brown, University of Houston, Lawrence Livermore Natl. Lab.
c
c-----------------------------------------------------------------------
c
c Type declarations for local variables --------------------------------
c
      doubleprecision C, S, T, T1, T2
      INTEGER I, IQ, J, K, KM1, KP1, NM1
c
      IF (IJOB .GT. 1) GO TO 70
c-----------------------------------------------------------------------
c A new facorization is desired.
c-----------------------------------------------------------------------
c
c     QR decomposition without pivoting
c
      INFO = 0
      DO 60 K = 1, N
      KM1 = K - 1
      KP1 = K + 1
c
c           Compute kth column of R.
c           First, multiply the kth column of A by the previous
c           k-1 Givens rotations.
c
      IF (KM1 .LT. 1) GO TO 20
      DO 10 J = 1, KM1
      I = 2*(J-1) + 1
      T1 = A(J,K)
      T2 = A(J+1,K)
      C = Q(I)
      S = Q(I+1)
      A(J,K) = C*T1 - S*T2
      A(J+1,K) = S*T1 + C*T2
   10 CONTINUE
c
c           Compute Givens components c and s
c
   20 CONTINUE
      IQ = 2*KM1 + 1
      T1 = A(K,K)
      T2 = A(KP1,K)
      IF (T2 .NE. 0.0d0) GO TO 30
      C = 1.0d0
      S = 0.0d0
      GO TO 50
   30 CONTINUE
      IF (ABS(T2) .LT. ABS(T1)) GO TO 40
      T = T1/T2
      S = -1.0d0/SQRT(1.0d0+T*T)
      C = -S*T
      GO TO 50
   40 CONTINUE
      T = T2/T1
      C = 1.0d0/SQRT(1.0d0+T*T)
      S = -C*T
   50 CONTINUE
      Q(IQ) = C
      Q(IQ+1) = S
      A(K,K) = C*T1 - S*T2
      IF (A(K,K) .EQ. 0.0d0) INFO = K
   60 CONTINUE
      RETURN
c-----------------------------------------------------------------------
c The old factorization of A will be updated.  A row and a column
c have been added to the matrix A.
c N by N-1 is now the old size of the matrix.
c-----------------------------------------------------------------------
   70 CONTINUE
      NM1 = N - 1
c-----------------------------------------------------------------------
c Multiply the new column by the N previous Givens rotations.
c-----------------------------------------------------------------------
      DO 100 K = 1, NM1
      I = 2*(K-1) + 1
      T1 = A(K,N)
      T2 = A(K+1,N)
      C = Q(I)
      S = Q(I+1)
      A(K,N) = C*T1 - S*T2
      A(K+1,N) = S*T1 + C*T2
  100 CONTINUE
c-----------------------------------------------------------------------
c Complete update of decomposition by forming last Givens rotation,
c and multiplying it times the column vector (A(N,N),A(NP1,N)).
c-----------------------------------------------------------------------
      INFO = 0
      T1 = A(N,N)
      T2 = A(N+1,N)
      IF (T2 .NE. 0.0d0) GO TO 110
      C = 1.0d0
      S = 0.0d0
      GO TO 130
  110 CONTINUE
      IF (ABS(T2) .LT. ABS(T1)) GO TO 120
      T = T1/T2
      S = -1.0d0/SQRT(1.0d0+T*T)
      C = -S*T
      GO TO 130
  120 CONTINUE
      T = T2/T1
      C = 1.0d0/SQRT(1.0d0+T*T)
      S = -C*T
  130 CONTINUE
      IQ = 2*N - 1
      Q(IQ) = C
      Q(IQ+1) = S
      A(N,N) = C*T1 - S*T2
      IF (A(N,N) .EQ. 0.0d0) INFO = N
      RETURN
c----------------------- End of Subroutine SHEQR -----------------------
      END
      SUBROUTINE SHELS (A, LDA, N, Q, B)
      doubleprecision A, B, Q
      INTEGER LDA, N
      DIMENSION A(LDA, *), B(*), Q(*)
c-----------------------------------------------------------------------
c This is part of the LINPACK routine SGESL with changes
c due to the fact that  A  is an upper Hessenberg matrix.
c-----------------------------------------------------------------------
c     SHELS solves the least squares problem
c
c           min ( b - A*x , b - A*x )
c
c     using the factors computed by SHEQR.
c
c     On entry
c
c        A       Real array of dimension LDA by N
c                The output from SHEQR which contains the upper
c                triangular factor R in the QR decomposition of A.
c
c        LDA     integer
c                The leading dimension of the array  a .
c
c        N       integer
c                A is originally an (N+1) by N matrix.
c
c        Q       Real vector of dimension 2*N
c                The coefficients of the N Givens rotations
c                used in the QR factorization of A.
c
c        B       Real vector of dimension N+1
c                The right hand side vector.
c
c
c     On return
c
c        B       the solution vector  x .
c
c
c     Modification of LINPACK. This version dated 1/13/86.
c     Peter Brown, University of Houston, Lawrence Livermore Natl. Lab.
c     Revised, Aug. 9, 1989 to make dimension and real declarations
c     comply with ANSI standard. GDB
c     BLAS SAXPY
c-----------------------------------------------------------------------
c
c Type declarations for local variables --------------------------------
c
      doubleprecision C, S, T, T1, T2
      INTEGER IQ, K, KB, KP1
c
c        Minimize ( b - A*x , b - A*x )
c        First form Q*b.
c
      DO 20 K = 1, N
      KP1 = K + 1
      IQ = 2*(K-1) + 1
      C = Q(IQ)
      S = Q(IQ+1)
      T1 = B(K)
      T2 = B(KP1)
      B(K) = C*T1 - S*T2
      B(KP1) = S*T1 + C*T2
   20 CONTINUE
c
c        Now solve  R*x = Q*b.
c
      DO 40 KB = 1, N
      K = N + 1 - KB
      B(K) = B(K)/A(K,K)
      T = -B(K)
      CALL daxpy_u(K-1, T, A(1,K), 1, B(1), 1)
   40 CONTINUE
      RETURN
c----------------------- End of Subroutine SHELS -----------------------
      END
      SUBROUTINE SVRORTHOG (VNEW, V, HES , N, LL, LDHES, KMP, SNORMW)
      doubleprecision VNEW, V, HES , SNORMW
      INTEGER N, LL, LDHES, KMP
      DIMENSION VNEW(*), V(N, *), HES(LDHES, *)
c-----------------------------------------------------------------------
c This routine orthogonalizes the vector VNEW against the previous
c KMP vectors in the V array.  It uses a modified Gram-Schmidt
c orthogonalization procedure with conditional reorthogonalization.
c This is the version of 28 May 1986.
c-----------------------------------------------------------------------
c
c      On entry
c
c         VNEW = the vector of length N containing a scaled product
c                of the Jacobian and the vector V(*,LL).
c
c         V    = the N x LL array containing the previous LL
c                orthogonal vectors V(*,1) to V(*,ll).
c
c         HES  = an LL x LL upper Hessenberg matrix containing,
c                in HES(i,k), k.lt.ll, scaled inner products of
c                A*V(*,k) and V(*,i).
c
c        LDHES = the leading dimension of the HES array.
c
c         N    = the order of the matrix A, and the length of VNEW.
c
c         LL   = the current order of the matrix HES .
c
c          KMP = the number of previous vectors the new vector VNEW
c                must be made orthogonal to (KMP .le. MAXL).
c
c
c      On return
c
c         VNEW = the new vector orthogonal to V(*,I0) to V(*,LL),
c                where I0 = max(1, LL-KMP+1).
c
c         HES  = upper Hessenberg matrix with column LL filled in with
c                scaled inner products of A*V(*,ll) and V(*,i).
c
c      SNORNMW = l-2 norm of VNEW.
c
c-----------------------------------------------------------------------
c
c Type declarations for local variables --------------------------------
c
      doubleprecision ARG, SUMDSQ, TEM, VNRM
      INTEGER I, I0
c
c Type declaration for function subroutines called ---------------------
c
      doubleprecision ddot_u, dnrm2_u
c-----------------------------------------------------------------------
c Get norm of unaltered VNEW for later use. ----------------------------
      VNRM = dnrm2_u(N, VNEW, 1)
c-----------------------------------------------------------------------
c Do modified Gram-Schmidt on VNEW = A*V(ll).
c Scaled inner products give new column of HES .
c Projections of earlier vectors are subtracted from VNEW.
c-----------------------------------------------------------------------
      I0 = max(1,LL-KMP+1)
      DO 10 I = I0, LL
      HES (I,LL) = ddot_u(N, V(1,I), 1, VNEW, 1)
      TEM = - HES (I,LL)
      CALL daxpy_u(N, TEM, V(1,I), 1, VNEW, 1)
   10 CONTINUE
c-----------------------------------------------------------------------
c Compute SNORNMW = norm of VNEW.
c If VNEW is small compared to its input value (in norm), then
c reorthogonalize VNEW to V(*,1) through V(*,ll).
c correct if relative correction exceeds 1000*(unit roundoff).
c Finally, correct SNORNMW using the dot products involved.
c-----------------------------------------------------------------------
      SNORMW = dnrm2_u(N, VNEW, 1)
      IF (VNRM + 0.001d0*SNORMW .NE. VNRM) RETURN
      SUMDSQ = 0.0d0
      DO 30 I = I0, LL
      TEM = -ddot_u(N, V(1,I), 1, VNEW, 1)
      IF ( HES (I,LL) + 0.001d0*TEM .EQ. HES (I,LL)) GO TO 30
      HES (I,LL) = HES (I,LL) - TEM
      CALL daxpy_u(N, TEM, V(1,I), 1, VNEW, 1)
      SUMDSQ = SUMDSQ + TEM**2
   30 CONTINUE
      IF (SUMDSQ .EQ. 0.0d0) RETURN
      ARG = max(0.0d0,SNORMW**2 - SUMDSQ)
      SNORMW = SQRT(ARG)
c
      RETURN
c----------------------- End of Subroutine SVRORTHOG ----------------------
      END
      subroutine precond5(nn,ndiag,ndiagm,a,am,rowvec,colvec,id1,id2, 
     &   sigma,fmu,idiag)
cProlog
c
c   This subroutine builds the pre-conditioning matrix, am.
c   It is assumed that it has the same structure as the
c   Jacobian matrix and so it is stored in the same way, i.e.
c   by storing the non-zero diagonals as colums.
c
c    input variables
c
      integer nn, ndiag, ndiagm
      integer id1(0:ndiagm), id2(0:ndiagm), idiag(ndiagm)
      integer k, mdiag, iprcnd
      integer i, ii, j, m, irow, jcol, l, icnt1, icnt2
c
      doubleprecision a(nn,ndiag),am(0:nn,ndiagm), rowvec(0:nn),colvec(0
     &   :nn), sigma(nn), fmu(nn)
c
      doubleprecision tacc, parm, test
c
c ***************************************************
c
c   Find the column in A where the main diagonal is stored
c
      do 1 k=1,ndiag
    1    if (idiag(k).eq.0) mdiag=k
c
      iprcnd=0
      if (iprcnd.eq.1) then
c
c   Use the identity matrix as the pre-conditioner
c
         do 111 i=1,nn
            do 111 k=1,ndiag
  111          am(i,k) = 0.d0
c
         do 2 i=1,nn
    2       am(i,mdiag) = 1.d0
c
      else
c
c   This algorithm computes an approximate LU factorization of the
c   Jacobian matrix.  The algorithm assumes the resulting matrix
c   structure of (LU) is the same as the original Jacobian.
c
c   Initialize the pre-conditioning matrix and work vectors
c
         do 15 i=1,nn
            colvec(i) = 0.d0
            rowvec(i) = 0.d0
            do 5 k=1,ndiag
               am(i,k) = a(i,k)
    5          continue
            do 6 k=ndiag+1,ndiagm
               am(i,k) = 0.d0
    6          continue
   15       continue
c
c
         do 10 ii=1,nn
c
            sigma(ii) = 0.d0
            fmu(ii) = 0.d0
c
c=========================
c   Lower Diagonal Matrix
c=========================
c
            j = ii
c
c   Load the column vector for use in computing the recursive terms
c
            icnt2 = 0
            do 38 m=mdiag+1,ndiagm
c
               irow = j - idiag(m)
               if ((irow.ge.1).and.(irow.lt.j)) then
                  icnt2 = icnt2 + 1
                  colvec(irow) = am(irow,m)
                  id2(icnt2) = irow
               endif
c
   38          continue
c
c   Compute the jth column of L - first sweeping over the
c   original non-zero diagonals
c
            do 30 k=1,mdiag
c
               i = j - idiag(k)
c
               if (i.le.nn) then
c
c   Load the row vector for use in computing the recursive terms
c
c        original non-zero diagonals
c
                  icnt1 = 0
                  do 35 m=1,k-1
c
                     jcol = i + idiag(m)
                     if (jcol.ge.1) then
                        icnt1 = icnt1 + 1
                        rowvec(jcol) = am(i,m)
                        id1(icnt1) = jcol
                     endif
c
   35                continue
c
c        new non-zero diagonals resulting from ILU fill-in
c
                  do 36 m=ndiag+1,ndiagm
c
                     jcol = i + idiag(m)
                     if ((jcol.ge.1).and.(jcol.lt.i)) then
                        icnt1 = icnt1 + 1
                        rowvec(jcol) = am(i,m)
                        id1(icnt1) = jcol
                     endif
c
   36                continue
c
c   Compute the recursive terms in the ILU factorization
c
                  do 45 l=1,icnt1
c
                     am(i,k) = am(i,k) - rowvec(id1(l))*colvec(id1(l))
                     rowvec(id1(l)) = 0.d0
c
   45                continue
c
c   Compute sigma(i) to be used in testing for
c   unstable pivots
c
                  sigma(ii) = max(sigma(ii),abs(am(i,k)))
c
c
               endif
c
   30          continue
c
c   Now sweep over the non-zero diagonals generated from the
c   ILU fill-in
c
            do 32 k=ndiag+1,ndiagm
c
               i = j - idiag(k)
               if ((i.le.nn).and.(i.ge.j)) then
c
c   Load the row vector for use in computing the recursive terms
c
                  icnt1 = 0
                  do 55 m=1,ndiagm
c
                     jcol = i + idiag(m)
                     if ((jcol.ge.1).and.(jcol.lt.j)) then
                        icnt1 = icnt1 + 1
                        rowvec(jcol) = am(i,m)
                        id1(icnt1) = jcol
                     endif
c
   55                continue
c
c   Compute the recursive terms in the ILU factorization
c
                  do 65 l=1,icnt1
c
                     am(i,k) = am(i,k) - rowvec(id1(l))*colvec(id1(l))
                     rowvec(id1(l)) = 0.d0
c
   65                continue
c
c   Compute sigma(i) to be used in testing for
c   unstable pivots
c
                  sigma(ii) = max(sigma(ii),abs(am(i,k)))
c
c
               endif
c
   32          continue
c
c   Zero the remaining entries in the row and column work vectors
c
            do 41 l=1,icnt2
               colvec(id2(l)) = 0.d0
   41          continue
c
c
c=========================
c   Upper Diagonal Matrix
c=========================
c
            i = ii
c
c   Load the row vector for use in computing the recursive terms
c
c      original non-zero diagonals
c
            icnt1 = 0
            do 25 m=1,mdiag-1
c
               jcol = i + idiag(m)
               if (jcol.ge.1) then
                  icnt1 = icnt1 + 1
                  rowvec(jcol) = am(i,m)
                  id1(icnt1) = jcol
               endif
c
   25          continue
c
c      new non-zero diagonals generated from ILU fill-in
c
            do 26 m=ndiag+1,ndiagm
c
               jcol = i + idiag(m)
               if ((jcol.ge.1).and.(jcol.lt.i)) then
                  icnt1 = icnt1 + 1
                  rowvec(jcol) = am(i,m)
                  id1(icnt1) = jcol
               endif
c
   26          continue
c
c   Compute the ith row of U - original non-zero diagonals first
c
            do 20 k=mdiag+1,ndiag
c
               j = i + idiag(k)
c
               if (j.le.nn) then
c
c   Load the column vector for use in computing the recursive terms
c
                  icnt2 = 0
                  do 28 m=k+1,ndiagm
c
                     irow = j - idiag(m)
                     if ((irow.ge.1).and.(irow.lt.j)) then
                        icnt2 = icnt2 + 1
                        colvec(irow) = am(irow,m)
                        id2(icnt2) = irow
                     endif
c
   28                continue
c
c   Compute the recursive terms in the ILU factorization
c
                  do 29 l=1,icnt2
c
                     am(i,k) = am(i,k) - rowvec(id2(l))*colvec(id2(l))
                     colvec(id2(l)) = 0.d0
c
   29                continue
c
c   Compute fmu(i) to be used in testing for
c   unstable pivots
c
                  fmu(ii) = max(fmu(ii),abs(am(i,k)))
c
c
               endif
c
   20          continue
c
c   Now the new non-zero diagonals generated from the ILU fill-in
c
            do 21 k = ndiag+1,ndiagm
c
               j = i + idiag(k)
               if ((j.le.nn).and.(j.gt.i)) then
c
c   Load the column vector for use in computing the recursive terms
c
                  icnt2 = 0
                  do 88 m=1,ndiagm
c
                     irow = j - idiag(m)
                     if ((irow.ge.1).and.(irow.lt.j)) then
                        icnt2 = icnt2 + 1
                        colvec(irow) = am(irow,m)
                        id2(icnt2) = irow
                     endif
c
   88                continue
c
c   Compute the recursive terms in the ILU factorization
c
                  do 89 l=1,icnt2
c
                     am(i,k) = am(i,k) - rowvec(id2(l))*colvec(id2(l))
                     colvec(id2(l)) = 0.d0
c
   89                continue
c
c   Compute fmu(i) to be used in testing for
c   unstable pivots
c
                  fmu(ii) = max(fmu(ii),abs(am(i,k)))
c
c
               endif
c
   21          continue
c
c   Zero the remaining entries in the row and column work vectors
c
            do 31 l=1,icnt1
c
               rowvec(id1(l)) = 0.d0
c
   31          continue
c
c
c   Test for unstable pivots and adjust if necessary before
c   dividing through to obtain U
c
            tacc = 51
c       tacc = 21
            parm = 2.d0**(-tacc)
            test = parm*sigma(ii)*fmu(ii)
            if (am(ii,mdiag)**2.lt.test) then
c         write(*,*) 'pivot adjusted, row  = ',ii
c         write(*,*) '      before-   diag = ',am(ii,mdiag)
               am(ii,mdiag) = sign(1.d0,am(ii,mdiag))*sqrt(test)
c         write(*,*) '                test = ',test
c         write(*,*) '      after-    diag = ',am(ii,mdiag)
c         write(*,*) '                fmu  = ',fmu(ii)
c         write(*,*) '                sigma= ',sigma(ii)
            endif

            do 70 k=mdiag+1,ndiagm
               if (idiag(k).gt.0) then
                  if (am(ii,mdiag).eq.0.d0) then
                     write(*,*) 'zero diagonal in preconditioner'
                     stop
                  endif
                  am(ii,k) = am(ii,k)/am(ii,mdiag)
               endif
   70          continue
c
   10       continue
c
      endif
c
      return
      end
      subroutine minvmul(nn,ndiag,ndiagm,am,idiag,x,y)
cProlog
c
c   This subroutine solves, (LU)x = y for the vector x
c   where am is an approximate LU decomposition of
c   the Jacobian matrix
c
c   The integer array idiag contains the information
c   that relates the actual column to the main diagonal
c   since only the non-zero diagonals of A are stored, i.e.,
c
c     i = row number
c     j = column number = i + idiag(k)
c     k = non-zero diagonal index numbered from left to right
c
      implicit none
c
c    input variables
c
      integer nn, ndiag, ndiagm, k, mdiag, i, jcol
c
      doubleprecision am(0:nn,ndiagm), x(nn), y(nn), sum
      integer idiag(ndiagm)
c
c
c ***************************************************
c
c   Find column in am(i,j) where main diagonal is located
c
      do 10 k=1,ndiag
   10    if (idiag(k).eq.0) mdiag=k
c
c   Compute the b' vector which is the solution to L(b')=y
c
      x(1) = y(1)/am(1,mdiag)
c
      do 20 i = 2,nn
c
         sum = 0.d0
c
         do 30 k=1,mdiag-1
c
            jcol = i + idiag(k)
            if (jcol.ge.1) sum = sum + am(i,k)*x(jcol)
c
   30       continue
c
         do 35 k = ndiag+1,ndiagm
c
            jcol = i + idiag(k)
            if ((idiag(k).lt.0).and.(jcol.ge.1)) then
               sum = sum + am(i,k)*x(jcol)
            endif
c
   35       continue
c
         x(i) = (y(i) - sum)/am(i,mdiag)
c
   20    continue
c
c   Now compute x which is the solution to Ux = b'
c
      do 50 i=nn-1,1,-1
c
         sum = 0.d0
c
         do 60 k=mdiag+1,ndiag
c
            jcol = i + idiag(k)
            if (jcol.le.nn) sum = sum + am(i,k)*x(jcol)
c
   60       continue
c
         do 65 k = ndiag+1,ndiagm
c
            jcol = i + idiag(k)
            if ((idiag(k).gt.0).and.(jcol.le.nn)) then
               sum = sum + am(i,k)*x(jcol)
            endif
c
   65       continue
c
         x(i) = x(i) - sum
c
   50    continue
c
c
      return
      end
c  end of minvmul
c-----------------------------------------------------------------------
      subroutine cdiagsrt (n,adiag,ndiag,ioff,iwork1,iwork2,rwork)
cProlog
      integer n, ndiag, iwork1(2*n-1), iwork2(ndiag), ioff(ndiag)
      doubleprecision adiag(n,ndiag), rwork(ndiag)
c-----------------------------------------------------------------------
c This routine sorts the elements of a matrix (stored in Diagonal
c Format) in increasing order of their column indices within
c each row.
c-----------------------------------------------------------------------
c on entry:
c---------
c n      = the row dimension of the matrix
c adiag  = the matrix A in diagonal format.
c ndiag  = the number of non-zero diagonals in A
c ioff   = integer array of length idiag, containing the offsets of the
c          diagonals
c iwork1 = integer work array of length 2*n-1.
c iwork2 = integer work array of length ndiag.
c rwork  = real work array of length ndiag.
c
c on return:
c----------
c the matrix stored in the structure adiag is permuted in such a
c way that the column indices are in increasing order within each row.
c iwork2(1:ndiag) contains the permutation used to rearrange the
c elements.
c-----------------------------------------------------------------------
c P. Brown 3-19-93.
c-----------------------------------------------------------------------
c local variables
      integer i, k
c
c calculate permutation.
c
      do 10 i = 1,ndiag
         iwork1(n+ioff(i)) = i
   10    continue
c delete zero entries from iwork1.
      k = 1
      do 20 i = 1,2*n-1
         if (iwork1(i) .ne. 0) then
            iwork1(k) = iwork1(i)
            k = k + 1
         endif
   20    continue
c calculate inverse permutation of that in iwork1.
      do 25 i = 1,ndiag
         iwork2(iwork1(i)) = i
   25    continue
c perform an in-place permutation of the arrays ioff and adiag.
      call ivperm (ndiag, ioff, iwork2)
      do 50 k = 1,n
         do 30 i = 1,ndiag
            rwork(i) = adiag(k,i)
   30       continue
         call dvperm (ndiag, rwork, iwork2)
         do 40 i = 1,ndiag
            adiag(k,i) = rwork(i)
   40       continue
   50    continue
c
      return
c---------------end-of-cdiagsrt-----------------------------------------
c-----------------------------------------------------------------------
      end
