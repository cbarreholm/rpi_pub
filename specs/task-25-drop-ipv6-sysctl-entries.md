# Task 25 — Drop IPv6 sysctl Entries (Resolve modprobe/sysctl Collision)

**Type:** Bug fix
**Requirements:** §1.4 REQ-KRN-02, REQ-KRN-07; §2.3 REQ-KRN-06 (amendment)

## Background

The `os_kernel` role disables IPv6 via two independent mechanisms:

1. **modprobe blacklist** — `ansible/roles/os_kernel/tasks/main.yml:92-98` writes
   `/etc/modprobe.d/ipv6.conf` containing `blacklist ipv6` (tag: `modprobe`).
2. **sysctl** — `ansible/roles/os_kernel/tasks/main.yml:192-204` writes IPv6
   sysctl keys (`net.ipv6.conf.{all,default,lo}.disable_ipv6 = 1` plus
   `accept_ra`, `accept_redirects`, `accept_source_route`, `forwarding`) into
   `/etc/sysctl.d/10-harden_sysctl.conf` (tag: `sysctl`).

After a reboot following the modprobe blacklist taking effect, the IPv6 module
is no longer loaded and `/proc/sys/net/ipv6/*` does not exist. The subsequent
`Reload Sysctl Changes` task (`tasks/main.yml:207-212`) fails:

```
sysctl: cannot stat /proc/sys/net/ipv6/conf/all/accept_ra: No such file or directory
sysctl: cannot stat /proc/sys/net/ipv6/conf/all/disable_ipv6: No such file or directory
... (8 more)
non-zero return code
```

Observed on `reverseproxy` 2026-05-11 during Phase 4 of the Trixie phased
rollout (`plans/trixie-bring-up-rollout.md`). The two mechanisms collide:
once the module is unloaded, the sysctl entries become unsettable.

## Goal

Use the modprobe blacklist as the single source of truth for disabling IPv6.
Remove the IPv6 sysctl entries entirely. The blacklist is strictly stronger
(the stack is unloaded, not merely disabled per-interface), so the sysctl
entries are redundant.

## Approach

1. Edit `ansible/roles/os_kernel/tasks/main.yml` to remove the IPv6 blocks
   from `/etc/sysctl.d/10-harden_sysctl.conf`:
   - `## IPV6 Networking` block (lines 192-199 in current main)
   - `## IPV6 Disabled` block (lines 201-204 in current main)
2. Leave the IPv4 hardening block and the `Reload Sysctl Changes` task
   unchanged.
3. Add a handler/task or playbook step to remove any pre-existing IPv6
   keys from `/etc/sysctl.d/10-harden_sysctl.conf` on hosts that have
   already received the old version (the `copy` task with new content
   handles this naturally — it replaces the file wholesale).

## Tests (write first)

1. Assert that the rendered content of `/etc/sysctl.d/10-harden_sysctl.conf`
   contains **no** `net.ipv6.*` keys.
2. Assert that the IPv4 hardening keys are still present.
3. Assert that `/etc/modprobe.d/ipv6.conf` still exists with
   `blacklist ipv6` (regression guard for REQ-KRN-02).
4. Integration check (manual or via molecule if available): on a Trixie
   host with the role applied, `sysctl -p /etc/sysctl.d/10-harden_sysctl.conf`
   exits 0 after a reboot.

Place unit tests under `ansible/roles/os_kernel/tests/` following the
project's existing test layout.

## Acceptance

- Phase 4 of `plans/trixie-bring-up-rollout.md` completes without the
  `Reload Sysctl Changes` failure on `reverseproxy`.
- IPv6 remains disabled on the host (`ip -6 addr` shows no addresses,
  `lsmod | grep ipv6` is empty).
- All existing IPv4 sysctl hardening still applied (`sysctl net.ipv4.tcp_syncookies`
  returns `1`, etc.).
- `os_kernel` role tests pass.
- Requirements updated (see below).

## Requirements changes

- **§1.4 REQ-KRN-07** — amend wording. Current text bundles "and disabling
  IPv6" into the sysctl requirement. Change to: "…hardening IPv4 networking
  parameters." Remove the "and disabling IPv6" clause; REQ-KRN-02 already
  covers IPv6 disablement via modprobe.
- **§2.3 REQ-KRN-06** — remove or rewrite. Current text: "The `os_kernel`
  role shall disable IPv6 via sysctl on all platforms." This is the requirement
  that directly contradicts REQ-KRN-02. Replace with a cross-reference to
  REQ-KRN-02, or delete and renumber subsequent entries.

## Out of scope

- Making IPv6 disable optional per-host (would be a future task aligned with
  the declarative-capability work in commit `6761f3c`).
- Touching the IPv4 sysctl entries.
- Changing the `Reload Sysctl Changes` task to ignore errors (option 2 from
  the rollout investigation; rejected in favour of removing the contradiction).
