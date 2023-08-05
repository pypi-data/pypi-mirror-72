#ifndef CHEMFP_INTERNAL_H
#define CHEMFP_INTERNAL_H

/* 
# Copyright (c) 2011-2020 Andrew Dalke Scientific, AB (Sweden)
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

#define ALIGNMENT(POINTER, BYTE_COUNT) \
  (((uintptr_t)(const void *)(POINTER)) % (BYTE_COUNT))


/* Macro to use for variable names which exist as a */
/* function parameter but otherwise aren't used */
/* This is to prevent compiler warnings on msvc /W4 */
#define UNUSED(x) (void)(x);

int chemfp_get_min_intersect_popcount(int popcount_sum, double threshold);
  
int chemfp_get_option_report_popcount(void);
int chemfp_set_option_report_popcount(int);

int chemfp_get_option_report_intersect_popcount(void);
int chemfp_set_option_report_intersect_popcount(int);

int chemfp_get_option_report_algorithm(void);
int chemfp_set_option_report_algorithm(int);

int chemfp_get_option_use_specialized_algorithms(void);
int chemfp_set_option_use_specialized_algorithms(int);

int chemfp_get_option_num_column_threads(void);
int chemfp_set_option_num_column_threads(int);


int chemfp_add_hit(chemfp_search_result *result, int target_index, double score);

/* Scaling factor to convert floats and doubles into integers */
#define CHEMFP_FLOAT_SCALE 10000

#endif
