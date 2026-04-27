"""
Tests for Task 15: Implement per-host user management.

Verifies that:
- os_users/defaults/main.yml defines platform_default_user: pi
- os_users/tasks/main.yml uses {{ platform_default_user }} instead of hardcoded 'pi'
- The fail guard uses platform_default_user
- The password task uses platform_default_user
- The lock task uses platform_default_user
- The credentials path uses platform_default_user

Run with: python3 ansible/roles/os_users/tests/test_per_host_user_management.py
"""
import unittest
import yaml
import os

TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "tasks", "main.yml")
DEFAULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "defaults", "main.yml")


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def find_task(tasks, name_substr):
    for task in tasks:
        if isinstance(task, dict) and "name" in task:
            if name_substr.lower() in task["name"].lower():
                return task
    return None


class TestDefaultsHavePlatformDefaultUser(unittest.TestCase):
    def test_platform_default_user_defined(self):
        defaults = load_yaml(DEFAULTS_FILE)
        self.assertIn("platform_default_user", defaults,
                      "platform_default_user not defined in defaults/main.yml")

    def test_platform_default_user_is_pi(self):
        defaults = load_yaml(DEFAULTS_FILE)
        self.assertEqual(defaults.get("platform_default_user"), "pi",
                         "platform_default_user default should be 'pi'")


class TestTasksUsePlatformDefaultUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_yaml(TASKS_FILE)
        with open(TASKS_FILE) as f:
            cls.raw = f.read()

    def _get_task(self, name_substr):
        task = find_task(self.tasks, name_substr)
        self.assertIsNotNone(task, f"Task containing '{name_substr}' not found")
        return task

    def test_no_hardcoded_pi_in_user_name(self):
        """No task should set user name to the literal string 'pi'."""
        for task in self.tasks:
            if not isinstance(task, dict):
                continue
            for key in ("user",):
                if key in task:
                    user_block = task[key]
                    if isinstance(user_block, dict):
                        self.assertNotEqual(
                            user_block.get("name"), "pi",
                            f"Task '{task.get('name')}' has hardcoded name: pi"
                        )

    def test_fail_guard_uses_variable(self):
        task = self._get_task("not allowed to run as")
        when = task.get("when", "")
        self.assertIn("platform_default_user", str(when),
                      f"fail guard 'when' should reference platform_default_user, got: {when!r}")

    def test_fail_guard_no_hardcoded_pi(self):
        task = self._get_task("not allowed to run as")
        when = task.get("when", "")
        self.assertNotIn("== 'pi'", str(when),
                         f"fail guard 'when' still has hardcoded 'pi': {when!r}")

    def test_password_task_uses_variable(self):
        task = self._get_task("auto generated password")
        user_block = task.get("user", {})
        name_val = str(user_block.get("name", ""))
        self.assertIn("platform_default_user", name_val,
                      f"password task user name should use platform_default_user, got: {name_val!r}")

    def test_password_task_credentials_path_uses_variable(self):
        task = self._get_task("auto generated password")
        user_block = task.get("user", {})
        password_val = str(user_block.get("password", ""))
        self.assertIn("platform_default_user", password_val,
                      f"credentials path should use platform_default_user, got: {password_val!r}")

    def test_remove_password_file_uses_variable(self):
        task = self._get_task("remove generated")
        # local_action can be a string or dict
        action = task.get("local_action", "")
        self.assertIn("platform_default_user", str(action),
                      f"remove password file task should use platform_default_user, got: {action!r}")

    def test_disable_user_task_uses_variable(self):
        task = self._get_task("disable")
        user_block = task.get("user", {})
        name_val = str(user_block.get("name", ""))
        self.assertIn("platform_default_user", name_val,
                      f"disable user task name should use platform_default_user, got: {name_val!r}")

    # REQ-PRE-01: playbook refuses to run as the default user
    def test_fail_guard_is_fail_module_task(self):
        fail_tasks = [t for t in self.tasks if isinstance(t, dict) and "fail" in t]
        self.assertTrue(fail_tasks,
                        "No 'fail' module task found — playbook must refuse to run as default user")


if __name__ == "__main__":
    unittest.main(verbosity=2)
