# Uploads

## Summary
Handles file uploads for story cover images and profile images. Also exposes routes for serving stored files.

## Endpoints
- `POST /upload` (generic file upload)
- `POST /upload/profile`
- `POST /upload/story/<story_id>`
- `GET /upload/profiles/<filename>`
- `GET /upload/stories/<filename>`
- `GET /uploads/profiles/<filename>`
- `GET /uploads/stories/<filename>`

## Auth
- Upload endpoints are currently unauthenticated.

## Related Files
- `routes/upload_routes.py`
- `app.py`
- `config.py`
