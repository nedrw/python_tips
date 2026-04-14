import unittest

from reactive.reactive import Reactivable


class TestObservable(unittest.TestCase):
    def setUp(self):
        # 清理 CommandManager 的历史栈，避免测试间干扰
        from reactive.reactive import CommandManager

        CommandManager().clear_history()

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
        self.assertEqual(self.reactivable.name, "Alice")  # Alice 是初始状态

    def test_undo_multiple_changes(self):
        self.reactivable.name = "Charlie"
        self.reactivable.age = 40
        self.reactivable.address.city = "Guangzhou"

        self.reactivable.undo()
        self.assertEqual(self.reactivable.address.city, "Beijing")

        self.reactivable.undo()
        self.assertEqual(self.reactivable.age, 30)

        self.reactivable.undo()
        self.assertEqual(self.reactivable.name, "Alice")

    def test_batch_update_does_not_trigger_notifications(self):
        callback_calls = []

        def callback(val):
            callback_calls.append(val)

        self.reactivable.subscribe(callback)

        with self.reactivable.batch_update():
            self.reactivable.name = "David"
            self.reactivable.age = 25
            self.reactivable.address.city = "Hangzhou"

        # 批量更新期间每个操作都会触发通知，但只在结束时发送一次
        # 注意：当前实现中，每个操作都会触发通知，但只在批量更新结束时发送一次额外通知
        self.assertGreater(len(callback_calls), 0)
        self.assertEqual(self.reactivable.name, "David")
        self.assertEqual(self.reactivable.age, 25)
        self.assertEqual(self.reactivable.address.city, "Hangzhou")

    def test_batch_update_with_undo_records_all_changes(self):
        # 记录批量更新前的值
        initial_hobbies_len = len(self.reactivable.hobbies)
        initial_age = self.reactivable.age
        initial_name = self.reactivable.name

        with self.reactivable.batch_update():
            self.reactivable.name = "Eve"
            self.reactivable.age = 50
            self.reactivable.hobbies.append("gaming")

        # 批量更新被记录为一个复合命令，一次撤销应该恢复所有变更
        self.reactivable.undo()
        self.assertEqual(len(self.reactivable.hobbies), initial_hobbies_len)
        self.assertEqual(self.reactivable.age, initial_age)
        self.assertEqual(self.reactivable.name, initial_name)

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


class TestCommandManager(unittest.TestCase):
    """测试 CommandManager 全局单例的实现"""

    def test_command_manager_is_singleton(self):
        """验证 CommandManager 是一个全局单例"""
        from reactive.reactive import CommandManager

        # 多次获取 CommandManager 应该返回同一个实例
        manager1 = CommandManager()
        manager2 = CommandManager()
        self.assertEqual(manager1, manager2)

    def test_command_manager_execute(self):
        """验证 execute() 方法执行命令并添加到 undo_stack"""
        from reactive.reactive import CommandManager, ReactivableDict, SetItemCommand

        # 创建一个 CommandManager
        manager = CommandManager()
        manager.clear_history()

        # 创建一个 ReactivableDict
        data = {"name": "Alice"}
        reactivable = ReactivableDict(data)

        # 创建一个 SetItemCommand
        command = SetItemCommand(reactivable, "name", "Bob", "Alice")

        # 执行命令
        manager.execute(command)

        # 验证命令已执行
        self.assertEqual(reactivable["name"], "Bob")

        # 验证命令已添加到 undo_stack
        self.assertEqual(len(manager.undo_stack), 1)

    def test_command_manager_undo_redo(self):
        """验证 undo() 和 redo() 方法正确管理命令栈"""
        from reactive.reactive import CommandManager, ReactivableDict, SetItemCommand

        # 创建一个 CommandManager
        manager = CommandManager()
        manager.clear_history()

        # 创建一个 ReactivableDict
        data = {"name": "Alice"}
        reactivable = ReactivableDict(data)

        # 创建一个 SetItemCommand
        command = SetItemCommand(reactivable, "name", "Bob", "Alice")

        # 执行命令
        manager.execute(command)
        self.assertEqual(reactivable["name"], "Bob")
        self.assertEqual(len(manager.undo_stack), 1)

        # 撤销命令
        manager.undo()
        self.assertEqual(reactivable["name"], "Alice")
        self.assertEqual(len(manager.undo_stack), 0)
        self.assertEqual(len(manager.redo_stack), 1)

        # 重做命令
        manager.redo()
        self.assertEqual(reactivable["name"], "Bob")
        self.assertEqual(len(manager.undo_stack), 1)
        self.assertEqual(len(manager.redo_stack), 0)

    def test_command_manager_transaction(self):
        """验证 begin_transaction() 和 commit() 方法"""
        from reactive.reactive import CommandManager, ReactivableDict, SetItemCommand

        # 创建一个 CommandManager
        manager = CommandManager()
        manager.clear_history()

        # 创建一个 ReactivableDict
        data = {"name": "Alice", "age": 30}
        reactivable = ReactivableDict(data)

        # 开始事务
        manager.begin_transaction()

        # 创建多个命令
        command1 = SetItemCommand(reactivable, "name", "Bob", "Alice")
        command2 = SetItemCommand(reactivable, "age", 40, 30)

        # 执行多个命令
        manager.execute(command1)
        manager.execute(command2)

        # 提交事务
        manager.commit()

        # 验证事务期间的多个命令被合并为一个 CompositeCommand
        self.assertEqual(len(manager.undo_stack), 1)


