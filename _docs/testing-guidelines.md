# Testing Guidelines

> **Status:** This document defines testing conventions for tooling that #1
> (backend and frontend scaffold) and #24 (Playwright E2E) will add. It does
> not claim that `backend/`, `frontend/`, or the commands below already exist.
> Use it to build those changes; once the tooling lands, this document becomes
> the contract for contributors and agents.

For product scope see [`_docs/plan.md`](plan.md), for workflow and roles see
[`_docs/process.md`](process.md), and for agent commands and rules see
[`_docs/AGENTS.md`](AGENTS.md). This document adds testing-specific detail and
does not replace those documents.

## Choose the right layer

Each behaviour belongs in the lowest layer that can verify it. Avoid duplicating
the same assertion at every layer.

| Layer | Tool | One responsibility | Runs against |
| --- | --- | --- | --- |
| API | pytest + pytest-django | Django models and API endpoints, authentication and owner isolation, validation, cascade deletion, date rules, and list search/filter/ordering. | A real Django app and an isolated test database, without the Vue frontend. |
| Component | Vitest | Vue rendering, user interactions, routing, and loading/empty/error states with the API mocked. | Vue components in isolation; no Django server or database. |
| End-to-end | Playwright | Full user journeys through the real frontend and backend, including reload persistence and owner isolation. | A running frontend, a running backend, and a dedicated test database. |

## Backend API tests

API tests belong in `backend/tests/`. Name files `test_<subject>.py`, one subject
per file, for example `test_models.py`, `test_auth.py`, `test_items_api.py`, or
`test_notes_api.py`. Tests with database access use pytest-django's database
marker so the test database is created for them.

Run these commands from `backend/`:

```bash
uv sync                                      # prepare dependencies
uv run pytest                                # full API suite
uv run pytest tests/<file>.py                # one test file
uv run pytest tests/<file>.py::<test_name>   # one test
```

pytest-django creates a dedicated test database and applies migrations before
the suite runs. Each test runs in a transaction that is rolled back afterwards,
so tests must not leave records behind for later tests. Never point pytest at
the development database: do not reuse, disable, or override test database
creation. The development SQLite file is for manual use only.

## Frontend component tests

Component tests belong next to the code they cover under `frontend/src/`. Name
files `<Name>.spec.js`, for example
`frontend/src/components/ItemForm.spec.js`. Keep one component or composable
per file and name the file after it.

Run these commands from `frontend/`:

```bash
npm install                                    # prepare dependencies
npm test                                       # all component tests
npm test -- <path>                             # one test file
npm test -- <path> -t "<test name>"            # one test
```

Component tests must mock the API. They must not require a running Django
server, a database, or a real network request. Mock the API boundary used by
the component and assert the rendered result and emitted behaviour; leave real
HTTP and persistence to the API and E2E layers.

## End-to-end tests

E2E tests belong in `frontend/e2e/`. Name specs after the journey they cover,
for example `items.spec.js`, and name individual tests after the user outcome.
From a clean checkout, run `npm install` in `frontend/` before the browser
install command. Run these commands from `frontend/`:

```bash
npx playwright install                          # install browser binaries
npm run test:e2e                                # all E2E tests
npm run test:e2e -- <spec>                      # one spec
npm run test:e2e -- <spec> --grep "<test name>" # one test
```

#24 owns adding the matching `test:e2e` script and the Playwright
configuration that starts and stops the servers. The commands above are the
contract that script must support.

### Data and server preparation

- Use a dedicated test database that is separate from the development
  database. The E2E suite must never read from or write to development data.
- Apply migrations and then seed or reset the database before the suite starts.
  Starting from a known state is part of the suite, not a manual step.
- Run the backend and frontend on fixed, known ports so specs can address them
  reliably. The convention is backend port `8000` and frontend port `5173`;
  #24 may choose different values but must keep both fixed and documented. Do
  not let the orchestration choose random ports for either server.
- Check readiness for both servers before the first test. Wait for the backend
  health endpoint and the frontend dev server to respond, and fail the run if
  either does not become ready.
- Locally, `reuseExistingServer` may reuse an already running development server
  to shorten feedback loops. CI must always start fresh servers and must not
  reuse a running process.
- Tear down what the suite started: stop both servers, stop the test database
  process or remove its isolated file, and clear data created by the run.

To reproduce a failure without reusing dirty data, stop any manually started
servers, reset the dedicated test database so migrations and seed run again, and
run only the failing spec or test from a fresh suite start. Do not diagnose a
failure by reusing a server or database left over from an earlier run.

## Conventions checklist

- [ ] File names follow the conventions above: `test_<subject>.py` for API
      tests, `<Name>.spec.js` under `frontend/src/` for component tests, and
      `<journey>.spec.js` under `frontend/e2e/` for E2E specs.
- [ ] Tests use arrange-act-assert: set up the state, perform one action, then
      assert the observable result.
- [ ] Tests are independent. Each test passes alone and in any order; do not
      depend on state, ordering, or side effects from another test.
- [ ] Test data is unique per test so parallel or repeated runs do not collide.
- [ ] Tests do not use arbitrary sleeps. Wait for a condition, response, or UI
      state instead.
- [ ] Tests do not call real external services or send email. Mock or fake
      those boundaries.
- [ ] No secrets, tokens, passwords, or credentials are committed in tests or
      fixtures. Use clearly fake test values.
- [ ] Every record a test creates is cleaned up by that test, or by a teardown
      that runs even when the test fails.
