# Task 12 — Gate os_base_packages Tasks by Platform

**Type:** Implementation
**Requirements:** §2.5 REQ-PKG-01, REQ-PKG-02

## Background
The current package lists include `raspberrypi-kernel-headers` which does not exist
on generic Debian. Installing it on a VPS or NUC will fail. RPi-specific packages
must be excluded on `generic_server` hosts.

## Changes required

File: `ansible/roles/os_base_packages/tasks/main.yml`

### Option A — Separate package lists (recommended)
Split each existing version task (Debian 10, Debian 12) into two tasks:

1. A task with packages common to all platforms — no `when` guard needed beyond the
   version check.
2. A task with RPi-specific packages guarded with:
   `when: ansible_distribution_major_version == "12" and inventory_hostname in groups['pi_server']`

RPi-specific packages to move to the gated task:
- `raspberrypi-kernel-headers`
- `dkms` (only needed for RPi kernel module builds)
- `xkbset` (physical keyboard utility, not needed on VPS)
- `ttf-mscorefonts-installer` (irrelevant on headless server without display)
- `console-data` (Debian 10 only — console keyboard data for physical hardware)

### Option B — Inline when condition
Add `when: inventory_hostname in groups['pi_server']` to the entire existing task
and create a separate task for the common subset.

Option A is preferred for clarity.

## Verification
Run against a generic host with `--check` and confirm no `raspberrypi-kernel-headers`
install is attempted.
