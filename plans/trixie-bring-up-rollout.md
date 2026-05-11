# Trixie Bring-Up Phased Rollout Procedure

**Status:** Procedure / runbook (not a single-shot implementation task)
**Applies to:** `prepPiServer.yml` against a freshly-flashed Debian 13 (Trixie) Raspberry Pi
**Last validated against:** `reverseproxy` host investigation, 2026-05-11

## Background

During multi-iteration ansible runs against a freshly-flashed Trixie Pi
(`reverseproxy`), several issues compounded and made root-cause attribution
difficult. After investigation we concluded:

- Commit `61a850d` (the original suspect) was **not** at fault.
- Several pre-existing or unrelated issues surfaced together:
  - Trixie's netplan/cloud-init chain (`cc_netplan_nm_patch` missing in
    cloud-init's module discovery) loses the rendered NetworkManager Wi-Fi
    profile across reboots; workaround is a manual `nmcli connection add`.
  - UniFi **Client Device Isolation** on the DMZ SSID prevented
    wireless-to-wireless reachability between laptop and Pi — a
    network-policy decision, not a playbook bug. eth0-attached management
    bypasses it.
  - fail2ban's `nginx-botsearch` jail is unconditionally enabled and
    crashes the service on hosts without nginx (tracked as Task 22).
  - `wireless-regdb` was missing on Trixie's default RPi image (now added;
    tracked as Task 23).
  - IPv6 disabled via `os_kernel` sysctl/modprobe causes NetworkManager
    warning spam (`failure 13 (Permission denied - ipv6: IPv6 is disabled)`)
    — by design, not blocking.

This document captures the phased rollout to use when bringing up a
freshly-flashed Trixie host, so any future regression has a clean isolation
path instead of multiple compounding causes.

## Pre-flight

Before re-flashing or applying the first phase:

1. Set `has_wifi` for the target host in `ansible/inventory.yaml` to match
   its intended capability. For eth0-only management (e.g. `reverseproxy`
   on a Pi 4B with reliable Ethernet), set `has_wifi: false` — this will
   blacklist `brcmfmac` in Phase 3, eliminating WiFi as a fallback but
   reducing attack surface.
2. Confirm SSH access works to the freshly-imaged Pi via eth0 using the
   imager-provisioned user before running anything.
3. **Trixie deb822 caveat:** the `apt-sources` task targets
   `/etc/apt/sources.list` (one-line legacy format) via regex. Trixie
   defaults to deb822 (`/etc/apt/sources.list.d/debian.sources`), so the
   task may silently no-op. Verify your effective mirror after Phase 1
   (`apt-cache policy | head`).

## Phases

Each phase: run `prepPiServer.yml` with the indicated `--skip-tags`,
reboot, verify before proceeding.

| Phase | --skip-tags | Adds (vs previous phase) | Verify |
|-------|-------------|---------------------------|--------|
| 1 — Foundation | `modprobe,sysctl,firewall,fail2ban,autoupdate,rsyslog` | users, ssh, timezone, locale, keyboard, apt, apt-sources, fstabsetup, swapsize, hostname, basepackages, kernelscheduler | SSH over eth0; `apt-get update` works; hostname correct |
| 2 — Sysctl hardening | `modprobe,firewall,fail2ban,autoupdate,rsyslog` | sysctl | SSH; expect NM IPv6-disabled warnings in journal (benign) |
| 3 — Module blacklists | `firewall,fail2ban,autoupdate,rsyslog` | modprobe | SSH; `dmesg` shows no module-load errors; correct `has_wifi` value confirmed via `/etc/modprobe.d/` contents |
| 4 — Firewall | `fail2ban,autoupdate,rsyslog` | firewall | SSH (new session); `sudo ufw status verbose`; apt + ntp still work outbound |
| 5 — Auxiliary services | `fail2ban` | autoupdate, rsyslog | SSH; `unattended-upgrades --dry-run`; rsyslog targets resolve (if configured) |
| 6 — fail2ban | (none) | fail2ban | **Expected failure on non-nginx hosts until Task 22 is complete**; SSH still works; `systemctl status fail2ban` |

## Per-phase verification commands

From your laptop after each reboot:

```bash
ssh <user>@<host> 'uptime && (systemctl --failed --no-legend || echo "all units healthy")'
```

For Phase 4 (firewall) specifically:

```bash
ssh <user>@<host> 'sudo ufw status verbose; apt-get -s upgrade >/dev/null && echo apt-ok; getent hosts deb.debian.org'
```

## If a phase breaks

1. Don't proceed.
2. From a clean pre-phase state (re-flash if necessary), apply phases
   up to the failing one again.
3. Localize within the phase: run with `--tags <single-tag>` to enable
   one tag at a time.
4. File the finding as a new task in `plans/implementation-plan.md`
   before returning to the rollout.
