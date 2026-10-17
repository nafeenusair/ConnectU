# ConnectU — Project Structure (trimmed)

This file is a curated, annotated project tree for the ConnectU Django project. Migration files are intentionally omitted and only the important files/folders are shown.

```
CAMPUS/
├── README.md                 — Setup & high-level project info
├── .env.example              — Example environment variables (copy to .env)
├── .gitignore
├── delete_migrations.sh      — Utility to remove migration files
├── manage.py                 — Django CLI entrypoint
├── requirements.txt
├── requirements_versions.txt
|
├── connect/
│   ├── __init__.py
│   ├── asgi.py               — ASGI deployment entrypoint
│   ├── wsgi.py               — WSGI deployment entrypoint
│   ├── settings.py           — Main Django settings (INSTALLED_APPS, DB, AUTH_USER_MODEL, media/static)
│   ├── urls.py               — Root URL configuration (includes app namespaces)
│   └── views.py              — Project-level views (e.g., home)
|
├── apps/
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py          — Admin registration for user/profile models
│   │   ├── models.py         — Custom email-based `User`, `UserProfile`, `UserManager`
│   │   ├── forms.py          — Auth/register/profile forms
│   │   ├── views.py          — Account views (login/register/profile)
│   │   ├── urls.py
│   │   └── signals.py        — Auto-create profile and related hooks
│   |
│   ├── common/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── choices.py        — Central TextChoices enums used across apps
│   │   └── models.py         — Shared base models / utilities
│   |
│   ├── threads/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py         — Canonical Thread / Message / Vote domain (reference pattern)
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── signals.py        — Vote/notification hooks and denormalized count updates
│   |
│   ├── forum/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── services.py       — Forum-specific business logic built on `threads`
│   │   ├── views.py
│   │   └── urls.py
│   |
│   ├── lost_found/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── matching.py       — Auto-matching engine for lost & found posts
│   │   ├── signals.py        — Triggers to run matching when posts change
│   │   ├── views.py
│   │   └── urls.py
│   |
│   ├── skill_exchange/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── services.py       — Matching engine & helper services
│   │   ├── signals.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templatetags/     — Template helpers for skill exchange
│   |
│   ├── marketplace/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   |
│   ├── ride_share/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── signals.py
│   |
│   ├── media/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   └── models.py         — Upload models & storage (uploads/user_{id}/)
│   |
│   ├── notifications/
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── signals.py        — Event -> Notification hooks
│   │   └── views.py
│   |
│   └── rankings/
│       ├── apps.py
│       ├── admin.py
│       └── models.py         — XP / ranking skeleton and helpers
|
├── templates/
│   ├── base.html             — Global base template (site chrome)
│   ├── home.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── forum/base.html
│   ├── lost_found/base.html
│   ├── marketplace/base.html
│   ├── skill_exchange/base.html
│   ├── ride_share/base.html
│   └── threads/thread_detail.html
|
├── static/
│   ├── css/
│   │   ├── campus.css        — Global styling
│   │   └── home.css
│   ├── js/
│   │   └── campus.js
│   ├── accounts/css/
│   ├── forum/css/
│   ├── lost_found/css/
│   └── sounds/duck.mp3
|
└── media/
    └── uploads/
        ├── user_1/
        ├── user_2/
        ├── user_3/
        ├── user_4/
        └── user_6/
```

## Quick start files to inspect
- `campus/settings.py` — environment, DB, `AUTH_USER_MODEL`, static/media
- `apps/accounts/models.py` — custom User & profile logic
- `apps/threads/models.py` — canonical pattern for domain models
- `apps/common/choices.py` — most domain enums live here
- `apps/lost_found/matching.py` and `apps/skill_exchange/services.py` — matching engines
- `templates/base.html` and `static/css/campus.css` — UI entrypoints
- `manage.py` and `AGENTS.md` — run commands and repo conventions

## Notes / conventions
- Soft-delete is used inconsistently (prefer `deleted_at` where present).
- Threads/messages use denormalized counts that are updated via signals (may drift).
- Tests are mostly placeholders; use `python manage.py check` and runserver for local checks.

---
Generated: PROJECT_STRUCTURE.md — trimmed, no migrations included.
# ConnectU — Project Structure (curated)

This is a curated file tree for the ConnectU Django project. Migration files are intentionally omitted. Only important files and folders are listed with short explanations to help you navigate the codebase.

## Top-level files
- [AGENTS.md](AGENTS.md) — Agent/developer guidelines and repo conventions.
- [README.md](README.md) — Setup instructions and high-level project info.
- [.env.example](.env.example) — Example environment variables (copy to `.env`).
- [manage.py](manage.py) — Django management CLI entrypoint.
- [requirements.txt](requirements.txt) / [requirements_versions.txt](requirements_versions.txt) — Dependency manifests.
- [delete_migrations.sh](delete_migrations.sh) — Helper script to remove migration files.
- [.gitignore](.gitignore)

## Project package
- campus/
  - [campus/settings.py](campus/settings.py) — Main Django settings: INSTALLED_APPS, AUTH_USER_MODEL, DB, media/static.
  - [campus/urls.py](campus/urls.py) — Root URL dispatcher; includes app namespaces.
  - [campus/wsgi.py](campus/wsgi.py) — WSGI entrypoint for deployment.
  - [campus/asgi.py](campus/asgi.py) — ASGI entrypoint for async servers.
  - [campus/views.py](campus/views.py) — Project-level views (home, misc).

## Apps (important files)

