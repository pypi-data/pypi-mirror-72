.. highlight:: pycon

=========================
The chemfp Python library
=========================

The chemfp command-line programs use a Python library called
chemfp. Portions of the API are in flux and subject to change. The
stable portions of the API which are open for general use are
documented in :ref:`chemfp-api`.

The API includes:

 - low-level Tanimoto and popcount operations
 - Tanimoto search algorithms based on threshold and/or k-nearest neighbors
 - a cross-toolkit interface for reading fingerprints from a structure file

The following chapters give examples of how to use the API.

Byte and hex fingerprints
=========================

In this section you'll learn how chemfp stores fingerprints and some
of the low-level bit operations on those fingerprints.

chemfp stores fingerprints as byte strings. Here are two 8 bit
fingerprints::

    >>> fp1 = "A"
    >>> fp2 = "B"

The :ref:`chemfp.bitops <chemfp.bitops>` module contains functions which work on byte
fingerprints. Here's the Tanimoto of those two fingerprints::

    >>> from chemfp import bitops
    >>> bitops.byte_tanimoto(fp1, fp2)
    0.33333333333333331

To understand why, you have to know that ASCII character "A" has the
value 65, and "B" has the value 66. The bit representation is::

     "A" = 01000001   and   "B" = 01000010

so their intersection has 1 bit and the union has 3, giving a Tanimoto
of 1/3 or 0.33333333333333331 when represented as a 64 bit floating
point number on the computer.

You can compute the Tanimoto between any two byte strings with the
same length, as in::

    >>> bitops.byte_tanimoto("apples&", "oranges")
    0.58333333333333337

You'll get a chemfp exception if they have different lengths.

.. highlight:: none

Most fingerprints are not as easy to read as the English ones I showed
above. They tend to look more like::


    P1@\x84K\x1aN\x00\n\x01\xa6\x10\x98\\\x10\x11

which is hard to read. I usually show hex-encoded fingerprints. The above
fingerprint in hex is::

    503140844b1a4e000a01a610985c1011

.. highlight:: pycon 

which is simpler to read, though you still need to know your hex
digits. There are two ways to hex-encode a byte string. I suggest
using chemfp's :func:`.hex_encode` function::
  
    >>> bitops.hex_encode("P1@\x84K\x1aN\x00\n\x01\xa6\x10\x98\\\x10\x11")
    '503140844b1a4e000a01a610985c1011'

Older versions of chemfp recommended using the s.encode() method of strings::

     >>> "P1@\x84K\x1aN\x00\n\x01\xa6\x10\x98\\\x10\x11".encode("hex")
     '503140844b1a4e000a01a610985c1011'

However, this will not work on Python 3. That version of Python
distinguishes between text/Unicode strings and byte strings. There is
no "hex" encoding for text strings, and byte strings do not implement
the "encode()" method.

Use chemfp's :func:`.hex_decode` function to decode a hex string to
a fingerprint byte string.

The bitops module includes other low-level functions which work on
byte fingerprints, as well as corresponding functions which work on
hex fingerprints. (Hex-encoded fingerprints are decidedly second-class
citizens in chemfp, but they are citizens.)


Fingerprint collections and metadata
====================================

In this section you'll learn the basic operations on a fingerprint
collection and the fingerprint metadata.

A fingerprint record is the fingerprint plus an identifier. In chemfp,
a fingerprint collection is a object which contains fingerprint
records and which follows the common API providing access to those
records.

That's rather abstract, so let's work with a few real examples. You'll
need to create a copy of the "pubchem_targets.fps" file generated in
:ref:`pubchem_fingerprints` in order to follow along.

Here's how to open an FPS file::

    >>> import chemfp
    >>> reader = chemfp.open("pubchem_targets.fps")

Every fingerprint collection has a metadata attribute with details
about the fingerprints. It comes from the header of the FPS file. You
can view the metadata in Python repr format:

    >>> reader.metadata
    Metadata(num_bits=881, num_bytes=111,
    type=u'CACTVS-E_SCREEN/1.0 extended=2', aromaticity=None,
    sources=[u'Compound_048500001_049000000.sdf.gz'],
    software=u'CACTVS/unknown', date='2020-05-06T12:40:32')
    
but I think it's easier to view it in string format, which matches the
format of the FPS header:

    >>> print reader.metadata
    #num_bits=881
    #type=CACTVS-E_SCREEN/1.0 extended=2
    #software=CACTVS/unknown
    #source=Compound_048500001_049000000.sdf.gz
    #date=2020-05-06T12:40:32

All fingerprint collections support iteration. Each step of the
iteration returns the fingerprint identifier and its score. Since I
know the 6th record has the id 48500164, I can write a simple loop
which stops with that record::

    >>> from chemfp.bitops import hex_encode
    >>> for (id, fp) in reader:
    ...   print id, "starts with", hex_encode(fp)[:20]
    ...   if id == "48500164":
    ...     break
    ...
    48500020 starts with 07de0500000000000000
    48500053 starts with 07de0c00000000000000
    48500091 starts with 07de8c00000000000000
    48500092 starts with 07de0d00020000000000
    48500110 starts with 075e0c00000000000000
    48500164 starts with 07de0c00000000000000

Fingerprint collections also support iterating via arenas, and several
support Tanimoto search functions.


FingerprintArena
================

In this section you'll learn about the FingerprintArena fingerprint
collection and how to iterate through arenas in a collection.

The FPSReader reads through or searches a fingerprint file once. If
you want to read the file again you have to reopen it.

Reading from disk is slow, and the FPS format is designed for
ease-of-use and not performance. If you want to do many queries then
it's best to store everything in memory. The
:class:`.FingerprintArena` is a
fingerprint collection which does that.

Here's how to load fingerprints into an arena::

    >>> import chemfp
    >>> arena = chemfp.load_fingerprints("pubchem_targets.fps")
    >>> print arena.metadata
    #num_bits=881
    #type=CACTVS-E_SCREEN/1.0 extended=2
    #software=CACTVS/unknown
    #source=Compound_048500001_049000000.sdf.gz
    #date=2020-05-06T12:40:32

This implements the fingerprint collection API, so you can do things
like iterate over an arena and get the id/fingerprint pairs.::

    >>> from chemfp import bitops
    >>> for id, fp in arena:
    ...     print id, "with popcount", bitops.byte_popcount(fp)
    ...     if id == "48656867":
    ...         break
    ... 
    48942244 with popcount 33
    48941399 with popcount 39
    48940284 with popcount 40
    48943050 with popcount 40
    48656359 with popcount 41
    48656867 with popcount 42

If you look closely you'll notice that the fingerprint record order
has changed from the previous section, and that the population counts
are suspiciously non-decreasing. By default :func:`.load_fingerprints`
reorders the fingerprints into a data structure which is faster to
search, although you can disable that if you want the fingerprints to
be the same as the input order.

