/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(flx_handler, FLX_HANDLER)
#else
void FF_ID(flx_handler, FLX_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* rho1 */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* r1 */
        void *A8 = cfcnarg[8];  /* r2 */
        void *A9 = cfcnarg[9];  /* r3 */
        void *A10 = cfcnarg[10];  /* alf */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10);
        break;
        }
    case 1: {     /* rho1dn */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* t4 */
        void *A8 = cfcnarg[8];  /* r1 */
        void *A9 = cfcnarg[9];  /* r2 */
        void *A10 = cfcnarg[10];  /* r3 */
        void *A11 = cfcnarg[11];  /* r4 */
        void *A12 = cfcnarg[12];  /* alf */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12);
        break;
        }
    case 2: {     /* rho2dn */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* t4 */
        void *A8 = cfcnarg[8];  /* r1 */
        void *A9 = cfcnarg[9];  /* r2 */
        void *A10 = cfcnarg[10];  /* r3 */
        void *A11 = cfcnarg[11];  /* r4 */
        void *A12 = cfcnarg[12];  /* fac */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12);
        break;
        }
    case 3: {     /* rho3dn */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* t4 */
        void *A8 = cfcnarg[8];  /* r1 */
        void *A9 = cfcnarg[9];  /* r2 */
        void *A10 = cfcnarg[10];  /* r3 */
        void *A11 = cfcnarg[11];  /* r4 */
        void *A12 = cfcnarg[12];  /* slp2fac */
        void *A13 = cfcnarg[13];  /* slp3fac */
        void *A14 = cfcnarg[14];  /* r2p */
        void *A15 = cfcnarg[15];  /* r3p */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15);
        break;
        }
    case 4: {     /* rho1l */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* r1 */
        void *A7 = cfcnarg[7];  /* r2 */
        void *A8 = cfcnarg[8];  /* r1p */
        func(A1, A2, A3, A4, A5, A6, A7, A8);
        break;
        }
    case 5: {     /* rho1r */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* r1 */
        void *A7 = cfcnarg[7];  /* r2 */
        void *A8 = cfcnarg[8];  /* r2p */
        func(A1, A2, A3, A4, A5, A6, A7, A8);
        break;
        }
    case 6: {     /* rho2 */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* r1 */
        void *A8 = cfcnarg[8];  /* r2 */
        void *A9 = cfcnarg[9];  /* r3 */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9);
        break;
        }
    case 7: {     /* rho3 */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* r1 */
        void *A8 = cfcnarg[8];  /* r2 */
        void *A9 = cfcnarg[9];  /* r3 */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9);
        break;
        }
    case 8: {     /* rho4 */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* r1 */
        void *A8 = cfcnarg[8];  /* r2 */
        void *A9 = cfcnarg[9];  /* r3 */
        void *A10 = cfcnarg[10];  /* s2 */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10);
        break;
        }
    case 9: {     /* rho5 */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* rho */
        void *A3 = cfcnarg[3];  /* nt */
        void *A4 = cfcnarg[4];  /* t1 */
        void *A5 = cfcnarg[5];  /* t2 */
        void *A6 = cfcnarg[6];  /* t3 */
        void *A7 = cfcnarg[7];  /* r1 */
        void *A8 = cfcnarg[8];  /* r2 */
        void *A9 = cfcnarg[9];  /* r3 */
        void *A10 = cfcnarg[10];  /* r2p */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10);
        break;
        }
    case 10: {     /* aeqdsk */
        func();
        break;
        }
    case 11: {     /* neqdsk */
        func();
        break;
        }
    case 12: {     /* readefit */
        func();
        break;
        }
    case 13: {     /* procefit */
        func();
        break;
        }
    case 14: {     /* refine */
        func();
        break;
        }
    case 15: {     /* contours */
        void *A1 = cfcnarg[1];  /* ns */
        func(A1);
        break;
        }
    case 16: {     /* flxrun */
        func();
        break;
        }
    case 17: {     /* flxfin */
        func();
        break;
        }
    case 18: {     /* inflx */
        func();
        break;
        }
    case 19: {     /* theta_ok */
        void *A1 = cfcnarg[1];  /* r */
        void *A2 = cfcnarg[2];  /* z */
        void *A3 = cfcnarg[3];  /* n */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, A2, A3);
        break;
        }
    case 20: {     /* efitvers */
        void *A1 = cfcnarg[1];  /* vmonth */
        void *A2 = cfcnarg[2];  /* vday */
        void *A3 = cfcnarg[3];  /* vyear */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, A2, A3);
        break;
        }
    case 21: {     /* findstrike */
        void *A1 = cfcnarg[1];  /* js */
        void *A2 = cfcnarg[2];  /* rs */
        void *A3 = cfcnarg[3];  /* zs */
        func(A1, A2, A3);
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
