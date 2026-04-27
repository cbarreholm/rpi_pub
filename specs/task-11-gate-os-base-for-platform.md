# Task 11 — Gate os_base Tasks by Platform

**Type:** Implementation
**Requirements:** §2.1 REQ-PLT-02, §2.4 REQ-BASE-01 – REQ-BASE-09

## Background
Several tasks in `os_base` are RPi-specific (SD card fstab, dphys-swapfile, APT mirror,
/etc/hosts raspberrypi fixup). These must be skipped on `generic_server` hosts.
Tasks that apply to all platforms (timezone, locale, keyboard, APT config, hostname)
must continue to run unchanged.

## Changes required

File: `ansible/roles/os_base/tasks/main.yml`

Add `when: inventory_hostname in groups['pi_server']` to the following tasks:

| Task | Requirement |
|---|---|
| fstab template task | REQ-BASE-01 / REQ-BASE-02 |
| `dphys-swapfile` lineinfile task | REQ-BASE-03 / REQ-BASE-04 |
| `/etc/hosts` replace task (raspberrypi) | REQ-BASE-06 / REQ-BASE-07 |
| APT mirror `replace` tasks (both main and security) | REQ-BASE-08 / REQ-BASE-09 |
| `findmnt` tasks for PARTUUID (boot and boot/firmware) | REQ-BASE-01 / REQ-BASE-02 |

The following tasks must **not** be gated — they apply on all platforms:
- Timezone
- Locale and language
- Keyboard layout
- APT config (`99-custom-configs`, `99-custom-cache`)
- Hostname via `ansible.builtin.hostname`

## Notes
- The `groups['pi_server']` check requires `gather_facts: true` (already set in playbooks).
- Run a dry run (`--check`) against a generic host after changes to confirm no RPi tasks execute.
