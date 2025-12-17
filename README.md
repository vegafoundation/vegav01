# VEGA Agent Orchestration System

A fully autonomous multi-agent platform with modular architecture, persistent Time Crystal storage, and infinity loop coordination.

## Overview

VEGA is a meta-system that orchestrates multiple AI agents working together. The system includes:

- **AE-Agent**: Core decision-making agent with AI-powered analysis
- **MicroAgents**: Specialized task-specific agents (DataProcessor, TaskRunner, HealthMonitor, CreativeAssist)
- **Æ-Agent (Cross-Agent)**: Handles inter-agent communication and event relay
- **Time Crystal (VTC)**: Persistent storage for all agent states, events, and system history
- **Infinity Loop**: 3-5-8 iteration cycle for continuous optimization

## Project Structure

```
/vega-replit-prototype
├── agents/
│   ├── base_agent.py      # Base agent class
│   ├── ae_agent.py        # Core decision-making agent
│   ├── micro_agent.py     # Task-specific agents
│   ├── ae_cross_agent.py  # Cross-module communication
│   └── orchestrator.py    # Infinity Loop orchestrator
├── modules/
│   ├── base_module.py     # Base module class
│   └── (future modules)
├── vtc/
│   ├── time_crystal.py    # Time Crystal persistence
│   └── time_crystal.json  # Persistent data store
├── configs/
│   ├── agents_config.yaml # Agent configurations
│   └── modules_config.yaml# Module configurations
├── web/
│   ├── app.py             # Flask web dashboard
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│       └── style.css
├── scripts/
│   ├── initialize_agents.py
│   └── git_sync.sh
└── main.py                # Main entry point
```

## The 3-5-8 Infinity Loop

The system operates on a continuous optimization cycle:

1. **Iteration 3 - Resonance Analysis**: Analyzes all agent states and system resonance
2. **Iteration 5 - Optimization**: Optimizes communication and resource allocation
3. **Iteration 8 - Stabilization**: Stabilizes the system and activates full orchestration

## Getting Started

1. Start the system:
   ```bash
   python main.py
   ```

2. Access the dashboard at `http://localhost:5000`

3. Use the dashboard to:
   - View agent statuses
   - Run Infinity Loop cycles
   - Monitor Time Crystal data
   - Trigger agent decisions

## API Endpoints

- `GET /api/status` - System status
- `GET /api/agents` - All agent information
- `GET /api/events` - Recent events
- `GET /api/vtc` - Time Crystal data
- `POST /api/infinity-loop/run` - Run full 3-5-8 cycle
- `POST /api/infinity-loop/iteration/<n>` - Run specific iteration (3, 5, or 8)
- `POST /api/agent/<name>/decision` - Trigger agent decision

## Configuration

Edit YAML files in `/configs` to customize:
- Agent parameters and specialties
- Module settings
- Infinity Loop behavior
- AI integration settings

## Future Modules (Planned)

- VEGA Health - Wellness monitoring
- VEGA Creative Hub - Creative assistance
- VEGA Finance - Financial analysis
- VEGA BioLab - Biological simulations

## License

Open source - VEGA Meta-System
