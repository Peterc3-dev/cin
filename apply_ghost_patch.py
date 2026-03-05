#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
 ROUTER PATCH — Shell Ghost Integration
 
 Apply this to router.py to add Ghost as a routing target.
 
 Changes:
 1. Import shell_ghost module
 2. Add "ghost" to TIER_TO_NODE mapping
 3. Add shell intent detection to ComplexityAnalyzer
 4. Route shell queries to Ghost instead of Ollama
 
 Usage:
   python3 apply_ghost_patch.py
 
 This script patches router.py in-place. Back up first.
═══════════════════════════════════════════════════════════════
"""

INTEGRATION_GUIDE = """
═══════════════════════════════════════════════════════════════
 MANUAL INTEGRATION GUIDE (if you prefer to patch by hand)
═══════════════════════════════════════════════════════════════

1. At the top of router.py, add:

    from shell_ghost import ShellGhost, detect_shell_intent

2. In BootstrapRouter.__init__(), add:

    self.ghost = ShellGhost()

3. In BootstrapRouter.TIER_TO_NODE, add:

    "shell": "ghost",

4. In ComplexityAnalyzer.analyze(), add BEFORE the final return:

    # Shell intent detection — takes priority over all other routing
    if detect_shell_intent(query):
        return {
            "tier": "shell",
            "method": "ghost-detection",
            "tokens_est": tokens,
            "keyword_tier": "shell",
            "keyword_confidence": 1.0,
            "token_tier": token_tier,
            "sentences": sentences,
            "timestamp": datetime.now().isoformat(),
        }

5. In BootstrapRouter.route(), add after the tier assignment:

    # Ghost routing — bypass Ollama entirely
    if analysis["tier"] == "shell":
        self.visual("Routing to Shell Ghost", "route")
        self.visual("Processing locally ($0.00)", "cost")
        
        ghost_result = self.ghost.process(
            query, confirm_destructive=("confirm" in query.lower())
        )
        
        if ghost_result.get("success") or ghost_result.get("error") == "sudo_confirm":
            self.visual("Ghost complete", "success")
        else:
            self.visual(f"Ghost: {ghost_result.get('error', '?')}", "warn")
        
        full_result = {
            "analysis": analysis,
            "generation": {
                "response": ghost_result.get("message", ""),
                "duration_sec": ghost_result.get("duration_sec", 0),
                "model": "shell-ghost",
                "node": "ghost",
                "success": ghost_result.get("success", False),
            },
            "routed_to": "ghost",
            "timestamp": datetime.now().isoformat(),
            "cost": 0.0,
        }
        self._log_decision(full_result)
        return full_result

6. In routing-config.yaml, add under nodes:

    ghost:
      name: "Shell Ghost"
      host: "localhost"
      port: null
      compute: "shell"
      models:
        - name: "shell-ghost"
          role: "command-execution"
          priority: 1
      max_tokens_comfortable: 0
      latency_ceiling_sec: 30
      tier: "shell"

7. In routing-config.yaml, add to routing_rules.keywords:

    shell:
      - "check ports"
      - "check disk"
      - "update packages"
      - "restart service"
      - "show logs"
      - "list files"
      - "system status"
      - "ollama status"
      - "git status"

═══════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(INTEGRATION_GUIDE)
