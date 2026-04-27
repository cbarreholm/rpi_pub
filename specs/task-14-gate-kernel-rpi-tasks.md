# Task 14 — Gate RPi-specific Kernel Tasks by Platform

**Type:** Implementation
**Requirements:** §2.3 REQ-KRN-07, REQ-KRN-08

## Background
Two areas of `os_kernel` are specific to Raspberry Pi hardware:
1. The Kyber I/O scheduler for the SD card (`mmcblk0`)
2. Wi-Fi power saving configuration via `rc.local` and `iwconfig`

These must not run on generic Debian hosts where neither applies.

## Changes required

File: `ansible/roles/os_kernel/tasks/main.yml`

### REQ-KRN-07 — Gate Kyber scheduler tasks
Add `when: inventory_hostname in groups['pi_server']` to:
- The `replace` task that sets `elevator=kyber` in `/boot/cmdline.txt`
- The `command` task that writes `kyber` to `/sys/block/mmcblk0/queue/scheduler`
- The `lineinfile` task that adds the Kyber persistence line to `/etc/rc.local`

### REQ-KRN-08 — Gate Wi-Fi power saving tasks
Add `when: inventory_hostname in groups['pi_server']` to:
- The `lineinfile` task that adds `/sbin/iwconfig wlan0 power off` to `/etc/rc.local`
- The `copy` task that writes the Wi-Fi power saving modprobe options
  (this overlaps with task 13 — coordinate to avoid double-gating)

## Notes
- `/boot/cmdline.txt` does not exist on generic Debian — the task will fail without the guard.
- `/sys/block/mmcblk0` does not exist on VPS or NUC — the runtime command will also fail.
- Verify with `--check` against a generic host that none of these tasks are attempted.
