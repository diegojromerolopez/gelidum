import unittest
from typing import Any

from gelidum import FrozenException, freeze
from gelidum.collections.frozenzet import frozenzet
from gelidum.frozen import FrozenBase


class TestFrozenzet(unittest.TestCase):  # noqa
    def test_empty_construction(self):
        frozen_zet = frozenzet()

        self.assertEqual(0, len(frozen_zet))

    def test_construction(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_zet = frozenzet([Dummy(1), Dummy(2), Dummy(3)])
        unfrozen_list = sorted(list(frozen_zet), key=lambda d: d.value)

        self.assertTrue(isinstance(frozen_zet, FrozenBase))
        self.assertEqual(3, len(frozen_zet))
        self.assertEqual(3, len(unfrozen_list))
        self.assertTrue(isinstance(unfrozen_list[0], FrozenBase))
        self.assertEqual(1, unfrozen_list[0].value)
        self.assertTrue(isinstance(unfrozen_list[1], FrozenBase))
        self.assertEqual(2, unfrozen_list[1].value)
        self.assertTrue(isinstance(unfrozen_list[2], FrozenBase))
        self.assertEqual(3, unfrozen_list[2].value)

    def test_construction_from_tuple(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

            def __lt__(self, other):
                return self.value < int(other)

        dummy = Dummy(3)
        frozen_dummy = freeze(dummy)
        frozen_zet = frozenzet((1, "2", frozen_dummy))

        self.assertTrue(isinstance(frozen_zet, FrozenBase))
        self.assertEqual(3, len(frozen_zet))
        self.assertTrue(1 in frozen_zet)
        self.assertTrue("2" in frozen_zet)
        self.assertFalse(dummy in frozen_zet)
        self.assertTrue(frozen_dummy in frozen_zet)

    def test_construction_from_generator(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        def generator():
            yield Dummy(1)
            yield Dummy(2)
            yield Dummy(3)

        frozen_zet = frozenzet(generator())
        unfrozen_list = sorted(list(frozen_zet), key=lambda d: d.value)

        self.assertTrue(isinstance(frozen_zet, FrozenBase))
        self.assertEqual(3, len(frozen_zet))
        self.assertEqual(3, len(unfrozen_list))
        self.assertTrue(isinstance(unfrozen_list[0], FrozenBase))
        self.assertEqual(1, unfrozen_list[0].value)
        self.assertTrue(isinstance(unfrozen_list[1], FrozenBase))
        self.assertEqual(2, unfrozen_list[1].value)
        self.assertTrue(isinstance(unfrozen_list[2], FrozenBase))
        self.assertEqual(3, unfrozen_list[2].value)

    def test_castings(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

            def __str__(self) -> str:
                return f"{self.value}"

        dummy = Dummy(3)
        frozen_dummy = freeze(dummy)

        self.assertEqual(
            {1, "2", frozen_dummy},
            set(frozenzet((1, "2", frozen_dummy)))
        )
        self.assertEqual(
            [1, "2", frozen_dummy],
            sorted(list(frozenzet((1, "2", frozen_dummy))), key=lambda e: str(e))
        )

    def test_setattr_exception(self):
        frozen_zet = frozenzet([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            setattr(frozen_zet, "my_attr", "value")

        self.assertEqual("'frozenzet' object is immutable",
                         str(context.exception))

    def test_len(self):
        frozen_zet = frozenzet([1, 2, 3])

        self.assertEqual(3, len(frozen_zet))

    def test_add(self):
        frozen_zet = frozenzet([1, 2, 3])
        unfrozen_list = list(frozen_zet)
        frozen_zet2 = frozen_zet + frozenzet([1, 2]) + frozenzet([2, 3, 4])
        unfrozen_list2 = list(frozen_zet2)
        unfrozen_set2 = set(frozen_zet2)

        self.assertTrue(isinstance(frozen_zet, FrozenBase))
        self.assertEqual(3, len(frozen_zet))
        self.assertEqual(3, len(unfrozen_list))
        self.assertEqual(1, unfrozen_list[0])
        self.assertEqual(2, unfrozen_list[1])
        self.assertEqual(3, unfrozen_list[2])
        self.assertTrue(1 in frozen_zet)
        self.assertTrue(2 in frozen_zet)
        self.assertTrue(3 in frozen_zet)
        self.assertTrue(isinstance(frozen_zet2, FrozenBase))
        self.assertEqual(4, len(frozen_zet2))
        self.assertEqual(4, len(unfrozen_list2))
        self.assertEqual(4, len(unfrozen_set2))
        self.assertEqual(1, unfrozen_list2[0])
        self.assertEqual(2, unfrozen_list2[1])
        self.assertEqual(3, unfrozen_list2[2])
        self.assertEqual(4, unfrozen_list2[3])
        self.assertTrue(1 in unfrozen_set2)
        self.assertTrue(2 in unfrozen_set2)
        self.assertTrue(3 in unfrozen_set2)
        self.assertTrue(4 in unfrozen_set2)
        self.assertTrue(1 in frozen_zet2)
        self.assertTrue(2 in frozen_zet2)
        self.assertTrue(3 in frozen_zet2)
        self.assertTrue(4 in frozen_zet2)

    def test_hash(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_zet = frozenzet([
            1, 2, 3, [4, 5, 6], Dummy(2),
            frozenzet({6, 7})
        ])

        self.assertTrue(isinstance(hash(frozen_zet), int))

    def test_contains(self):
        frozen_zet = frozenzet([1, 2, 3])

        self.assertTrue(1 in frozen_zet)
        self.assertFalse(1 not in frozen_zet)
        self.assertTrue(9 not in frozen_zet)
        self.assertFalse(9 in frozen_zet)

    def test_subset_superset(self):
        frozen_zet = frozenzet([1, 2, 3])
        frozen_zet_copy = frozenzet([1, 2, 3])
        superset_frozen_zet = frozenzet([1, 2, 3, 4, 5,6])

        self.assertTrue(superset_frozen_zet.issuperset(frozen_zet))
        self.assertTrue(superset_frozen_zet >= frozen_zet)
        self.assertFalse(frozen_zet_copy > frozen_zet)
        self.assertTrue(frozen_zet_copy >= frozen_zet)
        self.assertTrue(superset_frozen_zet > frozen_zet)
        self.assertTrue(frozen_zet.issubset(superset_frozen_zet))
        self.assertTrue(frozen_zet <= superset_frozen_zet)
        self.assertTrue(frozen_zet < superset_frozen_zet)
        self.assertFalse(frozen_zet_copy < frozen_zet)
        self.assertTrue(frozen_zet_copy <= frozen_zet)

    def test_min(self):
        frozen_zet = frozenzet([1, 2, 3])

        self.assertEqual(1, min(frozen_zet))

    def test_max(self):
        frozen_zet = frozenzet([1, 2, 3])

        self.assertEqual(3, max(frozen_zet))

    def test_iter(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(9))
        frozen_zet = frozenzet([1, 2, 3, frozen_dummy])
        items = set()
        for item in frozen_zet:
            items.add(item)

        self.assertSetEqual({1, 2, 3, frozen_dummy}, items)

    def test_next(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(9))
        frozen_zet = frozenzet([1, 2, 3, frozen_dummy])
        frozen_list_iter = iter(frozen_zet)

        items = set()
        for _ in frozen_zet:
            items.add(next(frozen_list_iter))

        self.assertSetEqual({1, 2, 3, frozen_dummy}, items)

    def test_copy(self):
        frozen_zet = frozenzet([1, 2, 3])

        frozen_zet_copy = frozen_zet.copy()

        self.assertEqual(id(frozen_zet_copy), id(frozen_zet))

    def test_add_exception(self):
        frozen_zet = frozenzet([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_zet.add(11)

        self.assertEqual("'frozenzet' object is immutable",
                         str(context.exception))

    def test_remove_exception(self):
        frozen_zet = frozenzet([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_zet.remove(2)

        self.assertEqual("'frozenzet' object is immutable",
                         str(context.exception))

    def test_pop_exception(self):
        frozen_zet = frozenzet([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_zet.pop()

        self.assertEqual("'frozenzet' object is immutable",
                         str(context.exception))

    def test_clear_exception(self):
        frozen_zet = frozenzet([1, 2, 3])

        with self.assertRaises(FrozenException) as context:
            frozen_zet.clear()

        self.assertEqual("'frozenzet' object is immutable",
                         str(context.exception))

    def test_update_exception(self):
        frozen_zet = frozenzet([1, 2, 3])
        frozen_zet2 = frozenzet([4, 5, 6])

        with self.assertRaises(FrozenException) as context1:
            frozen_zet.update(frozen_zet2)

        with self.assertRaises(FrozenException) as context2:
            frozen_zet |= frozen_zet2

        self.assertEqual("'frozenzet' object is immutable",
                         str(context1.exception))
        self.assertEqual("'frozenzet' object is immutable",
                         str(context2.exception))

    def test_intersection_update_exception(self):
        frozen_zet = frozenzet([1, 2, 3])
        frozen_zet2 = frozenzet([4, 5, 6])

        with self.assertRaises(FrozenException) as context1:
            frozen_zet.intersection_update(frozen_zet2)

        with self.assertRaises(FrozenException) as context2:
            frozen_zet &= frozen_zet2

        self.assertEqual("'frozenzet' object is immutable",
                         str(context1.exception))
        self.assertEqual("'frozenzet' object is immutable",
                         str(context2.exception))

    def test_difference_update_exception(self):
        frozen_zet = frozenzet([1, 2, 3])
        frozen_zet2 = frozenzet([4, 5, 6])

        with self.assertRaises(FrozenException) as context1:
            frozen_zet.difference_update(frozen_zet2)

        with self.assertRaises(FrozenException) as context2:
            frozen_zet -= frozen_zet2

        self.assertEqual("'frozenzet' object is immutable",
                         str(context1.exception))
        self.assertEqual("'frozenzet' object is immutable",
                         str(context2.exception))

    def test_symmetric_difference_update_exception(self):
        frozen_zet = frozenzet([1, 2, 3])
        frozen_zet2 = frozenzet([4, 5, 6])

        with self.assertRaises(FrozenException) as context1:
            frozen_zet.symmetric_difference_update(frozen_zet2)

        with self.assertRaises(FrozenException) as context2:
            frozen_zet ^= frozen_zet2

        self.assertEqual("'frozenzet' object is immutable",
                         str(context1.exception))
        self.assertEqual("'frozenzet' object is immutable",
                         str(context2.exception))