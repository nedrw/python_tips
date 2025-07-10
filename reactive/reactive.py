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


class Reactivable:
    __exclude_attr = {
        "_value",
        "_parent",
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

    def __init__(self, value, parent=None):
        self._value = self._wrap_reactive(value)
        self._parent = parent
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
                value[k] = ReactivableList(v, parent=self)
            if isinstance(v, dict):
                value[k] = ReactivableDict(v, parent=self)
        return value

    def __getattribute__(self, item):
        if item in Reactivable.__exclude_attr:
            return object.__getattribute__(self, item)
        return object.__getattribute__(self._value, item)

    def __setattr__(self, key, value):
        if key not in Reactivable.__exclude_attr:
            old_value = object.__getattribute__(self, key)
            if old_value != value:
                self._value = value
                self._record_change(old_value)
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
        # todo
        for observer in self._observers:
            observer(self._value)

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
        del self._value[key]
        self._record_change({key: old_value})
        self.notify()

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
        del self._value[index]
        self._record_change([(index, old_value)])
        self.notify()

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
