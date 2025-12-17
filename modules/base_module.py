from datetime import datetime
from vtc.time_crystal import TimeCrystal


class BaseModule:
    """
    Base class for VEGA modules.
    Provides foundation for specialized modules like Health, Creative Hub, etc.
    """
    
    def __init__(self, name, module_type="base", time_crystal=None):
        self.name = name
        self.module_type = module_type
        self.status = "initialized"
        self.time_crystal = time_crystal or TimeCrystal()
        self.agents = []
        self.created_at = datetime.now().isoformat()
        
        self._register_module()
    
    def _register_module(self):
        """Register module in Time Crystal"""
        self.time_crystal.store(self.name, {
            "type": self.module_type,
            "status": self.status,
            "created_at": self.created_at,
            "agents": [a.name for a in self.agents]
        }, category="modules")
    
    def activate(self):
        """Activate the module"""
        self.status = "active"
        self._register_module()
        self.time_crystal.log_event("module_activated", {
            "module": self.name,
            "type": self.module_type
        })
    
    def deactivate(self):
        """Deactivate the module"""
        self.status = "inactive"
        self._register_module()
    
    def attach_agent(self, agent):
        """Attach an agent to this module"""
        self.agents.append(agent)
        self._register_module()
    
    def get_status(self):
        """Get module status"""
        return {
            "name": self.name,
            "type": self.module_type,
            "status": self.status,
            "agents": [a.name for a in self.agents],
            "created_at": self.created_at
        }
