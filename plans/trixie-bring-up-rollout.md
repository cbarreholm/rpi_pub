# Trixie Bring-Up Phased Rollout Procedure

**Status:** Procedure / runbook (not a single-shot implementation task)
**Applies to:** `prepPiServer.yml` against a freshly-flashed Debian 13 (Trixie) Raspberry Pi
**Last validated against:**
- Pi 4B `pi_server`, full rollout (Phases 1–6) with `has_wifi: true`, 2026-05-12 — eth0 + Wi-Fi both functional; only `--failed` units are the two pre-existing tracked issues (exim4 / Task 26, fail2ban nginx jails / Task 22).
- Same host, in-place flip `has_wifi: true → false`, 2026-05-12 — `--tags modprobe` re-run + reboot; `wlan0` absent, `brcmfmac`/`cfg80211` not loaded, `nmcli` retains the netplan-rendered wifi connection definition with an empty `DEVICE` column (unbound, not active), `--failed` set unchanged from baseline, no new wifi-related `dmesg`. Confirms the "Post-rollout" procedure below.

## Background

During multi-iteration ansible runs against a freshly-flashed Trixie Pi
(`reverseproxy`), several issues compounded and made root-cause attribution
difficult. After investigation we concluded:

- Commit `61a850d` (the original suspect) was **not** at fault.
- Several pre-existing or unrelated issues surfaced together:
  - The cloud-init `cc_netplan_nm_patch` warning on Trixie (`Could not
    find module named cc_netplan_nm_patch`, cloud-init 25.2) is benign
    noise — the referenced module is absent in this cloud-init version
    and does not block NetworkManager profile rendering. Under netplan,
    NM keyfiles are runtime-rendered to
    `/run/NetworkManager/system-connections/` on every boot, and
    `/etc/NetworkManager/system-connections/` is expected to be empty.
    The originally-observed "no Wi-Fi after reboot" on `reverseproxy`
    (no `nmcli` connection, no IP on `wlan0`) is now attributed to
    `has_wifi: false` blacklisting `brcmfmac` — i.e. expected behaviour
    when wireless is intentionally disabled, not a cloud-init/netplan
    bug. Validated 2026-05-12 on a Pi 4B with `has_wifi: true`: full
    bring-up brings wireless up cleanly without any manual `nmcli`
    workaround.
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

## Post-rollout: in-place flip of `has_wifi: true → false`

Scenario: a host has already completed the full rollout with
`has_wifi: true` (e.g. the 2026-05-12 Pi 4B validation) and is now
being transitioned to its production posture with wireless disabled.
This is a single targeted change, not a re-rollout. Use this path
when the wifi-enabled build has been validated and you want to
reduce attack surface without re-flashing.

### Pre-checks (capture baseline before the change)

1. Confirm SSH over eth0 works independently of `wlan0`:
   `ssh <user>@<host> 'ip -br link show eth0; ip -br addr show eth0'`
   — eth0 must show `UP` with an IPv4 address. If management has
   ever depended on `wlan0` for this host, do **not** proceed.
2. Capture the current `--failed` baseline so post-change drift is
   easy to spot:
   `ssh <user>@<host> 'systemctl --failed --no-legend'`
   — expect only `exim4.service` (Task 26) and `fail2ban.service`
   (Task 22). Anything else: investigate first.
3. Record current wireless state for the diff:
   `ssh <user>@<host> 'nmcli -t -f NAME,DEVICE,TYPE connection show; ip -br link show wlan0; lsmod | grep -E "^brcmfmac|^cfg80211"'`

### Apply the change

1. In `ansible/inventory.yaml`, set `has_wifi: false` for the host.
   Commit before applying so the inventory matches what was deployed.
2. Re-run only the modprobe-affecting tag (no need to re-run the
   whole playbook):
   ```bash
   ansible-playbook -i ansible/inventory.yaml \
     -e @ansible/secrets/secrets_file.enc \
     --vault-password-file ansible/secrets/vault_password_file \
     --limit <host> --tags modprobe ansible/prepPiServer.yml
   ```
3. Verify the blacklist drop-in is present **before** rebooting:
   `ssh <user>@<host> 'ls /etc/modprobe.d/ | grep -i -E "wifi|brcm"; cat /etc/modprobe.d/<the-file>'`
   — the file should contain `blacklist brcmfmac` (and any
   companion entries the role writes for `has_wifi: false`).
4. Reboot: `ssh <user>@<host> 'sudo systemctl reboot'`

### Post-reboot verification

1. SSH over eth0 still works (this is the load-bearing check).
2. `wlan0` is gone, brcmfmac did not load:
   ```bash
   ssh <user>@<host> 'ip -br link show wlan0 2>&1; lsmod | grep -E "^brcmfmac|^cfg80211" || echo "wifi modules not loaded (expected)"'
   ```
   Expected: `ip link` reports `Device "wlan0" does not exist`; no
   `brcmfmac` row in `lsmod`.
3. `nmcli` no longer binds the wifi profile:
   `ssh <user>@<host> 'nmcli -t -f NAME,DEVICE,TYPE connection show'`
   — the `netplan-wlan0-*` connection either disappears or shows
   with an empty/`--` device column. Either is acceptable; the
   important property is that nothing is **active** on wifi.
4. `--failed` set is unchanged from baseline:
   `ssh <user>@<host> 'systemctl --failed --no-legend'`
   — still only exim4 + fail2ban. Anything new is a regression.
5. `dmesg` shows no new wifi-related errors and no module
   load/unload churn:
   `ssh <user>@<host> 'sudo dmesg --since=-2min | grep -i -E "brcmfmac|cfg80211|wlan" || echo "no wifi-related kernel messages (expected)"'`

### Concerning outcomes (stop and investigate)

- SSH over eth0 fails after reboot — you've lost management. Recover
  via console or re-flash. This is why pre-check (1) is mandatory.
- A new entry appears in `systemctl --failed` that isn't exim4 or
  fail2ban. Likely candidates: any service that was implicitly
  depending on `wlan0` existing (none expected in this repo, but
  worth checking before declaring done).
- `brcmfmac` still loads despite the blacklist (`lsmod` shows it).
  Indicates the drop-in didn't land in the right path, or
  `update-initramfs` needs re-running. Re-run the `modprobe` tag and
  reboot; if it persists, file a task before proceeding.
- Netplan/NetworkManager throws errors about the missing `wlan0`
  device at boot (warnings about a missing device are expected and
  benign; an actual error that fails a unit is not).

### What this in-place flip does **not** validate

- First-boot behaviour when `has_wifi: false` is set from Phase 1 of
  a fresh flash. If/when a future host (e.g. a Pi zero W
  alternative or another Pi 4B) is brought up eth0-only from
  scratch, run the full Phase 1–6 rollout against it with
  `has_wifi: false` set before Phase 1, and update **Last validated
  against** above with the result.
