import json
import os
import time
from datetime import datetime
from threading import Lock

class TimeCrystal:
    """
    VEGA Time Crystal (VTC) - Persistent storage system for all agent states,
    actions, feedback loops, and system events.
    
    The Time Crystal maintains a chronological record of all system activity,
    enabling state persistence, historical analysis, and system recovery.
    """
    
    def __init__(self, path="vtc/time_crystal.json"):
        self.path = path
        self.lock = Lock()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the Time Crystal storage file exists"""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            initial_data = {
                "meta": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "system": "VEGA Time Crystal"
                },
                "agents": {},
                "events": [],
                "communications": [],
                "infinity_loop": {
                    "current_iteration": 0,
                    "phase": "idle",
                    "history": []
                },
                "modules": {}
            }
            self._write_data(initial_data)
    
    def _read_data(self):
        """Read all data from the Time Crystal"""
        with self.lock:
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
    
    def _write_data(self, data):
        """Write data to the Time Crystal"""
        with self.lock:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4, default=str)
    
    def store(self, key, data, category="agents"):
        """Store data in a specific category of the Time Crystal"""
        current = self._read_data()
        if category not in current:
            current[category] = {}
        
        if isinstance(current[category], dict):
            current[category][key] = {
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
        elif isinstance(current[category], list):
            current[category].append({
                "key": key,
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
        
        self._write_data(current)
    
    def retrieve(self, key, category="agents"):
        """Retrieve data from the Time Crystal"""
        current = self._read_data()
        if category in current and isinstance(current[category], dict):
            entry = current[category].get(key)
            if entry:
                return entry.get("data")
        return None
    
    def log_event(self, event_type, data, source="system"):
        """Log an event to the Time Crystal"""
        current = self._read_data()
        if "events" not in current:
            current["events"] = []
        
        event = {
            "type": event_type,
            "source": source,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        current["events"].append(event)
        
        if len(current["events"]) > 1000:
            current["events"] = current["events"][-500:]
        
        self._write_data(current)
        return event
    
    def log_communication(self, from_agent, to_agent, message):
        """Log inter-agent communication"""
        current = self._read_data()
        if "communications" not in current:
            current["communications"] = []
        
        comm = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        current["communications"].append(comm)
        
        if len(current["communications"]) > 500:
            current["communications"] = current["communications"][-250:]
        
        self._write_data(current)
        return comm
    
    def update_infinity_loop(self, iteration, phase, data=None):
        """Update the Infinity Loop state"""
        current = self._read_data()
        if "infinity_loop" not in current:
            current["infinity_loop"] = {"current_iteration": 0, "phase": "idle", "history": []}
        
        current["infinity_loop"]["current_iteration"] = iteration
        current["infinity_loop"]["phase"] = phase
        current["infinity_loop"]["history"].append({
            "iteration": iteration,
            "phase": phase,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(current["infinity_loop"]["history"]) > 100:
            current["infinity_loop"]["history"] = current["infinity_loop"]["history"][-50:]
        
        self._write_data(current)
    
    def get_all_data(self):
        """Get all Time Crystal data"""
        return self._read_data()
    
    def get_agent_states(self):
        """Get all agent states"""
        data = self._read_data()
        return data.get("agents", {})
    
    def get_recent_events(self, limit=20):
        """Get recent events"""
        data = self._read_data()
        events = data.get("events", [])
        return events[-limit:] if events else []
    
    def get_infinity_loop_status(self):
        """Get current Infinity Loop status"""
        data = self._read_data()
        return data.get("infinity_loop", {})
    
    def clear(self):
        """Clear all Time Crystal data (use with caution)"""
        self._ensure_file_exists()
