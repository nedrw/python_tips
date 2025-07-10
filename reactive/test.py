import unittest
from .reactive import Reactivable


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


if __name__ == "__main__":
    unittest.main()
