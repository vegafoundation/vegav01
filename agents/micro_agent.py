from agents.base_agent import BaseAgent
from datetime import datetime


class MicroAgent(BaseAgent):
    """
    MicroAgent: Task-Specific Assistant Agent
    
    MicroAgents are lightweight, specialized agents that handle specific tasks.
    They can be spawned dynamically and report back to the AE-Agent.
    """
    
    def __init__(self, name="MicroAgent", specialty="general", time_crystal=None):
        super().__init__(name, agent_type="MicroAgent", time_crystal=time_crystal)
        self.specialty = specialty
        self.tasks_completed = 0
        self.current_task = None
    
    def decision(self, data, use_ai=False):
        """Make a task-specific decision"""
        self.state["status"] = "processing"
        self._save_state()
        
        if use_ai:
            system_prompt = f"""You are a specialized MicroAgent with expertise in: {self.specialty}.
            Process the task efficiently and provide a concise result."""
            
            result = self._get_ai_response(
                f"Process this task: {data}",
                system_prompt
            )
        else:
            result = f"[{self.specialty}] Processed: {data}"
        
        decision_result = {
            "task": data,
            "specialty": self.specialty,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
        self.state["decisions_made"] += 1
        self.state["last_decision"] = decision_result
        self.state["status"] = "ready"
        self._save_state()
        
        return decision_result
    
    def perform_task(self, task_data):
        """Perform a specific task"""
        self.current_task = task_data
        self.state["status"] = "working"
        self._save_state()
        
        result = self.decision(task_data)
        
        self.tasks_completed += 1
        self.current_task = None
        self.state["tasks_completed"] = self.tasks_completed
        self.state["status"] = "ready"
        self._save_state()
        
        self._log_event("task_completed", {
            "task": str(task_data)[:100],
            "specialty": self.specialty,
            "total_completed": self.tasks_completed
        })
        
        return result
    
    def report_to(self, agent, report_data):
        """Report task results to another agent"""
        report = {
            "from": self.name,
            "specialty": self.specialty,
            "report": report_data,
            "tasks_completed": self.tasks_completed,
            "timestamp": datetime.now().isoformat()
        }
        
        self.communicate(f"Report: {report_data}", agent)
        return report
    
    def get_specialty_info(self):
        """Get information about this agent's specialty"""
        return {
            "name": self.name,
            "specialty": self.specialty,
            "tasks_completed": self.tasks_completed,
            "current_task": self.current_task
        }
