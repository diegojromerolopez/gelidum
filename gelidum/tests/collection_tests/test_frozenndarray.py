import unittest

from gelidum import NUMPY_INSTALLED, freeze
from gelidum.frozen import FrozenBase


@unittest.skipUnless(NUMPY_INSTALLED, "numpy is not installed, TestFrozenndarray tests skipped")
class TestFrozenndarray(unittest.TestCase):  # noqa
    def test_freeze_int64_ndarray(self):
        import numpy as np

        array = np.array([1, 2, 3], dtype=np.int64).reshape((1, 3))
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
        import numpy as np

        array = np.array([1, 2, 3, 4], dtype=np.int64).reshape((2, 2))
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

    def test_assignment_single_value(self):
        import numpy as np

        array = np.array([1, 2, 3, 4], dtype=np.int64).reshape((2, 2))
        frozen_array = freeze(array, on_freeze="copy")

        with self.assertRaises(ValueError) as context:
            frozen_array[0, 1] = 99

        array[0, 1] = 99

        self.assertEqual("assignment destination is read-only", str(context.exception))
        self.assertEqual(2, frozen_array[0, 1])
        self.assertEqual(99, array[0, 1])

    def test_assignment_multiple_values(self):
        import numpy as np

        array = np.array([1, 2, 3, 4], dtype=int).reshape((2, 2))
        frozen_array = freeze(array, on_freeze="copy")

        with self.assertRaises(ValueError) as context:
            frozen_array[:, 0] = 99

        array[:, 0] = 99

        self.assertEqual("assignment destination is read-only", str(context.exception))
        self.assertEqual(99, array[0, 0])
        self.assertEqual(99, array[1, 0])
        self.assertEqual(1, frozen_array[0, 0])
        self.assertEqual(3, frozen_array[1, 0])
