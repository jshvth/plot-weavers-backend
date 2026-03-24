# Likes

## Summary
Chapter likes can be listed and toggled for a given chapter.

## Endpoints
- `GET /likes/chapters/<chapter_id>/likes`
- `POST /likes/chapters/<chapter_id>/like`

## Auth
- These endpoints are currently unauthenticated. The client must provide `user_id` when posting.

## Related Files
- `routes/like_routes.py`
- `models.py`
