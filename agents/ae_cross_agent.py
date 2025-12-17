from agents.base_agent import BaseAgent
from datetime import datetime


class AECrossAgent(BaseAgent):
    """
    Æ-Agent (AE-Cross-Agent): Cross-Module Communication Agent
    
    The Æ-Agent handles communication and event relay between different
    modules and agent groups. It serves as the communication backbone
    of the VEGA system.
    """
    
    def __init__(self, name="Æ-Agent", time_crystal=None):
        super().__init__(name, agent_type="AE-Cross-Agent", time_crystal=time_crystal)
        self.event_queue = []
        self.relay_history = []
        self.connected_modules = set()
    
    def decision(self, data, use_ai=False):
        """Decide how to route/relay information"""
        self.state["status"] = "routing"
        self._save_state()
        
        routing_decision = {
            "data": data,
            "action": "relay",
            "priority": self._determine_priority(data),
            "timestamp": datetime.now().isoformat()
        }
        
        self.state["decisions_made"] += 1
        self.state["last_decision"] = routing_decision
        self.state["status"] = "ready"
        self._save_state()
        
        return routing_decision
    
    def _determine_priority(self, data):
        """Determine the priority of a message/event"""
        if isinstance(data, dict):
            if data.get("urgent") or data.get("priority") == "high":
                return "high"
            if data.get("priority") == "low":
                return "low"
        return "normal"
    
    def relay(self, event, target_agents=None):
        """Relay an event to target agents or broadcast"""
        relay_record = {
            "event": event,
            "targets": [a.name for a in target_agents] if target_agents else "broadcast",
            "timestamp": datetime.now().isoformat()
        }
        
        self.relay_history.append(relay_record)
        self.event_queue.append(event)
        
        if target_agents:
            for agent in target_agents:
                self.communicate(f"Relayed event: {event}", agent)
        
        self._log_event("relay", {
            "event_type": type(event).__name__,
            "targets": relay_record["targets"]
        })
        
        return relay_record
    
    def broadcast(self, message, agents):
        """Broadcast a message to all agents"""
        broadcast_record = {
            "message": message,
            "recipients": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for agent in agents:
            self.communicate(message, agent)
            broadcast_record["recipients"].append(agent.name)
        
        self._log_event("broadcast", {
            "message": message[:100] if len(message) > 100 else message,
            "recipient_count": len(agents)
        })
        
        return broadcast_record
    
    def register_module(self, module_name):
        """Register a module for cross-communication"""
        self.connected_modules.add(module_name)
        self.state["connected_modules"] = list(self.connected_modules)
        self._save_state()
        
        self._log_event("module_registered", {"module": module_name})
    
    def get_event_queue(self):
        """Get pending events in the queue"""
        return self.event_queue.copy()
    
    def clear_event_queue(self):
        """Clear the event queue after processing"""
        cleared_count = len(self.event_queue)
        self.event_queue = []
        return cleared_count
    
    def get_relay_stats(self):
        """Get statistics about relay operations"""
        return {
            "total_relays": len(self.relay_history),
            "pending_events": len(self.event_queue),
            "connected_modules": list(self.connected_modules),
            "recent_relays": self.relay_history[-10:] if self.relay_history else []
        }
