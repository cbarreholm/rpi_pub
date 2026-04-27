# Task 01 — Verify Pre-conditions

**Type:** Verification
**Requirements:** §1.1 REQ-PRE-01, REQ-PRE-02

## What to verify

### REQ-PRE-01 — Playbook refuses to run as `pi` user
File: `ansible/roles/os_users/tasks/main.yml`

- Confirm a `fail` task is present that triggers `when: ansible_user_id == 'pi'`.
- Confirm the failure message is meaningful.

### REQ-PRE-02 — SSH key authentication required before run
File: `README.md`

- Confirm the README documents that passwordless SSH key authentication must be
  configured for the connecting user before running the playbook.
- Confirm `ssh-copy-id` or equivalent is mentioned in the pre-requirements section.

## Pass criteria
Both checks pass with no code changes required.
Any gap must be noted and a follow-up task created.