- apps/accounts/
  - [apps/accounts/models.py](apps/accounts/models.py) — Custom `User` model and `UserManager` (email-based auth).
  - [apps/accounts/forms.py](apps/accounts/forms.py) — Auth & profile forms.
  - [apps/accounts/signals.py](apps/accounts/signals.py) — `UserProfile` creation and related hooks.
  - [apps/accounts/admin.py](apps/accounts/admin.py)
  - [apps/accounts/views.py](apps/accounts/views.py)
  - [apps/accounts/urls.py](apps/accounts/urls.py)
  - [apps/accounts/tests.py](apps/accounts/tests.py)

- apps/common/
  - [apps/common/choices.py](apps/common/choices.py) — Central TextChoices enums used across apps.
  - [apps/common/models.py](apps/common/models.py) — Shared base models and utilities.
  - [apps/common/admin.py](apps/common/admin.py)

- apps/threads/
  - [apps/threads/models.py](apps/threads/models.py) — Thread, Message, Vote, Attachment domain (canonical pattern).
  - [apps/threads/signals.py](apps/threads/signals.py) — Vote/notification hooks and denormalized-count updates.
  - [apps/threads/admin.py](apps/threads/admin.py)
  - [apps/threads/views.py](apps/threads/views.py)
  - [apps/threads/urls.py](apps/threads/urls.py)

- apps/lost_found/
  - [apps/lost_found/models.py](apps/lost_found/models.py)
  - [apps/lost_found/matching.py](apps/lost_found/matching.py) — Auto-match engine for lost & found posts.
  - [apps/lost_found/signals.py](apps/lost_found/signals.py)
  - [apps/lost_found/views.py](apps/lost_found/views.py)
  - [apps/lost_found/forms.py](apps/lost_found/forms.py)
  - [apps/lost_found/admin.py](apps/lost_found/admin.py)

- apps/skill_exchange/
  - [apps/skill_exchange/models.py](apps/skill_exchange/models.py)
  - [apps/skill_exchange/services.py](apps/skill_exchange/services.py) — Matching engine and helper services.
  - [apps/skill_exchange/signals.py](apps/skill_exchange/signals.py)
  - [apps/skill_exchange/forms.py](apps/skill_exchange/forms.py)
  - [apps/skill_exchange/urls.py](apps/skill_exchange/urls.py)
  - [apps/skill_exchange/templatetags/skill_exchange_extras.py](apps/skill_exchange/templatetags/skill_exchange_extras.py)

- apps/forum/
  - [apps/forum/models.py](apps/forum/models.py)
  - [apps/forum/services.py](apps/forum/services.py)
  - [apps/forum/forms.py](apps/forum/forms.py)
  - [apps/forum/views.py](apps/forum/views.py)
  - [apps/forum/admin.py](apps/forum/admin.py)

- apps/media/
  - [apps/media/models.py](apps/media/models.py) — Upload models and storage paths.
  - [apps/media/views.py](apps/media/views.py)
  - [apps/media/admin.py](apps/media/admin.py)

- apps/notifications/
  - [apps/notifications/models.py](apps/notifications/models.py)
  - [apps/notifications/signals.py](apps/notifications/signals.py)
  - [apps/notifications/views.py](apps/notifications/views.py)
  - [apps/notifications/admin.py](apps/notifications/admin.py)

- apps/marketplace/
  - [apps/marketplace/models.py](apps/marketplace/models.py)
  - [apps/marketplace/views.py](apps/marketplace/views.py)
  - [apps/marketplace/admin.py](apps/marketplace/admin.py)
  - [apps/marketplace/urls.py](apps/marketplace/urls.py)

- apps/ride_share/
  - [apps/ride_share/models.py](apps/ride_share/models.py)
  - [apps/ride_share/forms.py](apps/ride_share/forms.py)
  - [apps/ride_share/signals.py](apps/ride_share/signals.py)
  - [apps/ride_share/views.py](apps/ride_share/views.py)

- apps/rankings/
  - [apps/rankings/models.py](apps/rankings/models.py) — XP skeleton & ranking logic.
  - [apps/rankings/views.py](apps/rankings/views.py)
  - [apps/rankings/admin.py](apps/rankings/admin.py)

- apps/academics/
  - [apps/academics/models.py](apps/academics/models.py)
  - [apps/academics/views.py](apps/academics/views.py)
  - [apps/academics/admin.py](apps/academics/admin.py)

## Templates
- [templates/base.html](templates/base.html) — Base template used across the site.
- [templates/home.html](templates/home.html) — Homepage.
- Per-app template folders: `templates/accounts/`, `templates/forum/`, `templates/lost_found/`, `templates/skill_exchange/`, `templates/ride_share/`, `templates/marketplace/`, `templates/threads/`.

## Static assets
- [static/css/campus.css](static/css/campus.css) — Global styles.
- [static/js/campus.js](static/js/campus.js) — Global JavaScript.
- Per-app static folders under `static/<app>/` (css, js, images, etc.).

## Media / Uploads
- `media/uploads/user_{id}/` — User-uploaded files organized per user (e.g., `media/uploads/user_1/`).

## Notable conventions & quick notes
- **Soft deletes:** mixture of `deleted_at` and `is_deleted` across apps — remember to filter accordingly.
- **Denormalized counts:** threads/messages hold denormalized counts updated by signals (can drift; consider aggregations for accuracy).
- **Tests:** `tests.py` files exist but are mostly placeholders; test coverage is limited.
- **Patterns:** `apps/threads` is the canonical domain pattern for threaded conversations; `apps/accounts` is the auth pattern.

## Quick-start files to inspect
- [campus/settings.py](campus/settings.py)
- [apps/accounts/models.py](apps/accounts/models.py)
- [apps/threads/models.py](apps/threads/models.py)
- [apps/skill_exchange/services.py](apps/skill_exchange/services.py)
- [templates/base.html](templates/base.html)

---

Generated by the repository assistant; migration files omitted intentionally.
