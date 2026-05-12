"""
Tests for Task 27: Prevent nginx postinst auto-start on IPv6-disabled hosts.

The nginx package's postinst invokes `invoke-rc.d nginx start` immediately
after unpack. The stock `/etc/nginx/sites-enabled/default` listens on
[::]:80, and `os_kernel` blacklists the ipv6 module, so the socket()
call returns EAFNOSUPPORT and dpkg leaves nginx in an `iU` state.
A policy-rc.d shim (exit 101) wrapped around the apt task suppresses the
auto-start; the role's existing "Remove default site" + "Deploy ..." +
"Restart nginx" sequence then brings nginx up with the role's IPv4-only
config.

Verifies that:
- A policy-rc.d copy task exists before the "Install nginx package" task.
- The shim is removed after the apt task.
- Both new tasks are privileged and shaped correctly.

Run with:
    python -m unittest discover -s ansible/roles/http_reverse_proxy/tests \
        -p "test_nginx_install_no_autostart.py" -v
"""
import os
import unittest

import yaml

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "nginx.yml"
)

POLICY_RC_D_PATH = "/usr/sbin/policy-rc.d"
EXPECTED_CONTENT = "#!/bin/sh\nexit 101\n"


def load_tasks():
    with open(TASKS_FILE) as f:
        return yaml.safe_load(f)


def task_index(tasks, predicate):
    for i, task in enumerate(tasks):
        if isinstance(task, dict) and predicate(task):
            return i
    return -1


def get_module(task, *names):
    for name in names:
        if name in task:
            return task[name]
    return None


class TestNginxInstallNoAutostart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks()

        cls.install_idx = task_index(
            cls.tasks,
            lambda t: "install nginx package" in t.get("name", "").lower(),
        )

        def is_policy_copy(task):
            module = get_module(task, "ansible.builtin.copy", "copy")
            if not isinstance(module, dict):
                return False
            return module.get("dest") == POLICY_RC_D_PATH

        def is_policy_remove(task):
            module = get_module(task, "ansible.builtin.file", "file")
            if not isinstance(module, dict):
                return False
            return (
                module.get("path") == POLICY_RC_D_PATH
                and module.get("state") == "absent"
            )

        cls.copy_idx = task_index(cls.tasks, is_policy_copy)
        cls.remove_idx = task_index(cls.tasks, is_policy_remove)

    def test_install_nginx_task_exists(self):
        self.assertGreaterEqual(
            self.install_idx,
            0,
            "Expected the existing 'Install nginx package' task to be "
            "present — Task 27 wraps it but does not remove it.",
        )

    def test_policy_rc_d_copy_task_exists(self):
        self.assertGreaterEqual(
            self.copy_idx,
            0,
            f"Expected a copy task that writes {POLICY_RC_D_PATH}.",
        )

    def test_policy_rc_d_remove_task_exists(self):
        self.assertGreaterEqual(
            self.remove_idx,
            0,
            f"Expected a file task that removes {POLICY_RC_D_PATH} "
            "with state: absent.",
        )

    def test_policy_rc_d_copy_runs_before_apt(self):
        self.assertLess(
            self.copy_idx,
            self.install_idx,
            "policy-rc.d shim must be written BEFORE the apt install task "
            "so invoke-rc.d in nginx postinst sees it.",
        )

    def test_policy_rc_d_remove_runs_after_apt(self):
        self.assertGreater(
            self.remove_idx,
            self.install_idx,
            "policy-rc.d shim must be removed AFTER the apt install task "
            "so the role's later 'Restart nginx' handler is not blocked.",
        )

    def test_policy_rc_d_copy_content_and_mode(self):
        module = get_module(
            self.tasks[self.copy_idx], "ansible.builtin.copy", "copy"
        )
        self.assertEqual(
            module.get("content"),
            EXPECTED_CONTENT,
            "policy-rc.d must be exactly '#!/bin/sh\\nexit 101\\n' so "
            "invoke-rc.d denies the start.",
        )
        self.assertEqual(
            str(module.get("mode")),
            "0755",
            "policy-rc.d must be mode 0755 to be executable by "
            "invoke-rc.d.",
        )

    def test_policy_rc_d_tasks_are_privileged(self):
        self.assertTrue(
            self.tasks[self.copy_idx].get("become") is True,
            "policy-rc.d copy task must run with become: true.",
        )
        self.assertTrue(
            self.tasks[self.remove_idx].get("become") is True,
            "policy-rc.d remove task must run with become: true.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