The :class:`.FingerprintArena` has new capabilities. You can ask it
how many fingerprints it contains, get the list of identifiers, and
look up a fingerprint record given an index, as in::

    >>> len(arena)
    14967
    >>> arena.ids[:5]
    ['48942244', '48941399', '48940284', '48943050', '48656359']
    >>> id, fp = arena[6]
    >>> id
    '48839855'
    >>> arena[-1][0]
    '48985180'
    >>> bitops.byte_popcount(arena[-1][1])
    253

An arena supports iterating through subarenas. This is like having a
long list and being able to iterate over sublists. Here's an example
of iterating over the arena to get subarenas of size 1000 (the last
subarea may have fewer elements), and print information about each
subarena.::

    >>> for subarena in arena.iter_arenas(1000):
    ...   print subarena.ids[0], len(subarena)
    ... 
    48942244 1000
    48867092 1000
    48629741 1000
    48795302 1000
    48848217 1000
    48689418 1000
    48873983 1000
    48503654 1000
    48575094 1000
    48575460 1000
    48531270 1000
    48960181 1000
    48806978 1000
    48837835 1000
    48584671 967
    >>> arena[0][0]
    '48942244'
    >>> arena[1000][0]
    '48867092'

To help demonstrate what's going on, I showed the first id of each
record along with the main arena ids for records 0 and 1000, so you
can verify that they are the same.

Arenas are a core part of chemfp. Processing one fingerprint at a time
is slow, so the main search routines expect to iterate over query
arenas, rather than query fingerprints.

Thus, the FPSReaders -- and all chemfp fingerprint collections -- also
support the :func:`.iter_arenas` interface. Here's an example of reading the
targets file 2000 records at a time::

    >>> queries = chemfp.open("pubchem_queries.fps")
    >>> for arena in queries.iter_arenas(2):
    ...   print len(arena)
    ...
    2000
    2000
    2000
    2000
    2000
    826

Those add up to 10,826, which you can verify is the number of
structures in the original source file.

If you have a :class:`.FingerprintArena` instance then you can also
use Python's slice notation to make a subarena::

    >>> queries = chemfp.load_fingerprints("pubchem_queries.fps")
    >>> queries[10:15]
    <chemfp.arena.FingerprintArena object at 0x552c10>
    >>> queries[10:15].ids
    ['99110546', '99110547', '99123452', '99123453', '99133437']
    >>> queries.ids[10:15]
    ['99110546', '99110547', '99123452', '99123453', '99133437']

The big restriction is that slices can only have a step size
of 1. Slices like `[10:20:2]` and `[::-1]` aren't supported. If you
want something like that then you'll need to make a new arena instead
of using a subarena slice.

In case you were wondering, yes, you can use `iter_arenas` or the other
FingerprintArena methods on a subarena::

    >>> queries[10:15][1:3].ids
    ['99110547', '99123452']
    >>> queries.ids[11:13]
    ['99110547', '99123452']



How to use query fingerprints to search for similar target fingerprints
=======================================================================

In this section you'll learn how to do a Tanimoto search using the
previously created PubChem fingerprint files for the queries and the
targets.

It's faster to search an arena, so I'll load the target fingerprints:

    >>> import chemfp
    >>> targets = chemfp.load_fingerprints("pubchem_targets.fps")
    >>> len(targets)
    14967

and open the queries as an FPSReader.

    >>> queries = chemfp.open("pubchem_queries.fps")

I'll use :func:`.threshold_tanimoto_search` to find, for each query,
all hits which are at least 0.7 similar to the query.

    >>> for (query_id, hits) in chemfp.threshold_tanimoto_search(queries, targets, threshold=0.7):
    ...   print query_id, len(hits), list(hits)[:2]
    ... 
    99000039 641 [(3619, 0.7085714285714285), (4302, 0.7371428571428571)]
    99000230 373 [(2747, 0.703030303030303), (3608, 0.7041420118343196)]
    99002251 270 [(2512, 0.7006369426751592), (2873, 0.7088607594936709)]
    99003537 523 [(6697, 0.7230769230769231), (7478, 0.7085427135678392)]
    99003538 523 [(6697, 0.7230769230769231), (7478, 0.7085427135678392)]
    99005028 131 [(772, 0.7589285714285714), (796, 0.7522123893805309)]
    99005031 131 [(772, 0.7589285714285714), (796, 0.7522123893805309)]
    99006292 308 [(805, 0.7058823529411765), (808, 0.7)]
    99006293 308 [(805, 0.7058823529411765), (808, 0.7)]
    99006597 0 []
          # ... many lines omitted ...

I'm only showing the first two hits for the sake of space. It seems
rather pointless, after all, to show all 641 hits of query id 99000039.

What you don't see is that the implementation uses the iter_arenas()
interface on the queries so that it processes only a subarena at a
time. There's a tradeoff between a large arena, which is faster
because it doesn't often go back to Python code, or a small arena,
which uses less memory and is more responsive. You can change the
tradeoff using the *arena_size* parameter.


If all you care about is the count of the hits within a given
threshold then use :func:`chemfp.count_tanimoto_hits`::

    >>> queries = chemfp.open("pubchem_queries.fps")
    >>> for (query_id, count) in chemfp.count_tanimoto_hits(queries, targets, threshold=0.7):
    ...     print query_id, count
    ... 
    99000039 641
    99000230 373
    99002251 270
    99003537 523
    99003538 523
    99005028 131
    99005031 131
    99006292 308
    99006293 308
    99006597 0
         # ... many lines omitted ...

Or, if you only want the k=2 nearest neighbors to each target within
that same threshold of 0.7 then use
:func:`chemfp.knearest_tanimoto_search`::

    >>> queries = chemfp.open("pubchem_queries.fps")
    >>> for (query_id, hits) in chemfp.knearest_tanimoto_search(queries, targets, k=2, threshold=0.7):
    ...     print query_id, list(hits)
    ... 
    99000039 [(10706, 0.8784530386740331), (10551, 0.8729281767955801)]
    99000230 [(8201, 0.8588235294117647), (10267, 0.8522727272727273)]
    99002251 [(6939, 0.8109756097560976), (8628, 0.8106508875739645)]
    99003537 [(13023, 0.9035532994923858), (12924, 0.8984771573604061)]
    99003538 [(13023, 0.9035532994923858), (12924, 0.8984771573604061)]
    99005028 [(906, 0.8288288288288288), (1746, 0.8166666666666667)]
         # ... many lines omitted ...



How to search an FPS file
=========================

In this section you'll learn how to search an FPS file directly,
without loading it into a FingerprintArena.

The previous example loaded the fingerprints into a
FingerprintArena. That's the fastest way to do multiple
searches. Sometimes though you only want to do one or a couple of
queries. It seems rather excessive to read the entire targets file
into an in-memory data structure before doing the search when you
could search will processing the file.

For that case, use an FPSReader as the target file. Here I'll get the
first two records from the queries file and use them to search the
targets file::

    >>> query_arena = next(chemfp.open("pubchem_queries.fps").iter_arenas(2))

