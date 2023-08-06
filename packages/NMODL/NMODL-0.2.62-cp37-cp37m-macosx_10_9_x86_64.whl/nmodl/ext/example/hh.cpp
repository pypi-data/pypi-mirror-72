/* Created by Language version: 6.2.0 */
/* NOT VECTORIZED */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#undef PI
 
#include "coreneuron/utils/randoms/nrnran123.h"
#include "coreneuron/nrnoc/md1redef.h"
#include "coreneuron/nrnconf.h"
#include "coreneuron/sim/multicore.hpp"
#include "coreneuron/nrniv/nrniv_decl.h"
#include "coreneuron/utils/ivocvect.hpp"
#include "coreneuron/utils/nrnoc_aux.hpp"
#include "coreneuron/gpu/nrn_acc_manager.hpp"
#include "coreneuron/mechanism/mech/cfile/scoplib.h"

#include "coreneuron/sim/scopmath/newton_struct.h"
#include "coreneuron/nrnoc/md2redef.h"
#include "coreneuron/mechanism/register_mech.hpp"
#include "_kinderiv.h"
#if !NRNGPU
#if !defined(DISABLE_HOC_EXP)
#undef exp
#define exp hoc_Exp
#endif
#endif
 namespace coreneuron {
 
#undef LAYOUT
#define LAYOUT 1
#define _STRIDE 1
 
#define nrn_init _nrn_init__hh
#define nrn_cur _nrn_cur__hh
#define _nrn_current _nrn_current__hh
#define nrn_jacob _nrn_jacob__hh
#define nrn_state _nrn_state__hh
#define initmodel initmodel__hh
#define _net_receive _net_receive__hh
#define _net_init _net_init__hh
#define nrn_state_launcher nrn_state_hh_launcher
#define nrn_cur_launcher nrn_cur_hh_launcher
#define nrn_jacob_launcher nrn_jacob_hh_launcher 
#define rates rates_hh 
#define states states_hh 
 
#undef _threadargscomma_
#undef _threadargsprotocomma_
#undef _threadargs_
#undef _threadargsproto_
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gnabar _p[0*_STRIDE]
#define gkbar _p[1*_STRIDE]
#define gl _p[2*_STRIDE]
#define el _p[3*_STRIDE]
#define gna _p[4*_STRIDE]
#define gk _p[5*_STRIDE]
#define il _p[6*_STRIDE]
#define minf _p[7*_STRIDE]
#define hinf _p[8*_STRIDE]
#define ninf _p[9*_STRIDE]
#define mtau _p[10*_STRIDE]
#define htau _p[11*_STRIDE]
#define ntau _p[12*_STRIDE]
#define m _p[13*_STRIDE]
#define h _p[14*_STRIDE]
#define n _p[15*_STRIDE]
#define Dm _p[16*_STRIDE]
#define Dh _p[17*_STRIDE]
#define Dn _p[18*_STRIDE]
#define ena _p[19*_STRIDE]
#define ek _p[20*_STRIDE]
#define ina _p[21*_STRIDE]
#define ik _p[22*_STRIDE]
#define _g _p[23*_STRIDE]
#define _ion_ena		_nt_data[_ppvar[0*_STRIDE]]
#define _ion_ina	_nt_data[_ppvar[1*_STRIDE]]
#define _ion_dinadv	_nt_data[_ppvar[2*_STRIDE]]
#define _ion_ek		_nt_data[_ppvar[3*_STRIDE]]
#define _ion_ik	_nt_data[_ppvar[4*_STRIDE]]
#define _ion_dikdv	_nt_data[_ppvar[5*_STRIDE]]
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 extern double celsius;
 #define _celsius_ _celsius__hh
double _celsius_;
#pragma acc declare copyin(_celsius_)
 
#if 0 /*BBCORE*/
 /* declaration of user functions */
 static void _hoc_rates(void);
 static void _hoc_vtrap(void);
 
#endif /*BBCORE*/
 static int _mechtype;
 
#if 0 /*BBCORE*/
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_hh", _hoc_setdata,
 "rates_hh", _hoc_rates,
 "vtrap_hh", _hoc_vtrap,
 0, 0
};
 
#endif /*BBCORE*/
#define vtrap vtrap_hh
 #pragma acc routine seq
 inline double vtrap( double , double );
 /* declare global and static user variables */
#define zz zz_hh
 double zz = 0;
 #pragma acc declare copyin (zz)
 
