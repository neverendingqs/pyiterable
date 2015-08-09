# Pyiterable

Python comes with some nice built-in methods for operating on iterables, but it can get messy really quickly if you want to transform an iterable multiple times. Write more expressive code by chaining built-in transformations with this module.

## Example

    from pyiterable import Iterable
    ...
    values = Iterable(["1", "2", "5", "9"])
    
    sum = (values
           .map(lambda x: int(x))
           .filter(lambda x: x > 4)
           .reduce(lambda a, b: a + b)
    )

## Inspiration

* [C#'s Enumerable class](https://msdn.microsoft.com/en-us/library/system.linq.enumerable.aspx)
* [Apache Spark RDD Operations](http://spark.apache.org/docs/latest/programming-guide.html#rdd-operations)
* [Java stream package](https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html)

## API Docs
<link to come>
