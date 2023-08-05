/* 
# Copyright (c) 2010-2020 Andrew Dalke Scientific, AB (Sweden)
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
#include "popcount.h"
#include "chemfp_internal.h"
#include <stdio.h>
#include <math.h>

/* Bit operations related to byte and hex fingerprints

  A byte fingerprint is a length and a sequence of bytes where each byte
  stores 8 fingerprints bits, in the usual order. (That is, the byte 'A',
  which is the hex value 0x41, is the bit pattern "01000001".)


  A hex fingerprint is also stored as a length and a sequence of bytes
  but each byte encode 4 bits of the fingerprint as a hex character. The
  only valid byte values are 0-9, A-F and a-f. Other values will cause
  an error value to be returned. */

/***** Functions for hex fingerprints ******/

/* Map from ASCII value to bit count. Used with hex fingerprints.
   BIG is used in cumulative bitwise-or tests to check for non-hex input */

#define BIG 16
static int hex_to_value[256] = {
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  0,     1,   2,   3,   4,   5,   6,   7,   8,   9, BIG, BIG, BIG, BIG, BIG, BIG,

  /* Upper-case A-F */
  BIG,  10,  11,  12,  13,  14,  15, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,

  /* Lower-case a-f */
  BIG,  10,  11,  12,  13,  14,  15, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,

  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,

  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
  BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG, BIG,
};

/* Map from ASCII value to popcount. Used with hex fingerprints. */

