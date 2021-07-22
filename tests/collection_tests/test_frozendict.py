import unittest
from collections import ValuesView, KeysView
from typing import Any

from gelidum import FrozenException, freeze
from gelidum.collections.frozendict import frozendict
from gelidum.frozen import FrozenBase


class TestFrozendict(unittest.TestCase):  # noqa
    def test_empty_construction(self):
        frozen_list = frozendict()

        self.assertEqual(0, len(frozen_list))

    def test_construction(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3)})

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(3, len(frozen_dict))
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_add(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(3))
        frozen_dict1 = frozendict({"one": 1, "two": "2", "three": frozen_dummy})
        frozen_dict2 = frozendict({"one": 1, "two": "2.5"})
        joined_frozen_dict = frozendict({"one": 1, "two": "2.5", "three": frozen_dummy})

        self.assertDictEqual(joined_frozen_dict, frozen_dict1 + frozen_dict2)

    def test_or(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(3))
        frozen_dict1 = frozendict({"one": 1, "two": "2", "three": frozen_dummy})
        frozen_dict2 = frozendict({"one": 1, "two": "2.5"})
        joined_frozen_dict = frozendict({"one": 1, "two": "2.5", "three": frozen_dummy})

        self.assertDictEqual(joined_frozen_dict, frozen_dict1 | frozen_dict2)

    def test_sub(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dummy = freeze(Dummy(3))
        frozen_dict1 = frozendict({"one": 1, "two": "2", "three": frozen_dummy})
        frozen_dict2 = frozendict({"one": 1, "two": "2.5"})
        joined_frozen_dict = frozendict({"three": frozen_dummy})

        self.assertDictEqual(joined_frozen_dict, frozen_dict1 - frozen_dict2)

    def test_getitem(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3)})

        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual(1, frozen_dict.get("one"))
        self.assertEqual(None, frozen_dict.get("four"))
        self.assertEqual(4, frozen_dict.get("four", 4))

    def test_hash(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict(
            {"one": 1, "two": "2", "three": Dummy(3), "four": {"a": "1"}}
        )

        self.assertTrue(isinstance(hash(frozen_dict), int))

    def test_setitem(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3)})

        with self.assertRaises(FrozenException) as context_setitem:
            frozen_dict["four"] = 4

        self.assertEqual(
            "'frozendict' object is immutable",
            str(context_setitem.exception)
        )

    def test_del(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3)})
        with self.assertRaises(FrozenException) as context_del:
            del frozen_dict["one"]
        self.assertEqual(
            "'frozendict' object is immutable",
            str(context_del.exception)
        )

    def test_keys(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        dummy = Dummy(3)
        frozen_dict = frozendict({"one": 1, "two": "2", "three": dummy})
        frozen_dict_keys = frozen_dict.keys()
        frozen_dict_keys_iter = iter(frozen_dict_keys)
        frozen_dict_keys_list = list(frozen_dict_keys)

        self.assertTrue(isinstance(frozen_dict_keys, KeysView))
        self.assertEqual("one", next(frozen_dict_keys_iter))
        self.assertEqual("two", next(frozen_dict_keys_iter))
        self.assertEqual("three", next(frozen_dict_keys_iter))
        self.assertEqual(3, len(frozen_dict_keys_list))
        self.assertTrue("one" in frozen_dict_keys_list)
        self.assertTrue("two" in frozen_dict_keys_list)
        self.assertTrue("three" in frozen_dict_keys_list)

    def test_values(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        dummy = Dummy(3)
        frozen_dict = frozendict({"one": 1, "two": "2", "three": dummy})
        frozen_dict_values = frozen_dict.values()
        frozen_dict_values_iter = iter(frozen_dict.values())
        frozen_dict_values_list = list(frozen_dict_values)

        self.assertTrue(isinstance(frozen_dict_values, ValuesView))
        self.assertEqual(1, next(frozen_dict_values_iter))
        self.assertEqual("2", next(frozen_dict_values_iter))
        self.assertEqual(frozen_dict["three"], next(frozen_dict_values_iter))
        self.assertEqual(3, len(frozen_dict_values_list))
        self.assertTrue(1 in frozen_dict_values_list)
        self.assertTrue("2" in frozen_dict_values_list)
        self.assertFalse(dummy in frozen_dict_values_list)
        self.assertTrue(frozen_dict["three"] in frozen_dict_values_list)