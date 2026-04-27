# Implementation Plan

Tasks 01–08 are verification tasks for the existing Raspberry Pi baseline (Section 1).
Tasks 09–17 are implementation tasks for Generic Debian Platform Support (Section 2).

| Task | Description | Spec | Requirements |
|------|-------------|------|--------------|
| [x] 01 | Verify pre-conditions | [task-01-verify-preconditions.md](../specs/task-01-verify-preconditions.md) | §1.1 REQ-PRE-01, REQ-PRE-02 |
| [x] 02 | Verify OS base configuration | [task-02-verify-os-base.md](../specs/task-02-verify-os-base.md) | §1.2 REQ-BASE-01 – REQ-BASE-14 |
| [x] 03 | Verify OS base packages | [task-03-verify-os-base-packages.md](../specs/task-03-verify-os-base-packages.md) | §1.3 REQ-PKG-01 |
| [x] 04 | Verify kernel hardening | [task-04-verify-kernel.md](../specs/task-04-verify-kernel.md) | §1.4 REQ-KRN-01 – REQ-KRN-08 |
| [x] 05 | Verify user management | [task-05-verify-user-management.md](../specs/task-05-verify-user-management.md) | §1.5 REQ-USR-01 – REQ-USR-04 |
| [x] 06 | Verify SSH hardening | [task-06-verify-ssh.md](../specs/task-06-verify-ssh.md) | §1.6 REQ-SSH-01 – REQ-SSH-08 |
| [x] 07 | Verify firewall | [task-07-verify-firewall.md](../specs/task-07-verify-firewall.md) | §1.7 REQ-FW-01 – REQ-FW-10 |
| [x] 08 | Verify services (upgrades, fail2ban, rsyslog) | [task-08-verify-services.md](../specs/task-08-verify-services.md) | §1.8 REQ-UPD-01, §1.9 REQ-F2B-01, §1.10 REQ-LOG-01 |
| [x] 09 | Rename playbooks | [task-09-rename-playbooks.md](../specs/task-09-rename-playbooks.md) | §2.8 REQ-PLY-01, REQ-PLY-03 – REQ-PLY-06 |
| [x] 10 | Add generic_server inventory group and create prepGenericHwServer.yml | [task-10-generic-inventory-and-playbook.md](../specs/task-10-generic-inventory-and-playbook.md) | §2.1 REQ-PLT-01, §2.8 REQ-PLY-02 |
| [x] 11 | Gate os_base tasks by platform | [task-11-gate-os-base-for-platform.md](../specs/task-11-gate-os-base-for-platform.md) | §2.1 REQ-PLT-02, §2.4 REQ-BASE-01 – REQ-BASE-09 |
| [ ] 12 | Gate os_base_packages tasks by platform | [task-12-gate-os-base-packages-for-platform.md](../specs/task-12-gate-os-base-packages-for-platform.md) | §2.5 REQ-PKG-01, REQ-PKG-02 |
| [ ] 13 | Refactor kernel module blacklisting to use per-host variables | [task-13-refactor-kernel-module-host-vars.md](../specs/task-13-refactor-kernel-module-host-vars.md) | §2.3 REQ-KRN-01 – REQ-KRN-06 |
| [ ] 14 | Gate RPi-specific kernel tasks by platform | [task-14-gate-kernel-rpi-tasks.md](../specs/task-14-gate-kernel-rpi-tasks.md) | §2.3 REQ-KRN-07, REQ-KRN-08 |
| [ ] 15 | Implement per-host user management | [task-15-per-host-user-management.md](../specs/task-15-per-host-user-management.md) | §2.2 REQ-USR-01, REQ-USR-02 |
| [ ] 16 | Implement secondary disk management | [task-16-secondary-disk.md](../specs/task-16-secondary-disk.md) | §2.6 REQ-DSK-01 – REQ-DSK-05 |
| [ ] 17 | Document playbook applicability in README | [task-17-playbook-applicability.md](../specs/task-17-playbook-applicability.md) | §2.8 REQ-PLY-07 – REQ-PLY-10 |
