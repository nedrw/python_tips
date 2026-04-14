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

    def test_parent_and_key_attributes(self):
        """验证 _parent 和 _key 属性是否正确设置"""
        # address 是嵌套的 ReactivableDict
        address = self.reactivable.address
        self.assertIsNotNone(address._parent)
        self.assertEqual(address._key, "address")

        # hobbies 是嵌套的 ReactivableList
        hobbies = self.reactivable.hobbies
        self.assertIsNotNone(hobbies._parent)
        self.assertEqual(hobbies._key, "hobbies")

    def test_change_bubbling(self):
        """验证变更冒泡：子对象变更时，父对象是否收到通知"""
        callback_calls = []

        def callback(val):
            callback_calls.append(val)

        # 父对象订阅通知
        self.reactivable.subscribe(callback)

        # 修改子对象的属性
        self.reactivable.address.city = "Shanghai"

        # 父对象应该收到通知
        self.assertEqual(len(callback_calls), 1)


class TestCommand(unittest.TestCase):
    """测试 Command 基类和具体命令的实现"""

    def test_command_base_class_has_undo_redo_methods(self):
        """验证 Command 基类有 undo() 和 redo() 方法"""
        from reactive.reactive import Command

        # Command 应该是一个抽象基类
        # 它应该定义 undo() 和 redo() 方法
        self.assertTrue(hasattr(Command, "undo"))
        self.assertTrue(hasattr(Command, "redo"))

    def test_setitem_command_undo_redo(self):
        """验证 SetItemCommand 可以撤销和重做"""
        from reactive.reactive import ReactivableDict, SetItemCommand

        # 创建一个 ReactivableDict
        data = {"name": "Alice", "age": 30}
        reactivable = ReactivableDict(data)

        # 创建一个 SetItemCommand
        command = SetItemCommand(reactivable, "name", "Bob", "Alice")

        # 执行命令
        command.execute()
        self.assertEqual(reactivable["name"], "Bob")

        # 撤销命令
        command.undo()
        self.assertEqual(reactivable["name"], "Alice")

        # 重做命令
        command.redo()
        self.assertEqual(reactivable["name"], "Bob")

    def test_delitem_command_undo_redo(self):
        """验证 DelItemCommand 可以撤销和重做删除操作"""
        from reactive.reactive import DelItemCommand, ReactivableDict

        # 创建一个 ReactivableDict
        data = {"name": "Alice", "age": 30}
        reactivable = ReactivableDict(data)

        # 创建一个 DelItemCommand
        command = DelItemCommand(reactivable, "age", 30)

        # 执行命令
        command.execute()
        self.assertNotIn("age", reactivable._value)

        # 撤销命令
        command.undo()
        self.assertIn("age", reactivable._value)
        self.assertEqual(reactivable["age"], 30)

        # 重做命令
        command.redo()
        self.assertNotIn("age", reactivable._value)

    def test_insert_command_undo_redo(self):
        """验证 InsertCommand 可以撤销和重做插入操作"""
        from reactive.reactive import InsertCommand, ReactivableList

        # 创建一个 ReactivableList
        data = ["a", "b", "c"]
        reactivable = ReactivableList(data)

        # 创建一个 InsertCommand
        command = InsertCommand(reactivable, 1, "x")

        # 执行命令
        command.execute()
        self.assertEqual(reactivable._value, ["a", "x", "b", "c"])

        # 撤销命令
        command.undo()
        self.assertEqual(reactivable._value, ["a", "b", "c"])

        # 重做命令
        command.redo()
        self.assertEqual(reactivable._value, ["a", "x", "b", "c"])

    def test_append_command_undo_redo(self):
        """验证 AppendCommand 可以撤销和重做追加操作"""
        from reactive.reactive import AppendCommand, ReactivableList

        # 创建一个 ReactivableList
        data = ["a", "b"]
        reactivable = ReactivableList(data)

        # 创建一个 AppendCommand
        command = AppendCommand(reactivable, "c")

        # 执行命令
        command.execute()
        self.assertEqual(reactivable._value, ["a", "b", "c"])

        # 撤销命令
        command.undo()
        self.assertEqual(reactivable._value, ["a", "b"])

        # 重做命令
        command.redo()
        self.assertEqual(reactivable._value, ["a", "b", "c"])

    def test_pop_command_undo_redo(self):
        """验证 PopCommand 可以撤销和重做弹出操作"""
        from reactive.reactive import PopCommand, ReactivableList

        # 创建一个 ReactivableList
        data = ["a", "b", "c"]
        reactivable = ReactivableList(data)

        # 创建一个 PopCommand
        command = PopCommand(reactivable, 1, "b")

        # 执行命令
        command.execute()
        self.assertEqual(reactivable._value, ["a", "c"])

        # 撤销命令
        command.undo()
        self.assertEqual(reactivable._value, ["a", "b", "c"])

        # 重做命令
        command.redo()
        self.assertEqual(reactivable._value, ["a", "c"])

    def test_composite_command_undo_redo(self):
        """验证 CompositeCommand 可以撤销和重做多个子命令"""
        from reactive.reactive import CompositeCommand, ReactivableDict, SetItemCommand

        # 创建一个 ReactivableDict
        data = {"name": "Alice", "age": 30}
        reactivable = ReactivableDict(data)

        # 创建多个子命令
        command1 = SetItemCommand(reactivable, "name", "Bob", "Alice")
        command2 = SetItemCommand(reactivable, "age", 40, 30)

        # 创建一个 CompositeCommand
        composite = CompositeCommand([command1, command2])

        # 执行命令
        composite.execute()
        self.assertEqual(reactivable["name"], "Bob")
        self.assertEqual(reactivable["age"], 40)

        # 撤销命令（逆序撤销）
        composite.undo()
        self.assertEqual(reactivable["name"], "Alice")
        self.assertEqual(reactivable["age"], 30)

        # 重做命令（正序重做）
        composite.redo()
        self.assertEqual(reactivable["name"], "Bob")
        self.assertEqual(reactivable["age"], 40)


if __name__ == "__main__":
    unittest.main()
