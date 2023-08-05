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


#include "popcount.h"

/* Quoting from Knuth, Fascicle 1,

  The first textbook on programming, "The Preparation of Programs for
  an Electronic Digital Computer" by Wilkes, Wheeler, and Gill,
  second edition (Reading, Mass.: Addison-Wesley, 1957), 155, 191-193,
  presented an interesting subroutine for sideways addition due to
  D. B. Gillies and J. C. P. Miller. Their method was devised for the
  35-bit numbers of the EDSAC, but it is readily converted to the
  following 64-bit procedure...

What follows is essentially this code, which is in Wikipedia
   http://en.wikipedia.org/wiki/Hamming_weight
as "popcount_3".

*/

int 
chemfp_popcount_gillies(int n, uint64_t *fp) {
  const uint64_t m1  = UINT64_C(0x5555555555555555);
  const uint64_t m2  = UINT64_C(0x3333333333333333);
  const uint64_t m4  = UINT64_C(0x0F0F0F0F0F0F0F0F);
  const uint64_t h01 = UINT64_C(0x0101010101010101);

  int bit_count = 0, i;
  int size = (n+7) / 8;
  uint64_t x;

  for (i=0; i<size; i++) {
    x = fp[i];
    x =  x       - ((x >> 1)  & m1);
    x = (x & m2) + ((x >> 2)  & m2);
    x = (x       +  (x >> 4)) & m4;
    bit_count += (int) ((x * h01) >> 56);
  }
  return bit_count;
}

int
chemfp_intersect_popcount_gillies(int n, uint64_t *fp1, uint64_t *fp2) {
  const uint64_t m1  = UINT64_C(0x5555555555555555);
  const uint64_t m2  = UINT64_C(0x3333333333333333);
  const uint64_t m4  = UINT64_C(0x0F0F0F0F0F0F0F0F);
  const uint64_t h01 = UINT64_C(0x0101010101010101);

  int bit_count = 0, i;
  int size = (n+7) / 8;
  uint64_t x;

  for (i=0; i<size; i++) {
    x = fp1[i] & fp2[i];
    x =  x       - ((x >> 1)  & m1);
    x = (x & m2) + ((x >> 2)  & m2);
    x = (x       +  (x >> 4)) & m4;
    bit_count += (int) ((x * h01) >> 56);
  }
  return bit_count;
}
