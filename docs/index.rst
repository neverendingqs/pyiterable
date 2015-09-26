Pyiterable API Documentation
============================
Python comes with some nice built-in methods for operating on iterables, but it can get messy really quickly if you want to transform an iterable multiple times. Write more expressive code by chaining built-in transformations with this module.

The module is available on `PyPI <https://pypi.python.org/pypi/pyiterable>`_ via ``pip``:

``pip install pyiterable``


Examples below.


Classes
-------

.. toctree::

    classes/iterable


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


Release
-------

0.3.1

* Added support for Python 3.5
* Removed support for Python 3.2

0.3.0

* Added set-like functionality, including ``difference()``, ``intersection()``,  ``symmetric_difference()``, and ``union()``.
* Added ``concat()`` as an alternative to ``union()``
* Added ``distinct()``
* Added frozenset support (``to_frozenset()``)

0.2.0

* Added ``first()``, which gives you the first value in ``Iterable``, with an optional default if no values exist
* Added ``mapmany()``, which functions like map, except it expects more than one output for each item of ``Iterable``

0.1.0

* First release!
* *Iterable* class with equivalent built-in functions related to iterables


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

