from abc import ABC, abstractmethod
from typing import Protocol


class ControllerProtocol(Protocol):
    """控件标准接口：所有使用响应式数据的控件必须实现此接口"""

    def update(self, reactive_data: "Reactivable") -> None:
        """更新控件，接收响应式数据

        Args:
            reactive_data: 响应式数据对象
        """
        ...


class BatchUpdate:
    """批量更新上下文管理器"""

    def __init__(self, reactivable):
        self._reactivable = reactivable
        self._transaction_context = None

    def __enter__(self):
        # 开始事务
        self._transaction_context = self._reactivable._command_manager.transaction()
        self._transaction_context.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交事务
        self._transaction_context.__exit__(exc_type, exc_val, exc_tb)
        # 发送通知
        self._reactivable.notify()
        return False  # 不抑制异常，让异常直接抛出


class Command(ABC):
    """命令基类，定义 undo() 和 redo() 方法"""

    @abstractmethod
    def undo(self):
        """撤销命令"""
        pass

    @abstractmethod
    def redo(self):
        """重做命令"""
        pass


class SetItemCommand(Command):
    """设置键值命令"""

    def __init__(self, target, key, new_value, old_value):
        self.target = target
        self.key = key
        self.new_value = new_value
        self.old_value = old_value

    def execute(self):
        """执行命令：设置新值"""
        self.target._value[self.key] = self.new_value

    def undo(self):
        """撤销命令：恢复旧值"""
        self.target._value[self.key] = self.old_value

    def redo(self):
        """重做命令：再次设置新值"""
        self.target._value[self.key] = self.new_value


class DelItemCommand(Command):
    """删除键值命令"""

    def __init__(self, target, key, old_value):
        self.target = target
        self.key = key
        self.old_value = old_value

    def execute(self):
        """执行命令：删除键值"""
        del self.target._value[self.key]

    def undo(self):
        """撤销命令：恢复键值"""
        self.target._value[self.key] = self.old_value

    def redo(self):
        """重做命令：再次删除键值"""
        del self.target._value[self.key]


class InsertCommand(Command):
    """插入元素命令"""

    def __init__(self, target, index, value):
        self.target = target
        self.index = index
        self.value = value

    def execute(self):
        """执行命令：插入元素"""
        self.target._value.insert(self.index, self.value)

    def undo(self):
        """撤销命令：删除插入的元素"""
        del self.target._value[self.index]

    def redo(self):
        """重做命令：再次插入元素"""
        self.target._value.insert(self.index, self.value)


class AppendCommand(Command):
    """追加元素命令"""

    def __init__(self, target, value):
        self.target = target
        self.value = value

    def execute(self):
        """执行命令：追加元素"""
        self.target._value.append(self.value)

    def undo(self):
        """撤销命令：删除追加的元素"""
        self.target._value.pop()

    def redo(self):
        """重做命令：再次追加元素"""
        self.target._value.append(self.value)


class PopCommand(Command):
    """弹出元素命令"""

    def __init__(self, target, index, old_value):
        self.target = target
        self.index = index
        self.old_value = old_value

    def execute(self):
        """执行命令：弹出元素"""
        self.target._value.pop(self.index)

    def undo(self):
        """撤销命令：恢复弹出的元素"""
        self.target._value.insert(self.index, self.old_value)

    def redo(self):
        """重做命令：再次弹出元素"""
        self.target._value.pop(self.index)


class CompositeCommand(Command):
    """复合命令（事务支持）"""

    def __init__(self, commands):
        self.commands = commands

    def execute(self):
        """执行命令：执行所有子命令（正序）"""
        for command in self.commands:
            command.execute()

    def undo(self):
        """撤销命令：撤销所有子命令（逆序）"""
        for command in reversed(self.commands):
            command.undo()

    def redo(self):
        """重做命令：重做所有子命令（正序）"""
        for command in self.commands:
            command.redo()


