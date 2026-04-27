# Task 05 — Verify User Management

**Type:** Verification
**Requirements:** §1.5 REQ-USR-01 – REQ-USR-04

## What to verify

File: `ansible/roles/os_users/tasks/main.yml`

### REQ-USR-01 — pi user gets random password and is locked
Confirm a `user` task:
- Targets the `pi` user
- Sets a randomly generated password using `lookup('password', ...)`
- Sets `password_lock: true`
- Sets `shell: /sbin/nologin`
- Sets `expires: 1.0`

### REQ-USR-02 — Generated password file deleted from controller
Confirm a `local_action` (or `delegate_to: localhost`) task removes
`credentials/pi/password.txt` after applying the password.

### REQ-USR-03 — ssh-users group created
Confirm a `group` task creates the `ssh-users` group.

### REQ-USR-04 — Connecting user added to ssh-users
Confirm a `user` task appends the connecting user (`ansible_user_id`) to the
`ssh-users` group.

## Pass criteria
All checks pass with no code changes required.
Any gap must be noted and a follow-up task created.
