# Favorites

## Summary
Favorites can be toggled and retrieved for the logged-in user. There are two API surfaces: `/favorites/*` and `/stories/favorites/*`.

## Endpoints
- `GET /favorites/me`
- `POST /favorites/toggle/<story_id>`
- `GET /stories/favorites`
- `POST /stories/favorites/<story_id>`
- `DELETE /stories/favorites/<story_id>`

## Auth
- All favorites endpoints require JWT.

## Notes
- The frontend currently uses the `/favorites/*` toggle endpoints.

## Related Files
- `routes/favorites_routes.py`
- `routes/story_routes.py`
- `models.py`
