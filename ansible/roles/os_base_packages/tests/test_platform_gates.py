"""
Tests for Task 12: Gate os_base_packages tasks by platform.

Verifies that RPi-specific packages are only installed on pi_server hosts,
and that common packages are installed on all platforms.

Run with: python3 ansible/roles/os_base_packages/tests/test_platform_gates.py
"""
import unittest
import yaml
import os

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "tasks", "main.yml"
)

PI_SERVER_WHEN = "inventory_hostname in groups['pi_server']"

RPI_ONLY_PACKAGES = [
    "raspberrypi-kernel-headers",
    "dkms",
    "xkbset",
    "ttf-mscorefonts-installer",
]

DEBIAN10_RPI_ONLY_PACKAGES = RPI_ONLY_PACKAGES + ["console-data"]

COMMON_PACKAGES = [
    "dnsutils",
    "screen",
    "vim",
    "git",
    "curl",
    "wget",
    "rsync",
    "iotop",
    "aptitude",
]


def load_tasks():
    with open(TASKS_FILE) as f:
        return yaml.safe_load(f)


def has_pi_server_gate(task):
    when = task.get("when")
    if when is None:
        return False
    if isinstance(when, list):
        return any(PI_SERVER_WHEN in str(w) for w in when)
    return PI_SERVER_WHEN in str(when)


def get_packages_from_task(task):
    packages = []
    # packages may be in vars or directly in the task
    vars_block = task.get("vars", {})
    if "packages" in vars_block:
        packages = vars_block["packages"]
    elif "name" in task.get("apt", {}):
        packages = task["apt"]["name"]
    return packages or []


class TestPlatformGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks()

    def _get_tasks_by_version(self, version):
        """Return all tasks whose 'when' condition checks for the given major version."""
        result = []
        for task in self.tasks:
            if not isinstance(task, dict):
                continue
            when = task.get("when", "")
            when_str = " ".join(str(w) for w in when) if isinstance(when, list) else str(when)
            if f'ansible_distribution_major_version == "{version}"' in when_str:
                result.append(task)
        return result

    def _all_packages_for_version(self, version):
        """Return (common_pkgs, rpi_pkgs) for a given Debian major version."""
        tasks = self._get_tasks_by_version(version)
        common_pkgs = []
        rpi_pkgs = []
        for task in tasks:
            pkgs = get_packages_from_task(task)
            if has_pi_server_gate(task):
                rpi_pkgs.extend(pkgs)
            else:
                common_pkgs.extend(pkgs)
        return common_pkgs, rpi_pkgs

    def test_debian12_rpi_packages_are_gated(self):
        _, rpi_pkgs = self._all_packages_for_version("12")
        for pkg in RPI_ONLY_PACKAGES:
            with self.subTest(package=pkg):
                self.assertIn(pkg, rpi_pkgs, f"RPi package '{pkg}' must be in a pi_server-gated task for Debian 12")

    def test_debian12_rpi_packages_not_in_common(self):
        common_pkgs, _ = self._all_packages_for_version("12")
        for pkg in RPI_ONLY_PACKAGES:
            with self.subTest(package=pkg):
                self.assertNotIn(pkg, common_pkgs, f"RPi package '{pkg}' must NOT be in common (ungated) task for Debian 12")

    def test_debian10_rpi_packages_are_gated(self):
        _, rpi_pkgs = self._all_packages_for_version("10")
        for pkg in DEBIAN10_RPI_ONLY_PACKAGES:
            with self.subTest(package=pkg):
                self.assertIn(pkg, rpi_pkgs, f"RPi package '{pkg}' must be in a pi_server-gated task for Debian 10")

    def test_debian10_rpi_packages_not_in_common(self):
        common_pkgs, _ = self._all_packages_for_version("10")
        for pkg in DEBIAN10_RPI_ONLY_PACKAGES:
            with self.subTest(package=pkg):
                self.assertNotIn(pkg, common_pkgs, f"RPi package '{pkg}' must NOT be in common (ungated) task for Debian 10")

    def test_common_packages_in_debian12_common_task(self):
        common_pkgs, _ = self._all_packages_for_version("12")
        for pkg in COMMON_PACKAGES:
            with self.subTest(package=pkg):
                self.assertIn(pkg, common_pkgs, f"Common package '{pkg}' must be in ungated task for Debian 12")

    def test_common_packages_in_debian10_common_task(self):
        common_pkgs, _ = self._all_packages_for_version("10")
        for pkg in COMMON_PACKAGES:
            with self.subTest(package=pkg):
                self.assertIn(pkg, common_pkgs, f"Common package '{pkg}' must be in ungated task for Debian 10")

    def test_debian13_common_packages_present(self):
        common_pkgs, _ = self._all_packages_for_version("13")
        for pkg in COMMON_PACKAGES:
            with self.subTest(package=pkg):
                self.assertIn(pkg, common_pkgs, f"Common package '{pkg}' must be in ungated task for Debian 13")

    def test_debian13_rpi_packages_gated_to_pi_server(self):
        _, rpi_pkgs = self._all_packages_for_version("13")
        for pkg in ["dkms", "xkbset", "ttf-mscorefonts-installer"]:
            with self.subTest(package=pkg):
                self.assertIn(pkg, rpi_pkgs, f"RPi package '{pkg}' must be in a pi_server-gated task for Debian 13")

    def test_debian13_rpi_packages_not_in_common(self):
        common_pkgs, _ = self._all_packages_for_version("13")
        for pkg in ["dkms", "xkbset", "ttf-mscorefonts-installer"]:
            with self.subTest(package=pkg):
                self.assertNotIn(pkg, common_pkgs, f"RPi package '{pkg}' must NOT be in common task for Debian 13")

    def test_debian13_rpi_uses_dynamic_kernel_headers(self):
        tasks = self._get_tasks_by_version("13")
        rpi_tasks = [t for t in tasks if has_pi_server_gate(t)]
        self.assertTrue(rpi_tasks, "No RPi task found for Debian 13")
        vars_block = rpi_tasks[0].get("vars", {})
        self.assertIn("rpi_kernel_variant", vars_block,
                      "rpi_kernel_variant missing from Debian 13 RPi task vars")
        packages = vars_block.get("packages", [])
        dynamic = [p for p in packages if "linux-headers-" in str(p) and "rpi_kernel_variant" in str(p)]
        self.assertTrue(dynamic, "No dynamic linux-headers-{{ rpi_kernel_variant }} package found in Debian 13 RPi task")

    def test_debian13_rpi_does_not_use_static_raspberrypi_kernel_headers(self):
        _, rpi_pkgs = self._all_packages_for_version("13")
        self.assertNotIn("raspberrypi-kernel-headers", rpi_pkgs,
                         "raspberrypi-kernel-headers must not be used for Debian 13")


if __name__ == "__main__":
    unittest.main(verbosity=2)
