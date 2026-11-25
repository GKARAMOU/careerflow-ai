# CareerFlow

CareerFlow is a polished job-search command center for tracking applications, prioritizing next steps and measuring resume-to-role alignment. It is intentionally built as a portfolio project around technologies commonly requested in modern software roles.

[Open the live interactive demo](https://gkaramou.github.io/careerflow-ai/)

![CareerFlow dashboard](docs/careerflow-dashboard.png)

## Why this project matters

- A complete React + TypeScript product interface, not an API-only demo
- FastAPI backend with typed schemas and OpenAPI documentation
- PostgreSQL persistence through async SQLAlchemy
- JWT authentication and Argon2 password hashing
- User-scoped application data and fit analysis
- Pytest coverage, Docker Compose and GitHub Actions CI
- Responsive dashboard with a functional add-application workflow

## Run the interface

```bash
npm ci
npm run dev
```

Open `http://localhost:5173`.

The GitHub Pages deployment is a browser-only interactive demo using sample data. You can add, search, filter and select applications; changes last only until the page is refreshed. Scores and insights are examples, not AI predictions. The frontend is not yet connected to the backend. Docker Compose starts the API and PostgreSQL independently for API exploration.

## Run the full stack

```bash
docker compose up --build
```

- Web UI: `http://localhost:8080`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Backend tests

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Architecture

```text
React + TypeScript UI (browser demo; not connected to API)

FastAPI application
        |
        | async SQLAlchemy
        v
PostgreSQL
```

## Production roadmap

- Add Alembic migrations and refresh-token rotation
- Connect the UI to the authenticated API
- Replace lexical fit scoring with an embedding service
- Add scheduled reminders and calendar integration
- Deploy frontend and API separately with managed PostgreSQL

## Security

Development defaults are included only for local setup. Production secrets must be injected through the deployment platform. Passwords are Argon2-hashed and application queries are scoped to the authenticated user.

## License

MIT