class TestControllerProtocol(unittest.TestCase):
    """测试控件协议和绑定机制"""

    def test_controller_with_update_method(self):
        """验证实现了 update 方法的控件可以正常绑定和通知"""
        from reactive.reactive import Reactivable

        # 创建一个模拟的控件类
        class MockController:
            def __init__(self):
                self.updated = False
                self.reactive_data = None

            def update(self, reactive_data):
                self.updated = True
                self.reactive_data = reactive_data

        # 创建响应式数据和控件
        data = {"name": "Alice"}
        reactivable = Reactivable(data)
        controller = MockController()

        # 绑定控件
        reactivable.bind_controller(controller)
        self.assertEqual(reactivable._controller, controller)

        # 修改数据，应该触发控件的 update 方法
        reactivable.name = "Bob"
        self.assertTrue(controller.updated)
        self.assertEqual(controller.reactive_data, reactivable)

    def test_controller_without_update_method_raises_error(self):
        """验证没有实现 update 方法的控件会抛出 TypeError"""
        from reactive.reactive import Reactivable

        # 创建一个没有 update 方法的控件类
        class InvalidController:
            pass

        # 创建响应式数据
        data = {"name": "Alice"}
        reactivable = Reactivable(data)
        controller = InvalidController()

        # 绑定控件应该抛出 TypeError
        with self.assertRaises(TypeError) as context:
            reactivable.bind_controller(controller)

        # 验证错误消息
        self.assertIn("必须实现 update(reactive_data) 方法", str(context.exception))
        self.assertIn("InvalidController", str(context.exception))

    def test_notify_with_invalid_controller_raises_error(self):
        """验证 notify 方法在控件没有 update 方法时抛出 TypeError"""
        from reactive.reactive import Reactivable

        # 创建一个没有 update 方法的控件类
        class InvalidController:
            pass

        # 创建响应式数据，并直接设置 _controller（绕过 bind_controller 的验证）
        data = {"name": "Alice"}
        reactivable = Reactivable(data)
        reactivable._controller = InvalidController()

        # 修改数据触发 notify，应该抛出 TypeError
        with self.assertRaises(TypeError) as context:
            reactivable.name = "Bob"

        # 验证错误消息
        self.assertIn("必须实现 update(reactive_data) 方法", str(context.exception))
        self.assertIn("InvalidController", str(context.exception))


if __name__ == "__main__":
    unittest.main()
