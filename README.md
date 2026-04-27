# Overview
Raspberry Pi Base Setup and Security Hardening

This repository serves to create a repeatable and uniform process in efforts of standardizing a raspbian deployment on one or more Raspberry Pi's. It also is my work in progress for adopting and using ansible to perform these tasks and continued learning. 

See the Features section below and give it a go. 

# Why?
I wanted to learn ansible and enjoy running pihole on two Pi Zero W's. I also test on a RPI3B+. I also wanted to harden and tweak the raspbian OS to achieve a greater level of security. Lynis is the benchmark tool which evaluated my test systems. This ansible playbook will achieve a score just above 80 (Which is pretty good). This is a healthy level that allows for continued expansion and varied use cases which doesn't sacrifice too much security.

A second explicit goal is **extending the life of the SD card**. SD cards have limited write endurance and are the most common point of failure on a Raspberry Pi. Several design decisions in this project directly target reducing unnecessary writes: `noatime` mount options, delayed write commits, keeping transient data in `/tmp`, directing apt cache to `/tmp`, and using the Kyber I/O scheduler which is optimised for flash storage.

# Features
I'll list some features of this repository and ansible setup. This can also be known as "What does this playbook do for me?". 

## OS (Base)
* Setup System Timezone (default: Europe/Stockholm)
* Setup System Localization and Language (default: en_US.UTF-8)
* Setup Keyboard Layout (default: US)
* Configure System Package Manager (apt)
    * Don't acquire extra languages
    * Use IPV4 for downloads
    * Don't Install "Recommends"
    * Don't Install "Suggests"
    * Don't Autoremove "RecommendsImportant"
    * Don't Autoremove "SuggestsImportant"
    * Allow apt to run non-interactively
        * Use --force-confdef
        * Use --force-confold
    * Setup apt cache directory (/tmp/apt) — keeps apt cache off the SD card (SD card longevity)
    * Setup apt cache archive (/var/cache/apt/arhive)
* Setup System fstab file
    * Ensure Security Settings on Mountpoints and Commit (Write) time of 30 Minutes on root partition
    * Uses 'findmnt' to automatically find PARTUUID for /boot and /
    * Mounts the following mountpoints with their own settings
        * /boot - defaults,noatime (SD card longevity: suppresses access-time writes)
        * / - defaults,noatime,commit=1800 (SD card longevity: flushes writes at most every 30 min)
        * /tmp - rw,bind,noatime,nodev,nosuid,noexec (SD card longevity: transient data stays off persistent storage)
        * /opt - rw,bind,noatime,nodev,nosuid
        * /home - rw,bind,noatime,nodev
        * /var - rw,bind,noatime,nodev,nosuid
        * /var/log - rw,bind,noatime,nodev,nosuid,noexec
        * /var/tmp - rw,bind,noatime,nodev,nosuid,noexec
        *  /dev/shm - noatime,noexec,nodev,nosuid
* Setup Systen Swap Size (256MB)

## OS Base Packages
* Install OS Base Packages that enhance the functionality of the system while keeping the package count low
    - aptitude
    - python-apt
    - apt-transport-https
    - raspberrypi-kernel-headers
    - dkms
    - debian-archive-keyring
    - console-data
    - xkbset
    - locales-all
    - dnsutils
    - screen
    - rsync
    - wget
    - curl
    - vim
    - git
    - ttf-mscorefonts-installer
    - iotop

## OS Kernel Tweaks
* Disable Unused Filesystems (Security)
    - cramfs
    - dccp
    - freevxfs
    - hfs
    - hfsplus
    - jffs2
    - rds
    - sctp
    - squashfs
    - tipc
    - udf
* Disable Kernel IPV6 Support (Security)
* Disable Kernel Bluetooth Support (Security)
* Disable Kernel FireWire Support (Security)
* Disable Kernel USB Storage Support (Security)
* Disable Wi-Fi Power Savings (Pi Zero (W) and Non Pi-Zero Models)
* Enable Kernel Hardening via Sysctl Settings (Security)
   * Kernel Randomize VA Space
   * IPV4 Networking Items
   * IPV6 Networking Items 
* Ensure Disable of Wi-Fi PowerSave at Startup for Persistence
* Kernel Scheduler change from deadline to kyber and with Persistence (SD card longevity: Kyber is optimised for flash/NVMe storage)

## OS Services Setups
* Auto Update
   * Automatic updates. Warning! Updates may break the system.
* SSH
   * SSH Security Hardening
* Firewall
   * Local firewall
* nginx
   * HTTPS reverse proxy with Let's Encrypt certificates and mutual TLS (client certificate) authentication
* fail2ban
   * Network security tool that scans log files and bans IP addresses
* RSYSLOG
   * Enable High Precision Timestamping

# Playbooks

| Playbook | Target group | Hardware requirement |
|---|---|---|
| `prepPiServer.yml` | `pi_server` | Raspberry Pi |
| `prepGenericHwServer.yml` | `generic_server` | Any Debian x86/ARM |
| `prepMosquitto.yml` | any | None |
| `prepHttpReverseProxy.yml` | any | None |
| `prepZigbee2Mqtt.yml` | any | Zigbee USB adapter |
| `prepMiFloraServer.yml` | any | Bluetooth hardware |

# Pre-requirements and Assumptions
* Your have burned latest (buster or even bookworm) raspbian (preferably 64 bit) image to SD card
* You have done 'touch /boot/ssh" to enable headless ssh login
* You have set up Wifi with wpa_supplicant.conf or for Bookworm use the imager
  Or add an out of range connection
