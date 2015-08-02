from unittest import TestCase

from iterable import Iterable


class TestIterableTestClazz:
        def __lt__(self, other):
            # Overridden for sorting related functions
            # http://stackoverflow.com/a/7152796/2687324
            return self.stub < other.stub

        def __init__(self, stub):
            self.stub = stub


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
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                actual = Iterable(test_input).to_list()

                self.assertCountEqual(
                    list(test_input),
                    actual
                )

                self.assertIs(
                    type([]),
                    type(actual)
                )

    def test_to_set(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                actual = Iterable(test_input).to_set()

                self.assertCountEqual(
                    set(test_input),
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

        for test_input in test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    all(test_input),
                    Iterable(test_input).all()
                )

    def test_all_onlyHasTrue_returnsTrue(self):
        test_list = [True for i in range(7)]

        test_input = [
            test_list,
            set(test_list)
        ]

        for test_input in test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    all(test_input),
                    Iterable(test_input).all()
                )

    def test_any_hasTrue_returnsTrue(self):
        test_list = [True, False, True, True]

        test_input = [
            test_list,
            set(test_list)
        ]

        for test_input in test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    any(test_input),
                    Iterable(test_input).any()
                )

    def test_any_onlyHasFalse_returnsFalse(self):
        test_list = [False for i in range(7)]

        test_input = [
            test_list,
            set(test_list)
        ]

        for test_input in test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    any(test_input),
                    Iterable(test_input).any()
                )

    def test_enumerate_defaultStart(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    list(enumerate(test_input)),
                    list(Iterable(test_input).enumerate())
                )

    def test_enumerate_customStart(self):
        start = 3
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    list(enumerate(test_input, start)),
                    list(Iterable(test_input).enumerate(start))
                )

    def test_filter(self):
        for test_input in self.__test_input:
            # Extract a random item to filter on
            filtered_item = set(test_input).pop()
            func = lambda x: x is filtered_item

            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    filter(func, test_input),
                    Iterable(test_input).filter(func)
                )

    def test_len(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    len(test_input),
                    Iterable(test_input).len()
                )

    def test_map(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                func = lambda x: str(x)[0]

                self.assertCountEqual(
                    list(map(func, test_input)),
                    list(Iterable(test_input).map(func))
                )

    def test_max_noDefault_returnsMax(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    max(test_input),
                    Iterable(test_input).max()
                )

    def test_max_noDefaultWithKeyArgument_returnsMax(self):
        key = lambda x: x.stub

        test_inputs = [
            self.__clazz_list,
            set(self.__clazz_list)
        ]

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    max(test_input, key=key),
                    Iterable(test_input).max(key=key)
                )

    def test_max_emptyIterableWithDefault_returnsDefault(self):
        default = 7

        for test_input in [[], set()]:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    max(test_input, default=default),
                    Iterable(test_input).max(default=default)
                )

    def test_min_noDefault_returnsMin(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    min(test_input),
                    Iterable(test_input).min()
                )

    def test_min_noDefaultWithKeyArgument_returnsMin(self):
        key = lambda x: x.stub

        test_inputs = [
            self.__clazz_list,
            set(self.__clazz_list)
        ]

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    min(test_input, key=key),
                    Iterable(test_input).min(key=key)
                )

    def test_min_emptyIterableWithDefault_returnsDefault(self):
        default = -6

        for test_input in [[], set()]:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    min(test_input, default=default),
                    Iterable(test_input).min(default=default)
                )

    def test_reversed(self):
        for test_input in self.__test_lists:
            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    reversed(test_input),
                    Iterable(test_input).reversed()
                )

    def test_sorted_noOptionalArguments_returnsSortedIterable(self):
        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    sorted(test_input),
                    Iterable(test_input).sorted()
                )

    def test_sorted_reverse_returnsReversedSortedIterable(self):
        reversed_sort = True

        for test_input in self.__test_input:
            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    sorted(test_input, reverse=reversed_sort),
                    Iterable(test_input).sorted(reverse=reversed_sort)
                )

    def test_sorted_withKey_returnsSortedIterable(self):
        key = lambda x: x.stub

        for test_input in [self.__clazz_list, set(self.__clazz_list)]:
            with self.subTest(test_input=test_input):
                self.assertCountEqual(
                    sorted(test_input, key=key),
                    Iterable(test_input).sorted(key=key)
                )

    def test_sum(self):
        self.fail()

    def test_zip(self):
        self.fail()

    def test_reduce(self):
        self.fail()