# OpenStack Research Documentation

[![Deploy OpenStack Wiki to GitHub Pages](https://github.com/AbyanDimas/Opentack-Research/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/AbyanDimas/Opentack-Research/actions/workflows/deploy-pages.yml)

Technical research and architectural notes on **OpenStack** deployment and operational workflows (DevStack Multi-Node Lab).

**Official Documentation Site:** [https://abyandimas.github.io/Opentack-Research/](https://abyandimas.github.io/Opentack-Research/)

---

## Directory Structure & Categorization

The documentation is organized in `docs/` by domain:

```
docs/
├── overview/
│   ├── architecture.md           # Topology and multi-node role split
│   ├── environment-setup.md      # Host preparation and local.conf
│   └── devstack-lab-notes.md     # Real-world lessons from constrained hardware
├── core-services/
│   ├── keystone.md               # Identity service and Fernet tokens
│   ├── nova-placement.md         # Compute orchestration and Placement API
│   ├── neutron-ovn.md            # Software-defined networking with OVN
│   └── storage.md                # Glance image registry and Cinder block storage
└── operations/
    └── troubleshooting.md        # OOM prevention, AMQP tuning, OVN DB sync
```

---

## CI/CD Pipeline & GitHub Pages Configuration

- **Theme Engine:** Jekyll Dinky theme with customized sidebar navigation and client-side real-time search.
- **Automated Workflow:** GitHub Actions (`.github/workflows/deploy-pages.yml`).
- **Deployment Gate:** Governed by the `github-pages` environment with mandatory review and approval gates.
