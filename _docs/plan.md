# Reading and Watch Journal — v1 Scope

## Purpose

A Python web app where users privately track books and movies and record their thoughts.

## User experience

- **Accounts:** register with a username and password, log in, and log out. Each user sees only their own data.
- **Collection:** one list with title search and filters for book/movie and status; recently updated items appear first.
- **Items:** add, edit, and delete a book or movie. Require a title and type; author/director is optional.
- **Progress:** Planned, In progress, Finished, or Dropped.
- **Dates:** first entering In progress or Finished fills the corresponding empty date with today. Dates remain editable and optional.
- **Thoughts:** each item has multiple plain-text notes, automatically dated when created. Users can edit or delete their notes.
- **Detail page:** shows an item’s information, progress, dates, and notes.

Deletion requires confirmation; deleting an item also deletes its notes.

## Acceptance checks

- A new user can register, add an item, update its progress, and write multiple notes.
- Saved information survives refreshing and restarting the app.
- Search and filters return matching entries.
- Users cannot access another user’s items or notes, including through direct URLs.
- Automatic dates preserve previously entered dates; a finish date cannot precede a start date.

## Defaults and boundaries

Use **Django, HTML templates, and SQLite**, with a custom journal interface.

Exclude sharing, ratings, tags, catalog integrations, covers, page/minute tracking, email verification, and password-reset emails.

Keep the course delivery work alongside this product scope: documented specifications and agent workflow, tests, Docker, deployment, CI/CD with rollback, observability, an alert trigger, and a responder agent.
