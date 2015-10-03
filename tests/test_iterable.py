from collections import Counter
from copy import deepcopy
from functools import reduce
from unittest2 import skipIf, TestCase
import uuid
import sys

from pyiterable import Iterable


class TestIterableTestClazz:
    def __add__(self, other):
        # Overridden for reduce
        return TestIterableTestClazz(self.stub + other.stub)

    def __eq__(self, other):
        # Overridden for reduce
        if type(self) is not type(other):
            return False

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

    def __extend_test(self, test):
        """
        Extends test to different iterable types,
        making it easier to add/remove iterable types we want to test for in this test suite.

        :param test: an iterable representing the test input
        :return: list of test inputs, each of the type we want to test for
        """
        new_tests = [
            list(test),
            set(test),
            tuple(test),
            Iterable(test)
        ]

        return new_tests

    def __extend_tests(self, tests):
        """
        Extends tests to different iterable types,
        making it easier to add/remove iterable types we want to test for in this test suite.

        :param tests: an iterable containing multiple test inputs
        :return: list of test inputs, represented by all iterable types we want to test for
        """
        new_tests = []
        for test in tests:
            new_tests.extend(self.__extend_test(test))

        return new_tests

    def _extend_test_tuples(self, tests):
        """
        Extends tests of type tuple(left_iterable, right_iterable),
        making it easier to add/remove iterable types we want to test for in this test suite.

        :param tests: an iterable of tuples of the form (left_iterable, right_iterable)
        :return: list of test inputs of the form, represented by all iterable types we want to test for
        """
        new_tests = list(map(lambda t: (list(t[0]), list(t[1])), tests))
        tests.extend(list(map(lambda t: (set(t[0]), set(t[1])), tests)))
        tests.extend(list(map(lambda t: (tuple(t[0]), tuple(t[1])), tests)))
        tests.extend(list(map(lambda t: (Iterable(t[0]), Iterable(t[1])), tests)))

        return new_tests

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
        self.__test_inputs = self.__extend_tests(self.__test_lists)

    def test_constructor_nonIterable_throwsError(self):
        test_inputs = [
            1,
            -3.4,
            TestIterableTestClazz("y")
        ]

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(TypeError):
                    Iterable(test_input)

    def test_constructor_copiesIterable(self):
        for test_input in self.__test_lists:
            with self.subTest(test_input=test_input):
                iterable = Iterable(test_input)
                test_input.append(uuid.uuid4())

                self.assertNotEquals(
                    Counter(test_input),
                    Counter(iterable)
                )

    def test_to_frozenset(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                actual = Iterable(test_input).to_frozenset()

                self.assertEqual(
                    Counter(frozenset(test_input)),
                    Counter(actual)
                )

                self.assertIs(
                    type(frozenset()),
                    type(actual)
                )

    def test_to_list(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
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
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                actual = Iterable(test_input).to_set()
    
                self.assertEqual(
                    Counter(set(test_input)),
                    Counter(actual)
                )
    
                self.assertIs(
                    type(set()),
                    type(actual)
                )

    def test_to_tuple(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                actual = Iterable(test_input).to_tuple()
    
                self.assertEqual(
                    Counter(tuple(test_input)),
                    Counter(actual)
                )
    
                self.assertIs(
                    type(tuple()),
                    type(actual)
                )

    def test_all_hasFalse_returnsFalse(self):
        test = [True, False, True, True]
        test_inputs = self.__extend_test(test)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    all(test_input),
                    Iterable(test_input).all()
                )

    def test_all_onlyHasTrue_returnsTrue(self):
        test = [True for i in range(7)]
        test_inputs = self.__extend_test(test)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    all(test_input),
                    Iterable(test_input).all()
                )

    def test_any_hasTrue_returnsTrue(self):
        test = [True, False, True, True]
        test_inputs = self.__extend_test(test)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    any(test_input),
                    Iterable(test_input).any()
                )

    def test_any_onlyHasFalse_returnsFalse(self):
        test = [False for i in range(7)]
        test_inputs = self.__extend_test(test)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    any(test_input),
                    Iterable(test_input).any()
                )

    def test_enumerate_defaultStart(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    Counter(list(enumerate(test_input))),
                    Counter(Iterable(test_input).enumerate().to_list())
                )

    @skipIf(sys.version_info < (2, 6), "'start' keyword-only argument is new in 2.6")
    def test_enumerate_customStart(self):
        start = 3
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    Counter(list(enumerate(test_input, start))),
                    Counter(Iterable(test_input).enumerate(start).to_list())
                )

    def test_filter(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                # Extract a random item to filter on
                filtered_item = set(test_input).pop()
                func = lambda x: x is filtered_item
    
                self.assertEqual(
                    Counter(filter(func, test_input)),
                    Counter(Iterable(test_input).filter(func))
                )

    def test_len(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    len(list(test_input)),
                    Iterable(test_input).len()
                )

    def test_map(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                func = lambda x: str(x)[0]
    
                self.assertEqual(
                    Counter(list(map(func, test_input))),
                    Counter(Iterable(test_input).map(func).to_list())
                )

    def test_max_noDefault_returnsMax(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    max(test_input),
                    Iterable(test_input).max()
                )

    def test_max_noDefaultWithKeyArgument_returnsMax(self):
        key = lambda x: x.stub
        test_inputs = self.__extend_test(self.__clazz_list)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    max(test_input, key=key),
                    Iterable(test_input).max(key=key)
                )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_max_emptyIterableWithDefault_returnsDefault(self):
        default = 7

        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).max(default=default)
                )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_max_emptyIterableAndDefaultIsNone_returnsNone(self):
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).max(default=None)
                )

    def test_max_invalidKeywordParameter_throwsError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(Exception) as expected_error:
                    max([0], invalid=2)
    
                with self.assertRaises(Exception) as actual_error:
                    Iterable(test_input).max(invalid=2)
    
                self.assertEqual(
                    type(expected_error),
                    type(actual_error)
                )

    def test_min_noDefault_returnsMin(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    min(test_input),
                    Iterable(test_input).min()
                )

    def test_min_noDefaultWithKeyArgument_returnsMin(self):
        key = lambda x: x.stub
        test_inputs = self.__extend_test(self.__clazz_list)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    min(test_input, key=key),
                    Iterable(test_input).min(key=key)
                )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_min_emptyIterableWithDefault_returnsDefault(self):
        default = -6

        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).min(default=default)
                )

    @skipIf(sys.version_info < (3, 4), "'default' keyword-only argument is new in 3.4")
    def test_min_emptyIterableAndDefaultIsNone_returnsNone(self):
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).min(default=None)
                )

    def test_min_invalidKeywordParameter_throwsError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
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
            with self.subTest(test_input=test_input):
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
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                sorted_iterable = (Iterable(test_input)
                                   .sorted()
                                   .to_list())
    
                self.assertTrue(
                    all(sorted_iterable[i] <= sorted_iterable[i+1] for i in range(len(sorted_iterable) - 1)),
                    msg="Iterable {} not sorted".format(sorted_iterable)
                )

    def test_sorted_reverse_returnsReversedSortedIterable(self):
        reversed_sort = True

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                sorted_iterable = (Iterable(test_input)
                                   .sorted(reverse=reversed_sort)
                                   .to_list())
    
                self.assertTrue(
                    all(sorted_iterable[i] >= sorted_iterable[i+1] for i in range(len(sorted_iterable) - 1)),
                    msg="Iterable {} not sorted".format(sorted_iterable)
                )

    def test_sorted_withKey_returnsSortedIterable(self):
        key = lambda x: x.stub
        test_inputs = self.__extend_test(self.__clazz_list)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                sorted_iterable = (Iterable(test_input)
                                   .sorted(key=key)
                                   .to_list())
    
                self.assertTrue(
                    all(sorted_iterable[i].stub <= sorted_iterable[i+1].stub for i in range(len(sorted_iterable) - 1)),
                    msg="Iterable {} not sorted".format(sorted_iterable)
                )

    def test_sum_noStartValue_returnsSum(self):
        test_inputs = self.__extend_test(self.__int_list) + self.__extend_test(self.__float_list)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    sum(test_input),
                    Iterable(test_input).sum()
                )

    def test_sum_withStartValue_returnsSumWithStartValue(self):
        start = 10
        test_inputs = self.__extend_test(self.__int_list) + self.__extend_test(self.__float_list)

        for test_input in test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    sum(test_input, start),
                    Iterable(test_input).sum(start)
                )

    def test_zip_twoIterables_returnsProperZip(self):
        for left in self.__test_inputs:
            for right in self.__test_inputs:
                with self.subTest(left=left, right=right):
                    self.assertEqual(
                        Counter(list(zip(left, right))),
                        Counter(Iterable(left).zip(right).to_list())
                    )

    def test_zip_multipleIterables_returnsProperZip(self):
        right = self.__test_inputs

        for left in self.__test_inputs:
            with self.subTest(left=left, right=right):
                self.assertEqual(
                    Counter(list(zip(left, *right))),
                    Counter(Iterable(left).zip(*right).to_list())
                )

    def test_zip_iterableWithIterableObject_returnsProperZip(self):
        for left in self.__test_inputs:
            for right in self.__test_inputs:
                with self.subTest(left=left, right=right):
                    self.assertEqual(
                        Counter(zip(left, right)),
                        Counter(Iterable(left).zip(Iterable(right)))
                    )

    def test_zip_iterableWithMultipleIterableObjects_returnsProperZip(self):
        right = list(map(lambda x: Iterable(x), self.__test_inputs))
        for left in self.__test_inputs:
            with self.subTest(left=left, right=right):
                self.assertEqual(
                    Counter(zip(left, *right)),
                    Counter(Iterable(left).zip(*right))
                )

    def test_reduce_noInitializer_returnsValue(self):
        func = lambda a, b: a + b

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    reduce(func, test_input),
                    Iterable(test_input).reduce(func)
                )

    def test_reduce_withInitializer_returnsValueWithInitializer(self):
        func = lambda a, b: a + b

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                # Extract a random item to be the initializer
                initializer = set(test_input).pop()
                self.assertEqual(
                    reduce(func, test_input, initializer),
                    Iterable(test_input).reduce(func, initializer)
                )

    def test_contains_doesNotContainValue_returnsFalse(self):
        value_not_in_test_input = uuid.uuid4()

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertFalse(Iterable(test_input).contains(value_not_in_test_input))

    def test_contains_containsValue_returnsTrue(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                a_value_in_test_input = list(test_input)[-1]
                self.assertTrue(Iterable(test_input).contains(a_value_in_test_input))

    def test_is_empty_isNotEmpty_returnsFalse(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertFalse(Iterable(test_input).is_empty())

    def test_is_empty_isEmpty_returnsTrue(self):
        for test_input in self.__extend_test([]):
            self.assertTrue(Iterable(test_input).is_empty())

    def test_mapmany_eachElementMapsToList_returnsFlattenedIterable(self):
        function = lambda x: [x, x]

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                expected_output = list(test_input) + list(test_input)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(test_input).mapmany(function).to_list())
                )

    def test_mapmany_eachElementMapsToTuple_returnsFlattenedIterable(self):
        function = lambda x: (x, x)

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                expected_output = list(test_input) + list(test_input)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(test_input).mapmany(function).to_list())
                )

    def test_single_withFunc_returnsMatchingElement(self):
        test_inputs = [set(t) for t in self.__test_lists]

        for test_input in self.__extend_tests(test_inputs):
            with self.subTest(test_input=test_input):
                expected_value = list(test_input)[-1]
                func = lambda x: x == expected_value

                self.assertEqual(
                    expected_value,
                    Iterable(test_input).single(filter_by=func)
                )

    def test_single_emptyIterableWithNoDefault_returnsNone(self):
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).single()
                )

    def test_single_emptyIterableWithDefault_returnsDefault(self):
        default = "default"
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).single(default=default)
                )

    def test_single_noneMatchingFuncWithNoDefault_returnsNone(self):
        # create a func that should not match anything
        func = lambda x: x == uuid.uuid4()

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).single(filter_by=func)
                )

    def test_single_noneMatchingFuncWithDefault_returnsDefault(self):
        # create a func that should not match anything
        func = lambda x: x == uuid.uuid4()
        default = "default"

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).single(filter_by=func, default=default)
                )

    def test_single_iterableHasMoreThanOneValue_raisesValueError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(ValueError):
                    Iterable(test_input).single()

    def test_single_multipleMatchingFunc_RaisesValueError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                test_input_list = list(test_input)
                matching_values = {test_input_list[0], test_input_list[-1]}
                func = lambda x: x in matching_values

                with self.assertRaises(ValueError):
                    Iterable(test_input).single(filter_by=func)

    def test_concat_leftAndRightHasSameContents_returnsLeftConcatRight(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    Counter(list(test_input) + list(test_input)),
                    Counter(Iterable(test_input).concat(test_input).to_list())
                )

    def test_concat_leftAndRightHaveNoIntersectingValues_returnsLeftConcatRight(self):
        tests_list = [
            ([True], [False]),
            ([13, -5, 1982], [-10, 2384, 98]),
            ([6.837, -374.6, -2.73], [3.210, 2.038, -3927.23]),
            ("ab", "cd"),
            (["querty", "dvorak", "abcde"], ["orange", "black", "blue"]),
            ([TestIterableTestClazz(i) for i in range(0, 5)], [TestIterableTestClazz(i) for i in range(5, 9)])
        ]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = list(left) + list(right)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).concat(right).to_list())
                )

    def test_concat_leftAndRightHasSomeIntersectingValues_returnsLeftConcatRight(self):
        # Remove an element from both left and right
        tests_list = [(list(deepcopy(t))[1:], list(deepcopy(t))[:-1]) for t in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = list(left) + list(right)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).concat(right).to_list())
                )

    def test_concat_leftIsEmpty_returnsRight(self):
        for right in self.__test_inputs:
            with self.subTest(right=right):
                self.assertEqual(
                    Counter(list(right)),
                    Counter(Iterable([]).concat(right).to_list())
                )

    def test_concat_rightIsEmpty_returnsLeft(self):
        for left in self.__test_inputs:
            with self.subTest(left=left):
                self.assertEqual(
                    Counter(list(left)),
                    Counter(Iterable(left).concat([]).to_list())
                )

    def test_first_noArgs_returnsFirstElement(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                expected_first = list(test_input)[0]

                self.assertEqual(
                    expected_first,
                    Iterable(test_input).first()
                )

    def test_first_withFunc_returnsFirstMatchingElement(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                expected_first = list(test_input)[-1]
                func = lambda x: x == expected_first

                self.assertEqual(
                    expected_first,
                    Iterable(test_input).first(function=func)
                )

    def test_first_emptyIterableWithNoDefault_returnsNone(self):
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).first()
                )

    def test_first_emptyIterableWithDefault_returnsDefault(self):
        default = "default"
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).first(default=default)
                )

    def test_first_noneMatchingFuncWithNoDefault_returnsNone(self):
        # create a func that should not match anything
        func = lambda x: x == '32bf4b67-42f6-4a86-8229-aa10da364ff7'

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).first(function=func)
                )

    def test_first_noneMatchingFuncWithDefault_returnsDefault(self):
        # create a func that should not match anything
        func = lambda x: x == '32bf4b67-42f6-4a86-8229-aa10da364ff7'
        default = "default"

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).first(function=func, default=default)
                )

    def test_get_indexInsideBounds_returnsValue(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                index = int(len(test_input) / 2)

                self.assertEqual(
                    list(test_input)[index],
                    Iterable(test_input).get(index)
                )

    def test_get_indexIsZero_returnsFirstValue(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    list(test_input)[0],
                    Iterable(test_input).get(0)
                )

    def test_get_indexIsLastElement_returnsLastValue(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                last_element = len(test_input) - 1

                self.assertEqual(
                    list(test_input)[last_element],
                    Iterable(test_input).get(last_element)
                )

    def test_get_indexLessThanZero_raisesIndexError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(IndexError):
                    Iterable(test_input).get(-1)

    def test_get_indexTooLarge_raisesIndexError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(IndexError):
                    Iterable(test_input).get(len(test_input))

    def test_last_noArgs_returnsLastElement(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                expected_last = list(test_input)[-1]

                self.assertEqual(
                    expected_last,
                    Iterable(test_input).last()
                )

    def test_last_withFunc_returnsLastMatchingElement(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                expected_last = list(test_input)[-1]
                func = lambda x: x == expected_last

                self.assertEqual(
                    expected_last,
                    Iterable(test_input).last(filter_by=func)
                )

    def test_last_emptyIterableWithNoDefault_returnsNone(self):
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).last()
                )

    def test_last_emptyIterableWithDefault_returnsDefault(self):
        default = "default"
        for test_input in self.__extend_test([]):
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).last(default=default)
                )

    def test_last_noneMatchingFuncWithNoDefault_returnsNone(self):
        # create a func that should not match anything
        func = lambda x: x == uuid.uuid4()

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    None,
                    Iterable(test_input).last(filter_by=func)
                )

    def test_last_noneMatchingFuncWithDefault_returnsDefault(self):
        # create a func that should not match anything
        func = lambda x: x == uuid.uuid4()
        default = "default"

        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    default,
                    Iterable(test_input).last(filter_by=func, default=default)
                )

    def test_skip_countIsZero_returnsIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    list(test_input),
                    Iterable(test_input).skip(0).to_list()
                )

    def test_skip_countIsSmallerThanLengthOfIterable_returnsSubsetOfIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                count = int(len(test_input) / 2)

                self.assertEqual(
                    list(test_input)[count:],
                    Iterable(test_input).skip(count).to_list()
                )

    def test_skip_countIsExactlyLengthOfIterable_returnsEmptyIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    [],
                    Iterable(test_input).skip(len(test_input)).to_list()
                )

    def test_skip_countIsGreaterThanLengthOfIterable_returnsEmptyIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    [],
                    Iterable(test_input).skip(len(test_input) + 1).to_list()
                )

    def test_skip_countIsNegative_raisesValueError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(ValueError):
                    Iterable(test_input).skip(-1)

    def test_take_countIsZero_returnsEmptyIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    [],
                    Iterable(test_input).take(0).to_list()
                )

    def test_take_countIsSmallerThanLengthOfIterable_returnsSubsetOfIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                prefix_length = int(len(test_input) / 2)

                self.assertEqual(
                    list(test_input)[:prefix_length],
                    Iterable(test_input).take(prefix_length).to_list()
                )

    def test_take_countIsExactlyLengthOfIterable_returnsIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                length = len(test_input)

                self.assertEqual(
                    list(test_input),
                    Iterable(test_input).take(length).to_list()
                )

    def test_take_countIsGreaterThanLengthOfIterable_returnsIterable(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                length = len(test_input) + 1

                self.assertEqual(
                    list(test_input),
                    Iterable(test_input).take(length).to_list()
                )

    def test_take_countIsNegative_raisesValueError(self):
        for test_input in self.__test_inputs:
            with self.subTest(test_input=test_input):
                with self.assertRaises(ValueError):
                    Iterable(test_input).take(-1)

    def test_difference_leftAndRightHasSameContents_returnsEmptyIterable(self):
        tests = [(left, deepcopy(left)) for left in self.__test_inputs]

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable(left).difference(right).to_list())
                )

    def test_difference_leftIsSupersetOfRight_returnsElementsFromLeft(self):
        # Remove an element from right
        tests_list = [(left, left[:-1]) for left in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).difference(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).difference(right).to_list())
                )

    def test_difference_leftIsSubsetOfRight_returnsEmptyIterable(self):
        # Remove an element from right
        tests_list = [(list(deepcopy(right))[1:], right) for right in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable(left).difference(right).to_list())
                )

    def test_difference_leftAndRightHasSomeIntersectingValues_returnsElementsFromLeft(self):
        # Remove an element from both left and right
        tests_list = [(list(deepcopy(t))[1:], list(deepcopy(t))[:-1]) for t in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).difference(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).difference(right).to_list())
                )

    def test_difference_leftAndRightHasNoIntersectingValues_returnsAllDistinctElementsOfLeft(self):
        tests_list = [
            ([True], [False]),
            ([13, -5, 1982], [-10, 2384, 98]),
            ([6.837, -374.6, -2.73], [3.210, 2.038, -3927.23]),
            ("ab", "cd"),
            (["querty", "dvorak", "abcde"], ["orange", "black", "blue"]),
            ([TestIterableTestClazz(i) for i in range(0, 5)], [TestIterableTestClazz(i) for i in range(5, 9)])
        ]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                self.assertEqual(
                    Counter(set(left)),
                    Counter(Iterable(left).difference(right).to_list())
                )

    def test_difference_leftIsEmpty_returnsEmptyIterable(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for right in tests:
            with self.subTest(right=right):
                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable([]).difference(right).to_list())
                )

    def test_difference_rightIsEmpty_returnsAllDistinctElementsOfLeft(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for left in tests:
            with self.subTest(left=left):
                self.assertEqual(
                    Counter(set(left)),
                    Counter(Iterable(left).difference([]).to_list())
                )

    def test_distinct_returnsDistinctIterable(self):
        tests_list = [
            [True, False, False, True, True],
            [3, 2, 2, -5, 7],
            [3.42, 828.3, -6.4, -6.4, 5.99],
            "aabaaydddk;eadddd",
            ["orange", "black", "blue", "black", "white"],
            [TestIterableTestClazz(5), TestIterableTestClazz("cloud"), TestIterableTestClazz("cloud")]
        ]
        tests = self.__extend_tests(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                self.assertEqual(
                    Counter(list(set(test_input))),
                    Counter(Iterable(test_input).distinct().to_list())
                )

    def test_intersection_leftAndRightHasSameContents_returnsLeft(self):
        tests = [(left, deepcopy(left)) for left in self.__test_inputs]

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).intersection(right).to_list())
                )

    def test_intersection_leftIsSupersetOfRight_returnsRight(self):
        # Remove an element from right
        tests_list = [(left, left[:-1]) for left in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(right)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).intersection(right).to_list())
                )

    def test_intersection_leftIsSubsetOfRight_returnsLeft(self):
        # Remove an element from right
        tests_list = [(list(deepcopy(right))[1:], right) for right in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).intersection(right).to_list())
                )

    def test_intersection_leftAndRightHasSomeIntersectingValues_returnsIntersection(self):
        # Remove an element from both left and right
        tests_list = [(list(deepcopy(t))[1:], list(deepcopy(t))[:-1]) for t in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).intersection(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).intersection(right).to_list())
                )

    def test_intersection_leftAndRightHasNoIntersectingValues_returnsEmptyIterable(self):
        tests_list = [
            ([True], [False]),
            ([13, -5, 1982], [-10, 2384, 98]),
            ([6.837, -374.6, -2.73], [3.210, 2.038, -3927.23]),
            ("ab", "cd"),
            (["querty", "dvorak", "abcde"], ["orange", "black", "blue"]),
            ([TestIterableTestClazz(i) for i in range(0, 5)], [TestIterableTestClazz(i) for i in range(5, 9)])
        ]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable(left).intersection(right).to_list())
                )

    def test_intersection_leftIsEmpty_returnsEmptyIterable(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for right in tests:
            with self.subTest(right=right):
                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable([]).intersection(right).to_list())
                )

    def test_intersection_rightIsEmpty_returnsEmptyIterable(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for left in tests:
            with self.subTest(left=left):
                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable(left).intersection([]).to_list())
                )

    def test_symmetric_difference_leftAndRightHasSameContents_returnsEmptyIterable(self):
        tests = [(left, deepcopy(left)) for left in self.__test_inputs]

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                self.assertEqual(
                    Counter(list()),
                    Counter(Iterable(left).symmetric_difference(right).to_list())
                )

    def test_symmetric_difference_leftIsSupersetOfRight_returnsElementsFromLeft(self):
        # Remove an element from right
        tests_list = [(left, left[:-1]) for left in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).symmetric_difference(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).symmetric_difference(right).to_list())
                )

    def test_symmetric_difference_leftIsSubsetOfRight_returnsElementsFromRight(self):
        # Remove an element from right
        tests_list = [(list(deepcopy(right))[1:], right) for right in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).symmetric_difference(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).symmetric_difference(right).to_list())
                )

    def test_symmetric_difference_leftAndRightHasSomeIntersectingValues_returnsNonIntersectingValues(self):
        # Remove an element from both left and right
        tests_list = [(list(deepcopy(t))[1:], list(deepcopy(t))[:-1]) for t in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).symmetric_difference(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).symmetric_difference(right).to_list())
                )

    def test_symmetric_difference_leftAndRightHasNoIntersectingValues_returnsLeftUnionRight(self):
        tests_list = [
            ([True], [False]),
            ([13, -5, 1982], [-10, 2384, 98]),
            ([6.837, -374.6, -2.73], [3.210, 2.038, -3927.23]),
            ("ab", "cd"),
            (["querty", "dvorak", "abcde"], ["orange", "black", "blue"]),
            ([TestIterableTestClazz(i) for i in range(0, 5)], [TestIterableTestClazz(i) for i in range(5, 9)])
        ]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).union(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).symmetric_difference(right).to_list())
                )

    def test_symmetric_difference_leftIsEmpty_returnsAllDistinctElementsOfRight(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for right in tests:
            with self.subTest(right=right):
                self.assertEqual(
                    Counter(set(right)),
                    Counter(Iterable([]).symmetric_difference(right).to_list())
                )

    def test_symmetric_difference_rightIsEmpty_returnsAllDistinctElementsOfLeft(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for left in tests:
            with self.subTest(left=left):
                self.assertEqual(
                    Counter(set(left)),
                    Counter(Iterable(left).symmetric_difference([]).to_list())
                )

    def test_union_leftAndRightHasSameContents_returnsLeft(self):
        tests = [(left, deepcopy(left)) for left in self.__test_inputs]

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).union(right).to_list())
                )

    def test_union_leftIsSupersetOfRight_returnsLeft(self):
        # Remove an element from right
        tests_list = [(left, left[:-1]) for left in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).union(right).to_list())
                )

    def test_union_leftIsSubsetOfRight_returnsRight(self):
        # Remove an element from right
        tests_list = [(list(deepcopy(right))[1:], right) for right in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)
        
        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(right)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).union(right).to_list())
                )

    def test_union_leftAndRightHasSomeIntersectingValues_returnsUnionOfLeftAndRight(self):
        # Remove an element from both left and right
        tests_list = [(list(deepcopy(t))[1:], list(deepcopy(t))[:-1]) for t in self.__test_lists]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = set(left).union(set(right))

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).union(right).to_list())
                )

    def test_union_leftAndRightHasNoIntersectingValues_returnsLeftUnionRight(self):
        tests_list = [
            ([True], [False]),
            ([13, -5, 1982], [-10, 2384, 98]),
            ([6.837, -374.6, -2.73], [3.210, 2.038, -3927.23]),
            ("ab", "cd"),
            (["querty", "dvorak", "abcde"], ["orange", "black", "blue"]),
            ([TestIterableTestClazz(i) for i in range(0, 5)], [TestIterableTestClazz(i) for i in range(5, 9)])
        ]
        tests = self._extend_test_tuples(tests_list)

        for test_input in tests:
            with self.subTest(test_input=test_input):
                left = test_input[0]
                right = test_input[1]

                expected_output = list(left) + list(right)

                self.assertEqual(
                    Counter(expected_output),
                    Counter(Iterable(left).union(right).to_list())
                )

    def test_union_leftIsEmpty_returnsAllDistinctElementsOfRight(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for right in tests:
            with self.subTest(right=right):
                self.assertEqual(
                    Counter(set(right)),
                    Counter(Iterable([]).union(right).to_list())
                )

    def test_union_rightIsEmpty_returnsAllDistinctElementsOfLeft(self):
        # Add a duplicate element
        tests_list = list(map(lambda t: t + t[:1], self.__test_lists))
        tests = self.__extend_tests(tests_list)

        for left in tests:
            with self.subTest(left=left):
                self.assertEqual(
                    Counter(set(left)),
                    Counter(Iterable(left).union([]).to_list())
                )