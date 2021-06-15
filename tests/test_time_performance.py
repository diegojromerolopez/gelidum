import time
import unittest
from gelidum import freeze
from gelidum.frozen import clear_frozen_classes


class TestTimePerformance(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

    def test_freeze_inplace_or_not(self):
        class DummyAttrLevel3(object):
            def __init__(self, attr: str):
                self.attr = attr

        class DummyAttrLevel2(object):
            def __init__(self, attr: str):
                self.attr = DummyAttrLevel3(attr)

        class DummyAttrLevel1(object):
            def __init__(self, attr: str):
                self.attr = DummyAttrLevel2(attr)

        class Dummy(object):
            def __init__(self, attr: str):
                self.attr = DummyAttrLevel1(attr)
                for attr_index in range(0, 10000):
                    setattr(self, f"attr{attr_index+1}", attr)

        dummy1 = Dummy(attr="1")
        start_inplace = time.time()
        freeze(dummy1, inplace=True)
        spent_time_inplace = time.time() - start_inplace
        dummy2 = Dummy(attr="1")
        start_not_inplace = time.time()
        freeze(dummy2, inplace=False)
        spent_time_not_inplace = time.time() - start_not_inplace

        self.assertLessEqual(spent_time_inplace, spent_time_not_inplace)

    def test_many_attr_class_freeze(self):
        class BigDummy(object):
            def __init__(self, attr: str):
                for attr_index in range(0, 10000):
                    setattr(self, f"attr{attr_index+1}", attr)

        dummy = BigDummy(attr="1")

        spent_times = []
        for i in range(5):
            start = time.time()
            freeze(dummy, inplace=False)
            spent_times.append(time.time() - start)

        spent_time = sum(spent_times) / len(spent_times)

        self.assertLessEqual(spent_time, 0.4)

