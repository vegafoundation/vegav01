from agents.base_agent import BaseAgent
from datetime import datetime


class AEAgent(BaseAgent):
    """
    AE-Agent: Core Decision-Making Agent
    
    The AE-Agent is the primary decision-making entity in the VEGA system.
    It processes complex inputs, makes strategic decisions, and coordinates
    with other agents through the Time Crystal.
    """
    
    def __init__(self, name="AE-Agent", time_crystal=None):
        super().__init__(name, agent_type="AE-Agent", time_crystal=time_crystal)
        self.decision_history = []
        self.resonance_level = 1.0
    
    def decision(self, data, use_ai=True):
        """
        Make a core decision based on input data.
        Uses AI when available for enhanced decision-making.
        """
        self.state["status"] = "processing"
        self._save_state()
        
        if use_ai:
            system_prompt = """You are VEGA AE-Agent, a core decision-making AI.
            Analyze the input and provide a structured decision with:
            1. Analysis summary
            2. Recommended action
            3. Confidence level (0-100)
            Respond in JSON format."""
            
            ai_response = self._get_ai_response(
                f"Analyze and decide on: {data}",
                system_prompt
            )
            decision_result = {
                "input": data,
                "analysis": ai_response,
                "timestamp": datetime.now().isoformat(),
                "resonance": self.resonance_level
            }
        else:
            decision_result = {
                "input": data,
                "analysis": f"Processed: {data}",
                "action": "Standard processing complete",
                "timestamp": datetime.now().isoformat(),
                "resonance": self.resonance_level
            }
        
        self.decision_history.append(decision_result)
        self.state["decisions_made"] += 1
        self.state["last_decision"] = decision_result
        self.state["status"] = "ready"
        self._save_state()
        
        self._log_event("decision_made", {
            "input": str(data)[:100],
            "decision_count": self.state["decisions_made"]
        })
        
        return decision_result
    
    def update_resonance(self, level):
        """Update the resonance level for decision-making"""
        self.resonance_level = max(0.1, min(10.0, level))
        self.state["resonance_level"] = self.resonance_level
        self._save_state()
    
    def coordinate(self, agents, task):
        """Coordinate multiple agents for a complex task"""
        coordination_plan = {
            "task": task,
            "agents": [a.name for a in agents],
            "timestamp": datetime.now().isoformat()
        }
        
        for agent in agents:
            self.communicate(f"Task assignment: {task}", agent)
        
        self._log_event("coordination", coordination_plan)
        return coordination_plan
    
    def analyze_system_state(self):
        """Analyze the overall system state from Time Crystal data"""
        agent_states = self.time_crystal.get_agent_states()
        events = self.time_crystal.get_recent_events(50)
        loop_status = self.time_crystal.get_infinity_loop_status()
        
        analysis = {
            "total_agents": len(agent_states),
            "recent_events": len(events),
            "infinity_loop_phase": loop_status.get("phase", "unknown"),
            "current_iteration": loop_status.get("current_iteration", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        return analysis
