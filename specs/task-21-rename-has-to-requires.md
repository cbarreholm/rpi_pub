# Task 21 — Rename `has_*` Hardware Flags to `requires_*` Capability Flags

**Type:** Implementation / Refactor
**Requirements:** §2.3 REQ-KRN-01 – REQ-KRN-04 (semantic update)

## Background
Task 13 renamed `requires_bluetooth` to `has_bluetooth` and introduced
`has_usb`, `has_firewire`, and `has_wifi` as per-host flags describing what
hardware is present.

The intent at the server-configuration level is the inverse: each host should
declare what capabilities it **requires**, independent of what the hardware
provides. If Bluetooth or Wi-Fi is physically present but the server does not
require it, the role should disable it.

This task renames the flags and re-frames their semantics accordingly.

## Changes required

### 1. Rename variables in `ansible/roles/os_kernel/`
- `has_bluetooth` → `requires_bluetooth`
- `has_usb` → `requires_usb`
- `has_firewire` → `requires_firewire`
- `has_wifi` → `requires_wifi`

Files affected:
- `ansible/roles/os_kernel/defaults/main.yml` — defaults remain `false`
  (server requires nothing by default; modules get blacklisted).
- `ansible/roles/os_kernel/tasks/main.yml` — update all `when:` conditions.
  Logic stays inverted (`when: not (requires_X | default(false))`) so the
  blacklist applies when the capability is not required.

### 2. Update inventory / host_vars
Replace any `has_*: true` settings with `requires_*: true` where the host
needs the capability (e.g. an RPi server that uses Wi-Fi sets
`requires_wifi: true`, even though the hardware always has it).

### 3. Update requirements
File: `specs/requirements.md` §2.3
- REQ-KRN-01: "While `requires_bluetooth` is false …"
- REQ-KRN-02: "While `requires_usb` is false …"
- REQ-KRN-03: "While `requires_firewire` is false …"
- REQ-KRN-04: "While `requires_wifi` is false …"

Also update §1.4 if the same flag names appear in the Section 1
verification requirements.

### 4. Update project overview
File: `specs/project.md` — update the hardware-capabilities paragraph to
describe `requires_*` capability flags instead of `has_*` hardware flags.

### 5. Update task specs and learnings
- `specs/task-04-verify-kernel.md` — update REQ-KRN-03 description.
- `specs/task-13-refactor-kernel-module-host-vars.md` — add a note at the
  top that this task was superseded by Task 21 with respect to naming.
- `memory/learnings.md` — record the rename and the rationale (server
  declares required capabilities; hardware presence is irrelevant).

### 6. Update README
If `README.md` references `has_*` flags, update to `requires_*`.

## Verification
- `ansible-playbook --syntax-check` for `prepPiServer.yml` and
  `prepGenericHwServer.yml`.
- `ansible-lint` clean.
- `ansible-playbook --check` against an RPi host confirms the blacklist
  tasks are skipped only for capabilities the host declares it requires.
- `grep -r "has_bluetooth\|has_usb\|has_firewire\|has_wifi"` returns no
  matches in `ansible/`, `specs/`, or `memory/`.

## Notes
- Logic is unchanged; only naming and the documented intent change.
- Default of `false` for all `requires_*` flags means a host with no
  inventory overrides is locked down by default.
