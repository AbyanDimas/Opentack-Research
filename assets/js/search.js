(function () {
  const searchInput = document.getElementById('wiki-search-input');
  const dropdown = document.getElementById('search-dropdown');
  if (!searchInput || !dropdown) return;

  const baseUrl = (searchInput.getAttribute('data-baseurl') || '').replace(/\/$/, '');

  const searchIndex = [
    {
      title: "Introduction",
      url: baseUrl + "/",
      category: "Overview",
      description: "Project overview, scope, and OpenStack release lifecycle (2025-2026: Epoxy, Flamingo, Gazpacho).",
      keywords: "openstack research wiki overview introduction epoxy flamingo gazpacho release slurp architecture map"
    },
    {
      title: "Architecture & Topology",
      url: baseUrl + "/architecture",
      category: "Overview",
      description: "Two-node DevStack topology on 4GB RAM VMs. Controller vs Compute role split, AMQP RPC, single NIC design.",
      keywords: "devstack multi-node 4gb ram homelab topology controller compute rabbitmq mysql amqp rpc single nic br-ex ens3 floating ip"
    },
    {
      title: "Environment & Setup (local.conf)",
      url: baseUrl + "/prerequisites",
      category: "Overview",
      description: "Ubuntu 24.04 LTS host configuration, 8GB swap sizing, non-root stack user, local.conf for Node 1 and Node 2.",
      keywords: "ubuntu 24.04 swap 8gb stack user sudo local.conf controller compute stacking devstack ovn geneve"
    },
    {
      title: "Keystone: Identity Service",
      url: baseUrl + "/keystone",
      category: "Core Architecture",
      description: "Fernet token architecture, key rotation, system-scoped and project-scoped RBAC, service catalog and service tokens.",
      keywords: "keystone identity auth authentication fernet token rotation rbac system scope project scope service catalog service token"
    },
    {
      title: "Nova & Placement: Compute",
      url: baseUrl + "/nova-placement",
      category: "Core Architecture",
      description: "Placement API decoupling, Resource Providers, Traits, instance boot lifecycle, Nova Conductor, libvirt/KVM tuning.",
      keywords: "nova compute placement api resource provider inventory traits allocation instance boot lifecycle scheduler libvirt kvm"
    },
    {
      title: "Neutron & OVN: Networking",
      url: baseUrl + "/neutron-ovn",
      category: "Core Architecture",
      description: "OVN SDN backend, Geneve encapsulation, Northbound/Southbound DB, Distributed Virtual Routing (DVR), br-ex single NIC.",
      keywords: "neutron sdn ovn open virtual network geneve vxlan dvr distributed virtual routing floating ip br-ex bridge ip_forward"
    },
    {
      title: "Glance & Cinder: Storage",
      url: baseUrl + "/storage-glance-cinder",
      category: "Core Architecture",
      description: "Image management (RAW vs QCOW2), Cinder persistent block storage, LVM loopback driver, volume attachment workflow.",
      keywords: "glance cinder image raw qcow2 block storage persistent volume iscsi lvm loopback ceph rbd"
    },
    {
      title: "Troubleshooting & Diagnostics",
      url: baseUrl + "/troubleshooting",
      category: "Operations",
      description: "Solving OOM kills on MySQL and RabbitMQ, AMQP heartbeat tuning, OVN DB synchronization, systemd service management.",
      keywords: "troubleshooting diagnostic oom killer mysqld memory out of memory rabbitmq heartbeat timeout ovn db sync systemd journalctl"
    }
  ];

  let selectedIndex = -1;

  function renderResults(results) {
    if (results.length === 0) {
      dropdown.innerHTML = '<div class="search-empty">No matching documents found</div>';
      dropdown.style.display = 'block';
      return;
    }

    dropdown.innerHTML = results.map((item, idx) => `
      <a href="${item.url}" class="search-result-item" data-index="${idx}">
        <div class="search-result-header">
          <span class="search-result-title">${item.title}</span>
          <span class="search-result-category">${item.category}</span>
        </div>
        <div class="search-result-desc">${item.description}</div>
      </a>
    `).join('');

    dropdown.style.display = 'block';
    selectedIndex = -1;
  }

  function handleSearch() {
    const query = searchInput.value.trim().toLowerCase();
    if (!query) {
      dropdown.style.display = 'none';
      dropdown.innerHTML = '';
      return;
    }

    const matches = searchIndex.filter(item => {
      return item.title.toLowerCase().includes(query) ||
             item.description.toLowerCase().includes(query) ||
             item.keywords.toLowerCase().includes(query) ||
             item.category.toLowerCase().includes(query);
    });

    renderResults(matches);
  }

  searchInput.addEventListener('input', handleSearch);

  searchInput.addEventListener('keydown', function (e) {
    const items = dropdown.querySelectorAll('.search-result-item');
    if (!items.length || dropdown.style.display === 'none') return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = (selectedIndex + 1) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = (selectedIndex - 1 + items.length) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && items[selectedIndex]) {
        items[selectedIndex].click();
      } else if (items.length > 0) {
        items[0].click();
      }
    } else if (e.key === 'Escape') {
      dropdown.style.display = 'none';
      searchInput.blur();
    }
  });

  function updateActiveItem(items) {
    items.forEach((item, idx) => {
      if (idx === selectedIndex) {
        item.classList.add('selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('selected');
      }
    });
  }

  // Keyboard shortcut '/' to focus search
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.sidebar-search')) {
      dropdown.style.display = 'none';
    }
  });
})();
