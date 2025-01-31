#!/bin/sh
opkg update
if ! python -c "import requests" &> /dev/null; then
  echo "Installing python3-requests..."
  opkg install python3-requests
fi
echo "Checking WireGuard dependencies..."
if [ ! -f /etc/iptables/iptables.rules ]; then
  echo "Installing iptables..."
  opkg --force-reinstall --force-overwrite install iptables &> /dev/null
fi
if [ ! -f /usr/bin/wg ]; then
  echo "Installing WireGuard tools and dependencies..."
  opkg --force-reinstall --force-overwrite install wireguard-tools &> /dev/null
  opkg --force-reinstall --force-overwrite install wireguard-tools-bash-completion &> /dev/null
  opkg --force-reinstall --force-overwrite install openresolv &> /dev/null
fi
if [ ! -f /usr/bin/aplay ]; then
  echo "Installing aplay (alsa-utils)..."
  opkg --force-reinstall --force-overwrite install alsa-utils &> /dev/null
fi
rm -rf /tmp/*.ipk
exit 0
