import unittest

from gelidum import freeze
from gelidum.dependencies import NUMPY_INSTALLED
from gelidum.frozen import FrozenBase, clear_frozen_classes


class TestFreezeNumpyObjects(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    @unittest.skipUnless(NUMPY_INSTALLED, 'numpy is not installed, TestFreeze.test_freeze_ndarray test skipped')
    def test_freeze_ndarray(self) -> None:
        import numpy as np

        array = np.array([1, 2, 3])
        frozen_array = freeze(array, on_freeze='copy')
        frozen_array_copy = frozen_array.copy()

        self.assertEqual(array.shape, frozen_array.shape)
        self.assertEqual(array.shape, frozen_array_copy.shape)
        self.assertEqual(array[0], frozen_array[0])
        self.assertEqual(array[1], frozen_array[1])
        self.assertEqual(array[2], frozen_array[2])
        self.assertEqual(array[0], frozen_array_copy[0])
        self.assertEqual(array[1], frozen_array_copy[1])
        self.assertEqual(array[2], frozen_array_copy[2])
        self.assertTrue(isinstance(frozen_array, FrozenBase))
        self.assertTrue(isinstance(frozen_array, np.ndarray))
        self.assertTrue(isinstance(frozen_array_copy, FrozenBase))
        self.assertTrue(isinstance(frozen_array_copy, np.ndarray))