static void _acc_globals_update() {
 #pragma acc update device (zz) if(nrn_threads->compute_gpu)
 _celsius_ = celsius;
 #pragma acc update device(_celsius_)
 }

 #define celsius _celsius_
 
#if 0 /*BBCORE*/
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "gl_hh", 0, 1e+09,
 "gkbar_hh", 0, 1e+09,
 "gnabar_hh", 0, 1e+09,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gnabar_hh", "S/cm2",
 "gkbar_hh", "S/cm2",
 "gl_hh", "S/cm2",
 "el_hh", "mV",
 "gna_hh", "S/cm2",
 "gk_hh", "S/cm2",
 "il_hh", "mA/cm2",
 "mtau_hh", "ms",
 "htau_hh", "ms",
 "ntau_hh", "ms",
 0,0
};
 
#endif /*BBCORE*/
 static double delta_t = 0.01;
#pragma acc declare copyin(delta_t)
 static double h0 = 0;
#pragma acc declare copyin(h0)
 static double m0 = 0;
#pragma acc declare copyin(m0)
 static double n0 = 0;
#pragma acc declare copyin(n0)
 static double v = 0;
#pragma acc declare copyin(v)
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "zz_hh", &zz_hh,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(double*, Datum*, int);
void nrn_init(NrnThread*, Memb_list*, int);
void nrn_state(NrnThread*, Memb_list*, int);
 void nrn_cur(NrnThread*, Memb_list*, int);
 void nrn_jacob(NrnThread*, Memb_list*, int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "6.2.0",
"hh",
 "gnabar_hh",
 "gkbar_hh",
 "gl_hh",
 "el_hh",
 0,
 "gna_hh",
 "gk_hh",
 "il_hh",
 "minf_hh",
 "hinf_hh",
 "ninf_hh",
 "mtau_hh",
 "htau_hh",
 "ntau_hh",
 0,
 "m_hh",
 "h_hh",
 "n_hh",
 0,
 0};
 static int _na_type;
 static int _k_type;
 
static void nrn_alloc(double* _p, Datum* _ppvar, int _type) {
 
#if 0 /*BBCORE*/
 	/*initialize range parameters*/
 	gnabar = 0.12;
 	gkbar = 0.036;
 	gl = 0.0003;
 	el = -54.3;
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
#endif /* BBCORE */
 
}
 static void _initlists();
 static void _update_ion_pointer(Datum*);
 
#define _psize 24
#define _ppsize 6
 void _hh_reg() {
	int _vectorized = 0;
  _initlists();
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 if (_mechtype == -1) return;
 _nrn_layout_reg(_mechtype, LAYOUT);
 _na_type = nrn_get_mechtype("na_ion"); _k_type = nrn_get_mechtype("k_ion"); 
#if 0 /*BBCORE*/
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 
#endif /*BBCORE*/
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
  hoc_register_prop_size(_mechtype, _psize, _ppsize);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
 	hoc_register_var(hoc_scdoub, hoc_vdoub, NULL);
 }
 static double _zyy ;
static int _reset;
static const char *modelname = "hh.mod squid sodium, potassium, and leak channels";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static inline int rates(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 
#define _slist1 _slist1_hh
int* _slist1;
#pragma acc declare create(_slist1)

#define _dlist1 _dlist1_hh
int* _dlist1;
#pragma acc declare create(_dlist1)
 static inline int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
   Dm = ( minf - m ) / mtau ;
   Dh = ( hinf - h ) / htau ;
   Dn = ( ninf - n ) / ntau ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / mtau )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / htau )) ;
 Dn = Dn  / (1. - dt*( ( ( ( - 1.0 ) ) ) / ntau )) ;
 return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / mtau)))*(- ( ( ( minf ) ) / mtau ) / ( ( ( ( - 1.0) ) ) / mtau ) - m) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / htau)))*(- ( ( ( hinf ) ) / htau ) / ( ( ( ( - 1.0) ) ) / htau ) - h) ;
    n = n + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / ntau)))*(- ( ( ( ninf ) ) / ntau ) / ( ( ( ( - 1.0) ) ) / ntau ) - n) ;
   }
  return 0;
}
 
