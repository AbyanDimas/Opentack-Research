# OpenStack Research Wiki

Selamat datang di repositori riset dan dokumentasi **OpenStack**. Repositori ini berisi kumpulan catatan arsitektur, eksperimen homelab, konfigurasi DevStack, serta panduan implementasi cloud privat multi-node.

---

## 📚 Daftar Isi / Navigasi Dokumen

- [**Arsitektur & DevStack Lab Overview**](./OpenStack-DevStack-Overview)
  - Arsitektur Lab Multi-node (Controller + Compute)
  - Penjelasan Alur Komunikasi (Nova, Neutron, Keystone, Glance, RabbitMQ, MySQL)
  - Konfigurasi Single NIC dengan Bridge `br-ex`

---

## 🏗️ Ringkasan Topologi Lab

Topologi eksperimen menggunakan dua node Ubuntu 24.04 LTS dengan alokasi memori minimalis (4GB RAM per node):

| Node | Hostname | IP | Peran (Role) |
|---|---|---|---|
| **Node 1** | `ab-lab-research-01` | `192.168.101.142` | Controller & Network Node (Keystone, Nova API, Neutron Server, Glance, MySQL, RabbitMQ) |
| **Node 2** | `ab-lab-research-02` | `192.168.101.143` | Compute Node (`nova-compute`, libvirt, KVM, Neutron L2 Agent / OVS) |

```mermaid
flowchart TB
    subgraph LAN["LAN 192.168.101.0/24"]
        direction TB
    end

    subgraph Node1["Node01 (.142) - Controller & Network Node"]
        API["Keystone, Nova API,<br/>Neutron server, Glance"]
        DATA["MySQL & RabbitMQ"]
        BREX["br-ex shares ens3"]
    end

    subgraph Node2["Node02 (.143) - Compute Node"]
        COMPUTE["nova-compute<br/>libvirt & KVM"]
        AGENT["neutron L2 agent, OVS"]
    end

    LAN --> Node1
    LAN --> Node2
    API <--> DATA
    DATA <-- "RPC over RabbitMQ & DB queries" --> AGENT
    DATA <-- "RPC over RabbitMQ & DB queries" --> COMPUTE
```

---

## 💡 Pelajaran Utama dari Lab

1. **Resource Headroom & Split Peran:**
   Menjalankan OpenStack di 4GB RAM memerlukan pemisahan ketat: Node 1 menampung seluruh *control plane*, sementara Node 2 hanya menjalankan *compute agent*.
2. **Ketiadaan Dedicated NIC:**
   External network di-share langsung di atas interface fisik yang sama (`ens3`) dengan mengarahkan `br-ex`, `FLOATING_RANGE`, dan `PUBLIC_INTERFACE` ke subnet lokal.

---

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
  document.querySelectorAll('pre code.language-mermaid').forEach(el => {
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = el.textContent;
    el.parentElement.replaceWith(div);
  });
</script>
