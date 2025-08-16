import unittest
from typing import List

from gelidum import FrozenException, freeze
from gelidum.frozen import clear_frozen_classes


class TestFreezeDataclasses(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_freeze_simple_dataclass(self) -> None:
        from dataclasses import dataclass

        @dataclass
        class Dummy:
            attr1: str
            attr2: str
            attr3: str = '0'

        dummy = Dummy(attr1='1', attr2='2', attr3='3')
        frozen_dummy_on_freeze_copy = freeze(dummy, on_freeze='copy')
        frozen_dummy_inplace = freeze(dummy, on_freeze='inplace')

        with self.assertRaises(FrozenException) as context_on_freeze_copy:
            frozen_dummy_on_freeze_copy.attr1 = '2'

        with self.assertRaises(FrozenException) as context_inplace:
            frozen_dummy_inplace.attr2 = '2'

        self.assertEqual("Can't assign attribute 'attr1' on immutable instance", str(context_on_freeze_copy.exception))
        self.assertEqual("Can't assign attribute 'attr2' on immutable instance", str(context_inplace.exception))
        self.assertEqual(id(dummy), id(frozen_dummy_inplace))
        self.assertNotEqual(id(dummy), id(frozen_dummy_on_freeze_copy))

    def test_freeze_nested_dataclass(self) -> None:
        from dataclasses import dataclass

        @dataclass
        class ItemType:
            id: int
            name: str

        @dataclass
        class Item:
            id: int
            name: str
            order: int
            type: ItemType

        @dataclass
        class Database:
            items: List[Item]

        item_type1 = ItemType(1, 'item type 1')
        item_type2 = ItemType(2, 'item type 2')

        dummy_database = Database(
            items=[
                Item(1, 'item 1', 5, item_type1),
                Item(2, 'item 2', 1, item_type1),
                Item(3, 'item 3', 99, item_type2),
            ]
        )
        frozen_dummy_on_freeze_copy = freeze(dummy_database, on_freeze='copy')
        frozen_dummy_inplace = freeze(dummy_database, on_freeze='inplace')

        with self.assertRaises(FrozenException) as context_on_freeze_copy_items_assignment:
            frozen_dummy_on_freeze_copy.items = []

        with self.assertRaises(FrozenException) as context_on_freeze_copy_item_assignment:
            frozen_dummy_on_freeze_copy.items[0] = Item(9, 'item 9', 99, item_type1)

        with self.assertRaises(FrozenException) as context_inplace:
            frozen_dummy_inplace.attr2 = '2'

        self.assertEqual(
            "Can't assign attribute 'items' on immutable instance",
            str(context_on_freeze_copy_items_assignment.exception),
        )
        self.assertEqual("'frozenlist' object is immutable", str(context_on_freeze_copy_item_assignment.exception))
        self.assertEqual("Can't assign attribute 'attr2' on immutable instance", str(context_inplace.exception))
        self.assertEqual(id(dummy_database), id(frozen_dummy_inplace))
        self.assertNotEqual(id(dummy_database), id(frozen_dummy_on_freeze_copy))
