---
title: "Frankencluster: Deliberately Heterogeneous Distributed Systems"
category: "Infrastructure Engineering"
date: "October 2025"
github: "https://github.com/resurrexio/frankencluster-docs"
description: "7-node K8s cluster built from scavenged hardware spanning AMD Ryzen 9, Intel i7/i5, and potato-tier Celeron. Production-grade infrastructure on deliberately heterogeneous hardware—because understanding failure modes requires systems that occasionally fail."
tags: ["Kubernetes", "Infrastructure", "Distributed Systems", "Homelab"]
---

## Philosophy

**"Production-grade research infrastructure on deliberately heterogeneous hardware—because understanding failure modes requires systems that occasionally fail."**

Cloud providers abstract away hardware heterogeneity, storage topology, and failure domains. Building distributed systems from scavenged hardware teaches:

- **Resource heterogeneity:** 12-core Zen 5 vs 2-core Celeron
- **Failure domains:** Which workloads survive node failures?
- **Storage topology:** Where does data actually live?
- **Network dynamics:** Latency, bandwidth, packet loss
- **Power constraints:** Thermal throttling, PSU limitations

## Cluster Topology

### 7 Nodes, 58 Cores, 168GB RAM

**PurrPower (192.168.1.99)** - BEAST MACHINE 🔥
- AMD Ryzen 9 9900X (12C/24T Zen 5, up to 5.4GHz)
- 128GB DDR5 5600MHz
- Dual GPU: AMD Radeon 7900 XTX (24GB) + 7800 XT (16GB)
- 2TB Gen5 NVMe
- Role: Main workstation, LLM inference, K3s worker (tainted)

**SudoSenpai (192.168.1.98)** - CONTROL PLANE
- AMD Ryzen 9 5900X (12C/24T)
- 32GB DDR4
- 5.5TB storage (1TB NVMe + 3TB HDD + 1.5TB harvested)
- Role: K3s control plane, storage server, MCP RAG (NodePort 30800)

**KawaiiKali (192.168.1.97)** - SLEEK ULTRABOOK
- AMD Ryzen AI 9 HX 370 (12C/24T, up to 5.1GHz)
- 32GB LPDDR5X
- XDNA 2 NPU (dedicated AI acceleration)
- Role: K3s worker, portable development

**WolfWhoami (192.168.1.96)** - RELIABLE WORKER
- Intel i7-7700HQ (4C/8T)
- 7.6GB RAM
- 128GB SATA M.2
- Role: K3s worker (solid until thermal throttling)

**NekoNetcat (192.168.1.95)** - LEGACY MAC
- Intel i5-3210M (2C/4T)
- 3.7GB RAM
- 64GB flash drive
- Role: K3s worker (low specs, does the job occasionally)

**VeryVuln (192.168.1.94)** - VULNERABLE TARGET 🎯
- Intel Celeron N2830 (potato tier)
- Limited RAM
- 64GB flash drive
- Role: Intentionally vulnerable for autonomous red team testing

**BittyBash (192.168.1.92)** - ADDITIONAL WORKER
- Intel i5-8250U (4C/8T)
- 8GB RAM
- 256GB NVMe
- Role: K3s worker (expands distributed compute)

## Network Architecture

**GL.iNet Flint 2 (192.168.1.1)** - Primary Gateway
- OpenWrt with WireGuard, AdGuard
- 5G USB tethering support
- 5Gbps Community Fibre (no CGNAT)

**IP Scheme:**
- `.99 downwards` → Static cluster nodes & workstations
- `.100-.200` → DHCP pool (phones, temporary devices)

**WireGuard Tunnel:**
- Global access (even from Azerbaijan)
- Persistent connection to all cluster nodes
- Traffic routing for remote development

## Storage Topology

### Custom StorageClass: `pwnie-storage`

**Problem:** K3s default StorageClass killed flash drives by writing to random nodes

**Solution:** Node-restricted provisioner
```yaml
kind: StorageClass
metadata:
  name: pwnie-storage
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
  - matchLabelExpressions:
      - key: kubernetes.io/hostname
        values:
          - sudosenpai
```

**Result:** All PersistentVolumes write to SudoSenpai's 5.5TB storage, protecting flash drives on other nodes

### Data Layout

- `/mnt/storage/k3s-pvs/` - Kubernetes PersistentVolumes
- `/mnt/storage/mcp-data/` - MCP RAG indexes and repositories
- Harvested drives provide additional capacity for experiments

## Research Applications

### Adversarial Conditions

- **Resource contention:** What happens when PurrPower hogs CPU for LLM inference?
- **Node failures:** Which services survive WolfWhoami thermal throttling?
- **Storage latency:** How does distributed data access perform with HDD vs NVMe?
- **Network partitions:** WireGuard tunnel failures simulate split-brain scenarios

### Failure Mode Analysis

- **Graceful degradation:** Do workloads reschedule properly?
- **Data consistency:** Do PersistentVolumes maintain integrity during node failures?
- **Resource starvation:** How does K8s scheduler handle heterogeneous nodes?

### Offensive Security

- **VeryVuln as target:** Intentionally vulnerable node for autonomous red teams
- **Lateral movement:** Can compromised node access control plane?
- **Data exfiltration:** Network policies prevent unauthorized access?

## Lessons Learned

1. **Protocol Compliance is Critical:** Missing MCP handshake notifications broke entire system
2. **Storage Policy Enforcement:** Default StorageClass destroyed flash drives
3. **Node Identity Matters:** Almost made strongest node the vulnerable target (naming error)
4. **K8s Security is Strict:** Even "Unconfined" seccomp blocks some syscalls
5. **Async + Containers = Tricky:** socketpair() syscall commonly blocked
6. **Thermal Management:** Intel i7 laptops throttle under sustained load
7. **Flash Drive Longevity:** Don't let K8s write logs to USB flash drives

## Future Enhancements

- **ARM nodes:** Raspberry Pi cluster for heterogeneous CPU architectures
- **GPU scheduling:** Multi-GPU workload distribution (7900 XTX + 7800 XT)
- **Network simulation:** Artificial latency/packet loss for adversarial testing
- **Power monitoring:** Energy consumption analysis per workload
- **Distributed tracing:** OpenTelemetry for multi-node observability

## Status

**Operational since October 2025**

**Uptime:** 99.2% (excluding intentional chaos experiments)

**Workloads:** MCP RAG server, autonomous red team agents, LLM inference, research experiments
