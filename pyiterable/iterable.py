from functools import reduce


class Iterable:

    def __init__(self, iterable):
        iter(iterable)
        self.__iterable = iterable

    def __iter__(self):
        return self.__iterable.__iter__()

    def __next__(self):
        return self.__iterable.__next__()

    # built-in equivalent data structures
    def to_list(self):
        return list(self.__iterable)

    def to_set(self):
        return set(self.__iterable)

    # built-in equivalent transformations
    def all(self):
        return all(self.__iterable)

    def any(self):
        return any(self.__iterable)

    def enumerate(self, start=0):
        return Iterable(enumerate(self.__iterable, start))

    def filter(self, function):
        return Iterable(filter(function, self.__iterable))

    def len(self):
        return len(self.__iterable)

    def map(self, function):
        return Iterable(map(function, self.__iterable))

    def max(self, key=lambda x: x, default=None):
        if len(self.__iterable) == 0 and default is not None:
            return default
        else:
            return max(self.__iterable, key=key)

    def min(self, key=lambda x: x, default=None):
        if len(self.__iterable) == 0 and default is not None:
            return default
        else:
            return min(self.__iterable, key=key)

    def reversed(self):
        return Iterable(reversed(self.__iterable))

    def sorted(self, **args):
        return Iterable(sorted(self.__iterable, **args))

    def sum(self, start=0):
        return sum(self.__iterable, start)

    def zip(self, *args):
        return Iterable(zip(self.__iterable, *args))

    # functools equivalent transformations
    def reduce(self, function, **args):
        return reduce(function, self.__iterable, **args)