This line opens the file, iterates over its fingerprint records, and
return the two as an arena. Perhaps a slightly less confusing way to
write the above is::

    >>> for query_arena in chemfp.open("pubchem_queries.fps").iter_arenas(1):
    ...   break

Here are the k=5 closest hits against the targets file::

    >>> targets = chemfp.open("pubchem_targets.fps")
    >>> for query_id, hits in chemfp.knearest_tanimoto_search(query_arena, targets, k=5, threshold=0.0):
    ...   print "Hits for", query_id
    ...   for hit in hits:
    ...     print "", hit
    ... 
    Hits for 99000039
     ('48503376', 0.8784530386740331)
     ('48503380', 0.8729281767955801)
     ('48732162', 0.8595505617977528)
     ('48520532', 0.8540540540540541)
     ('48985130', 0.8449197860962567)
    Hits for 99000230
     ('48563034', 0.8588235294117647)
     ('48731730', 0.8522727272727273)
     ('48583483', 0.8411764705882353)
     ('48563042', 0.8352941176470589)
     ('48935653', 0.8333333333333334)

Remember that the FPSReader is based on reading an FPS file. Once
you've done a search, the file is read, and you can't do another
search. You'll need to reopen the file.

Each search processes *arena_size* query fingerprints at a time. You
will need to increase that value if you want to search more than that
number of fingerprints with this method. The search performance
tradeoff between a FPSReader search and loading the fingerprints into
a FingerprintArena occurs with under 10 queries, so there should be
little reason to worry about this.


FingerprintArena searches returning indices instead of ids
===========================================================

In this section you'll learn how to search a FingerprintArena and use
hits based on integer indices rather than string ids.

The previous sections used a high-level interface to the Tanimoto
search code. Those are designed for the common case where you just
want the query id and the hits, where each hit includes the target id.

Working with strings is actually rather inefficient in both speed and
memory. It's usually better to work with indices if you can, and in
the next section I'll show how to make a distance matrix using this
interface.

The index-based search functions are in the :mod:`chemfp.search` module.
They can be categorized into three groups:

  1. Count the number of hits:

    * :func:`chemfp.search.count_tanimoto_hits_fp` - search an arena using a single fingerprint

    * :func:`chemfp.search.count_tanimoto_hits_arena` - search an arena using an arena

    * :func:`chemfp.search.count_tanimoto_hits_symmetric` - search an arena using itself

  2. Find all hits at or above a given threshold, sorted arbitrarily:

    * :func:`chemfp.search.threshold_tanimoto_search_fp` - search an arena using a single fingerprint

    * :func:`chemfp.search.threshold_tanimoto_search_arena` - search an arena using an arena

    * :func:`chemfp.search.threshold_tanimoto_search_symmetric` - search an arena using itself


  3. Find the k-nearest hits at or above a given threshold, sorted by decreasing similarity:

    * :func:`chemfp.search.knearest_tanimoto_search_fp` - search an arena using a single fingerprint

    * :func:`chemfp.search.knearest_tanimoto_search_arena` - search an arena using an arena

    * :func:`chemfp.search.knearest_tanimoto_search_symmetric` - search an arena using itself

The functions ending '_fp' take a query fingerprint and a target
arena. The functions ending '_arena' take a query arena and a target
arena. The functions ending '_symmetric' use the same arena as both
the query and target.

In the following example, I'll use the first 5 fingerprints of a data
set to search the entire data set. To do this, I load the data set as
an arena, read the 5 records of the same file as a query arena, and do
the search.

    >>> import chemfp
    >>> from chemfp import search
    >>> targets = chemfp.load_fingerprints("pubchem_queries.fps")
    >>> queries = next(chemfp.open("pubchem_queries.fps").iter_arenas(5))
    >>> results = search.threshold_tanimoto_search_arena (queries, targets, threshold=0.7)

The threshold_tanimoto_search_arena search finds the target
fingerprints which have a similarity score of at least 0.7 compared to
the query.

You can iterate over the results to get the list of hits for each of
the queries. The order of the results is the same as the order of the
records in the query.::

    >>> for hits in results:
    ...   print len(hits), hits.get_ids_and_scores()[:3]
    ...
    261 [('99115962', 0.7005649717514124), ('99115963', 0.7005649717514124), ('99103967', 0.7303370786516854)]
    281 [('99141183', 0.7202380952380952), ('99174339', 0.7017543859649122), ('99275524', 0.7093023255813954)]
    118 [('99123562', 0.7564102564102564), ('99104138', 0.7080745341614907), ('99104141', 0.7080745341614907)]
    223 [('99121080', 0.7591623036649214), ('99210542', 0.7106598984771574), ('99210544', 0.7106598984771574)]
    223 [('99121080', 0.7591623036649214), ('99210542', 0.7106598984771574), ('99210544', 0.7106598984771574)]

This result is like what you saw earlier, except that it doesn't have
the query id. You can get that from the arena's `id` attribute, which
contains the list of fingerprint identifiers.

    >>> for query_id, hits in zip(queries.ids, results):
    ...   print "Hits for", query_id
    ...   for hit in hits.get_ids_and_scores()[:3]:
    ...     print "", hit
    Hits for 99000039
    ('99115962', 0.7005649717514124)
    ('99115963', 0.7005649717514124)
    ('99103967', 0.7303370786516854)
    Hits for 99000230
    ('99141183', 0.7202380952380952)
    ('99174339', 0.7017543859649122)
    ('99275524', 0.7093023255813954)
    Hits for 99002251
       ...

What I really want to show is that you can get the same data only
using the offset index for the target record instead of its id. The
result from a Tanimoto search is a :class:`.SearchResults`
instance, with methods that include
:meth:`SearchResults.get_indices_and_scores`,
:meth:`SearchResults.get_ids`, and :meth:`SearchResults.get_scores`::

  >>> for hits in results:
  ...   print len(hits), hits.get_indices_and_scores()[:3]
  ... 
  261 [(2998, 0.7005649717514124), (2999, 0.7005649717514124), (3816, 0.7303370786516854)]
  281 [(2953, 0.7202380952380952), (3162, 0.7017543859649122), (3543, 0.7093023255813954)]
  118 [(2491, 0.7564102564102564), (2584, 0.7080745341614907), (2585, 0.7080745341614907)]
  223 [(5509, 0.7591623036649214), (5793, 0.7106598984771574), (5794, 0.7106598984771574)]
  223 [(5509, 0.7591623036649214), (5793, 0.7106598984771574), (5794, 0.7106598984771574)]
  >>> 
  >>> targets.ids[0]
  '99116624'
  >>> targets.ids[3]
  '99116668'
  >>> targets.ids[15]
  '99134597'

I did a few id lookups given the target dataset to show you that the
index corresponds to the identifiers from the previous code.

