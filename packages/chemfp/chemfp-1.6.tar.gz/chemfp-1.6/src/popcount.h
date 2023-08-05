#if !defined(POPCOUNT_H)
#define POPCOUNT_H
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

#include <stdint.h>
#include "chemfp.h"
#include "chemfp_internal.h"


enum {
  CHEMFP_ALIGN1=0,
  CHEMFP_ALIGN4,
  CHEMFP_ALIGN8_SMALL,
  CHEMFP_ALIGN8_LARGE,
  CHEMFP_ALIGN_SSSE3
};

/* These are in the same order as compile_time_methods */
enum {
  CHEMFP_LUT8_1=0,
  CHEMFP_LUT8_4,
  CHEMFP_LUT16_4,
  CHEMFP_LAURADOUX,
  CHEMFP_POPCNT,
  CHEMFP_GILLIES,
  CHEMFP_SSSE3
};

typedef int (*chemfp_method_check_f)(void);

typedef struct {
  int detected_index;
  int id;
  const char *name;
  int alignment;
  int min_size;
  chemfp_method_check_f check;
  chemfp_popcount_f popcount;
  chemfp_intersect_popcount_f intersect_popcount;
} chemfp_method_type;

typedef struct {
  const char *name;
  int alignment;
  int min_size;
  chemfp_method_type *method_p;
} chemfp_alignment_type;


extern chemfp_alignment_type chemfp_alignments[];

int chemfp_popcount_lut8_1(int n, const unsigned char *fp);
int chemfp_intersect_popcount_lut8_1(int n, const unsigned char *fp1, const unsigned char *fp2);

int chemfp_popcount_lut8_4(int n, uint32_t *fp);
int chemfp_intersect_popcount_lut8_4(int n, uint32_t *fp1, uint32_t *fp2);

int chemfp_popcount_lut16_4(int n, uint32_t *fp);
int chemfp_intersect_popcount_lut16_4(int n, uint32_t *fp1, uint32_t *fp2);

int chemfp_popcount_gillies(int n, uint64_t *fp);
int chemfp_intersect_popcount_gillies(int n, uint64_t *fp1, uint64_t *fp2);

int chemfp_popcount_lauradoux(int size, const uint64_t *fp);
int chemfp_intersect_popcount_lauradoux(int size, const uint64_t *fp1, const uint64_t *fp2);

int chemfp_popcount_popcnt(int size, const uint64_t *fp);
int chemfp_intersect_popcount_popcnt(int size, const uint64_t *fp1, const uint64_t *fp2);

/* Special case for the MACCS keys stored in 24 bytes */
int chemfp_popcount_popcnt_24(ssize_t size, const uint64_t *fp);
int chemfp_intersect_popcount_popcnt_24(ssize_t size, const uint64_t *fp1, const uint64_t *fp2);

/* Special cases for 512, 881, 1024, and 2048 bits */
int chemfp_popcount_popcnt_64(ssize_t size, const uint64_t *fp);
int chemfp_intersect_popcount_popcnt_64(ssize_t size, const uint64_t *fp1, const uint64_t *fp2);

int chemfp_popcount_popcnt_112(ssize_t size, const uint64_t *fp);
int chemfp_intersect_popcount_popcnt_112(ssize_t size, const uint64_t *fp1, const uint64_t *fp2);

int chemfp_popcount_popcnt_128(ssize_t size, const uint64_t *fp);
int chemfp_intersect_popcount_popcnt_128(ssize_t size, const uint64_t *fp1, const uint64_t *fp2);

int chemfp_popcount_popcnt_128_128(ssize_t size, const uint64_t *fp);
int chemfp_intersect_popcount_popcnt_128_128(ssize_t size, const uint64_t *fp1, const uint64_t *fp2);


int chemfp_popcount_SSSE3(int, const unsigned*);
int chemfp_intersect_popcount_SSSE3(int, const unsigned*, const unsigned*);
int chemfp_has_ssse3(void);
#endif
