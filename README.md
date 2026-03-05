# Bootstrap Router

Distributed inference routing engine for OpenClaw infrastructure.
Routes queries to ThinkCentre (CPU), GPD Pocket 4 (GPU), or Cloud (Kimi 2.5)
based on complexity analysis, keyword signals, and adaptive feedback.

## Architecture

```
User Query
    │
    ▼
┌───────────────────┐
│ ComplexityAnalyzer │  ← token count, keywords, sentence depth
│   (rule-based)    │  ← feedback adjustments from history
└────────┬──────────┘
         │
    ┌────▼────┐
    │ Router  │
    └────┬────┘
         │
    ┌────┴─────────────────────────┐
    │            │                 │
    ▼            ▼                 ▼
ThinkCentre   GPD Pocket 4     Cloud (Kimi)
 CPU/7-8B     GPU-Vulkan/7-8B   Moonshot API
 $0.00        $0.00             $$
    │            │                 │
    └────────────┴─────────────────┘
         │
    ┌────▼────┐
    │ Logger  │ → routing-decisions.log
    └────┬────┘
         │
    ┌────▼─────────┐
    │ Feedback Loop │ ← "that needed cloud" / "overkill"
    └──────────────┘
```

## Quick Start

```bash
# Install dependency
pip install pyyaml requests --break-system-packages

# Health check
python3 router.py --health

# Route a query
python3 router.py "summarize this paragraph about magnetism"

# Analyze without generating
python3 router.py --analyze-only "explain the trade-offs between microservices and monoliths"

# Force a specific node
python3 router.py --force gpd "debug this Python function"

# Pipe from stdin
echo "translate this to Spanish" | python3 router.py --stdin

# JSON output
python3 router.py --json "list the planets"
```

## Dashboard & Reports

```bash
# Terminal dashboard
bash visual-feedback.sh dashboard

# Node health
bash visual-feedback.sh health

# Daily report
python3 routing-logger.py --report

# Last 10 decisions
python3 routing-logger.py --tail 10

# All-time stats
python3 routing-logger.py --stats

# Save report to file
python3 routing-logger.py --report --save
```

## Feedback Loop

```bash
# After a bad local result:
python3 feedback-loop.py --feedback "that needed cloud" --tier simple

# After cloud was overkill:
python3 feedback-loop.py --feedback "overkill" --tier cloud

# Check current adjustments
python3 feedback-loop.py --status

# Reset learned adjustments
python3 feedback-loop.py --reset
```

## Deployment on ThinkCentre

```bash
# Copy to ThinkCentre
scp -r bootstrap-router/ boo@192.168.12.190:~/bootstrap-router/

# Create required directories
ssh boo@192.168.12.190 'mkdir -p ~/.openclaw/workspace/{memory,reports}'

# Add to PATH (in ~/.bashrc or ~/.zshrc)
export PATH="$HOME/bootstrap-router:$PATH"
alias route='python3 ~/bootstrap-router/router.py'
alias routedash='bash ~/bootstrap-router/visual-feedback.sh dashboard'
alias routelog='python3 ~/bootstrap-router/routing-logger.py'
alias routefb='python3 ~/bootstrap-router/feedback-loop.py'
```

## File Layout

```
bootstrap-router/
├── router.py            # Main routing engine
├── routing-config.yaml  # Thresholds, nodes, keywords
├── routing-logger.py    # Decision logging & daily reports
├── feedback-loop.py     # Adaptive threshold learning
├── visual-feedback.sh   # Phosphor green terminal display
└── README.md
```

## Cloud Relay (TODO)

The `_cloud_generate()` method in router.py is a placeholder.
Wire it to OpenClaw's Kimi 2.5 relay when ready. The router
will auto-escalate to cloud if local nodes fail, but actual
cloud generation requires the relay connection.