These examples iterated over each individual :class:`SearchResult` to
fetch the ids and scores, or indices and scores. Another possibility
is to ask the `SearchResults` collection to iterate directly over the
list of fields you want.

  >>> for row in results.iter_indices_and_scores():
  ...   print len(row), row[:3]
  ...
  261 [(2998, 0.7005649717514124), (2999, 0.7005649717514124), (3816, 0.7303370786516854)]
  281 [(2953, 0.7202380952380952), (3162, 0.7017543859649122), (3543, 0.7093023255813954)]
  118 [(2491, 0.7564102564102564), (2584, 0.7080745341614907), (2585, 0.7080745341614907)]
  223 [(5509, 0.7591623036649214), (5793, 0.7106598984771574), (5794, 0.7106598984771574)]
  223 [(5509, 0.7591623036649214), (5793, 0.7106598984771574), (5794, 0.7106598984771574)]

This was added to get a bit more performance out of chemfp and because
the API is sometimes cleaner one way and sometimes cleaner than the
other. Yes, I know that the Zen of Python recommends that "there
should be one-- and preferably only one --obvious way to do it." Oh
well.


Computing a distance matrix for clustering
==========================================

In this section you'll learn how to compute a distance matrix using
the chemfp API.

chemfp does not do clustering. There's a huge number of tools which
already do that. A goal of chemfp in the future is to provide some
core components which clustering algorithms can use.

That's in the future. Right now you can use the following to build a
distance matrix and pass that to one of those tools.

Since we're using the same fingerprint arena for both queries and
targets, we know the distance matrix will be symmetric along the
diagonal, and the diagonal terms will be 1.0. The
:func:`chemfp.search.threshold_tanimoto_search_symmetric` functions can take
advantage of the symmetry for a factor of two performance
gain. There's also a way to limit it to just the upper triangle, which
gives a factor of two memory gain as well.


Most of those tools use `NumPy <http://numpy.scipy.org/>`_, which is a
popular third-party package for numerical computing. You will need to
have it installed for the following to work.

.. highlight:: python 

::

  import numpy  # NumPy must be installed
  from chemfp import search
  
  # Compute distance[i][j] = 1-Tanimoto(fp[i], fp[j])
  
  def distance_matrix(arena):
      n = len(arena)
      
      # Start off a similarity matrix with 1.0s along the diagonal
      similarities = numpy.identity(n, "d")
      
      ## Compute the full similarity matrix.
      # The implementation computes the upper-triangle then copies
      # the upper-triangle into lower-triangle. It does not include
      # terms for the diagonal.
      results = search.threshold_tanimoto_search_symmetric(arena, threshold=0.0)
      
      # Copy the results into the NumPy array.
      for row_index, row in enumerate(results.iter_indices_and_scores()):
          for target_index, target_score in row:
              similarities[row_index, target_index] = target_score
      
      # Return the distance matrix using the similarity matrix
      return 1.0 - similarities


Once you've computed the distance matrix, clustering is easy. I
installed the `hcluster <http://code.google.com/p/scipy-cluster/>`_
package, as well as `matplotlib <http://matplotlib.sourceforge.net/>`_,
then ran the following to see the hierarchical clustering::

  import chemfp
  import hcluster # Clustering package from http://code.google.com/p/scipy-cluster/
  
  # ... insert the 'distance_matrix' function definition here ...
  
  dataset = chemfp.load_fingerprints("pubchem_queries.fps")
  distances  = distance_matrix(dataset)
  
  linkage = hcluster.linkage(distances, method="single", metric="euclidean")
  
  # Plot using matplotlib, which you must have installed
  hcluster.dendrogram(linkage, labels=dataset.ids)
  
  import pylab
  pylab.show()

In practice you'll almost certainly want to use one of the `scikit-learn clustering algorithms
<http://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster>`_.


Convert SearchResults to a SciPy csr matrix
===========================================

In this section you'll learn how to convert a SearchResults object
into a SciPy compressed sparse row matrix.

In the previous section you learned how to use the chemfp API to
create a NumPy similarity matrix, and convert that into a distance
matrix. The result is a dense matrix, and the amount of memory goes as
the square of the number of structures.

If you have a reasonably high similarity threshold, like 0.7, then
most of the similarity scores will be zero. Internally the
:class:`.SearchResults` object only stores the non-zero values for
each row, along with an index to specify the column. This is a common
way to compress sparse data.

SciPy has its own
`compressed sparse row ("csr") matrix
<https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html>`_
data type, which can be used as input to many of the
`scikit-learn clustering algorithms
<http://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster>`_.

If you want to use those algorithms, call the
:meth:`.SearchResults.to_csr` method to convert the SearchResults
scores (and only the scores) into a csr matrix. The rows will be in
the same order as the SearchResult (and the original queries), and
the columns will be in the same order as the target arena, including
its ids.

I don't know enough about scikit-learn to give a useful example. (If
you do, let me know!) Instead, I'll start by doing an NxM search of
two sets of fingerprints::

  from __future__ import print_function
  import chemfp
  from chemfp import search
  
  queries = chemfp.load_fingerprints("pubchem_queries.fps")
  targets = chemfp.load_fingerprints("pubchem_targets.fps")
  results = search.threshold_tanimoto_search_arena(queries, targets, threshold = 0.8)

.. highlight:: pycon

The SearchResults attribute :attr:`~.SearchResults.shape` describes the
number of rows and columns::
  
  >>> results.shape
  (10826, 14967)
  >>> len(queries)
  10826
  >>> len(targets)
  14967
  >>> results[2001].get_indices_and_scores()
  [(2031, 0.8770491803278688), (2032, 0.8770491803278688)]

I'll turn it into a SciPy csr::

  >>> csr = results.to_csr()
  >>> csr
  <10826x14967 sparse matrix of type '<type 'numpy.float64'>'
      with 369471 stored elements in Compressed Sparse Row format>
  >>> csr.shape
  (10826, 14967)

and look at the same row to show it has the same indices and scores::

  >>> csr[2001]
  <1x14967 sparse matrix of type '<type 'numpy.float64'>'
      with 2 stored elements in Compressed Sparse Row format>
  >>> csr[2001].indices
  array([2031, 2032], dtype=int32)
  >>> csr[2001].data
  array([0.87704918, 0.87704918])

Taylor-Butina clustering
========================

For the last clustering example, here's my (non-validated) variation
of the `Butina algorithm from JCICS 1999, 39, 747-750 <http://www.chemomine.co.uk/dbclus-paper.pdf>`_.
See also http://www.redbrick.dcu.ie/~noel/R_clustering.html . You
might know it as Leader clustering.

.. highlight:: python 

First, for each fingerprint find all other fingerprints with a
threshold of 0.8::

  import chemfp
  from chemfp import search
  
  arena = chemfp.load_fingerprints("pubchem_targets.fps")
  results = search. threshold_tanimoto_search_symmetric (arena, threshold = 0.8)


