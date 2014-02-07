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
%}


%include "specest/reciprocal_ff.h"
GR_SWIG_BLOCK_MAGIC2(specest, reciprocal_ff);
%include "specest/pad_vector.h"
GR_SWIG_BLOCK_MAGIC2(specest, pad_vector);
%include "specest/stream_to_vector_overlap.h"
GR_SWIG_BLOCK_MAGIC2(specest, stream_to_vector_overlap);
%include "specest/moving_average_vff.h"
GR_SWIG_BLOCK_MAGIC2(specest, moving_average_vff);
