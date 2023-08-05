/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(wdf_handler, WDF_HANDLER)
#else
void FF_ID(wdf_handler, WDF_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* write_degas */
        func();
        break;
        }
    case 1: {     /* write_namelist */
        func();
        break;
        }
    case 2: {     /* frrate */
        func();
        break;
        }
    case 3: {     /* ueplasma */
        func();
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
