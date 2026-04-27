"""
Tests for Task 11: Gate os_base tasks by platform.

Verifies that RPi-specific tasks have `when: inventory_hostname in groups['pi_server']`
and that generic tasks do not.

Run with: python3 ansible/roles/os_base/tests/test_platform_gates.py
"""
import unittest
import yaml
import os

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "main.yml"
)

PI_SERVER_WHEN = "inventory_hostname in groups['pi_server']"

PI_ONLY_TASK_NAMES = [
    "Select raspbian mirror",
    "Select raspbian security mirror",
    "obtain system PARTUUID for /boot",
    "obtain system PARTUUID for /boot/firmware",
    "Setup fstab file",
    "Set Swap File Size",
    "Update /etc/hosts",
]

GENERIC_TASK_NAMES = [
    "Set timezone",
    "Ensure localisation files for system locale",
    "Ensure localisation files for system language",
    "Get current locale",
    "Parse 'LANG'",
    "Parse 'LANGUAGE'",
    "Configure locale",
    "Set Keyboard Layout",
    "Fixup APT Configs",
    "Fixup APT Cache",
    "Set hostname",
]


def load_tasks():
    with open(TASKS_FILE) as f:
        return yaml.safe_load(f)


def find_task(tasks, name_substr):
    for task in tasks:
        if isinstance(task, dict) and "name" in task:
            if name_substr.lower() in task["name"].lower():
                return task
    return None


def has_pi_server_gate(task):
    when = task.get("when")
    if when is None:
        return False
    if isinstance(when, list):
        return any(PI_SERVER_WHEN in str(w) for w in when)
    return PI_SERVER_WHEN in str(when)


class TestPlatformGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks()

    def _get_task(self, name_substr):
        task = find_task(self.tasks, name_substr)
        self.assertIsNotNone(task, f"Task containing '{name_substr}' not found")
        return task

    def test_pi_only_tasks_are_gated(self):
        for name_substr in PI_ONLY_TASK_NAMES:
            with self.subTest(task=name_substr):
                task = self._get_task(name_substr)
                self.assertTrue(
                    has_pi_server_gate(task),
                    f"Task '{task['name']}' missing pi_server gate; when={task.get('when')!r}",
                )

    def test_generic_tasks_are_not_gated(self):
        for name_substr in GENERIC_TASK_NAMES:
            with self.subTest(task=name_substr):
                task = self._get_task(name_substr)
                self.assertFalse(
                    has_pi_server_gate(task),
                    f"Task '{task['name']}' should not have pi_server gate",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
