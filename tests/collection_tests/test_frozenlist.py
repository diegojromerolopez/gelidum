import unittest
from typing import Any

from gelidum import FrozenException, freeze
from gelidum.collections.frozenlist import frozenlist
from gelidum.frozen import FrozenBase


class TestFrozenlist(unittest.TestCase):  # noqa
    def test_empty_construction(self):
        frozen_list = frozenlist()

        self.assertEqual(0, len(frozen_list))

    def test_construction(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_list = frozenlist(1, "2", Dummy(3))

        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual("2", frozen_list[1])
        self.assertTrue(isinstance(frozen_list[2], FrozenBase))
        self.assertEqual(3, frozen_list[2].value)

    def test_setattr_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            setattr(frozen_list, "my_attr", "value")

        self.assertEqual("Can't assign attribute 'my_attr' on immutable instance",
                         str(context.exception))

    def test_len(self):
        frozen_list = frozenlist(1, 2, 3)

        self.assertEqual(3, len(frozen_list))

    def test_add(self):
        frozen_list = frozenlist(1, 2, 3)
        frozen_list2 = frozen_list + 2

        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertEqual(4, len(frozen_list2))
        self.assertEqual(1, frozen_list2[0])
        self.assertEqual(2, frozen_list2[1])
        self.assertEqual(3, frozen_list2[2])
        self.assertEqual(2, frozen_list2[3])

    def test_mul(self):
        frozen_list = frozenlist(1, 2, 3)
        frozen_list2 = frozen_list * 2

        self.assertNotEqual(id(frozen_list), id(frozen_list2))
        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertTrue(isinstance(frozen_list2, FrozenBase))
        self.assertEqual(6, len(frozen_list2))
        self.assertEqual(1, frozen_list2[0])
        self.assertEqual(2, frozen_list2[1])
        self.assertEqual(3, frozen_list2[2])
        self.assertEqual(1, frozen_list2[3])
        self.assertEqual(2, frozen_list2[4])
        self.assertEqual(3, frozen_list2[5])

    def test_contains(self):
        frozen_list = frozenlist(1, 2, 3)

        self.assertTrue(1 in frozen_list)
        self.assertFalse(9 in frozen_list)

    def test_iter(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(9))
        frozen_list = frozenlist(1, 2, 3, frozen_dummy)
        items = []
        for item in frozen_list:
            items.append(item)

        self.assertListEqual([1, 2, 3, frozen_dummy], items)

    def test_next(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(9))
        frozen_list = frozenlist(1, 2, 3, frozen_dummy)
        frozen_list_iter = iter(frozen_list)

        self.assertEqual(1, next(frozen_list_iter))
        self.assertEqual(2, next(frozen_list_iter))
        self.assertEqual(3, next(frozen_list_iter))
        self.assertEqual(frozen_dummy, next(frozen_list_iter))

    def test_reversed(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_list = frozenlist(1, 2, 3, Dummy(9))
        reversed_frozen_list = reversed(frozen_list)

        self.assertNotEqual(id(frozen_list), id(reversed_frozen_list))
        self.assertEqual(4, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertEqual(3, frozen_list[2])
        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(9, frozen_list[3].value)

        self.assertEqual(4, len(reversed_frozen_list))
        self.assertTrue(isinstance(reversed_frozen_list, FrozenBase))
        self.assertEqual(9, reversed_frozen_list[0].value)
        self.assertEqual(3, reversed_frozen_list[1])
        self.assertEqual(2, reversed_frozen_list[2])
        self.assertEqual(1, reversed_frozen_list[3])

    def test_getitem(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(IndexError) as context:
            _val = frozen_list[4]

        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertEqual("frozenlist index out of range",
                         str(context.exception))

    def test_setitem_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list[0] = 11

        self.assertEqual("Can't set key '0' on immutable instance",
                         str(context.exception))

    def test_append_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.append(4)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_extend_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.extend([4])

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_insert_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.insert(i=4, x=2)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_remove_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.remove(4)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_pop_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.pop(items=4)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_clear_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.clear()

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_index_ok(self):
        frozen_list = frozenlist(1, 2, 3)

        index = frozen_list.index(2)

        self.assertEqual(1, index)

    def test_sort_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.sort()

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_reverse_exception(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(FrozenException) as context:
            frozen_list.reverse()

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))


