/* -*- c++ -*- */

#define SPECEST_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "specest_swig_doc.i"

%{
#include "specest_adaptiveweighting_vff.h"
#include "specest_api.h"
#include "specest_arburg_vcc.h"
#include "specest_arfcov_vcc.h"
#include "specest_arfmcov_vcc.h"
#include "specest_burg.h"
#include "specest_cyclo_fam_calcspectrum_vcf.h"
#include "specest_cyclo_fam.h"
#include "specest_esprit.h"
#include "specest_esprit_spectrum_vcf.h"
#include "specest_esprit_vcf.h"
#include "specest_fcov.h"
#include "specest_fmcov.h"
#include "specest_moving_average_vff.h"
#include "specest_music.h"
#include "specest_music_vcf.h"
#include "specest_music_spectrum_vcf.h"
#include "specest_pad_vector.h"
#include "specest_reciprocal_ff.h"
#include "specest_stream_to_vector_overlap.h"
#include "specest_welch.h"
#include "specest_welchsp.h"
%}

GR_SWIG_BLOCK_MAGIC(specest,adaptiveweighting_vff);
%include "specest_adaptiveweighting_vff.h"

GR_SWIG_BLOCK_MAGIC(specest,arburg_vcc);
%include "specest_arburg_vcc.h"

GR_SWIG_BLOCK_MAGIC(specest,arfcov_vcc);
%include "specest_arfcov_vcc.h"

GR_SWIG_BLOCK_MAGIC(specest,arfmcov_vcc);
%include "specest_arfmcov_vcc.h"

GR_SWIG_BLOCK_MAGIC(specest,burg);
%include "specest_burg.h"

GR_SWIG_BLOCK_MAGIC(specest,cyclo_fam_calcspectrum_vcf);
%include "specest_cyclo_fam_calcspectrum_vcf.h"

GR_SWIG_BLOCK_MAGIC(specest,cyclo_fam);
%include "specest_cyclo_fam.h"

GR_SWIG_BLOCK_MAGIC(specest,esprit);
%include "specest_esprit.h"

GR_SWIG_BLOCK_MAGIC(specest,esprit_spectrum_vcf);
%include "specest_esprit_spectrum_vcf.h"

GR_SWIG_BLOCK_MAGIC(specest,esprit_vcf);
%include "specest_esprit_vcf.h"

GR_SWIG_BLOCK_MAGIC(specest,fcov);
%include "specest_fcov.h"

GR_SWIG_BLOCK_MAGIC(specest,fmcov);
%include "specest_fmcov.h"

GR_SWIG_BLOCK_MAGIC(specest,moving_average_vff);
%include "specest_moving_average_vff.h"

GR_SWIG_BLOCK_MAGIC(specest,music);
%include "specest_music.h"

GR_SWIG_BLOCK_MAGIC(specest,music_vcf);
%include "specest_music_vcf.h"

GR_SWIG_BLOCK_MAGIC(specest,music_spectrum_vcf);
%include "specest_music_spectrum_vcf.h"

GR_SWIG_BLOCK_MAGIC(specest,pad_vector);
%include "specest_pad_vector.h"

GR_SWIG_BLOCK_MAGIC(specest,reciprocal_ff);
%include "specest_reciprocal_ff.h"

GR_SWIG_BLOCK_MAGIC(specest,stream_to_vector_overlap);
%include "specest_stream_to_vector_overlap.h"

GR_SWIG_BLOCK_MAGIC(specest,welch);
%include "specest_welch.h"

GR_SWIG_BLOCK_MAGIC(specest,welchsp);
%include "specest_welchsp.h"