Sort the results so that fingerprints with more hits come first. This
is more likely to be a cluster centroid. Break ties arbitrarily by the
fingerprint id; since fingerprints are ordered by the number of bits
this likely makes larger structures appear first.::

  # Reorder so the centroid with the most hits comes first.
  # (That's why I do a reverse search.)
  # Ignore the arbitrariness of breaking ties by fingerprint index
  results = sorted( (  (len(indices), i, indices)
                            for (i,indices) in enumerate(results.iter_indices())  ),
                    reverse=True)


Apply the leader algorithm to determine the cluster centroids and the singletons::


  # Determine the true/false singletons and the clusters
  true_singletons = []
  false_singletons = []
  clusters = []
  
  seen = set()
  for (size, fp_idx, members) in results:
      if fp_idx in seen:
          # Can't use a centroid which is already assigned
          continue
      seen.add(fp_idx)
  
      # Figure out which ones haven't yet been assigned
      unassigned = set(members) - seen
  
      if not unassigned:
          false_singletons.append(fp_idx)
          continue
      
      # this is a new cluster
      clusters.append( (fp_idx, unassigned) )
      seen.update(unassigned)

Once done, report the results::

  print len(true_singletons), "true singletons"
  print "=>", " ".join(sorted(arena.ids[idx] for idx in true_singletons))
  print
  
  print len(false_singletons), "false singletons"
  print "=>", " ".join(sorted(arena.ids[idx] for idx in false_singletons))
  print
  
  # Sort so the cluster with the most compounds comes first,
  # then by alphabetically smallest id
  def cluster_sort_key(cluster):
      centroid_idx, members = cluster
      return -len(members), arena.ids[centroid_idx]
  
  clusters.sort(key=cluster_sort_key)
    
  print len(clusters), "clusters"
  for centroid_idx, members in clusters:
      print arena.ids[centroid_idx], "has", len(members), "other members"
      print "=>", " ".join(arena.ids[idx] for idx in members)


The algorithm is quick for this small data set. (Less than a second.)

Out of curiosity, I tried this on 100,000 compounds selected
arbitrarily from PubChem. It took 35 seconds on my desktop (a 3.2 GHZ
Intel Core i3) with a threshold of 0.8. In the Butina paper, it took
24 hours to do the same, although that was with a 1024 bit fingerprint
instead of 881. It's hard to judge the absolute speed differences of a
MIPS R4000 from 1998 to a desktop from 2011, but it's less than the
factor of about 2000 you see here.

More relevent is the comparison between these numbers for the 1.1
release compared to the original numbers for the 1.0 release. On my
old laptop, may it rest it peace, it took 7 minutes to compute the
same benchmark. Where did the roughly 16-fold peformance boost come
from? Money. After 1.0 was released, Roche funded me to add various
optimizations, including taking advantage of the symmetery (2x) and
using hardware POPCNT if available (4x). Roche and another company
helped fund the OpenMP support, and when my desktop reran this
benchmark it used 4 cores instead of 1.

The wary among you might notice that 2*4*4 = 32x faster, while I
said the overall code was only 16x faster. Where's the factor of 2x
slowdown? It's in the Python code! The
:func:`chemfp.search.threshold_tanimoto_search_symmetric` step took only 13 seconds. The
remaining 22 seconds was in the leader code written in Python. To
make the analysis more complicated, improvements to the chemfp API
sped up the clustering step by about 40%.

With chemfp 1.0 version, the clustering performance overhead was minor
compared to the full similarity search, so I didn't keep track of
it. With chemfp 1.1, those roles have reversed! 

Update for chemfp 1.6 in 2020: I re-ran the same algorithm on an even
newer Mac laptop, with a single thread on an 2.3 GHz Intel Core i5. It
took 19 seconds. The laptop is more powerful, and chemfp 1.6 added
an even faster search implementation. (The commercial version, chemfp
3, is faster still.)

Reading structure fingerprints using a toolkit
==============================================

In this section you'll learn how to use a chemistry toolkit in order
to compute fingerprints from a given structure file.

NOTE: this is here mostly for historical interest. chemfp 1.6 was
released in 2020. None of the underlying chemistry toolkits support
Python 2.7 and I no longer have a working setup where I can test the
older toolkits. This section shows the output from chemfp 1.4.

What happens if you're given a structure file and you want to find the
two nearest matches in an FPS file? You'll have to generate the
fingerprints for the structures in the structure file, then do the
comparison.

.. highlight:: pycon 

For this section you'll need to have a chemistry toolkit. I'll use the
"chebi_maccs.fps" file generated in :ref:`chebi_fingerprints` as the
targets, and the PubChem file `Compound_027575001_027600000.sdf.gz
<ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_027575001_027600000.sdf.gz>`_
as the source of query structures::

  >>> import chemfp
  >>> from chemfp import search
  >>> targets = chemfp.load_fingerprints("chebi_maccs.fps")
  >>> queries = chemfp.read_molecule_fingerprints(targets.metadata, "Compound_027575001_027600000.sdf.gz")
  >>> for (query_id, hits) in chemfp.knearest_tanimoto_search(queries, targets, k=2, threshold=0.4):
  ...   print query_id, "=>",
  ...   for (target_id, score) in hits.get_ids_and_scores():
  ...     print "%s %.3f" % (target_id, score),
  ...   print
  ...
  27575190 => CHEBI:116551 0.779 CHEBI:105622 0.771
  27575192 => CHEBI:105622 0.809 CHEBI:108425 0.809
  27575198 => CHEBI:109833 0.736 CHEBI:105937 0.730
  27575208 => CHEBI:105622 0.783 CHEBI:108425 0.783
  27575240 => CHEBI:91516 0.747 CHEBI:111326 0.737
  27575250 => CHEBI:105622 0.809 CHEBI:108425 0.809
  27575257 => CHEBI:105622 0.732 CHEBI:108425 0.732
  27575282 => CHEBI:126087 0.764 CHEBI:127676 0.764
  27575284 => CHEBI:105622 0.900 CHEBI:108425 0.900
       # ... many lines omitted ...

That's it! Pretty simple, wasn't it? You didn't even need to explictly
specify which toolkit you wanted to use.

The only new thing here is :func:`chemfp.read_molecule_fingerprints`. The
first parameter of this is the metadata used to configure the
reader. In my case it's::

  >>> print targets.metadata
  #num_bits=166
  #type=RDKit-MACCS166/2
  #software=RDKit/2017.09.1.dev1 chemfp/1.4
  #source=ChEBI_lite.sdf.gz
  #date=2017-09-14T11:19:31

The "type" told chemfp which toolkit to use to read molecules, and how
to generate fingerprints from those molecules, while "aromaticity"
told it which aromaticity model to use when reading the molecule file.

You can instead course pass in your own metadata as the first parameter to
read_molecule_fingerprints, and as a shortcut, if you pass in a
string then it will be used as the fingerprint type.

