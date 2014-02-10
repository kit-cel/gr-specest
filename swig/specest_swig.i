/* -*- c++ -*- */

#define SPECEST_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "specest_swig_doc.i"

%{
#include "specest/reciprocal_ff.h"
#include "specest/pad_vector.h"
#include "specest/stream_to_vector_overlap.h"
#include "specest/moving_average_vff.h"
#include "specest/adaptiveweighting_vff.h"
//#include "specest/arfcov_vcc.h"
//#include "specest/fcov.h"
#include "specest/arfmcov_vcc.h"
#include "specest/fmcov.h"
#include "specest/arburg_vcc.h"
#include "specest/burg.h"
#include "specest/welch.h"
%}


%include "specest/reciprocal_ff.h"
GR_SWIG_BLOCK_MAGIC2(specest, reciprocal_ff);
%include "specest/pad_vector.h"
GR_SWIG_BLOCK_MAGIC2(specest, pad_vector);
%include "specest/stream_to_vector_overlap.h"
GR_SWIG_BLOCK_MAGIC2(specest, stream_to_vector_overlap);
%include "specest/moving_average_vff.h"
GR_SWIG_BLOCK_MAGIC2(specest, moving_average_vff);
%include "specest/adaptiveweighting_vff.h"
GR_SWIG_BLOCK_MAGIC2(specest, adaptiveweighting_vff);

//%include "specest/arfcov_vcc.h"
//GR_SWIG_BLOCK_MAGIC2(specest, arfcov_vcc);
//%include "specest/fcov.h"
//GR_SWIG_BLOCK_MAGIC2(specest, fcov);
%include "specest/arfmcov_vcc.h"
GR_SWIG_BLOCK_MAGIC2(specest, arfmcov_vcc);
%include "specest/fmcov.h"
GR_SWIG_BLOCK_MAGIC2(specest, fmcov);
%include "specest/arburg_vcc.h"
GR_SWIG_BLOCK_MAGIC2(specest, arburg_vcc);
%include "specest/burg.h"
GR_SWIG_BLOCK_MAGIC2(specest, burg);
%include "specest/welch.h"
GR_SWIG_BLOCK_MAGIC2(specest, welch);
