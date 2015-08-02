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
        return Iterable(all(self.__iterable))

    def any(self):
        return Iterable(any(self.__iterable))

    def enumerate(self, start=0):
        return Iterable(enumerate(self.__iterable, start))

    def filter(self, func):
        return Iterable(filter(func, self.__iterable))

    def len(self):
        return len(self.__iterable)

    def map(self, func):
        return Iterable(map(func, self.__iterable))

    def max(self, key=lambda x: x, default=None):
        if default is None:
            return Iterable(max(self.__iterable, key=key))
        else:
            return Iterable(max(self.__iterable, key=key, default=default))

    def min(self, key=lambda x: x, default=None):
        if default is None:
            return Iterable(min(self.__iterable, key=key))
        else:
            return Iterable(min(self.__iterable, key=key, default=default))

    def reversed(self):
        return Iterable(reversed(self.__iterable))

    def sorted(self, key=lambda x: x, reverse=False):
        return Iterable(sorted(self.__iterable, key=key, reverse=reverse))

    def sum(self, start=0):
        return sum(self.__iterable, start)

    def zip(self, *args):
        return Iterable(zip(self.__iterable, args))

    # functools equivalent transformations
    def reduce(self, func, initializer=None):
        if initializer is None:
            return reduce(func, self.__iterable)
        else:
            return reduce(func, self.__iterable, initializer)
