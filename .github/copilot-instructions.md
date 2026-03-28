---
applyTo: "**/*"
---

# Copilot Instructions

Prefer concise, production-ready code aligned with this stack:
- Backend: Python, FastAPI, SQLModel, feedparser
- Frontend: Svelte, Tailwind CSS
- Ops: Docker, GitHub Actions

Repository-wide rules:
- Use spaces, not tabs.
- Prefer small, modular, reusable functions/components.
- Comment only non-obvious logic.
- Avoid globals and unnecessary side effects.
- Follow existing project patterns before introducing new ones.
- Include tests for new behavior when practical.
- Keep code deployable with existing Docker and GitHub Actions setup.

---
applyTo: "**/*.py"
---

Python rules:
- Follow PEP 8.
- Prefer type hints for public functions and return values.
- Use docstrings for public modules, classes, and functions.
- Use clear division of concerns between following layers: API, services, repository, database, models.
- Use ABCs and interfaces for complex behavior
- Use dependency injection for better testability.
- Use dependency inversion to decouple high-level logic from low-level details.
- Prefer helper functions/classes over duplication.
- Use context managers for managed resources.
- Use logging instead of print.
- Raise clear, actionable exceptions.
- Use hatch for dependency management and virtual environments.

---
applyTo: "**/*.{svelte,css,html,js,ts}"
---

Frontend rules:
- Prefer small, composable Svelte components.
- Use Svelte reactivity/stores where appropriate.
- Use type annotations in TypeScript.
- Avoid inline styles; prefer Tailwind/CSS classes.