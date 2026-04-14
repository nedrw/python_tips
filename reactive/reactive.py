from abc import ABC, abstractmethod
from typing import Protocol


class ChangeHistory(Protocol):
    def notify(self) -> None: ...

    def switch(self, value: bool) -> None: ...


class BatchUpdate:
    def __init__(self, data: ChangeHistory):
        self._data = data

    def __enter__(self):
        self._data.switch(True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._data.switch(False)
        self._data.notify()


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


class Reactivable:
    __exclude_attr = {
        "_value",
        "_parent",
        "_key",
        "_controller",
        "_observers",
        "_history",
        "_redo",
        "_batching",
        "_batch_record",
        "_wrap_reactive",
        "_record_change",
        "notify",
        "subscribe",
        "undo",
        "redo",
        "switch",
        "batch_update",
    }

    def __init__(self, value, parent=None, key=None):
        self._value = self._wrap_reactive(value)
        self._parent = parent
        self._key = key
        self._controller = None
        self._observers = set()
        self._history = []
        self._redo = []
        self._batching = False
        self._batch_record = None

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
                    self._value[key] = value
                    self._record_change(old_value)
                    if not self._batching:
                        self.notify()
            else:
                # 属性不存在（新增属性），设置值
                self._value[key] = value
                self._record_change(None)
                if not self._batching:
                    self.notify()
        else:
            object.__setattr__(self, key, value)

    def __str__(self):
        return str(self._value)

    def _record_change(self, old_value):
        if self._batching:
            return
        self._history.append((old_value, self._value))
        self._redo.clear()

    def undo(self):
        # todo
        if self._history:
            old_value, new_value = self._history.pop()
            self._value = old_value
            self._redo.append(new_value)
            self.notify()

    def redo(self):
        # todo
        if self._redo:
            new_value = self._redo.pop()
            self._history.append((self._value, new_value))
            self._value = new_value
            self.notify()

    def notify(self):
        # 通知自己的观察者
        for observer in self._observers:
            observer(self._value)

        # 如果绑定了控件，直接通知控件
        if self._controller is not None:
            if hasattr(self._controller, "update"):
                self._controller.update(self)
        else:
            # 没有绑定控件，通知父对象（变更冒泡）
            if self._parent is not None:
                self._parent.notify()

    def subscribe(self, callback):
        self._observers.add(callback)

    def switch(self, value: bool):
        self._batching = value
        if value:
            self._batch_record = self._value
        elif self._batch_record:
            self._record_change(self._batch_record)
            self._batch_record = None

    def batch_update(self):
        return BatchUpdate(self)


class ReactivableDict(Reactivable):
    def __getitem__(self, key):
        return self._value[key]

    def __setitem__(self, key, value):
        old_value = self._value.get(key)
        self._value[key] = self._wrap_reactive(value)
        self._record_change({key: old_value})
        self.notify()

    def __delitem__(self, key):
        old_value = self._value.pop(key)
        self._record_change({key: old_value})
        self.notify()

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
        self._value[index] = self._wrap_reactive(value)
        self._record_change([(index, old_value)])
        self.notify()

    def __delitem__(self, index):
        old_value = self._value.pop(index)
        self._record_change([(index, old_value)])
        self.notify()

    def __len__(self):
        return len(self._value)

    def __contains__(self, item):
        return item in self._value

    def append(self, value):
        self._value.append(self._wrap_reactive(value))
        self._record_change([(len(self._value) - 1, None)])
        self.notify()

    def insert(self, index, value):
        self._value.insert(index, self._wrap_reactive(value))
        self._record_change([(index, None)])
        self.notify()

    def pop(self, index=-1):
        old_value = self._value.pop(index)
        self._record_change([(index, old_value)])
        self.notify()
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
