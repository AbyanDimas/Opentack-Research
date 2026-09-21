# OpenStack Research Documentation

[![Deploy OpenStack Wiki to GitHub Pages](https://github.com/AbyanDimas/Opentack-Research/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/AbyanDimas/Opentack-Research/actions/workflows/deploy-pages.yml)

Technical research and architectural notes on **OpenStack** deployment and operational workflows (DevStack Multi-Node Lab).

**Official Documentation Site:** [https://abyandimas.github.io/Opentack-Research/](https://abyandimas.github.io/Opentack-Research/)

---

## Documentation Index

- [Introduction](./index.md)
- [Architecture & Topology](./architecture.md)
- [Environment & Setup](./prerequisites.md)
- [Keystone: Identity Architecture](./keystone.md)
- [Nova & Placement: Compute Orchestration](./nova-placement.md)
- [Neutron & OVN: Software-Defined Networking](./neutron-ovn.md)
- [Glance & Cinder: Storage Architecture](./storage-glance-cinder.md)
- [Troubleshooting & Diagnostics](./troubleshooting.md)

---

## CI/CD Pipeline & GitHub Pages Configuration

- **Jekyll Custom Engine:** Responsive documentation shell with client-side interactive search and dark sidebar.
- **Automated Workflow:** GitHub Actions (`.github/workflows/deploy-pages.yml`).
- **Deployment Protection:** Governed by the `github-pages` environment with mandatory review and approval gates.
