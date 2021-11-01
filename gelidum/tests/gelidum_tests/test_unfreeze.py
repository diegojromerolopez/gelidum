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
from typing import Dict, List, Union, Any
from unittest.mock import patch
from gelidum import FrozenException
from gelidum import freeze
from gelidum.collections import frozendict, frozenlist, frozenzet
from gelidum.frozen import clear_frozen_classes
from gelidum.unfreeze import unfreeze


class TestUnfreeze(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_unfreeze_simple_case_copy_on_freeze(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

        dummy1 = Dummy(value=1)
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        unfrozen_dummy1 = unfreeze(frozen_dummy1)

        self.assertEqual(1, unfrozen_dummy1.attr)
        self.assertEqual(unfrozen_dummy1.attr, dummy1.attr)
        self.assertEqual(unfrozen_dummy1.__class__, dummy1.__class__)
        self.assertEqual(frozen_dummy1.get_hot_class(), dummy1.__class__)

    def test_unfreeze_simple_case_freeze_inplace(self):
        class Dummy(object):
            def __init__(self, value: int):
                self.attr = value

        dummy1 = Dummy(value=1)
        frozen_dummy1 = freeze(dummy1, on_freeze="inplace")
        unfrozen_dummy1 = unfreeze(frozen_dummy1)

        self.assertEqual(1, unfrozen_dummy1.attr)
        self.assertEqual(unfrozen_dummy1.attr, dummy1.attr)
        self.assertEqual(unfrozen_dummy1.__class__, Dummy)
        self.assertNotEqual(unfrozen_dummy1.__class__, dummy1.__class__)
        self.assertNotEqual(frozen_dummy1.get_hot_class(), dummy1.__class__)

    def test_unfreeze_deep_case(self):
        class Dummy2(object):
            def __init__(self, value: int):
                self.attr = value

        class Dummy1(object):
            def __init__(self, value: Dummy2):
                self.attr = value

        dummy2 = Dummy2(value=1)
        dummy1 = Dummy1(value=dummy2)
        frozen_dummy1 = freeze(dummy1, on_freeze="copy")
        unfrozen_dummy1 = unfreeze(frozen_dummy1)

        self.assertEqual(unfrozen_dummy1.__class__, dummy1.__class__)
        self.assertEqual(Dummy1, unfrozen_dummy1.__class__)
        self.assertEqual(Dummy2, unfrozen_dummy1.attr.__class__)
        self.assertNotEqual(id(dummy1), id(unfrozen_dummy1))
        self.assertNotEqual(id(dummy2), id(unfrozen_dummy1.attr))
        self.assertEqual(1, unfrozen_dummy1.attr.attr)

    def test_frozendict(self):
        frozen_dict = frozendict({"a": 1 ,"b": 2, "c": 3})
        unfrozen_dict = unfreeze(frozen_dict)

        self.assertEqual({"a": 1, "b": 2, "c": 3}, unfrozen_dict)

    def test_frozenlist(self):
        frozen_list = frozenlist([1, 2, 3])
        unfrozen_list = unfreeze(frozen_list)

        self.assertEqual([1, 2, 3], unfrozen_list)

    def test_frozenzet(self):
        frozen_set = frozenzet({1, 2, 3})
        unfrozen_set = unfreeze(frozen_set)

        self.assertEqual({1, 2, 3}, unfrozen_set)
