/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(grd_handler, GRD_HANDLER)
#else
void FF_ID(grd_handler, GRD_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* xfcn */
        void *A1 = cfcnarg[1];  /* t */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 1: {     /* xfcn2 */
        void *A1 = cfcnarg[1];  /* t */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 2: {     /* xfcn3 */
        void *A1 = cfcnarg[1];  /* t */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 3: {     /* xfcn4 */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* nxtotal */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2);
        break;
        }
    case 4: {     /* xcscoef */
        func();
        break;
        }
    case 5: {     /* setidim */
        func();
        break;
        }
    case 6: {     /* grdrun */
        func();
        break;
        }
    case 7: {     /* ingrd */
        func();
        break;
        }
    case 8: {     /* codsys */
        void *A1 = cfcnarg[1];  /* j */
        void *A2 = cfcnarg[2];  /* icood */
        void *A3 = cfcnarg[3];  /* iseg */
        void *A4 = cfcnarg[4];  /* is */
        void *A5 = cfcnarg[5];  /* dy */
        void *A6 = cfcnarg[6];  /* region */
        void *A7 = cfcnarg[7];  /* alpha1 */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 9: {     /* findalph */
        void *A1 = cfcnarg[1];  /* nsys */
        void *A2 = cfcnarg[2];  /* iseg */
        void *A3 = cfcnarg[3];  /* j */
        void *A4 = cfcnarg[4];  /* xob */
        void *A5 = cfcnarg[5];  /* yob */
        void *A6 = cfcnarg[6];  /* alphab */
        func(A1, A2, A3, A4, A5, A6);
        break;
        }
    case 10: {     /* readflx */
        func();
        break;
        }
    case 11: {     /* prune */
        func();
        break;
        }
    case 12: {     /* extend */
        func();
        break;
        }
    case 13: {     /* splfit */
        func();
        break;
        }
    case 14: {     /* sow */
        func();
        break;
        }
    case 15: {     /* meshgen */
        void *A1 = cfcnarg[1];  /* region */
        func(A1);
        break;
        }
    case 16: {     /* orthogx */
        void *A1 = cfcnarg[1];  /* ixtyp */
        void *A2 = cfcnarg[2];  /* i */
        void *A3 = cfcnarg[3];  /* j0 */
        void *A4 = cfcnarg[4];  /* j */
        void *A5 = cfcnarg[5];  /* xob */
        void *A6 = cfcnarg[6];  /* yob */
        void *A7 = cfcnarg[7];  /* alphab */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 17: {     /* orthogrd */
        void *A1 = cfcnarg[1];  /* ixtyp */
        void *A2 = cfcnarg[2];  /* i */
        void *A3 = cfcnarg[3];  /* j0 */
        void *A4 = cfcnarg[4];  /* j */
        void *A5 = cfcnarg[5];  /* xob */
        void *A6 = cfcnarg[6];  /* yob */
        void *A7 = cfcnarg[7];  /* alphab */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 18: {     /* readgrid */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 19: {     /* writesn */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 20: {     /* writedn */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 21: {     /* writedata */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 22: {     /* writednf */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 23: {     /* intersect2 */
        void *A1 = cfcnarg[1];  /* x1 */
        void *A2 = cfcnarg[2];  /* y1 */
        void *A3 = cfcnarg[3];  /* i1min */
        void *A4 = cfcnarg[4];  /* i1max */
        void *A5 = cfcnarg[5];  /* x2 */
        void *A6 = cfcnarg[6];  /* y2 */
        void *A7 = cfcnarg[7];  /* i2min */
        void *A8 = cfcnarg[8];  /* i2max */
        void *A9 = cfcnarg[9];  /* xc */
        void *A10 = cfcnarg[10];  /* yc */
        void *A11 = cfcnarg[11];  /* i1c */
        void *A12 = cfcnarg[12];  /* i2c */
        void *A13 = cfcnarg[13];  /* fuzz */
        void *A14 = cfcnarg[14];  /* ierr */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14);
        break;
        }
    case 24: {     /* meshmod2 */
        void *A1 = cfcnarg[1];  /* region */
        func(A1);
        break;
        }
    case 25: {     /* smooth */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j1 */
        void *A3 = cfcnarg[3];  /* j2 */
        func(A1, A2, A3);
        break;
        }
    case 26: {     /* writeue */
        func();
        break;
        }
    case 27: {     /* grd2wdf */
        func();
        break;
        }
    case 28: {     /* evalspln */
        void *A1 = cfcnarg[1];  /* iseg */
        void *A2 = cfcnarg[2];  /* j */
        void *A3 = cfcnarg[3];  /* xo */
        void *A4 = cfcnarg[4];  /* yo */
        func(A1, A2, A3, A4);
        break;
        }
    case 29: {     /* idealgrd */
        func();
        break;
        }
    case 30: {     /* mirrorgrd */
        func();
        break;
        }
    case 31: {     /* gett */
        func();
        break;
        }
    case 32: {     /* getu */
        func();
        break;
        }
    case 33: {     /* getd */
        func();
        break;
        }
    case 34: {     /* getp */
        func();
        break;
        }
    case 35: {     /* meshmod3 */
        void *A1 = cfcnarg[1];  /* region */
        func(A1);
        break;
        }
    case 36: {     /* smoother */
        func();
        break;
        }
    case 37: {     /* smoother2 */
        func();
        break;
        }
    case 38: {     /* meshff */
        void *A1 = cfcnarg[1];  /* region */
        func(A1);
        break;
        }
    case 39: {     /* fpoloidal */
        void *A1 = cfcnarg[1];  /* psi */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 40: {     /* pressure */
        void *A1 = cfcnarg[1];  /* psi */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 41: {     /* psif */
        void *A1 = cfcnarg[1];  /* r */
        void *A2 = cfcnarg[2];  /* z */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2);
        break;
        }
    case 42: {     /* brf */
        void *A1 = cfcnarg[1];  /* r */
        void *A2 = cfcnarg[2];  /* z */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2);
        break;
        }
    case 43: {     /* bzf */
        void *A1 = cfcnarg[1];  /* r */
        void *A2 = cfcnarg[2];  /* z */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2);
        break;
        }
    case 44: {     /* rsurface */
        void *A1 = cfcnarg[1];  /* quadrant */
        func(A1);
        break;
        }
    case 45: {     /* fluxcurve */
        void *A1 = cfcnarg[1];  /* quadrant */
        void *A2 = cfcnarg[2];  /* iy */
        func(A1, A2);
        break;
        }
    case 46: {     /* refinexm */
        func();
        break;
        }
    case 47: {     /* refine_xpt */
        func();
        break;
        }
    case 48: {     /* smoothx */
        void *A1 = cfcnarg[1];  /* rmm */
        void *A2 = cfcnarg[2];  /* zmm */
        void *A3 = cfcnarg[3];  /* nd1 */
        void *A4 = cfcnarg[4];  /* nd2 */
        void *A5 = cfcnarg[5];  /* iy1 */
        void *A6 = cfcnarg[6];  /* iy2 */
        void *A7 = cfcnarg[7];  /* quadrant */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 49: {     /* mapdnbot */
        func();
        break;
        }
    case 50: {     /* mapdntop */
        func();
        break;
        }
    case 51: {     /* magnetics */
        void *A1 = cfcnarg[1];  /* ixmin */
        void *A2 = cfcnarg[2];  /* ixmax */
        void *A3 = cfcnarg[3];  /* iymin */
        void *A4 = cfcnarg[4];  /* iymax */
        func(A1, A2, A3, A4);
        break;
        }
    case 52: {     /* add_guardc_tp */
        func();
        break;
        }
    case 53: {     /* exponseed */
        func();
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
