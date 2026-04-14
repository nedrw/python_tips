import unittest

from reactive.reactive import Reactivable


class TestObservable(unittest.TestCase):
    def setUp(self):
        self.data = {
            "name": "Alice",
            "age": 30,
            "hobbies": ["reading", "coding"],
            "address": {"city": "Beijing", "zip": "100000"},
        }
        self.reactivable = Reactivable(self.data)

    def test_initial_value(self):
        self.assertEqual(self.reactivable.name, "Alice")
        self.assertEqual(self.reactivable.age, 30)
        self.assertEqual(self.reactivable.address.city, "Beijing")

    def test_property_change_triggers_callback(self):
        callback_calls = []

        def callback(val):
            callback_calls.append(val)

        self.reactivable.subscribe(callback)
        self.reactivable.name = "Bob"

        self.assertEqual(len(callback_calls), 1)
        self.assertEqual(self.reactivable.name, "Bob")

    def test_nested_dict_access_and_update(self):
        self.assertEqual(self.reactivable.address.city, "Beijing")
        self.reactivable.address.city = "Shanghai"
        self.assertEqual(self.reactivable.address.city, "Shanghai")

    def test_list_access_and_mutations(self):
        self.assertEqual(self.reactivable.hobbies[0], "reading")
        self.reactivable.hobbies.append("traveling")
        self.assertEqual(self.reactivable.hobbies[-1], "traveling")

        self.reactivable.hobbies.pop(1)
        self.assertEqual(len(self.reactivable.hobbies), 2)

    def test_undo_single_change(self):
        self.reactivable.name = "Charlie"
        self.reactivable.undo()
        self.assertEqual(self.reactivable.name, "Bob")  # Bob 是上一个状态

    def test_undo_multiple_changes(self):
        self.reactivable.name = "Charlie"
        self.reactivable.age = 40
        self.reactivable.address.city = "Guangzhou"

        self.reactivable.undo()
        self.assertEqual(self.reactivable.address.city, "Shanghai")

        self.reactivable.undo()
        self.assertEqual(self.reactivable.age, 30)

        self.reactivable.undo()
        self.assertEqual(self.reactivable.name, "Bob")

    def test_batch_update_does_not_trigger_notifications(self):
        callback_calls = []

        def callback(val):
            callback_calls.append(val)

        self.reactivable.subscribe(callback)

        with self.reactivable.batch_update():
            self.reactivable.name = "David"
            self.reactivable.age = 25
            self.reactivable.address.city = "Hangzhou"

        self.assertEqual(len(callback_calls), 1)
        self.assertEqual(self.reactivable.name, "David")
        self.assertEqual(self.reactivable.age, 25)
        self.assertEqual(self.reactivable.address.city, "Hangzhou")

    def test_batch_update_with_undo_records_all_changes(self):
        with self.reactivable.batch_update():
            self.reactivable.name = "Eve"
            self.reactivable.age = 50
            self.reactivable.hobbies.append("gaming")

        self.reactivable.undo()
        self.assertEqual(self.reactivable.hobbies[-1], "gaming")

        self.reactivable.undo()
        self.assertEqual(self.reactivable.age, 25)

        self.reactivable.undo()
        self.assertEqual(self.reactivable.name, "David")

    def test_setattr_for_non_existent_attribute(self):
        """测试设置不存在的属性时不会抛出 AttributeError"""
        # 这个测试验证 __setattr__ 在第一次设置属性时不会崩溃
        reactivable = Reactivable({"name": "Alice"})
        # 设置新属性应该正常工作
        reactivable.name = "Bob"
        self.assertEqual(reactivable.name, "Bob")

    def test_reactivable_list_delitem(self):
        """测试 ReactivableList 的 __delitem__ 方法"""
        # 测试删除列表元素
        hobbies = self.reactivable.hobbies
        self.assertEqual(len(hobbies), 2)

        # 删除第一个元素
        del hobbies[0]
        self.assertEqual(len(hobbies), 1)
        self.assertEqual(hobbies[0], "coding")

        # 删除最后一个元素
        del hobbies[0]
        self.assertEqual(len(hobbies), 0)

    def test_reactivable_dict_delitem(self):
        """测试 ReactivableDict 的 __delitem__ 方法"""
        # 测试删除字典键
        address = self.reactivable.address
        self.assertIn("city", address)
        self.assertIn("zip", address)

        # 删除一个键
        del address["city"]
        self.assertNotIn("city", address)
        self.assertIn("zip", address)


if __name__ == "__main__":
    unittest.main()
