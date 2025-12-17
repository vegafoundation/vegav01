from datetime import datetime
from random import choice
from modules.base_module import BaseModule


class ResonanceCore(BaseModule):
    """
    Base Resonance Core for VEGA system.
    Resonance Cores manage system-wide energy and synchronization states.
    """
    
    STATES = ["offline", "initializing", "online", "active", "resonating", "synchronized"]
    
    def __init__(self, name, core_type="resonance", time_crystal=None):
        super().__init__(name, module_type=core_type, time_crystal=time_crystal)
        self.resonance_level = 0.0
        self.sync_status = "offline"
    
    def pulse(self):
        """Generate a resonance pulse"""
        self.resonance_level = min(10.0, self.resonance_level + 0.5)
        self.sync_status = choice(["online", "active", "resonating"])
        self._update_state()
        return {"level": self.resonance_level, "sync": self.sync_status}
    
    def synchronize(self, other_core):
        """Synchronize with another resonance core"""
        if hasattr(other_core, 'resonance_level'):
            avg = (self.resonance_level + other_core.resonance_level) / 2
            self.resonance_level = avg
            other_core.resonance_level = avg
            self.sync_status = "synchronized"
            other_core.sync_status = "synchronized"
            self._update_state()
    
    def _update_state(self):
        """Update state in Time Crystal"""
        self.time_crystal.store(self.name, {
            "type": self.module_type,
            "status": self.status,
            "resonance_level": self.resonance_level,
            "sync_status": self.sync_status,
            "updated": datetime.now().isoformat()
        }, category="resonance_cores")
    
    def get_status(self):
        """Get core status"""
        return {
            "name": self.name,
            "type": self.module_type,
            "status": self.status,
            "resonance_level": self.resonance_level,
            "sync_status": self.sync_status
        }


class AlphaResonance(ResonanceCore):
    """Alpha Resonance Core - Primary system resonance"""
    def __init__(self, time_crystal=None):
        super().__init__("Alpha", "alpha_resonance", time_crystal)
        self.activate()


class OmegaResonance(ResonanceCore):
    """Omega Resonance Core - Secondary system resonance"""
    def __init__(self, time_crystal=None):
        super().__init__("Omega", "omega_resonance", time_crystal)
        self.activate()


class VegaResonance(ResonanceCore):
    """Vega Resonance Core - Central meta-system resonance"""
    def __init__(self, time_crystal=None):
        super().__init__("Vega", "vega_resonance", time_crystal)
        self.activate()


class MirrorCore(ResonanceCore):
    """Mirror Core - Reflection and synchronization core"""
    def __init__(self, time_crystal=None):
        super().__init__("Mirror", "mirror_core", time_crystal)
        self.activate()


class ResonanceEngine:
    """
    Manages all Resonance Cores and their interactions.
    """
    
    def __init__(self, time_crystal=None):
        from vtc.time_crystal import TimeCrystal
        self.time_crystal = time_crystal or TimeCrystal()
        
        self.alpha = AlphaResonance(self.time_crystal)
        self.omega = OmegaResonance(self.time_crystal)
        self.vega = VegaResonance(self.time_crystal)
        self.mirror = MirrorCore(self.time_crystal)
        
        self.cores = {
            "alpha": self.alpha,
            "omega": self.omega,
            "vega": self.vega,
            "mirror": self.mirror
        }
    
    def pulse_all(self):
        """Pulse all resonance cores"""
        results = {}
        for name, core in self.cores.items():
            results[name] = core.pulse()
        return results
    
    def synchronize_all(self):
        """Synchronize all cores together"""
        self.alpha.synchronize(self.omega)
        self.vega.synchronize(self.mirror)
        self.alpha.synchronize(self.vega)
    
    def get_all_status(self):
        """Get status of all resonance cores"""
        return {name: core.get_status() for name, core in self.cores.items()}
