# Stories

## Summary
Story CRUD endpoints for listing, reading, creating, and deleting stories. Includes a story cover upload endpoint and a "my stories" endpoint.

## Endpoints
- `GET /stories/all`
- `GET /stories/<id>`
- `POST /stories/create`
- `DELETE /stories/<id>`
- `GET /stories/my-stories`
- `POST /stories/upload/story-cover`

## Auth
- Create, delete, my-stories, and cover upload require JWT.

## Notes
- Delete is allowed for the story owner; admins can delete any story.
- Response payloads normalize cover image URLs to absolute URLs when possible.

## Related Files
- `routes/story_routes.py`
- `models.py`
