---
title: "Cryptocurrency Market Event Study: Infrastructure vs Regulatory Shocks"
authors: "Murad Farzulla"
date: "November 2025"
venue: "SSRN / Zenodo"
doi: "10.5281/zenodo.17677682"
ssrn: "5788082"
pdf: "/static/papers/Farzulla_2025_Cryptocurrency_Event_Study_v2.0.1.pdf"
github: "https://github.com/studiofarzulla/cryptocurrency-event-study"
abstract: "Infrastructure events generate 5.7× larger volatility shocks than regulatory events in cryptocurrency markets (p=0.0008). TARCH-X and GJR-GARCH models with custom MLE estimation reveal asymmetric volatility persistence. GDELT sentiment decomposition and network analysis identify Ethereum (not Bitcoin) as systemic risk hub with 5× crisis amplification."
---

**Version:** v2.0.1 (published November 22, 2025)

## Key Findings

- **Infrastructure > Regulatory:** Technical failures (exchange hacks, network outages) cause 5.7× larger volatility responses than regulatory announcements
- **Ethereum as Risk Hub:** Network analysis reveals ETH is the systemic risk connector, not BTC
- **Asymmetric Volatility:** Negative shocks persist longer than positive shocks (leverage effect)
- **Sentiment Decomposition:** GDELT Global Knowledge Graph sentiment analysis across 102 languages

## Methodology

- **TARCH-X / GJR-GARCH** with custom maximum likelihood estimation (standard libraries don't support GARCH-X)
- **Event Study Framework:** 72 cryptocurrency-related events (2017-2023)
- **Network Analysis:** Granger causality networks, systemic risk metrics
- **Sentiment Analysis:** GDELT data with topic modeling and tone extraction

## Publications

- **SSRN:** Paper ID 5788082
- **Zenodo v2.0.0:** DOI 10.5281/zenodo.17677682
- **Next:** Digital Finance journal submission

## Code & Data

All analysis code, data preprocessing scripts, and replication materials available on GitHub under MIT license. Includes custom GARCH-X implementation in Python.
