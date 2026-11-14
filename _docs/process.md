- Tasks are GitHub issues, one at a time
- Read the acceptance criteria before starting and before closing
- Commit regularly
- Every role reads `_docs/AGENTS.md`, this file, and its role document before acting

Backlog

- Process issues in numeric order unless a dependency requires another order
- When the processing order differs from the issue numbers, record it in `_docs/tasks.md`
- Issue titles carry their backlog position, for example `[1] ...`, because GitHub cannot renumber issues
- A run may be limited to a fixed set of issues; that scope overrides the repeat rule below

Roles

- PM - grooms a task before anyone implements it, follows `_docs/team/pm.md`
- Engineer - implements one groomed task, follows `_docs/team/software-engineer.md`
- QA - checks the result against the acceptance criteria, follows `_docs/team/qa-engineer.md`

Orchestrator

The main session is the orchestrator. It launches the PM, the engineer
and QA as subagents. It does not groom, implement or test itself.

Lifecycle

1. Pick the next open github issue from the backlog
2. PM grooms it
3. Engineer implements it
4. QA verifies it
5. On FAIL, back to step 3 with the QA comment as input
6. On PASS, close the issue
7. Repeat until the backlog is empty

Rules

- Do not skip step 2
- The engineer does not close the issue
- QA does not fix the code, only outputs PASS or FAIL
- The orchestrator closes the issue only after QA outputs PASS
- Only the orchestrator changes issue state or closes issues
- PM commits only documentation changes; the engineer commits code and tests; QA commits nothing
- Work on the current branch. Do not open a PR or push unless asked
- If QA fails the same issue three times in a row, stop and ask the user
