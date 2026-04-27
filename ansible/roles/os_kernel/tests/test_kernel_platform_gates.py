"""
Tests for Task 14: Gate RPi-specific kernel tasks by platform.

Verifies that:
- Kyber scheduler tasks have pi_server group gate
- Wi-Fi power saving tasks have pi_server group gate
- Wi-Fi modprobe task has both has_wifi and pi_server gates

Run with: python3 ansible/roles/os_kernel/tests/test_kernel_platform_gates.py
"""
import unittest
import yaml
import os

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "main.yml"
)

PI_SERVER_GATE = "inventory_hostname in groups['pi_server']"


def load_tasks():
    with open(TASKS_FILE) as f:
        return yaml.safe_load(f)


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


class TestKernelPlatformGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks()

    def _get_task(self, name_substr):
        task = find_task(self.tasks, name_substr)
        self.assertIsNotNone(task, f"Task containing '{name_substr}' not found")
        return task

    # REQ-KRN-07: Kyber scheduler tasks gated to pi_server

    def test_kyber_cmdline_gated_to_pi_server(self):
        task = self._get_task("Set Kernel Scheduler (Kyber) boot cmdline")
        when = get_when_str(task)
        self.assertIn(PI_SERVER_GATE, when,
                      f"pi_server gate missing from Kyber cmdline task when: {when!r}")

    def test_kyber_runtime_gated_to_pi_server(self):
        task = self._get_task("Set Kernel Scheduler (Kyber) On System Already Running")
        when = get_when_str(task)
        self.assertIn(PI_SERVER_GATE, when,
                      f"pi_server gate missing from Kyber runtime task when: {when!r}")

    def test_kyber_persistent_gated_to_pi_server(self):
        task = self._get_task("Enable Kernel Scheduler (Kyber) on Reboot")
        when = get_when_str(task)
        self.assertIn(PI_SERVER_GATE, when,
                      f"pi_server gate missing from Kyber persistence task when: {when!r}")

    # REQ-KRN-08: Wi-Fi power saving tasks gated to pi_server

    def test_wifi_powersaving_lineinfile_gated_to_pi_server(self):
        task = self._get_task("Disable Wi-Fi Power Savings (pi zero w models)")
        when = get_when_str(task)
        self.assertIn(PI_SERVER_GATE, when,
                      f"pi_server gate missing from Wi-Fi power saving lineinfile when: {when!r}")

    def test_wifi_modprobe_gated_to_pi_server(self):
        task = self._get_task("Disable Wi-Fi Power Saving (non pi zero w models)")
        when = get_when_str(task)
        self.assertIn(PI_SERVER_GATE, when,
                      f"pi_server gate missing from Wi-Fi modprobe task when: {when!r}")

    def test_wifi_modprobe_retains_has_wifi_gate(self):
        task = self._get_task("Disable Wi-Fi Power Saving (non pi zero w models)")
        when = get_when_str(task)
        self.assertIn("has_wifi", when,
                      f"has_wifi gate missing from Wi-Fi modprobe task when: {when!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
