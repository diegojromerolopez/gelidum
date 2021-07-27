import unittest
from typing import Any, Iterator

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

        frozen_list = frozenlist([1, "2", Dummy(3)])

        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual("2", frozen_list[1])
        self.assertTrue(isinstance(frozen_list[2], FrozenBase))
        self.assertEqual(3, frozen_list[2].value)

    def test_construction_from_tuple(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_list = frozenlist((1, "2", Dummy(3)))

        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual("2", frozen_list[1])
        self.assertTrue(isinstance(frozen_list[2], FrozenBase))
        self.assertEqual(3, frozen_list[2].value)

    def test_construction_from_generator(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        def generator():
            yield 1
            yield "2"
            yield Dummy(3)

        frozen_list = frozenlist(generator())

        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual("2", frozen_list[1])
        self.assertTrue(isinstance(frozen_list[2], FrozenBase))
        self.assertEqual(3, frozen_list[2].value)

    def test_setattr_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            setattr(frozen_list, "my_attr", "value")

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_count(self):
        frozen_list = frozenlist([1, 2, 3, 2, 3, 8, 3])

        self.assertEqual(1, frozen_list.count(1))
        self.assertEqual(2, frozen_list.count(2))
        self.assertEqual(3, frozen_list.count(3))
        self.assertEqual(1, frozen_list.count(8))
        self.assertEqual(0, frozen_list.count(10))

    def test_len(self):
        frozen_list = frozenlist([1, 2, 3])

        self.assertEqual(3, len(frozen_list))

    def test_add(self):
        frozen_list = frozenlist([1, 2, 3])
        frozen_list2 = frozen_list + frozenlist([2])

        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertTrue(isinstance(frozen_list2, FrozenBase))
        self.assertEqual(4, len(frozen_list2))
        self.assertEqual(1, frozen_list2[0])
        self.assertEqual(2, frozen_list2[1])
        self.assertEqual(3, frozen_list2[2])
        self.assertEqual(2, frozen_list2[3])

    def test_hash(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_list = frozenlist([1, 2, 3, [4, 5, 6], Dummy(2)])

        self.assertTrue(isinstance(hash(frozen_list), int))

    def test_mul(self):
        frozen_list = frozenlist([1, 2, 3])
        frozen_list2 = frozen_list * 2

        self.assertNotEqual(id(frozen_list), id(frozen_list2))
        self.assertTrue(isinstance(frozen_list2, FrozenBase))
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

    def test_slice(self):
        frozen_list = frozenlist([1, 2, 3])
        frozen_list_slice_2_items = frozen_list[0:2]
        frozen_list_slice_all_items = frozen_list[0:6]

        self.assertNotEqual(id(frozen_list), id(frozen_list_slice_2_items))
        self.assertNotEqual(id(frozen_list), id(frozen_list_slice_all_items))
        self.assertTrue(isinstance(frozen_list_slice_2_items, FrozenBase))
        self.assertEqual(2, len(frozen_list_slice_2_items))
        self.assertEqual(1, frozen_list_slice_2_items[0])
        self.assertEqual(2, frozen_list_slice_2_items[1])
        self.assertTrue(isinstance(frozen_list_slice_all_items, FrozenBase))
        self.assertEqual(3, len(frozen_list_slice_all_items))
        self.assertEqual(1, frozen_list_slice_all_items[0])
        self.assertEqual(2, frozen_list_slice_all_items[1])
        self.assertEqual(3, frozen_list_slice_all_items[2])

    def test_contains(self):
        frozen_list = frozenlist([1, 2, 3])

        self.assertTrue(1 in frozen_list)
        self.assertFalse(9 in frozen_list)

    def test_min(self):
        frozen_list = frozenlist([1, 2, 3])

        self.assertEqual(1, min(frozen_list))

    def test_max(self):
        frozen_list = frozenlist([1, 2, 3])

        self.assertEqual(3, max(frozen_list))

    def test_iter(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(9))
        frozen_list = frozenlist([1, 2, 3, frozen_dummy])
        items = []
        for item in frozen_list:
            items.append(item)

        self.assertListEqual([1, 2, 3, frozen_dummy], items)

    def test_next(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(9))
        frozen_list = frozenlist([1, 2, 3, frozen_dummy])
        frozen_list_iter = iter(frozen_list)

        self.assertEqual(1, next(frozen_list_iter))
        self.assertEqual(2, next(frozen_list_iter))
        self.assertEqual(3, next(frozen_list_iter))
        self.assertEqual(frozen_dummy, next(frozen_list_iter))

    def test_reversed(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_list = frozenlist([1, 2, 3, Dummy(9)])
        reversed_frozen_list = reversed(frozen_list)

        self.assertNotEqual(id(frozen_list), id(reversed_frozen_list))
        self.assertEqual(4, len(frozen_list))
        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertEqual(3, frozen_list[2])
        self.assertTrue(isinstance(frozen_list, FrozenBase))
        self.assertEqual(9, frozen_list[3].value)
        self.assertTrue(isinstance(reversed_frozen_list, Iterator))
        self.assertEqual(9, next(reversed_frozen_list).value)
        self.assertEqual(3, next(reversed_frozen_list))
        self.assertEqual(2, next(reversed_frozen_list))
        self.assertEqual(1, next(reversed_frozen_list))

    def test_copy(self):
        frozen_list = frozenlist([1, 2, 3])

        frozen_list_copy = frozen_list.copy()

        self.assertEqual(id(frozen_list_copy), id(frozen_list))

    def test_getitem(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(IndexError) as context:
            _val = frozen_list[4]

        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertEqual("frozenlist index out of range",
                         str(context.exception))

    def test_setitem_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list[0] = 11

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_append_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.append(4)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_extend_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.extend([4])

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_insert_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.insert(i=4, x=2)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_remove_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.remove(4)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_pop_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.pop(items=4)

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_clear_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.clear()

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_index_ok(self):
        frozen_list = frozenlist([1, 2, 3, 4, 5, 6, 7])

        index_for_2 = frozen_list.index(2)
        index_for_4_from_1_to_10 = frozen_list.index(4, 1, 10)

        with self.assertRaises(ValueError) as context_12:
            frozen_list.index(12)

        with self.assertRaises(ValueError) as context_2_from_5_to_10:
            frozen_list.index(2, 5, 10)

        self.assertEqual(1, index_for_2)
        self.assertEqual(3, index_for_4_from_1_to_10)
        self.assertEqual("12 is not in frozenlist",
                         str(context_12.exception))
        self.assertEqual("2 is not in frozenlist",
                         str(context_2_from_5_to_10.exception))

    def test_sort_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.sort()

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))

    def test_reverse_exception(self):
        frozen_list = frozenlist([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_list.reverse()

        self.assertEqual("'frozenlist' object is immutable",
                         str(context.exception))


