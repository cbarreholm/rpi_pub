# Task 26 — Disable Default exim4 MTA on Pi/Generic Servers

**Type:** Bug fix / hardening
**Requirements:** §1.8 (refinement — new requirement to be added)

## Background

The default Raspberry Pi OS / Debian images ship `exim4-daemon-light`
enabled, which attempts to bind a listener on boot. Because `os_kernel`
disables IPv6 via modprobe blacklist (REQ-KRN-02) and sysctl, exim4
fails on every boot with:

```
exim4[<pid>]: IPv6 socket creation failed: Address family not supported by protocol
systemd[1]: exim4.service: Main process exited, code=exited, status=1/FAILURE
systemd[1]: exim4.service: Failed with result 'exit-code'.
```

Observed on a Trixie Pi 4B after the 2026-05-11 bring-up, Phase 5
verification on 2026-05-12. `systemctl --failed` lists exim4 on an
otherwise healthy host. Same interaction is expected on every
freshly-flashed Trixie pi_server until addressed.

No role in this repo configures exim4, no host requires an MTA, and
nothing depends on local mail delivery. The failure is benign but
pollutes `--failed` output and obscures real regressions in future
phased rollouts (`plans/trixie-bring-up-rollout.md`).

## Goal

Ensure no installed-by-default MTA leaves the host in a `failed` state
after `prepPiServer.yml` / `prepGenericHwServer.yml` completes. The
target is a clean `systemctl --failed` output on a freshly-flashed
Trixie image once the playbook has run.

## Approach (pick one during implementation)

1. **Mask exim4 in `os_services`** — add a task that runs `systemctl
   disable --now exim4` followed by `systemctl mask exim4`, idempotent,
   conditional on the unit existing. Lowest blast radius, reversible.
2. **Purge exim4 packages in `os_base_packages`** — `apt purge exim4
   exim4-base exim4-config exim4-daemon-light bsd-mailx` (verify the
   exact package set on Trixie vs Bookworm first). Cleaner footprint
   but irreversible without re-install; also pulls in dependency
   considerations (mailutils, cron MAILTO behaviour).
3. **Reconfigure exim4 to IPv4-only** — edit
   `/etc/exim4/update-exim4.conf.conf` to drop `::1` from
   `dc_local_interfaces`, then `update-exim4.conf`. Only worth doing if
   a future requirement actually needs local mail; otherwise it just
   keeps a service alive for no reason.

Recommendation: option 1 for the bug fix. Revisit if a host ever needs
local mail delivery (no current host does).

## Tests (write first)

1. Assert that after the relevant role runs against a target where
   `exim4.service` exists, the service is `masked` (or absent under
   option 2).
2. Assert `systemctl --failed --no-legend` is empty on a freshly-applied
   host (integration check; can be expressed as a Molecule/verify
   step or as a checklist line in the runbook).
3. Assert the change is idempotent: a second playbook run reports no
   changes for the exim4 task.

Run with: `python -m unittest discover -s ansible/roles/os_services/tests -p "test_exim4_disabled.py" -v`
(adjust path to whichever role owns the change).

## Acceptance

- `systemctl status exim4` on any freshly-flashed Trixie pi_server
  reports `masked` (or "Unit not found" under option 2), not `failed`.
- `systemctl --failed --no-legend` on a freshly-applied host is empty.
- Playbook is idempotent across runs.
- `specs/requirements.md` §1.8 gains a requirement stating that the
  playbook shall not leave any installed-by-default service in a
  `failed` state, with exim4 named as the concrete instance.
- `plans/trixie-bring-up-rollout.md` Phase 5 verification line updated
  to expect a clean `--failed` list (i.e. remove the exim4 caveat once
  the fix lands).

## Out of scope

- Configuring a working MTA (no host needs one today).
- Removing other default-installed packages that do not fail
  (`bluez` on `has_bluetooth: false` hosts, etc. — those are already
  handled by module blacklisting and are not in `failed` state).
- Revisiting the IPv6-disabled policy itself — that is tracked
  separately under Task 25 and the broader `os_kernel` IPv6 work in
  progress.
