from functools import reduce


class Iterable:

    def __init__(self, iterable):
        iter(iterable)
        self.__iterable = iterable

    def __iter__(self):
        return self.__iterable.__iter__()

    def __next__(self):
        return self.__iterable.__next__()

    def __len__(self):
        return len(self.__iterable)

    # built-in equivalent data structures
    def to_list(self):
        return list(self.__iterable)

    def to_set(self):
        return set(self.__iterable)

    # built-in equivalent transformations
    def all(self):
        """ Equivalent to the built-in function **all(** *iterable* **)**

            >>> Iterable([True, False, True]).all()
            False
            >>> Iterable([True, True, True, True]).all()
            True
        """
        return all(self.__iterable)

    def any(self):
        """ Equivalent to the built-in function **any(** *iterable* **)**

            >>> Iterable([True, False, True]).any()
            True
            >>> Iterable([False, False, False, False]).any()
            False
        """
        return any(self.__iterable)

    def enumerate(self, start=0):
        return Iterable(enumerate(self.__iterable, start))

    def filter(self, function):
        return Iterable(filter(function, self.__iterable))

    def len(self):
        return self.__len__()

    def map(self, function):
        return Iterable(map(function, self.__iterable))

    def max(self, **kwargs):
        return max(self.__iterable, **kwargs)

    def min(self, **kwargs):
        return min(self.__iterable, **kwargs)

    def reversed(self):
        return Iterable(reversed(self.__iterable))

    def sorted(self, **kwargs):
        return Iterable(sorted(self.__iterable, **kwargs))

    def sum(self, start=0):
        return sum(self.__iterable, start)

    def zip(self, *args):
        return Iterable(zip(self.__iterable, *args))

    # functools equivalent transformations
    def reduce(self, function, **kwargs):
        return reduce(function, self.__iterable, **kwargs)
