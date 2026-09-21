---
layout: default
title: Troubleshooting & Lab Learnings - OpenStack Research Wiki
---

# 🛠️ Troubleshooting & Lab Learnings

Catatan operasional dan pemecahan masalah nyata yang ditemui selama mengoperasikan DevStack pada spesifikasi perangkat keras terbatas (RAM 4GB).

---

## 1. Menangani Masalah Out-Of-Memory (OOM Killer)

### Gejala Masalah:
Proses `mysqld`, `beam.smp` (RabbitMQ), atau `nova-conductor` tiba-tiba mati tanpa pesan kesalahan eksplisit di log aplikasi.

### Diagnosa:
Periksa log dmesg sistem:
```bash
sudo dmesg -T | grep -i oom
```
Jika terlihat baris *`Out of memory: Killed process <PID> (mysqld)`*, berarti alokasi RAM fisik telah terlampaui.

### Solusi:
1. **Tingkatkan Ukuran Swap:** Pastikan swap berukuran minimal 8GB–10GB aktif.
2. **Batasi Buffer Pool MySQL:** Tambahkan konfigurasi pembatas memori di `/etc/mysql/mariadb.conf.d/50-server.cnf`:
   ```ini
   [mysqld]
   innodb_buffer_pool_size = 256M
   max_connections = 100
   ```
3. **Nonaktifkan Layanan Non-Kritis:** Matikan Horizon dashboard, Aodh, Ceilometer, dan Heat pada `local.conf`.

---

## 2. RabbitMQ Connection Timeout & Heartbeat Lost

### Gejala Masalah:
Nova Compute di Node 2 gagal melaporkan status ke Nova Controller di Node 1:  
*`AMQP server on 192.168.101.142:5672 is unreachable`* atau *`Heartbeat timeout on AMQP connection`*.

### Solusi:
1. Verifikasi listener port 5672 di Node 1:
   ```bash
   sudo ss -tulpn | grep 5672
   sudo rabbitmqctl status
   ```
2. Pastikan user RabbitMQ dan virtual host terdaftar:
   ```bash
   sudo rabbitmqctl list_users
   sudo rabbitmqctl list_permissions -p /
   ```
3. Sesuaikan timeout heartbeat di `/etc/nova/nova.conf`:
   ```ini
   [oslo_messaging_rabbit]
   heartbeat_timeout_threshold = 60
   heartbeat_rate = 2
   ```

---

## 3. Instance Tidak Mendapat IP Address (OVN Metadata & DHCP)

### Gejala Masalah:
Instance berhasil dibuat di Node 2, namun terhenti pada *cloud-init* dan tidak mendapatkan alamat IP dari DHCP.

### Diagnosa & Solusi:
1. Periksa sinkronisasi database OVN:
   ```bash
   sudo ovn-nbctl show
   sudo ovn-sbctl show
   ```
2. Jika ada ketidaksesuaian antara state Neutron dan OVN, jalankan utilitas sinkronisasi:
   ```bash
   neutron-ovn-db-sync-util \
     --config-file /etc/neutron/neutron.conf \
     --config-file /etc/neutron/plugins/ml2/ml2_conf.ini
   ```
3. Pastikan agen `ovn-controller` di Node 2 terhubung sempurna ke Southbound DB di Node 1:
   ```bash
   sudo ovs-vsctl get open . external_ids:ovn-remote
   # Output harus mengarah ke: tcp:192.168.101.142:6642
   ```

---

## 4. Memeriksa Layanan DevStack Berbasis Systemd

Pada rilis DevStack modern, seluruh service dikelola via *systemd user session* di bawah akun `stack`:

```bash
# Melihat daftar seluruh service OpenStack yang aktif
systemctl --user list-units "devstack@*"

# Memeriksa log real-time service tertentu
journalctl --user -u devstack@n-cpu.service -f --no-tail
journalctl --user -u devstack@q-svc.service -f --no-tail

# Merestart layanan tertentu tanpa menjalankan unstack.sh
systemctl --user restart devstack@n-cpu.service
```

---

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/storage-glance-cinder' | relative_url }}">&larr; Glance & Cinder</a>
  <a class="page-nav-btn" href="{{ '/' | relative_url }}">Kembali ke Beranda Wiki 🏠</a>
</div>
