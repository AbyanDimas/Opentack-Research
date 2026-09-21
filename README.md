# Opentack-Research

[![Deploy OpenStack Wiki to GitHub Pages](https://github.com/AbyanDimas/Opentack-Research/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/AbyanDimas/Opentack-Research/actions/workflows/deploy-pages.yml)

Kumpulan dokumentasi, riset, dan eksperimen arsitektur seputar **OpenStack** (DevStack Multi-Node Lab).

🌐 **Situs Wiki Resmi:** [https://abyandimas.github.io/Opentack-Research/](https://abyandimas.github.io/Opentack-Research/)

---

## 📖 Konten Riset

- [OpenStack DevStack Lab: Overview and Architecture](./OpenStack-DevStack-Overview.md)
- [Struktur & Beranda Wiki](./index.md)

## ⚙️ Konfigurasi GitHub Pages & CI/CD

- **Framework / Theme:** Jekyll (**Dinky** theme via `_config.yml`)
- **CI/CD Pipeline:** GitHub Actions (`.github/workflows/deploy-pages.yml`)
- **Deployment Gate:** Menggunakan GitHub Environment `github-pages` dengan proteksi review manual (memerlukan persetujuan / approve dari pemilik repo sebelum proses deploy dipublikasikan).
