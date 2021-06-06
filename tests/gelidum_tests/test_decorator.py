import concurrent.futures
import unittest
from typing import Dict, List, Tuple, Any
from gelidum import freeze_params, FrozenException


class TestDecorator(unittest.TestCase):
    def test_decorator_with_list_input_param(self):
        @freeze_params()
        def append_to_list(a_list: List, new_item: int):
            a_list.append(new_item)

        with self.assertRaises(AttributeError) as context:
            append_to_list([], 3)

        self.assertEqual("'tuple' object has no attribute 'append'",
                         str(context.exception))

    def test_decorator_with_dict_input_param(self):
        @freeze_params()
        def add_to_dict(a_dict: Dict, new_item: Tuple[str, Any]):
            a_dict[new_item[0]] = new_item[1]

        with self.assertRaises(TypeError) as context:
            add_to_dict({}, ("key", "value"))

        self.assertEqual("'frozendict' object doesn't support item assignment",
                         str(context.exception))

    def test_decorator_with_object_input_param_object_frozen(self):
        class Dummy(object):
            def __init__(self, attr: int):
                self.attr = attr

        @freeze_params()
        def assign_to_dummy(dummy_param: Dummy, value: int):
            dummy_param.attr = value

        dummy = Dummy(1)
        with self.assertRaises(TypeError) as context:
            assign_to_dummy(dummy, 999)

        dummy.attr = 100

        self.assertEqual("Can't assign 'attr' on immutable instance",
                         str(context.exception))
        self.assertEqual(100, dummy.attr)

    def test_decorator_only_some_params(self):
        class Dummy(object):
            def __init__(self, attr: int):
                self.attr = attr

        @freeze_params(params={"dummy_const"})
        def assign_to_dummies(a_dummy: Dummy, other_dummy: Dummy, the_dummy_const: Dummy):
            a_dummy.attr = the_dummy_const.attr
            other_dummy.attr = the_dummy_const.attr

        dummy1 = Dummy(1)
        dummy2 = Dummy(2)
        dummy_const = Dummy(99)
        assign_to_dummies(a_dummy=dummy1, other_dummy=dummy2,
                          the_dummy_const=dummy_const)

        self.assertEqual(99, dummy1.attr)
        self.assertEqual(99, dummy2.attr)
        self.assertEqual(99, dummy_const.attr)

    def test_concurrent_futures(self):
        class Dummy(object):
            def __init__(self, attr: int):
                self.attr = attr

        @freeze_params()
        def job(dummy_input: Dummy):
            dummy_input.attr += 1

        thread_pool_executor = concurrent.futures.ThreadPoolExecutor(2)
        fut1 = thread_pool_executor.submit(job, Dummy(1))
        fut2 = thread_pool_executor.submit(job, Dummy(2))
        futures = [fut1, fut2]
        concurrent.futures.wait(futures)
        future_count = 0
        for future_i in futures:
            with self.assertRaises(FrozenException) as context:
                future_i.result()
            self.assertEqual("Can't assign 'attr' on immutable instance",
                             str(context.exception))
            future_count += 1
        self.assertEqual(2, future_count)
