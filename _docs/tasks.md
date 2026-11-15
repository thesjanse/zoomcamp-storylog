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

## Run 2: issues #4-#8 (completed)

Backlog order, oldest to newest: #4, #5, #6, #7, #8.

Processing order for this run: #4, #5, #6, #7, #8. Processing follows
numeric order; #4 adds the DRF/API connection that later API tasks build on.

| Processing order | Backlog | Issue | Title | Status |
| --- | --- | --- | --- | --- |
| 1 | 4 | #4 | [4] Connect the Vue client to the Django API | Closed |
| 2 | 5 | #5 | [5] Add the journal item model | Closed |
| 3 | 6 | #6 | [6] Add the note model with cascade deletion | Closed |
| 4 | 7 | #7 | [7] Implement the registration API | Closed |
| 5 | 8 | #8 | [8] Implement login, logout, and current-user API | Closed |

This run is scoped to issues #4-#8 in that order. #4 is API integration and
status wiring only; journal models, authentication, and product screens are
tracked by #5-#23 and are not part of #4. #5 is the journal item model,
migration, and model tests only; #6 is the note model, migration, and model
tests only. The note API is tracked by #11, the notes UI by #22, item APIs by
#9-#10, date rules by #12, and search/filtering by #13. #7 is the registration
API only: it adds the public register endpoint, DRF authtoken issuance, and API
tests; login, logout, current-user, and protected-endpoint 401 behavior are
tracked by #8, the shared API client by #15, and the auth screens by #16. #8 is
login, logout, and current-user only: it adds token login, caller-only token
revocation, `/me/`, and 401 behavior for those protected auth endpoints; item
and note protected endpoints remain #9-#13, the shared API client #15, and the
auth screens #16.
