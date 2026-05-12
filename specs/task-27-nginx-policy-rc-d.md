# Task 27 — Prevent nginx postinst auto-start on IPv6-disabled hosts

**Type:** Bug fix
**Requirements:** §1.8 (refinement — same "no installed-by-default service
in `failed` state" intent as Task 26, applied to the `http_reverse_proxy`
role)

## Background

`prepHttpReverseProxy.yml` fails on a freshly-flashed Trixie host at the
very first task, `http_reverse_proxy : Install nginx package`. The
`nginx` package's `postinst` script invokes `invoke-rc.d nginx start`
immediately after unpack, before the role has a chance to swap in its
own configuration. The stock `/etc/nginx/sites-enabled/default` shipped
by `nginx-common` contains:

```
listen [::]:80 default_server;
```

`os_kernel` blacklists the `ipv6` module (REQ-KRN-02), so the kernel
returns `EAFNOSUPPORT (97)` for any `AF_INET6` socket. nginx fails its
config test, the postinst exits non-zero, and dpkg leaves `nginx` and
`python3-certbot-nginx` in `iU` (unpacked-but-unconfigured) state:

```
nginx: [emerg] socket() [::]:80 failed (97: Address family not supported by protocol)
dpkg: error processing package nginx (--configure):
 installed nginx package post-installation script subprocess returned error
dpkg: error processing package python3-certbot-nginx (--configure):
 dependency problems - leaving unconfigured
```

This is the same class of bug as Task 26 (default exim4 failing to bind
IPv6) but surfaced as an apt failure rather than a `--failed` unit,
because the failure happens during package configuration.

The role already handles the stock default site correctly *after* apt
finishes: there is an existing "Remove default site" task followed by
deployment of the role's own IPv4-only templates. The fix is only to
get past the postinst.

## Goal

`prepHttpReverseProxy.yml` shall complete cleanly on a freshly-flashed
IPv6-disabled Trixie host without manual intervention. The role's own
templates remain authoritative for the running configuration.

## Approach

Use the Debian-blessed `policy-rc.d` mechanism: drop a
`/usr/sbin/policy-rc.d` shim that exits 101 (deny) immediately before
the apt task, and remove it immediately after. `invoke-rc.d` consults
this shim and skips the auto-start, leaving the package in `ii`
(installed-configured) state. The role's subsequent "Remove default
site" / "Deploy …" / "Restart nginx" sequence then brings nginx up
with its IPv4-only config as today.

Why not the alternatives:

- **Mask `nginx.service` before install** — works, but requires an
  unmask step and a separate enable. More moving parts than the
  policy-rc.d shim, which is purpose-built for exactly this situation.
- **Patch `/etc/nginx/sites-enabled/default` post-unpack but
  pre-configure** — fragile; would need to hook between `apt-get`
  phases.
- **Re-enable IPv6** — contradicts Task 25 / REQ-KRN-02.

## Tests (write first)

`ansible/roles/http_reverse_proxy/tests/test_nginx_install_no_autostart.py`
asserting on `tasks/nginx.yml`:

1. A task that writes `/usr/sbin/policy-rc.d` exists and:
   - Uses `ansible.builtin.copy`.
   - Sets `mode: '0755'`.
   - Content matches `#!/bin/sh\nexit 101\n` (literal).
2. A task that removes `/usr/sbin/policy-rc.d` exists and uses
   `ansible.builtin.file` with `state: absent`.
3. The policy-rc.d copy task appears strictly before the existing
   "Install nginx package" task (ordering matters — must run before
   apt).
4. The policy-rc.d removal task appears strictly after the apt install
   task (also ordering-critical; the shim must be lifted before the
   role's later "Restart nginx" handler fires).
5. Both new tasks use `become: true`.

Run with:

```
python -m unittest discover -s ansible/roles/http_reverse_proxy/tests \
    -p "test_nginx_install_no_autostart.py" -v
```

## Acceptance

- `prepHttpReverseProxy.yml` against a freshly-flashed Trixie
  `reverseproxy` host runs to completion without manual intervention.
- After the playbook completes, `dpkg -l nginx python3-certbot-nginx`
  reports both packages as `ii`, `systemctl is-active nginx` reports
  `active`, and `nginx -T` shows only the role's IPv4-only config (no
  `listen [::]:80`).
- The playbook is idempotent: a second run reports the apt task as
  `ok` (already installed) and the policy-rc.d tasks as `changed`
  only on the first run, or both runs benignly (acceptable either
  way since the shim is short-lived and not security-sensitive when
  it briefly exists during the apt task).
- `specs/requirements.md` §1.8 already covers this under Task 26's
  "no failed services" refinement; no new REQ-* needed.

## Out of scope

- Changing how IPv6 is disabled (Task 25 settled this).
- Refactoring the rest of `nginx.yml` (certbot bootstrap, HTTPS
  template deploy, etc.) — only the install task and its surroundings
  are touched.
- Generalising the policy-rc.d pattern into a reusable role helper.
  If a second role hits the same issue (e.g. mosquitto on IPv6 binds),
  promote at that point.
