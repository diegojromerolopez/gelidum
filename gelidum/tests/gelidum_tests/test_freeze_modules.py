import unittest

from gelidum import FrozenException, freeze
from gelidum.frozen import clear_frozen_classes


class TestFreezeModules(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_freeze_this_module(self):
        import sys

        with self.assertRaises(FrozenException) as context:
            freeze(sys.modules[__name__])

        self.assertEqual('Modules cannot be frozen', str(context.exception))

    def test_freeze_modules_copy(self):
        import sys

        with self.assertRaises(FrozenException) as context:
            freeze(sys, on_freeze='copy')

        self.assertEqual('Modules cannot be frozen', str(context.exception))

    def test_freeze_modules_inplace(self):
        import sys

        with self.assertRaises(FrozenException) as context:
            freeze(sys, on_freeze='inplace')

        self.assertEqual('Modules cannot be frozen', str(context.exception))
