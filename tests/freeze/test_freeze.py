import unittest
from frozendict import frozendict
from freeze.freeze import freeze
from freeze.frozen import FrozenException


class TestFreeze(unittest.TestCase):
    def test_freeze_builtins(self):
        self.assertEqual(3, freeze(3))
        self.assertEqual(3.9, freeze(3.9))
        self.assertEqual(True, freeze(True))
        self.assertEqual(False, freeze(False))
        self.assertEqual(None, freeze(None))
        self.assertEqual(complex(1, 2), freeze(complex(1, 2)))
        self.assertEqual(b"Bytes", freeze(b"Bytes"))
        self.assertEqual("String", freeze("String"))

    def test_freeze_bytearray(self):
        self.assertEqual(b"Byte array", freeze(bytearray(b"Byte array")))

    def test_freeze_dict(self):
        self.assertEqual(frozendict({"one": 1, "two": 2}), freeze({"one": 1, "two": 2}))

    def test_freeze_list(self):
        self.assertEqual(("one", 2, "three"), freeze(["one", 2, "three"]))

    def test_freeze_tuple(self):
        self.assertEqual(("one", 2, "three"), freeze(("one", 2, "three")))

    def test_freeze_set(self):
        self.assertEqual(frozenset(["one", 2, "three"]), freeze({"one", 2, "three"}))

    def test_freeze_simple_object(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy)

        with self.assertRaises(FrozenException) as context_exc_attr1:
            frozen_dummy.attr1 = 99
        with self.assertRaises(FrozenException) as context_exc_attr2:
            frozen_dummy._attr2 = 99
        with self.assertRaises(FrozenException) as context_exc_attr3:
            frozen_dummy._Dummy__attr3 = 99

        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertEqual("Can't assign \"attr1\" on immutable instance", str(context_exc_attr1.exception))
        self.assertEqual("Can't assign \"_attr2\" on immutable instance", str(context_exc_attr2.exception))
        self.assertEqual("Can't assign \"_Dummy__attr3\" on immutable instance", str(context_exc_attr3.exception))

    def test_freeze_deep_object(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        class DeepDummy(object):
            def __init__(self, dummy1: Dummy, dummy2: Dummy, dummy3: Dummy):
                self.dummy1 = dummy1
                self._dummy2 = dummy2
                self.__dummy3 = dummy3

        deep_dummy = DeepDummy(
            dummy1=Dummy(attr1=11, attr2=12, attr3=13),
            dummy2=Dummy(attr1=21, attr2=22, attr3=23),
            dummy3=Dummy(attr1=31, attr2=32, attr3=33)
        )

        frozen_deep_dummy = freeze(deep_dummy)

        with self.assertRaises(FrozenException) as context_exc_dummy1:
            frozen_deep_dummy.dummy1 = 99
        with self.assertRaises(FrozenException) as context_exc_dummy1_attr1:
            frozen_deep_dummy.dummy1.attr1 = 99
        with self.assertRaises(FrozenException) as context_exc_dummy1_attr2:
            frozen_deep_dummy.dummy1._attr2 = 99
        with self.assertRaises(FrozenException) as context_exc_dummy1_attr3:
            frozen_deep_dummy.dummy1._Dummy__attr3 = 99
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1:
            setattr(frozen_deep_dummy, "dummy1", 99)
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1_attr1:
            setattr(frozen_deep_dummy.dummy1, "attr1", 99)
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1_attr2:
            setattr(frozen_deep_dummy.dummy1, "_attr2", 99)
        with self.assertRaises(FrozenException) as context_exc_dummy1_attr3:
            setattr(frozen_deep_dummy.dummy1, "_Dummy__attr3", 99)

        self.assertEqual(11, frozen_deep_dummy.dummy1.attr1)
        self.assertEqual(12, frozen_deep_dummy.dummy1._attr2)
        self.assertEqual(13, frozen_deep_dummy.dummy1._Dummy__attr3)
        self.assertEqual("Can't assign \"dummy1\" on immutable instance", str(context_exc_dummy1.exception))
        self.assertEqual("Can't assign \"attr1\" on immutable instance", str(context_exc_dummy1_attr1.exception))
        self.assertEqual("Can't assign \"_attr2\" on immutable instance", str(context_exc_dummy1_attr2.exception))
        self.assertEqual("Can't assign \"_Dummy__attr3\" on immutable instance",
                         str(context_exc_dummy1_attr3.exception))

        self.assertEqual("Can't assign \"dummy1\" on immutable instance", str(context_exc_setattr_dummy1.exception))
        self.assertEqual("Can't assign \"attr1\" on immutable instance",
                         str(context_exc_setattr_dummy1_attr1.exception))
        self.assertEqual("Can't assign \"_attr2\" on immutable instance",
                         str(context_exc_setattr_dummy1_attr2.exception))
        self.assertEqual("Can't assign \"_Dummy__attr3\" on immutable instance",
                         str(context_exc_dummy1_attr3.exception))