For examples, if you have OpenBabel installed then you can do::

  >>> from chemfp.bitops import hex_encode
  >>> reader = chemfp.read_molecule_fingerprints("OpenBabel-MACCS", "Compound_027575001_027600000.sdf.gz")
  >>> for i, (id, fp) in enumerate(reader):
  ...   print id, hex_encode(fp)
  ...   if i == 3:
  ...     break
  ... 
  27575433 800404000840549e848189cca1f132aedfab6eff1b
  27575577 800400000000449e850581c22190022f8a8baadf1b
  27575602 000000000000449e840191d820a0122eda9abaff1b
  27575603 000000000000449e840191d820a0122eda9abaff1b

If you have OEChem and OEGraphSim installed then you can do::

  >>> from chemfp.bitops import hex_encode
  >>> reader = chemfp.read_molecule_fingerprints("OpenEye-MACCS166", "Compound_027575001_027600000.sdf.gz")
  >>> for i, (id, fp) in enumerate(reader):
  ...   print id, hex_encode(fp)
  ...   if i == 3:
  ...     break
  ... 
  27575433 000000080840448e8481cdccb1f1b216daaa6a7e3b
  27575577 000000080000448e850185c2219082178a8a6a5e3b
  27575602 000000080000448e8401d14820a01216da983b7e3b
  27575603 000000080000448e8401d14820a01216da983b7e3b

And if you have RDKit installed then you can do::

  >>> from chemfp.bitops import hex_encode
  >>> reader = chemfp.read_molecule_fingerprints("RDKit-MACCS166", "Compound_027575001_027600000.sdf.gz")
  >>> for i, (id, fp) in enumerate(reader):
  ...   print id, hex_encode(fp)
  ...   if i == 3:
  ...     break
  ... 
  27575433 000000000840549e84818dccb1f1323cdfab6eff1f
  27575577 000000000000449e850185c22190023d8a8beadf1f
  27575602 000000000000449e8401915820a0123eda98bbff1f
  27575603 000000000000449e8401915820a0123eda98bbff1f


Select a random fingerprint sample
==================================

In this section you'll learn how to make a new arena where the
fingerprints are randomly selected from the old arena.

A FingerprintArena slice creates a subarena. Technically speaking,
this is a "view" of the original data. The subarena doesn't actually
copy its fingerprint data from the original arena. Instead, it uses
the same fingerprint data, but keeps track of the start and end
position of the range it needs. This is why it's not possible to slice
with a step size other than +1.

This also means that memory for a large arena won't be freed until
all of its subarenas are also removed.

You can see some evidence for this because a :class:`.FingerprintArena` stores
the entire fingerprint data as a set of bytes named `arena`::

  >>> import chemfp
  >>> targets = chemfp.load_fingerprints("pubchem_targets.fps") 
  >>> subset = targets[10:20]
  >>> targets.arena is subset.arena
  True

This shows that the `targets` and `subset` share the same raw data
set. At least it shows that to me, the person who wrote the code.

You can ask an arena or subarena to make a
:meth:`.FingerprintArena.copy`. This allocates new memory for the new
arena and copies all of its fingerprints there.

::

  >>> new_subset = subset.copy()
  >>> len(new_subset) == len(subset)
  >>> new_subset.arena is subset.arena
  False
  >>> subset[7][0]
  '48637548'
  >>> new_subset[7][0]
  '48637548'


The :meth:`.FingerprintArena.copy` method can do more than just copy
the arena. You can give it a list of indices and it will only copy
those fingerprints::

  >>> three_targets = targets.copy([3112, 0, 1234])
  >>> three_targets.ids
  ['48942244', '48568841', '48628197']
  >>> [targets.ids[3112], targets.ids[0], targets.ids[1234]]
  ['48628197', '48942244', '48568841']

Are you confused about why the identifiers aren't in the same order?
That's because when you specify indicies, the copy automatically
reorders them by popcount and stores the popcount information. This
extra work help makes future searches faster. Use
:option:`reorder=False` to leave the order unchanged

  >>> my_ordering = targets.copy([3112, 0, 1234], reorder=False)
  >>> my_ordering.ids
  ['48628197', '48942244', '48568841']

This interesting, in a boring sort of way. Let's get back to the main
goal of getting a random subset of the data. I want to select *m*
records at random, without replacement, to make a new data set. You
can see this just means making a list with *m* different index
values. Python's built-in `random.sample <http://docs.python.org/2/library/random.html#random.sample>`_ function makes this easy::

  >>> import random
  >>> random.sample("abcdefgh", 3)
  ['b', 'h', 'f']
  >>> random.sample("abcdefgh", 2)
  ['d', 'a']
  >>> random.sample([5, 6, 7, 8, 9], 2)
  [7, 9]
  >>> help(random.sample)
  sample(self, population, k) method of random.Random instance
     Chooses k unique random elements from a population sequence.
     ...
     To choose a sample in a range of integers, use xrange as an argument.
     This is especially fast and space efficient for sampling from a
     large population:   sample(xrange(10000000), 60)

The last line of the help points out what do next!::

  >>> random.sample(xrange(len(targets)), 5)
  [610, 2850, 705, 1402, 2635]
  >>> random.sample(xrange(len(targets)), 5)
  [1683, 2320, 1385, 2705, 1850]

Putting it all together, and here's how to get a new arena containing
100 randomly selected fingerprints, without replacement, from the
`targets` arena::

  >>> sample_indices = random.sample(xrange(len(targets)), 100)
  >>> sample = targets.copy(indices=sample_indices)
  >>> len(sample)
  100


Look up a fingerprint with a given id
=====================================

In this section you'll learn how to get a fingerprint record with a
given id.

All fingerprint records have an identifier and a
fingerprint. Identifiers should be unique. (Duplicates are allowed, and
if they exist then the lookup code described in this section will
arbitrarily decide which record to return. Once made, the choice will
not change.)

Let's find the fingerprint for the record in "pubchem_targets.fps"
which has the identifier `48626981`. One solution is to iterate
over all of the records in a file, using the FPS reader::

  >>> import chemfp
  >>> for id, fp in chemfp.open("pubchem_targets.fps"):
  ...   if id == "48626981":
  ...     break
  ... else:
  ...   raise KeyError("%r not found" % (id,))
  ... 
  >>> fp[:5]
  '\x07\xde\x1c\x00\x00'
    
I used the somewhat obscure `else` clause to the `for` loop. If the
`for` finishes without breaking, which would happen if the identifier
weren't present, then it will raise an exception saying that it
couldn't find the given identifier.

If the fingerprint records are already in a :class:`.FingerprintArena`
then there's a better solution. Use the
:meth:`.FingerprintArena.get_fingerprint_by_id` method to get the
fingerprint byte string, or `None` if the identifier doesn't exist::

  >>> arena = chemfp.load_fingerprints("pubchem_targets.fps")
  >>> fp = arena.get_fingerprint_by_id("48626981")
  >>> fp[:5]
  '\x07\xde\x1c\x00\x00'
  >>> missing_fp = arena.get_fingerprint_by_id("does-not-exist")
  >>> missing_fp
  >>> missing_fp is None
  True

