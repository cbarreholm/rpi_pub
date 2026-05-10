# Learnings

## Running Tests
- `pytest` is NOT installed. Always run tests with: `python -m unittest discover -s <test-dir> -p "<test-file>.py" -v`
- Example: `python -m unittest discover -s ansible/roles/os_users/tests -p "test_limited_users.py" -v`
- Running `python -m unittest ansible/roles/os_users/tests/test_foo.py` fails because Python treats the path as a dotted module name and tries to import `ansible.roles...`.
- Running `python -m pytest ...` fails because pytest is not installed.

## Lint
- `ansible-lint` reports 66 pre-existing violations across all roles (fqcn, risky-file-permissions, yaml[truthy], trailing-spaces, indentation). These are not in scope for verification tasks — note but do not fix unless task explicitly targets lint.
- No `.ansible-lint` config file exists in the repo.

## Naming Inconsistencies
- Task 13 resolved: renamed `requires_bluetooth` → `has_bluetooth` and added `has_usb`, `has_firewire`, `has_wifi` gates to `os_kernel/tasks/main.yml`. Defaults set to `false` in `os_kernel/defaults/main.yml`. Inventory updated accordingly.

## Verified Tasks
- Task 16: Added `os_base/tasks/secondary_disk.yml` with stat/fail/blkid/filesystem/mount tasks. Imported in `main.yml` with `when: secondary_disk_device is defined and secondary_disk_device != ""`. Defaults added to `os_base/defaults/main.yml`. All privileged tasks (blkid, filesystem, mount) require `become: true`. Spec-defined register names (`disk_stat`, `disk_fs_type`) conflict with `var-naming[no-role-prefix]` lint rule — left as-is (same as pre-existing violations). Test at `os_base/tests/test_secondary_disk.py`.
- Task 19: Added `additional_limited_users` list to `os_users`. Default `[]` in `defaults/main.yml`. Each entry requires `name` and `shell`; `ssh_public_key` is optional. Tasks: create accounts with `password_lock: true` and `shell: "{{ item.shell }}"` (guarded by list length > 0), set authorized keys and add to `ssh-users` (both guarded by list length > 0 AND `item.ssh_public_key is defined`). No privileged groups. Example added to `inventory.yaml.example`. Test at `os_users/tests/test_limited_users.py`.
- Task 18: Added `additional_admin_users` list to `os_users`. Default `[]` in `defaults/main.yml`. Real values (usernames + SSH keys) belong in `ansible/secrets/secrets_file.enc` (vault-encrypted) — not in inventory/host_vars — to avoid intel leakage. Tasks: create `alt-admins` group, write `/etc/sudoers.d/099_alt-admins-nopasswd` (mode 0440, validate via visudo), create accounts with `password_lock: true`, set authorized keys via `ansible.posix.authorized_key`, add to both `alt-admins` and `ssh-users`. All 5 new task blocks guarded by `additional_admin_users | length > 0`. `var-naming[no-role-prefix]` lint warning on `additional_admin_users` is pre-existing pattern (same as `platform_default_user`). Test at `os_users/tests/test_additional_admin_users.py`.
- Task 17: Added `# Playbooks` reference table to README.md (before Pre-requirements section) and added `prepGenericHwServer.yml` to AGENTS.md available playbooks list. Documentation-only task, no tests.
- Task 15: Introduced `platform_default_user` variable (default `pi`) in `os_users/defaults/main.yml`. All hardcoded `pi` references in `os_users/tasks/main.yml` replaced with `{{ platform_default_user }}`. `generic_server` group in inventory gets `vars: platform_default_user: debian`. Test at `os_users/tests/test_per_host_user_management.py`.
- Task 01–08: All functional requirements pass. Verification tasks do not require test files — just read the role and compare against spec requirements.
- Task 11: Added `when: inventory_hostname in groups['pi_server']` to 7 RPi-specific tasks in `os_base/tasks/main.yml`. The two `findmnt` tasks already had a `when` for version check — combined as a YAML list. Test written as `tests/test_platform_gates.py` using `unittest` + `pyyaml` (pytest not installed).
- Task 05 note: REQ-USR-01 is fulfilled by two separate `user` tasks (one sets password, another sets lock/shell/expires) — functionally correct, not a gap.
- Task 06 note: Some ssh.yml regexp patterns only match commented lines (e.g. `'^#PasswordAuthentication(.*)'`). This is pre-existing behavior; not a gap since Debian defaults keep these lines commented.
