/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(aph_handler, APH_HANDLER)
#else
void FF_ID(aph_handler, APH_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* rsa */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* ne */
        void *A3 = cfcnarg[3];  /* r */
        void *A4 = cfcnarg[4];  /* k */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3, A4);
        break;
        }
    case 1: {     /* rra */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* ne */
        void *A3 = cfcnarg[3];  /* r */
        void *A4 = cfcnarg[4];  /* k */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3, A4);
        break;
        }
    case 2: {     /* rcx */
        void *A1 = cfcnarg[1];  /* t0 */
        void *A2 = cfcnarg[2];  /* n0 */
        void *A3 = cfcnarg[3];  /* k */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 3: {     /* rqa */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* ne */
        void *A3 = cfcnarg[3];  /* k */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 4: {     /* erl1 */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* ne */
        void *A3 = cfcnarg[3];  /* r */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 5: {     /* erl2 */
        void *A1 = cfcnarg[1];  /* te */
        void *A2 = cfcnarg[2];  /* ne */
        void *A3 = cfcnarg[3];  /* r */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 6: {     /* svdiss */
        void *A1 = cfcnarg[1];  /* te */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 7: {     /* readrt */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 8: {     /* readeh */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 9: {     /* readnw */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 10: {     /* readehr1 */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 11: {     /* readehr2 */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 12: {     /* aphread */
        func();
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
