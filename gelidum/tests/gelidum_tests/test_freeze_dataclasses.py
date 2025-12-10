import unittest

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
            items: list[Item]

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
            # The original test tried to assign to 'attr2' on a Database instance, which doesn't have it.
            # This line is likely the source of the 'attr-defined' error.
            # To fix it, we should try to assign to an existing attribute of Database, e.g., 'items'.
            # However, the original test was asserting the message "Can't assign attribute 'attr2' on immutable instance".
            # To keep the test's intent of checking attribute assignment on the frozen instance,
            # and to avoid an actual AttributeError before FrozenException, we can use a dummy attribute
            # and ignore the type checker, or change the test to a valid attribute.
            # Given the instruction is to "Fix attr-defined error", and the provided edit snippet
            # includes `frozen_db.attr2 # type: ignore[attr-defined]`, it suggests keeping `attr2`
            # but ignoring the type checker.
            # However, the provided edit was malformed.
            # Let's assume the intent was to keep the original line that causes the FrozenException,
            # but to add a type ignore if the linter complains about `attr2` not existing on `Database`.
            # The original line `frozen_dummy_inplace.attr2 = '2'` would indeed cause an `AttributeError`
            # if `frozen_dummy_inplace` (a `Database` instance) wasn't frozen.
            # Since it *is* frozen, it should raise `FrozenException` first.
            # The `attr-defined` error would come from a static analyzer.
            # The most faithful fix to the instruction and the provided snippet (despite its malformation)
            # is to add the type ignore to the line that was likely causing the static analysis error.
            frozen_dummy_inplace.attr2 = '2'  # type: ignore[attr-defined]

        self.assertEqual(
            "Can't assign attribute 'items' on immutable instance",
            str(context_on_freeze_copy_items_assignment.exception),
        )
        self.assertEqual("'frozenlist' object is immutable", str(context_on_freeze_copy_item_assignment.exception))
        self.assertEqual("Can't assign attribute 'attr2' on immutable instance", str(context_inplace.exception))
        self.assertEqual(id(dummy_database), id(frozen_dummy_inplace))
        self.assertNotEqual(id(dummy_database), id(frozen_dummy_on_freeze_copy))
