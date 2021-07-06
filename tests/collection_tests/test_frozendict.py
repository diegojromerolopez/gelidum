import unittest
from typing import Any, Iterator

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
