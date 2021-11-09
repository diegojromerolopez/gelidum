import numpy as np
import unittest
from typing import Any, Iterator

from gelidum import FrozenException, freeze
from gelidum.collections.frozenndarray import frozenndarray
from gelidum.frozen import FrozenBase


class TestFrozenndarray(unittest.TestCase):  # noqa
    def test_freeze_int64_ndarray(self):
        array = np.ndarray([1, 2, 3], dtype=np.int64)
        frozen_array = freeze(array, on_freeze="copy")
        frozen_array_copy = frozen_array.copy()

        self.assertEqual(array.shape, frozen_array.shape)
        self.assertEqual(array.shape, frozen_array_copy.shape)
        self.assertEqual(array.tolist(), frozen_array.tolist())
        self.assertEqual(array.tolist(), frozen_array_copy.tolist())
        self.assertTrue(isinstance(frozen_array, FrozenBase))
        self.assertTrue(isinstance(frozen_array, np.ndarray))
        self.assertTrue(isinstance(frozen_array_copy, FrozenBase))
        self.assertTrue(isinstance(frozen_array_copy, np.ndarray))

    def test_freeze_int64_custom_shape_ndarray(self):
        array = np.ndarray(buffer=np.ndarray([1, 2, 3, 4]), shape=(2, 2), dtype=np.int64)
        frozen_array = freeze(array, on_freeze="copy")
        frozen_array_copy = frozen_array.copy()

        self.assertEqual(array.shape, frozen_array.shape)
        self.assertEqual(array.shape, frozen_array_copy.shape)
        self.assertEqual(array.tolist(), frozen_array.tolist())
        self.assertEqual(array.tolist(), frozen_array_copy.tolist())
        self.assertTrue(isinstance(frozen_array, FrozenBase))
        self.assertTrue(isinstance(frozen_array, np.ndarray))
        self.assertTrue(isinstance(frozen_array_copy, FrozenBase))
        self.assertTrue(isinstance(frozen_array_copy, np.ndarray))
