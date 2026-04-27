"""
Tests for Task 13: Refactor kernel module blacklisting to per-host variables.

Verifies that:
- Bluetooth blacklist uses has_bluetooth (not requires_bluetooth)
- USB storage blacklist uses has_usb
- FireWire blacklist uses has_firewire
- Wi-Fi power saving uses has_wifi
- Defaults are set to false for all four variables

Run with: python3 ansible/roles/os_kernel/tests/test_kernel_host_vars.py
"""
import unittest
import yaml
import os

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "main.yml"
)
DEFAULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "defaults", "main.yml"
)


def load_tasks():
    with open(TASKS_FILE) as f:
        return yaml.safe_load(f)


def load_defaults():
    with open(DEFAULTS_FILE) as f:
        return yaml.safe_load(f) or {}


def find_task(tasks, name_substr):
    for task in tasks:
        if isinstance(task, dict) and "name" in task:
            if name_substr.lower() in task["name"].lower():
                return task
    return None


def get_when_str(task):
    when = task.get("when")
    if when is None:
        return ""
    if isinstance(when, list):
        return " ".join(str(w) for w in when)
    return str(when)


class TestKernelHostVars(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks()
        cls.defaults = load_defaults()

    def _get_task(self, name_substr):
        task = find_task(self.tasks, name_substr)
        self.assertIsNotNone(task, f"Task containing '{name_substr}' not found")
        return task

    def test_bluetooth_uses_has_bluetooth(self):
        task = self._get_task("Disable Bluetooth")
        when = get_when_str(task)
        self.assertIn("has_bluetooth", when,
                       f"'has_bluetooth' not in when: {when!r}")
        self.assertNotIn("requires_bluetooth", when,
                          f"Old var 'requires_bluetooth' still present in when: {when!r}")

    def test_bluetooth_when_is_negated(self):
        task = self._get_task("Disable Bluetooth")
        when = get_when_str(task)
        self.assertIn("not", when,
                       f"Expected negation in when: {when!r}")

    def test_usb_storage_uses_has_usb(self):
        task = self._get_task("Disable USB Storage")
        when = get_when_str(task)
        self.assertIn("has_usb", when,
                       f"'has_usb' not in when: {when!r}")

    def test_firewire_uses_has_firewire(self):
        task = self._get_task("Disable FireWire")
        when = get_when_str(task)
        self.assertIn("has_firewire", when,
                       f"'has_firewire' not in when: {when!r}")

    def test_wifi_power_saving_uses_has_wifi(self):
        task = self._get_task("Disable Wi-Fi Power Saving (non pi zero w models)")
        when = get_when_str(task)
        self.assertIn("has_wifi", when,
                       f"'has_wifi' not in when: {when!r}")

    def test_defaults_has_bluetooth_is_false(self):
        self.assertIn("has_bluetooth", self.defaults,
                       "has_bluetooth missing from defaults")
        self.assertFalse(self.defaults["has_bluetooth"],
                          "has_bluetooth default should be false")

    def test_defaults_has_usb_is_false(self):
        self.assertIn("has_usb", self.defaults,
                       "has_usb missing from defaults")
        self.assertFalse(self.defaults["has_usb"],
                          "has_usb default should be false")

    def test_defaults_has_firewire_is_false(self):
        self.assertIn("has_firewire", self.defaults,
                       "has_firewire missing from defaults")
        self.assertFalse(self.defaults["has_firewire"],
                          "has_firewire default should be false")

    def test_defaults_has_wifi_is_false(self):
        self.assertIn("has_wifi", self.defaults,
                       "has_wifi missing from defaults")
        self.assertFalse(self.defaults["has_wifi"],
                          "has_wifi default should be false")


if __name__ == "__main__":
    unittest.main(verbosity=2)
