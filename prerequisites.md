---
layout: default
title: Prasyarat & Setup local.conf - OpenStack Research Wiki
---

# ⚙️ Prasyarat & Konfigurasi local.conf

Halaman ini memandu langkah demi langkah persiapan sistem operasi Ubuntu 24.04 LTS serta penulisan file `local.conf` untuk kedua node agar DevStack berhasil melakukan *stacking* tanpa kehabisan memori.

---

## 1. Persiapan Sistem Operasi

Lakukan langkah ini pada **Node 1 (Controller)** dan **Node 2 (Compute)**:

### A. Alokasi Swap (Krusial untuk RAM 4GB)
Tanpa swap yang memadai, kompilasi modul Python dan proses inisialisasi database akan langsung memicu Linux OOM Killer. Alokasikan swap minimal 8GB:

```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### B. Pembuatan Pengguna `stack` Non-Root
DevStack menolak dijalankan sebagai root secara langsung:

```bash
sudo useradd -s /bin/bash -d /opt/stack -m stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo chmod 0440 /etc/sudoers.d/stack
```

Beralih ke pengguna `stack` dan clone repositori DevStack:

```bash
sudo su - stack
git clone https://opendev.org/openstack/devstack.git
cd devstack
```

---

## 2. File `local.conf` Node 1 (Controller)

Simpan konfigurasi berikut di `/opt/stack/devstack/local.conf` pada Node 1 (`192.168.101.142`):

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

# Disable service berat yang tidak esensial
disable_service horizon
disable_service tempest
disable_service heat

# Gunakan Neutron dengan OVN modern
enable_plugin neutron https://opendev.org/openstack/neutron
Q_AGENT=ovn
Q_ML2_PLUGIN_MECHANISM_DRIVERS=ovn,logger
Q_ML2_TENANT_NETWORK_TYPE=geneve

# Konfigurasi Single NIC External Bridge
PUBLIC_INTERFACE=ens3
FLOATING_RANGE=192.168.101.224/28
Q_FLOATING_ALLOCATION_METHOD=continuous
PUBLIC_NETWORK_GATEWAY=192.168.101.1
```

---

## 3. File `local.conf` Node 2 (Compute)

Simpan konfigurasi berikut di `/opt/stack/devstack/local.conf` pada Node 2 (`192.168.101.143`):

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

# Nonaktifkan semua control plane pada compute node
ENABLED_SERVICES=n-cpu,ovn-controller,ovs-vswitchd,ovsdb-server,placement-client
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://192.168.101.142:6080/vnc_auto.html"
VNCSERVER_LISTEN=192.168.101.143
VNCSERVER_PROXYCLIENT_ADDRESS=192.168.101.143
```

---

## 4. Eksekusi Stacking

Jalankan skrip instalasi secara berurutan:
1. Jalankan `./stack.sh` pada **Node 1** terlebih dahulu hingga selesai.
2. Setelah Node 1 selesai sempurna, jalankan `./stack.sh` pada **Node 2**.

Verifikasi node komputasi telah terdaftar dari Node 1:
```bash
source openrc admin admin
openstack hypervisor list
openstack compute service list
```

---

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/architecture' | relative_url }}">&larr; Arsitektur Lab</a>
  <a class="page-nav-btn" href="{{ '/keystone' | relative_url }}">Lanjut: 🔐 Keystone (Identity) &rarr;</a>
</div>
