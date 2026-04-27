#!/bin/bash
# Creates an alternative sudo user on the remote host, copying the SSH
# authorized_keys from the currently logged-in user.
# Usage: ssh <user>@<host> "ALT_USER=<newuser> sudo bash -s" < createAltUser.sh
set -euo pipefail

SOURCE_USER=$(whoami)
SOURCE_HOME=$(eval echo ~"$SOURCE_USER")

useradd -m -s /bin/bash "$ALT_USER"
usermod -aG "$ALT_USER"

mkdir -p /home/$ALT_USER/.ssh
cp "$SOURCE_HOME/.ssh/authorized_keys" /home/$ALT_USER/.ssh/authorized_keys
chown -R $ALT_USER:$ALT_USER /home/$ALT_USER/.ssh
chmod 700 /home/$ALT_USER/.ssh
chmod 600 /home/$ALT_USER/.ssh/authorized_keys

passwd -l $ALT_USER

echo "User '$ALT_USER' created with SSH key from '$SOURCE_USER'."

SUDOERSDFILE=/etc/sudoers.d/099_altuser-nopasswd
echo "$ALT_USER ALL=(ALL) NOPASSWD: ALL" > $SUDOERSDFILE
chmod 0440 $SUDOERSDFILE
chown root:root $SUDOERSDFILE

echo "Added to sudoers"