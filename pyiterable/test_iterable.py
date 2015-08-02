from unittest import TestCase
from pyiterable.iterable import Iterable


class TestIterableTestClazz:
        def __init__(self, stub):
            self.__stub = stub


class TestIterable(TestCase):

    def setUp(self):
        self.__int_list = [1, 2, 5, 0, -8]
        self.__float_list = [1.3, 74.5, 9837.293, -283.4]
        self.__string_list = ["akd", "fadskl", "dfa"]
        self.__clazz_list = [TestIterableTestClazz(i) for i in range(7)]

        self.__test_lists = [
            self.__int_list,
            self.__float_list,
            self.__string_list,
            self.__clazz_list
        ]

        self.__test_sets = [set(l) for l in self.__test_lists]

        self.__test_input = self.__test_lists + self.__test_sets

    def test_to_list(self):
        for i in self.__test_input:
            with self.subTest(i=i):
                actual = Iterable(i).to_list()

                self.assertCountEqual(
                    i,
                    actual
                )

                self.assertIs(
                    type([]),
                    type(actual)
                )

    def test_to_set(self):
        for i in self.__test_input:
            with self.subTest(i=i):
                actual = Iterable(i).to_set()

                self.assertCountEqual(
                    i,
                    actual
                )

                self.assertIs(
                    type(set()),
                    type(actual)
                )

    def test_all(self):
        self.fail()

    def test_any(self):
        self.fail()

    def test_enumerate(self):
        self.fail()

    def test_filter(self):
        self.fail()

    def test_len(self):
        self.fail()

    def test_map(self):
        self.fail()

    def test_max(self):
        self.fail()

    def test_min(self):
        self.fail()

    def test_reversed(self):
        self.fail()

    def test_sorted(self):
        self.fail()

    def test_sum(self):
        self.fail()

    def test_zip(self):
        self.fail()

    def test_reduce(self):
        self.fail()