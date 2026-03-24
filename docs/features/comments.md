# Comments

## Summary
Comments can be listed, created, and deleted for a given story.

## Endpoints
- `GET /stories/<story_id>/comments`
- `POST /stories/<story_id>/comments`
- `DELETE /comments/<comment_id>`

## Auth
- These endpoints are currently unauthenticated. The client must provide `user_id` when posting.

## Related Files
- `routes/comment_routes.py`
- `models.py`
