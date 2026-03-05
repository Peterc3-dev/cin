# Centralized Inference Network (CIN)

**Distributed AI compute with local-first routing and transparent cost optimization.**

## Overview

CIN is a hub-and-spoke mesh network for distributed LLM inference. The system routes queries intelligently between local compute nodes (ThinkCentre, GPD Pocket 4) and cloud APIs (Kimi/Opus), minimizing costs while maintaining capability.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│              (Telegram Bot - Single Entry)              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    ROUTER CORE                           │
│  ┌─────────────┐    ┌──────────┐    ┌────────────────┐  │
│  │  Classifier │ →  │  Router  │ →  │ Status Display │  │
│  │  (7B local) │    │ (decision│    │ ⚡ ThinkCentre  │  │
│  └─────────────┘    │  tree)   │    │ · qwen2.5:7b   │  │
│                     └────┬─────┘    │ · 1.2s · $0.00 │  │
│                          │          └────────────────┘  │
│              ┌───────────┼───────────┐                  │
│              ▼           ▼           ▼                  │
│  ┌──────────────┐ ┌──────────┐ ┌──────────────┐        │
│  │ ThinkCentre  │ │  GPD     │ │ Cloud Kimi   │        │
│  │ (CPU · 7-8B) │ │(GPU·7-14B)│ │ (Complex)    │        │
│  │ $0 · ~1-2s   │ │ $0 · ~2-3s │ │ $0.01 · ~2s  │        │
│  └──────────────┘ └──────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  SHELL GHOST MODULE                      │
│         (Integrated command execution layer)             │
│  Auto-detect shell intent OR explicit: ghost: command    │
│  Whitelist · Dry-run · Audit log · No sudo w/o confirm   │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Transparent Routing
Every response includes cost and routing information:
```
⚡ ThinkCentre · qwen2.5:7b · 1.2s · $0.00
```

### 2. Self-Aware Sub-Agent
The system knows its limits and communicates confidence:
- **"I can handle that. Processing..."** (high confidence)
- **"I can try, but this might need more reasoning. Attempt or escalate?"** (uncertain)
- **"This requires complex judgment. Escalating to cloud..."** (auto-route)

### 3. Remote File Access
Fetch files from home machines while away:
```
User (at work): "Send me my resume from GPD"
System: SSH via Tailscale → fetch → deliver via Telegram
Cost: $0
```

### 4. Cost Optimization
| Route | Cost | Speed | Use Case |
|-------|------|-------|----------|
| ThinkCentre 7B | $0 | ~1-2s | File ops, status, simple tasks |
| GPD 14B | $0 | ~2-3s | Code, analysis, local reasoning |
| Cloud Kimi | $0.005-0.015 | ~2-3s | Complex reasoning, creativity |

**Target: 90% local, 10% cloud = 70-85% cost reduction**

### 5. Shell Ghost
Dedicated command execution layer:
- Auto-detects shell intent from natural language
- `ghost:` prefix for explicit shell mode
- Whitelist validation, dry-run for destructive ops
- Audit logging to `~/.local/share/shell-ghost/`

## Components

### Bootstrap Process
1. **Setup Phase**: Cloud agents (Kimi/Opus) design and install local sub-agents
2. **Operation Phase**: Local agents handle routine tasks autonomously
3. **Escalation**: Cloud only wakes for complex decisions

### Nodes
- **ThinkCentre (Hub)**: Central coordinator, routing decisions, lightweight inference
- **GPD Pocket 4 (Compute)**: GPU-accelerated inference, portable node
- **Cloud (Fallback)**: Complex reasoning, architecture decisions, empathy

### Network
- Tailscale mesh VPN (encrypted, authenticated)
- Auto-discovery and joining
- Graceful degradation (nodes operate independently if coordinator down)

## Economics

### Before CIN
- Daily API usage: $3-5
- Monthly: $90-150

### After CIN (Bootstrapped)
- Local power: ~$0.20/day
- Cloud (10% of queries): ~$0.30-0.50/day
- **Total: ~$0.50-0.70/day**
- **Monthly: ~$15-21**

**Savings: 85-90% cost reduction**

## Status

**Phase 1: Design Complete** ✅
- Architecture defined
- Interface designed (transparent routing, status line)
- Component specifications complete

**Phase 2: Implementation** 🚧
- Router module (Opus building)
- Telegram bot interface
- Shell Ghost integration
- Systemd service deployment

**Phase 3: Deployment** ⏳
- ThinkCentre hub setup
- GPD node auto-join
- Testing and tuning
- Documentation

## Philosophy

> "Seamlessness is a luxury for people who don't care about the bill. You care about the bill."

CIN prioritizes **transparency** over seamlessness. You always know when you're burning tokens vs running locally. The system trains you, and you train the system.

## License

MIT — The cathedral is open source.

---

*Built for survival, designed for escape.*
