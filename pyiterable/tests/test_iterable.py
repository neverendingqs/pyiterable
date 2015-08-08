from collections import Counter
from functools import reduce
from unittest import TestCase
from unittest import skipIf
import sys

from pyiterable import Iterable


class TestIterableTestClazz:
    def __add__(self, other):
        # Overridden for reduce
        return TestIterableTestClazz(self.stub + other.stub)

    def __eq__(self, other):
        # Overridden for reduce
        return self.stub == other.stub

    def __hash__(self):
        # Overridden for reduce
        return hash(self.stub)

    def __ge__(self, other):
        # Overridden for sorting related functions
        # Test idea from http://stackoverflow.com/a/3755251/2687324
        return self.stub >= other.stub

    def __le__(self, other):
        # Overridden for sorting related functions
        # Test idea from http://stackoverflow.com/a/3755251/2687324
        return self.stub <= other.stub

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
        self.__string = "qwerty"
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

    def test_constructor_nonIterable_throwsError(self):
        test_inputs = [
            1,
            -3.4,
            TestIterableTestClazz("y")
        ]

        for test_input in test_inputs:
            with self.assertRaises(TypeError):
                Iterable(test_input)

    def test_to_list(self):
        for test_input in self.__test_input:
            actual = Iterable(test_input).to_list()

            self.assertEqual(
                Counter(list(test_input)),
                Counter(actual)
            )

            self.assertIs(
                type([]),
                type(actual)
            )

    def test_to_set(self):
        for test_input in self.__test_input:
            actual = Iterable(test_input).to_set()

            self.assertEqual(
                Counter(set(test_input)),
                Counter(actual)
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
            self.assertEqual(
                any(test_input),
                Iterable(test_input).any()
            )

    def test_enumerate_defaultStart(self):
        for test_input in self.__test_input:
            self.assertEqual(
                Counter(list(enumerate(test_input))),
                Counter(list(Iterable(test_input).enumerate()))
            )

    @skipIf(sys.version_info < (2, 6), "'start' keyword-only argument is new in 2.6")
    def test_enumerate_customStart(self):
        start = 3
        for test_input in self.__test_input:
            self.assertEqual(
                Counter(list(enumerate(test_input, start))),
                Counter(list(Iterable(test_input).enumerate(start)))
            )

    def test_filter(self):
        for test_input in self.__test_input:
            # Extract a random item to filter on
            filtered_item = set(test_input).pop()
            func = lambda x: x is filtered_item

            self.assertEqual(
                Counter(filter(func, test_input)),
                Counter(Iterable(test_input).filter(func))
            )

    def test_len(self):
        for test_input in self.__test_input:
            self.assertEqual(
                len(test_input),
                Iterable(test_input).len()
            )

    def test_map(self):
        for test_input in self.__test_input:
            func = lambda x: str(x)[0]

            self.assertEqual(
                Counter(list(map(func, test_input))),
                Counter(list(Iterable(test_input).map(func)))
            )

    def test_max_noDefault_returnsMax(self):
        for test_input in self.__test_input:
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
            self.assertEqual(
                max(test_input, key=key),
                Iterable(test_input).max(key=key)
            )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_max_emptyIterableWithDefault_returnsDefault(self):
        default = 7

        for test_input in [[], set()]:
            self.assertEqual(
                default,
                Iterable(test_input).max(default=default)
            )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_max_emptyIterableAndDefaultIsNone_returnsNone(self):
        for test_input in [[], set()]:
            self.assertEqual(
                None,
                Iterable(test_input).max(default=None)
            )

    def test_max_invalidKeywordParameter_throwsError(self):
        for test_input in self.__test_input:
            with self.assertRaises(Exception) as expected_error:
                max([0], invalid=2)

            with self.assertRaises(Exception) as actual_error:
                Iterable(test_input).max(invalid=2)

            self.assertEqual(
                type(expected_error),
                type(actual_error)
            )

    def test_min_noDefault_returnsMin(self):
        for test_input in self.__test_input:
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
            self.assertEqual(
                min(test_input, key=key),
                Iterable(test_input).min(key=key)
            )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_min_emptyIterableWithDefault_returnsDefault(self):
        default = -6

        for test_input in [[], set()]:
            self.assertEqual(
                default,
                Iterable(test_input).min(default=default)
            )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_min_emptyIterableAndDefaultIsNone_returnsNone(self):
        for test_input in [[], set()]:
            self.assertEqual(
                None,
                Iterable(test_input).min(default=None)
            )

    def test_min_invalidKeywordParameter_throwsError(self):
        for test_input in self.__test_input:
            with self.assertRaises(Exception) as expected_error:
                min([0], invalid=2)

            with self.assertRaises(Exception) as actual_error:
                Iterable(test_input).min(invalid=2)

            self.assertEqual(
                type(expected_error),
                type(actual_error)
            )

    def test_reversed(self):
        err_msg = "{} is not the reverse of the input {}"

        for test_input in self.__test_lists:
            reversed_iterable = (Iterable(test_input)
                                 .reversed()
                                 .to_list())

            self.assertEqual(
                len(test_input),
                len(reversed_iterable),
                msg=err_msg.format(reversed_iterable, test_input)
            )

            self.assertTrue(
                all(
                    test_input[i] == reversed_iterable[len(reversed_iterable) - i - 1]
                    for i in range(len(reversed_iterable))
                ),
                msg=err_msg.format(reversed_iterable, test_input)
            )

    def test_sorted_noOptionalArguments_returnsSortedIterable(self):
        for test_input in self.__test_input:
            sorted_iterable = (Iterable(test_input)
                               .sorted()
                               .to_list())

            self.assertTrue(
                all(sorted_iterable[i] <= sorted_iterable[i+1] for i in range(len(sorted_iterable) - 1)),
                msg="Iterable {} not sorted".format(sorted_iterable)
            )

    def test_sorted_reverse_returnsReversedSortedIterable(self):
        reversed_sort = True

        for test_input in self.__test_input:
            sorted_iterable = (Iterable(test_input)
                               .sorted(reverse=reversed_sort)
                               .to_list())

            self.assertTrue(
                all(sorted_iterable[i] >= sorted_iterable[i+1] for i in range(len(sorted_iterable) - 1)),
                msg="Iterable {} not sorted".format(sorted_iterable)
            )

    def test_sorted_withKey_returnsSortedIterable(self):
        key = lambda x: x.stub

        for test_input in [self.__clazz_list, set(self.__clazz_list)]:
            sorted_iterable = (Iterable(test_input)
                               .sorted(key=key)
                               .to_list())

            self.assertTrue(
                all(sorted_iterable[i].stub <= sorted_iterable[i+1].stub for i in range(len(sorted_iterable) - 1)),
                msg="Iterable {} not sorted".format(sorted_iterable)
            )

    def test_sum_noStartValue_returnsSum(self):
        test_inputs = [
            self.__int_list,
            self.__float_list,
            set(self.__int_list),
            set(self.__float_list)
        ]

        for test_input in test_inputs:
            self.assertEqual(
                sum(test_input),
                Iterable(test_input).sum()
            )

    def test_sum_withStartValue_returnsSumWithStartValue(self):
        test_inputs = [
            self.__int_list,
            self.__float_list,
            set(self.__int_list),
            set(self.__float_list)
        ]

        start = 10

        for test_input in test_inputs:
            self.assertEqual(
                sum(test_input, start),
                Iterable(test_input).sum(start)
            )

    def test_zip_twoIterables_returnsProperZip(self):
        for left in self.__test_input:
            for right in self.__test_input:
                self.assertEqual(
                    Counter(list(zip(left, right))),
                    Counter(list(Iterable(left).zip(right)))
                )

    def test_zip_multipleIterables_returnsProperZip(self):
        right = self.__test_input

        for left in self.__test_input:
            self.assertEqual(
                Counter(list(zip(left, *right))),
                Counter(list(Iterable(left).zip(*right)))
            )

    def test_zip_iterableWithIterableObject_returnsProperZip(self):
        for left in self.__test_input:
            for right in self.__test_input:
                self.assertEqual(
                    Counter(zip(left, right)),
                    Counter(Iterable(left).zip(Iterable(right)))
                )

    def test_zip_iterableWithMultipleIterableObjects_returnsProperZip(self):
        right = list(map(lambda x: Iterable(x), self.__test_input))
        for left in self.__test_input:
            self.assertEqual(
                Counter(zip(left, *right)),
                Counter(Iterable(left).zip(*right))
            )

    def test_reduce(self):
        func = lambda a, b: a + b

        for test_input in self.__test_input:
            self.assertEqual(
                reduce(func, test_input),
                Iterable(test_input).reduce(func)
            )