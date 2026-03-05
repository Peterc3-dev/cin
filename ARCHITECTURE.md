# CIN Architecture Decisions

## Routing Strategy

### Decision Tree
```
User Request
    │
    ▼
[Classifier: What type?]
    │
    ├── Simple task? ────────┐
    │   (file ops, status,   │
    │    simple lookup)       │
    │                         ▼
    │              ┌──────────────────┐
    │              │ ThinkCentre 7B   │
    │              │ $0 · ~1-2s       │
    │              └──────────────────┘
    │
    ├── Complex but local? ──┐
    │   (code, analysis,     │
    │    summarization)       │
    │                         ▼
    │              ┌──────────────────┐
    │              │ GPD 14B          │
    │              │ $0 · ~2-3s       │
    │              └──────────────────┘
    │
    └── Complex/Subjective? ─┐
        (reasoning, empathy,  │
         creativity, planning)│
                              ▼
                   ┌──────────────────┐
                   │ Cloud Kimi       │
                   │ $0.01-0.05       │
                   └──────────────────┘
```

### Interface Philosophy

**Option 1+4 Hybrid: Single Interface, Transparent Routing**

- One Telegram bot (not multiple)
- Router decides destination
- Status line on EVERY response
- User always knows cost and routing

**Status Line Format:**
```
⚡ ThinkCentre · qwen2.5:7b · 1.2s · $0.00
⚡ GPD · qwen3:8b · 2.1s · $0.00
☁️ Cloud · kimi-k2.5 · 2.3s · $0.02
```

### Commands

**Force Local Mode (Selective Mutism Accommodation):**
```
/pin local    # Force all queries to local nodes
/unpin        # Return to smart routing
```

**Feedback Loop:**
- "that needed cloud" — tells system local was insufficient
- "overkill" — tells system cloud was unnecessary
- Natural language, inline, no special commands

## Shell Ghost Design

### Why Integrated?

Shell Ghost is a **capability module**, not a service:
- Receives commands from router
- Executes locally
- Returns output
- Function call, not daemon

**NOT a separate systemd service because:**
- No event loop needed
- No network listener
- No IPC overhead
- One less failure point

### Security Model

**Isolation via policy, not process:**
- Command whitelist
- Dry-run gate for destructive ops
- Audit logging
- No sudo without confirmation

**NOT process isolation because:**
- Shell commands need system access
- Additional process = complexity without benefit
- Whitelist + audit = actual security

### Trigger Design

**Primary: Auto-detect**
Router classifies shell intent from natural language.

**Override: `ghost:` prefix**
Explicit shell mode when classifier uncertain.

**Examples:**
```
"update my packages"              → Shell Ghost (auto)
"ghost: pacman -Syu"              → Shell Ghost (explicit)
"check disk space"                → Shell Ghost (auto)
"ghost: df -h"                    → Shell Ghost (explicit)
```

## Node Capabilities

### ThinkCentre (Hub)
**Role:** Central coordinator, lightweight inference
**Specs:** i5-14400T, 32GB RAM, CPU-only
**Models:** 
- qwen2.5:7b (general)
- hermes3:8b (tool calling)
- qwen3:8b (latest)
- nomic-embed-text (embeddings)
**Best for:** File ops, status checks, routing decisions, simple Q&A

### GPD Pocket 4 (Compute)
**Role:** GPU-accelerated inference, portable node
**Specs:** AMD HX 370, Radeon 890M, 32GB RAM
**Models:**
- qwen2.5:7b (general)
- dolphin-llama3:8b (conversation)
**Best for:** Code analysis, summarization, local reasoning, heavier tasks

### Cloud (Fallback)
**Role:** Complex reasoning, creativity, empathy
**Models:** kimi-k2.5, kimi-k2-thinking
**Best for:** Architecture decisions, emotional support, creative writing, multi-step planning

## Network

### Tailscale Mesh
- Encrypted WireGuard tunnels
- Automatic NAT traversal
- No port forwarding
- Zero-config

### Auto-Discovery
- Nodes announce on boot
- Heartbeat every 30s
- Timeout after 45s = node offline
- Graceful reconnection

### Fallback Behavior
If coordinator (ThinkCentre) unreachable:
- GPD continues operating locally
- Queries run on GPD 14B
- No cloud escalation (unless configured)
- Logs locally, syncs when coordinator returns

## Cost Tracking

### Per-Query Cost Display
Every response shows:
- Node used
- Model name
- Response time
- Cost in USD

### Daily Reports
```
Daily CIN Report - 2026-03-05
==============================
Queries: 45
Local: 38 (84%) · $0.00
Cloud: 7 (16%) · $0.23
Total: $0.23 (vs $3.15 uncached)
Savings: $2.92 (93%)
```

### Feedback Integration
User feedback updates routing rules:
- "that needed cloud" → lowers threshold for that query type
- "overkill" → raises threshold for that query type
- Learns over time, improves accuracy

## Bootstrap Process

### Phase 1: Cloud Seed
Cloud agents (Kimi/Opus):
- Design router architecture
- Create local sub-agent scripts
- Install systemd services
- Configure Tailscale mesh

### Phase 2: Local Operation
Sub-agents run autonomously:
- Handle routine tasks ($0)
- Log decisions
- Report to coordinator

### Phase 3: Minimal Cloud
Cloud only wakes for:
- Edge cases
- Complex decisions
- User explicitly requests cloud
- System training/updates

**Result:** $0.20/day electricity vs $3/day API calls = 90% savings

## Design Principles

1. **Transparency over Seamlessness**
   - Always show cost
   - Always show routing
   - User trains system, system trains user

2. **Local-First**
   - Default to local
   - Escalate only when necessary
   - Graceful degradation

3. **Self-Awareness**
   - System knows its limits
   - Communicates confidence
   - Asks for help when needed

4. **Survival Economics**
   - Built for budget constraints
   - Every query has a cost
   - Optimization is the product

---

*The cathedral sustains itself on electricity.*
