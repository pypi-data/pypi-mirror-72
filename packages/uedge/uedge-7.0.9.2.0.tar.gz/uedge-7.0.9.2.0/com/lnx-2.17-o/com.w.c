/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(com_handler, COM_HANDLER)
#else
void FF_ID(com_handler, COM_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* glbwrlog */
        void *A1 = cfcnarg[1];  /* ioun */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 1: {     /* xerrab */
        char *A1 = *(char **) cfcnarg[1];  /* msg */
        int L2 = *(Integer *) cfcnarg[2];  /* len of msg */
        func(A1, L2);
        break;
        }
    case 2: {     /* readne_dat */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 3: {     /* readte_dat */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 4: {     /* readti_dat */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 5: {     /* fit_neteti */
        func();
        break;
        }
    case 6: {     /* tanh_multi */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* a */
        void *A3 = cfcnarg[3];  /* j */
        void *A4 = cfcnarg[4];  /* b */
        char *A5 = *(char **) cfcnarg[5];  /* fname */
        int L6 = *(Integer *) cfcnarg[6];  /* len of fname */
        void *A7 = cfcnarg[7];  /* d */
        func(A1, A2, A3, A4, A5, A7, L6);
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
