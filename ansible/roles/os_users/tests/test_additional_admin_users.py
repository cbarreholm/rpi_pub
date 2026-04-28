"""Tests for Task 18: additional admin users in os_users role."""
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


def load_tasks(path):
    with open(path) as f:
        return yaml.safe_load(f)


class TestAdditionalAdminUsersDefaults(unittest.TestCase):
    def setUp(self):
        self.defaults = load_yaml(DEFAULTS_FILE)

    def test_additional_admin_users_defaults_to_empty_list(self):
        self.assertIn("additional_admin_users", self.defaults)
        self.assertEqual(self.defaults["additional_admin_users"], [])


class TestAdditionalAdminUsersTasks(unittest.TestCase):
    def setUp(self):
        self.tasks = load_tasks(TASKS_FILE)

    def _find_tasks(self, predicate):
        return [t for t in self.tasks if t and predicate(t)]

    def _guard_present(self, task):
        when = task.get("when", "")
        if isinstance(when, list):
            return any("additional_admin_users | length > 0" in str(w) for w in when)
        return "additional_admin_users | length > 0" in str(when)

    def test_create_alt_admins_group_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("ansible.builtin.group", {}).get("name") == "alt-admins"
        )
        self.assertTrue(matches, "No task creates the alt-admins group")
        self.assertTrue(
            self._guard_present(matches[0]),
            "alt-admins group task not guarded by 'additional_admin_users | length > 0'",
        )

    def test_sudoers_file_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("ansible.builtin.copy", {}).get("dest")
            == "/etc/sudoers.d/099_alt-admins-nopasswd"
        )
        self.assertTrue(matches, "No task writes /etc/sudoers.d/099_alt-admins-nopasswd")
        task = matches[0]
        copy_params = task["ansible.builtin.copy"]
        self.assertIn(
            "%alt-admins ALL=(ALL) NOPASSWD: ALL",
            copy_params.get("content", ""),
        )
        self.assertEqual(copy_params.get("mode"), "0440")
        self.assertEqual(copy_params.get("owner"), "root")
        self.assertEqual(copy_params.get("group"), "root")
        self.assertEqual(copy_params.get("validate"), "/usr/sbin/visudo -cf %s")
        self.assertTrue(
            self._guard_present(task),
            "sudoers task not guarded by 'additional_admin_users | length > 0'",
        )

    def test_create_user_accounts_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_admin_users }}"
            and t.get("ansible.builtin.user", {}).get("password_lock") is True
            and "name" not in t.get("ansible.builtin.user", {})  # uses item.name
        )
        # Broaden: any user task looping additional_admin_users with password_lock: true
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_admin_users }}"
            and t.get("ansible.builtin.user", {}).get("password_lock") is True
        )
        self.assertTrue(
            matches,
            "No task creates user accounts looping additional_admin_users with password_lock: true",
        )

    def test_ssh_authorized_key_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_admin_users }}"
            and "ansible.posix.authorized_key" in t
        )
        self.assertTrue(
            matches,
            "No task sets SSH authorized keys looping over additional_admin_users",
        )

    def test_add_users_to_groups_task_exists(self):
        matches = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_admin_users }}"
            and "alt-admins" in str(t.get("ansible.builtin.user", {}).get("groups", []))
            and "ssh-users" in str(t.get("ansible.builtin.user", {}).get("groups", []))
        )
        self.assertTrue(
            matches,
            "No task adds users to alt-admins and ssh-users groups",
        )

    def test_no_new_tasks_reference_sudo_group(self):
        new_tasks = self._find_tasks(
            lambda t: t.get("loop") == "{{ additional_admin_users }}"
            or t.get("ansible.builtin.group", {}).get("name") == "alt-admins"
            or t.get("ansible.builtin.copy", {}).get("dest")
            == "/etc/sudoers.d/099_alt-admins-nopasswd"
        )
        for task in new_tasks:
            task_str = str(task)
            self.assertNotIn(
                "'sudo'",
                task_str,
                f"Task references 'sudo' group: {task.get('name')}",
            )
            self.assertNotIn(
                '"sudo"',
                task_str,
                f"Task references 'sudo' group: {task.get('name')}",
            )


if __name__ == "__main__":
    unittest.main()