Internally this does about what you think it would. It uses the
arena's `id` list to make a lookup table mapping identifier to
index, and caches the table for later use. Given the index, it's very
easy to get the fingerprint.

In fact, you can get the index and do the record lookup yourself::

  >>> arena.get_index_by_id("48626981")
  11223
  >>> fp_index = arena.get_index_by_id("48626981")
  >>> arena[fp_index]
  ('48626981', '\x07\xde\x1c\x00  ... many bytes deleted ...')


Sorting search results
======================

In this section you'll learn how to sort the search results.

The k-nearest searches return the hits sorted from highest score to
lowest, and break ties arbitrarily. This is usually what you want, and
the extra cost to sort is small (k*log(k)) compared to the time needed
to maintain the internal heap (N*log(k)).

By comparison, the threshold searches return the hits in arbitrary
order. Sorting takes up to N*log(N) time, which is extra work for
those cases where you don't want sorted data. Use the
:meth:`SearchResult.reorder` method if you want the hits sorted
in-place::

  >>> import chemfp
  >>> arena = chemfp.load_fingerprints("pubchem_queries.fps")
  >>> query_fp = arena.get_fingerprint_by_id("99129158")
  >>> from chemfp import search
  >>> result = search.threshold_tanimoto_search_fp(query_fp, arena, threshold=0.90)
  >>> len(result)
  5
  >>> for pair in result.get_ids_and_scores():
  ...   print pair
  ...
  ('99129178', 0.9733333333333334)
  ('99129047', 0.9166666666666666)
  ('99129278', 0.9166666666666666)
  ('99129158', 1.0)
  ('99129260', 0.9548387096774194)
  >>> result.reorder("decreasing-score")
  >>> result.reorder("decreasing-score")
  >>> for pair in result.get_ids_and_scores():
  ...   print pair
  ...
  ('99129158', 1.0)
  ('99129178', 0.9733333333333334)
  ('99129260', 0.9548387096774194)
  ('99129047', 0.9166666666666666)
  ('99129278', 0.9166666666666666)
  >>> result.reorder("increasing-score")
  >>> for pair in result.get_ids_and_scores():
  ...   print pair
  ...
  ('99129047', 0.9166666666666666)
  ('99129278', 0.9166666666666666)
  ('99129260', 0.9548387096774194)
  ('99129178', 0.9733333333333334)
  ('99129158', 1.0)

There are currently six different sort methods, all specified by
name. These are

    * increasing-score: sort by increasing score
    * decreasing-score: sort by decreasing score
    * increasing-index: sort by increasing target index
    * decreasing-index: sort by decreasing target index
    * reverse: reverse the current ordering
    * move-closest-first: move the hit with the highest score to the first position

The first two should be obvious from the examples. If you find
something useful for the next two then let me know. The "reverse"
option reverses the current ordering, and is most useful if you want
to reverse the sorted results from a k-nearest search.

The "move-closest-first" option exists to improve the leader algorithm
stage used by the Taylor-Butina algorithm. The newly seen compound is
either in the same cluster as its nearest neighbor or it is the new
centroid. I felt it best to implement this as a special reorder term,
rather than one of the other possible options.

If you are interested in other ways to help improve your clustering
performance, let me know.

Each :class:`.SearchResult` has a :meth:`SearchResult.reorder` 
method. If you want to reorder all of the hits of a :class:`.SearchResults`
then use its :meth:`.SearchResults.reorder_all` method::

  >>> similarity_matrix = search.threshold_tanimoto_search_symmetric(
  ...                         arena, threshold=0.8)
  >>> for query_id, row in zip(arena.ids, similarity_matrix):
  ...   if len(row) == 3:
  ...     print query_id, "->", row.get_ids_and_scores()
  ...
  99110554 -> [('99110555', 1.0), ('99110552', 0.8214285714285714), ('99110553', 0.8214285714285714)]
  99110555 -> [('99110552', 0.8214285714285714), ('99110553', 0.8214285714285714), ('99110554', 1.0)]
  99110556 -> [('99110557', 1.0), ('99110552', 0.8214285714285714), ('99110553', 0.8214285714285714)]
         ... many lines omitted ...
  >>> similarity_matrix.reorder_all("decreasing-score")
  >>> for query_id, row in zip(arena.ids, similarity_matrix):
  ...   if len(row) == 3:
  ...     print query_id, "->", row.get_ids_and_scores()
  ...
  99110554 -> [('99110555', 1.0), ('99110552', 0.8214285714285714), ('99110553', 0.8214285714285714)]
  99110555 -> [('99110554', 1.0), ('99110552', 0.8214285714285714), ('99110553', 0.8214285714285714)]
  99110556 -> [('99110557', 1.0), ('99110552', 0.8214285714285714), ('99110553', 0.8214285714285714)]

It takes the same set of ordering names as :meth:`.SearchResult.reorder`.



Working with raw scores and counts in a range
=============================================

In this section you'll learn how to get the hit counts and raw scores
for a interval.

The length of the :class:`.SearchResult` is the number of hits it contains::

  >>> import chemfp
  >>> from chemfp import search
  >>> arena = chemfp.load_fingerprints("pubchem_targets.fps")
  >>> fp = arena.get_fingerprint_by_id("48692333")
  >>> result = search.threshold_tanimoto_search_fp(fp, arena, threshold=0.2)
  >>> len(result)
  14888

This gives you the number of hits at or above a threshold of 0.2,
which you can also get by doing
:func:`chemfp.search.count_tanimoto_hits_fp`.
The result also stores the hits, and you can get the number of hits
which are within a specified interval. Here are the hits counts at or
above 0.5, 0.80, and 0.95::

  >>> result.count(0.5)
  8976
  >>> result.count(0.8)
  150
  >>> result.count(0.85)
  24
  >>> result.count(0.9)
  0

The first parameter, *min_score*, specifies the minimum
threshold. The second, *max_score*, specifies the maximum. Here's
how to get the number of hits with a score of at most 0.95 and 0.5::

  >>> result.count(max_score=0.95)
  14865
  >>> result.count(max_score=0.5)
  6035

If you work do the addition for the min/max score of 0.5 you'll
realize that 8976 + 6035 equals 15011 which is 123 elements larger
than the result size of 14888. This is because the default interval
uses a closed range, and there are 123 hits with a score of exactly
0.5::

  >>> result.count(0.5, 0.5)
  26

The third parameter, *interval*, specifies the end conditions. The
default is "[]" which means that both ends are closed. The interval
"()" means that both ends are open, and "[)" and "(]" are the two
half-open/half-closed ranges. To get the number of hits below 0.5 and
the number of hits at or above 0.5 then you might use:

  >>> result.count(None, 0.5, "[)")
  5912
  >>> result.count(0.5, None, "[]")
  8976

