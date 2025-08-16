import unittest

from gelidum import (
    freeze,
    isfrozen,
)
from gelidum.frozen import clear_frozen_classes


class TestIsFrozen(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_immutable_builtin_objects(self) -> None:
        self.assertTrue(isfrozen(3))
        self.assertTrue(isfrozen(3.9))
        self.assertTrue(isfrozen(True))
        self.assertTrue(isfrozen(False))
        self.assertTrue(isfrozen(None))
        self.assertTrue(isfrozen(complex(1, 2)))
        self.assertTrue(isfrozen(b'Bytes'))
        self.assertTrue(isfrozen('String'))

    def test_dict(self) -> None:
        my_dict = {
            'a': 1,
        }

        self.assertFalse(isfrozen(my_dict))

    def test_frozendict(self) -> None:
        my_dict = {
            'a': 1,
        }
        frozen_dict = freeze(my_dict)

        self.assertTrue(isfrozen(frozen_dict))

    def test_list(self) -> None:
        my_list = [1, 2, 3]

        self.assertFalse(isfrozen(my_list))

    def test_frozenlist(self) -> None:
        my_list = [1, 2, 3]

        frozen_set = freeze(my_list)

        self.assertTrue(isfrozen(frozen_set))

    def test_set(self) -> None:
        my_set = {'a', 'b', 'c'}

        self.assertFalse(isfrozen(my_set))

    def test_frozenset(self) -> None:
        my_set = {'a', 'b', 'c'}
        frozen_set = freeze(my_set)

        self.assertTrue(isfrozen(frozen_set))

    def test_on_object(self):
        dummy1 = object()

        self.assertFalse(isfrozen(dummy1))

    def test_on_frozen_object(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

        dummy1 = Dummy(value=1)
        frozen_dummy1 = freeze(dummy1, on_freeze='copy')

        self.assertTrue(isfrozen(frozen_dummy1))
