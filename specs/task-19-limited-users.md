# Task 19 — Implement Limited Users

**Type:** Implementation
**Requirements:** §3.2 REQ-LUSR-01 – REQ-LUSR-08

## Background

Some server roles benefit from a dedicated user account with tightly restricted
permissions — for example, a `git` user whose shell is `/usr/bin/git-shell` so that
SSH access can only be used to push/pull repositories, not to execute arbitrary
commands. This task extends `os_users` to provision any number of such limited users
from a configurable list, with optional SSH key access per user.

## Changes required

### 1. Add defaults
File: `ansible/roles/os_users/defaults/main.yml`

Add:
```yaml
additional_limited_users: []
```

Each entry in the list is a mapping with:
- `name` (string, required) — the username
- `shell` (string, required) — the login shell (e.g. `/usr/bin/git-shell`, `/bin/rbash`)
- `ssh_public_key` (string, optional) — the full public key line; omit to deny SSH login

### 2. Add tasks for limited users
File: `ansible/roles/os_users/tasks/main.yml`

Append the following logical blocks. All blocks are guarded by
`when: additional_limited_users | length > 0` where appropriate.

**a) Create each limited user account**

Each user shall be created with:
- the specified `shell`
- a locked password (`password_lock: true`)
- home directory created
- no supplementary groups beyond the user's own primary group

```yaml
- name: Create limited user accounts
  become: true
  ansible.builtin.user:
    name: "{{ item.name }}"
    shell: "{{ item.shell }}"
    create_home: true
    password_lock: true
  loop: "{{ additional_limited_users }}"
  tags: users
```

**b) Configure SSH authorized key for limited users that have one**

Only runs for entries where `ssh_public_key` is defined:

```yaml
- name: Configure SSH authorized key for limited users
  become: true
  ansible.posix.authorized_key:
    user: "{{ item.name }}"
    key: "{{ item.ssh_public_key }}"
    state: present
    exclusive: false
  loop: "{{ additional_limited_users }}"
  when: item.ssh_public_key is defined
  tags: users
```

**c) Add limited users with an SSH key to `ssh-users` group**

Only users with `ssh_public_key` defined are added to `ssh-users`, so that SSH access
is permitted for them but blocked for users without a key.

```yaml
- name: Add limited users with SSH key to ssh-users group
  become: true
  ansible.builtin.user:
    name: "{{ item.name }}"
    groups:
      - ssh-users
    append: true
  loop: "{{ additional_limited_users }}"
  when: item.ssh_public_key is defined
  tags: users
```

### 3. Document variables
File: `ansible/roles/os_users/defaults/main.yml` (inline comments)

Document the `additional_limited_users` list variable and its expected fields,
including that `ssh_public_key` is optional.

## Tests
File: `ansible/roles/os_users/tests/test_limited_users.py`

Tests must verify (by parsing YAML, not running Ansible):

- `additional_limited_users` defaults to `[]` in `defaults/main.yml`
- A task exists that creates user accounts by looping over `additional_limited_users`
  with `password_lock: true` and `shell: "{{ item.shell }}"`
- A task exists that sets SSH authorized keys by looping over
  `additional_limited_users` and is conditioned on `item.ssh_public_key is defined`
- A task exists that adds users to `ssh-users` by looping over
  `additional_limited_users` and is conditioned on `item.ssh_public_key is defined`
- None of the new tasks add limited users to `sudo`, `alt-admins`, or any other
  privileged group

## Notes
- The `git-shell` use case requires `git` to be installed on the host. Ensure
  `git` is present in the base packages role (it already is per REQ-PKG-01).
- `/usr/bin/git-shell` must be listed in `/etc/shells` on the target host for SSH
  to permit it as a login shell. A follow-up task or a note in the variable
  documentation should highlight this dependency; the operator must ensure it is
  present (Debian ships git-shell in `/etc/shells` automatically when `git` is
  installed via the `git` package).
- Limited users intentionally have no sudo access and are not in `alt-admins`.
  This must be enforced by omission — the tasks must not reference those groups.
