# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack trading application with microservices architecture:
- **sin-trade-fe**: React + TypeScript frontend (Vite)
- **sin-trade-be**: Flask backend API (Python 3.12)
- **sin-trade-ds**: Flask data science service (Python 3.12)

Services communicate via RabbitMQ (CloudAMQP) message queues and share a Supabase database.

## Development Setup

### Initial Setup
```bash
# Install version managers (if needed)
asdf plugin add nodejs && asdf plugin add python
asdf install python 3.12.4 && asdf global python 3.12.4
asdf install nodejs 22.1.0 && asdf global nodejs 22.1.0
brew install pnpm

# Frontend setup
cd sin-trade-fe
pnpm install

# Backend virtual environments (important for VSCode launch.json)
python -m venv sin-trade-be/be-venv
source sin-trade-be/be-venv/bin/activate
pip install -r sin-trade-be/requirements.txt
deactivate

python -m venv sin-trade-ds/ds-venv
source sin-trade-ds/ds-venv/bin/activate
pip install -r sin-trade-ds/requirements.txt
deactivate
```

### Running Tests

Backend (BE):
```bash
source sin-trade-be/be-venv/bin/activate
cd sin-trade-be
pytest
```

Data Science (DS):
```bash
source sin-trade-ds/ds-venv/bin/activate
cd sin-trade-ds
pytest
```

Frontend:x
```bash
cd sin-trade-fe
pnpm test
```

### Running Services

Frontend:
```bash
cd sin-trade-fe
pnpm start          # Development server on port 5173
pnpm build          # Build for production
pnpm lint           # Run ESLint
```

Backend services run via Flask with APScheduler and background threads:
- BE: Port 5002
- DS: Port 5004

Use the VSCode compound configurations in `.vscode/launch.json`:
- "Run Full App" - starts all three services
- "Run Frontend" - starts frontend server and Chrome debugger

## Architecture

### Message Queue System

The application uses RabbitMQ for asynchronous communication between services:

**Queues:**
- `stock_queue`: BE → DS (stock asset processing requests)
- `crypto_queue`: BE → DS (crypto asset processing requests)
- `email_queue`: DS → BE (email notification requests)

**Publishers:**
- BE publishes to: `stock_queue`, `crypto_queue`
- DS publishes to: `email_queue`

**Subscribers:**
- BE subscribes to: `email_queue`
- DS subscribes to: `stock_queue`, `crypto_queue`

Queue handling:
- `amqp_*_publisher.py`: Publishes messages to queues
- `amqp_*_subscriber.py`: Consumes messages in background threads with dedicated callbacks
- `declare_queues()`: Called on service startup to ensure queues exist
- `subscribe_to_queues()`: Starts daemon threads for message consumption

### Backend (sin-trade-be)

Structure:
- `app.py`: Flask app factory, initializes routes and background scheduler
- `config.py`: BackendConfig class with Supabase and AMQP connections
- `routes/`: Route blueprints (auth, asset, test)
- `controllers/`: Business logic layer
- `services/`: External API integrations and message queue handlers
- `models/`: Data models
- `middleware/`: Request/response middleware

On startup:
1. Declares message queues
2. Subscribes to `email_queue`
3. Starts APScheduler with processpool executor

### Data Science (sin-trade-ds)

Structure:
- `app.py`: Flask app factory with scheduled jobs
- `config.py`: DSConfig class with Supabase, AMQP, and API keys (Polygon, AlphaVantage)
- `services/`: Data fetching (alphavantage, kraken), queue handlers, job scheduler
- `routes/`: Minimal routes (health check, test)
- `models/`: Data models

On startup:
1. Declares message queues
2. Subscribes to `stock_queue` and `crypto_queue`
3. Starts APScheduler with `check_targets()` job (runs every minute)
4. `check_targets()` runs async tasks including `run_history_flow()`

**Data Flow:**
- DS service receives asset symbols via message queues
- Fetches historical data from external APIs (AlphaVantage for stocks, Kraken for crypto)
- Stores data in Supabase
- Publishes notifications to `email_queue` when needed

### Frontend (sin-trade-fe)

React application using:
- TypeScript with strict mode
- Vite for build/dev tooling
- React Router for navigation
- Tailwind CSS + HeadlessUI for styling
- Framer Motion for animations
- Vitest for testing

Structure:
- `pages/`: Route components
- `components/`: Reusable UI components
- `api/`: Backend API client code
- `context/`: React context providers
- `utils/`: Helper functions
- `interfaces/`: TypeScript type definitions

## Environment Variables

Both Python services require `.env` files:
- `SUPABASE_URL`, `SUPABASE_KEY`: Database connection
- `CLOUDAMQP_URL`: Message queue connection
- `CORS_ORIGINS`: Allowed origins (default: `http://localhost:5173`)
- `ENVIRONMENT`: `development` or `production`
- `POLYGON_KEY`, `ALPHAVANTAGE_KEY`: External API keys (DS only)

## Key Patterns

### Async/Event Loop Handling
The DS service mixes Flask (synchronous) with async data fetching. When calling async functions from sync contexts (like scheduler jobs or queue callbacks):
```python
try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.run_coroutine_threadsafe(async_function(), loop)
    else:
        loop.run_until_complete(async_function())
except RuntimeError:
    asyncio.run(async_function())
```

### Database Access
Both services use Supabase client from config:
```python
from src.config import BackendConfig  # or DSConfig
supabase = BackendConfig.supabase
```

### Message Queue Pattern
```python
# Publishing
from src.services.amqp_*_publisher import publish_message
publish_message("queue_name", message_body)

# Subscribing (in app.py startup)
from src.services.amqp_*_subscriber import subscribe_to_queues
subscribe_to_queues()  # Starts background threads
```

## Docker

`docker-compose.yml` defines all three services with health checks at `/health` endpoints.
Individual Dockerfiles in each service directory.
