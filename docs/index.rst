Pyiterable API Documentation
============================
Python comes with some nice built-in methods for operating on iterables, but it can get messy really quickly if you want to transform an iterable multiple times. Write more expressive code by chaining built-in transformations with this module.

Scroll down for examples.


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

    values = ["1", "2", "5", "9"]
    
    to_int = map(lambda x: int(x), values)
    filtered = filter(lambda x: x > 4)
    sum = reduce(lambda a, b: a + b, to_int)

or:

.. code-block:: python

    values = ["1", "2", "5", "9"]
    
    sum = reduce(
        lambda a, b: a + b,
        filter(
            lambda x: x > 4,
            map(lambda x: int(x), values)
        )
    )

do this:

.. code-block:: python

    from pyiterable import Iterable
    ...
    values = Iterable(["1", "2", "5", "9"])
    
    sum = (values
           .map(lambda x: int(x))
           .filter(lambda x: x > 4)
           .reduce(lambda a, b: a + b)
    )


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