```
sudo nmcli connection add type wifi con-name TheConnectionName ssid TheSsId 802-11-wireless-security.key-mgmt WPA-PSK 802-11-wireless-security.psk TheSecret
```
* You have created an alternative user with sudo permissions. You should not run as user `pi`, which will be disabled
* You have done 'ssh-copy-id -i ~/.ssh/id_rsa.pub <user>@<your pi's IP address>'
* You can successfully login to <user>@<your pi's IP address> using passwordless (key-based) authentication with no errors.
* You can sucessfully run sudo without as password. Verify by running `sudo visudo`
* OPTIONAL: You have run `apt update` to catch issues such as repos becomming `oldstable`
* OPTIONAL: install NMAP on the host system you run ansible from. This will enable the discoverPi.sh script to help you find your pi on the network.

The first steps can be achieved by configuring those details while burning the OS image.

## Passwordless sudoer
The alternative user needs passwordless sudo permissions, which can be achieved like this (or while burning image):

> **Security note:** Passwordless sudo is an accepted design trade-off. Ansible requires it to run `become` tasks without a vault password. The compensating control is SSH key-only authentication — a compromised session requires a stolen private key, not just a password.


```
USER=myalternativeuser
SUDOERSDFILE=/etc/sudoers.d/099_altuser-nopasswd
echo "$USER ALL=(ALL) NOPASSWD: ALL" > $SUDOERSDFILE
chmod 0440 $SUDOERSDFILE
chown root:root $SUDOERSDFILE    
```

## Generated credentials

Ansible generates a random password for the `pi` user and automatically deletes it from the controller (`credentials/pi/password.txt`) after applying it to the host. The pi account is immediately locked, so the password is never usable. A new random password is generated on each playbook run.

# How To Get This Repository
`git clone git@github.com:cbarreholm/rpi_pub.git`

## Setup
#### Discover your Pi's IP Address on your network
* cd rpi_pub   
* Run ./discoverPi 192.168.1.0/24 (or whatever your network CIDR is)
* View the output file called "inventory.txt" in rpi_pub folder

#### Use the IP that was discovered for your pi as inventory
* edit the rpi_pub/ansible/inventory.yaml file to include the IP that was discovered in the [rpi_server] group. Alternatively add in /etc/hosts

#### Edit the rpi_pub/ansible/prepPiServer.yml file to play with roles and tags, but this is optional and advanced

## Usage
> cd rpi_pub/ansible

> ansible-playbook -i inventory.yaml -e @secrets/secrets_file.enc --vault-password-file secrets/vault_password_file prepPiServer.yml

* Include `-vv` at the end to see more output
* Include `--tags "ssh"` as an example to see it just do the SSH configurations
* Playbooks that use secrets (passwords, network keys, MACs) require the `-e @secrets/secrets_file.enc --vault-password-file` flags — omitting them will result in undefined variables

## References and Sources
* Jeff Geerling - https://www.jeffgeerling.com/
* Lynis Security Auditing Tool - https://cisofy.com/lynis/
* Kyber MultiQueue I/O
    * https://lwn.net/Articles/720071/
    * https://lwn.net/Articles/720675/
* Extending the life of your Raspberry PI SD Card - https://domoticproject.com/extending-life-raspberry-pi-sd-card/
* Raspberry Pi Hardening Guide - https://chrisapproved.com/blog/raspberry-pi-hardening.html

# HTTP Reverse Proxy (prepHttpReverseProxy.yml)

Sets up nginx as an HTTPS reverse proxy with Let's Encrypt TLS and mutual TLS (client certificate) authentication.

## Two-phase deployment

Because the Let's Encrypt certificate must exist before an HTTPS server block can be configured, the playbook uses a two-phase approach:

### Phase 1 — Bootstrap (first run, no certificate yet)

1. Deploys an HTTP-only nginx config so certbot can complete the ACME HTTP-01 challenge.
2. Runs `certbot --nginx` to issue the certificate and reconfigure nginx.
3. If `nginx_site_https` template already exists, renders it to a temp file and diffs it against certbot's config so you can verify they match.
4. **Does not deploy the HTTPS template** — review certbot's resulting config at `/etc/nginx/sites-available/<nginx_site>` on the host and use it to build your `nginx_site_https` template.

### Phase 2 — Normal deploy (certificate exists)

1. Skips HTTP config and certbot entirely.
2. Deploys the HTTPS template (`nginx_site_https`) directly.
3. Certificate renewals are handled automatically by certbot's own systemd timer — independent of Ansible.

### Preview changes before applying

```bash
ansible-playbook --diff --check -i ansible/inventory.yaml -e @ansible/secrets/secrets_file.enc --vault-password-file ansible/secrets/vault_password_file ansible/prepHttpReverseProxy.yml
```

## Required inventory variables

| Variable | Description | Example |
|---|---|---|
| `nginx_site` | HTTP-only bootstrap template filename | `sample-reverse-proxy-bootstrap.conf` |
| `nginx_site_https` | HTTPS template filename | `sample-reverse-proxy-https.conf` |
| `nginx_server_name` | Space-separated list of server names | `app.example.com altname.example.com` |
| `nginx_upstream_ip` | IP of the upstream service | `192.168.1.2` |
| `nginx_upstream_port` | Port of the upstream service | `8080` |
| `nginx_clientca_crt` | Client CA certificate filename (in files/nginx/) | `clientCA.crt` |
| `nginx_certbot_email` | Email for Let's Encrypt notifications | `admin@example.com` |
| `nginx_certbot_domains` | Comma-separated domains for the certificate | `app.example.com,altname.example.com` |
| `nginx_certbot_primary_domain` | First domain in `nginx_certbot_domains`; used as certbot's cert directory name | `app.example.com` |

# Acknowledgement
This repo is a fork of https://github.com/raajivrekha/rpi_pub created by Raajiv Rekha
