/* Character variables come in as bare address + length. */
#include <Fcc.h>

#include <basis-c-defs.h>
/*--------------------------------------------------------------------------*/
#ifdef __cplusplus
extern "C" void FF_ID(bbb_handler, BBB_HANDLER)
#else
void FF_ID(bbb_handler, BBB_HANDLER)
#endif
    (Integer *index, void (*func)(), void *result,
    void **cfcnarg, integer *result_len)
{
    switch (*index) {
    case 0: {     /* exmain */
        func();
        break;
        }
    case 1: {     /* exmain_prelims */
        func();
        break;
        }
    case 2: {     /* uedriv */
        func();
        break;
        }
    case 3: {     /* convert */
        func();
        break;
        }
    case 4: {     /* convsr_vo */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j */
        void *A3 = cfcnarg[3];  /* yl */
        func(A1, A2, A3);
        break;
        }
    case 5: {     /* convsr_aux */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j */
        func(A1, A2);
        break;
        }
    case 6: {     /* pandf */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j */
        void *A3 = cfcnarg[3];  /* neq */
        void *A4 = cfcnarg[4];  /* t */
        void *A5 = cfcnarg[5];  /* yl */
        void *A6 = cfcnarg[6];  /* yldot */
        func(A1, A2, A3, A4, A5, A6);
        break;
        }
    case 7: {     /* pandf1 */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j */
        void *A3 = cfcnarg[3];  /* ieq */
        void *A4 = cfcnarg[4];  /* neq */
        void *A5 = cfcnarg[5];  /* t */
        void *A6 = cfcnarg[6];  /* yl */
        void *A7 = cfcnarg[7];  /* yldot */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 8: {     /* bouncon */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* yl */
        void *A3 = cfcnarg[3];  /* yldot */
        func(A1, A2, A3);
        break;
        }
    case 9: {     /* poteneq */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* a */
        void *A3 = cfcnarg[3];  /* b */
        func(A1, A2, A3);
        break;
        }
    case 10: {     /* ffun */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* t */
        void *A3 = cfcnarg[3];  /* yl */
        void *A4 = cfcnarg[4];  /* yldot */
        func(A1, A2, A3, A4);
        break;
        }
    case 11: {     /* resid */
        void *A1 = cfcnarg[1];  /* t */
        void *A2 = cfcnarg[2];  /* y */
        void *A3 = cfcnarg[3];  /* yp */
        void *A4 = cfcnarg[4];  /* delta */
        void *A5 = cfcnarg[5];  /* ires */
        void *A6 = cfcnarg[6];  /* rp */
        void *A7 = cfcnarg[7];  /* ip */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 12: {     /* ueinit */
        func();
        break;
        }
    case 13: {     /* set_var_norm */
        void *A1 = cfcnarg[1];  /* job */
        void *A2 = cfcnarg[2];  /* neq */
        void *A3 = cfcnarg[3];  /* nvars */
        void *A4 = cfcnarg[4];  /* yl */
        void *A5 = cfcnarg[5];  /* norm_cons */
        void *A6 = cfcnarg[6];  /* floor_cons */
        void *A7 = cfcnarg[7];  /* su */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 14: {     /* gridseq */
        func();
        break;
        }
    case 15: {     /* nphygeo */
        func();
        break;
        }
    case 16: {     /* jacnw */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* yl */
        void *A3 = cfcnarg[3];  /* f0 */
        void *A4 = cfcnarg[4];  /* dt */
        void *A5 = cfcnarg[5];  /* wk */
        void *A6 = cfcnarg[6];  /* wp */
        void *A7 = cfcnarg[7];  /* iwp */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 17: {     /* psolnw */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* yl */
        void *A3 = cfcnarg[3];  /* wk */
        void *A4 = cfcnarg[4];  /* wp */
        void *A5 = cfcnarg[5];  /* iwp */
        void *A6 = cfcnarg[6];  /* bl */
        void *A7 = cfcnarg[7];  /* ierr */
        func(A1, A2, A3, A4, A5, A6, A7);
        break;
        }
    case 18: {     /* psolbody */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* using */
        void *A3 = cfcnarg[3];  /* suscal */
        void *A4 = cfcnarg[4];  /* wk */
        void *A5 = cfcnarg[5];  /* wp */
        void *A6 = cfcnarg[6];  /* iwp */
        void *A7 = cfcnarg[7];  /* bl */
        void *A8 = cfcnarg[8];  /* ierr */
        func(A1, A2, A3, A4, A5, A6, A7, A8);
        break;
        }
    case 19: {     /* csrcsc */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* job */
        void *A3 = cfcnarg[3];  /* ipos */
        void *A4 = cfcnarg[4];  /* rcsc */
        void *A5 = cfcnarg[5];  /* icsc */
        void *A6 = cfcnarg[6];  /* jcsc */
        void *A7 = cfcnarg[7];  /* jac */
        void *A8 = cfcnarg[8];  /* jacj */
        void *A9 = cfcnarg[9];  /* jaci */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9);
        break;
        }
    case 20: {     /* allocate */
        func();
        break;
        }
    case 21: {     /* walsor */
        func();
        break;
        }
    case 22: {     /* volsor */
        func();
        break;
        }
    case 23: {     /* write_profs */
        func();
        break;
        }
    case 24: {     /* read_profs */
        func();
        break;
        }
    case 25: {     /* write_profs_boris */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 26: {     /* read_profs_boris */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        void *A3 = cfcnarg[3];  /* ierr */
        func(A1, A3, L2);
        break;
        }
    case 27: {     /* quadsvr */
        void *A1 = cfcnarg[1];  /* neq */
        void *A2 = cfcnarg[2];  /* a */
        void *A3 = cfcnarg[3];  /* b */
        void *A4 = cfcnarg[4];  /* c */
        void *A5 = cfcnarg[5];  /* d */
        void *A6 = cfcnarg[6];  /* yl */
        void *A7 = cfcnarg[7];  /* yldot */
        void *A8 = cfcnarg[8];  /* ylprev */
        void *A9 = cfcnarg[9];  /* ylchng */
        void *A10 = cfcnarg[10];  /* sfscal */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10);
        break;
        }
    case 28: {     /* aplsb */
        void *A1 = cfcnarg[1];  /* nrow */
        void *A2 = cfcnarg[2];  /* ncol */
        void *A3 = cfcnarg[3];  /* a */
        void *A4 = cfcnarg[4];  /* ja */
        void *A5 = cfcnarg[5];  /* ia */
        void *A6 = cfcnarg[6];  /* s */
        void *A7 = cfcnarg[7];  /* b */
        void *A8 = cfcnarg[8];  /* jb */
        void *A9 = cfcnarg[9];  /* ib */
        void *A10 = cfcnarg[10];  /* c */
        void *A11 = cfcnarg[11];  /* jc */
        void *A12 = cfcnarg[12];  /* ic */
        void *A13 = cfcnarg[13];  /* nzmax */
        void *A14 = cfcnarg[14];  /* iw */
        void *A15 = cfcnarg[15];  /* ierr */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15);
        break;
        }
    case 29: {     /* jacmap */
        func();
        break;
        }
    case 30: {     /* map_var_jac1d */
        func();
        break;
        }
    case 31: {     /* jacstnlout */
        func();
        break;
        }
    case 32: {     /* jacout */
        func();
        break;
        }
    case 33: {     /* radintp */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j */
        void *A3 = cfcnarg[3];  /* k */
        void *A4 = cfcnarg[4];  /* l */
        void *A5 = cfcnarg[5];  /* m */
        void *A6 = cfcnarg[6];  /* n */
        void *A7 = cfcnarg[7];  /* ii */
        void *A8 = cfcnarg[8];  /* jj */
        void *A9 = cfcnarg[9];  /* kk */
        void *A10 = cfcnarg[10];  /* ll */
        void *A11 = cfcnarg[11];  /* a */
        void *A12 = cfcnarg[12];  /* b */
        void *A13 = cfcnarg[13];  /* c */
        void *A14 = cfcnarg[14];  /* d */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14);
        break;
        }
    case 34: {     /* polintp */
        void *A1 = cfcnarg[1];  /* i */
        void *A2 = cfcnarg[2];  /* j */
        void *A3 = cfcnarg[3];  /* k */
        void *A4 = cfcnarg[4];  /* l */
        void *A5 = cfcnarg[5];  /* m */
        void *A6 = cfcnarg[6];  /* n */
        void *A7 = cfcnarg[7];  /* ii */
        void *A8 = cfcnarg[8];  /* jj */
        void *A9 = cfcnarg[9];  /* kk */
        void *A10 = cfcnarg[10];  /* ll */
        void *A11 = cfcnarg[11];  /* a */
        void *A12 = cfcnarg[12];  /* b */
        void *A13 = cfcnarg[13];  /* c */
        void *A14 = cfcnarg[14];  /* d */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14);
        break;
        }
    case 35: {     /* intpvar */
        void *A1 = cfcnarg[1];  /* a */
        void *A2 = cfcnarg[2];  /* b */
        void *A3 = cfcnarg[3];  /* i */
        void *A4 = cfcnarg[4];  /* j */
        void *A5 = cfcnarg[5];  /* k */
        func(A1, A2, A3, A4, A5);
        break;
        }
    case 36: {     /* engbal */
        void *A1 = cfcnarg[1];  /* a */
        func(A1);
        break;
        }
    case 37: {     /* pradpltwl */
        func();
        break;
        }
    case 38: {     /* ebindz */
        void *A1 = cfcnarg[1];  /* za */
        void *A2 = cfcnarg[2];  /* zn */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2);
        break;
        }
    case 39: {     /* wtottim */
        func();
        break;
        }
    case 40: {     /* rundt */
        func();
        break;
        }
    case 41: {     /* domain_dc */
        func();
        break;
        }
    case 42: {     /* map_var_jac */
        func();
        break;
        }
    case 43: {     /* bbb2wdf */
        func();
        break;
        }
    case 44: {     /* write30 */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 45: {     /* write31 */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 46: {     /* write_eirene */
        func();
        break;
        }
    case 47: {     /* read32 */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 48: {     /* read44 */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 49: {     /* writemcnfile */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        char *A3 = *(char **) cfcnarg[3];  /* runid */
        int L4 = *(Integer *) cfcnarg[4];  /* len of runid */
        func(A1, A3, L2, L4);
        break;
        }
    case 50: {     /* readmcntest */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 51: {     /* readmcnsor */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 52: {     /* readmcndens */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        func(A1, L2);
        break;
        }
    case 53: {     /* readmcnoutput */
        char *A1 = *(char **) cfcnarg[1];  /* fname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of fname */
        void *A3 = cfcnarg[3];  /* skip */
        void *A4 = cfcnarg[4];  /* var */
        void *A5 = cfcnarg[5];  /* rsd */
        func(A1, A3, A4, A5, L2);
        break;
        }
    case 54: {     /* readmcnmoments */
        char *A1 = *(char **) cfcnarg[1];  /* dname */
        int L2 = *(Integer *) cfcnarg[2];  /* len of dname */
        func(A1, L2);
        break;
        }
    case 55: {     /* lmode_roots */
        void *A1 = cfcnarg[1];  /* bcoef */
        void *A2 = cfcnarg[2];  /* ccoef */
        void *A3 = cfcnarg[3];  /* omega */
        func(A1, A2, A3);
        break;
        }
    case 56: {     /* lmode_chi_norm */
        void *A1 = cfcnarg[1];  /* kappabar */
        void *A2 = cfcnarg[2];  /* lte */
        void *A3 = cfcnarg[3];  /* rhos */
        void *A4 = cfcnarg[4];  /* cubrtnu */
        void *A5 = cfcnarg[5];  /* ti0 */
        void *A6 = cfcnarg[6];  /* ted */
        void *A7 = cfcnarg[7];  /* zavg */
        void *A8 = cfcnarg[8];  /* lpi */
        void *A9 = cfcnarg[9];  /* lambdap */
        void *A10 = cfcnarg[10];  /* maxmag */
        void *A11 = cfcnarg[11];  /* nky */
        void *A12 = cfcnarg[12];  /* kybeg */
        void *A13 = cfcnarg[13];  /* kyend */
        void *A14 = cfcnarg[14];  /* kya */
        void *A15 = cfcnarg[15];  /* kyb */
        void *A16 = cfcnarg[16];  /* tol */
        void *A17 = cfcnarg[17];  /* iprint */
        void *A18 = cfcnarg[18];  /* islmodebeta */
        void *A19 = cfcnarg[19];  /* kt */
        void *A20 = cfcnarg[20];  /* lmodechin */
        void *A21 = cfcnarg[21];  /* gammamax */
        void *A22 = cfcnarg[22];  /* kymax */
        func(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17, A18, A19, A20, A21, A22);
        break;
        }
    case 57: {     /* hmode_chi_norm */
        void *A1 = cfcnarg[1];  /* gradvconst */
        void *A2 = cfcnarg[2];  /* cubrtnu */
        void *A3 = cfcnarg[3];  /* epsilon */
        void *A4 = cfcnarg[4];  /* lambdap */
        void *A5 = cfcnarg[5];  /* hmodechin */
        func(A1, A2, A3, A4, A5);
        break;
        }
    case 58: {     /* turb_chi */
        void *A1 = cfcnarg[1];  /* lmodechin */
        void *A2 = cfcnarg[2];  /* hmodechin */
        void *A3 = cfcnarg[3];  /* rhos */
        void *A4 = cfcnarg[4];  /* csed */
        void *A5 = cfcnarg[5];  /* lte */
        void *A6 = cfcnarg[6];  /* lambdap */
        void *A7 = cfcnarg[7];  /* cubrtnu */
        void *A8 = cfcnarg[8];  /* chi */
        func(A1, A2, A3, A4, A5, A6, A7, A8);
        break;
        }
    case 59: {     /* read_zag */
        func();
        break;
        }
    case 60: {     /* kappa */
        void *A1 = cfcnarg[1];  /* fqpsati */
        void *A2 = cfcnarg[2];  /* fqpsate */
        void *A3 = cfcnarg[3];  /* fqp */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1, A2, A3);
        break;
        }
    case 61: {     /* mombal */
        void *A1 = cfcnarg[1];  /* ix */
        void *A2 = cfcnarg[2];  /* ix1 */
        void *A3 = cfcnarg[3];  /* iy */
        func(A1, A2, A3);
        break;
        }
    case 62: {     /* mombalni */
        void *A1 = cfcnarg[1];  /* ix */
        void *A2 = cfcnarg[2];  /* ix1 */
        void *A3 = cfcnarg[3];  /* iy */
        func(A1, A2, A3);
        break;
        }
    case 63: {     /* fitdata2svar */
        func();
        break;
        }
    case 64: {     /* onedconteq */
        func();
        break;
        }
    case 65: {     /* fit_neteti */
        func();
        break;
        }
    case 66: {     /* ru_active */
        void *A1 = cfcnarg[1];  /* amumass */
        void *A2 = cfcnarg[2];  /* znucleus */
        void *A3 = cfcnarg[3];  /* charge */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, A2, A3);
        break;
        }
    case 67: {     /* upvisneo */
        func();
        break;
        }
    case 68: {     /* jvisneo */
        func();
        break;
        }
    case 69: {     /* init_neutrals */
        func();
        break;
        }
    case 70: {     /* init_degas2 */
        func();
        break;
        }
    case 71: {     /* init_eirene */
        func();
        break;
        }
    case 72: {     /* run_neutrals */
        func();
        break;
        }
    case 73: {     /* run_uedge */
        func();
        break;
        }
    case 74: {     /* run_degas2 */
        func();
        break;
        }
    case 75: {     /* run_eirene */
        func();
        break;
        }
    case 76: {     /* convertmcnsor */
        func();
        break;
        }
    case 77: {     /* uedge_plasma */
        func();
        break;
        }
    case 78: {     /* uedge_neutrals */
        func();
        break;
        }
    case 79: {     /* uedge_uedge */
        func();
        break;
        }
    case 80: {     /* uedge_degas2 */
        func();
        break;
        }
    case 81: {     /* run_pnc */
        func();
        break;
        }
    case 82: {     /* uedge_save_pdb */
        char *A1 = *(char **) cfcnarg[1];  /* filename */
        int L2 = *(Integer *) cfcnarg[2];  /* len of filename */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, L2);
        break;
        }
    case 83: {     /* uedge_save */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0();
        break;
        }
    case 84: {     /* uedge_read_pdb */
        char *A1 = *(char **) cfcnarg[1];  /* filename */
        int L2 = *(Integer *) cfcnarg[2];  /* len of filename */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, L2);
        break;
        }
    case 85: {     /* uedge_read */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0();
        break;
        }
    case 86: {     /* mcnsor_save_pdb */
        char *A1 = *(char **) cfcnarg[1];  /* filename */
        int L2 = *(Integer *) cfcnarg[2];  /* len of filename */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, L2);
        break;
        }
    case 87: {     /* mcnsor_append_pdb */
        char *A1 = *(char **) cfcnarg[1];  /* filename */
        int L2 = *(Integer *) cfcnarg[2];  /* len of filename */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, L2);
        break;
        }
    case 88: {     /* pnc_save_pdb */
        char *A1 = *(char **) cfcnarg[1];  /* filename */
        int L2 = *(Integer *) cfcnarg[2];  /* len of filename */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, L2);
        break;
        }
    case 89: {     /* get_fnrm */
        void *A1 = cfcnarg[1];  /* dtreal_try */
        real8 (*func0)() = (real8 (*)()) func;
        * (real8 *) result = func0(A1);
        break;
        }
    case 90: {     /* test_opt */
        char *A1 = *(char **) cfcnarg[1];  /* optarg */
        int L2 = *(Integer *) cfcnarg[2];  /* len of optarg */
        func(A1, L2);
        break;
        }
    case 91: {     /* test_parser */
        char *A1 = *(char **) cfcnarg[1];  /* optarg */
        int L2 = *(Integer *) cfcnarg[2];  /* len of optarg */
        func(A1, L2);
        break;
        }
    case 92: {     /* interpmcnvec */
        void *A1 = cfcnarg[1];  /* mcvar */
        void *A2 = cfcnarg[2];  /* uevar */
        void *A3 = cfcnarg[3];  /* mcvar_rsd */
        void *A4 = cfcnarg[4];  /* uevar_rsd */
        func(A1, A2, A3, A4);
        break;
        }
    case 93: {     /* convertmcnvec */
        void *A1 = cfcnarg[1];  /* mcvar */
        void *A2 = cfcnarg[2];  /* uevar */
        void *A3 = cfcnarg[3];  /* mcvar_rsd */
        void *A4 = cfcnarg[4];  /* uevar_rsd */
        void *A5 = cfcnarg[5];  /* sgn */
        func(A1, A2, A3, A4, A5);
        break;
        }
    case 94: {     /* convertmcnvector */
        void *A1 = cfcnarg[1];  /* mcvar */
        void *A2 = cfcnarg[2];  /* uevar */
        void *A3 = cfcnarg[3];  /* mcvar_rsd */
        void *A4 = cfcnarg[4];  /* uevar_rsd */
        func(A1, A2, A3, A4);
        break;
        }
    case 95: {     /* convertmcntensor */
        void *A1 = cfcnarg[1];  /* mcvar */
        void *A2 = cfcnarg[2];  /* uevar */
        void *A3 = cfcnarg[3];  /* mcvar_rsd */
        void *A4 = cfcnarg[4];  /* uevar_rsd */
        func(A1, A2, A3, A4);
        break;
        }
    case 96: {     /* convertmcnmoments */
        func();
        break;
        }
    case 97: {     /* mcndivide */
        void *A1 = cfcnarg[1];  /* out */
        void *A2 = cfcnarg[2];  /* var */
        void *A3 = cfcnarg[3];  /* dens */
        void *A4 = cfcnarg[4];  /* out_rsd */
        void *A5 = cfcnarg[5];  /* var_rsd */
        void *A6 = cfcnarg[6];  /* dens_rsd */
        func(A1, A2, A3, A4, A5, A6);
        break;
        }
    case 98: {     /* mcuedivide */
        void *A1 = cfcnarg[1];  /* out */
        void *A2 = cfcnarg[2];  /* var */
        void *A3 = cfcnarg[3];  /* dens */
        void *A4 = cfcnarg[4];  /* out_rsd */
        void *A5 = cfcnarg[5];  /* var_rsd */
        void *A6 = cfcnarg[6];  /* dens_rsd */
        func(A1, A2, A3, A4, A5, A6);
        break;
        }
    case 99: {     /* mcnrsdfix */
        void *A1 = cfcnarg[1];  /* mcrsd */
        func(A1);
        break;
        }
    case 100: {     /* mcnblend */
        void *A1 = cfcnarg[1];  /* out */
        void *A2 = cfcnarg[2];  /* uevar */
        void *A3 = cfcnarg[3];  /* mcvar */
        void *A4 = cfcnarg[4];  /* out_rsd */
        void *A5 = cfcnarg[5];  /* mcrsd */
        void *A6 = cfcnarg[6];  /* alpha */
        func(A1, A2, A3, A4, A5, A6);
        break;
        }
    case 101: {     /* mult23 */
        void *A1 = cfcnarg[1];  /* var2 */
        void *A2 = cfcnarg[2];  /* var3 */
        void *A3 = cfcnarg[3];  /* n3 */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, A2, A3);
        break;
        }
    case 102: {     /* mult24 */
        void *A1 = cfcnarg[1];  /* var2 */
        void *A2 = cfcnarg[2];  /* var4 */
        void *A3 = cfcnarg[3];  /* n3 */
        void *A4 = cfcnarg[4];  /* n4 */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, A2, A3, A4);
        break;
        }
    case 103: {     /* mult34 */
        void *A1 = cfcnarg[1];  /* var2 */
        void *A2 = cfcnarg[2];  /* var4 */
        void *A3 = cfcnarg[3];  /* n3 */
        void *A4 = cfcnarg[4];  /* n4 */
        integer (*func0)() = (integer (*)()) func;
        * (integer *) result = func0(A1, A2, A3, A4);
        break;
        }
    case 104: {     /* wallflux */
        func();
        break;
        }
    case 105: {     /* plateflux */
        func();
        break;
        }
    case 106: {     /* setLogFile */
        char *A1 = *(char **) cfcnarg[1];  /* filename */
        int L2 = *(Integer *) cfcnarg[2];  /* len of filename */
        func(A1, L2);
        break;
        }
    case 107: {     /* writeToLog */
        char *A1 = *(char **) cfcnarg[1];  /* message */
        int L2 = *(Integer *) cfcnarg[2];  /* len of message */
        func(A1, L2);
        break;
        }
/*    default: */

    }
    return;
}
/*--------------------------------------------------------------------------*/
