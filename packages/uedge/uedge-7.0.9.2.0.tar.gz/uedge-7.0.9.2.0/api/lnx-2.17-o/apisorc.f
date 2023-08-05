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
c     ./../apisorc.m
c
c BASIS-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c



c
c XUEDGE-M-DEFS.D - configured MPPL language defines
c                - This file is generated - do not edit
c




















































































c!include "api.h"
      subroutine imp_sorc_walls (nxd, nzsptd, xcwi, xcwo, syi, syo, 
     &   ixp1i, ixp1o, fnzysi, fnzyso)
cProlog

c ... Calculate impurity-source profiles along the inner and outer walls
c     for a number of impurity sources.

      implicit none

c ... Input arguments:
c number of physical cells along wall
      integer nxd
c total number of impurity species
      integer nzsptd
c poloidal index of cell physically adjacent
      integer ixp1i(0:nxd+1)
c to right face of cells along inner wall
c poloidal index of cell physically adjacent
      integer ixp1o(0:nxd+1)
c to right face of cells along outer wall
c x-coord. of cell center on inner wall
      doubleprecision xcwi(0:nxd+1)
c x-coord. of cell center on outer wall
      doubleprecision xcwo(0:nxd+1)
c surface areas of inner-wall cells
      doubleprecision syi(0:nxd+1)
c surface areas of outer-wall cells
      doubleprecision syo(0:nxd+1)

c ... Output arguments:
c source profiles along inner wall
      doubleprecision fnzysi(0:nxd+1,nzsptd)
c source profiles along outer wall
      doubleprecision fnzyso(0:nxd+1,nzsptd)

c ... Common block:
c Group Dim
      integer nx, ny, nxm, nym, nxpt, nhsp, nzsp(1:6-1), nzspt
      integer nzspmx, nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      integer num_elem
      common /com20/ nx, ny, nxm, nym, nxpt, nhsp, nzsp, nzspt, nzspmx
      common /com20/ nisp, nusp, nfsp, ngsp, nhgsp, imx, imy, lnst
      common /com20/ num_elem
c End of Dim
c nxpt
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
c ixlb,ixrb
c Group Sources_at_walls
      integer nzsor

      integer iszsorlb ( nzspt,nzsor)
      pointer(piszsorlb,iszsorlb)

      integer jxzsori ( nzspt,nzsor)
      pointer(pjxzsori,jxzsori)

      integer jxzsoro ( nzspt,nzsor)
      pointer(pjxzsoro,jxzsoro)

      integer ixzbegi ( nzspt,nzsor)
      pointer(pixzbegi,ixzbegi)

      integer ixzendi ( nzspt,nzsor)
      pointer(pixzendi,ixzendi)

      integer ixzbego ( nzspt,nzsor)
      pointer(pixzbego,ixzbego)

      integer ixzendo ( nzspt,nzsor)
      pointer(pixzendo,ixzendo)

      double precision ximpi ( nzspt,nzsor)
      pointer(pximpi,ximpi)

      double precision ximpo ( nzspt,nzsor)
      pointer(pximpo,ximpo)

      double precision wimpi ( nzspt,nzsor)
      pointer(pwimpi,wimpi)

      double precision wimpo ( nzspt,nzsor)
      pointer(pwimpo,wimpo)

      double precision impsori ( nzspt,nzsor)
      pointer(pimpsori,impsori)

      double precision impsoro ( nzspt,nzsor)
      pointer(pimpsoro,impsoro)
      common /api60/ nzsor
      common /api66/ piszsorlb, pjxzsori, pjxzsoro
      common /api66/ pixzbegi, pixzendi, pixzbego
      common /api66/ pixzendo, pximpi, pximpo
      common /api66/ pwimpi, pwimpo, pimpsori
      common /api66/ pimpsoro
c End of Sources_at_walls
c nzsor,iszsorlb,ximpi,ximpo,wimpi,wimpo,
c impsori,impsoro
c jxzsori,jxzsoro
c ixzbegi,ixbego,ixzendi,ixzendo

c ... Local variables:
      integer iz, ix, isor, jxlbi, jxrbi, jxlbo, jxrbo

c ... Check that array limits are not exceeded.
      if (nzsor .gt. 10) call xerrab( 
     &      '*** nzsor > NZSORMX; enlarge impurity-source arrays.')

c ... Zero output arrays.
      do 23000 iz = 1, nzsptd
         do 23002 ix = 0, nxd+1
            fnzysi(ix,iz) = 0.d0
            fnzyso(ix,iz) = 0.d0
