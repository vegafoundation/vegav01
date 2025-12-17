import time
from datetime import datetime
from agents.ae_agent import AEAgent
from agents.micro_agent import MicroAgent
from agents.ae_cross_agent import AECrossAgent
from vtc.time_crystal import TimeCrystal


class InfinityLoopOrchestrator:
    """
    VEGA Infinity Loop Orchestrator
    
    Manages the 3-5-8 iteration cycle for system optimization:
    - Iteration 3: Initial Resonance Analysis
    - Iteration 5: Optimization & Cross-Module Integration
    - Iteration 8: Stabilization & Full System Activation
    
    The orchestrator coordinates all agents and maintains system coherence.
    """
    
    PHASE_3 = "resonance_analysis"
    PHASE_5 = "optimization"
    PHASE_8 = "stabilization"
    
    def __init__(self, time_crystal=None):
        self.time_crystal = time_crystal or TimeCrystal()
        self.current_iteration = 0
        self.phase = "idle"
        self.agents = {}
        self.is_running = False
        self.cycle_count = 0
        
        self.ae_agent = AEAgent("AE-Master", self.time_crystal)
        self.cross_agent = AECrossAgent("Æ-Orchestrator", self.time_crystal)
        
        self.agents["AE-Master"] = self.ae_agent
        self.agents["Æ-Orchestrator"] = self.cross_agent
        
        self._log("Infinity Loop Orchestrator initialized")
    
    def _log(self, message):
        """Log orchestrator activity"""
        self.time_crystal.log_event("orchestrator", {
            "message": message,
            "iteration": self.current_iteration,
            "phase": self.phase,
            "cycle": self.cycle_count
        }, source="InfinityLoop")
    
    def register_agent(self, agent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        self.cross_agent.register_module(agent.name)
        self._log(f"Registered agent: {agent.name}")
    
    def create_micro_agent(self, name, specialty):
        """Create and register a new MicroAgent"""
        agent = MicroAgent(name, specialty, self.time_crystal)
        self.register_agent(agent)
        return agent
    
    def run_iteration(self, iteration_number):
        """Run a single iteration of the Infinity Loop"""
        self.current_iteration = iteration_number
        
        if iteration_number == 3:
            return self._phase_resonance_analysis()
        elif iteration_number == 5:
            return self._phase_optimization()
        elif iteration_number == 8:
            return self._phase_stabilization()
        else:
            return self._phase_intermediate(iteration_number)
    
    def _phase_resonance_analysis(self):
        """Phase 3: Initial Resonance Analysis"""
        self.phase = self.PHASE_3
        self.time_crystal.update_infinity_loop(3, self.PHASE_3)
        self._log("Starting Phase 3: Resonance Analysis")
        
        system_analysis = self.ae_agent.analyze_system_state()
        
        agent_resonance = {}
        for name, agent in self.agents.items():
            status = agent.get_status()
            agent_resonance[name] = {
                "status": status["state"].get("status", "unknown"),
                "decisions": status["state"].get("decisions_made", 0),
                "messages": status["state"].get("messages_sent", 0)
            }
        
        result = {
            "phase": self.PHASE_3,
            "iteration": 3,
            "system_analysis": system_analysis,
            "agent_resonance": agent_resonance,
            "timestamp": datetime.now().isoformat()
        }
        
        self._log("Phase 3 complete: Resonance analyzed")
        return result
    
    def _phase_optimization(self):
        """Phase 5: Optimization & Cross-Module Integration"""
        self.phase = self.PHASE_5
        self.time_crystal.update_infinity_loop(5, self.PHASE_5)
        self._log("Starting Phase 5: Optimization")
        
        for name, agent in self.agents.items():
            if hasattr(agent, 'update_resonance'):
                agent.update_resonance(1.5)
        
        all_agents = list(self.agents.values())
        self.cross_agent.broadcast("Optimization phase initiated", all_agents)
        
        optimization_actions = []
        for name, agent in self.agents.items():
            messages = agent.process_pending_messages()
            optimization_actions.append({
                "agent": name,
                "processed_messages": len(messages)
            })
        
        result = {
            "phase": self.PHASE_5,
            "iteration": 5,
            "optimization_actions": optimization_actions,
            "cross_module_status": self.cross_agent.get_relay_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
        self._log("Phase 5 complete: System optimized")
        return result
    
    def _phase_stabilization(self):
        """Phase 8: Stabilization & Full System Activation"""
        self.phase = self.PHASE_8
        self.time_crystal.update_infinity_loop(8, self.PHASE_8)
        self._log("Starting Phase 8: Stabilization")
        
        for name, agent in self.agents.items():
            agent.state["status"] = "stable"
            agent._save_state()
        
        final_analysis = self.ae_agent.analyze_system_state()
        
        self.cycle_count += 1
        
        result = {
            "phase": self.PHASE_8,
            "iteration": 8,
            "system_stable": True,
            "cycle_completed": self.cycle_count,
            "final_analysis": final_analysis,
            "active_agents": len(self.agents),
            "timestamp": datetime.now().isoformat()
        }
        
        self._log(f"Phase 8 complete: System stabilized (Cycle {self.cycle_count})")
        return result
    
    def _phase_intermediate(self, iteration):
        """Handle intermediate iterations (1, 2, 4, 6, 7)"""
        self.phase = f"intermediate_{iteration}"
        self.time_crystal.update_infinity_loop(iteration, self.phase)
        
        return {
            "phase": self.phase,
            "iteration": iteration,
            "status": "intermediate_processing",
            "timestamp": datetime.now().isoformat()
        }
    
    def run_full_cycle(self):
        """Run a complete 3-5-8 Infinity Loop cycle"""
        self._log("Starting full 3-5-8 cycle")
        self.is_running = True
        
        results = []
        
        for i in range(1, 9):
            result = self.run_iteration(i)
            results.append(result)
            
            if i in [3, 5, 8]:
                time.sleep(0.1)
        
        self.is_running = False
        self.phase = "cycle_complete"
        
        cycle_summary = {
            "cycle_number": self.cycle_count,
            "iterations": results,
            "total_agents": len(self.agents),
            "completed_at": datetime.now().isoformat()
        }
        
        self._log(f"Cycle {self.cycle_count} completed")
        return cycle_summary
    
    def get_status(self):
        """Get current orchestrator status"""
        return {
            "is_running": self.is_running,
            "current_iteration": self.current_iteration,
            "phase": self.phase,
            "cycle_count": self.cycle_count,
            "registered_agents": list(self.agents.keys()),
            "infinity_loop_status": self.time_crystal.get_infinity_loop_status()
        }
    
    def get_all_agent_statuses(self):
        """Get status of all registered agents"""
        return {name: agent.get_status() for name, agent in self.agents.items()}