static int  rates (  double _lv ) {
   double _lalpha , _lbeta , _lsum , _lq10 ;
  _lq10 = pow( 3.0 , ( ( celsius - 6.3 ) / 10.0 ) ) ;
   _lalpha = .1 * vtrap ( _threadargscomma_ - ( _lv + 40.0 ) , 10.0 ) ;
   _lbeta = 4.0 * exp ( - ( _lv + 65.0 ) / 18.0 ) ;
   _lsum = _lalpha + _lbeta ;
   mtau = 1.0 / ( _lq10 * _lsum ) ;
   minf = _lalpha / _lsum ;
   _lalpha = .07 * exp ( - ( _lv + 65.0 ) / 20.0 ) ;
   _lbeta = 1.0 / ( exp ( - ( _lv + 35.0 ) / 10.0 ) + 1.0 ) ;
   _lsum = _lalpha + _lbeta ;
   htau = 1.0 / ( _lq10 * _lsum ) ;
   hinf = _lalpha / _lsum ;
   _lalpha = .01 * vtrap ( _threadargscomma_ - ( _lv + 55.0 ) , 10.0 ) ;
   _lbeta = .125 * exp ( - ( _lv + 65.0 ) / 80.0 ) ;
   _lsum = _lalpha + _lbeta ;
   ntau = 1.0 / ( _lq10 * _lsum ) ;
   ninf = _lalpha / _lsum ;
   zz = 1.0 ;
    return 0; }
 
#if 0 /*BBCORE*/
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) ;
 hoc_retpushx(_r);
}
 
#endif /*BBCORE*/
 
double vtrap (  double _lx , double _ly ) {
   double _lvtrap;
 if ( fabs ( _lx / _ly ) < 1e-6 ) {
     _lvtrap = _ly * ( 1.0 - _lx / _ly / 2.0 ) ;
     }
   else {
     _lvtrap = _lx / ( exp ( _lx / _ly ) - 1.0 ) ;
     }
   
return _lvtrap;
 }
 
#if 0 /*BBCORE*/
 
static void _hoc_vtrap(void) {
  double _r;
   _r =  vtrap (  *getarg(1) , *getarg(2) ;
 hoc_retpushx(_r);
}
 
#endif /*BBCORE*/
 static void _update_ion_pointer(Datum* _ppvar) {
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
  n = n0;
 {
   rates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
   n = ninf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(NrnThread* _nt, Memb_list* _ml, int _type){
double _v; int* _ni; int _iml, _cntml_padded, _cntml_actual;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
    _v = _vec_v[_nd_idx];
    _PRCELLSTATE_V
 v = _v;
  ena = _ion_ena;
  ek = _ion_ek;
 initmodel();
  }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   gna = gnabar * m * m * m * h ;
   ina = gna * ( v - ena ) ;
   gk = gkbar * n * n * n * n ;
   ik = gk * ( v - ek ) ;
   il = gl * ( v - el ) ;
   }
 _current += ina;
 _current += ik;
 _current += il;

} return _current;
}

static void nrn_cur(NrnThread* _nt, Memb_list* _ml, int _type){
int* _ni; double _rhs, _v; int _iml, _cntml_padded, _cntml_actual;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
    _v = _vec_v[_nd_idx];
    _PRCELLSTATE_V
  ena = _ion_ena;
  ek = _ion_ek;
 _g = _nrn_current(_v + .001);
 	{ double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
  _ion_ik += ik ;
	VEC_RHS(_ni[_iml]) -= _rhs;
 
}}

static void nrn_jacob(NrnThread* _nt, Memb_list* _ml, int _type){
int* _ni; int _iml, _cntml_padded, _cntml_actual;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize;
	VEC_D(_ni[_iml]) += _g;
 
}}

static void nrn_state(NrnThread* _nt, Memb_list* _ml, int _type){
double _v = 0.0; int* _ni; int _iml, _cntml_padded, _cntml_actual;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
    _v = _vec_v[_nd_idx];
    _PRCELLSTATE_V
 v=_v;
 _PRCELLSTATE_V
{
  ena = _ion_ena;
  ek = _ion_ek;
 { error =  states();
 if(error){fprintf(stderr,"at line 62 in file nmodl/ext/example/hh.mod:\n    SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 }  }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
 int _cntml_actual=1;
 int _cntml_padded=1;
 int _iml=0;
  if (!_first) return;
 
 _slist1 = (int*)malloc(sizeof(int)*3);
 _dlist1 = (int*)malloc(sizeof(int)*3);
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
 _slist1[1] = &(h) - _p;  _dlist1[1] = &(Dh) - _p;
 _slist1[2] = &(n) - _p;  _dlist1[2] = &(Dn) - _p;
 #pragma acc enter data copyin(_slist1[0:3])
 #pragma acc enter data copyin(_dlist1[0:3])

_first = 0;
}
 } // namespace coreneuron
