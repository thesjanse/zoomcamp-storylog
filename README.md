# StoryLog

A reading and watch journal. This repository currently contains only a
minimal development scaffold: a Django backend and a Vue 3 + Vite frontend,
each with one smoke test.

> **Scaffold only.** There are no journal models, authentication, API
> integration, or product screens yet. See the scope notes below for the
> issues that add them.

## Prerequisites

- Python 3.12 or newer
- Node.js 22.12 or newer
- [uv](https://docs.astral.sh/uv/) for the backend
- npm (ships with Node.js) for the frontend

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
```

`npm install` installs the frontend dependencies from `package.json` and
`package-lock.json`. The Vite development server listens on
<http://localhost:5173> by default.

To use environment overrides, copy the example file and edit it:

```bash
cp .env.example .env
```

`frontend/.env.example` lists `VITE_API_BASE_URL` with a local placeholder.
No frontend code consumes this value until issue #4 adds API wiring. Do not
commit a real `.env` file.

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

This issue intentionally stops at the scaffold. The following are **not**
built yet and are tracked by later issues:

- Django REST Framework
- CORS or a Vite proxy
- Environment-based API base URL wiring
- A `/api/v1/health/` endpoint
- Journal item and note models and migrations
- Registration, login, logout, and authentication
- Product screens and the app shell

Do not assume any of these exist when working on this scaffold.
