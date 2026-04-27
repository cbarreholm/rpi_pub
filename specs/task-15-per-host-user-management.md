# Task 15 — Implement Per-host User Management

**Type:** Implementation
**Requirements:** §2.2 REQ-USR-01, REQ-USR-02

## Background
The current `os_users` role hardcodes the `pi` user as the default system user to
disable. On generic Debian hosts the default user is typically `debian` (or another
provider-specific user). Both the initial connection user and the user to be locked
must be configurable per host.

## Changes required

### 1. Introduce platform_default_user variable
File: `ansible/roles/os_users/defaults/main.yml` (create if absent)

```yaml
platform_default_user: pi
```

This variable holds the name of the default OS user that should be locked after
the alternative user has been set up.

### 2. Update os_users tasks to use the variable
File: `ansible/roles/os_users/tasks/main.yml`

Replace all hardcoded references to `pi` with `{{ platform_default_user }}`:
- The `fail` guard: `when: ansible_user_id == platform_default_user`
- The `user` task that sets the random password: `name: "{{ platform_default_user }}"`
- The `user` task that locks the account: `name: "{{ platform_default_user }}"`
- The `local_action` that removes the password file: update path to use the variable,
  e.g. `credentials/{{ platform_default_user }}/password.txt`

### 3. Set per-host values in inventory
File: `ansible/inventory.yaml`

For `pi_server` hosts: `platform_default_user: pi` (or rely on the default)
For `generic_server` hosts: `platform_default_user: debian`

### 4. ansible_user is already per-host
`ansible_user` is a built-in Ansible variable and is set per host in the inventory.
Confirm it is set correctly for each host group — no role changes needed for this.

## Notes
- The credentials directory path (`credentials/<user>/password.txt`) should also
  use the variable so each platform stores its generated credential separately.
- After locking, verify the locked user cannot authenticate via SSH.
