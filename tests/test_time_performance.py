import time
import unittest
from gelidum import freeze
from gelidum.frozen import clear_frozen_classes


class TestTimePerformance(unittest.TestCase):
    def setUp(self) -> None:
        clear_frozen_classes()

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

