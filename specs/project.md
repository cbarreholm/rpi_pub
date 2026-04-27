# Project Spec: Raspberry Pi (and Generic Debian) Server Automation


## Objective

Provide a repeatable, idempotent Ansible-based process for provisioning and hardening Raspberry Pi servers (and generic Debian hosts) running home-automation and infrastructure services. A secondary goal is to extend SD card lifetime on Raspberry Pi hardware through targeted I/O optimisations.


## Tech Stack

- **Target OS**: Raspberry Pi OS (Bookworm / Bullseye, 64-bit preferred) and generic Debian
- **Automation**: Ansible (playbooks + roles)
- **Secrets**: ansible-vault (encrypted secrets file + vault password file, both git-ignored)
- **Security benchmark**: Lynis (target score > 80)


## Inventory Groups

| Group | Purpose |
|---|---|
| `pi_server` | Raspberry Pi hosts — full RPi-specific hardening |
| `generic_server` | Generic Debian hosts (VPS, NUC, etc.) — platform-agnostic hardening |
| `mi_flora_server` | Hosts that run the Mi Flora MQTT bridge (requires Bluetooth) |
| `http_reverse_proxy_server` | Hosts that run the nginx HTTPS reverse proxy |
| `zigbee2mqtt_server` | Hosts that run Zigbee2MQTT (requires Zigbee adapter) |
| `mosquitto_server` | Hosts that run the Mosquitto MQTT broker |


## Playbooks

| Playbook | Target group | Purpose |
|---|---|---|
| `prepPiServer.yml` | `pi_server` | Full OS hardening for Raspberry Pi |
| `prepGenericHwServer.yml` | `generic_server` | Full OS hardening for generic Debian |
| `prepMosquitto.yml` | `mosquitto_server` | Install/configure Mosquitto MQTT broker |
| `prepZigbee2Mqtt.yml` | `zigbee2mqtt_server` | Install/configure Zigbee2MQTT |
| `prepHttpReverseProxy.yml` | `http_reverse_proxy_server` | Install/configure nginx HTTPS reverse proxy |
| `prepMiFloraServer.yml` | `mi_flora_server` | Install/configure Mi Flora MQTT bridge |


## Roles

| Role | Responsibility |
|---|---|
| `os_users` | Lock `pi` account, create `ssh-users` group, add admin user |
| `os_base` | Timezone, locale, APT config, fstab/swap (RPi only), hostname |
| `os_base_packages` | Install base package set (RPi packages gated to `pi_server`) |
| `os_kernel` | Module blacklisting, sysctl hardening, Kyber I/O scheduler (RPi only), Wi-Fi power saving (RPi only) |
| `os_services` | SSH hardening, UFW firewall, fail2ban, unattended-upgrades, rsyslog |
| `mosquitto` | Mosquitto MQTT broker |
| `zigbee2mqtt` | Zigbee2MQTT service |
| `http_reverse_proxy` | nginx with Let's Encrypt TLS and mutual TLS |
| `mqtt_bridge` | Mi Flora Bluetooth sensor → MQTT bridge |


## Key Design Decisions

### SD Card Longevity (Raspberry Pi)
Minimise writes to extend SD card life:
- `noatime` on all mountpoints
- 30-minute write-commit interval on `/`
- `/tmp`, `/var`, `/var/log`, `/var/tmp` as tmpfs bind mounts
- APT cache redirected to `/tmp/apt`
- Kyber I/O scheduler (optimised for flash storage)

### Platform Gating
RPi-specific tasks (fstab longevity tweaks, swap config, Raspbian APT mirror, `raspberrypi-kernel-headers`, Kyber scheduler, Wi-Fi power saving) are gated on the host being in the `pi_server` group. Generic hosts skip these.

### Peripheral Feature Flags
Hardware capabilities are expressed as per-host boolean variables (`has_bluetooth`, `has_usb`, `has_firewire`, `has_wifi`, `has_zigbee`). Kernel module blacklisting is conditional on these flags so the same role works across varied hardware.

### Secondary Disk
When `secondary_disk_device` is defined for a host, `os_base` detects whether the device exists and has a filesystem, formats with ext4 if needed, mounts at `secondary_disk_mount_path`, and adds a persistent fstab entry.

### HTTPS Reverse Proxy — Two-Phase Deploy
Because a Let's Encrypt certificate must exist before an HTTPS server block can be configured:
1. **Phase 1 (bootstrap)**: Deploy HTTP-only nginx, run `certbot --nginx` for the ACME challenge.
2. **Phase 2 (normal)**: Skip certbot, deploy the HTTPS template directly. Certificate renewal is handled by certbot's own systemd timer.

### Secrets
All passwords, network keys, and MAC addresses are stored in `ansible/secrets/secrets_file.enc` (ansible-vault) and `ansible/secrets/vault_password_file`. Both are git-ignored. Credentials never appear in plaintext in tracked files.

### Passwordless sudo
The Ansible connecting user requires passwordless sudo (compensating control: SSH key-only authentication is enforced). The `os_users` role refuses to run when connected as the `pi` user.


## Prerequisites (before running any playbook)

1. A Raspberry Pi OS or Debian image has been written to the target.
2. SSH is enabled on the target (touch `/boot/ssh` or configured via imager).
3. An alternative admin user with passwordless sudo exists on the target.
4. SSH key-based authentication is configured for that user (`ssh-copy-id`).
5. `ansible/secrets/secrets_file.enc` and `ansible/secrets/vault_password_file` are in place (git-ignored).


## Security Posture

- SSH: key-only, no root login, restricted ciphers/MACs/KEX, `ssh-users` group gate, fail2ban
- Firewall (UFW): default deny in/out; allowlist-only outbound (DNS, NTP, APT mirrors, upstream service IPs)
- Kernel: unused filesystem/protocol/hardware modules blacklisted, sysctl hardening, ASLR enabled, IPv6 disabled
- Updates: unattended security upgrades enabled
- Logging: rsyslog with high-precision timestamps
- Lynis benchmark target: score > 80