23002    continue
23000 continue

c ... Find the beginning and ending ix-indices for each wall
      do 23004 isor = 1, nzsor
         do 23006 iz = 1, nzsptd
            jxlbo = jxzsoro(iz,isor)
c     On the outboard wall, sources begin and end in the same mesh region:
            jxrbo = jxlbo
            ixzbego(iz,isor) = ixlb(jxlbo)
            ixzendo(iz,isor) = ixrb(jxrbo)+1

            jxlbi = jxzsori(iz,isor)
c     On private flux walls, sources may begin and end in different mesh regions
c     if nxpt > 1 as in a full double-null configuration.
            if (jxlbi.eq.1) then
               jxrbi = nxpt
            else
               jxrbi = jxlbi - 1
            endif
            ixzbegi(iz,isor) = ixlb(jxlbi)
            ixzendi(iz,isor) = ixrb(jxrbi)+1
23006    continue
23004 continue

c ... Loop over impurity sources, doing the outer and inner walls.
      do 23008 isor = 1, nzsor
         call imp_sorc (nxd, nzsptd, iszsorlb(1,isor), ixzbego(1,isor), 
     &      ixzendo(1,isor), ixp1o, ximpo(1,isor), wimpo(1,isor), 
     &      impsoro(1,isor), xcwo, syo, fnzyso)
         call imp_sorc (nxd, nzsptd, iszsorlb(1,isor), ixzbegi(1,isor), 
     &      ixzendi(1,isor), ixp1i, ximpi(1,isor), wimpi(1,isor), 
     &      impsori(1,isor), xcwi, syi, fnzysi)
23008 continue

      return
      end
c----------------------------------------------------------------------c
      subroutine imp_sorc (nx, nzspt, iszsorlb, ixbeg, ixend, ixplus1, 
     &   ximp, wimp, impsor, xgrd, sy, fnzys)
cProlog

c ... Calculate impurity-source profiles along a single wall for a set
c     of impurities.

      implicit none

c ... Input arguments:
c number of physical cells along wall
      integer nx
c number of impurity species
      integer nzspt
c =1 if origin for ximp is at left bndry
      integer iszsorlb(nzspt)
c beginning ix-index for wall
      integer ixbeg(nzspt)
c ending ix-index for wall
      integer ixend(nzspt)
c poloidal index of cell physically adjacent
      integer ixplus1(0:nx+1)
c to right face
c centers of impurity-source profiles
      doubleprecision ximp(nzspt)
c widths of impurity-source profiles
      doubleprecision wimp(nzspt)
c impurity source strengths (Amps)
      doubleprecision impsor(nzspt)
c cell locations
      doubleprecision xgrd(0:nx+1)
c surface areas of cells
      doubleprecision sy(0:nx+1)

c ... In-out argument:
      doubleprecision fnzys(0:nx+1,nzspt)

c ... Common block:
c Group Physical_constants2
      double precision ev2, qe2
      common /api13/ ev2, qe2
c End of Physical_constants2
c qe2

c ... Local variables:
      integer iz, ix
      doubleprecision pi, sycos, xnot, arg

      pi = 3.14159265358979323d0

c ... Begin loop over impurity species.
      do 23000 iz = 1, nzspt

c ... Initialize normalization factor and center of profile
         sycos = 0.d0
         xnot = iszsorlb(iz)*ximp(iz) + (1-iszsorlb(iz))*(xgrd(ixend(iz)
     &      )-ximp(iz))

c ... Calculate normalization factor
         ix = ixbeg(iz)
23002    continue
            arg = (xgrd(ix) - xnot) * pi / (wimp(iz) + 1.d-20)
            if (abs(arg) .lt. pi/2.d0) sycos = sycos + cos(arg) * sy(ix)
            if (ix.eq.ixend(iz)) go to 23003
            ix = ixplus1(ix)
c -- repeat
         go to 23002
23003    continue

c ... Add impurity-source profile to any previous contributions.
         ix = ixbeg(iz)
23004    continue
            arg = (xgrd(ix) - xnot) * pi / (wimp(iz) + 1.d-20)
            if (abs(arg) .lt. pi/2.d0 .and. sycos .gt. 0.d0) then
               fnzys(ix,iz) = fnzys(ix,iz) + impsor(iz) * cos(arg) * sy(
     &            ix) / (sycos * qe2)
            endif
            if (ix.eq.ixend(iz)) go to 23005
            ix = ixplus1(ix)
c -- repeat
         go to 23004
23005    continue

c ... End loop over impurity species.
23000 continue

      return
      end
