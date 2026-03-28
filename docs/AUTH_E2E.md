# Auth E2E Test Suggestions

Use Playwright for full-stack authentication journeys against the Svelte UI and FastAPI backend.

## Recommended scenarios

1. Register a new user
   - Open `/register`
   - Submit valid `email`, `username`, `password`
   - Assert redirect to `/profile`
   - Assert top navigation shows `Profile` and `Logout`

2. Login with existing user
   - Seed a user in the test database
   - Open `/login`
   - Submit `username` and `password`
   - Assert redirect to `/profile`
   - Assert profile details render correctly

3. Reject duplicate registration
   - Seed a user
   - Open `/register`
   - Submit the same `email` or `username`
   - Assert validation error from backend is visible

4. Reject invalid login
   - Seed a user
   - Open `/login`
   - Submit a valid username with a wrong password
   - Assert the error message is shown
   - Assert the navbar still shows `Login` and `Register`

5. Logout clears authenticated UI
   - Login as an existing user
   - Click `Logout`
   - Assert `Profile` disappears
   - Assert `Login` and `Register` return

6. Protected profile redirect
   - Ensure there is no auth token in storage
   - Open `/profile`
   - Assert redirect to `/login`

## Suggested setup

- Run FastAPI on a dedicated test port backed by a temporary SQLite database.
- Run the Svelte app against that backend with `VITE_API_URL` pointing at the test server.
- Create and destroy the SQLite schema per test run.
- Seed users directly through the backend database for login-only scenarios.
- Keep these tests separate from Vitest component tests; use Playwright only for browser-to-backend flows.

## Good first file layout

- `ui/playwright.config.ts`
- `ui/tests/e2e/auth.register.spec.ts`
- `ui/tests/e2e/auth.login.spec.ts`
- `ui/tests/e2e/auth.logout.spec.ts`
