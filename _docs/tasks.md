# Tasks

Ordered work log for the agent workflow. The PM maintains this file.

Backlog order, oldest to newest: #1, #2, #3.

Processing order for this run: #2, #1, #3. Testing guidelines must exist
before the scaffold writes tests.

| Processing order | Backlog | Issue | Title | Status |
| --- | --- | --- | --- | --- |
| 1 | 2 | #2 | [2] Write testing guidelines | Closed |
| 2 | 1 | #1 | [1] Scaffold backend and frontend with passing tests | Open |
| 3 | 3 | #3 | [3] Define the journal design system | Open |

This run is scoped to the first three issues. The full backlog remains in
GitHub. #2 is documentation-only: the scaffold, browser test tooling, and
CI work it describes are tracked by #1, #24, and #26. #1 is scaffold-only:
it adds a minimal Django project and Vue/Vite app with one smoke test per
side. DRF, CORS/proxy, and API integration are tracked by #4; journal
models, authentication, and product screens are tracked by #5-#23.
