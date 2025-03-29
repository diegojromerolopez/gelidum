import logging
import unittest
from unittest import mock
from typing import List, Any
from unittest.mock import call

from gelidum import OnFreezeCopier, OnFreezeOriginalObjTracker, OnFreezeIdentityFunc
from gelidum import freeze
from gelidum.frozen import FrozenBase, clear_frozen_classes


class TestOnFreeze(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_on_freeze_original_obj_tracking(self):
        class DummyAttr1(object):
            def __init__(self, value: int):
                self.attr = value

        class DummyAttr2(object):
            def __init__(self, value: int):
                self.attr = value

        class Dummy(object):
            def __init__(self, value1: int, value2: int):
                self.attr1 = DummyAttr1(value1)
                self.attr2 = DummyAttr2(value2)

        dummy1 = Dummy(value1=1, value2=2)

        freezer = OnFreezeOriginalObjTracker()

        frozen_dummy1 = freeze(dummy1, on_freeze=freezer)
        original_obj = freezer.original_obj

        self.assertEqual(id(dummy1), id(original_obj))
        self.assertNotEqual(id(dummy1), id(frozen_dummy1))
        self.assertTrue(isinstance(original_obj, Dummy))
        self.assertTrue(isinstance(original_obj.attr1, DummyAttr1))
        self.assertTrue(isinstance(original_obj.attr2, DummyAttr2))
        self.assertIs(original_obj.__class__, Dummy)
        self.assertIs(original_obj.attr1.__class__, DummyAttr1)
        self.assertIs(original_obj.attr2.__class__, DummyAttr2)
        self.assertEqual(1, original_obj.attr1.attr)
        self.assertEqual(2, original_obj.attr2.attr)
        self.assertTrue(isinstance(frozen_dummy1, Dummy))
        self.assertTrue(isinstance(frozen_dummy1.attr1, DummyAttr1))
        self.assertTrue(isinstance(frozen_dummy1.attr2, DummyAttr2))
        self.assertTrue(isinstance(frozen_dummy1, FrozenBase))
        self.assertTrue(isinstance(frozen_dummy1.attr1, FrozenBase))
        self.assertTrue(isinstance(frozen_dummy1.attr2, FrozenBase))
        self.assertIsNot(frozen_dummy1.__class__, Dummy)
        self.assertIsNot(frozen_dummy1.attr1.__class__, DummyAttr1)
        self.assertIsNot(frozen_dummy1.attr2.__class__, DummyAttr2)
        self.assertEqual(1, frozen_dummy1.attr1.attr)
        self.assertEqual(2, frozen_dummy1.attr2.attr)

    def test_on_freeze_logging(self):
        class DummyAttr1(object):
            def __init__(self, value: int):
                self.attr = value

        class DummyAttr2(object):
            def __init__(self, value: int):
                self.attr = value

        class Dummy(object):
            def __init__(self, value1: int, value2: int):
                self.attr1 = DummyAttr1(value1)
                self.attr2 = DummyAttr2(value2)

        dummy1 = Dummy(value1=1, value2=2)

        class OnFreezeLogger(OnFreezeCopier):
            def __init__(self, log: logging.Logger):
                self.__log = log

            def __call__(self, obj: Any) -> Any:
                self.__log.debug(f"{obj.__class__.__name__} object frozen")
                return super().__call__(obj=obj)

        mock_log = mock.Mock()
        freezer = OnFreezeLogger(log=mock_log)

        frozen_dummy1 = freeze(dummy1, on_freeze=freezer)

        self.assertEqual(
            [call("Dummy object frozen"), call("DummyAttr1 object frozen"), call("DummyAttr2 object frozen")],
            mock_log.debug.call_args_list,
        )
        self.assertTrue(isinstance(frozen_dummy1, Dummy))
        self.assertTrue(isinstance(frozen_dummy1.attr1, DummyAttr1))
        self.assertTrue(isinstance(frozen_dummy1.attr2, DummyAttr2))
        self.assertTrue(isinstance(frozen_dummy1, FrozenBase))
        self.assertTrue(isinstance(frozen_dummy1.attr1, FrozenBase))
        self.assertTrue(isinstance(frozen_dummy1.attr2, FrozenBase))
        self.assertIsNot(frozen_dummy1.__class__, Dummy)
        self.assertIsNot(frozen_dummy1.attr1.__class__, DummyAttr1)
        self.assertIsNot(frozen_dummy1.attr2.__class__, DummyAttr2)
        self.assertEqual(1, frozen_dummy1.attr1.attr)
        self.assertEqual(2, frozen_dummy1.attr2.attr)

    def test_on_freeze_custom_freezer_in_place(self):
        class DummyAttr1(object):
            def __init__(self, value: int):
                self.attr = value

        class DummyAttr2(object):
            def __init__(self, value: int):
                self.attr = value

        class Dummy(object):
            def __init__(self, value1: int, value2: int):
                self.attr1 = DummyAttr1(value1)
                self.attr2 = DummyAttr2(value2)

        dummy1 = Dummy(value1=1, value2=2)

        class OnFreezeFullTrackingInPlace(OnFreezeIdentityFunc):
            def __init__(self):
                self.__objs: List[Any] = []

            def __call__(self, obj: Any) -> Any:
                self.__objs.append(obj)
                return super().__call__(obj=obj)

            @property
            def original_objs(self) -> List[Any]:
                return self.__objs

        freezer = OnFreezeFullTrackingInPlace()

        frozen_dummy1 = freeze(dummy1, on_freeze=freezer)
        original_objs = freezer.original_objs

        self.assertEqual(3, len(original_objs))
        self.assertEqual(id(dummy1), id(original_objs[0]))
        self.assertEqual(id(dummy1.attr1), id(original_objs[1]))
        self.assertEqual(id(dummy1.attr2), id(original_objs[2]))
        self.assertEqual(id(original_objs[0].attr1), id(original_objs[1]))
        self.assertEqual(id(original_objs[0].attr2), id(original_objs[2]))
        self.assertEqual(id(dummy1), id(frozen_dummy1))
        self.assertTrue(isinstance(original_objs[0], Dummy))
        self.assertTrue(isinstance(original_objs[1], DummyAttr1))
        self.assertTrue(isinstance(original_objs[2], DummyAttr2))
        self.assertEqual(1, original_objs[1].attr)
        self.assertEqual(2, original_objs[2].attr)
        self.assertTrue(isinstance(frozen_dummy1, Dummy))
        self.assertTrue(isinstance(frozen_dummy1.attr1, DummyAttr1))
        self.assertTrue(isinstance(frozen_dummy1.attr2, DummyAttr2))
        self.assertTrue(isinstance(frozen_dummy1, FrozenBase))
        self.assertTrue(isinstance(frozen_dummy1.attr1, FrozenBase))
        self.assertTrue(isinstance(frozen_dummy1.attr2, FrozenBase))
        self.assertIsNot(frozen_dummy1.__class__, Dummy)
        self.assertIsNot(frozen_dummy1.attr1.__class__, DummyAttr1)
        self.assertIsNot(frozen_dummy1.attr2.__class__, DummyAttr2)
        self.assertEqual(1, frozen_dummy1.attr1.attr)
        self.assertEqual(2, frozen_dummy1.attr2.attr)
