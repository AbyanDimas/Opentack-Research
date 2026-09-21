#!/usr/bin/env bash
# ==============================================================================
# Bootstrap Script for DevStack on Ubuntu 22.04 / 24.04 LTS
# ==============================================================================
set -euo pipefail

echo "==> [1/4] Updating package index and installing base dependencies..."
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    curl \
    wget \
    sudo \
    bridge-utils \
    iptables \
    net-tools \
    python3 \
    python3-pip \
    python3-venv

echo "==> [2/4] Configuring Linux kernel network forwarding..."
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/60-openstack.conf

echo "==> [3/4] Creating dedicated 'stack' user with sudo rights..."
if ! id -u stack >/dev/null 2>&1; then
    useradd -s /bin/bash -d /opt/stack -m stack
    echo "stack ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/50_stack_sh
    chmod 0440 /etc/sudoers.d/50_stack_sh
    echo "User 'stack' successfully created."
else
    echo "User 'stack' already exists."
fi

echo "==> [4/4] Cloning DevStack repository into /opt/stack/devstack..."
sudo -u stack bash -c '
    if [ ! -d "/opt/stack/devstack" ]; then
        git clone https://opendev.org/openstack/devstack /opt/stack/devstack
        echo "DevStack cloned successfully."
    else
        echo "DevStack directory already present. Updating..."
        cd /opt/stack/devstack && git pull origin master
    fi
'

echo "======================================================================"
echo " Bootstrap Complete! Next steps:"
echo " 1. Switch to user: su - stack"
echo " 2. Copy local.conf: cd /opt/stack/devstack && nano local.conf"
echo " 3. Run stack: ./stack.sh"
echo "======================================================================"
