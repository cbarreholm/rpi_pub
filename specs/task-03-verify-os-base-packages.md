# Task 03 — Verify OS Base Packages

**Type:** Verification
**Requirements:** §1.3 REQ-PKG-01

## What to verify

File: `ansible/roles/os_base_packages/tasks/main.yml`

### REQ-PKG-01 — Base package list
Confirm the Debian 12 package task includes all of the following:
- `aptitude`
- `dkms`
- `xkbset`
- `dnsutils`
- `screen`
- `python3-apt`
- `raspberrypi-kernel-headers`
- `debian-archive-keyring`
- `locales-all`
- `rsync`
- `wget`
- `curl`
- `vim`
- `git`
- `ttf-mscorefonts-installer`
- `iotop`

## Pass criteria
All packages listed in REQ-PKG-01 are present in the task.
Any gap must be noted and a follow-up task created.
