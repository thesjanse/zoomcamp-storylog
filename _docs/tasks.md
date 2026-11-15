# Tasks

Ordered work log for the agent workflow. The PM maintains this file.

## Run 1: issues #1-#3 (completed)

Backlog order, oldest to newest: #1, #2, #3.

Processing order for this run: #2, #1, #3. Testing guidelines must exist
before the scaffold writes tests.

| Processing order | Backlog | Issue | Title | Status |
| --- | --- | --- | --- | --- |
| 1 | 2 | #2 | [2] Write testing guidelines | Closed |
| 2 | 1 | #1 | [1] Scaffold backend and frontend with passing tests | Closed |
| 3 | 3 | #3 | [3] Define the journal design system | Closed |

This run is scoped to the first three issues. The full backlog remains in
GitHub. #2 is documentation-only: the scaffold, browser test tooling, and
CI work it describes are tracked by #1, #24, and #26. #1 is scaffold-only:
it adds a minimal Django project and Vue/Vite app with one smoke test per
side. DRF, CORS/proxy, and API integration are tracked by #4; journal
models, authentication, and product screens are tracked by #5-#23. #3 is
documentation-only: it defines the design system tokens, states, and copy
that #14-#23 apply; it does not add Vue components or change the scaffold.

## Run 2: issues #4-#8 (current)

Backlog order, oldest to newest: #4, #5, #6, #7, #8.

Processing order for this run: #4, #5, #6, #7, #8. Processing follows
numeric order; #4 adds the DRF/API connection that later API tasks build on.

| Processing order | Backlog | Issue | Title | Status |
| --- | --- | --- | --- | --- |
| 1 | 4 | #4 | [4] Connect the Vue client to the Django API | Closed |
| 2 | 5 | #5 | [5] Add the journal item model | Open |
| 3 | 6 | #6 | Add the note model with cascade deletion | Open |
| 4 | 7 | #7 | Implement the registration API | Open |
| 5 | 8 | #8 | Implement login, logout, and current-user API | Open |

This run is scoped to issues #4-#8 in that order. #4 is API integration and
status wiring only; journal models, authentication, and product screens are
tracked by #5-#23 and are not part of #4. #5 is the journal item model,
migration, and model tests only; notes, item APIs, date rules, search/filtering,
and screens are tracked by #6 and #9-#13.