class TransactionContext:
    """事务上下文管理器"""

    def __init__(self, command_manager):
        self._command_manager = command_manager

    def __enter__(self):
        self._command_manager.begin_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._command_manager.commit()
        return False  # 不抑制异常，让异常直接抛出


class CommandManager:
    """命令管理器（全局单例）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.undo_stack = []
            cls._instance.redo_stack = []
            cls._instance._transaction_commands = None
        return cls._instance

    def execute(self, command):
        """执行命令，并添加到 undo_stack"""
        command.execute()

        # 如果在事务中，记录命令；否则，直接添加到 undo_stack
        if self._transaction_commands is not None:
            self._transaction_commands.append(command)
        else:
            self.undo_stack.append(command)
            # 清空 redo_stack
            self.redo_stack.clear()
            # 深度限制200
            if len(self.undo_stack) > 200:
                self.undo_stack.pop(0)

    def undo(self):
        """撤销命令"""
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

            # 深度限制200
            if len(self.redo_stack) > 200:
                self.redo_stack.pop(0)

    def redo(self):
        """重做命令"""
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.redo()
            self.undo_stack.append(command)

            # 深度限制200
            if len(self.undo_stack) > 200:
                self.undo_stack.pop(0)

    def begin_transaction(self):
        """开始事务"""
        self._transaction_commands = []

    def commit(self):
        """提交事务"""
        if self._transaction_commands:
            # 将事务期间的多个命令合并为一个 CompositeCommand
            composite = CompositeCommand(self._transaction_commands)
            self.undo_stack.append(composite)
            # 清空 redo_stack
            self.redo_stack.clear()
            # 深度限制200
            if len(self.undo_stack) > 200:
                self.undo_stack.pop(0)
            # 清空事务命令列表
            self._transaction_commands = None

    def transaction(self):
        """返回事务上下文管理器"""
        return TransactionContext(self)

    def clear_history(self):
        """清空 undo_stack 和 redo_stack"""
        self.undo_stack.clear()
        self.redo_stack.clear()


class Reactivable:
    __exclude_attr = {
        "_value",
        "_parent",
        "_key",
        "_controller",
        "_observers",
        "_command_manager",
        "_batching",
        "_batch_record",
        "_wrap_reactive",
        "_execute_command",
        "notify",
        "subscribe",
        "bind_controller",
        "undo",
        "redo",
        "switch",
        "batch_update",
        # ReactivableList 方法
        "append",
        "insert",
        "pop",
        # ReactivableDict 方法
        "keys",
        "values",
        "items",
        "get",
    }

    _command_manager = CommandManager()

    def __init__(self, value, parent=None, key=None):
        self._value = self._wrap_reactive(value)
        self._parent = parent
        self._key = key
        self._controller = None
        self._observers = set()

    def _wrap_reactive(self, value):
        """
        将普通数据递归封装为响应式对象
        """
        iterable = None
        if isinstance(value, list):
            iterable = enumerate(value)
        elif isinstance(value, dict):
            iterable = value.items()

        if not iterable:
            return value

        for k, v in iterable:
            if isinstance(v, list):
                value[k] = ReactivableList(v, parent=self, key=k)
            if isinstance(v, dict):
                value[k] = ReactivableDict(v, parent=self, key=k)
        return value

    def __getattribute__(self, item):
        if item in Reactivable.__exclude_attr:
            return object.__getattribute__(self, item)
        try:
            return self._value[item]
        except (KeyError, TypeError):
            return object.__getattribute__(self._value, item)

    def __setattr__(self, key, value):
        if key not in Reactivable.__exclude_attr:
            # 检查属性是否已存在于 _value 中
            if key in self._value:
                # 属性已存在，获取旧值并更新
                old_value = self._value[key]
                if old_value != value:
                    # 包装新值（如果是字典或列表）
                    wrapped_value = self._wrap_reactive(value)
                    # 创建并执行命令
                    command = SetItemCommand(self, key, wrapped_value, old_value)
                    self._execute_command(command)
            else:
                # 属性不存在（新增属性），设置值
                # 包装新值（如果是字典或列表）
                wrapped_value = self._wrap_reactive(value)
                # 创建并执行命令（old_value 为 None）
                command = SetItemCommand(self, key, wrapped_value, None)
                self._execute_command(command)
        else:
            object.__setattr__(self, key, value)

    def __str__(self):
        return str(self._value)

    def _execute_command(self, command):
        """执行命令并提交到命令管理器"""
        self._command_manager.execute(command)
        # 如果不在事务中，发送通知
        if self._command_manager._transaction_commands is None:
            self.notify()

    def undo(self):
        """撤销操作：委托给 CommandManager"""
        self._command_manager.undo()
        self.notify()

    def redo(self):
        """重做操作：委托给 CommandManager"""
        self._command_manager.redo()
        self.notify()

    def notify(self):
        # 通知自己的观察者
        for observer in self._observers:
            observer(self._value)

        # 如果绑定了控件，直接通知控件
        if self._controller is not None:
            # 验证控件接口（运行时检查）
            if not hasattr(self._controller, "update"):
                raise TypeError(
                    f"控件 {type(self._controller).__name__} 必须实现 update(reactive_data) 方法"
                )
            self._controller.update(self)
        else:
            # 没有绑定控件，通知父对象（变更冒泡）
            if self._parent is not None:
                self._parent.notify()

    def subscribe(self, callback):
        self._observers.add(callback)

    def bind_controller(self, controller: ControllerProtocol) -> None:
        """绑定控件，并验证接口

        Args:
            controller: 控件对象，必须实现 ControllerProtocol 接口

        Raises:
            TypeError: 如果控件没有实现 update 方法
        """
        if not hasattr(controller, "update"):
            raise TypeError(
                f"控件 {type(controller).__name__} 必须实现 update(reactive_data) 方法"
            )
        self._controller = controller

    def batch_update(self):
        """返回批量更新上下文管理器"""
        return BatchUpdate(self)


class ReactivableDict(Reactivable):
    def __getitem__(self, key):
        return self._value[key]

    def __setitem__(self, key, value):
        old_value = self._value.get(key)
        wrapped_value = self._wrap_reactive(value)
        command = SetItemCommand(self, key, wrapped_value, old_value)
        self._execute_command(command)

    def __delitem__(self, key):
        old_value = self._value[key]
        command = DelItemCommand(self, key, old_value)
        self._execute_command(command)

    def __len__(self):
        return len(self._value)

    def __contains__(self, key):
        return key in self._value

    def keys(self):
        return self._value.keys()

    def values(self):
        return self._value.values()

    def items(self):
        return self._value.items()


class ReactivableList(Reactivable):
    def __getitem__(self, index):
        return self._value[index]

    def __setitem__(self, index, value):
        old_value = self._value[index]
        wrapped_value = self._wrap_reactive(value)
        command = SetItemCommand(self, index, wrapped_value, old_value)
        self._execute_command(command)

    def __delitem__(self, index):
        old_value = self._value[index]
        command = PopCommand(self, index, old_value)
        self._execute_command(command)

    def __len__(self):
        return len(self._value)

    def __contains__(self, item):
        return item in self._value

    def append(self, value):
        wrapped_value = self._wrap_reactive(value)
        command = AppendCommand(self, wrapped_value)
        self._execute_command(command)

    def insert(self, index, value):
        wrapped_value = self._wrap_reactive(value)
        command = InsertCommand(self, index, wrapped_value)
        self._execute_command(command)

    def pop(self, index=-1):
        old_value = self._value[index]
        command = PopCommand(self, index, old_value)
        self._execute_command(command)
        return old_value


if __name__ == "__main__":
    data = {
        "name": "Alice",
        "age": 30,
        "hobbies": ["reading", "coding"],
        "address": {"city": "Beijing", "zip": "100000"},
    }
    reactivable = ReactivableDict(data)
    print(reactivable)
    print(reactivable["name"])
    print(reactivable["age"])
    reactivable["name"] = "Bob"
    print(reactivable["name"], reactivable._history)
    reactivable.undo()
    print(reactivable)
