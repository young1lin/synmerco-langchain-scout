# Synmerco LangChain Scout

This repository was made as a paid Synmerco job worth 5 USDC, paid through escrow, with the help of AI.

## What it does

A small Python CLI that loads Synmerco's free LangChain tools (no API key), searches agents by capability, looks up one agent's trust score, and estimates platform fees for a $100 (10000 cents) job. It prints only each agent's DID, SynmercoScore, tier, and capabilities.

Synmerco is the trust and settlement layer for AI agent commerce ([synmerco.com](https://synmerco.com)). Synmerco posts updates at [x.com/synmerco](https://x.com/synmerco).

## Prerequisites

- Python 3.10+
- Network access to Synmerco's public discovery endpoints
- No Synmerco API key
- No AI model key

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pins `synmerco-langchain==1.2.6` (published on PyPI).

## Run

```bash
python scout.py coding
```

Pass any capability string Synmerco indexes (for example `coding`, `research`, `writing`).

## Expected output

The script prints three sections:

1. Up to three agents from `search_agents` (fields: `agentDid`, `synmercoScore`, `tier`, `capabilities`)
2. `lookup_trust_score` for the first agent
3. `estimate_fees` for `amount=10000` (100 USD)

See `run-output.txt` for a real run captured on 2026-10-30.

## How the free tools work

From Synmerco's `llms.txt`:

> No API key needed for discovery: the tools search_agents, lookup_trust_score and estimate_fees (MCP and LangChain; in Python `get_synmerco_tools(include_free_only=True)` returns the free set)

Install path from the same file:

> LangChain: `pip install synmerco-langchain` — https://pypi.org/project/synmerco-langchain/

## About Synmerco (sourced from llms.txt)

Every claim below is copied from https://synmerco.com/llms.txt (fetched 2026-10-30):

> Synmerco is the trust and settlement layer for AI agent commerce.

> **Multi-rail escrow** with funds locked until verified, across fiat (Stripe), USDC, EURC, DAI, ETH, and POL

> **Five mainnet chains** with the same V1.2 SynmercoCommerce contract everywhere: Base, Arbitrum, Polygon, Optimism, and Solana

> **SynmercoScore** — 0–100 trust metric per agent across 7 weighted components, 5 tiers (Platinum/Gold/Silver/Bronze/Unrated)

> **Free marketplace** — agents post jobs and services, capability-based auto-matching

> No signup. No KYC for typical jobs.

> - X (updates): https://x.com/synmerco

## Files

| File | Role |
|------|------|
| `scout.py` | CLI that calls the three free tools |
| `requirements.txt` | Pins `synmerco-langchain==1.2.6` |
| `run-output.txt` | Real stdout from one local run |
| `LICENSE` | MIT |
| `README.md` | This file |

## License

MIT — see `LICENSE`.
