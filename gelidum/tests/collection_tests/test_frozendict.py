import unittest
from collections.abc import ValuesView, KeysView
from typing import Any, Tuple

from gelidum import FrozenException, freeze
from gelidum.collections.frozendict import frozendict
from gelidum.frozen import FrozenBase


class TestFrozendict(unittest.TestCase):  # noqa
    def test_empty_construction(self):
        frozen_list = frozendict()

        self.assertEqual(0, len(frozen_list))

    def test_construction_from_dict(self):
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

    def test_construction_from_empty_dict(self):
        frozen_dict = frozendict({})

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(0, len(frozen_dict))

    def test_construction_from_generator(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        def test_generator() -> Tuple[str, int]:
            yield "one", 1
            yield "two", "2"
            yield "three", Dummy(3)

        frozen_dict = frozendict(test_generator())

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(3, len(frozen_dict))
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_construction_from_kwargs(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict(one=1, two="2", three=Dummy(3))

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(3, len(frozen_dict))
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_construction_from_dict_and_kwargs(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"k0": "v0", "k1": "v1"}, one=1, two="2", three=Dummy(3))

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(5, len(frozen_dict))
        self.assertEqual("v0", frozen_dict["k0"])
        self.assertEqual("v1", frozen_dict["k1"])
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_construction_empty_dict_and_kwargs(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({}, one=1, two="2", three=Dummy(3))

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(3, len(frozen_dict))
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_construction_from_list_of_pairs_and_kwargs(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict([("k0", "v0"), ("k1", "v1")], one=1, two="2", three=Dummy(3))

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(5, len(frozen_dict))
        self.assertEqual("v0", frozen_dict["k0"])
        self.assertEqual("v1", frozen_dict["k1"])
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_construction_list_of_strings_and_kwargs(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict(["k0", "v0", "k1", "v1"], one=1, two="2", three=Dummy(3))

        self.assertTrue(isinstance(frozen_dict, FrozenBase))
        self.assertEqual(5, len(frozen_dict))
        self.assertEqual("1", frozen_dict["k"])
        self.assertEqual("1", frozen_dict["v"])
        self.assertEqual(1, frozen_dict["one"])
        self.assertEqual("2", frozen_dict["two"])
        self.assertTrue(isinstance(frozen_dict["three"], FrozenBase))
        self.assertEqual(3, frozen_dict["three"].value)

    def test_construction_empty_list_and_kwargs(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict([], one=1, two="2", three=Dummy(3))

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

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3), "four": {"a": "1"}})

        self.assertTrue(isinstance(hash(frozen_dict), int))

    def test_setitem(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3)})

        with self.assertRaises(FrozenException) as context_setitem:
            frozen_dict["four"] = 4

        self.assertEqual("'frozendict' object is immutable", str(context_setitem.exception))

    def test_del(self):
        class Dummy:
            def __init__(self, value: Any):
                self.value = value

        frozen_dict = frozendict({"one": 1, "two": "2", "three": Dummy(3)})
        with self.assertRaises(FrozenException) as context_del:
            del frozen_dict["one"]
        self.assertEqual("'frozendict' object is immutable", str(context_del.exception))

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
