# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Wagtail Tag Manager (WTM) is a Wagtail add-on for GDPR/ePrivacy-compliant management of scripts and tags ("tags" = HTML/JS snippets injected into pages, not CMS content tags). Distributed on PyPI as `wagtail-tag-manager`. Python package lives in `src/wagtail_tag_manager/`; frontend TypeScript/SCSS in `frontend/`.

## Commands

```bash
make test            # pytest, --nomigrations --reuse-db (fast). Settings: tests.settings
make retest          # same, verbose (-vvv)
make coverage        # with coverage report (term + html)
pytest tests/unit/test_strategy.py::test_name   # run a single test
make lint            # flake8 + isort + mypy over src/ and tests/
make format          # isort + black (py37 target) + prettier
make bundle          # yarn build → static JS/CSS bundles (needed before sandbox)
make sandbox         # build bundle, reset sqlite, load fixtures, runserver (demo site)
yarn watch           # rebuild frontend on change during development
```

Frontend build is webpack → `src/wagtail_tag_manager/static/wagtail_tag_manager/wtm.bundle.{js,css}`. E2E tests are Cypress (`yarn cypress:run` against a running sandbox on :8000).

Compatibility is broad (`setup.py`: Wagtail 4–6, Django 4–5; `tox.ini` covers the full matrix). Code uses runtime Django-version branching (e.g. `ugettext_lazy` vs `gettext_lazy`) — preserve it when editing.

## Architecture

The core question WTM answers on every request: **which tags may load, given this user's consent state and the request method?** Everything routes through `TagStrategy`.

**Consent model** (`settings.py`): four default tag *types* (necessary/preferences/statistics/marketing), each mapped to a *load setting* — `required`, `initial`, `delayed`, or default (`""`). Types are configurable via `WTM_TAG_TYPES`. A user's consent per type is one of `true`/`false`/`unset`/`pending`, persisted in the `wtm` cookie (`consent.py`). As of v2.0 the cookie is a base64+uri-encoded JSON blob with `meta` + `state`; old pipe-delimited cookies auto-upgrade on read.

**`TagStrategy`** (`strategy.py`) is the decision engine. `CONSENT_MAP` is a declarative table keyed by `(method, load_setting)` → validator lambdas that decide, per tag type: the resulting consent value, whether to include *instant* tags, and whether to include *lazy* tags. `define_strategy()` walks it to build a queryset of `(loading, type)` pairs; `.result` resolves that to rendered tag elements, including page-specific tags (via `TagMixin` on pages, with `wtm_include_children` inheritance up the tree). A `wtm_debug=true` cookie loads all tags.

**Two delivery mechanisms** (mutually exclusive — never both):
- `TagManagerMiddleware` (`middleware.py`) rewrites the HTML response with BeautifulSoup, inserting instant tags at their `tag_location` (top/bottom of head/body) and appending the lazy manager script/style.
- Template tags (`templatetags/wtm_tags.py`): `wtm_instant_tags`, `wtm_lazy_manager`, `wtm_cookie_bar`. Toggle off middleware injection with `WTM_INJECT_TAGS`/`WTM_INJECT_SCRIPT`/`WTM_INJECT_STYLE`.

`CookieConsentMiddleware` runs regardless — it computes strategy state and refreshes the consent cookie via `process_template_response`.

**Instant vs lazy loading:** instant tags ship in the initial HTML. Lazy tags (and trigger-fired tags) are fetched by the frontend client (`frontend/client/`) POSTing to `lazy_endpoint` (`endpoints.py`, wired at `wtm:lazy`). The endpoint re-runs `TagStrategy` with the payload (pathname/search/trigger) and returns tags as JSON for the client to inject.

**Tag model** (`models/tags.py`): `content` is a Django template rendered per-request with a context of Constants + Variables (`Tag.create_context`). `clean()` wraps bare scripts in `<script>`, prettifies via BeautifulSoup, and validates the template compiles. Ordering fields (`tag_loading`, `auto_load`, `tag_location`, `priority`) control injection order.

**Other models** (`models/`): `Constant` (static reusable values), `Variable` (dynamic, request-derived; extensible by developers), `Trigger` (browser-event-driven tag loading), `CookieDeclaration`. Admin is via `wagtail_modeladmin` (`wagtail_hooks.py`).

## Layout

- `src/wagtail_tag_manager/` — the package. Key files: `strategy.py` (decision engine), `consent.py` (cookie state), `middleware.py`, `endpoints.py` (lazy/config views), `models/`, `settings.py` (tag-type config), `templatetags/wtm_tags.py`.
- `frontend/admin/` — Wagtail admin widgets (CodeMirror codearea, form views). `frontend/client/` — the runtime cookie bar, tag manager, trigger monitor shipped to end users.
- `tests/` — pytest + factory_boy; `tests/settings.py` is the test Django settings, `tests/site/` a minimal test site.
- `sandbox/` — runnable demo Wagtail project with example fixtures.
