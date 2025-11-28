---
title: "K8s-Native MCP RAG Server for Offensive Security"
category: "Infrastructure Engineering"
date: "October 2025"
github: "https://github.com/resurrexio/mcp-rag-server"
description: "World's first Kubernetes-native Model Context Protocol RAG server purpose-built for offensive security research. Distributed indexing, vector search, and automatic repository synchronization."
tags: ["MCP", "RAG", "Kubernetes", "Offensive Security", "Infrastructure"]
---

## Overview

**World's first K8s-native MCP RAG server** designed for offensive security research. Automatically indexes GitHub repositories (BlackArch tools, exploit databases, security documentation) and provides semantic search via Model Context Protocol.

## Why K8s-Native?

Traditional RAG servers run as single processes. This architecture:

- **Scales horizontally:** Multiple indexing workers across cluster nodes
- **Fault tolerance:** Pod restarts don't lose state (PersistentVolumes)
- **Resource isolation:** Indexing doesn't impact inference workloads
- **Distributed storage:** 5.5TB on SudoSenpai via pwnie-storage StorageClass

## Architecture

### Components

**MCP Server (NodePort 30800):**
- Model Context Protocol compliant
- JSONRPC 2.0 over stdin/stdout
- Exposes tools: `search`, `index_repo`, `list_repos`

**Vector Database:**
- ChromaDB for semantic search
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Persistent storage: `/mnt/storage/mcp-data/`

**Repository Sync:**
- Automatic git clone/pull for configured repos
- BlackArch tools, ExploitDB, PayloadsAllTheThings
- Custom offensive security documentation

**Kubernetes Integration:**
- Deployment: 2 replicas for HA
- Service: NodePort 30800 (accessible cluster-wide)
- PersistentVolumeClaim: 100GB on SudoSenpai
- ConfigMap: Repository list, indexing config

## Capabilities

**Semantic Search:**
```python
# Query: "SSH brute force tools"
# Returns: hydra, medusa, patator, ncrack with usage examples
```

**Repository Indexing:**
- Automatically indexes markdown, code, documentation
- Chunking strategy: 512 tokens with 50-token overlap
- Metadata: file path, repository, commit hash, last updated

**MCP Protocol:**
- LLM agents query via standard MCP interface
- No custom APIs—works with any MCP-compatible client
- Streaming responses for large result sets

## Research Applications

**Autonomous Red Teams:**
- Agents discover tools via semantic search ("privilege escalation Linux kernel 5.4")
- Documentation retrieval for tool usage
- Exploit selection based on target fingerprinting

**Vulnerability Research:**
- Cross-reference CVEs with available exploits
- Historical vulnerability patterns
- Zero-day discovery via code analysis

**Infrastructure Documentation:**
- Internal lab documentation indexed
- Network topology, node capabilities, deployed services
- Session logs and technical write-ups

## Technical Challenges Solved

**Protocol Compliance:**
- MCP handshake requires `notifications/initialized` (missing = handshake failure)
- JSONRPC strict format requirements
- Async event loop compatibility with K8s

**Storage Policy:**
- K3s default StorageClass killed flash drives
- Custom pwnie-storage restricts writes to SudoSenpai's 5.5TB storage
- Node affinity prevents writes to vulnerable nodes

**Security Considerations:**
- Offensive tools indexed but not executed
- Read-only file system for indexed repos
- Network policies restrict external access

## Performance

- **Indexing:** ~1000 files/minute
- **Query latency:** <100ms for semantic search
- **Storage:** ~2GB indexed data (50+ repositories)
- **Concurrent users:** 10+ simultaneous MCP clients

## Future Enhancements

- **Multi-modal indexing:** Images, PDFs, videos
- **Real-time indexing:** Webhook-triggered updates
- **Collaborative filtering:** Usage patterns inform search ranking
- **Federated search:** Cross-cluster RAG coordination

## Status

**Operational:** Deployed on K3s cluster since October 2025

**In Use:** Autonomous red team agents, manual research queries, documentation retrieval
