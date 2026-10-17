# CAMPUS Django Project - AI Agent Instructions

## Project Overview
CAMPUS is a Django-based community platform with modular apps for user accounts, discussion threads, media uploads, and planned features like forums, rankings, skill exchange, and lost & found.

**App Status:**
- **Active**: accounts, threads, forum, skill_exchange, lost_found
- **Partial**: ride_share, marketplace, notifications, rankings

## Essential Setup & Commands
- **Environment**: Always activate virtual environment (`source venv/bin/activate`)
- **Database**: Run `python manage.py makemigrations` after making any model changes
- **Development Server**: `python manage.py runserver`
- **Code Check**: `python manage.py check` for verifying Django configuration (currently used instead of tests)
- **Testing**: Formal test coverage is not yet implemented. All tests.py files are templates. Opportunity to add TestCase fixtures.
- **New Dependencies**: Run `pip freeze > requirements_versions.txt` after installing new dependencies
- **Static Files**: `python manage.py collectstatic --noinput` for production-like setup
- **Admin Access**: Create superuser with `python manage.py createsuperuser` (email-based, no username)

See [README.md](README.md) for complete setup instructions.

## Architecture & Conventions
- **App Structure**: Each feature in `apps/` with standard Django files (models.py, views.py, admin.py, etc.)
- **Custom User Model**: Email-based authentication in `accounts.User`; handle as unique identifier. Custom `UserManager` enforces email, first_name, last_name (no username field).
- **Soft Deletes**: Use `deleted_at` (DateTimeField, nullable) or `is_deleted` (boolean). Standard pattern: `.filter(deleted_at__isnull=True)` in querysets.
- **Status Models**: Separate TextChoices enums in [apps/common/choices.py](apps/common/choices.py) (40+ choice classes)
- **Signals**: Use for OneToOne creation (e.g., UserProfile via [apps/accounts/signals.py](apps/accounts/signals.py)), matching engines (Skill Exchange), and auto-actions (Lost & Found).
- **Admin Customization**: Use `@admin.register`, inlines, search/filter fields; reference [apps/threads/admin.py](apps/threads/admin.py)
- **URLs**: Include app URLs with namespaces; use `reverse('app_name:url_name')`
- **One-to-One Extensions**: ForumThread↔Thread, ExchangeSession↔ExchangeMatch for wrapping base entities with domain-specific logic
- **Email Domain Parsing**: Extracts institution metadata from email (e.g., UIU department mapping); currently UIU-focused but extensible

## Key Patterns & Pitfalls
- **Models**: Follow `threads` app for complex domains (self-referencing, voting, attachments); use unique constraints to prevent duplicates
- **Avoid**: Hard deletes; stale denormalized counts (use aggregation instead); incomplete apps without migrations
- **Migrations**: Create via `makemigrations` when changing models
- **Media**: User-organized upload paths (`uploads/user_{id}/`); soft delete via boolean flag or `deleted_at`
- **Denormalized Counts**: Update manually (e.g., via signals on Vote creation) or replace with `Count()` aggregation for accuracy
- **Query Performance**: Use `select_related()` for FKs, `prefetch_related()` for M2M/reverse FKs, `values_list().flat` for efficient set operations
- **No Test Coverage**: All test files are empty templates, no need to create test files now
- **Soft Delete Inconsistency**: Photo app uses `is_deleted` boolean; Thread/Lost+Found use `deleted_at` — standardize when refactoring

## Key Files
- [campus/settings.py](campus/settings.py): INSTALLED_APPS, database config, custom User, media/static paths
- [apps/accounts/models.py](apps/accounts/models.py): Custom User & Profile models, UserManager
- [apps/accounts/signals.py](apps/accounts/signals.py): UserProfile creation signal
- [apps/common/choices.py](apps/common/choices.py): All TextChoices enums for domain values
- [apps/threads/models.py](apps/threads/models.py): Rich domain model example (Thread, Message, Vote, Attachment)
- [apps/threads/admin.py](apps/threads/admin.py): Admin customization example with inlines

When working on new features, reference existing apps for patterns.

## Agent Guidelines for AI coding agents

### Development Workflow
- **First steps:** Activate the virtualenv (`source venv/bin/activate`), run `python manage.py check` and `python manage.py runserver` to reproduce runtime issues locally.
- **Safe workflow:** 1) Read related files in `apps/<name>/` (models, views, admin). 2) Check [apps/threads/models.py](apps/threads/models.py) and [apps/threads/admin.py](apps/threads/admin.py) for canonical patterns.
- **Note:** Project currently uses `python manage.py check` instead of formal tests (all test files are templates). No test coverage exists yet.

