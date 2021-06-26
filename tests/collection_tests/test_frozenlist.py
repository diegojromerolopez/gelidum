import unittest

from gelidum.collections.frozenlist import frozenlist


class TestFrozenlist(unittest.TestCase):  # noqa
    def test_getitem(self):
        frozen_list = frozenlist(1, 2, 3)

        with self.assertRaises(IndexError) as context:
            _val = frozen_list[4]

        self.assertEqual(1, frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual(3, frozen_list[2])
        self.assertEqual("frozenlist index out of range", str(context.exception))

    def test_tree(self):
        cons(cons(1, 2), cons(3, 4))

