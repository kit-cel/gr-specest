/* -*- c++ -*- */

#define SPECEST_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "specest_swig_doc.i"

%{
#include "specest/reciprocal_ff.h"
#include "specest/pad_vector.h"
%}


%include "specest/reciprocal_ff.h"
GR_SWIG_BLOCK_MAGIC2(specest, reciprocal_ff);
%include "specest/pad_vector.h"
GR_SWIG_BLOCK_MAGIC2(specest, pad_vector);
