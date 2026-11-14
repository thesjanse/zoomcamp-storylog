# StoryLog

A reading and watch journal. This repository contains a Django backend and a
Vue 3 + Vite frontend. The frontend checks the versioned API health endpoint on
load, and local development reaches the backend through a Vite proxy.

## Prerequisites

- Python 3.12 or newer
- Node.js 22.12 or newer
- [uv](https://docs.astral.sh/uv/) for the backend
- npm (ships with Node.js) for the frontend

## Running both development servers

Start the backend in one terminal, from `backend/`:

```bash
uv sync
uv run python manage.py runserver
```

Start the frontend in a second terminal, from `frontend/`:

```bash
npm install
npm run dev
```

The backend listens on <http://localhost:8000> and the Vite development server
listens on <http://localhost:5173>. Open the frontend at
<http://localhost:5173>.

Vite proxies browser requests whose path starts with `/api` to
`http://localhost:8000`, so <http://localhost:5173/api/v1/health/> reaches the
Django health endpoint without CORS configuration.

## Backend

Run these commands from `backend/`:

```bash
uv sync
uv run python manage.py runserver
uv run pytest
```

`uv sync` installs the backend dependencies from `pyproject.toml` and
`uv.lock`. The development server listens on <http://localhost:8000> by
default.

The versioned API health endpoint is `GET /api/v1/health/`. It requires no
authentication and returns HTTP 200 with a JSON body:

```json
{"status": "ok"}
```

To use environment overrides, copy the example file and edit it:

```bash
cp .env.example .env
```

`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` are read from
the environment. Development-only defaults are built into the settings, so the
backend runs without a `.env` file. Do not commit a real `.env` file or a real
secret.

## Frontend

Run these commands from `frontend/`:

```bash
npm install
npm run dev
npm test
npm run build
```

`npm install` installs the frontend dependencies from `package.json` and
`package-lock.json`. The Vite development server listens on
<http://localhost:5173> by default.

To use environment overrides, copy the example file and edit it:

```bash
cp .env.example .env
```

Local development leaves `VITE_API_BASE_URL` empty so API requests use the
relative `/api` path and go through the Vite proxy. For a production build, set
`VITE_API_BASE_URL` to the deployed backend origin, without an `/api` suffix:

```bash
VITE_API_BASE_URL=https://api.example.com npm run build
```

The health request then targets
`https://api.example.com/api/v1/health/`. Do not commit a real `.env` file or a
real secret.

## Directory layout

```text
backend/
  manage.py
  pyproject.toml
  uv.lock
  .env.example
  config/
    __init__.py
    settings.py
    urls.py
    views.py
    asgi.py
    wsgi.py
  tests/
    __init__.py
    test_home.py
    test_health.py
frontend/
  package.json
  package-lock.json
  vite.config.js
  index.html
  .env.example
  src/
    main.js
    App.vue
    App.spec.js
README.md
.gitignore
```

## Not built yet

The following are **not** built yet and are tracked by later issues:

- Journal item and note models and migrations
- Registration, login, logout, and authentication
- Product screens and the app shell

Do not assume any of these exist when working on this scaffold.
