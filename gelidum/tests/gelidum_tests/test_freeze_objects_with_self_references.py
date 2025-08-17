import unittest

from gelidum import freeze, isfrozen
from gelidum.frozen import FrozenBase


class TestFreezeObjectsWithSelfReferences(unittest.TestCase):
    def test_freeze_objects_with_self_reference(self):
        class Dummy(object):
            def __init__(self):
                self.ref = self

        dummy = Dummy()

        frozen_dummy = freeze(dummy)

        self.assertIsInstance(frozen_dummy, FrozenBase)
        self.assertIsInstance(frozen_dummy.ref, FrozenBase)
        self.assertIs(frozen_dummy.ref, frozen_dummy)
        self.assertTrue(isfrozen(frozen_dummy))
