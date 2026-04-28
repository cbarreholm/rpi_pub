# Task 18 — Implement Additional Admin Users

**Type:** Implementation
**Requirements:** §3.1 REQ-AUSR-01 – REQ-AUSR-09

## Background

The `os_users` role currently manages only the primary admin (the Ansible connecting
user) and the platform default user (e.g. `pi`). There is no mechanism to provision
additional admin users via Ansible. Operationally this is done by hand with
`createAltUser.sh`, which creates a user, copies an SSH authorized key, locks the
password, and drops a per-user sudoers file granting `NOPASSWD: ALL`.

This task automates the same outcome for a configurable list of additional admin users,
using a shared `alt-admins` group rather than per-user sudoers files.

## Changes required

### 1. Add defaults
File: `ansible/roles/os_users/defaults/main.yml`

Add:
```yaml
additional_admin_users: []
```

Each entry in the list is a mapping with:
- `name` (string, required) — the username
- `ssh_public_key` (string, required) — the full public key line

### 2. Add tasks for additional admin users
File: `ansible/roles/os_users/tasks/main.yml`

Append the following logical blocks (all guarded by
`when: additional_admin_users | length > 0`):

**a) Create the `alt-admins` group**
```yaml
- name: Create alt-admins group
  become: true
  ansible.builtin.group:
    name: alt-admins
    state: present
  when: additional_admin_users | length > 0
  tags: users
```

**b) Create the sudoers drop-in for the group**

File: `/etc/sudoers.d/099_alt-admins-nopasswd`
Content: `%alt-admins ALL=(ALL) NOPASSWD: ALL`
Owner: `root:root`, mode: `0440`

```yaml
- name: Configure passwordless sudo for alt-admins group
  become: true
  ansible.builtin.copy:
    dest: /etc/sudoers.d/099_alt-admins-nopasswd
    content: "%alt-admins ALL=(ALL) NOPASSWD: ALL\n"
    owner: root
    group: root
    mode: "0440"
    validate: /usr/sbin/visudo -cf %s
  when: additional_admin_users | length > 0
  tags: users
```

**c) Create each additional admin user account**

Iterate over `additional_admin_users`. Each user shall be created with:
- a locked password (`password_lock: true`)
- shell `/bin/bash`
- home directory created

```yaml
- name: Create additional admin user accounts
  become: true
  ansible.builtin.user:
    name: "{{ item.name }}"
    shell: /bin/bash
    create_home: true
    password_lock: true
  loop: "{{ additional_admin_users }}"
  tags: users
```

**d) Configure SSH authorized key for each additional admin user**

```yaml
- name: Configure SSH authorized key for additional admin users
  become: true
  ansible.posix.authorized_key:
    user: "{{ item.name }}"
    key: "{{ item.ssh_public_key }}"
    state: present
    exclusive: false
  loop: "{{ additional_admin_users }}"
  tags: users
```

**e) Add each additional admin user to `alt-admins` and `ssh-users` groups**

```yaml
- name: Add additional admin users to alt-admins and ssh-users groups
  become: true
  ansible.builtin.user:
    name: "{{ item.name }}"
    groups:
      - alt-admins
      - ssh-users
    append: true
  loop: "{{ additional_admin_users }}"
  tags: users
```

### 3. Document variables
File: `ansible/roles/os_users/vars/main.yml` (or inline comments in defaults)

Document the `additional_admin_users` list variable and its expected fields.

## Tests
File: `ansible/roles/os_users/tests/test_additional_admin_users.py`

Tests must verify (by parsing YAML, not running Ansible):

- `additional_admin_users` defaults to `[]` in `defaults/main.yml`
- A task exists that creates the `alt-admins` group, guarded by
  `additional_admin_users | length > 0`
- A task exists that writes `/etc/sudoers.d/099_alt-admins-nopasswd` with content
  `%alt-admins ALL=(ALL) NOPASSWD: ALL`, mode `0440`, owner `root`, group `root`,
  and uses `validate: /usr/sbin/visudo -cf %s`
- A task exists that creates user accounts by looping over `additional_admin_users`
  with `password_lock: true`
- A task exists that sets SSH authorized keys by looping over `additional_admin_users`
- A task exists that adds users to `alt-admins` and `ssh-users` groups by looping
  over `additional_admin_users`
- None of the new tasks reference the `sudo` group

## Notes
- Using a group-level sudoers file instead of per-user files (as `createAltUser.sh`
  does) is cleaner and avoids accumulating stale files if users are removed.
- The `validate` parameter on the sudoers copy task prevents a broken sudoers file
  from locking out all sudo access.
- `ansible.posix.authorized_key` requires the `ansible.posix` collection (already
  used elsewhere in the project — confirm before implementing).
