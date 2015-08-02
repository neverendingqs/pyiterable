from unittest import TestCase
from pyiterable.iterable import Iterable


class TestIterableTestClazz:
        def __init__(self, stub):
            self.__stub = stub


class TestIterable(TestCase):

    def setUp(self):
        self.__bool_list = [True, False, False, True, False, False]
        self.__int_list = [1, 2, 2, 5, 0, -8]
        self.__float_list = [1.3, 74.5, 9837.293, -283.4, 74.5]
        self.__string_list = ["akd", "fadskl", "dfa", "akd"]
        self.__clazz_list = [TestIterableTestClazz(i) for i in range(7)]
        self.__clazz_list.append(self.__clazz_list[0])  # Creates duplicates in list

        self.__test_lists = [
            self.__bool_list,
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
                    list(i),
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
                    set(i),
                    actual
                )

                self.assertIs(
                    type(set()),
                    type(actual)
                )

    def test_all_hasFalse_returnsFalse(self):
        test_list = [True, False, True, True]

        test_input = [
            test_list,
            set(test_list)
        ]

        for i in test_input:
            with self.subTest(i=i):
                self.assertEqual(
                    all(i),
                    Iterable(i).all()
                )

    def test_all_onlyHasTrue_returnsTrue(self):
        test_list = [True for i in range(7)]

        test_input = [
            test_list,
            set(test_list)
        ]

        for i in test_input:
            with self.subTest(i=i):
                self.assertEqual(
                    all(i),
                    Iterable(i).all()
                )

    def test_any_hasTrue_returnsTrue(self):
        test_list = [True, False, True, True]

        test_input = [
            test_list,
            set(test_list)
        ]

        for i in test_input:
            with self.subTest(i=i):
                self.assertEqual(
                    any(i),
                    Iterable(i).any()
                )

    def test_any_onlyHasFalse_returnsFalse(self):
        test_list = [False for i in range(7)]

        test_input = [
            test_list,
            set(test_list)
        ]

        for i in test_input:
            with self.subTest(i=i):
                self.assertEqual(
                    any(i),
                    Iterable(i).any()
                )

    def test_enumerate_defaultStart(self):
        for i in self.__test_input:
            with self.subTest(i=i):
                self.assertCountEqual(
                    list(enumerate(i)),
                    list(Iterable(i).enumerate())
                )

    def test_enumerate_customStart(self):
        start = 3
        for i in self.__test_input:
            with self.subTest(i=i):
                self.assertCountEqual(
                    list(enumerate(i, start)),
                    list(Iterable(i).enumerate(start))
                )

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