# Learnings

## Lint
- `ansible-lint` reports 66 pre-existing violations across all roles (fqcn, risky-file-permissions, yaml[truthy], trailing-spaces, indentation). These are not in scope for verification tasks — note but do not fix unless task explicitly targets lint.
- No `.ansible-lint` config file exists in the repo.

## Naming Inconsistencies
- `requires_bluetooth` variable used in `os_kernel/tasks/main.yml` (line 111) vs `has_bluetooth` used in Section 2 requirements. To be resolved in Task 13.

## Verified Tasks
- Task 01–08: All functional requirements pass. Verification tasks do not require test files — just read the role and compare against spec requirements.
- Task 05 note: REQ-USR-01 is fulfilled by two separate `user` tasks (one sets password, another sets lock/shell/expires) — functionally correct, not a gap.
- Task 06 note: Some ssh.yml regexp patterns only match commented lines (e.g. `'^#PasswordAuthentication(.*)'`). This is pre-existing behavior; not a gap since Debian defaults keep these lines commented.
