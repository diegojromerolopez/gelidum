import unittest
import warnings

from gelidum import FrozenException, freeze
from gelidum.collections import frozendict, frozenlist, frozenzet
from gelidum.frozen import clear_frozen_classes


class TestFreezeBuiltinObjects(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_freeze_immutable_builtin_objects(self) -> None:
        self.assertEqual(3, freeze(3))
        self.assertEqual(3.9, freeze(3.9))
        self.assertEqual(True, freeze(True))
        self.assertEqual(False, freeze(False))
        self.assertEqual(None, freeze(None))
        self.assertEqual(complex(1, 2), freeze(complex(1, 2)))
        self.assertEqual(b'Bytes', freeze(b'Bytes'))
        self.assertEqual('String', freeze('String'))

    def test_freeze_bytearray(self) -> None:
        self.assertEqual(b'Byte array', freeze(bytearray(b'Byte array')))

    def test_freeze_dict(self) -> None:
        frozen_obj: frozendict = freeze({'one': 1, 'two': 2})

        with self.assertRaises(FrozenException) as context_assignment:
            frozen_obj['one'] = 'another value'  # noqa

        with self.assertRaises(FrozenException) as context_clear:
            frozen_obj.clear()  # noqa

        with self.assertRaises(FrozenException) as context_update:
            frozen_obj.update({'three': 3})  # noqa

        with self.assertRaises(FrozenException) as context_deletion:
            del frozen_obj['one']  # noqa

        self.assertEqual(2, len(frozen_obj))
        self.assertTrue('one' in frozen_obj)
        self.assertTrue('two' in frozen_obj)
        self.assertEqual(1, frozen_obj['one'])
        self.assertEqual(2, frozen_obj['two'])
        self.assertEqual("'frozendict' object is immutable", str(context_assignment.exception))
        self.assertEqual("'frozendict' object is immutable", str(context_clear.exception))
        self.assertEqual("'frozendict' object is immutable", str(context_update.exception))
        self.assertEqual("'frozendict' object is immutable", str(context_deletion.exception))

    def test_freeze_list(self) -> None:
        frozen_list = freeze(['one', 2, 'three', ['a', 'b', 'c', 4, 5]])
        self.assertTrue(isinstance(frozen_list, frozenlist))
        self.assertEqual(4, len(frozen_list))
        self.assertEqual('one', frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual('three', frozen_list[2])
        self.assertTrue(isinstance(frozen_list[3], frozenlist))
        self.assertEqual(5, len(frozen_list[3]))
        self.assertEqual('a', frozen_list[3][0])
        self.assertEqual('b', frozen_list[3][1])
        self.assertEqual('c', frozen_list[3][2])
        self.assertEqual(4, frozen_list[3][3])
        self.assertEqual(5, frozen_list[3][4])

    def test_freeze_list_inplace_true_deprecated_parameter(self) -> None:
        with warnings.catch_warnings(record=True) as caught_warnings:
            frozen_list = freeze(['one', 2, 'three'], inplace=True)

        self.assertTrue(isinstance(frozen_list, frozenlist))
        self.assertEqual(3, len(frozen_list))
        self.assertEqual('one', frozen_list[0])
        self.assertEqual(2, frozen_list[1])
        self.assertEqual('three', frozen_list[2])
        self.assertEqual(1, len(caught_warnings))
        self.assertEqual(
            'Use of inplace is deprecated and will be removed in next major version (0.6.0)',
            str(caught_warnings[0].message),
        )

    def test_freeze_tuple(self) -> None:
        self.assertEqual(('one', 2, 'three'), freeze(('one', 2, 'three')))

    def test_freeze_set(self) -> None:
        self.assertEqual(frozenzet(['one', 2, 'three']), freeze({'one', 2, 'three'}))
