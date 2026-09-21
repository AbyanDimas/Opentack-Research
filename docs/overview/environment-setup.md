---
layout: default
title: Environment & Setup - OpenStack Research Documentation
permalink: /docs/overview/environment-setup/
---

# Prerequisites and Environment Setup

This section details host operating system preparation for Ubuntu 24.04 LTS and the dual `local.conf` configurations required to deploy DevStack across the controller and compute nodes under 4GB RAM constraints.

---

## 1. Operating System Preparation

Execute these initial steps on both **Node 1 (Controller)** and **Node 2 (Compute)**:

### Swap Space Allocation (Required for 4GB RAM)
Python compilation, dependency installation, and database initialization will exhaust 4GB of physical RAM. Allocate an 8GB swapfile to prevent premature process termination:

```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Dedicated Stack User
DevStack must be executed under a dedicated non-root user with passwordless sudo privileges:

```bash
sudo useradd -s /bin/bash -d /opt/stack -m stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo chmod 0440 /etc/sudoers.d/stack
```

Switch to the `stack` user and clone the DevStack repository:

```bash
sudo su - stack
git clone https://opendev.org/openstack/devstack.git
cd devstack
```

---

## 2. Controller Configuration (Node 1)

Create `/opt/stack/devstack/local.conf` on Node 1 (`192.168.101.142`):

```ini
[[local|localrc]]
HOST_IP=192.168.101.142
SERVICE_HOST=192.168.101.142
MYSQL_HOST=192.168.101.142
RABBIT_HOST=192.168.101.142
GLANCE_HOSTPORT=192.168.101.142:9292

ADMIN_PASSWORD=SecretPassword123
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

# Disable resource-intensive non-essential services
disable_service horizon
disable_service tempest
disable_service heat

# Enable Neutron with modern OVN driver
enable_plugin neutron https://opendev.org/openstack/neutron
Q_AGENT=ovn
Q_ML2_PLUGIN_MECHANISM_DRIVERS=ovn,logger
Q_ML2_TENANT_NETWORK_TYPE=geneve

# Single NIC External Bridge Mapping
PUBLIC_INTERFACE=ens3
FLOATING_RANGE=192.168.101.224/28
Q_FLOATING_ALLOCATION_METHOD=continuous
PUBLIC_NETWORK_GATEWAY=192.168.101.1
```

---

## 3. Compute Node Configuration (Node 2)

Create `/opt/stack/devstack/local.conf` on Node 2 (`192.168.101.143`):

```ini
[[local|localrc]]
HOST_IP=192.168.101.143
SERVICE_HOST=192.168.101.142
MYSQL_HOST=192.168.101.142
RABBIT_HOST=192.168.101.142
GLANCE_HOSTPORT=192.168.101.142:9292

ADMIN_PASSWORD=SecretPassword123
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

# Disable all control-plane services on the compute node
ENABLED_SERVICES=n-cpu,ovn-controller,ovs-vswitchd,ovsdb-server,placement-client
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://192.168.101.142:6080/vnc_auto.html"
VNCSERVER_LISTEN=192.168.101.143
VNCSERVER_PROXYCLIENT_ADDRESS=192.168.101.143
```

---

## 4. Stacking Execution and Verification

Execute the setup scripts in sequential order:
1. Run `./stack.sh` on **Node 1** and ensure all services finish initial provisioning.
2. Run `./stack.sh` on **Node 2**.

Verify hypervisor registration from Node 1:
```bash
source openrc admin admin
openstack hypervisor list
openstack compute service list
```

---

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/docs/overview/architecture/' | relative_url }}">&larr; Architecture & Topology</a>
  <a class="page-nav-btn" href="{{ '/docs/core-services/keystone/' | relative_url }}">Next: Keystone (Identity) &rarr;</a>
</div>
