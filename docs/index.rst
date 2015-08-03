.. pyiterable documentation master file, created by
   sphinx-quickstart on Sun Aug 02 18:38:45 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pyiterable API Documentation
============================
The purpose of this module is to allow chaining multiple built-in methods that operate on an iterable, which allows coders to be more expressive with the transformations occurring without the intermediate steps.


Classes
-------

.. toctree::
    :maxdepth: 2

    api


Details
-------
Inspired by:

* `C#'s Enumerable class <https://msdn.microsoft.com/en-us/library/system.linq.enumerable(v=vs.110).aspx>`_
* `Apache Spark RDD Operations <http://spark.apache.org/docs/latest/programming-guide.html#rdd-operations>`_
* `Java stream package <https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html>`_



Instead of:

.. code-block:: python

    no_quotes = map(lambda x: x.strip('"'), values)
    to_int = map(lambda x: int(x), no_quotes)
    sum = reduce(lambda a, b: a + b, to_int)

or:

.. code-block:: python

    sum = reduce(
        lambda a, b: a + b,
        map(
            lambda x: int(x),
            map(lambda x: x.strip('"'), values)
        )
    )

do this:

.. code-block:: python

    from pyiterable import Iterable
    ...
    sum = (Iterable(values)
        .map(lambda x: x.strip('"'))
        .map(lambda x: int(x))
        .reduce(lambda a, b: a + b)
    )


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

