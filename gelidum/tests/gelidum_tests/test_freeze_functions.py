import unittest
import warnings

from gelidum import FrozenException, freeze
from gelidum.frozen import clear_frozen_classes


class TestFreezeFunctions(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_freeze_function_and_reading_attributes(self) -> None:
        def times() -> None:
            pass  # pragma: no cover

        times.factor = 3

        frozen_times = freeze(times)

        self.assertEqual(3, frozen_times.factor)
        self.assertNotEqual(id(times), id(frozen_times))

    def test_freeze_function_inplace_is_ignored(self) -> None:
        def times() -> None:
            pass  # pragma: no cover

        times.factor = 3

        frozen_times = freeze(times, on_freeze='inplace')

        self.assertEqual(3, frozen_times.factor)
        self.assertNotEqual(id(times), id(frozen_times))

    def test_freeze_function_and_writing_attributes_with_exception(self):
        def times() -> None:
            pass  # pragma: no cover

        times.factor = 3

        frozen_times = freeze(times)

        with self.assertRaises(FrozenException) as context:
            frozen_times.factor = 10

        self.assertEqual('Can\'t assign attribute \'factor\' on immutable instance', str(context.exception))

    def test_freeze_function_and_writing_frozen_attributes_with_exception(self) -> None:
        def times() -> None:
            pass  # pragma: no cover

        times.cache = {}

        frozen_times = freeze(times)

        with self.assertRaises(FrozenException) as context:
            frozen_times.cache[10] = 789

        self.assertEqual("'frozendict' object is immutable", str(context.exception))

    def test_freeze_function_and_writing_attributes_with_function(self) -> None:
        def times() -> None:
            pass  # pragma: no cover

        times.factor = 3

        frozen_times = freeze(times, on_update='warning')

        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_times.factor = 10

        self.assertListEqual(
            ["Can't assign attribute 'factor' on immutable instance"],
            [str(warn.message) for warn in caught_warnings],
        )