### Design Expectations & Patterns
- **Custom User Model:** Email-based authentication (no username). Use email as unique identifier; custom `UserManager` requires email, first_name, last_name.
- **Models:** Use the `accounts` and `threads` apps as canonical patterns for complex domains.
  - Self-referencing FKs: `ThreadMessage.reply_to` for nested replies, `LFSuggestedMatch` for lost/found relationships
  - Unique constraints prevent duplicates: `unique_together = (('message', 'user'), ...)` for votes, claims, matches
  - Consistent `related_name` pattern for reverse queries: `sent_messages`, `thread_participations`, `message_votes`
- **Soft Deletes:** Prefer `deleted_at` (DateTimeField, nullable) over hard deletes. Filter manually: `.filter(deleted_at__isnull=True)` (no custom manager enforced yet).
  - **Inconsistency:** Photo app uses `is_deleted` boolean instead of `deleted_at` — standardize to `deleted_at` when refactoring.
  - **Optimization:** Consider adding `.objects.active()` custom manager to auto-filter deleted records.
- **Denormalized Counts:** Thread/Message fields like `upvote_count` are denormalized. Either:
  - Use signal on Vote creation to update count (preferred), or
  - Replace with `Count()` aggregation queries for accuracy.

### View & Form Patterns
- **Views:** Function-based views (FBV) only; use `@login_required`, `@transaction.atomic()`, `get_object_or_404()`, `messages.error()/success()`.
- **Error Handling:** Check ThreadParticipant membership for access control; return `redirect` with an error message for unauthorized actions.
- **Query Optimization:** Always use `select_related()` for FKs, `prefetch_related()` for collections; use `values_list(..., flat=True)` for set operations in matching logic.
- **File Uploads:** Whitelist MIME types (`{'image/jpeg', 'image/png', 'image/webp', 'image/gif'}`), enforce `MAX_PHOTO_MB` limit, organize as `uploads/user_{id}/{filename}`.

### Form Customization Pattern
```python
class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract custom kwargs
        super().__init__(*args, **kwargs)
    
    def clean(self):
        # Cross-field validation
        if invalid_condition:
            raise forms.ValidationError("Error message")
```

### Signal Patterns in Use
- **User creation:** `accounts.signals` creates UserProfile on User save
- **Skill Exchange:** `post_save` signal runs `find_and_create_matches()` (matching engine) and rating updates
- **Lost & Found:** `post_save` signal calls `run_auto_match()` when LFPost transitions to ACTIVE

### Conventions to Follow
- **Choices:** Define all domain TextChoices in [apps/common/choices.py](apps/common/choices.py) (40+ enums exist)
- **URLs:** Use namespaced routes: `reverse('app_name:url_name')`
- **Context-specific templates:** Views use `hasattr(thread, 'claim_thread')` to detect which domain (lost_found vs skill_exchange) and load appropriate templates
- **Admin:** Register all models with `@admin.register`, add list_display, search_fields, filters (reference [apps/threads/admin.py](apps/threads/admin.py))
- **Theming/Stylesheets:** Global CSS vars/rulesets defined in [static/css/campus.css](static/css/campus.css), reference it for template thematic inheritance

### Common Pitfalls to Avoid
1. **No test coverage:** Create TestCase fixtures for any new feature — don't skip testing.
2. **Soft deletes inconsistent:** Photo uses `is_deleted` boolean; Lost/Found, Thread models use `deleted_at`. Standardize on `deleted_at`.
3. **Soft delete not enforced:** Remember to `.filter(deleted_at__isnull=True)` in querysets or add custom manager.
4. **Stale denormalized counts:** Thread.upvote_count, Message counts may drift. Use signals or aggregation, not hard-coded updates.
5. **Missing admin customization:** forum, rankings, skill_exchange apps have minimal admin. Add list_display, search_fields for admin usability.
6. **Email validation strict:** Only UIU `@uiu.ac.bd` emails allowed. Consider allowing other institutions before expanding.
7. **Transactions inconsistent:** Some views use `@transaction.atomic()`, others don't. Standardize multi-model creates.

### Incomplete/Partial Apps
- **Forum (70%):** UI functional, admin registration missing, no search backend
- **Skill Exchange (80%):** Matching engine done, admin & rating displays minimal, old MatchDecision/SessionEndRequest models are pending removal (commented out)
- **Lost & Found (90%):** Most features complete, edge cases remain
- **Rankings (5%):** XP system skeleton only — no XP calculation logic implemented
- **Academics (60%):** Models complete, no views/admin

### Where to Look First
- [campus/settings.py](campus/settings.py) — INSTALLED_APPS, database config, custom User
- [apps/accounts/models.py](apps/accounts/models.py) — Custom User & Profile models, UserManager
- [apps/threads/models.py](apps/threads/models.py) — Rich domain model (Thread, Message, Vote, Attachment) — use as pattern
- [apps/threads/admin.py](apps/threads/admin.py) — Admin customization example with inlines
- [apps/common/choices.py](apps/common/choices.py) — All TextChoices enums
