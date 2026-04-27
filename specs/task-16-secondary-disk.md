# Task 16 — Implement Secondary Disk Management

**Type:** Implementation
**Requirements:** §2.6 REQ-DSK-01 – REQ-DSK-05

## Background
Generic Debian hosts may have an optional secondary disk (e.g. `/dev/vdb`) that
needs to be formatted and mounted at a user-defined path. This is not applicable
to RPi hosts (SD card only) so the feature is gated on the presence of
`secondary_disk_device` in host variables.

## Changes required

### 1. Create new task file
File: `ansible/roles/os_base/tasks/secondary_disk.yml`

Tasks in order:

**Skip if not configured (REQ-DSK-05)**
The entire task file is imported with a `when` condition — see step 2.

**Fail if device is missing (REQ-DSK-03)**
```yaml
- name: Verify secondary disk device exists
  ansible.builtin.stat:
    path: "{{ secondary_disk_device }}"
  register: disk_stat

- name: Fail if secondary disk device does not exist
  ansible.builtin.fail:
    msg: "Secondary disk device {{ secondary_disk_device }} is defined but does not exist on this host."
  when: not disk_stat.stat.exists
```

**Detect existing filesystem (REQ-DSK-01 / REQ-DSK-02)**
```yaml
- name: Check for existing filesystem on secondary disk
  ansible.builtin.command: blkid -s TYPE -o value {{ secondary_disk_device }}
  register: disk_fs_type
  changed_when: false
  failed_when: false
```

**Format if unformatted (REQ-DSK-01)**
```yaml
- name: Format secondary disk with ext4 if unformatted
  community.general.filesystem:
    fstype: ext4
    dev: "{{ secondary_disk_device }}"
  when: disk_fs_type.stdout == ""
```

**Mount and persist to fstab (REQ-DSK-01 / REQ-DSK-02 / REQ-DSK-04)**
```yaml
- name: Mount secondary disk and add fstab entry
  ansible.posix.mount:
    path: "{{ secondary_disk_mount_path }}"
    src: "{{ secondary_disk_device }}"
    fstype: ext4
    opts: defaults,noatime
    state: mounted
```

### 2. Import the task file in main.yml
File: `ansible/roles/os_base/tasks/main.yml`

Add at the end:
```yaml
- import_tasks: secondary_disk.yml
  when: secondary_disk_device is defined
  tags: secondary_disk
```

### 3. Add variable defaults
File: `ansible/roles/os_base/defaults/main.yml`

```yaml
secondary_disk_device: ""
secondary_disk_mount_path: ""
```

## Host variable example
In inventory, for a host with a secondary disk:
```yaml
secondary_disk_device: /dev/vdb
secondary_disk_mount_path: /opt
```

## Dependencies
- `community.general` collection (for `filesystem` module)
- `ansible.posix` collection (for `mount` module)

Verify both are available:
```
ansible-galaxy collection list | grep -E 'community.general|ansible.posix'
```

## Notes
- `blkid` requires sudo — the task runs with `become: yes`.
- Mounting with `state: mounted` both mounts immediately and writes the fstab entry.
- Test with `--check` first, then with `--diff` to review fstab changes before applying.
