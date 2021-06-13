import io
import json
import pickle
import sys
import tempfile
import unittest
from typing import Dict
from frozendict import frozendict
from gelidum import FrozenException
from gelidum import freeze
from gelidum.frozen import FrozenBase, clear_frozen_classes


class TestFreeze(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

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

    def test_freeze_simple_dataclass(self):
        from dataclasses import dataclass

        @dataclass
        class Dummy:
            attr1: str
            attr2: str
            attr3: str = "0"

        dummy = Dummy(attr1="1", attr2="2", attr3="3")
        frozen_dummy_not_inplace = freeze(dummy, inplace=False)
        frozen_dummy_inplace = freeze(dummy, inplace=True)

        with self.assertRaises(FrozenException) as context_not_inplace:
            frozen_dummy_not_inplace.attr1 = "2"

        with self.assertRaises(FrozenException) as context_inplace:
            frozen_dummy_inplace.attr2 = "2"

        self.assertEqual("Can't assign 'attr1' on immutable instance",
                         str(context_not_inplace.exception))
        self.assertEqual("Can't assign 'attr2' on immutable instance",
                         str(context_inplace.exception))
        self.assertEqual(id(dummy), id(frozen_dummy_inplace))
        self.assertNotEqual(id(dummy), id(frozen_dummy_not_inplace))

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
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_assign_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_assign_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_assign_attr3.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_inc_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_inc_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_inc_attr3.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_dec_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_dec_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
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
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_assign_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_assign_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_assign_attr3.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_inc_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_inc_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_inc_attr3.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_dec_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_dec_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
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
            "Can't assign 'dummy1' on immutable instance",
            str(context_exc_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_dummy1_attr3.exception)
        )
        self.assertEqual(
            "Can't assign 'dummy1' on immutable instance",
            str(context_exc_setattr_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_setattr_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_setattr_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
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
            "Can't assign 'dummy1' on immutable instance",
            str(context_exc_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_dummy1_attr3.exception)
        )
        self.assertEqual(
            "Can't assign 'dummy1' on immutable instance",
            str(context_exc_setattr_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context_exc_setattr_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance",
            str(context_exc_setattr_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance",
            str(context_exc_setattr_dummy1_attr3.exception)
        )

    def test_freeze_object_with_file_handler_attribute(self):
        with tempfile.TemporaryFile("w") as temp_text_file:
            with tempfile.TemporaryFile("wb") as temp_bin_file:
                class DummyWithTextFile(object):
                    def __init__(self):
                        self.text_file = temp_text_file

                class DummyWithBinaryFile(object):
                    def __init__(self):
                        self.binary_file = temp_bin_file

                dummy_with_text_file = DummyWithTextFile()
                dummy_with_binary_file = DummyWithBinaryFile()

                with self.assertRaises(io.UnsupportedOperation) as text_write_context:
                    freeze(dummy_with_text_file, inplace=True)

                with self.assertRaises(io.UnsupportedOperation) as binary_write_context:
                    freeze(dummy_with_binary_file, inplace=True)

        self.assertEqual("Text file handlers can't be frozen",
                         str(text_write_context.exception))
        self.assertEqual("Binary file handlers can't be frozen",
                         str(binary_write_context.exception))

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

    def test_hash_frozen_object_as_key_in_dict(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, inplace=False)
        frozen_dummy_inplace = freeze(dummy, inplace=True)
        my_dict: Dict = {dummy: "this is a dummy object"}

        self.assertNotEqual(hash(dummy), hash(frozen_dummy))
        self.assertEqual(None, my_dict.get(frozen_dummy))
        self.assertEqual(hash(dummy), hash(frozen_dummy_inplace))
        self.assertEqual("this is a dummy object", my_dict.get(frozen_dummy_inplace))

    def test_modifying_class_attribute_on_frozen_objects(self):
        class Dummy(object):
            COUNTER = 1

        dummy = Dummy()
        frozen_dummy = freeze(dummy, inplace=False)
        frozen_dummy_inplace = freeze(dummy, inplace=True)
        Dummy.COUNTER += 1

        self.assertEqual(2, Dummy.COUNTER)
        self.assertEqual(2, frozen_dummy.COUNTER)
        self.assertEqual(2, frozen_dummy_inplace.COUNTER)

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
            "Can't assign 'new_attribute' on immutable instance", str(context.exception))

    def test_cannot_use_modifying_attribute_method_in_frozen_object(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

            def inc_attr1(self):
                self.attr1 += 1

            def inc_attr2(self):
                self._attr2 += 1

            def inc_attr3(self):
                self.__attr3 += 1

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy)
        with self.assertRaises(FrozenException) as context1:
            frozen_dummy.inc_attr1()
        with self.assertRaises(FrozenException) as context2:
            frozen_dummy.inc_attr2()
        with self.assertRaises(FrozenException) as context3:
            frozen_dummy.inc_attr3()

        self.assertEqual(
            "Can't assign 'attr1' on immutable instance", str(context1.exception))
        self.assertEqual(
            "Can't assign '_attr2' on immutable instance", str(context2.exception))
        self.assertEqual(
            "Can't assign '_Dummy__attr3' on immutable instance", str(context3.exception))

    def test_json(self):
        data_list = [{"a": 1, "b": 2}, {"a": 11, "b": 22}]
        data_dict = {"first": [{"a": 1}, {"a": 1}]}

        self.assertEqual('[{"a": 1, "b": 2}, {"a": 11, "b": 22}]', json.dumps(freeze(data_list)))
        self.assertEqual('{"first": [{"a": 1}, {"a": 1}]}', json.dumps(freeze(data_dict)))

    def test_pickle(self):
        class DummyForPickle(object):
            def __init__(self, attr: int):
                self.attr = attr

        setattr(sys.modules[__name__], DummyForPickle.__name__, DummyForPickle)

        dummy = DummyForPickle(attr=1)
        frozen_dummy = freeze(dummy)
        pickled_frozen_dummy = pickle.dumps(frozen_dummy)
        unpickled_frozen_dummy = pickle.loads(pickled_frozen_dummy)

        with self.assertRaises(FrozenException) as context:
            unpickled_frozen_dummy.attr = 8

        self.assertEqual(
            "Can't assign 'attr' on immutable instance",
            str(context.exception)
        )
        self.assertEqual(1, frozen_dummy.attr, unpickled_frozen_dummy.attr)

    def test_pickle_object_of_same_name_classes(self):
        import tests.gelidum_tests.utils.dummy1
        import tests.gelidum_tests.utils.dummy2

        dummy1 = tests.gelidum_tests.utils.dummy1.Dummy(attr1=1)
        dummy2 = tests.gelidum_tests.utils.dummy2.Dummy(attr2=2)

        frozen_dummy1 = freeze(dummy1)
        frozen_dummy2 = freeze(dummy2)
        pickled_frozen_dummy1 = pickle.dumps(frozen_dummy1)
        pickled_frozen_dummy2 = pickle.dumps(frozen_dummy2)
        unpickled_frozen_dummy1 = pickle.loads(pickled_frozen_dummy1)
        unpickled_frozen_dummy2 = pickle.loads(pickled_frozen_dummy2)

        with self.assertRaises(FrozenException) as context1:
            unpickled_frozen_dummy1.attr1 = 99

        with self.assertRaises(FrozenException) as context2:
            unpickled_frozen_dummy2.attr2 = 99

        with self.assertRaises(FrozenException) as context1_get_gelidum_hot_class_module:
            unpickled_frozen_dummy2.get_gelidum_hot_class_module = 99

        with self.assertRaises(FrozenException) as context2_get_gelidum_hot_class_module:
            unpickled_frozen_dummy2.get_gelidum_hot_class_module = 99

        self.assertEqual(
            "Can't assign 'attr1' on immutable instance",
            str(context1.exception)
        )
        self.assertEqual(
            "Can't assign 'attr2' on immutable instance",
            str(context2.exception)
        )
        self.assertEqual(
            "Can't assign 'get_gelidum_hot_class_module' on immutable instance",
            str(context1_get_gelidum_hot_class_module.exception)
        )
        self.assertEqual(
            "Can't assign 'get_gelidum_hot_class_module' on immutable instance",
            str(context2_get_gelidum_hot_class_module.exception)
        )
        self.assertEqual(1, frozen_dummy1.attr1, unpickled_frozen_dummy1.attr1)
        self.assertEqual(2, frozen_dummy2.attr2, unpickled_frozen_dummy2.attr2)

        self.assertEqual("tests.gelidum_tests.utils.dummy1",
                         frozen_dummy1.get_gelidum_hot_class_module())
        self.assertEqual("tests.gelidum_tests.utils.dummy2",
                         frozen_dummy2.get_gelidum_hot_class_module())
        self.assertEqual("Dummy", frozen_dummy1.get_gelidum_hot_class_name())
        self.assertEqual("Dummy", frozen_dummy2.get_gelidum_hot_class_name())

    def test_hot_class_module_class(self):
        from tests.gelidum_tests.utils.dummy1 import Dummy

        dummy1 = Dummy(1)
        dummy2 = Dummy(2)
        dummy3 = Dummy(3)
        frozen_dummy1 = freeze(dummy1, inplace=False)
        frozen_dummy2 = freeze(dummy2, inplace=False)
        frozen_dummy3 = freeze(dummy3, inplace=False)

        self.assertEqual(Dummy.__name__, frozen_dummy1.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy2.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy3.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__module__, frozen_dummy1.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy2.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy3.get_gelidum_hot_class_module())

    def test_hot_class_module_internal_class(self):
        class Dummy(object):
            pass

        dummy1 = Dummy()
        dummy2 = Dummy()
        dummy3 = Dummy()
        frozen_dummy1 = freeze(dummy1, inplace=False)
        frozen_dummy2 = freeze(dummy2, inplace=False)
        frozen_dummy3 = freeze(dummy3, inplace=False)

        self.assertEqual(Dummy.__name__, frozen_dummy1.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy2.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy3.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__module__, frozen_dummy1.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy2.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy3.get_gelidum_hot_class_module())

    def test_count_frozen_classes(self):
        import gelidum.frozen

        frozen_classes = getattr(gelidum.frozen, "__FROZEN_CLASSES")

        class Dummy(object):
            def __init__(self, attr: int):
                self.attr = attr

        dummy1 = Dummy(1)
        dummy2 = Dummy(2)
        dummy3 = Dummy(3)
        frozen_dummy1 = freeze(dummy1, inplace=False)
        frozen_dummy2 = freeze(dummy2, inplace=False)
        frozen_dummy3 = freeze(dummy3, inplace=False)

        self.assertSetEqual({frozen_dummy1.__class__}, set(frozen_classes.values()))
        self.assertEqual(frozen_dummy1.__class__, frozen_dummy2.__class__, frozen_dummy3.__class__)
