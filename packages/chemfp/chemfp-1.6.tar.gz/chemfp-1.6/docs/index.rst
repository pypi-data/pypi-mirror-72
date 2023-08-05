.. _intro:

########################
chemfp 1.6 documentation
########################

`chemfp <http://chemfp.com/>`_ is a set of tools for working with
cheminformatics fingerprints in the FPS format.

This is the documentation for the no-cost/free software/open source
version of chemfp. To see the documentation for the commercial version
of chemfp, go to `http://chemfp.readthedocs.io/
<http://chemfp.readthedocs.io/>`_.

The commercial version is 20-50% faster than chemfp 1.6 on modern
hardware, has an improved API for web applications development,
supports the FPB binary format for fast loading, implements Tversky
similarity search, runs on Python 3, and much more.

**Chemfp 1.6 only supports Python 2.7.** It is still being maintained,
primarily to provide a baseline for similarity search benchmarking. If
a new search implementation is not faster than chemfp 1.6 then it
cannot be considered "high-performance", nor can its search algorithm
be considered an improvement over Swamidass and Baldi's BitBound
algorithm.

Note: If you are benchmarking chemfp, ask me for an evaluation license
so you can include chemfp 3 timings. If you are benchmarking free
software/open source methods, let me know as I may be able to optimize
chemfp 1.6 for your test case.

Chemfp 1.6 also exists for those decreasing number of people who are
still using Python 2.7. As they likely know, Python 2.7 has reached
its end-of-life and is no longer supported by the core Python
developers. Several vendors offer extended support for Python
2.7. Furthermore, I can provide some help to compile Python 2.7 for
those people who want to benchmark chemfp 1.6.

Most people will use the command-line programs to generate and search
fingerprint files. :ref:`ob2fps <ob2fps>`, :ref:`oe2fps <oe2fps>`, and
:ref:`rdkit2fps <rdkit2fps>` use respectively the `Open Babel
<http://openbabel.org/>`_, `OpenEye <http://www.eyesopen.com/>`_, and
`RDKit <http://www.rdkit.org/>`_ chemistry toolkits to convert
structure files into fingerprint files. :ref:`sdf2fps <sdf2fps>`
extracts fingerprints encoded in SD tags to make the fingerprint
file. :ref:`simsearch <simsearch>` finds targets in a fingerprint file
which are sufficiently similar to the queries. :ref:`fpcat <fpcat>`
can be used to merge fingerprint files.

Be aware that all of those those vendors dropped Python 2.7 support
by 2019. Use the commercial version of chemfp if you need to generate
fingerprints using those toolkits.

The programs are built using the :ref:`chemfp Python library API <chemfp-api>`,
which in turn uses a C extension for the performance
critical sections. The parts of the library API documented here are
meant for public use, and include examples.


Remember: chemfp cannot generate fingerprints from a structure file
without a third-party chemistry toolkit.

Chemfp 1.6 was released on 23 June 2020. It supports Python 2.7 and can
be used with any historic version of OEChem/OEGraphSim, Open Babel, or
RDKit which supports Python 2.7. Python 3 support is available in the
commerical version of chemfp. If you are interested in paying for a
copy, send an email to sales@dalkescientific.com .

To cite chemfp use: Dalke, A. The chemfp project. J Cheminform 11, 76
(2019). https://doi.org/10.1186/s13321-019-0398-8 .


.. toctree::
   :caption: Table of Contents

   installing
   using-tools
   tool-help
   using-api
   api
   whatsnew

*************************
License and advertisement
*************************

This program was developed by Andrew Dalke
<dalke@dalkescientific.com>, Andrew Dalke Scientific, AB. It is
distributed free of charge under the "MIT" license, shown below.

Further chemfp development depends on funding from people like
you. Asking for voluntary contributions almost never works. Instead,
starting with chemfp 1.1, there are two development tracks. You can
download and use the no-cost version or you can pay money to get
access to the commercial version.

This is the no-cost/free software version, available under the MIT
license.

The commerical version, currently chemfp 3.4, is available under
several different licenses, including 1) a no-cost evaluation license
for a pre-compiled package for Linux-based OSs, 2) source
code-available licenses for internal use, and 3) a full source code
license under the MIT license.

I'll stress that: the commercial version of chemfp is available under
an open source license, although that is the most expensive
option.

The current commercial version is 3.4. It can handle more than 4GB of
fingerprint data, it supports the FPB binary fingerprint format for
fast loading, it has an expanded API designed for web server and web
services development (for example, reading and writing from strings,
not just files), it supports both Python 2.7 and Python 3.5 or later,
and it has faster similarity search performance. Note: chemfp 3.4 is
the last version of the commercial chemfp track to support Python 2.7.

If you pay for the commercial distribution then you will get the most
recent version of chemfp, free upgrades for one year, support, and a
discount on renewing participation in the incentive program.

If you have questions about or with to purchase the commercial
distribution, send an email to sales@dalkescientific.com .


.. highlight:: none

::

  Copyright (c) 2010-2020 Andrew Dalke Scientific, AB (Sweden)
  
  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:
  
  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright to portions of the code are held by other people or
organizations, and may be under a different license. See the specific
code for details. These are:

 - OpenMP, cpuid, POPCNT, and Lauradoux implementations by Kim
   Walisch, <kim.walisch@gmail.com>, under the MIT license
 - SSSE3.2 popcount implementation by Stanford University (written by
   Imran S. Haque <ihaque@cs.stanford.edu>) under the BSD license
 - heapq by the Python Software Foundation under the Python license
 - TimSort code by Christopher Swenson under the MIT License
 - tests/unittest2 by Steve Purcell, the Python Software Foundation,
   and others, under the Python license
 - chemfp/rdmaccs.patterns and chemfp/rdmaccs2.patterns by Rational
   Discovery LLC, Greg Landrum, and Julie Penzotti, under the 3-Clause
   BSD License
 - chemfp/argparse.py by Steven J. Bethard under the Apache License 2.0 
 - chemfp/progressbar/ by Nilton Volpato under the LGPL 2.1 and/or BSD license
 - chemfp/futures/ by Brian Quinlan under the Python license

(Note: the last three modules are not part of the public API and were
removed in chemfp 3.1.)


******
Future
******

The chemfp code base is solid and in use at many companies, some of
whom have paid for the commercial version. It has great support for
fingerprint generation, fast similarity search, and multiple
cheminformatics toolkits.

There are two tracks for improvements. Most of the new feature
development is done in the commerical version of chemfp. I make my
living in part by selling software, and few people will pay for
software they can get for free.

The chemfp 1.x track is maintained only to provide a good reference
baseline for benchmarking other similarity search tools. It only
supports Python 2.7.

I will also accept contributions to chemfp. These must be under the
MIT license or similarly unrestrictive license so I can include it in
both the no-cost and commercial versions of chemfp.


*******
 Thanks
*******

In no particular order, the following contributed to chemfp in some
way: Noel O'Boyle, Geoff Hutchison, the Open Babel developers, Greg
Landrum, OpenEye, Roger Sayle, Phil Evans, Evan Bolton, Wolf-Dietrich
Ihlenfeldt, Rajarshi Guha, Dmitry Pavlov, Roche, Kim Walisch, Daniel
Lemire, Nathan Kurz, Chris Morely, Jörg Kurt Wegner, Phil Evans, Björn
Grüning, Andrew Henry, Brian McClain, Pat Walters, Brian Kelley,
Lionel Uran Landaburu, and Sereina Riniker.

Thanks also to my wife, Sara Marie, for her many years of support.


*******************
 Indices and tables
*******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

