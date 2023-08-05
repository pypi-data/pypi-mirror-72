/*
# Copyright (c) 2010-2018 Andrew Dalke Scientific, AB (Sweden)
#
# All chemfp 1.x software is distributed with the following license:
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
*/

#include "chemfp.h"
#include "chemfp_internal.h"
#include <string.h>

const char *chemfp_version(void) {
  return CHEMFP_VERSION_STRING;
}

const char *chemfp_strerror(int err) {
  switch (err) {
  case CHEMFP_OK: return "Ok";
  case CHEMFP_BAD_ARG: return "Bad argument";
   
  case CHEMFP_NO_MEM: return "Cannot allocate memory";

  case CHEMFP_UNSUPPORTED_WHITESPACE: return "Unsupported whitespace";
  case CHEMFP_MISSING_FINGERPRINT: return "Missing fingerprint field";
  case CHEMFP_BAD_FINGERPRINT: return "Fingerprint field is in the wrong format";
  case CHEMFP_UNEXPECTED_FINGERPRINT_LENGTH: return "Fingerprint is not the expected length";
  case CHEMFP_MISSING_ID: return "Missing id field";
  case CHEMFP_BAD_ID: return "Id field is in the wrong format";
  case CHEMFP_MISSING_NEWLINE: return "Line must end with a newline character";

  case CHEMFP_METHOD_MISMATCH: return "Mismatch between popcount method and alignment type";

  case CHEMFP_UNKNOWN_ORDERING: return "Unknown sort order";

  default: return "Unknown error";
  }
}

/* Code to handle getting and setting options */

typedef int (*get_option_f)(void);
typedef int (*set_option_f)(int);


typedef struct {
  const char *name;
  get_option_f getter;
  set_option_f setter;
} chemfp_option_type;

const chemfp_option_type chemfp_options[] = {
  {"report-popcount", chemfp_get_option_report_popcount, chemfp_set_option_report_popcount},
  {"report-intersect", chemfp_get_option_report_intersect_popcount,
   chemfp_set_option_report_intersect_popcount},

  /* Forwards-compatibility with chemfp-3.3. These always return the default. */
  {"report-algorithm", chemfp_get_option_report_algorithm, chemfp_set_option_report_algorithm},
  {"use-specialized-algorithms", chemfp_get_option_use_specialized_algorithms,
   chemfp_set_option_use_specialized_algorithms},
  {"num-column-threads", chemfp_get_option_num_column_threads,
   chemfp_set_option_num_column_threads}
};

int
chemfp_get_num_options(void) {
  return sizeof(chemfp_options) / sizeof(chemfp_option_type);
}

const char *
chemfp_get_option_name(int i) {
  if (i < 0 || i >= chemfp_get_num_options()) {
    return NULL;
  }
  return chemfp_options[i].name;
}

int
chemfp_get_option(const char *option) {
  int i;
  for (i=0; i<chemfp_get_num_options(); i++) {
    if (!strcmp(chemfp_options[i].name, option)) {
      return chemfp_options[i].getter();
    }
  }
  return CHEMFP_BAD_ARG;
}

int
chemfp_set_option(const char *option, int value) {
  int i;
  for (i=0; i<chemfp_get_num_options(); i++) {
    if (!strcmp(chemfp_options[i].name, option)) {
      return chemfp_options[i].setter(value);
    }
  }
  return CHEMFP_BAD_ARG;
}

/********* OpenMP ************/

#if defined(_OPENMP)
#include <omp.h>
/* The value 0 means "initialize using omp_get_max_threads()" */
/* Otherwise, this will be a value between 1 and omp_get_max_threads() */
static int chemfp_num_threads = 0;

#endif

int chemfp_get_num_threads(void) {
#if defined(_OPENMP)
  if (chemfp_num_threads == 0) {
    chemfp_num_threads = omp_get_max_threads();
  }
  return chemfp_num_threads;
#else
  return 1;
#endif
}

void chemfp_set_num_threads(int num_threads) {
#if defined(_OPENMP)
  /* Can only have between 1 thread and the number of logical cores */
  if (num_threads < 1) {
    num_threads = 1;
  }
  omp_set_num_threads(num_threads);

  /* Quoting from the docs: If you use omp_set_num_threads to change
     the number of threads, subsequent calls to omp_get_max_threads
     will return the new value. */
  chemfp_num_threads = omp_get_max_threads();
#else
  UNUSED(num_threads);
#endif
}

int chemfp_get_max_threads(void) {
#if defined(_OPENMP)
  return omp_get_max_threads();
#else
  return 1;
#endif

}

