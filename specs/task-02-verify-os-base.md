# Task 02 — Verify OS Base Configuration

**Type:** Verification
**Requirements:** §1.2 REQ-BASE-01 – REQ-BASE-14

## What to verify

File: `ansible/roles/os_base/tasks/main.yml`
Templates: `ansible/roles/os_base/templates/`

### REQ-BASE-01 — Timezone
- Confirm a `timezone` task is present using `config_timezone`.

### REQ-BASE-02 & REQ-BASE-03 — Locale and language
- Confirm two `locale_gen` tasks are present: one for `config_system_locale`, one for `config_system_language`.
- Confirm a `localectl set-locale` command task sets both values.

### REQ-BASE-04 — Keyboard layout
- Confirm a `lineinfile` task targets `/etc/default/keyboard` and sets `XKBLAYOUT` to `config_keyboard_layout`.

### REQ-BASE-05 — APT suppress recommends and suggests
- Confirm `/etc/apt/apt.conf.d/99-custom-configs` is deployed with:
  - `APT::Install-Recommends "false"`
  - `APT::Install-Suggests "false"`
  - `APT::AutoRemove::RecommendsImportant "false"`
  - `APT::AutoRemove::SuggestsImportant "false"`

### REQ-BASE-06 — APT force IPv4
- Confirm the same config file includes `Acquire::ForceIPv4 "true"`.

### REQ-BASE-07 — APT suppress language downloads
- Confirm the same config file includes `Acquire::Languages "none"`.

### REQ-BASE-08 — APT non-interactive
- Confirm the same config file includes `--force-confdef` and `--force-confold` dpkg options.

### REQ-BASE-09 — APT cache to /tmp
- Confirm `/etc/apt/apt.conf.d/99-custom-cache` is deployed with `Dir::Cache "/tmp/apt"`.

### REQ-BASE-10 — fstab with SD card longevity optimisations
- Confirm a `template` task deploys a versioned fstab template.
- Confirm `Debian-12.fstab.j2` contains:
  - `noatime` on all mountpoints
  - `commit=1800` on the root partition
  - tmpfs bind mounts for `/tmp`, `/var`, `/var/log`, `/var/tmp`, `/opt`, `/home`, `/dev/shm`

### REQ-BASE-11 — Swap 256 MB
- Confirm a `lineinfile` task sets `CONF_SWAPSIZE=256` in `/etc/dphys-swapfile`.

### REQ-BASE-12 — Hostname via hostnamectl
- Confirm an `ansible.builtin.hostname` task uses `config_system_hostname`.

### REQ-BASE-13 — /etc/hosts hostname replacement
- Confirm a `replace` task targets `/etc/hosts` and replaces `raspberrypi` with `config_system_hostname`.

### REQ-BASE-14 — Raspbian APT mirror
- Confirm a `replace` task updates `/etc/apt/sources.list` with `config_apt_mirror_url`.

## Pass criteria
All checks pass with no code changes required.
Any gap must be noted and a follow-up task created.
