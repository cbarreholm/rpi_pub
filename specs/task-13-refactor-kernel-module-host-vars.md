# Task 13 — Refactor Kernel Module Blacklisting to Per-host Variables

**Type:** Implementation
**Requirements:** §2.3 REQ-KRN-01 – REQ-KRN-06

## Background
Currently the Bluetooth blacklist uses `requires_bluetooth` (inverted logic).
The requirements define `has_bluetooth`, `has_usb`, `has_firewire`, and `has_wifi`
as per-host boolean variables. This task standardises all module blacklisting
to use this pattern and aligns the variable name for Bluetooth.

## Changes required

### 1. Rename variable: requires_bluetooth → has_bluetooth
File: `ansible/roles/os_kernel/tasks/main.yml`

Change:
```yaml
when: not (requires_bluetooth | default(false))
```
To:
```yaml
when: not (has_bluetooth | default(false))
```

Update any inventory files or host_vars that currently set `requires_bluetooth`
to use `has_bluetooth` instead.

### 2. Add when condition to USB storage blacklist task (REQ-KRN-02)
```yaml
when: not (has_usb | default(false))
```
Default is `false` (blacklisted) — safe for VPS, can be set `true` on NUC/RPi.

### 3. Add when condition to FireWire blacklist task (REQ-KRN-03)
```yaml
when: not (has_firewire | default(false))
```
Default is `false` (blacklisted) — FireWire is rarely present or needed.

### 4. Add when condition to Wi-Fi power saving task (REQ-KRN-04)
```yaml
when: not (has_wifi | default(false))
```
Default is `false` — VPS and NUC without Wi-Fi will skip writing the modprobe options.

### 5. Update role defaults
File: `ansible/roles/os_kernel/defaults/main.yml`

Add defaults:
```yaml
has_bluetooth: false
has_usb: false
has_firewire: false
has_wifi: false
```

### 6. Update inventory host_vars for RPi hosts
Set appropriate values in inventory for RPi hosts that have this hardware,
e.g. RPi with Wi-Fi: `has_wifi: true`.

## Notes
- REQ-KRN-05 (sysctl hardening) and REQ-KRN-06 (IPv6 disable via sysctl) require
  no changes — those tasks already run unconditionally and apply to all platforms.
