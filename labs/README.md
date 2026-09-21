# OpenStack Research Lab Assets

This directory contains automation scripts, configuration recipes, and bootstrap helpers for reproducing our OpenStack experimental testbeds.

## Subdirectories

- **`devstack/`**:
  - `bootstrap.sh`: One-liner environment preparation script for Ubuntu LTS hosts.
  - `local.conf`: Resource-constrained DevStack deployment configuration tuned for 4GB-8GB RAM nodes with OVN.

## Quickstart

```bash
# 1. Run bootstrap as root on target VM
sudo bash devstack/bootstrap.sh

# 2. Login as the stack user
su - stack

# 3. Deploy DevStack
cp /path/to/local.conf /opt/stack/devstack/local.conf
cd /opt/stack/devstack
./stack.sh
```
