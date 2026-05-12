"""
Tests for Task 25: Drop IPv6 sysctl entries (resolve modprobe/sysctl collision).

Verifies that:
- The rendered content of /etc/sysctl.d/10-harden_sysctl.conf contains
  no net.ipv6.* keys (the modprobe blacklist is the single source of truth).
- IPv4 hardening keys are still present.
- The modprobe task that writes /etc/modprobe.d/ipv6.conf with
  "blacklist ipv6" is still present (regression guard for REQ-KRN-02).

Run with:
    python -m unittest discover -s ansible/roles/os_kernel/tests \
        -p "test_ipv6_sysctl_removal.py" -v
"""
import os
import unittest

import yaml

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "main.yml"
)

IPV4_REQUIRED_KEYS = [
    "net.ipv4.conf.all.accept_redirects",
    "net.ipv4.conf.all.accept_source_route",
    "net.ipv4.conf.all.log_martians",
    "net.ipv4.conf.all.rp_filter",
    "net.ipv4.conf.all.secure_redirects",
    "net.ipv4.conf.all.send_redirects",
    "net.ipv4.conf.default.accept_redirects",
    "net.ipv4.conf.default.accept_source_route",
    "net.ipv4.conf.default.log_martians",
    "net.ipv4.conf.default.rp_filter",
    "net.ipv4.conf.default.secure_redirects",
    "net.ipv4.conf.default.send_redirects",
    "net.ipv4.icmp_echo_ignore_broadcasts",
    "net.ipv4.icmp_ignore_bogus_error_responses",
    "net.ipv4.ip_forward",
    "net.ipv4.tcp_syncookies",
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


def get_copy_content(task):
    copy_module = task.get("ansible.builtin.copy") or task.get("copy") or {}
    return copy_module.get("content", "")


class TestIpv6SysctlRemoval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks()
        cls.sysctl_task = find_task(
            cls.tasks, "Ensure Kernel Hardening via Sysctl is present"
        )
        cls.sysctl_content = (
            get_copy_content(cls.sysctl_task) if cls.sysctl_task else ""
        )

    def test_sysctl_hardening_task_exists(self):
        self.assertIsNotNone(
            self.sysctl_task,
            "Expected 'Ensure Kernel Hardening via Sysctl is present' task",
        )

    def test_sysctl_writes_expected_destination(self):
        copy_module = (
            self.sysctl_task.get("ansible.builtin.copy")
            or self.sysctl_task.get("copy")
            or {}
        )
        self.assertEqual(
            copy_module.get("dest"),
            "/etc/sysctl.d/10-harden_sysctl.conf",
        )

    def test_sysctl_content_has_no_ipv6_keys(self):
        # The modprobe blacklist disables IPv6; once the module is unloaded,
        # /proc/sys/net/ipv6/* disappears and these keys fail to apply.
        self.assertNotIn(
            "net.ipv6",
            self.sysctl_content,
            "sysctl content must contain no net.ipv6.* keys; "
            "modprobe blacklist is the single source of truth for IPv6.",
        )

    def test_sysctl_content_no_disable_ipv6(self):
        self.assertNotIn(
            "disable_ipv6",
            self.sysctl_content,
            "sysctl content must not contain disable_ipv6 entries.",
        )

    def test_sysctl_content_no_ipv6_section_headers(self):
        for header in ("## IPV6 Networking", "## IPV6 Disabled"):
            self.assertNotIn(
                header,
                self.sysctl_content,
                f"Stale IPv6 section header still present: {header!r}",
            )

    def test_sysctl_content_keeps_ipv4_hardening(self):
        for key in IPV4_REQUIRED_KEYS:
            self.assertIn(
                key,
                self.sysctl_content,
                f"IPv4 hardening key missing from sysctl content: {key}",
            )

    def test_sysctl_content_keeps_kernel_hardening(self):
        self.assertIn("fs.suid_dumpable = 0", self.sysctl_content)
        self.assertIn("kernel.randomize_va_space = 2", self.sysctl_content)

    def test_ipv6_modprobe_blacklist_task_still_present(self):
        task = find_task(self.tasks, "Disable IPV6")
        self.assertIsNotNone(
            task,
            "Expected modprobe task 'Disable IPV6' to still exist "
            "(REQ-KRN-02 regression guard).",
        )
        copy_module = (
            task.get("ansible.builtin.copy") or task.get("copy") or {}
        )
        self.assertEqual(
            copy_module.get("dest"), "/etc/modprobe.d/ipv6.conf"
        )
        self.assertIn("blacklist ipv6", copy_module.get("content", ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
