/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(api_handler, API_HANDLER)
#else
void FF_ID(api_handler, API_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* getatau */
        void *A1 = cfcnarg[1];  /* nx */
        void *A2 = cfcnarg[2];  /* ny */
        void *A3 = cfcnarg[3];  /* uu */
        void *A4 = cfcnarg[4];  /* gx */
        void *A5 = cfcnarg[5];  /* ixpt1 */
        void *A6 = cfcnarg[6];  /* ixpt2 */
        void *A7 = cfcnarg[7];  /* iysptrx */
        void *A8 = cfcnarg[8];  /* atau */
        void *A9 = cfcnarg[9];  /* tau1 */
        void *A10 = cfcnarg[10];  /* tau2 */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10);
        break;
        }
    case 1: {     /* getprad */
        void *A1 = cfcnarg[1];  /* nx */
        void *A2 = cfcnarg[2];  /* ny */
        void *A3 = cfcnarg[3];  /* ngsp */
        void *A4 = cfcnarg[4];  /* te */
        void *A5 = cfcnarg[5];  /* ne */
        void *A6 = cfcnarg[6];  /* ng */
        void *A7 = cfcnarg[7];  /* afrac */
        void *A8 = cfcnarg[8];  /* atau */
        void *A9 = cfcnarg[9];  /* prad */
        void *A10 = cfcnarg[10];  /* na */
        void *A11 = cfcnarg[11];  /* ntau */
        void *A12 = cfcnarg[12];  /* nratio */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12);
        break;
        }
    case 2: {     /* readmc */
        void *A1 = cfcnarg[1];  /* nzdf */
        char *A2 = *(char **) cfcnarg[2];  /* mcfilename */
        int L3 = *(Integer *) cfcnarg[3];  /* len of mcfilename */
        func(A1, A2, L3);
        break;
        }
    case 3: {     /* mcrates */
        void *A1 = cfcnarg[1];  /* ne */
        void *A2 = cfcnarg[2];  /* te */
        void *A3 = cfcnarg[3];  /* ti */
        void *A4 = cfcnarg[4];  /* za */
        void *A5 = cfcnarg[5];  /* zamax */
        void *A6 = cfcnarg[6];  /* zn */
        void *A7 = cfcnarg[7];  /* rion */
        void *A8 = cfcnarg[8];  /* rrec */
        void *A9 = cfcnarg[9];  /* rcxr */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9);
        break;
        }
    case 4: {     /* radmc */
        void *A1 = cfcnarg[1];  /* nz */
        void *A2 = cfcnarg[2];  /* znuc */
        void *A3 = cfcnarg[3];  /* te */
        void *A4 = cfcnarg[4];  /* dene */
        void *A5 = cfcnarg[5];  /* denz */
        void *A6 = cfcnarg[6];  /* radz */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3, A4, A5, A6);
        break;
        }
    case 5: {     /* rcxr_zn6 */
        void *A1 = cfcnarg[1];  /* tmp */
        void *A2 = cfcnarg[2];  /* za */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2);
        break;
        }
    case 6: {     /* readpost */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 7: {     /* splinem */
        func();
        break;
        }
    case 8: {     /* emissbs */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* nratio */
        void *A3 = cfcnarg[3];  /* ntau */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 9: {     /* z1avgbs */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* nratio */
        void *A3 = cfcnarg[3];  /* ntau */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 10: {     /* z2avgbs */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* nratio */
        void *A3 = cfcnarg[3];  /* ntau */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 11: {     /* syld96 */
        void *A1 = cfcnarg[1];  /* matt */
        void *A2 = cfcnarg[2];  /* matp */
        void *A3 = cfcnarg[3];  /* cion */
        void *A4 = cfcnarg[4];  /* cizb */
        void *A5 = cfcnarg[5];  /* crmb */
        func(A1, A2, A3, A4, A5);
        break;
        }
    case 12: {     /* yld96 */
        void *A1 = cfcnarg[1];  /* matt */
        void *A2 = cfcnarg[2];  /* matp */
        void *A3 = cfcnarg[3];  /* energy */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 13: {     /* sputchem */
        void *A1 = cfcnarg[1];  /* ioptchem */
        void *A2 = cfcnarg[2];  /* ee0 */
        void *A3 = cfcnarg[3];  /* temp */
        void *A4 = cfcnarg[4];  /* flux */
        void *A5 = cfcnarg[5];  /* ychem */
        func(A1, A2, A3, A4, A5);
        break;
        }
    case 14: {     /* readrates */
        char *A1 = *(char **) cfcnarg[1];  /* apidir */
        int L2 = *(Integer *) cfcnarg[2];  /* len of apidir */
        char *A3 = *(char **) cfcnarg[3];  /* impfname */
        int L4 = *(Integer *) cfcnarg[4];  /* len of impfname */
        func(A1, A3, L2, L4);
        break;
        }
    case 15: {     /* calcrates */
        void *A1 = cfcnarg[1];  /* ne */
        void *A2 = cfcnarg[2];  /* te */
        void *A3 = cfcnarg[3];  /* density */
        func(A1, A2, A3);
        break;
        }
    case 16: {     /* lineintegral */
        void *A1 = cfcnarg[1];  /* arg */
        void *A2 = cfcnarg[2];  /* rvertex */
        void *A3 = cfcnarg[3];  /* zvertex */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
