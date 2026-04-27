"""
Tests for Task 16: Implement secondary disk management.

Verifies that:
- secondary_disk.yml exists with required tasks
- main.yml imports secondary_disk.yml with correct when condition
- defaults/main.yml defines the required variables
- blkid task uses become: yes

Run with: python3 ansible/roles/os_base/tests/test_secondary_disk.py
"""
import unittest
import yaml
import os

TASKS_DIR = os.path.join(os.path.dirname(__file__), "..", "tasks")
SECONDARY_DISK_FILE = os.path.join(TASKS_DIR, "secondary_disk.yml")
MAIN_FILE = os.path.join(TASKS_DIR, "main.yml")
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


class TestSecondaryDiskFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_yaml(SECONDARY_DISK_FILE)

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(SECONDARY_DISK_FILE))

    def test_verify_device_exists_task(self):
        task = find_task(self.tasks, "Verify secondary disk device exists")
        self.assertIsNotNone(task, "Task 'Verify secondary disk device exists' not found")
        self.assertIn("ansible.builtin.stat", task)
        self.assertIn("secondary_disk_device", task["ansible.builtin.stat"]["path"])

    def test_fail_if_device_missing_task(self):
        task = find_task(self.tasks, "Fail if secondary disk device does not exist")
        self.assertIsNotNone(task, "Task 'Fail if secondary disk device does not exist' not found")
        when = task.get("when", "")
        self.assertIn("disk_stat.stat.exists", str(when))

    def test_check_filesystem_task(self):
        task = find_task(self.tasks, "Check for existing filesystem")
        self.assertIsNotNone(task, "Task 'Check for existing filesystem' not found")
        cmd = task.get("ansible.builtin.command", "")
        self.assertIn("blkid", str(cmd))
        self.assertTrue(
            task.get("become") or task.get("become") is True,
            "blkid task should have become: yes"
        )

    def test_format_disk_task(self):
        task = find_task(self.tasks, "Format secondary disk")
        self.assertIsNotNone(task, "Task 'Format secondary disk' not found")
        fs = task.get("community.general.filesystem", {})
        self.assertEqual(fs.get("fstype"), "ext4")
        self.assertIn("secondary_disk_device", str(fs.get("dev", "")))
        when = task.get("when", "")
        self.assertIn("disk_fs_type.stdout", str(when))

    def test_mount_task(self):
        task = find_task(self.tasks, "Mount secondary disk")
        self.assertIsNotNone(task, "Task 'Mount secondary disk' not found")
        mount = task.get("ansible.posix.mount", {})
        self.assertIn("secondary_disk_mount_path", str(mount.get("path", "")))
        self.assertIn("secondary_disk_device", str(mount.get("src", "")))
        self.assertEqual(mount.get("fstype"), "ext4")
        self.assertIn("noatime", str(mount.get("opts", "")))
        self.assertEqual(mount.get("state"), "mounted")


class TestMainYmlImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_yaml(MAIN_FILE)

    def test_imports_secondary_disk(self):
        import_task = None
        for task in self.tasks:
            if isinstance(task, dict):
                val = task.get("import_tasks", "")
                if "secondary_disk" in str(val):
                    import_task = task
                    break
        self.assertIsNotNone(import_task, "main.yml does not import secondary_disk.yml")

    def test_import_has_when_condition(self):
        for task in self.tasks:
            if isinstance(task, dict) and "secondary_disk" in str(task.get("import_tasks", "")):
                when = task.get("when", "")
                self.assertIn(
                    "secondary_disk_device",
                    str(when),
                    "Import of secondary_disk.yml missing 'secondary_disk_device is defined' when condition"
                )
                return
        self.fail("Import of secondary_disk.yml not found in main.yml")

    def test_import_has_tag(self):
        for task in self.tasks:
            if isinstance(task, dict) and "secondary_disk" in str(task.get("import_tasks", "")):
                tags = task.get("tags", "")
                self.assertIn("secondary_disk", str(tags))
                return
        self.fail("Import of secondary_disk.yml not found in main.yml")


class TestDefaults(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load_yaml(DEFAULTS_FILE) or {}

    def test_secondary_disk_device_default(self):
        self.assertIn(
            "secondary_disk_device",
            self.defaults,
            "secondary_disk_device not in defaults/main.yml"
        )

    def test_secondary_disk_mount_path_default(self):
        self.assertIn(
            "secondary_disk_mount_path",
            self.defaults,
            "secondary_disk_mount_path not in defaults/main.yml"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
