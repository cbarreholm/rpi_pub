# Implementation Plan

Tasks 01–08 are verification tasks for the existing Raspberry Pi baseline (Section 1).
Tasks 09–17 are implementation tasks for Generic Debian Platform Support (Section 2).
Tasks 18–19 are implementation tasks for Additional User Management (Section 3).
Task 20 completes the Section 1 requirements documentation gap.
Task 21 reverses the `requires_* → has_*` rename from Task 13 so hosts declare required capabilities rather than describe present hardware.
Tasks 22–25 address bugs and gaps surfaced during the 2026-05-11 Trixie bring-up investigation (see `plans/trixie-bring-up-rollout.md`).

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
| [x] 12 | Gate os_base_packages tasks by platform | [task-12-gate-os-base-packages-for-platform.md](../specs/task-12-gate-os-base-packages-for-platform.md) | §2.5 REQ-PKG-01, REQ-PKG-02 |
| [x] 13 | Refactor kernel module blacklisting to use per-host variables | [task-13-refactor-kernel-module-host-vars.md](../specs/task-13-refactor-kernel-module-host-vars.md) | §2.3 REQ-KRN-01 – REQ-KRN-06 |
| [x] 14 | Gate RPi-specific kernel tasks by platform | [task-14-gate-kernel-rpi-tasks.md](../specs/task-14-gate-kernel-rpi-tasks.md) | §2.3 REQ-KRN-07, REQ-KRN-08 |
| [x] 15 | Implement per-host user management | [task-15-per-host-user-management.md](../specs/task-15-per-host-user-management.md) | §2.2 REQ-USR-01, REQ-USR-02 |
| [x] 16 | Implement secondary disk management | [task-16-secondary-disk.md](../specs/task-16-secondary-disk.md) | §2.6 REQ-DSK-01 – REQ-DSK-05 |
| [x] 17 | Document playbook applicability in README | [task-17-playbook-applicability.md](../specs/task-17-playbook-applicability.md) | §2.8 REQ-PLY-07 – REQ-PLY-10 |
| [x] 18 | Implement additional admin users | [task-18-additional-admin-users.md](../specs/task-18-additional-admin-users.md) | §3.1 REQ-AUSR-01 – REQ-AUSR-09 |
| [x] 19 | Implement limited users | [task-19-limited-users.md](../specs/task-19-limited-users.md) | §3.2 REQ-LUSR-01 – REQ-LUSR-08 |
| [ ] 20 | Complete Section 1 requirements documentation | [task-20-complete-section1-requirements.md](../specs/task-20-complete-section1-requirements.md) | §1.1 – §1.10 |
| [ ] 21 | Rename `has_*` hardware flags to `requires_*` capability flags | [task-21-rename-has-to-requires.md](../specs/task-21-rename-has-to-requires.md) | §2.3 REQ-KRN-01 – REQ-KRN-04 |
| [ ] 22 | Gate fail2ban nginx jails to hosts running nginx | [task-22-gate-fail2ban-nginx-jail.md](../specs/task-22-gate-fail2ban-nginx-jail.md) | §1.9 REQ-F2B-01 (refinement) |
| [ ] 23 | Document and test wireless-regdb on Trixie pi_server hosts | [task-23-wireless-regdb-test.md](../specs/task-23-wireless-regdb-test.md) | §1.3 REQ-PKG-02 (new) |
| [ ] 24 | Reconcile Trixie cloud-init `manage_etc_hosts` with ansible | [task-24-trixie-cloud-init-etc-hosts.md](../specs/task-24-trixie-cloud-init-etc-hosts.md) | §1.2 REQ-BASE (refinement) |
| [ ] 25 | Drop IPv6 sysctl entries (resolve modprobe/sysctl collision) | [task-25-drop-ipv6-sysctl-entries.md](../specs/task-25-drop-ipv6-sysctl-entries.md) | §1.4 REQ-KRN-02, REQ-KRN-07; §2.3 REQ-KRN-06 (amendment) |
