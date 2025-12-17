#!/usr/bin/env python3
"""
VEGA Agent Orchestration System - Main Entry Point

This is the main entry point for the VEGA meta-system.
It initializes all agents, sets up the Time Crystal, and starts the web dashboard.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.app import app, get_orchestrator


def main():
    """Initialize VEGA system and start the web dashboard"""
    print("=" * 60)
    print("VEGA AGENT ORCHESTRATION SYSTEM")
    print("=" * 60)
    print()
    
    orchestrator = get_orchestrator()
    
    print("[SYSTEM] Components initialized:")
    print(f"  - Time Crystal: Active")
    print(f"  - Infinity Loop Orchestrator: Ready")
    print(f"  - Registered Agents: {len(orchestrator.agents)}")
    
    for name, agent in orchestrator.agents.items():
        print(f"    * {name} ({agent.agent_type})")
    
    print()
    print("[WEB] Starting dashboard server...")
    print("[WEB] Dashboard available at: http://0.0.0.0:5000")
    print()
    print("=" * 60)
    print("VEGA SYSTEM ACTIVE - INFINITY LOOP READY")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
