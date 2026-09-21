---
layout: default
title: Troubleshooting - OpenStack Research Documentation
---

# Troubleshooting and Diagnostic Guide

Operational diagnostics and remediation procedures derived from managing a multi-node DevStack deployment under 4GB RAM constraints.

---

## 1. Out-Of-Memory (OOM Killer) Remediation

### Symptoms:
Key daemons (`mysqld`, `beam.smp` for RabbitMQ, or `nova-conductor`) terminate unexpectedly without prior error messages in service logs.

### Diagnostics:
Inspect the kernel ring buffer:
```bash
sudo dmesg -T | grep -i oom
```
If an entry such as `Out of memory: Killed process <PID> (mysqld)` appears, memory pressure has triggered the Linux OOM killer.

### Resolution Steps:
1. **Verify Swap Space:** Ensure an 8GB–10GB swapfile is mounted with active priority.
2. **Constrain MySQL Buffer Pool:** Restrict memory limits in `/etc/mysql/mariadb.conf.d/50-server.cnf`:
   ```ini
   [mysqld]
   innodb_buffer_pool_size = 256M
   max_connections = 100
   ```
3. **Decommission Telemetry:** Ensure Ceilometer, Aodh, and Heat are disabled in `local.conf`.

---

## 2. AMQP Connection Timeouts & Heartbeat Loss

### Symptoms:
Nova Compute on Node 2 reports communication failure to the controller:  
`AMQP server on 192.168.101.142:5672 is unreachable` or `Heartbeat timeout on AMQP connection`.

### Resolution Steps:
1. Check port 5672 listener status on Node 1:
   ```bash
   sudo ss -tulpn | grep 5672
   sudo rabbitmqctl status
   ```
2. Verify rabbitmq users and permissions:
   ```bash
   sudo rabbitmqctl list_users
   sudo rabbitmqctl list_permissions -p /
   ```
3. Extend heartbeat thresholds in `/etc/nova/nova.conf`:
   ```ini
   [oslo_messaging_rabbit]
   heartbeat_timeout_threshold = 60
   heartbeat_rate = 2
   ```

---

## 3. DHCP and Metadata Resolution Failures in OVN

### Symptoms:
New virtual machine instances enter the `ACTIVE` state but fail to acquire an IP address via cloud-init.

### Diagnostics and Remediation:
1. Inspect logical flows and OVSDB status:
   ```bash
   sudo ovn-nbctl show
   sudo ovn-sbctl show
   ```
2. Execute a database resynchronization:
   ```bash
   neutron-ovn-db-sync-util \
     --config-file /etc/neutron/neutron.conf \
     --config-file /etc/neutron/plugins/ml2/ml2_conf.ini
   ```
3. Verify the Southbound DB remote target on Node 2:
   ```bash
   sudo ovs-vsctl get open . external_ids:ovn-remote
   # Expected output: tcp:192.168.101.142:6642
   ```

---

## 4. Systemd Service Inspection for DevStack

In modern DevStack environments, daemons run as user units under the `stack` account:

```bash
# List all active OpenStack systemd units
systemctl --user list-units "devstack@*"

# Stream logs for a specific service
journalctl --user -u devstack@n-cpu.service -f --no-tail
journalctl --user -u devstack@q-svc.service -f --no-tail

# Restart an individual daemon
systemctl --user restart devstack@n-cpu.service
```

---

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/storage-glance-cinder' | relative_url }}">&larr; Glance & Cinder</a>
  <a class="page-nav-btn" href="{{ '/' | relative_url }}">Return to Overview &rarr;</a>
</div>
