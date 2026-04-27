# Task 04 — Verify Kernel Hardening

**Type:** Verification
**Requirements:** §1.4 REQ-KRN-01 – REQ-KRN-08

## What to verify

File: `ansible/roles/os_kernel/tasks/main.yml`

### REQ-KRN-01 — Unused filesystem modules blacklisted
Confirm a `copy` task writes `install <module> /bin/true` to `/etc/modprobe.d/<module>.conf`
for each of: `cramfs`, `dccp`, `freevxfs`, `hfs`, `hfsplus`, `jffs2`, `rds`, `sctp`,
`squashfs`, `tipc`, `udf`.

### REQ-KRN-02 — IPv6 module blacklisted
Confirm a `copy` task writes `blacklist ipv6` to `/etc/modprobe.d/ipv6.conf`.

### REQ-KRN-03 — Bluetooth blacklisted when has_bluetooth is false
Confirm the Bluetooth blacklist task has a `when: not (requires_bluetooth | default(false))`
condition (or equivalent using `has_bluetooth`).
Note: variable name in code is `requires_bluetooth` — flag if it differs from `has_bluetooth`
used in Section 2 requirements and record as a naming inconsistency to resolve in task 13.

### REQ-KRN-04 — FireWire blacklisted
Confirm a `copy` task writes blacklist entries for all FireWire modules to
`/etc/modprobe.d/disable_firewire.conf`.

### REQ-KRN-05 — USB storage blacklisted
Confirm a `copy` task writes `blacklist usb-storage` to
`/etc/modprobe.d/disable_usb-storage.conf`.

### REQ-KRN-06 — Wi-Fi power saving disabled
Confirm a `copy` task writes `rtw_power_mgnt=0` options for Realtek Wi-Fi modules to
`/etc/modprobe.d/disable_wifi_powersaving.conf`.

### REQ-KRN-07 — Sysctl kernel hardening
Confirm a `copy` task deploys `/etc/sysctl.d/10-harden_sysctl.conf` containing:
- `fs.suid_dumpable = 0`
- `kernel.randomize_va_space = 2`
- `net.ipv4.conf.all.accept_redirects = 0` (and related IPv4 hardening entries)
- `net.ipv6.conf.all.disable_ipv6 = 1` (and related IPv6 disable entries)
Confirm a `sysctl -p` command task follows to apply changes.

### REQ-KRN-08 — Kyber I/O scheduler persistent
Confirm tasks are present to:
- Set `elevator=kyber` in `/boot/cmdline.txt`
- Write `kyber` to `/sys/block/mmcblk0/queue/scheduler` at runtime
- Add persistence via `/etc/rc.local`

## Pass criteria
All checks pass with no code changes required.
Any gap or naming inconsistency must be noted and a follow-up task created.
