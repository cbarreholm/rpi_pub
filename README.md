# Overview
Raspberry Pi Base Setup and Security Hardening

This repository serves to create a repeatable and uniform process in efforts of standardizing a raspbian deployment on one or more Raspberry Pi's. It also is my work in progress for adopting and using ansible to perform these tasks and continued learning. 

See the Features section below and give it a go. 

# Why?
I wanted to learn ansible and enjoy running pihole on two Pi Zero W's. I also test on a RPI3B+. I also wanted to harden and tweak the raspbian OS to achieve a greater level of security. Lynis is the benchmark tool which evaluated my test systems. This ansible playbook will achieve a score just above 80 (Which is pretty good). This is a healthy level that allows for continued expansion and varied use cases which doesn't sacrifice too much security.

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
    * Setup apt cache directory (/tmp/apt)
    * Setup apt cache archive (/var/cache/apt/arhive)
* Setup System fstab file
    * Ensure Security Settings on Mountpoints and Commit (Write) time of 30 Minutes on root partition
    * Uses 'findmnt' to automatically find PARTUUID for /boot and /
    * Mounts the following mountpoints with their own settings
        * /boot - defaults,noatime
        * / - defaults,noatime,commit=1800
        * /tmp - rw,bind,noatime,nodev,nosuid,noexec
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
* Kernel Scheduler change from deadline to kyber and with Persistence

## OS Services Setups
* Auto Update
   * Automatic updates. Warning! Updates may break the system.
* SSH
   * SSH Security Hardening
* Firewall
   * Local firewall
* nginx
   * Light weight web server including Let's Encrypt certificates
* fail2ban
   * Network security tool that scans log files and bans IP addresses
* RSYSLOG
   * Enable High Precision Timestamping

# Pre-requirements and Assumptions
* Your have burned latest raspbian (buster) image to SD card
* You have done 'touch /boot/ssh" to enable headless ssh login
* You have created an alternative user with sudo permissions. You should not run as user `pi`, which will be disabled
* You have done 'ssh-copy-id -i ~/.ssh/id_rsa.pub <user>@<your pi's IP address>'
* You can successfully login to <user>@<your pi's IP address> using passwordless (key-based) authentication with no errors.
* You can sucessfully run sudo without as password. Verify by running `sudo visudo`
* OPTIONAL: You have run `apt update` to catch issues such as repos becomming `oldstable`
* OPTIONAL: install NMAP on the host system you run ansible from. This will enable the discoverPi.sh script to help you find your pi on the network.

## Passwordless sudoer
The alternative user needs passwordless sudo permissions, which can be achieved like this 

```
USER=myalternativeuser
SUDOERSDFILE=/etc/sudoers.d/099_altuser-nopasswd
echo "$USER ALL=(ALL) NOPASSWD: ALL" > $SUDOERSDFILE
chmod 0440 $SUDOERSDFILE
chown root:root $SUDOERSDFILE    
```

# How To Get This Repository
`git clone git@github.com:cbarreholm/rpi_pub.git`

## Setup
#### Discover your Pi's IP Address on your network
* cd rpi_pub   
* Run ./discoverPi 192.168.1.0/24 (or whatever your network CIDR is)
* View the output file called "inventory.txt" in rpi_pub folder

#### Use the IP that was discovered for your pi as inventory
* edit the rpi_pub/ansible/inventory file to include the IP that was discovered in the [rpi_server] group

#### Edit the rpi_pub/ansible/prepPi.yml file to play with roles and tags, but this is optional and advanced

## Usage
> cd rpi_pub/ansible   

> ansible-playbook -i inventory prepPi.yml   

* Include -vv at the end to see more output
* Include --tags "ssh" as an example to see it just do the SSH configurations

## References and Sources
* Jeff Geerling - https://www.jeffgeerling.com/
* Lynis Security Auditing Tool - https://cisofy.com/lynis/
* Kyber MultiQueue I/O
    * https://lwn.net/Articles/720071/
    * https://lwn.net/Articles/720675/
* Extending the life of your Raspberry PI SD Card - https://domoticproject.com/extending-life-raspberry-pi-sd-card/
* Raspberry Pi Hardening Guide - https://chrisapproved.com/blog/raspberry-pi-hardening.html

# Acknowledgement
This repo is a fork of https://github.com/raajivrekha/rpi_pub created by Raajiv Rekha
