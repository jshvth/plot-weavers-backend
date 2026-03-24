# Authentication

## Summary
Handles user registration, login, and identity lookup with JWT tokens. A default admin and test user are created on first app start.

## Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

## Auth
- `GET /auth/me` requires a valid JWT.

## Notes
- On app startup, the backend creates a default `admin` user and a `testuser` if they do not exist.

## Related Files
- `routes/auth_routes.py`
- `extensions.py`
- `config.py`