to get the expected results. (A min or max of `None` means that there
is respectively no lower or no upper bound.)


Now for something a bit fancier. Suppose you have two sets of
structures. How well do they compare to each other? I can think of
various ways to do it. One is to look at a comparison profile. Find
all NxM comparisons between the two sets. How many of the hits have a
threshold of 0.2? How many at 0.5? 0.95?

If there are "many", then the two sets are likely more similar than
not. If the answer is "few", then they are likely rather distinct.

I'll be more specific. Are the coenzyme A-like structures in ChEBI
more similar to the penicillin-like structures than you would expect
by comparing two randomly chosen subsets? By similar, I'll use
Tanimoto similarity of the "chebi_maccs.fps" file created in the
:ref:`chebi_fingerprints` command-line tool example.

The CHEBI id for coenzyme A is CHEBI:15346 and for penicillin is
CHEBI:17334. I'll define the "coenzyme A-like" structures as the 117
structures where the fingerprint is at least 0.95 similar to coenzyme
A, and "penicillin-like" as the 15 structures at least 0.90 similar to
penicillin. This gives 1755 total comparisons.

.. highlight:: python 

You know enough to do this, but there's a nice optimization I haven't
told you about. You can get the total count of all of the threshold
hits using the :meth:`.SearchResults.count_all`
method, instead of looping over each :class:`.SearchResult`
and calling its :meth:`.SearchResult.count`::

    import chemfp
    from chemfp import search
    
    def get_neighbors_as_arena(arena, id, threshold):
        fp = arena.get_fingerprint_by_id(id)
        neighbor_results =  search.threshold_tanimoto_search_fp(fp, chebi, threshold=threshold)
        neighbor_arena = arena.copy(neighbor_results.get_indices())
        return neighbor_arena
    
    chebi = chemfp.load_fingerprints("chebi_maccs.fps")
    
    # coenzyme A
    coA_arena = get_neighbors_as_arena(chebi, "CHEBI:15346", threshold=0.95)
    print len(coA_arena), "coenzyme A-like structures"
    
    # penicillin
    penicillin_arena = get_neighbors_as_arena(chebi, "CHEBI:17334", threshold=0.9)
    print len(penicillin_arena), "penicillin-like structures"
    
    # I'll compute a profile at different thresholds
    thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    # Compare the two sets. (For this case the speed difference between a threshold
    # of 0.25 and 0.0 is not noticible, but having it makes me feel better.)
    coA_against_penicillin_result= search.threshold_tanimoto_search_arena(
        coA_arena, penicillin_arena, threshold=min(thresholds))
    
    # Show a similarity profile
    print "Counts  coA/penicillin"
    for threshold in thresholds:
        print " %.2f      %5d" % (threshold,
                                  coA_against_penicillin_result.count_all(min_score=threshold))

.. highlight:: none

This gives a not very useful output::

    261 coenzyme A-like structures
    8 penicillin-like structures
    Counts  coA/penicillin
     0.30       2088
     0.35       2088
     0.40       2087
     0.45       1113
     0.50          0
     0.60          0
     0.70          0
     0.80          0
     0.90          0

It's not useful because it's not possible to make any decisions from
this. Are the numbers high or low? It should be low, because these are
two quite different structure classes, but there's nothing to compare
it against.

.. highlight:: python 

I need some sort of background reference. What I'll two is construct
two randomly chosen sets, one with 117 fingerprints and the other with
15, and generate the same similarity profile with them. That isn't
quite fair, since randomly chosen sets will most likely be
diverse. Instead, I'll pick one fingerprint at random, then get its
117 or 15, respectively, nearest neighbors as the set members::

    # Get background statistics for random similarity groups of the same size
    import random
    
    # Find a fingerprint at random, get its k neighbors, return them as a new arena
    def get_random_fp_and_its_k_neighbors(arena, k):
        fp = arena[random.randrange(len(arena))][1]
        similar_search = search.knearest_tanimoto_search_fp(fp, arena, k)
        return arena.copy(similar_search.get_indices())

I'll construct 1000 pairs of sets this way, accumulate the threshold
profile, and compare the CoA/penicillin profile to it::

    # Initialize the threshold counts to 0
    total_background_counts = dict.fromkeys(thresholds, 0)
    
    REPEAT = 1000
    for i in range(REPEAT):
        # Select background sets of the same size and accumulate the threshold count totals
        set1 = get_random_fp_and_its_k_neighbors(chebi, len(coA_arena))
        set2 = get_random_fp_and_its_k_neighbors(chebi, len(penicillin_arena))
        background_search = search.threshold_tanimoto_search_arena(set1, set2, threshold=min(thresholds))
        for threshold in thresholds:
            total_background_counts[threshold] += background_search.count_all(min_score=threshold)
    
    print "Counts  coA/penicillin  background"
    for threshold in thresholds:
        print " %.2f      %5d          %5d" % (threshold,
                                               coA_against_penicillin_result.count_all(min_score=threshold),
                                               total_background_counts[threshold] / (REPEAT+0.0))

.. highlight:: none 
                                               
Your output should look something like::

    Counts  coA/penicillin  background
     0.30       2088            882
     0.35       2088            698
     0.40       2087            550
     0.45       1113            413
     0.50          0            322
     0.60          0            156
     0.70          0             58
     0.80          0             20
     0.90          0              5

This is a bit hard to interpret. Clearly the coenzyme A and penicillin
sets are not closely similar, but for low Tanimoto scores the
similarity is higher than expected.

That difficulty is okay for now because I mostly wanted to show an
example of how to use the chemfp API. If you want to dive deeper into
this sort of analysis then read a three-part series I wrote at
http://www.dalkescientific.com/writings/diary/archive/2017/03/20/fingerprint_set_similarity.html
on using chemfp to build a target set association network using ChEMBL.

I first learned about this approach from the `Similarity Ensemble
Approach` (SEA) work of Keiser, Roth, Armbruster, Ernsberger, and
Irwin. The paper is available online from http://sea.bkslab.org/ .

.. highlight:: pycon 

That paper actually wants you to use the "raw score". This is the sum
of the hit scores in a given range, and not just the number of
hits. No problem! Use :meth:`.SearchResult.cumulative_score` for an
individual result or :meth:`.SearchResults.cumulative_score_all` for
the entire set of results::

    >>> sum(row.cumulative_score(min_score=0.5, max_score=0.9)
    ...             for row in coA_against_penicillin_result)
    224.83239025119906
    >>> coA_against_penicillin_result.cumulative_score_all(min_score=0.5, max_score=0.9)
    224.83239025119866

These also take the *interval* parameter if you don't want the default
of `[]`.

You may wonder why these two values aren't exactly the same. Addition
of floating point numbers isn't associative. You can see that I get
still different results if I sum up the values in reverse order::

  >>> sum(list(row.cumulative_score(min_score=0.5, max_score=0.9)
  ...                for row in coA_against_penicillin_result)[::-1])
  224.83239025119875

