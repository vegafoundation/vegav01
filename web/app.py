import os
import json
import yaml
from datetime import datetime
from flask import Flask, render_template, jsonify, request

from vtc.time_crystal import TimeCrystal
from agents.orchestrator import InfinityLoopOrchestrator

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vega-dev-secret-key")

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

time_crystal = TimeCrystal()
orchestrator = None


def get_orchestrator():
    """Get or create the orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        orchestrator = InfinityLoopOrchestrator(time_crystal)
        orchestrator.create_micro_agent("BioLab", "biolab_simulation")
        orchestrator.create_micro_agent("CreativeHub", "creative_generation")
        orchestrator.create_micro_agent("FinanceCore", "finance_analysis")
        orchestrator.create_micro_agent("HealthMonitor", "health_monitoring")
        orchestrator.create_micro_agent("Playbox", "experimental")
        orchestrator.create_micro_agent("Atlas", "mapping_navigation")
    return orchestrator


@app.after_request
def add_header(response):
    """Disable caching for development"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route("/")
def landing():
    """VEGA.foundation landing page"""
    return render_template("landing.html")


@app.route("/dashboard")
def dashboard():
    """Agent orchestration dashboard"""
    orch = get_orchestrator()
    data = {
        "vtc_data": time_crystal.get_all_data(),
        "orchestrator_status": orch.get_status(),
        "agent_statuses": orch.get_all_agent_statuses(),
        "resonance_cores": orch.get_resonance_status(),
        "recent_events": time_crystal.get_recent_events(20),
        "infinity_loop": time_crystal.get_infinity_loop_status()
    }
    return render_template("dashboard.html", data=data)


@app.route("/api/status")
def api_status():
    """API endpoint for system status"""
    orch = get_orchestrator()
    return jsonify({
        "status": "operational",
        "orchestrator": orch.get_status(),
        "agents": orch.get_all_agent_statuses(),
        "resonance_cores": orch.get_resonance_status(),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/resonance")
def api_resonance():
    """API endpoint for resonance core status"""
    orch = get_orchestrator()
    return jsonify({
        "cores": orch.get_resonance_status(),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/resonance/pulse", methods=["POST"])
def api_pulse_resonance():
    """API endpoint to pulse all resonance cores"""
    orch = get_orchestrator()
    result = orch.pulse_resonance()
    return jsonify({
        "success": True,
        "result": result
    })


@app.route("/api/agents")
def api_agents():
    """API endpoint for agent information"""
    orch = get_orchestrator()
    return jsonify({
        "agents": orch.get_all_agent_statuses(),
        "count": len(orch.agents)
    })


@app.route("/api/events")
def api_events():
    """API endpoint for recent events"""
    limit = request.args.get("limit", 50, type=int)
    events = time_crystal.get_recent_events(limit)
    return jsonify({
        "events": events,
        "count": len(events)
    })


@app.route("/api/vtc")
def api_vtc():
    """API endpoint for Time Crystal data"""
    return jsonify(time_crystal.get_all_data())


@app.route("/api/infinity-loop/status")
def api_infinity_loop_status():
    """API endpoint for Infinity Loop status"""
    orch = get_orchestrator()
    return jsonify({
        "status": orch.get_status(),
        "loop_data": time_crystal.get_infinity_loop_status()
    })


@app.route("/api/infinity-loop/run", methods=["POST"])
def api_run_infinity_loop():
    """API endpoint to run a full Infinity Loop cycle"""
    orch = get_orchestrator()
    if orch.is_running:
        return jsonify({"error": "Infinity Loop is already running"}), 400
    
    result = orch.run_full_cycle()
    return jsonify({
        "success": True,
        "result": result
    })


@app.route("/api/infinity-loop/iteration/<int:iteration>", methods=["POST"])
def api_run_iteration(iteration):
    """API endpoint to run a specific iteration"""
    if iteration not in [3, 5, 8]:
        return jsonify({"error": "Valid iterations are 3, 5, or 8"}), 400
    
    orch = get_orchestrator()
    result = orch.run_iteration(iteration)
    return jsonify({
        "success": True,
        "result": result
    })


@app.route("/api/agent/<name>/decision", methods=["POST"])
def api_agent_decision(name):
    """API endpoint to trigger an agent decision"""
    orch = get_orchestrator()
    if name not in orch.agents:
        return jsonify({"error": f"Agent '{name}' not found"}), 404
    
    data = request.json or {}
    input_data = data.get("input", "test decision request")
    
    agent = orch.agents[name]
    result = agent.decision(input_data)
    
    return jsonify({
        "success": True,
        "agent": name,
        "result": result
    })


@app.route("/api/config/agents")
def api_config_agents():
    """API endpoint for agent configuration"""
    try:
        with open("configs/agents_config.yaml", "r") as f:
            config = yaml.safe_load(f)
        return jsonify(config)
    except FileNotFoundError:
        return jsonify({"error": "Config not found"}), 404


@app.route("/api/config/modules")
def api_config_modules():
    """API endpoint for module configuration"""
    try:
        with open("configs/modules_config.yaml", "r") as f:
            config = yaml.safe_load(f)
        return jsonify(config)
    except FileNotFoundError:
        return jsonify({"error": "Config not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
