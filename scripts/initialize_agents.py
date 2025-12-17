#!/usr/bin/env python3
"""
VEGA Agent Initialization Script

This script initializes all core VEGA agents and runs the Infinity Loop.
Can be used standalone or imported as a module.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import AEAgent, MicroAgent, AECrossAgent
from agents.orchestrator import InfinityLoopOrchestrator
from vtc.time_crystal import TimeCrystal


def initialize_vega_system():
    """Initialize the complete VEGA agent system"""
    print("=" * 60)
    print("VEGA AGENT ORCHESTRATION SYSTEM")
    print("Initializing Meta-System...")
    print("=" * 60)
    
    time_crystal = TimeCrystal()
    print("[VTC] Time Crystal initialized")
    
    orchestrator = InfinityLoopOrchestrator(time_crystal)
    print("[ORCH] Infinity Loop Orchestrator initialized")
    
    data_processor = orchestrator.create_micro_agent("DataProcessor", "data_processing")
    task_runner = orchestrator.create_micro_agent("TaskRunner", "task_execution")
    health_monitor = orchestrator.create_micro_agent("HealthMonitor", "health_monitoring")
    creative_assist = orchestrator.create_micro_agent("CreativeAssist", "creative")
    
    print(f"[AGENTS] {len(orchestrator.agents)} agents registered:")
    for name in orchestrator.agents.keys():
        print(f"  - {name}")
    
    return orchestrator, time_crystal


def run_demo_cycle(orchestrator):
    """Run a demonstration of the Infinity Loop"""
    print("\n" + "=" * 60)
    print("RUNNING 3-5-8 INFINITY LOOP CYCLE")
    print("=" * 60)
    
    result = orchestrator.run_full_cycle()
    
    print(f"\n[COMPLETE] Cycle {result['cycle_number']} completed")
    print(f"  - Total agents: {result['total_agents']}")
    print(f"  - Completed at: {result['completed_at']}")
    
    return result


def main():
    """Main entry point"""
    orchestrator, time_crystal = initialize_vega_system()
    
    status = orchestrator.get_status()
    print(f"\n[STATUS]")
    print(f"  - Registered agents: {len(status['registered_agents'])}")
    print(f"  - Current phase: {status['phase']}")
    print(f"  - Cycles completed: {status['cycle_count']}")
    
    run_demo = input("\nRun demo Infinity Loop cycle? (y/n): ").strip().lower()
    if run_demo == 'y':
        run_demo_cycle(orchestrator)
    
    print("\n[READY] VEGA System initialized and ready")
    print("Access the dashboard at: http://0.0.0.0:5000")
    
    return orchestrator


if __name__ == "__main__":
    main()