static int hex_to_popcount[256] = {
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
   0,   1,   1,   2,   1,   2,   2,   3,   1,   2,    0,   0,   0,   0,   0,   0,

    0,  2,   3,   2,   3,   3,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,  2,   3,   2,   3,   3,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,

    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,

    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

/* Map from an integer to its popcount. The maximum possible valid hex
   input is 'f'/'F', which is 15, but non-hex input will set bit 0x10, so
   I include the range 16-31 as well. */

static int nibble_popcount[32] = {
  0, 1, 1, 2, 1, 2, 2, 3,
  1, 2, 2, 3, 2, 3, 3, 4,
  0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0,
};

/* Return 1 if the string contains only an even number of hex characters; 0 otherwise */
int chemfp_hex_isvalid(ssize_t len, const char *sfp) {
  ssize_t i;
  int union_w=0;
  const unsigned char *fp = (unsigned char *) sfp;

  if (len % 2 != 0) {
    /* Must be an even number of characters */
    return 0;
  }
  /* Out of range values set 0x10 so do cumulative bitwise-or and see if that
     bit is set. Optimize for the expected common case of validfingerprints. */
  for (i=0; i<len; i++) {
    union_w |= hex_to_value[fp[i]];
  }
  return (union_w < BIG) ? 1 : 0;
}

/* Return the population count of a hex fingerprint, otherwise return -1 */
long long chemfp_hex_popcount(ssize_t len, const char *sfp) {
  ssize_t i;
  int union_w=0;
  long long popcount=0;
  const unsigned char *fp = (const unsigned char *) sfp;

  for (i=0; i<len; i++) {
    /* Keep track of the cumulative popcount and the cumulative bitwise-or */
    popcount += hex_to_popcount[fp[i]];
    union_w |= hex_to_value[fp[i]];
  }
  if (union_w >= BIG) {
    return -1;  /* Then this was an invalid fingerprint (contained non-hex characters) */
  }
  return popcount;
}

/* Return the population count of the intersection of two hex fingerprints,
   otherwise return -1. */
long long chemfp_hex_intersect_popcount(ssize_t len, const char *sfp1, const char *sfp2) {
  long long i, intersect_popcount=0;
  int w1, w2, union_w=0;
  const unsigned char *fp1 = (const unsigned char *) sfp1;
  const unsigned char *fp2 = (const unsigned char *) sfp2;
  for (i=0; i<len; i++) {
    /* Get the popcount for each hex value. (Or 0 for non-hex values.) */
    w1 = hex_to_value[fp1[i]];
    w2 = hex_to_value[fp2[i]];
    /* Cumulative bitwise-or to check for non-hex values  */
    union_w = union_w | (w1|w2);
    intersect_popcount = intersect_popcount + nibble_popcount[w1 & w2];
  }
  if (union_w >= BIG) {
    return -1;
  }
  return intersect_popcount;
}

/* Return the Tanimoto between two hex fingerprints, or -1.0 for invalid fingerprints
   If neither fingerprint has any set bits then return 1.0 */
double chemfp_hex_tanimoto(ssize_t len, const char *sfp1, const char *sfp2) {
  ssize_t i=0;
  int union_w=0;
  long long union_popcount=0, intersect_popcount=0;
  int w1, w2;
  int w3, w4;
  ssize_t upper_bound = len - (len%2);
  const unsigned char *fp1 = (const unsigned char *) sfp1;
  const unsigned char *fp2 = (const unsigned char *) sfp2;

  /* Hex fingerprints really should be even-length since two hex characters
     are used for a single fingerprint byte and all chemfp fingerprints must
     be a multiple of 8 bits. I'll allow odd-lengths since I don't see how
     that's a bad idea and I can see how some people will be confused by
     expecting odd lengths to work. More specifically, I was confused because
     I used some odd lengths in my tests. ;) */

  /* I'll process two characters at a time. Loop-unrolling was about 4% faster. */
  for (; i<upper_bound; i+=2) {
    w1 = hex_to_value[fp1[i]];
    w2 = hex_to_value[fp2[i]];
    w3 = hex_to_value[fp1[i+1]];
    w4 = hex_to_value[fp2[i+1]];
    /* Check for illegal characters */
    union_w |= (w1|w2|w3|w4);
    /* The largest possible index is w1|w2 = (16 | 15) == 31 and */
    /* is only possible when the input is not a legal hex character. */
    union_popcount += nibble_popcount[w1|w2]+nibble_popcount[w3|w4];
    /* The largest possible index is w1&w2 = (16 & 16) == 16 */
    intersect_popcount += nibble_popcount[w1&w2]+nibble_popcount[w3&w4];
  }
  /* Handle the final byte for the case of odd fingerprint length */
  for (; i<len; i++) {
    w1 = hex_to_value[fp1[i]];
    w2 = hex_to_value[fp2[i]];
    /* Check for illegal characters */
    union_w |= (w1|w2);
    /* The largest possible index is (16 | 15) == 31 */
    /* (and only when the input isn't a legal hex character) */
    union_popcount += nibble_popcount[w1|w2];
    /* The largest possible index is (16 & 16) == 16 */
    intersect_popcount += nibble_popcount[w1&w2];
  }
  /* Check for illegal character */
  if (union_w >= BIG) {
    return -1.0;
  }
  /* Special case define that 0/0 = 0.0. It's hard to decide what to 
         use here, for example, OpenEye uses 1.0. It seems that 0.0
     is the least surprising choice. */
  if (union_popcount == 0) {
    return 0.0;
  }
  return (intersect_popcount + 0.0) / union_popcount;  /* +0.0 to coerce to double */
}

/* Return the Tversky similarity between two hex fingerprints.
   If neither fingerprint has any set bits then return 0.0.
   Return -1.0 if either fingeprint is non-hex. */
/* Using Bradshaw's nomenclature and bounds from
   http://www.daylight.com/meetings/mug97/Bradshaw/MUG97/tv_tversky.html */
double chemfp_hex_tversky(ssize_t len, const char *sfp1,
                          const char *sfp2, double alpha, double beta) {
  ssize_t i;
  int A=0, B=0, c=0;
  int w1, w2, union_w=0;
  int scaled_alpha = (int)lrint(alpha * CHEMFP_FLOAT_SCALE);
  int scaled_beta = (int)lrint(beta * CHEMFP_FLOAT_SCALE);
  int denominator;
  const unsigned char *fp1 = (const unsigned char *) sfp1;
  const unsigned char *fp2 = (const unsigned char *) sfp2;
  if (scaled_alpha == 0 && scaled_beta == 0) {
    /* If there are any bits in common, return 1.0 */
    for (i=0; i<len; i++) {
      w1 = hex_to_value[fp1[i]];
      w2 = hex_to_value[fp2[i]];
      union_w |= (w1|w2);
      c |= (w1 & w2);  /* Only need a single match */
    }
    /* Check if there were non-hex characters */
    if (union_w >= BIG) {
      return -1.0;
    }
    if (c) {
      /* There was at least one bit in common */
      return 1.0;
    }
    /* Otherwise, return 0.0 */
    return 0.0;
  }

  /* Accumulate the total individual and intersection popcounts */
  for (i=0; i<len; i++) {
    w1 = hex_to_value[fp1[i]];
    w2 = hex_to_value[fp2[i]];
    union_w |= (w1|w2);
    A += nibble_popcount[w1];
    B += nibble_popcount[w2];
    c += nibble_popcount[w1&w2];
  }
  if (union_w >= BIG) {
    return -1.0;
  }
  /* Special case for when neither fingerprint has any bytes set */
  if (!A && !B) {
    return 0.0;
  }
  denominator = scaled_alpha*A + scaled_beta*B + c*(CHEMFP_FLOAT_SCALE-scaled_alpha-scaled_beta);
  if (denominator == 0) {
    /* We already handled the alpha=beta=0.0 case. */
    /* By definition, make this be 0.0. */
    return 0.0;
  }
  return ((double)(c * CHEMFP_FLOAT_SCALE)) / denominator;
}



/* Return 1 if the query fingerprint is contained in the target, 0 if it isn't,
   or -1 for invalid fingerprints */
/* This code assumes that 1) most tests fail and 2) most fingerprints are valid */
int chemfp_hex_contains(ssize_t len, const char *squery_fp,
                        const char *starget_fp) {
  ssize_t i;
  int query_w, target_w;
  int union_w=0;
  const unsigned char *query_fp = (const unsigned char *) squery_fp;
  const unsigned char *target_fp = (const unsigned char *) starget_fp;

  for (i=0; i<len; i++) {
    /* Subset test is easy; check if query & target == query
       I'll do word-by-word tests, where the word can also overflow to BIG
       Do the normal test against BIG to see if there was a non-hex input */
    query_w = hex_to_value[query_fp[i]];
    target_w = hex_to_value[target_fp[i]];
    union_w |= (query_w|target_w);
    if ((query_w & target_w) != query_w) {
      /* Not a subset, but first, check if there was a a non-hex input */
      if (union_w >= BIG) {
        return -1;
      }
      return 0;
    }
  }
  /* This was a subset, but there might have been a non-hex input */
  if (union_w >= BIG) {
    return -1;
  }
  return 1;
}

/* Return 1 if the fingerprint sets the bit, 0 if it isn't, or the bit is */
/* out of range or not a hex fingerprint. */
int chemfp_hex_contains_bit(ssize_t len, const char *fp, long long bit) {
  ssize_t byteno;
  int bitno;
  char c;
  int contains;
  
  if (bit < 0 || (bit/4LL >= (long long) len)) {
    return 0;
  }

  byteno = (int)(bit / 4);
  bitno = (int) bit % 8;
  if (bitno >= 4) {
    bitno -= 4;
    byteno--;
  } else {
    byteno++;
  }
  
  c = fp[byteno];
  switch (bitno) {
  case 0: contains = (c=='1' || c=='3' || c=='5' || c=='7' || c=='9'
		      || c=='b' || c=='d' || c=='f' || c=='B' || c=='D' || c=='F');
    break;
  case 1: contains = (c=='2' || c=='3' || c=='6' || c=='7' 
		      || c=='a' || c=='b' || c=='e' || c=='f'
		      || c=='A' || c=='B' || c=='E' || c=='F');
    break;
  case 2: contains = (c=='4' || c=='5' || c=='6' || c=='7'
		      || c=='c' || c=='d' || c=='e' || c=='f'
		      || c=='C' || c=='D' || c=='E' || c=='F');
    break;
  case 3: contains = (c=='8' || c=='9'
		      || ('a' <= c && c <='f')
		      || ('A' <= c && c <='F'));
    break;
  default:
    contains = 0;  /* Shouldn't get here */
  }
  return contains;
}


/* intersect[] = fp1[] & fp2 */

int chemfp_hex_intersect(ssize_t len, char *dest, const char *fp1, const char *fp2) {
  unsigned char *s1, *s2;
  ssize_t i;
  unsigned char val1, val2;

  s1 = (unsigned char *) fp1;
  s2 = (unsigned char *) fp2;
  for (i=0; i<len; i++) {
    if (s1[i] >= '0' && s1[i] <= '9') {
      val1 = s1[i]-'0';
    } else if (s1[i] >= 'a' && s1[i] <= 'f') {
      val1 = s1[i]-('a'-10);
    } else if (s1[i] >= 'A' && s1[i] <= 'F') {
      val1 = s1[i]-('A'-10);
    } else {
      for (;i<len; i++) {
	dest[i] = '0';
      }
      return CHEMFP_BAD_FINGERPRINT;
    }

    if (s2[i] >= '0' && s2[i] <= '9') {
      val2 = s2[i]-'0';
    } else if (s2[i] >= 'a' && s2[i] <= 'f') {
      val2 = s2[i]-('a'-10);
    } else if (s2[i] >= 'A' && s2[i] <= 'F') {
      val2 = s2[i]-('A'-10);
    } else {
      for (;i<len; i++) {
	dest[i] = '0';
      }
      return CHEMFP_BAD_FINGERPRINT;
    }
    
    val1 &= val2;
    if (val1 < 10) {
      dest[i] = '0' + val1;
    } else {
      dest[i] = 'a'-10 + val1;
    }
  }
  return CHEMFP_OK;
}

/* union[] = fp1[] | fp2 */

int chemfp_hex_union(ssize_t len, char *dest, const char *fp1, const char *fp2) {
  unsigned char *s1, *s2;
  ssize_t i;
  unsigned char val1, val2;

  s1 = (unsigned char *) fp1;
  s2 = (unsigned char *) fp2;
  for (i=0; i<len; i++) {
    if (s1[i] >= '0' && s1[i] <= '9') {
      val1 = s1[i]-'0';
    } else if (s1[i] >= 'a' && s1[i] <= 'f') {
      val1 = s1[i]-('a'-10);
    } else if (s1[i] >= 'A' && s1[i] <= 'F') {
      val1 = s1[i]-('A'-10);
    } else {
      for (;i<len; i++) {
	dest[i] = '0';
      }
      return CHEMFP_BAD_FINGERPRINT;
    }

    if (s2[i] >= '0' && s2[i] <= '9') {
      val2 = s2[i]-'0';
    } else if (s2[i] >= 'a' && s2[i] <= 'f') {
      val2 = s2[i]-('a'-10);
    } else if (s2[i] >= 'A' && s2[i] <= 'F') {
      val2 = s2[i]-('A'-10);
    } else {
      for (;i<len; i++) {
	dest[i] = '0';
      }
      return CHEMFP_BAD_FINGERPRINT;
    }
    
    val1 |= val2;
    if (val1 < 10) {
      dest[i] = '0' + val1;
    } else {
      dest[i] = 'a'-10 + val1;
    }
  }
  return CHEMFP_OK;
}

/* difference[] = fp1[] ^ fp2 */

int chemfp_hex_difference(ssize_t len, char *dest, const char *fp1, const char *fp2) {
  unsigned char *s1, *s2;
  ssize_t i;
  unsigned char val1, val2;

  s1 = (unsigned char *) fp1;
  s2 = (unsigned char *) fp2;
  for (i=0; i<len; i++) {
    if (s1[i] >= '0' && s1[i] <= '9') {
      val1 = s1[i]-'0';
    } else if (s1[i] >= 'a' && s1[i] <= 'f') {
      val1 = s1[i]-('a'-10);
    } else if (s1[i] >= 'A' && s1[i] <= 'F') {
      val1 = s1[i]-('A'-10);
    } else {
      for (;i<len; i++) {
	dest[i] = '0';
      }
      return CHEMFP_BAD_FINGERPRINT;
    }

    if (s2[i] >= '0' && s2[i] <= '9') {
      val2 = s2[i]-'0';
    } else if (s2[i] >= 'a' && s2[i] <= 'f') {
      val2 = s2[i]-('a'-10);
    } else if (s2[i] >= 'A' && s2[i] <= 'F') {
      val2 = s2[i]-('A'-10);
    } else {
      for (;i<len; i++) {
	dest[i] = '0';
      }
      return CHEMFP_BAD_FINGERPRINT;
    }
    
    val1 ^= val2;
    if (val1 < 10) {
      dest[i] = '0' + val1;
    } else {
      dest[i] = 'a'-10 + val1;
    }
  }
  return CHEMFP_OK;
}



/****** byte fingerprints *******/

/* These algorithms are a lot simpler than working with hex fingeprints.
   There are a number of performance tweaks I could put in, especially
   if I know the inputs are word aligned, but I'll leave those for later. */

static int byte_popcounts[] = {
  0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
  1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
  1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
  2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
  1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
  2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
  2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
  3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8  };


/* Return the population count of a byte fingerprint */
long long chemfp_byte_popcount(ssize_t len, const unsigned char *fp) {
  long long count = 0;
  int alignment;
  int extra_size;
  chemfp_popcount_f calc_popcount;
  if (len < 256) {
    /* The Python overhead is high enough that I won't worry about optimizing for small strings */
    return chemfp_popcount_lut8_1((int)len, fp);
  }

  /* Move up to the nearest 16 byte alignment */
  /* (Only the SSSE3 implementations require 16 byte alignment. The
     others can handle 8. When should I drop support for SSSE3?) */
  alignment = (int) ALIGNMENT(fp, 16);
  if (alignment) {
    extra_size = 16 - alignment;
    count += chemfp_popcount_lut8_1(extra_size, fp);
    len -= extra_size;
    fp += extra_size;
  }

  /* Every implementation can handle a multiple of 128 bytes */
  /* Figure out how many bytes remain past the last alignment */
  extra_size = (int) (len % 128);
  if (extra_size) {
    len -= extra_size;
  }
  calc_popcount = chemfp_select_popcount(1024, len, fp);
  /* The underlying functions return at most 32 bits of popcount. */
  /* This may fail if someone passes in, say, a 7 GB string. */
  /* Instead, process 2**27 bytes at a time and accumulate the results into a long long. */
  /* (The most number of bits in 2**27 bytes is 2**30, which fits into a 32 bit int.) */
  while (len > 134217728) {
    count += calc_popcount(134217728, fp);
    len -= 134217728;
    fp += 134217728;
  }
  if (len) {
    calc_popcount = chemfp_select_popcount((int) (8*len), len, fp);
    count += calc_popcount((int) len, fp);
    if (extra_size) {
      count += chemfp_popcount_lut8_1(extra_size, fp+len);
    }
  } else if (count) {
    count += chemfp_popcount_lut8_1(extra_size, fp);
  }
  
  return count;
}

/* Return the population count of the intersection of two byte fingerprints */
long long chemfp_byte_intersect_popcount(ssize_t len, const unsigned char *fp1,
                                         const unsigned char *fp2) {
  long long count = 0;
  int alignment;
  int extra_size;
  if (len < 256) {
    /* The Python overhead is high enough that I won't worry about optimizing for small strings */
    return chemfp_intersect_popcount_lut8_1((int) len, fp1, fp2);
  }

  /* Move up to the nearest 8 byte alignment */
  /* (Only the SSSE3 implementations require 16 byte alignment. The
     others can handle 8. When should I drop support for SSSE3?) */
  alignment = (int) ALIGNMENT(fp1, 16);
  if (alignment) {
    extra_size = 16 - alignment;
    count += chemfp_intersect_popcount_lut8_1(extra_size, fp1, fp2);
    len -= extra_size;
    fp1 += extra_size;
    fp2 += extra_size;
  }

  /* Figure out how many bytes remain past the last alignment */
  extra_size = (int) (len % 128);
  if (extra_size) {
    len -= extra_size;
  }

  chemfp_intersect_popcount_f calc_intersect_popcount = chemfp_select_intersect_popcount(1024, len, fp1, len, fp2);
  /* The underlying functions return at most 32 bits of popcount. */
  /* This may fail if someone passes in, say, a 7 GB string. */
  /* Instead, process 2**27 bytes at a time and accumulate the results into a long. */
  /* (The most number of bits in 2**27 bytes is 2**30, which fits into a 32 bit int.) */
  while (len > 134217728) {
    count += calc_intersect_popcount(134217728, fp1, fp2);
    len -= 134217728;
    fp1 += 134217728;
    fp2 += 134217728;
  }
  if (len) {
    count += calc_intersect_popcount((int) len, fp1, fp2);
    if (extra_size) {
      count += chemfp_intersect_popcount_lut8_1(extra_size, fp1+len, fp2+len);
    }
  } else if (count) {
    count += chemfp_intersect_popcount_lut8_1(extra_size, fp1+len, fp2+len);
  }
  
  return count;
}


/* Return the Tanimoto between two byte fingerprints.
   If neither fingerprint has any set bits then return 0.0 */
double chemfp_byte_tanimoto(ssize_t len, const unsigned char *fp1,
                            const unsigned char *fp2) {
  ssize_t i;
  long long A=0, B=0, union_popcount, intersect_popcount=0;
  /* Accumulate the total union and intersection popcounts */
  for (i=0; i<len; i++) {
    /* It's twice as fast to compute individual popcounts ... */
    A += byte_popcounts[fp1[i]];
    B += byte_popcounts[fp2[i]];
    /* ... than to compute the union first */
    /*union_popcount += byte_popcounts[fp1[i] | fp2[i]];*/
    
    intersect_popcount += byte_popcounts[fp1[i] & fp2[i]];
  }
  /* Special case for when neither fingerprint has any bytes set */
  union_popcount = A + B - intersect_popcount;
  if (union_popcount == 0) {
    return 0.0;
  }
  return ((double)intersect_popcount) / union_popcount;
}

/* Return the Tversky similarity between two byte fingerprints.
   If neither fingerprint has any set bits then return 0.0 */
/* Using Bradshaw's nomenclature and bounds from
   http://www.daylight.com/meetings/mug97/Bradshaw/MUG97/tv_tversky.html */
double chemfp_byte_tversky(ssize_t len, const unsigned char *fp1,
                           const unsigned char *fp2, double alpha, double beta) {
  ssize_t i;
  int A=0, B=0, c=0;
  int scaled_alpha = (int)lrint(alpha * CHEMFP_FLOAT_SCALE);
  int scaled_beta = (int)lrint(beta * CHEMFP_FLOAT_SCALE);
  int denominator;
  if (scaled_alpha == 0 && scaled_beta == 0) {
    /* If there are any bits in common, return 1.0 */
    for (i=0; i<len; i++) {
      if (fp1[i] & fp2[i]) {
	return 1.0;
      }
    }
    /* Otherwise, return 0.0 */
    return 0.0;
  }

  /* Accumulate the total individual and intersection popcounts */
  for (i=0; i<len; i++) {
    A += byte_popcounts[fp1[i]];
    B += byte_popcounts[fp2[i]];
    c += byte_popcounts[fp1[i] & fp2[i]];
  }

  /* Special case for when neither fingerprint has any bytes set */
  if (!A && !B) {
    return 0.0;
  }
  denominator = (scaled_alpha*A + scaled_beta*B
		 + c*(CHEMFP_FLOAT_SCALE-scaled_alpha-scaled_beta));
  if (denominator == 0) {
    /* We already handled the alpha=beta=0.0 case. */
    /* By definition, make this be 0.0. */
    return 0.0;
  }
  return ((double) (c * CHEMFP_FLOAT_SCALE)) / denominator;
}
double chemfp_byte_tversky_scaled(ssize_t len, const unsigned char *fp1,
				  const unsigned char *fp2,
				  int scaled_alpha, int scaled_beta) {
  ssize_t i;
  long long A=0, B=0, c=0;
  long long denominator;
  if (scaled_alpha == 0 && scaled_beta == 0) {
    /* If there are any bits in common, return 1.0 */
    for (i=0; i<len; i++) {
      if (fp1[i] & fp2[i]) {
	return 1.0;
      }
    }
    /* Otherwise, return 0.0 */
    return 0.0;
  }

  /* Accumulate the total individual and intersection popcounts */
  for (i=0; i<len; i++) {
    A += byte_popcounts[fp1[i]];
    B += byte_popcounts[fp2[i]];
    c += byte_popcounts[fp1[i] & fp2[i]];
  }

  /* Special case for when neither fingerprint has any bytes set */
  if (!A && !B) {
    return 0.0;
  }
  denominator = (scaled_alpha*A + scaled_beta*B
		 + c*(CHEMFP_FLOAT_SCALE-scaled_alpha-scaled_beta));
  if (denominator == 0) {
    /* We already handled the alpha=beta=0.0 case. */
    /* By definition, make this be 0.0. */
    return 0.0;
  }
  return ((double) (c * CHEMFP_FLOAT_SCALE)) / denominator;
}

/* Return 1 if the query fingerprint is contained in the target, 0 if it isn't */
int chemfp_byte_contains(ssize_t len, const unsigned char *query_fp,
                         const unsigned char *target_fp) {
  ssize_t i;
  for (i=0; i<len; i++) {
    if ((query_fp[i] & target_fp[i]) != query_fp[i]) {
      return 0;
    }
  }
  return 1;
}

/* Return 1 if the fingerprint sets the bit, 0 if it isn't, or the bit is */
/* out of range. */
int chemfp_byte_contains_bit(ssize_t len, const char *fp, long long bit) {
  const char *s = fp;
  if (bit < 0 || bit/8 >= len) {
    return 0;
  }
  return s[bit/8] & (1 << (bit%8) );
}


/* intersect[] = fp1[] & fp2 */

void chemfp_byte_intersect(ssize_t len, char *dest, const char *fp1, const char *fp2) {
  unsigned char *s, *s1, *s2;
  ssize_t i;

  s = (unsigned char *) dest;
  s1 = (unsigned char *) fp1;
  s2 = (unsigned char *) fp2;
  for (i=0; i<len; i++) {
    s[i] = s1[i] & s2[i];
  }
}

/* union[] = fp1[] | fp2 */

void chemfp_byte_union(ssize_t len, char *dest, const char *fp1, const char *fp2) {
  unsigned char *s, *s1, *s2;
  ssize_t i;

  s = (unsigned char *) dest;
  s1 = (unsigned char *) fp1;
  s2 = (unsigned char *) fp2;
  for (i=0; i<len; i++) {
    s[i] = s1[i] | s2[i];
  }
}

/* difference[] = fp1[] | fp2 */

void chemfp_byte_difference(ssize_t len, char *dest, const char *fp1, const char *fp2) {
  unsigned char *s, *s1, *s2;
  ssize_t i;

  s = (unsigned char *) dest;
  s1 = (unsigned char *) fp1;
  s2 = (unsigned char *) fp2;
  for (i=0; i<len; i++) {
    s[i] = s1[i] ^ s2[i];
  }
}


/* Construct tables of 4 bits for the byte nibble and 8 bits for the hex character */
/* Use 16 to indicate an error value. */

static unsigned char hex_union_popcount[16*256] = {
  /* 0 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 1 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  1, 1, 2, 2, 2, 2, 3, 3, 2, 2, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 2 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  1, 2, 1, 2, 2, 3, 2, 3, 2, 3, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 3 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 4 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 5 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  2, 2, 3, 3, 2, 2, 3, 3, 3, 3, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 6 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  2, 3, 2, 3, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 7 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 8 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 9 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  2, 2, 3, 3, 3, 3, 4, 4, 2, 2, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 10 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  2, 3, 2, 3, 3, 4, 3, 4, 2, 3, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 11 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 3, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 12 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  2, 3, 3, 4, 2, 3, 3, 4, 2, 3, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 13 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 3, 3, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 14 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 3, 4, 3, 4, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 15 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
};

static unsigned char hex_intersect_popcount[16*256] = {
  /* 0 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16,
  16, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 0, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 1 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 16, 16, 16, 16, 16, 16,
  16, 0, 1, 0, 1, 0, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 0, 1, 0, 1, 0, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 2 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 0, 0, 1, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 0, 0, 1, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 3 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 0, 1, 1, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 0, 1, 1, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 4 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 16, 16, 16, 16, 16, 16,
  16, 0, 0, 1, 1, 1, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 0, 0, 1, 1, 1, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 5 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 16, 16, 16, 16, 16, 16,
  16, 0, 1, 1, 2, 1, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 0, 1, 1, 2, 1, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 6 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 1, 1, 1, 1, 2, 2, 0, 0, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 1, 1, 2, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 1, 1, 2, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 7 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 1, 2, 1, 2, 2, 3, 0, 1, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 1, 2, 2, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 1, 2, 2, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 8 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 1, 1, 1, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 1, 1, 1, 1, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 9 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 0, 1, 0, 1, 0, 1, 1, 2, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 1, 2, 1, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 1, 2, 1, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 10 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 16, 16, 16, 16, 16, 16,
  16, 2, 2, 1, 1, 2, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 2, 1, 1, 2, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 11 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 1, 2, 0, 1, 1, 2, 1, 2, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 1, 2, 2, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 1, 2, 2, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 12 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 2, 2, 2, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 1, 2, 2, 2, 2, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 13 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 0, 1, 1, 2, 1, 2, 1, 2, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 2, 3, 2, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 1, 2, 2, 3, 2, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 14 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 16, 16, 16, 16, 16, 16,
  16, 2, 2, 2, 2, 3, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 2, 2, 2, 3, 3, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  /* 15 */
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 2, 3, 2, 3, 3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
};


/* Return the Tanimoto between a byte fingerprint and a hex fingerprint */
/* The size is the number of bytes in the byte_fp */
double chemfp_byte_hex_tanimoto(ssize_t len,
                                const unsigned char *byte_fp,
                                const char *shex_fp) {
  const unsigned char *hex_fp = (unsigned char *) shex_fp;
  int check_word=0;
  int union_popcount=0, intersect_popcount=0;
  int byte_union_popcount, byte_intersect_popcount;
  unsigned char byte;
  int high_nibble, low_nibble;

  while (len > 0) {
    byte = *byte_fp++;
    /* Construct 12 bit words with a nibble from the byte and character from the hex */
    high_nibble = (byte & 0xf0) << 4;
    low_nibble = (byte & 0xf) << 8;

    byte_union_popcount = (hex_union_popcount[high_nibble|hex_fp[0]] +
                           hex_union_popcount[low_nibble|hex_fp[1]]);
    byte_intersect_popcount = (hex_intersect_popcount[high_nibble|hex_fp[0]] +
                               hex_intersect_popcount[low_nibble|hex_fp[1]]);
    hex_fp += 2;

    check_word |= byte_intersect_popcount;
    union_popcount += byte_union_popcount;
    intersect_popcount += byte_intersect_popcount;
    len--;
  }
  if (check_word >= 16) {
    return -1.0;
  }
  /* Special case define that 0/0 = 0.0. It's hard to decide what to 
         use here, for example, OpenEye uses 1.0. It seems that 0.0
     is the least surprising choice. */
  if (union_popcount == 0) {
    return 0.0;
  }
  return (intersect_popcount + 0.0) / union_popcount;  /* +0.0 to coerce to double */
}

/* Return the Tversky between a byte fingerprint and a hex fingerprint */
/* The size is the number of bytes in the byte_fp */
double chemfp_byte_hex_tversky(ssize_t len,
                               const unsigned char *byte_fp,
                               const char *shex_fp,
			       double alpha, double beta) {
  const unsigned char *hex_fp = (unsigned char *) shex_fp;
  int scaled_alpha = (int)lrint(alpha * CHEMFP_FLOAT_SCALE);
  int scaled_beta = (int)lrint(beta * CHEMFP_FLOAT_SCALE);
  int check_word=0;
  int A=0, B=0, c=0;
  int byte_intersect_popcount, denominator;
  unsigned char byte;
  int high_nibble, low_nibble;

  while (len > 0) {
    byte = *byte_fp++;
    /* Construct 12 bit words with a nibble from the byte and character from the hex */
    high_nibble = (byte & 0xf0) << 4;
    low_nibble = (byte & 0xf) << 8;

    A += byte_popcounts[byte];
    B += hex_to_popcount[hex_fp[0]] + hex_to_popcount[hex_fp[1]];
    byte_intersect_popcount = (hex_intersect_popcount[high_nibble|hex_fp[0]] +
                               hex_intersect_popcount[low_nibble|hex_fp[1]]);
    hex_fp += 2;

    check_word |= byte_intersect_popcount;
    c += byte_intersect_popcount;
    len--;
  }
  if (check_word >= 16) {
    return -1.0;
  }
  /* Special case for when neither fingerprint has any bytes set */
  if (!A && !B) {
    return 0.0;
  }
  denominator = (scaled_alpha*A + scaled_beta*B
		 + c*(CHEMFP_FLOAT_SCALE-scaled_alpha-scaled_beta));
  if (denominator == 0) {
    /* We already handled the alpha=beta=0.0 case. */
    /* By definition, make this be 0.0. */
    return 0.0;
  }
  return ((double) (c * CHEMFP_FLOAT_SCALE)) / denominator;
}
double chemfp_byte_hex_tversky_scaled(
	ssize_t len,
	const unsigned char *byte_fp,
	const char *shex_fp,
	int scaled_alpha, int scaled_beta) {
  const unsigned char *hex_fp = (unsigned char *) shex_fp;
  int check_word=0;
  int A=0, B=0, c=0;
  int byte_intersect_popcount, denominator;
  unsigned char byte;
  int high_nibble, low_nibble;

  while (len > 0) {
    byte = *byte_fp++;
    /* Construct 12 bit words with a nibble from the byte and character from the hex */
    high_nibble = (byte & 0xf0) << 4;
    low_nibble = (byte & 0xf) << 8;

    A += byte_popcounts[byte];
    B += hex_to_popcount[hex_fp[0]] + hex_to_popcount[hex_fp[1]];
    byte_intersect_popcount = (hex_intersect_popcount[high_nibble|hex_fp[0]] +
                               hex_intersect_popcount[low_nibble|hex_fp[1]]);
    hex_fp += 2;

    check_word |= byte_intersect_popcount;
    c += byte_intersect_popcount;
    len--;
  }
  if (check_word >= 16) {
    return -1.0;
  }
  /* Special case for when neither fingerprint has any bytes set */
  if (!A && !B) {
    return 0.0;
  }
  denominator = (scaled_alpha*A + scaled_beta*B
		 + c*(CHEMFP_FLOAT_SCALE-scaled_alpha-scaled_beta));
  if (denominator == 0) {
    /* We already handled the alpha=beta=0.0 case. */
    /* By definition, make this be 0.0. */
    return 0.0;
  }
  return ((double) (c * CHEMFP_FLOAT_SCALE)) / denominator;
}
