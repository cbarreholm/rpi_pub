# Task 22 — Gate fail2ban nginx Jails to Hosts Running nginx

**Type:** Bug fix
**Requirements:** §1.9 REQ-F2B-01 (refinement)

## Background

`ansible/roles/os_services/files/fail2ban/jail.local` unconditionally enables
three nginx-related jails (`nginx-botsearch`, `nginx-noscript`,
`nginx-badbots`) on every host that runs `os_services`. On hosts without
nginx (e.g. `miflora`, `zigbee2mqtt`, `mosquitto`, and any pi_server before
the `http_reverse_proxy` role has run), fail2ban crashes at start:

```
[fail2ban-server] ERROR  Failed during configuration: Have not found any log file for nginx-botsearch jail
[fail2ban-server] ERROR  Async configuration of server failed
systemd[1]: fail2ban.service: Failed with result 'exit-code'.
```

Observed in `<host>` syslog 2026-05-11 (recurring on every boot since the
fail2ban tag was applied).

## Goal

Enable the nginx jails **only** on hosts that actually run nginx. All other
hosts should get the SSH jail only.

## Approach (pick one during implementation)

1. **Template `jail.local`** — convert `files/fail2ban/jail.local` to
   `templates/jail.local.j2`, gate each nginx jail block on a fact like
   `inventory_hostname in groups['http_reverse_proxy_server']` or a
   per-host `runs_nginx: true` flag.
2. **Split into per-feature drop-ins** — keep `jail.local` minimal (sshd
   only) and ship nginx jails in a separate file, dropped only by the
   `http_reverse_proxy` role (or by a conditional task in os_services).

Either is acceptable. Option 2 is cleaner separation of concerns since the
nginx jails logically belong with the role that installs nginx.

## Tests (write first)

1. Assert that on a host **not** in `http_reverse_proxy_server`, the
   rendered fail2ban config contains the `[sshd]` jail enabled and the
   nginx jails either absent or disabled.
2. Assert that on a host **in** `http_reverse_proxy_server`, the nginx
   jails are present and enabled.
3. Assert that no static `files/fail2ban/jail.local` ships with
   unconditionally enabled nginx jails.

Run with: `python -m unittest discover -s ansible/roles/os_services/tests -p "test_fail2ban_jail_gating.py" -v`

## Acceptance

- `fail2ban.service` starts cleanly on `miflora`, `zigbee2mqtt`, `mosquitto`.
- `fail2ban.service` starts cleanly on `reverseproxy` after the
  `http_reverse_proxy` role has run.
- Existing SSH jail behaviour unchanged on all hosts.
- README updated if the design splits config across roles.

## Out of scope

- Tuning ban times, max retries, or filter regexes.
- Adding new jails.
- Migrating to fail2ban v1.x configuration syntax (separate concern).
