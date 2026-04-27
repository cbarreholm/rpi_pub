# Learnings

## Lint
- `ansible-lint` reports 66 pre-existing violations across all roles (fqcn, risky-file-permissions, yaml[truthy], trailing-spaces, indentation). These are not in scope for verification tasks — note but do not fix unless task explicitly targets lint.
- No `.ansible-lint` config file exists in the repo.

## Naming Inconsistencies
- Task 13 resolved: renamed `requires_bluetooth` → `has_bluetooth` and added `has_usb`, `has_firewire`, `has_wifi` gates to `os_kernel/tasks/main.yml`. Defaults set to `false` in `os_kernel/defaults/main.yml`. Inventory updated accordingly.

## Verified Tasks
- Task 17: Added `# Playbooks` reference table to README.md (before Pre-requirements section) and added `prepGenericHwServer.yml` to AGENTS.md available playbooks list. Documentation-only task, no tests.
- Task 15: Introduced `platform_default_user` variable (default `pi`) in `os_users/defaults/main.yml`. All hardcoded `pi` references in `os_users/tasks/main.yml` replaced with `{{ platform_default_user }}`. `generic_server` group in inventory gets `vars: platform_default_user: debian`. Test at `os_users/tests/test_per_host_user_management.py`.
- Task 01–08: All functional requirements pass. Verification tasks do not require test files — just read the role and compare against spec requirements.
- Task 11: Added `when: inventory_hostname in groups['pi_server']` to 7 RPi-specific tasks in `os_base/tasks/main.yml`. The two `findmnt` tasks already had a `when` for version check — combined as a YAML list. Test written as `tests/test_platform_gates.py` using `unittest` + `pyyaml` (pytest not installed).
- Task 05 note: REQ-USR-01 is fulfilled by two separate `user` tasks (one sets password, another sets lock/shell/expires) — functionally correct, not a gap.
- Task 06 note: Some ssh.yml regexp patterns only match commented lines (e.g. `'^#PasswordAuthentication(.*)'`). This is pre-existing behavior; not a gap since Debian defaults keep these lines commented.
