# Task 24 — Reconcile Trixie cloud-init `manage_etc_hosts` with ansible

**Type:** Bug fix / cleanup
**Requirements:** §1.2 REQ-BASE (hostname handling, refinement)

## Background

On a freshly-flashed Debian 13 (Trixie) Raspberry Pi image, cloud-init
ships with `manage_etc_hosts: True`. This causes `/etc/hosts` to be
regenerated from `/etc/cloud/templates/hosts.debian.tmpl` on every boot.

Observed on `<host>` during the 2026-05-11 Trixie bring-up:

```
# Your system has configured 'manage_etc_hosts' as True.
# ...
127.0.1.1 <host> <host>
127.0.0.1 localhost
```

Two consequences:

1. The `127.0.1.1 {{fqdn}} {{hostname}}` template renders both fields as
   the short hostname when no domain is configured, producing the
   cosmetic duplicate (`<host> <host>`). Harmless — both aliases
   resolve to the same loopback address — but noisy.
2. The ansible task at `ansible/roles/os_base/tasks/main.yml:189-196`
   (`Update /etc/hosts with '{{config_system_hostname}}'`) is effectively
   dead on Trixie images:
   - Its regex `^(127.0.1.1)(\s)*(raspberrypi)$` does not match the
     cloud-init-rendered line (which contains the imager-provisioned
     hostname, not `raspberrypi`), so it silently no-ops.
   - Even if it did match, cloud-init would revert the edit on the next
     boot.

## Goal

Make the hostname / `/etc/hosts` handling on Trixie hosts coherent and
non-misleading: either ansible owns `/etc/hosts`, or cloud-init does —
not both, with one of them silently doing nothing.

## Approach (pick one during implementation)

1. **Let cloud-init own `/etc/hosts`** — remove the
   `Update /etc/hosts with ...` ansible task entirely. The
   `ansible.builtin.hostname` task immediately above it still sets the
   system hostname; cloud-init's template will then produce a correct
   `127.0.1.1 <hostname> <hostname>` line on next boot.
2. **Let ansible own `/etc/hosts`** — disable cloud-init's management
   (`manage_etc_hosts: False` in `/etc/cloud/cloud.cfg` or via a
   drop-in), and fix the regex in the ansible task to match
   whatever the imager actually wrote (or rewrite the task to template
   the file outright).

Option 1 is the lower-friction choice: cloud-init is already doing the
right thing on Trixie, and removing the dead task eliminates the
mismatch.

## Tests (write first)

1. Assert that after the `hostname` tag runs on a Trixie pi_server host,
   `/etc/hosts` contains a `127.0.1.1` line referencing
   `config_system_hostname`.
2. Assert that the line survives a reboot (i.e. cloud-init renders
   consistently with the ansible-set hostname).
3. If Option 1 is chosen: assert no ansible task attempts to edit
   `/etc/hosts` directly.
4. If Option 2 is chosen: assert `manage_etc_hosts` is `False` in the
   effective cloud-init config and the ansible task's regex matches the
   pre-edit state on a fresh image.

## Acceptance

- `getent hosts <hostname>` resolves to `127.0.1.1` on a freshly-imaged
  Trixie pi_server after Phase 1 of the rollout.
- The chosen owner (cloud-init or ansible) is the only writer; the other
  is either removed or explicitly disabled.
- No silent no-op tasks remain in `os_base` for `/etc/hosts`.
- README / `os_base` role docs updated to note the chosen ownership.

## Out of scope

- Cosmetic duplicate (`<host> <host>`) — accepted as a harmless
  consequence of cloud-init's default template when no domain is set.
  Adding a domain / FQDN is a separate concern.
- Changing the system hostname mechanism (`hostnamectl` vs. legacy
  `/etc/hostname` writes).
