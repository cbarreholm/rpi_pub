"""Tests for Task 19: limited users in os_users role."""
import os
import unittest
import yaml


DEFAULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "defaults", "main.yml"
)
TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "main.yml"
)


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


class TestLimitedUsersDefaults(unittest.TestCase):
    def setUp(self):
        self.defaults = load_yaml(DEFAULTS_FILE)

    def test_additional_limited_users_defaults_to_empty_list(self):
        self.assertIn("additional_limited_users", self.defaults)
        self.assertEqual(self.defaults["additional_limited_users"], [])


class TestLimitedUsersTasks(unittest.TestCase):
    def setUp(self):
        self.tasks = load_yaml(TASKS_FILE)

    def _find_tasks(self, predicate):
        return [t for t in self.tasks if t and predicate(t)]

    def test_create_user_accounts_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_limited_users }}"
            and t.get("ansible.builtin.user", {}).get("password_lock") is True
            and t.get("ansible.builtin.user", {}).get("shell") == "{{ item.shell }}"
        )
        self.assertTrue(
            matches,
            "No task creates limited user accounts looping additional_limited_users "
            "with password_lock: true and shell: '{{ item.shell }}'",
        )

    def test_ssh_authorized_key_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_limited_users }}"
            and "ansible.posix.authorized_key" in t
        )
        self.assertTrue(
            matches,
            "No task sets SSH authorized keys looping over additional_limited_users",
        )
        task = matches[0]
        when = task.get("when", "")
        when_str = str(when)
        self.assertIn(
            "item.ssh_public_key is defined",
            when_str,
            "SSH authorized_key task for limited users not conditioned on 'item.ssh_public_key is defined'",
        )

    def test_add_to_ssh_users_group_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_limited_users }}"
            and "ssh-users" in str(t.get("ansible.builtin.user", {}).get("groups", []))
        )
        self.assertTrue(
            matches,
            "No task adds limited users to ssh-users group",
        )
        task = matches[0]
        when = task.get("when", "")
        when_str = str(when)
        self.assertIn(
            "item.ssh_public_key is defined",
            when_str,
            "ssh-users group task for limited users not conditioned on 'item.ssh_public_key is defined'",
        )

    def test_no_limited_user_tasks_reference_privileged_groups(self):
        limited_tasks = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_limited_users }}"
        )
        for task in limited_tasks:
            task_str = str(task)
            for group in ("sudo", "alt-admins"):
                self.assertNotIn(
                    f"'{group}'",
                    task_str,
                    f"Limited user task references privileged group '{group}': {task.get('name')}",
                )
                self.assertNotIn(
                    f'"{group}"',
                    task_str,
                    f"Limited user task references privileged group '{group}': {task.get('name')}",
                )


if __name__ == "__main__":
    unittest.main()
