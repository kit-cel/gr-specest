/* -*- c++ -*- */
/* This file is appended to specest_swig.i */
/* All of these files have Armadillo dependencies */

%{
#include "specest_music.h"
#include "specest_music_vcf.h"
#include "specest_music_spectrum_vcf.h"
%}

GR_SWIG_BLOCK_MAGIC(specest,music);
%include "specest_music.h"

GR_SWIG_BLOCK_MAGIC(specest,music_vcf);
%include "specest_music_vcf.h"

GR_SWIG_BLOCK_MAGIC(specest,music_spectrum_vcf);
%include "specest_music_spectrum_vcf.h"

