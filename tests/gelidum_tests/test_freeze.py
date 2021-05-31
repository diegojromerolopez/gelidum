import unittest
from frozendict import frozendict
from gelidum import freeze
from gelidum import FrozenException
from gelidum.frozen import FrozenBase


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
        self.assertEqual(
            b"Byte array", freeze(bytearray(b"Byte array")))

    def test_freeze_dict(self):
        self.assertEqual(
            frozendict({"one": 1, "two": 2}), freeze({"one": 1, "two": 2}))

    def test_freeze_list(self):
        self.assertEqual(
            ("one", 2, "three"), freeze(["one", 2, "three"]))

    def test_freeze_tuple(self):
        self.assertEqual(
            ("one", 2, "three"), freeze(("one", 2, "three")))

    def test_freeze_set(self):
        self.assertEqual(
            frozenset(["one", 2, "three"]), freeze({"one", 2, "three"}))

    def test_freeze_simple_object_inplace(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, inplace=True)

        with self.assertRaises(FrozenException) as context_exc_assign_attr1:
            frozen_dummy.attr1 = 99
        with self.assertRaises(FrozenException) as context_exc_assign_attr2:
            frozen_dummy._attr2 = 99
        with self.assertRaises(FrozenException) as context_exc_assign_attr3:
            frozen_dummy._Dummy__attr3 = 99
        with self.assertRaises(FrozenException) as context_exc_inc_attr1:
            frozen_dummy.attr1 += 99
        with self.assertRaises(FrozenException) as context_exc_inc_attr2:
            frozen_dummy._attr2 += 99
        with self.assertRaises(FrozenException) as context_exc_inc_attr3:
            frozen_dummy._Dummy__attr3 += 99
        with self.assertRaises(FrozenException) as context_exc_dec_attr1:
            frozen_dummy.attr1 -= 99
        with self.assertRaises(FrozenException) as context_exc_dec_attr2:
            frozen_dummy._attr2 -= 99
        with self.assertRaises(FrozenException) as context_exc_dec_attr3:
            frozen_dummy._Dummy__attr3 -= 99

        self.assertEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((Dummy, FrozenBase), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_assign_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_assign_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_assign_attr3.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_inc_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_inc_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_inc_attr3.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_dec_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_dec_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_dec_attr3.exception)
        )

    def test_freeze_simple_object_not_inplace(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, inplace=False)

        with self.assertRaises(FrozenException) as context_exc_assign_attr1:
            frozen_dummy.attr1 = 99
        with self.assertRaises(FrozenException) as context_exc_assign_attr2:
            frozen_dummy._attr2 = 99
        with self.assertRaises(FrozenException) as context_exc_assign_attr3:
            frozen_dummy._Dummy__attr3 = 99
        with self.assertRaises(FrozenException) as context_exc_inc_attr1:
            frozen_dummy.attr1 += 99
        with self.assertRaises(FrozenException) as context_exc_inc_attr2:
            frozen_dummy._attr2 += 99
        with self.assertRaises(FrozenException) as context_exc_inc_attr3:
            frozen_dummy._Dummy__attr3 += 99
        with self.assertRaises(FrozenException) as context_exc_dec_attr1:
            frozen_dummy.attr1 -= 99
        with self.assertRaises(FrozenException) as context_exc_dec_attr2:
            frozen_dummy._attr2 -= 99
        with self.assertRaises(FrozenException) as context_exc_dec_attr3:
            frozen_dummy._Dummy__attr3 -= 99

        self.assertNotEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((Dummy, FrozenBase), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_assign_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_assign_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_assign_attr3.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_inc_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_inc_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_inc_attr3.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_dec_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_dec_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_dec_attr3.exception)
        )

    def test_freeze_deep_object_inplace(self):
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

        frozen_deep_dummy = freeze(deep_dummy, inplace=True)

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
        with self.assertRaises(FrozenException) as \
                context_exc_setattr_dummy1_attr1:
            setattr(frozen_deep_dummy.dummy1, "attr1", 99)
        with self.assertRaises(FrozenException) as \
                context_exc_setattr_dummy1_attr2:
            setattr(frozen_deep_dummy.dummy1, "_attr2", 99)
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1_attr3:
            setattr(frozen_deep_dummy.dummy1, "_Dummy__attr3", 99)

        self.assertEqual(id(deep_dummy), id(frozen_deep_dummy))
        self.assertEqual(11, frozen_deep_dummy.dummy1.attr1)
        self.assertEqual(12, frozen_deep_dummy.dummy1._attr2)
        self.assertEqual(13, frozen_deep_dummy.dummy1._Dummy__attr3)
        self.assertEqual(
            "Can't assign \"dummy1\" on immutable instance",
            str(context_exc_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_dummy1_attr3.exception)
        )
        self.assertEqual(
            "Can't assign \"dummy1\" on immutable instance",
            str(context_exc_setattr_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_setattr_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_setattr_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_setattr_dummy1_attr3.exception)
        )

    def test_freeze_deep_object_not_inplace(self):
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

        frozen_deep_dummy = freeze(deep_dummy, inplace=False)

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
        with self.assertRaises(FrozenException) as \
                context_exc_setattr_dummy1_attr1:
            setattr(frozen_deep_dummy.dummy1, "attr1", 99)
        with self.assertRaises(FrozenException) as \
                context_exc_setattr_dummy1_attr2:
            setattr(frozen_deep_dummy.dummy1, "_attr2", 99)
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1_attr3:
            setattr(frozen_deep_dummy.dummy1, "_Dummy__attr3", 99)

        self.assertNotEqual(id(deep_dummy), id(frozen_deep_dummy))
        self.assertEqual(11, frozen_deep_dummy.dummy1.attr1)
        self.assertEqual(12, frozen_deep_dummy.dummy1._attr2)
        self.assertEqual(13, frozen_deep_dummy.dummy1._Dummy__attr3)
        self.assertEqual(
            "Can't assign \"dummy1\" on immutable instance",
            str(context_exc_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_dummy1_attr3.exception)
        )
        self.assertEqual(
            "Can't assign \"dummy1\" on immutable instance",
            str(context_exc_setattr_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign \"attr1\" on immutable instance",
            str(context_exc_setattr_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign \"_attr2\" on immutable instance",
            str(context_exc_setattr_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign \"_Dummy__attr3\" on immutable instance",
            str(context_exc_setattr_dummy1_attr3.exception)
        )

    def test_hash_inplace(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, inplace=True)
        self.assertEqual(hash(dummy), hash(frozen_dummy))

    def test_hash_not_inplace(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, inplace=False)
        self.assertNotEqual(hash(dummy), hash(frozen_dummy))

    def test_modifying_method(self):
        pass

    def test_modifying_class_attribute(self):
        pass

    def test_modifying_class_method(self):
        pass

    def test_cannot_add_attribute_to_frozen_object(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy)
        with self.assertRaises(FrozenException) as context:
            frozen_dummy.new_attribute = 99
        self.assertEqual(
            "Can't assign \"new_attribute\" on immutable instance", str(context.exception))
