# Task 20 — Complete Section 1 Requirements Documentation

**Type:** Documentation
**Requirements:** §1.1 – §1.10 (gap completion)

## Background

The coverage note at the top of `specs/requirements.md` states:

> The baseline RPi requirements (Section 1) have not yet been fully documented — this is a known gap and a TODO.

Tasks 01–08 verified the existing implementation against the requirements as written, but the requirements themselves were written as a best-effort capture and may be incomplete. This task audits each role's actual task files against the documented Section 1 requirements and adds any missing requirements.

## Changes required

### 1. Audit each role against its Section 1 requirements

For each role, read the task files and compare against the documented requirements:

| Section | Role | Req range |
|---------|------|-----------|
| §1.1 | pre-conditions (playbook guard) | REQ-PRE-01 – REQ-PRE-02 |
| §1.2 | `os_base` | REQ-BASE-01 – REQ-BASE-14 |
| §1.3 | `os_base_packages` | REQ-PKG-01 |
| §1.4 | `os_kernel` | REQ-KRN-01 – REQ-KRN-08 |
| §1.5 | `os_users` | REQ-USR-01 – REQ-USR-04 |
| §1.6 | `os_services` (SSH) | REQ-SSH-01 – REQ-SSH-08 |
| §1.7 | `os_services` (UFW) | REQ-FW-01 – REQ-FW-10 |
| §1.8 | `os_services` (unattended-upgrades) | REQ-UPD-01 |
| §1.9 | `os_services` (fail2ban) | REQ-F2B-01 |
| §1.10 | `os_services` (rsyslog) | REQ-LOG-01 |

### 2. Add missing requirements to `specs/requirements.md`

For each gap found, append a new numbered requirement to the appropriate subsection following the existing numbering convention (e.g. REQ-BASE-15, REQ-PKG-02, etc.).

### 3. Remove the coverage note TODO

Once the audit is complete and gaps are filled, update the coverage note at the top of `specs/requirements.md` to reflect that Section 1 is now fully documented.

## Notes

- This is a documentation-only task. No role code changes are required.
- No tests are required for this task.
- If a gap is ambiguous (i.e. it is unclear whether behaviour is intentional or incidental), document it as a requirement — the implementation is the source of truth.
