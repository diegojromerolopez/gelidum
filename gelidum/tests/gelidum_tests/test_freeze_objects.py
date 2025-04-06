import copy
import datetime
import io
import json
import logging
import pickle
import sys
import tempfile
import threading
import unittest
import warnings
from typing import Any, Dict, List, Union
from unittest.mock import patch

from gelidum import FrozenException, freeze
from gelidum.frozen import FrozenBase, clear_frozen_classes, get_frozen_classes
from gelidum.tests.gelidum_tests.utils.datetime import utcnow


class TestFreezeObjects(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_freeze_objects_with__call__method(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

            def __call__(self, x: int, y: int):
                return self.attr + x * y

        dummy = Dummy(1)
        frozen_dummy = freeze(dummy, on_freeze="copy", save_original_on_copy=False)

        self.assertEqual(7, frozen_dummy(2, 3))

    def test_freeze_objects_by_copying_and_accessing_the_original_object(self):
        class DummyChild(object):
            def __init__(self, value: int):
                self.attr = value

        class Dummy(object):
            def __init__(self, child: DummyChild):
                self.child = child

        dummy_child = DummyChild(value=1)
        dummy = Dummy(child=dummy_child)
        frozen_dummy = freeze(dummy, on_freeze="copy", save_original_on_copy=True)

        self.assertNotEqual(frozen_dummy.__class__, dummy.__class__)
        self.assertEqual(frozen_dummy.original_obj.__class__, dummy.__class__)
        self.assertEqual(id(frozen_dummy.original_obj), id(dummy))
        self.assertEqual(frozen_dummy.child.original_obj, None)

    def test_freeze_objects_by_copying_but_not_saving_original_object(self):
        class DummyChild(object):
            def __init__(self, value: int):
                self.attr = value

        class Dummy(object):
            def __init__(self, child: DummyChild):
                self.child = child

        dummy_child = DummyChild(value=1)
        dummy = Dummy(child=dummy_child)
        frozen_dummy = freeze(dummy, on_freeze="copy", save_original_on_copy=False)

        self.assertNotEqual(frozen_dummy.__class__, dummy.__class__)
        self.assertIsNone(frozen_dummy.original_obj)

    def test_freeze_objects_inplace_and_no_access_to_original_object(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

        dummy = Dummy(value=1)
        frozen_dummy = freeze(dummy, on_freeze="inplace")

        self.assertEqual(frozen_dummy.__class__, dummy.__class__)
        self.assertIsNone(frozen_dummy.original_obj)

    def test_freeze_objects_of_same_class(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

        dummy1 = Dummy(value=1)
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        dummy2 = Dummy(value=2)
        frozen_dummy2 = freeze(dummy2, on_freeze="copy")

        self.assertEqual(frozen_dummy1.__class__, frozen_dummy2.__class__)

    def test_freeze_simple_object_inplace_true_deprecated_parameter(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_dummy = freeze(dummy, on_update="exception", inplace=True)

        self.assertEqual(id(dummy), id(frozen_dummy))
        self.assertEqual(1, len(caught_warnings))
        self.assertEqual(
            "Use of inplace is deprecated and will be removed in next major version (0.6.0)",
            str(caught_warnings[0].message),
        )

    def test_freeze_simple_object_inplace_false_deprecated_parameter(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_dummy = freeze(dummy, on_update="exception", inplace=False)

        self.assertNotEqual(id(dummy), id(frozen_dummy))
        self.assertEqual(1, len(caught_warnings))
        self.assertEqual(
            "Use of inplace is deprecated and will be removed in next major version (0.6.0)",
            str(caught_warnings[0].message),
        )

    def test_freeze_simple_object_on_update_warning_on_freeze_inplace(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_update="warning", on_freeze="inplace")

        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_dummy.attr1 = 99
            frozen_dummy._attr2 = 99
            frozen_dummy._Dummy__attr3 = 99

        self.assertEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertListEqual(
            [
                "Can't assign attribute 'attr1' on immutable instance",
                "Can't assign attribute '_attr2' on immutable instance",
                "Can't assign attribute '_Dummy__attr3' on immutable instance",
            ],
            [str(warn.message) for warn in caught_warnings],
        )

    def test_freeze_object_of_class_with_slots(self):
        class ClassWithSlots(object):
            __slots__ = ("attr1", "_attr2")

            def __init__(self, attr1: int, attr2: int):
                self.attr1 = attr1
                self._attr2 = attr2

        obj = ClassWithSlots(attr1=1, attr2=2)
        frozen_obj = freeze(obj, on_update="warning", on_freeze="copy")

        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_obj.attr1 = 99
            frozen_obj._attr2 = 99
            frozen_obj.new_attribute = 99

        self.assertNotEqual(id(obj), id(frozen_obj))
        self.assertEqual((FrozenBase, ClassWithSlots), frozen_obj.__class__.__bases__)
        self.assertEqual(1, frozen_obj.attr1)
        self.assertEqual(2, frozen_obj._attr2)
        self.assertListEqual(
            [
                "Can't assign attribute 'attr1' on immutable instance",
                "Can't assign attribute '_attr2' on immutable instance",
                "Can't assign attribute 'new_attribute' on immutable instance",
            ],
            [str(warn.message) for warn in caught_warnings],
        )

    def test_freeze_two_object_of_the_same_class_with_slots(self):
        class ClassWithSlots(object):
            __slots__ = ("attr1", "_attr2")

            def __init__(self, attr1: int, attr2: int):
                self.attr1 = attr1
                self._attr2 = attr2

        obj1 = ClassWithSlots(attr1=1, attr2=2)
        frozen_obj1 = freeze(obj1, on_update="warning", on_freeze="copy")

        obj2 = ClassWithSlots(attr1=3, attr2=4)
        frozen_obj2 = freeze(obj2, on_update="warning", on_freeze="copy")

        self.assertNotEqual(id(frozen_obj1.__class__), id(frozen_obj2.__class__))
        self.assertEqual((FrozenBase, ClassWithSlots), frozen_obj1.__class__.__bases__)
        self.assertEqual((FrozenBase, ClassWithSlots), frozen_obj2.__class__.__bases__)
        self.assertEqual(1, frozen_obj1.attr1)
        self.assertEqual(2, frozen_obj1._attr2)
        self.assertEqual(3, frozen_obj2.attr1)
        self.assertEqual(4, frozen_obj2._attr2)

    def test_freeze_object_with_class_with_slots_whose_attributes_are_objects_with_class_with_slots(self):
        class Attr(object):
            __slots__ = ("value",)

            def __init__(self, value: int):
                self.value = value

        class ClassWithSlots(object):
            __slots__ = ("attr1", "attr2")

            def __init__(self, attr1: Attr, attr2: Attr):
                self.attr1 = attr1
                self.attr2 = attr2

        obj = ClassWithSlots(attr1=Attr(1), attr2=Attr(2))
        frozen_obj = freeze(obj, on_update="warning", on_freeze="copy")

        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_obj.attr1 = 99
            frozen_obj.attr2 = 99

        self.assertNotEqual(id(obj), id(frozen_obj))
        self.assertEqual((FrozenBase, ClassWithSlots), frozen_obj.__class__.__bases__)
        self.assertEqual(1, frozen_obj.attr1.value)
        self.assertEqual(2, frozen_obj.attr2.value)
        self.assertListEqual(
            [
                "Can't assign attribute 'attr1' on immutable instance",
                "Can't assign attribute 'attr2' on immutable instance",
            ],
            [str(warn.message) for warn in caught_warnings],
        )

    def test_freeze_object_of_class_with_slots_inplace(self):
        class ClassWithSlots(object):
            __slots__ = ("attr1", "_attr2")

            def __init__(self, attr1: int, attr2: int):
                self.attr1 = attr1
                self._attr2 = attr2

        obj = ClassWithSlots(attr1=1, attr2=2)
        with self.assertRaises(FrozenException) as freeze_context:
            freeze(obj, on_update="warning", on_freeze="inplace")

        self.assertEqual("Objects of classes with __slots__ cannot be frozen inplace", str(freeze_context.exception))

    def test_freeze_object_of_class_with_slots_inplace_deprecated_parameter(self):
        class ClassWithSlots(object):
            __slots__ = ("attr1", "_attr2")

            def __init__(self, attr1: int, attr2: int):
                self.attr1 = attr1
                self._attr2 = attr2

        obj = ClassWithSlots(attr1=1, attr2=2)
        with self.assertRaises(FrozenException) as freeze_context:
            freeze(obj, on_update="warning", inplace=True)

        self.assertEqual("Objects of classes with __slots__ cannot be frozen inplace", str(freeze_context.exception))

    def test_freeze_simple_object_on_update_nothing_on_freeze_inplace(self):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_update="nothing", on_freeze="inplace")
        frozen_dummy.attr1 = 99
        frozen_dummy._attr2 = 99
        frozen_dummy._Dummy__attr3 = 99

        self.assertEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)

    def test_freeze_simple_object_and_catch_setattr_exception(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

        class DummyWithProperty(object):
            def __init__(self, value: int):
                self.__attr = value

            @property
            def attr(self):
                return self.__attr

        dummy = Dummy(value=1)
        frozen_dummy = freeze(dummy, on_update="exception", on_freeze="inplace")

        dummy_with_property = DummyWithProperty(value=1)
        frozen_dummy_with_property = freeze(dummy_with_property, on_update="exception", on_freeze="inplace")

        with self.assertRaises(FrozenException) as setattr_context:
            setattr(frozen_dummy, "attr", 99)

        with self.assertRaises(FrozenException) as setattr_context2:
            frozen_dummy_with_property.attr = "99"

        with self.assertRaises(FrozenException) as delattr_context:
            delattr(frozen_dummy, "attr")

        with self.assertRaises(FrozenException) as setitem_context:
            frozen_dummy["attr"] = 99

        with self.assertRaises(FrozenException) as delitem_context:
            del frozen_dummy["attr"]

        self.assertEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr)
        self.assertEqual(1, frozen_dummy_with_property.attr)
        self.assertEqual("Can't assign attribute 'attr' on immutable instance", str(setattr_context.exception))
        self.assertEqual("Can't assign attribute 'attr' on immutable instance", str(setattr_context2.exception))
        self.assertEqual("Can't delete attribute 'attr' on immutable instance", str(delattr_context.exception))
        self.assertEqual("Can't set key 'attr' on immutable instance", str(setitem_context.exception))
        self.assertEqual("Can't delete key 'attr' on immutable instance", str(delitem_context.exception))

    def test_freeze_object_with_set_descriptor_method_exception(self):
        class DummyCounter(object):
            def __init__(self, name: str):
                self.name = name

            def __get__(self, obj, type=None) -> object:  # noqa
                return obj.__dict__.get(self.name) or 0  # pragma: no cover

            def __set__(self, obj, value) -> None:
                obj.__dict__[self.name] = value  # pragma: no cover

        class Dummy:
            counter = freeze(DummyCounter("counter"))

            def __init__(self, value: int):
                self.attr = value

        dummy1 = Dummy(value=1)

        with self.assertRaises(FrozenException) as set_context:
            dummy1.counter = 1

        self.assertEqual("Can't assign setter on immutable instance", str(set_context.exception))

    @patch("datetime.datetime")
    def test_freeze_simple_object_on_update_function_freeze_inplace(self, mock_datetime):
        fixed_utcnow = datetime.datetime(2021, 6, 16, 14, 20, 56, 809581)
        mock_datetime.utcnow = unittest.mock.Mock(return_value=fixed_utcnow)

        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        writing_tries = []

        def on_update_func(message, *args, **kwargs):
            writing_tries.append(
                {"message": message, "args": args, "kwargs": kwargs, "time": datetime.datetime.utcnow()}
            )

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_update=on_update_func, on_freeze="inplace")
        frozen_dummy.attr1 = 99
        frozen_dummy._attr2 = 99
        frozen_dummy._Dummy__attr3 = 99

        expected_writing_tries = [
            {
                "args": (),
                "kwargs": {"key": "attr1", "value": 99, "frozen_obj": frozen_dummy},
                "message": "Can't assign attribute 'attr1' on immutable instance",
                "time": fixed_utcnow,
            },
            {
                "args": (),
                "kwargs": {"key": "_attr2", "value": 99, "frozen_obj": frozen_dummy},
                "message": "Can't assign attribute '_attr2' on immutable instance",
                "time": fixed_utcnow,
            },
            {
                "args": (),
                "kwargs": {"key": "_Dummy__attr3", "value": 99, "frozen_obj": frozen_dummy},
                "message": "Can't assign attribute '_Dummy__attr3' on immutable instance",
                "time": fixed_utcnow,
            },
        ]

        self.assertEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertListEqual(expected_writing_tries, writing_tries)

    @patch("logging.Logger")
    def test_freeze_simple_object_on_update_func_store_update_tries(self, mock_logger):
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self.attr2 = attr2
                self.attr3 = attr3

        class FrozenDummyUpdateTryRecorder(object):
            def __init__(self, log: logging.Logger) -> None:
                self.log = log
                self.lock = threading.Lock()
                self.writing_tries: List[Dict] = []
                self.original_obj = None

            def on_freeze(self, obj: object) -> object:
                frozen_object = copy.deepcopy(obj)
                self.original_obj = obj
                return frozen_object

            def on_update(self, frozen_obj: "FrozenBase", message: str, *args, **kwargs) -> None:
                self.log.warning(message)
                with self.lock:
                    self.writing_tries.append(
                        {
                            "frozen_obj": frozen_obj,
                            "args": args,
                            "kwargs": kwargs,
                            "datetime": utcnow(),
                        }
                    )

        update_try_recorder = FrozenDummyUpdateTryRecorder(log=mock_logger)

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_freeze=update_try_recorder.on_freeze, on_update=update_try_recorder.on_update)

        expected_writing_tries = [
            {
                "args": tuple(),
                "datetime": unittest.mock.ANY,
                "frozen_obj": frozen_dummy,
                "kwargs": {"key": "attr1", "value": 99},
            }
        ]

        frozen_dummy.attr1 = 99

        self.assertNotEqual(id(dummy), id(frozen_dummy))
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy.attr2)
        self.assertEqual(3, frozen_dummy.attr3)
        self.assertEqual(
            unittest.mock.call("Can't assign attribute 'attr1' on immutable instance"), mock_logger.warning.call_args
        )
        self.assertEqual(id(dummy), id(update_try_recorder.original_obj))
        self.assertEqual(expected_writing_tries, update_try_recorder.writing_tries)

    def test_freeze_simple_object_on_freeze_inplace(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_freeze="inplace")

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
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertEqual(
            "Can't assign attribute 'attr1' on immutable instance", str(context_exc_assign_attr1.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_attr2' on immutable instance", str(context_exc_assign_attr2.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_assign_attr3.exception)
        )
        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context_exc_inc_attr1.exception))
        self.assertEqual("Can't assign attribute '_attr2' on immutable instance", str(context_exc_inc_attr2.exception))
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_inc_attr3.exception)
        )
        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context_exc_dec_attr1.exception))
        self.assertEqual("Can't assign attribute '_attr2' on immutable instance", str(context_exc_dec_attr2.exception))
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_dec_attr3.exception)
        )

    def test_freeze_simple_object_on_freeze_copy(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int):
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_freeze="copy")

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
        self.assertEqual((FrozenBase, Dummy), frozen_dummy.__class__.__bases__)
        self.assertEqual(1, frozen_dummy.attr1)
        self.assertEqual(2, frozen_dummy._attr2)
        self.assertEqual(3, frozen_dummy._Dummy__attr3)
        self.assertEqual(
            "Can't assign attribute 'attr1' on immutable instance", str(context_exc_assign_attr1.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_attr2' on immutable instance", str(context_exc_assign_attr2.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_assign_attr3.exception)
        )
        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context_exc_inc_attr1.exception))
        self.assertEqual("Can't assign attribute '_attr2' on immutable instance", str(context_exc_inc_attr2.exception))
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_inc_attr3.exception)
        )
        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context_exc_dec_attr1.exception))
        self.assertEqual("Can't assign attribute '_attr2' on immutable instance", str(context_exc_dec_attr2.exception))
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_dec_attr3.exception)
        )

    def test_freeze_deep_object_on_freeze_inplace(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        class DeepDummy(object):
            def __init__(self, dummy1: Dummy, dummy2: Dummy, dummy3: Dummy) -> None:
                self.dummy1 = dummy1
                self._dummy2 = dummy2
                self.__dummy3 = dummy3

        deep_dummy = DeepDummy(
            dummy1=Dummy(attr1=11, attr2=12, attr3=13),
            dummy2=Dummy(attr1=21, attr2=22, attr3=23),
            dummy3=Dummy(attr1=31, attr2=32, attr3=33),
        )

        frozen_deep_dummy = freeze(deep_dummy, on_freeze="inplace")

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
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1_attr3:
            setattr(frozen_deep_dummy.dummy1, "_Dummy__attr3", 99)

        self.assertEqual(id(deep_dummy), id(frozen_deep_dummy))
        self.assertEqual(11, frozen_deep_dummy.dummy1.attr1)
        self.assertEqual(12, frozen_deep_dummy.dummy1._attr2)
        self.assertEqual(13, frozen_deep_dummy.dummy1._Dummy__attr3)
        self.assertEqual("Can't assign attribute 'dummy1' on immutable instance", str(context_exc_dummy1.exception))
        self.assertEqual(
            "Can't assign attribute 'attr1' on immutable instance", str(context_exc_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_attr2' on immutable instance", str(context_exc_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_dummy1_attr3.exception)
        )
        self.assertEqual(
            "Can't assign attribute 'dummy1' on immutable instance", str(context_exc_setattr_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign attribute 'attr1' on immutable instance", str(context_exc_setattr_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_attr2' on immutable instance", str(context_exc_setattr_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance",
            str(context_exc_setattr_dummy1_attr3.exception),
        )

    def test_freeze_deep_object_on_freeze_copy(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        class DeepDummy(object):
            def __init__(self, dummy1: Dummy, dummy2: Dummy, dummy3: Dummy) -> None:
                self.dummy1 = dummy1
                self._dummy2 = dummy2
                self.__dummy3 = dummy3

        deep_dummy = DeepDummy(
            dummy1=Dummy(attr1=11, attr2=12, attr3=13),
            dummy2=Dummy(attr1=21, attr2=22, attr3=23),
            dummy3=Dummy(attr1=31, attr2=32, attr3=33),
        )

        frozen_deep_dummy = freeze(deep_dummy, on_freeze="copy")

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
        with self.assertRaises(FrozenException) as context_exc_setattr_dummy1_attr3:
            setattr(frozen_deep_dummy.dummy1, "_Dummy__attr3", 99)

        self.assertNotEqual(id(deep_dummy), id(frozen_deep_dummy))
        self.assertEqual(11, frozen_deep_dummy.dummy1.attr1)
        self.assertEqual(12, frozen_deep_dummy.dummy1._attr2)
        self.assertEqual(13, frozen_deep_dummy.dummy1._Dummy__attr3)
        self.assertEqual("Can't assign attribute 'dummy1' on immutable instance", str(context_exc_dummy1.exception))
        self.assertEqual(
            "Can't assign attribute 'attr1' on immutable instance", str(context_exc_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_attr2' on immutable instance", str(context_exc_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance", str(context_exc_dummy1_attr3.exception)
        )
        self.assertEqual(
            "Can't assign attribute 'dummy1' on immutable instance", str(context_exc_setattr_dummy1.exception)
        )
        self.assertEqual(
            "Can't assign attribute 'attr1' on immutable instance", str(context_exc_setattr_dummy1_attr1.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_attr2' on immutable instance", str(context_exc_setattr_dummy1_attr2.exception)
        )
        self.assertEqual(
            "Can't assign attribute '_Dummy__attr3' on immutable instance",
            str(context_exc_setattr_dummy1_attr3.exception),
        )

    def test_freeze_object_with_file_handler_attribute(self) -> None:
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
                    freeze(dummy_with_text_file, on_freeze="inplace")

                with self.assertRaises(io.UnsupportedOperation) as binary_write_context:
                    freeze(dummy_with_binary_file, on_freeze="inplace")

        self.assertEqual("Text file handlers can't be frozen", str(text_write_context.exception))
        self.assertEqual("Binary file handlers can't be frozen", str(binary_write_context.exception))

    def test_hash_on_freeze_inplace(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_freeze="inplace")
        self.assertEqual(hash(dummy), hash(frozen_dummy))

    def test_hash_on_freeze_copy(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_freeze="copy")
        self.assertNotEqual(hash(dummy), hash(frozen_dummy))

    def test_hash_frozen_object_as_key_in_dict(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy, on_freeze="copy")
        frozen_dummy_inplace = freeze(dummy, on_freeze="inplace")
        my_dict: Dict = {dummy: "this is a dummy object"}

        self.assertNotEqual(hash(dummy), hash(frozen_dummy))
        self.assertEqual(None, my_dict.get(frozen_dummy))
        self.assertEqual(hash(dummy), hash(frozen_dummy_inplace))
        self.assertEqual("this is a dummy object", my_dict.get(frozen_dummy_inplace))

    def test_modifying_class_attribute_on_frozen_objects(self) -> None:
        class Dummy(object):
            COUNTER = 1

        dummy = Dummy()
        frozen_dummy = freeze(dummy, on_freeze="copy")
        frozen_dummy_inplace = freeze(dummy, on_freeze="inplace")
        Dummy.COUNTER += 1

        self.assertEqual(2, Dummy.COUNTER)
        self.assertEqual(2, frozen_dummy.COUNTER)
        self.assertEqual(2, frozen_dummy_inplace.COUNTER)

    def test_cannot_add_attribute_to_frozen_object(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
                self.attr1 = attr1
                self._attr2 = attr2
                self.__attr3 = attr3

        dummy = Dummy(attr1=1, attr2=2, attr3=3)
        frozen_dummy = freeze(dummy)
        with self.assertRaises(FrozenException) as context:
            frozen_dummy.new_attribute = 99
        self.assertEqual("Can't assign attribute 'new_attribute' on immutable instance", str(context.exception))

    def test_cannot_use_modifying_attribute_method_in_frozen_object(self) -> None:
        class Dummy(object):
            def __init__(self, attr1: int, attr2: int, attr3: int) -> None:
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

        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context1.exception))
        self.assertEqual("Can't assign attribute '_attr2' on immutable instance", str(context2.exception))
        self.assertEqual("Can't assign attribute '_Dummy__attr3' on immutable instance", str(context3.exception))

    def test_json(self) -> None:
        data_list = [{"a": 1, "b": 2}, {"a": 11, "b": 22}]
        data_dict = {"first": [{"a": 1}, {"a": 1}]}

        self.assertEqual('[{"a": 1, "b": 2}, {"a": 11, "b": 22}]', json.dumps(freeze(data_list)))
        self.assertEqual('{"first": [{"a": 1}, {"a": 1}]}', json.dumps(freeze(data_dict)))

    def test_pickle(self) -> None:
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

        self.assertEqual("Can't assign attribute 'attr' on immutable instance", str(context.exception))
        self.assertEqual(1, frozen_dummy.attr, unpickled_frozen_dummy.attr)

    def test_pickle_object_of_same_name_classes(self) -> None:
        import gelidum.tests.gelidum_tests.utils.dummy1
        import gelidum.tests.gelidum_tests.utils.dummy2

        dummy1 = gelidum.tests.gelidum_tests.utils.dummy1.Dummy(attr1=1)
        dummy2 = gelidum.tests.gelidum_tests.utils.dummy2.Dummy(attr2=2)

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

        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context1.exception))
        self.assertEqual("Can't assign attribute 'attr2' on immutable instance", str(context2.exception))
        self.assertEqual(
            "Can't assign attribute 'get_gelidum_hot_class_module' on immutable instance",
            str(context1_get_gelidum_hot_class_module.exception),
        )
        self.assertEqual(
            "Can't assign attribute 'get_gelidum_hot_class_module' on immutable instance",
            str(context2_get_gelidum_hot_class_module.exception),
        )
        self.assertEqual(1, frozen_dummy1.attr1, unpickled_frozen_dummy1.attr1)
        self.assertEqual(2, frozen_dummy2.attr2, unpickled_frozen_dummy2.attr2)

        self.assertEqual("gelidum.tests.gelidum_tests.utils.dummy1", frozen_dummy1.get_gelidum_hot_class_module())
        self.assertEqual("gelidum.tests.gelidum_tests.utils.dummy2", frozen_dummy2.get_gelidum_hot_class_module())
        self.assertEqual("Dummy", frozen_dummy1.get_gelidum_hot_class_name())
        self.assertEqual("Dummy", frozen_dummy2.get_gelidum_hot_class_name())

    def test_hot_class_module_class(self) -> None:
        from gelidum.tests.gelidum_tests.utils.dummy1 import Dummy

        dummy1 = Dummy(1)
        dummy2 = Dummy(2)
        dummy3 = Dummy(3)
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        frozen_dummy2 = freeze(dummy2, on_freeze="copy")
        frozen_dummy3 = freeze(dummy3, on_freeze="copy")

        self.assertEqual(Dummy.__name__, frozen_dummy1.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy2.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy3.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__module__, frozen_dummy1.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy2.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy3.get_gelidum_hot_class_module())

    def test_hot_class_module_internal_class(self) -> None:
        class Dummy(object):
            pass

        dummy1 = Dummy()
        dummy2 = Dummy()
        dummy3 = Dummy()
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        frozen_dummy2 = freeze(dummy2, on_freeze="copy")
        frozen_dummy3 = freeze(dummy3, on_freeze="copy")

        self.assertEqual(Dummy.__name__, frozen_dummy1.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy2.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__name__, frozen_dummy3.get_gelidum_hot_class_name())
        self.assertEqual(Dummy.__module__, frozen_dummy1.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy2.get_gelidum_hot_class_module())
        self.assertEqual(Dummy.__module__, frozen_dummy3.get_gelidum_hot_class_module())

    def test_count_frozen_classes(self) -> None:
        class Dummy(object):
            def __init__(self, attr: int) -> None:
                self.attr = attr

        dummy1 = Dummy(1)
        dummy2 = Dummy(2)
        dummy3 = Dummy(3)
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        frozen_dummy2 = freeze(dummy2, on_freeze="copy")
        frozen_dummy3 = freeze(dummy3, on_freeze="copy")
        frozen_classes = get_frozen_classes()

        self.assertSetEqual({frozen_dummy1.__class__}, frozen_classes)
        self.assertEqual(frozen_dummy1.__class__, frozen_dummy2.__class__, frozen_dummy3.__class__)

    def test_invalid_str_for_on_freeze_parameter(self) -> None:
        with self.assertRaises(AttributeError) as context:
            freeze(("one", 2, "three"), on_freeze="invalid")

        self.assertEqual(
            "Invalid value for on_freeze parameter, 'invalid' found, "
            "only 'copy' and 'inplace' are valid options if passed a string",
            str(context.exception),
        )

    def test_invalid_value_for_on_freeze_parameter(self) -> None:
        with self.assertRaises(AttributeError) as context:
            freeze(("one", 2, "three"), on_freeze=99)  # noqa

        self.assertEqual(
            "Invalid value for on_freeze parameter, '99' found, "
            "only 'copy', 'inplace' or a callable are valid options",
            str(context.exception),
        )

    def test_invalid_str_for_on_update_parameter(self) -> None:
        with self.assertRaises(AttributeError) as context:
            freeze(("one", 2, "three"), on_update="invalid")

        self.assertEqual(
            "Invalid value for on_update parameter, 'invalid' found, "
            "only 'exception', 'warning', and 'nothing' are valid options "
            "if passed a string",
            str(context.exception),
        )

    def test_invalid_value_for_on_update_parameter(self) -> None:
        with self.assertRaises(AttributeError) as context:
            freeze(("one", 2, "three"), on_update=1)  # noqa

        self.assertEqual(
            "Invalid value for on_update parameter, '1' found, "
            "only 'exception', 'warning', 'nothing' or a function are valid options",
            str(context.exception),
        )

    def test_structural_sharing_when_freezing_simple_objects(self) -> None:
        class Dummy(object):
            def __init__(self, value: int) -> None:
                self.value = value

        dummy = Dummy(value=1)
        frozen_dummy1 = freeze(dummy, on_update="exception", on_freeze="copy")
        frozen_dummy2 = freeze(frozen_dummy1, on_update="exception", on_freeze="copy")
        frozen_dummy3 = freeze(frozen_dummy2, on_update="exception", on_freeze="copy")

        self.assertNotEqual(id(dummy), id(frozen_dummy1))
        self.assertEqual(id(frozen_dummy1), id(frozen_dummy2))
        self.assertEqual(id(frozen_dummy2), id(frozen_dummy3))
        self.assertEqual(1, frozen_dummy1.value)
        self.assertEqual(1, frozen_dummy2.value)
        self.assertEqual(1, frozen_dummy3.value)

    def test_structural_sharing_when_freezing_same_objects_multiple_times(self) -> None:
        class DummyAttr(object):
            def __init__(self, value: str) -> None:
                self.value = value

        class Dummy(object):
            def __init__(self, dummy_attr: FrozenBase) -> None:
                self.dummy_attr: Union[FrozenBase, DummyAttr] = dummy_attr

        frozen_dummy_attr = freeze(DummyAttr("my_value"), on_update="exception", on_freeze="copy")
        dummy = Dummy(dummy_attr=frozen_dummy_attr)
        frozen_dummy1 = freeze(dummy, on_update="exception", on_freeze="copy")
        frozen_dummy2 = freeze(frozen_dummy1, on_update="exception", on_freeze="copy")
        frozen_dummy3 = freeze(frozen_dummy2, on_update="exception", on_freeze="copy")

        self.assertNotEqual(id(dummy), id(frozen_dummy1))
        self.assertEqual(id(frozen_dummy1), id(frozen_dummy2))
        self.assertEqual(id(frozen_dummy2), id(frozen_dummy3))
        self.assertEqual(id(dummy.dummy_attr), id(frozen_dummy_attr))
        self.assertEqual("my_value", dummy.dummy_attr.value)
        self.assertEqual("my_value", frozen_dummy_attr.value)
        self.assertEqual(id(frozen_dummy_attr), id(frozen_dummy1.dummy_attr))
        self.assertEqual(id(frozen_dummy1.dummy_attr), id(frozen_dummy2.dummy_attr))
        self.assertEqual(id(frozen_dummy2.dummy_attr), id(frozen_dummy3.dummy_attr))

    def test_structural_sharing_when_freezing_nested_objects(self) -> None:
        class Id(object):
            def __init__(self, value: str) -> None:
                self.value = value

        class Dummy(object):
            def __init__(self, value: int, obj_id: Id) -> None:
                self.value = value
                self.obj_id = freeze(obj_id, on_update="exception", on_freeze="copy")

        dummy = Dummy(value=1, obj_id=Id("unique_id"))
        frozen_dummy = freeze(dummy, on_update="exception", on_freeze="copy")

        self.assertNotEqual(id(dummy), id(frozen_dummy))
        self.assertEqual(id(dummy.obj_id.value), id(frozen_dummy.obj_id.value))
        self.assertEqual(id(dummy.obj_id), id(frozen_dummy.obj_id))
        self.assertEqual("unique_id", dummy.obj_id.value)
        self.assertEqual("unique_id", frozen_dummy.obj_id.value)

    def test_structural_sharing_immutable_list(self) -> None:
        class Dummy(object):
            def __init__(self, value: int):
                self.value = value

        class ConsList(object):
            @staticmethod
            def __freeze(item: Any) -> FrozenBase:
                return freeze(item, on_update="exception", on_freeze="copy")

            def __init__(self, *args):
                if len(args) > 0:
                    self._items = tuple(self.__freeze(arg_i) for arg_i in args)
                else:
                    self._items = tuple()

            def __getitem__(self, key) -> Any:
                return self._items[key]

            def __len__(self) -> int:
                return len(self._items)

            def __add__(self, other) -> "ConsList":
                frozen_other = freeze(other, on_update="exception", on_freeze="copy")
                return ConsList(*(self._items + (frozen_other,)))

        immutable_list_size_0 = ConsList()
        immutable_list_size_1 = immutable_list_size_0 + 1
        immutable_list_size_2 = immutable_list_size_1 + 2
        immutable_list_size_3 = immutable_list_size_2 + 3
        immutable_list_size_4 = immutable_list_size_3 + Dummy(5)
        immutable_list_size_6 = immutable_list_size_4 + Dummy(5) + "a string"

        self.assertNotEqual(id(immutable_list_size_1), id(immutable_list_size_2))
        self.assertNotEqual(id(immutable_list_size_2), id(immutable_list_size_3))
        self.assertNotEqual(id(immutable_list_size_3), id(immutable_list_size_4))
        self.assertNotEqual(id(immutable_list_size_4), id(immutable_list_size_6))
        self.assertEqual(1, len(immutable_list_size_1))
        self.assertEqual(2, len(immutable_list_size_2))
        self.assertEqual(3, len(immutable_list_size_3))
        self.assertEqual(4, len(immutable_list_size_4))
        self.assertEqual(6, len(immutable_list_size_6))
        self.assertEqual(id(immutable_list_size_1[0]), id(immutable_list_size_2[0]))
        self.assertEqual(id(immutable_list_size_1[0]), id(immutable_list_size_3[0]))
        self.assertEqual(id(immutable_list_size_1[0]), id(immutable_list_size_4[0]))
        self.assertEqual(id(immutable_list_size_1[0]), id(immutable_list_size_6[0]))
        self.assertEqual(id(immutable_list_size_2[1]), id(immutable_list_size_3[1]))
        self.assertEqual(id(immutable_list_size_2[1]), id(immutable_list_size_4[1]))
        self.assertEqual(id(immutable_list_size_2[1]), id(immutable_list_size_6[1]))
        self.assertEqual(id(immutable_list_size_3[2]), id(immutable_list_size_4[2]))
        self.assertEqual(id(immutable_list_size_3[2]), id(immutable_list_size_6[2]))
        self.assertEqual(id(immutable_list_size_4[3]), id(immutable_list_size_6[3]))

    def test_use_frozen_object_as_dict_key(self) -> None:
        class Dummy(object):
            def __init__(self, value: int) -> None:
                self.attr = value

        dummy1 = Dummy(value=1)
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        dummy2 = Dummy(value=2)
        frozen_dummy2 = freeze(dummy2, on_freeze="copy")
        my_dict = {frozen_dummy1: dummy1, frozen_dummy2: dummy2}

        self.assertEqual(2, len(my_dict))
        self.assertEqual({frozen_dummy1, frozen_dummy2}, set(my_dict.keys()))
        self.assertTrue(frozen_dummy1 in my_dict)
        self.assertEqual(dummy1, my_dict[frozen_dummy1])
        self.assertTrue(frozen_dummy2 in my_dict)
        self.assertEqual(dummy2, my_dict[frozen_dummy2])
