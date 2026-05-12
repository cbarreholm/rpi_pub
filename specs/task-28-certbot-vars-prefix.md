# Task 28 — Wire certbot variables and adopt group-prefixed vault names

**Type:** Bug fix / hygiene
**Requirements:** §1.8 (refinement — first-deploy hardening, same bring-up
sequence as Tasks 26–27)

## Background

The 2026-05-12 fresh bring-up of `prepHttpReverseProxy.yml` against a
freshly-flashed Trixie `reverseproxy` host (after Task 27 unblocked the
apt step) fails at the second relevant task:

```
TASK [http_reverse_proxy : Check if Let's Encrypt certificate exists] **
fatal: [reverseproxy]: FAILED! => "nginx_certbot_primary_domain is undefined"
```

Two related issues surfaced:

1. **`nginx_certbot_primary_domain` is never defined.** Only present as
   a commented-out example in `roles/http_reverse_proxy/vars/main.yml`.
   The role uses it as the certbot live-cert directory name
   (`/etc/letsencrypt/live/<primary>/fullchain.pem`).
2. **`nginx_certbot_email` is defined only as a flat vault entry
   (`nginx_certbot_email: <addr>`)**, loaded as a global extra-var via
   `-e @ansible/secrets/secrets_file.enc`. It works today only because
   the vault key name happens to match the role-side Jinja reference.
   No inventory aliasing, no group scoping — inconsistent with the
   pattern used for `nginx_certbot_domains` and `nginx_server_name`
   (`inventory.yaml:59-60`), which both reference group-prefixed vault
   entries (`http_reverse_proxy_server_*`).

The pattern across the inventory is: short alias visible to the role,
long group-prefixed name in the vault. Scoping by group keeps unrelated
groups from accidentally colliding on flat names like
`nginx_certbot_email`.

## Goal

`prepHttpReverseProxy.yml` shall complete the cert_stat → bootstrap →
certbot sequence on a freshly-flashed Trixie host without manual
variable injection, and the vault entry naming shall be consistent with
the established `<group>_<varname>` convention.

## Approach

**Role-side change** (`vars/main.yml`): replace the commented example
with a real derivation:

```yaml
nginx_certbot_primary_domain: "{{ nginx_certbot_domains.split(',')[0] | trim }}"
```

Single source of truth — no drift between primary_domain and "first
entry of domains". No new secret.

**Inventory-side change** (`inventory.yaml` + `inventory.yaml.example`):
add a line under the `http_reverse_proxy_server` group:

```yaml
nginx_certbot_email: "{{http_reverse_proxy_server_nginx_certbot_email}}"
```

**Vault-side change** (operator action, not committed via Ansible):
rename the existing flat `nginx_certbot_email` entry to
`http_reverse_proxy_server_nginx_certbot_email`. Done via
`ansible-vault edit ansible/secrets/secrets_file.enc`.

Why not the alternatives:

- **Add `nginx_certbot_primary_domain` as a separate vault entry** —
  duplicates info already present in `nginx_certbot_domains`. Drift
  risk if someone later changes the domain list and forgets the primary.
- **Leave `nginx_certbot_email` as a flat vault entry** — works, but
  inconsistent with the rest of the file and couples the role
  implicitly to a global namespace. Future addition of another role
  that also needs a `nginx_certbot_email` would silently collide.
- **Adopt `var-naming[no-role-prefix]` repo-wide** — would mean renaming
  many `nginx_*` and `config_*` vars across roles and inventory. That
  is a separate refactor (66 pre-existing lint hits per
  `memory/learnings.md`) and is out of scope for this bug fix.

## Tests (write first)

`ansible/roles/http_reverse_proxy/tests/test_certbot_primary_domain_derivation.py`
asserting on `vars/main.yml`:

1. `nginx_certbot_primary_domain` is defined as a real (uncommented) key.
2. Its value is a Jinja expression that:
   - References `nginx_certbot_domains`.
   - Splits on `','` and indexes `[0]`.
   - Pipes through `trim` to tolerate `"a.example.com, b.example.com"`
     style spacing.
3. No commented-out `nginx_certbot_primary_domain:` stub remains (avoid
   confusion between active and legacy definitions).

Inventory wiring is verified by playbook syntax-check + a successful
re-run of `prepHttpReverseProxy.yml` against `reverseproxy`. No
machine-checkable test for inventory content (it's site-specific
configuration).

Run with:

```
python -m unittest discover -s ansible/roles/http_reverse_proxy/tests \
    -p "test_certbot_primary_domain_derivation.py" -v
```

## Acceptance

- `prepHttpReverseProxy.yml --syntax-check` passes.
- After the operator renames the vault entry, running the playbook
  against `reverseproxy` reaches the certbot bootstrap step (no more
  `'nginx_certbot_primary_domain' is undefined` or
  `'nginx_certbot_email' is undefined`).
- `nginx -T` post-bootstrap shows the Let's Encrypt cert path matches
  the first domain in `nginx_certbot_domains`.
- `ansible-lint ansible/roles/http_reverse_proxy/vars/main.yml`
  reports `nginx_certbot_primary_domain` under `var-naming[no-role-prefix]`,
  same rule as the pre-existing hit on the adjacent
  `config_nginx_site_src_dir`. Total role-vars violations: 1 → 2 (+1).
  Repo-wide rename is out of scope; the new var follows the same
  no-role-prefix pattern as the rest of the role.

## Out of scope

- Renaming all role-internal vars to use the `http_reverse_proxy_`
  prefix that ansible-lint's `var-naming[no-role-prefix]` would prefer.
  Separate refactor.
- Templating the HTTPS site config (`nginx_site_https`) — that is the
  separate post-bootstrap step already present in the role.
- Rotating the certbot account email or the Let's Encrypt cert itself
  — the rename leaves the secret value unchanged.
