# Requirements

> **Coverage note**: This document is intended to capture all system requirements,
> both existing and new. The baseline RPi requirements (Section 1) have not yet been
> fully documented — this is a known gap and a TODO. Requirements in Section 2 onwards
> reflect the addition of generic Debian platform support and are complete.

---

## 1. Raspberry Pi Baseline

### 1.1 Pre-conditions

REQ-PRE-01: The `os_users` role shall refuse to execute when Ansible is connected as the `pi` user, requiring an alternative user with passwordless sudo to be created before running.

REQ-PRE-02: The target host shall have SSH key-based authentication configured for the connecting user before the playbook is run.

### 1.2 OS Base

REQ-BASE-01: The `os_base` role shall configure the system timezone to the value of `config_timezone`.

REQ-BASE-02: The `os_base` role shall ensure the system locale specified by `config_system_locale` is available and active.

REQ-BASE-03: The `os_base` role shall ensure the system language specified by `config_system_language` is available and active.

REQ-BASE-04: The `os_base` role shall configure the keyboard layout to the value of `config_keyboard_layout`.

REQ-BASE-05: The `os_base` role shall configure APT to suppress installation of recommended and suggested packages.

REQ-BASE-06: The `os_base` role shall configure APT to use IPv4 for package downloads.

REQ-BASE-07: The `os_base` role shall configure APT to suppress language file downloads.

REQ-BASE-08: The `os_base` role shall configure APT to run non-interactively, preserving existing configuration files on conflict.

REQ-BASE-09: The `os_base` role shall configure the APT package cache to use `/tmp/apt` to avoid persistent writes to the SD card.

REQ-BASE-10: The `os_base` role shall configure `/etc/fstab` with SD card longevity optimisations, including `noatime` on all mountpoints, a 30-minute write commit interval on `/`, and tmpfs bind mounts for `/tmp`, `/var`, `/var/log`, `/var/tmp`, `/opt`, `/home`, and `/dev/shm`.

REQ-BASE-11: The `os_base` role shall configure swap to 256 MB using `dphys-swapfile`.

REQ-BASE-12: The `os_base` role shall set the system hostname to the value of `config_system_hostname`.

REQ-BASE-13: The `os_base` role shall update `/etc/hosts` to replace the `raspberrypi` hostname entry with `config_system_hostname`.

REQ-BASE-14: The `os_base` role shall configure the Raspbian APT mirror to the value of `config_apt_mirror_url`.

### 1.3 OS Base Packages

REQ-PKG-01: The `os_base_packages` role shall install a defined set of base packages including: `aptitude`, `dkms`, `xkbset`, `dnsutils`, `screen`, `python3-apt`, `raspberrypi-kernel-headers`, `debian-archive-keyring`, `locales-all`, `rsync`, `wget`, `curl`, `vim`, `git`, `ttf-mscorefonts-installer`, and `iotop`.

### 1.4 Kernel

REQ-KRN-01: The `os_kernel` role shall blacklist unused filesystem kernel modules: `cramfs`, `dccp`, `freevxfs`, `hfs`, `hfsplus`, `jffs2`, `rds`, `sctp`, `squashfs`, `tipc`, and `udf`.

REQ-KRN-02: The `os_kernel` role shall blacklist the IPv6 kernel module.

REQ-KRN-03: While `has_bluetooth` is false for a host, the `os_kernel` role shall blacklist Bluetooth kernel modules.

REQ-KRN-04: The `os_kernel` role shall blacklist FireWire kernel modules.

REQ-KRN-05: The `os_kernel` role shall blacklist the USB storage kernel module.

REQ-KRN-06: The `os_kernel` role shall disable Wi-Fi power saving for Realtek Wi-Fi modules.

REQ-KRN-07: The `os_kernel` role shall apply sysctl kernel hardening settings, including: disabling SUID core dumps, enabling address space layout randomisation, hardening IPv4 and IPv6 networking parameters, and disabling IPv6.

REQ-KRN-08: The `os_kernel` role shall configure the Kyber I/O scheduler for the SD card block device (`mmcblk0`) persistently across reboots.

### 1.5 User Management

REQ-USR-01: The `os_users` role shall set a randomly generated password on the `pi` user and immediately lock the account.

REQ-USR-02: The `os_users` role shall delete the generated `pi` password file from the Ansible controller after applying it to the host.

REQ-USR-03: The `os_users` role shall create an `ssh-users` group.

REQ-USR-04: The `os_users` role shall add the connecting user to the `ssh-users` group.

