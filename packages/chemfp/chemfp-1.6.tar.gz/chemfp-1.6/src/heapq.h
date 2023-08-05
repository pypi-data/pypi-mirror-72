#ifndef CHEMFP_HEAPQ_H
#define CHEMFP_HEAPQ_H
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

/**** Low-level heap operations, for the best-of-N algorithms ****/

/* These are internal data types and functions. While they may */
/* be available in the library, do not call them directly. */


/* Compare two items in the heap. Return -1 on error, 1 for lt, otherwise 0 */
typedef int (*chemfp_heapq_lt)(void *data, int i, int j);

/* Swap two items in the heap. This function must never fail. */
typedef void (*chemfp_heapq_swap)(void *data, int i, int j);

/* Call after replacing the first element in a heapified list */
int chemfp_heapq_siftup(int len, void *heap, int pos,
                        chemfp_heapq_lt lt, chemfp_heapq_swap swap);

/* Convert the un-ordered list into a heap */
int chemfp_heapq_heapify(int len, void *heap,
                         chemfp_heapq_lt lt, chemfp_heapq_swap swap);

/* Must heapify first */
int chemfp_heapq_heapsort(int len, void *heap,
                          chemfp_heapq_lt lt, chemfp_heapq_swap swap);

#endif
