# Task 08 — Verify Services (Unattended Upgrades, fail2ban, rsyslog)

**Type:** Verification
**Requirements:** §1.8 REQ-UPD-01, §1.9 REQ-F2B-01, §1.10 REQ-LOG-01

## What to verify

### REQ-UPD-01 — Unattended upgrades installed and configured
File: `ansible/roles/os_services/tasks/autoupdate.yml`

- Confirm `unattended-upgrades` is installed.
- Confirm `apt-listchanges` and `apticron` are installed.
- Confirm a configuration file (`50unattended-upgrades`) is deployed to
  `/etc/apt/apt.conf.d/`.

### REQ-F2B-01 — fail2ban with SSH and nginx jails
File: `ansible/roles/os_services/tasks/fail2ban.yml`

- Confirm `fail2ban` is installed.
- Confirm `jail.local` is deployed to `/etc/fail2ban/`.
- Confirm `nginx-noscript.conf` is deployed to `/etc/fail2ban/filter.d/`.
- Confirm a symlink from `apache-badbots.conf` to `nginx-badbots.conf` is created.
- Open `ansible/roles/os_services/files/fail2ban/jail.local` and confirm it
  enables jails for `sshd` and at least one nginx jail.

### REQ-LOG-01 — rsyslog with high-precision timestamps
File: `ansible/roles/os_services/tasks/rsyslog.yml`

- Confirm `rsyslog` is installed.
- Confirm a `lineinfile` task enables `$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat`
  in `/etc/rsyslog.conf`.

## Pass criteria
All checks pass with no code changes required.
Any gap must be noted and a follow-up task created.