### 1.6 SSH

REQ-SSH-01: The `os_services` SSH configuration shall disable password authentication, requiring key-based authentication only.

REQ-SSH-02: The `os_services` SSH configuration shall deny root login.

REQ-SSH-03: The `os_services` SSH configuration shall restrict SSH access to members of the `ssh-users` group.

REQ-SSH-04: The `os_services` SSH configuration shall listen on IPv4 only.

REQ-SSH-05: The `os_services` SSH configuration shall disable TCP forwarding, agent forwarding, and X11 forwarding.

REQ-SSH-06: The `os_services` SSH configuration shall restrict ciphers, MACs, and key exchange algorithms to a modern approved set.

REQ-SSH-07: The `os_services` SSH configuration shall limit authentication attempts to 3 and concurrent sessions to 2.

REQ-SSH-08: The `os_services` SSH configuration shall set log level to VERBOSE to ensure authentication failures are visible to fail2ban.

### 1.7 Firewall

REQ-FW-01: The `os_services` firewall configuration shall default to deny all incoming and outgoing traffic.

REQ-FW-02: The `os_services` firewall configuration shall allow inbound SSH with rate limiting.

REQ-FW-03: While `firewall_inbound_http_port` is set, the `os_services` firewall configuration shall allow inbound TCP traffic on that port.

REQ-FW-04: While `firewall_inbound_https_port` is set, the `os_services` firewall configuration shall allow inbound TCP traffic on that port.

REQ-FW-05: While `firewall_inbound_mqtt_port` is set, the `os_services` firewall configuration shall allow inbound TCP traffic on that port.

REQ-FW-06: The `os_services` firewall configuration shall allow outbound DNS (UDP and TCP) to the IPs specified in `firewall_outbound_dns_ips`.

REQ-FW-07: The `os_services` firewall configuration shall allow outbound HTTP to the IPs specified in `config_firewall_apt_update_ips` to enable APT updates.

REQ-FW-08: The `os_services` firewall configuration shall allow outbound NTP (UDP) to the IPs specified in `config_firewall_ntp_ips`.

REQ-FW-09: The `os_services` firewall configuration shall allow outbound HTTPS to the IPs specified in `config_firewall_letsencrypt_ips` to enable certificate renewal.

REQ-FW-10: While `firewall_outbound_upstream_ip` is set to a non-loopback address, the `os_services` firewall configuration shall allow outbound TCP traffic to that IP and port.

### 1.8 Unattended Upgrades

REQ-UPD-01: The `os_services` role shall install and configure `unattended-upgrades` to automatically apply security updates.

### 1.9 fail2ban

REQ-F2B-01: The `os_services` role shall install and configure fail2ban with jails for SSH and nginx.

### 1.10 rsyslog

REQ-LOG-01: The `os_services` role shall install rsyslog and configure it to use high-precision timestamps.

---

## 2. Generic Debian Platform Support

### Scope

Extend the existing Raspberry Pi hardening automation to support generic Debian hosts
(VPS, Intel NUC, or similar x86/ARM hardware). A single codebase shall serve both
platform types, with platform-specific behaviour gated by host variables and playbook
selection.

### 2.1 Platform Targeting

REQ-PLT-01: The inventory shall support a `generic_server` host group for non-Raspberry Pi Debian hosts alongside the existing `pi_server` group.

REQ-PLT-02: The playbooks shall apply RPi-specific roles and tasks only to hosts in the `pi_server` group.

### 2.2 User Management

REQ-USR-01: The `os_users` role shall use a per-host `ansible_user` variable as the initial connection user, allowing different default users per host (e.g. `pi` on Raspberry Pi, `debian` on VPS images).

REQ-USR-02: The `os_users` role shall configure the administrative user account using a per-host variable, allowing different admin usernames per host.

### 2.3 Kernel Module Blacklisting

REQ-KRN-01: While `has_bluetooth` is false for a host, the `os_kernel` role shall blacklist Bluetooth kernel modules.

REQ-KRN-02: While `has_usb` is false for a host, the `os_kernel` role shall blacklist the USB storage kernel module.

REQ-KRN-03: While `has_firewire` is false for a host, the `os_kernel` role shall blacklist FireWire kernel modules.

REQ-KRN-04: While `has_wifi` is false for a host, the `os_kernel` role shall blacklist Wi-Fi kernel modules.

REQ-KRN-05: The `os_kernel` role shall apply sysctl kernel hardening settings on all platforms.

