/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(svr_handler, SVR_HANDLER)
#else
void FF_ID(svr_handler, SVR_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* xnewuoa */
        void *A1 = cfcnarg[1];  /* n */
        void *A2 = cfcnarg[2];  /* npt */
        void *A3 = cfcnarg[3];  /* x */
        void *A4 = cfcnarg[4];  /* rhobeg */
        void *A5 = cfcnarg[5];  /* rhoend */
        void *A6 = cfcnarg[6];  /* maxfun */
        void *A7 = cfcnarg[7];  /* iprint */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
