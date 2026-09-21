---
layout: default
title: Lab Scripts & Automation - OpenStack Research Documentation
permalink: /labs/
---

# Lab Automation Scripts & Configurations

This section provides production-ready configuration templates, bootstrap scripts, and automation assets used across our OpenStack lab environments.

---

## Directory Structure

```text
labs/
├── devstack/
│   ├── bootstrap.sh       # Automates OS prerequisites, user creation & git cloning
│   └── local.conf         # Multi-service DevStack configuration template (OVN + Placement)
└── README.md              # Quickstart guide for provisioning laboratory nodes
```

---

## DevStack Lab Automation

### 1. `bootstrap.sh`
The bootstrap script prepares a clean Ubuntu 22.04 LTS or 24.04 LTS virtual machine for DevStack deployment. It performs the following steps:
- Installs necessary base system utilities (`git`, `sudo`, `curl`, `bridge-utils`).
- Creates the dedicated unprivileged `stack` user with passwordless `sudo` rights.
- Configures kernel parameters for packet forwarding (`net.ipv4.ip_forward = 1`).
- Clones the official DevStack repository onto the `stack` user's home directory.

To execute on a new laboratory VM:
```bash
curl -fsSL https://raw.githubusercontent.com/AbyanDimas/Opentack-Research/pages/labs/devstack/bootstrap.sh | sudo bash
```

### 2. `local.conf`
A reference configuration tuned for single-node and multi-node controller setups under constrained memory environments (4GB RAM). It includes:
- OVN / OVS network backend integration.
- Keystone, Glance, Nova, Placement, and Neutron enablement.
- Optimized worker daemon concurrency (`API_WORKERS=2`, `CONDUCTOR_WORKERS=2`) to prevent out-of-memory crashes.

Download and place into `/opt/stack/devstack/local.conf`:
```bash
su - stack
cd /opt/stack/devstack
cp /path/to/Opentack-Research/labs/devstack/local.conf ./local.conf
./stack.sh
```

---

## Kolla-Ansible Assets

For multi-node containerized deployments, refer to the operational documentation in [Kolla-Ansible Multi-Node Deployment](/docs/operations/kolla-ansible/).

---

<div class="page-nav-box">
  <a href="/docs/operations/kolla-ansible/" class="page-nav-btn">← Kolla-Ansible Guide</a>
  <a href="/" class="page-nav-btn">Back to Home →</a>
</div>
