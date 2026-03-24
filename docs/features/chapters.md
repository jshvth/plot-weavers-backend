# Chapters

## Summary
Chapter endpoints allow creating, listing, retrieving, and deleting chapters. Chapters can optionally link to a parent for branching.

## Endpoints
- `GET /chapters?story_id=<id>`
- `GET /chapters/<id>`
- `POST /chapters/create`
- `DELETE /chapters/<id>`

## Auth
- Create and delete require JWT.

## Notes
- Delete is allowed for the chapter owner; admins can delete any chapter.

## Related Files
- `routes/chapter_routes.py`
- `models.py`
