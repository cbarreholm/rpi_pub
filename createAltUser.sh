#!/bin/bash
# Creates an alternative sudo user on the remote host, copying the SSH
# authorized_keys from the currently logged-in user.
# Usage: ssh <user>@<host> "ALT_USER=<newuser> bash -s" < createAltUser.sh
set -euo pipefail

echo "Set up user '$ALT_USER'"

SOURCE_USER=$(whoami)
SOURCE_HOME=$(eval echo ~"$SOURCE_USER")

sudo useradd -m -s /bin/bash "$ALT_USER"

sudo mkdir -p /home/$ALT_USER/.ssh
sudo cp "$SOURCE_HOME/.ssh/authorized_keys" /home/$ALT_USER/.ssh/authorized_keys
sudo chown -R $ALT_USER:$ALT_USER /home/$ALT_USER/.ssh
sudo chmod 700 /home/$ALT_USER/.ssh
sudo chmod 600 /home/$ALT_USER/.ssh/authorized_keys

sudo passwd -l $ALT_USER

echo "User '$ALT_USER' created with SSH key from '$SOURCE_USER'."

SUDOERSDFILE=/etc/sudoers.d/099_altuser-nopasswd
echo "$ALT_USER ALL=(ALL) NOPASSWD: ALL" | sudo tee $SUDOERSDFILE > /dev/null
sudo chmod 0440 $SUDOERSDFILE
sudo chown root:root $SUDOERSDFILE

echo "Added to sudoers"