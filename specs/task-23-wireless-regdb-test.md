# Task 23 — Document and Test wireless-regdb on Trixie pi_server Hosts

**Type:** Test backfill + requirement documentation
**Requirements:** §1.3 (new REQ-PKG-02 for wireless regulatory database)

## Background

On Debian 13 (Trixie) pi_server hosts using Wi-Fi the kernel logs at boot:

```
platform regulatory.0: Direct firmware load for regulatory.db failed with error -2
cfg80211: failed to load regulatory.db
```

Cause: the Trixie RPi OS image does not pull in the `wireless-regdb` package
by default. Without `/lib/firmware/regulatory.db` the kernel falls back to
the most restrictive "world" regulatory domain, restricting channels and
TX power.

The fix has already been applied: `wireless-regdb` was added to the
"Install OS Base RPi Packages Debian 13" task in
`ansible/roles/os_base_packages/tasks/main.yml`. This task backfills the
test (which should have been written first per AGENTS.md workflow) and
records the requirement.

## Changes required

### 1. Requirement (add to `specs/requirements.md` §1.3)

> REQ-PKG-02: On Debian 13 pi_server hosts, the `os_base_packages` role
> shall install `wireless-regdb` to provide the kernel regulatory database
> (`/lib/firmware/regulatory.db`) required for cfg80211 / Wi-Fi operation.

### 2. Test

Add `ansible/roles/os_base_packages/tests/test_wireless_regdb.py` using
`unittest` + `pyyaml` (pytest not installed). Assertions:

- Locate the task named `Install OS Base RPi Packages Debian 13` in
  `ansible/roles/os_base_packages/tasks/main.yml`.
- `wireless-regdb` is present in the task's `vars.packages` list.
- The task's `when:` includes both
  `ansible_distribution_major_version == "13"` and
  `inventory_hostname in groups['pi_server']`.

Run with:
```
python -m unittest discover -s ansible/roles/os_base_packages/tests -p "test_wireless_regdb.py" -v
```

## Acceptance

- New REQ-PKG-02 added to `specs/requirements.md` §1.3.
- New test passes against the current state of
  `os_base_packages/tasks/main.yml`.
- No behaviour change (package already added).

## Out of scope

- Installing `wireless-regdb` on Debian 10/12 (already pulled in by other
  dependencies on those releases; not validated here).
- Installing on `generic_server` hosts (out of pi_server scope).
