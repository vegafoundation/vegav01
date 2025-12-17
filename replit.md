# VEGA Agent Orchestration System

## Overview
VEGA is an autonomous multi-agent orchestration platform featuring:
- Multiple AI agents (AE-Agent, MicroAgents, Æ-Agent)
- Persistent Time Crystal (VTC) storage
- 3-5-8 Infinity Loop optimization cycle
- Real-time web dashboard for monitoring

## Project Architecture

### Core Components
1. **Agents** (`/agents/`): AI agents with decision-making, communication, and learning capabilities
2. **Time Crystal** (`/vtc/`): JSON-based persistent storage for all system state
3. **Orchestrator**: Manages the 3-5-8 Infinity Loop cycle
4. **Web Dashboard** (`/web/`): Flask-based monitoring interface

### Key Files
- `main.py` - Application entry point, starts Flask server on port 5000
- `agents/orchestrator.py` - Infinity Loop implementation
- `vtc/time_crystal.py` - Persistent storage system
- `web/app.py` - Flask routes and API endpoints

## Tech Stack
- **Backend**: Python 3.11, Flask
- **Frontend**: HTML/CSS/JavaScript, Chart.js
- **AI**: OpenAI GPT-5 (optional, with fallback mode)
- **Config**: YAML for agent/module configuration
- **Storage**: JSON-based Time Crystal

## Running the Application
The application runs on port 5000. Start with:
```bash
python main.py
```

## API Reference
- `GET /` - Dashboard
- `GET /api/status` - System status
- `GET /api/agents` - Agent information
- `POST /api/infinity-loop/run` - Run 3-5-8 cycle
- `POST /api/agent/<name>/decision` - Trigger decision

## User Preferences
- Dark theme cyberpunk-style dashboard
- Real-time updates every 5 seconds
- Modular, extensible architecture

## Recent Changes
- Initial system setup with core agents
- Time Crystal persistence implemented
- 3-5-8 Infinity Loop orchestration
- Web dashboard with agent monitoring
