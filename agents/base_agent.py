import os
import json
from datetime import datetime
from abc import ABC, abstractmethod
from vtc.time_crystal import TimeCrystal

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = os.environ.get("OPENAI_API_KEY") is not None
    if OPENAI_AVAILABLE:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    else:
        openai_client = None
except ImportError:
    OPENAI_AVAILABLE = False
    openai_client = None


class BaseAgent(ABC):
    """
    Base class for all VEGA agents.
    Provides core functionality for decision-making, communication, and learning.
    """
    
    def __init__(self, name, agent_type="base", time_crystal=None):
        self.name = name
        self.agent_type = agent_type
        self.state = {
            "status": "initialized",
            "created": datetime.now().isoformat(),
            "last_action": None,
            "decisions_made": 0,
            "messages_sent": 0,
            "messages_received": 0
        }
        self.time_crystal = time_crystal or TimeCrystal()
        self.message_queue = []
        self._save_state()
    
    def _save_state(self):
        """Save current agent state to Time Crystal"""
        self.time_crystal.store(self.name, {
            "type": self.agent_type,
            "state": self.state
        }, category="agents")
    
    def _log_event(self, event_type, data):
        """Log an event to the Time Crystal"""
        self.time_crystal.log_event(event_type, data, source=self.name)
    
    def _get_ai_response(self, prompt, system_prompt=None):
        """Get AI-powered response using OpenAI (if available)"""
        if not OPENAI_AVAILABLE or openai_client is None:
            return f"[Simulated AI Response for: {prompt[:50]}...]"
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = openai_client.chat.completions.create(
                model="gpt-5",
                messages=messages,
                max_completion_tokens=512
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[AI Error: {str(e)}]"
    
    @abstractmethod
    def decision(self, data) -> dict:
        """Make a decision based on input data"""
        ...
    
    def communicate(self, message, target_agent):
        """Send a message to another agent"""
        event = {
            "from": self.name,
            "to": target_agent.name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.time_crystal.log_communication(self.name, target_agent.name, message)
        target_agent.receive(message, self)
        
        self.state["messages_sent"] += 1
        self.state["last_action"] = f"Sent message to {target_agent.name}"
        self._save_state()
        
        return event
    
    def receive(self, message, sender):
        """Receive a message from another agent"""
        self.message_queue.append({
            "from": sender.name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        self.state["messages_received"] += 1
        self._save_state()
        
        self._log_event("message_received", {
            "from": sender.name,
            "message": message[:100] if len(message) > 100 else message
        })
    
    def learn(self, feedback):
        """Update internal state based on feedback"""
        self.state["last_feedback"] = feedback
        self.state["last_action"] = "Processed feedback"
        self._save_state()
        
        self._log_event("learning", {"feedback": feedback})
    
    def get_status(self):
        """Get current agent status"""
        return {
            "name": self.name,
            "type": self.agent_type,
            "state": self.state,
            "pending_messages": len(self.message_queue)
        }
    
    def process_pending_messages(self):
        """Process all pending messages"""
        processed = []
        while self.message_queue:
            msg = self.message_queue.pop(0)
            processed.append(msg)
        return processed
