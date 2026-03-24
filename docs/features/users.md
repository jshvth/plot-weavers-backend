# Users

## Summary
User endpoints for retrieving personal stories and chapters, and deleting the current account.

## Endpoints
- `GET /users/me/stories`
- `GET /users/me/chapters`
- `DELETE /users/me`

## Auth
- All user endpoints require JWT.

## Related Files
- `routes/user_routes.py`
- `models.py`