REQ-KRN-06: The `os_kernel` role shall disable IPv6 via sysctl on all platforms.

REQ-KRN-07: While the host is in the `pi_server` group, the `os_kernel` role shall configure the Kyber I/O scheduler for the SD card block device.

REQ-KRN-08: While the host is in the `pi_server` group, the `os_kernel` role shall configure Wi-Fi power saving settings.

### 2.4 OS Base Configuration

REQ-BASE-01: While the host is in the `pi_server` group, the `os_base` role shall configure `/etc/fstab` with SD card longevity optimisations (noatime, commit=1800, tmpfs bind mounts for /tmp, /var, /opt, /home).

REQ-BASE-02: While the host is in the `generic_server` group, the `os_base` role shall not modify `/etc/fstab`.

REQ-BASE-03: While the host is in the `pi_server` group, the `os_base` role shall configure `dphys-swapfile` with a 256 MB swap size.

REQ-BASE-04: While the host is in the `generic_server` group, the `os_base` role shall not configure swap.

REQ-BASE-05: The `os_base` role shall set the system hostname to the value of `config_system_hostname` on all platforms.

REQ-BASE-06: While the host is in the `pi_server` group, the `os_base` role shall update `/etc/hosts` to replace the `raspberrypi` hostname entry with `config_system_hostname`.

REQ-BASE-07: While the host is in the `generic_server` group, the `os_base` role shall not modify `/etc/hosts`.

REQ-BASE-08: While the host is in the `pi_server` group, the `os_base` role shall configure the Raspbian APT mirror using the `config_apt_mirror_url` variable.

REQ-BASE-09: While the host is in the `generic_server` group, the `os_base` role shall not modify APT sources.

### 2.5 Base Packages

REQ-PKG-01: While the host is in the `pi_server` group, the `os_base_packages` role shall install Raspberry Pi specific packages including `raspberrypi-kernel-headers`.

REQ-PKG-02: While the host is in the `generic_server` group, the `os_base_packages` role shall not install Raspberry Pi specific packages.

### 2.6 Secondary Disk

REQ-DSK-01: While `secondary_disk_device` is defined for a host, when the device exists and has no filesystem, the `os_base` role shall format the device with ext4 and mount it at `secondary_disk_mount_path`.

REQ-DSK-02: While `secondary_disk_device` is defined for a host, when the device exists and already has a filesystem, the `os_base` role shall mount it at `secondary_disk_mount_path` without formatting.

REQ-DSK-03: While `secondary_disk_device` is defined for a host, when the device does not exist on the host, the `os_base` role shall fail with a descriptive error message.

REQ-DSK-04: While `secondary_disk_device` is defined for a host and the disk is successfully mounted, the `os_base` role shall add a persistent fstab entry for the mount.

REQ-DSK-05: While `secondary_disk_device` is not defined for a host, the `os_base` role shall skip all secondary disk configuration.

### 2.7 Firewall

REQ-FW-01: The `os_services` firewall configuration shall default to deny all incoming and outgoing traffic on all platforms.

REQ-FW-02: The `os_services` firewall configuration shall allow SSH with rate limiting on all platforms.

### 2.8 Playbook Naming and Selection

REQ-PLY-01: The existing `prepPi.yml` playbook shall be renamed to `prepPiServer.yml`.

REQ-PLY-02: A new `prepGenericHwServer.yml` playbook shall be created for base hardening of generic Debian hosts.

REQ-PLY-03: The existing `prepPiMosquitto.yml` playbook shall be renamed to `prepMosquitto.yml`.

REQ-PLY-04: The existing `prepPiHttpReverseProxy.yml` playbook shall be renamed to `prepHttpReverseProxy.yml`.

REQ-PLY-05: The existing `prepPiZigbee2Mqtt.yml` playbook shall be renamed to `prepZigbee2Mqtt.yml`.

REQ-PLY-06: The existing `prepPiMiFloraServer.yml` playbook shall be renamed to `prepMiFloraServer.yml`.

REQ-PLY-07: The `prepZigbee2Mqtt.yml` playbook shall only be applicable to hosts with a Zigbee hardware adapter available.

REQ-PLY-08: The `prepMiFloraServer.yml` playbook shall only be applicable to hosts with Bluetooth hardware available.

REQ-PLY-09: The `prepMosquitto.yml` playbook shall be applicable on all platforms.

REQ-PLY-10: The `prepHttpReverseProxy.yml` playbook shall be applicable on all platforms.
