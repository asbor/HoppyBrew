# Community Features API Documentation

This document describes the community features API endpoints for recipe sharing, ratings, comments, and user profiles in HoppyBrew.

## Overview

The community features enable users to:
- Share recipes publicly or keep them private
- Rate and review recipes
- Comment on recipes with threaded discussions
- Star/favorite recipes for quick access
- Fork recipes to create personalized versions
- View and manage user profiles

## Authentication

Most community endpoints require authentication. Include a valid JWT token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

To obtain a token, use the login endpoint:
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

## Recipe Visibility

Recipes can have one of three visibility levels:
- `private` - Only visible to the owner (default)
- `public` - Visible to everyone and can be forked
- `unlisted` - Accessible via direct link but not listed publicly

### Set Recipe Visibility

When creating or updating a recipe, include the visibility field:

```bash
curl -X POST http://localhost:8000/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "My Public IPA",
    "visibility": "public",
    "type": "IPA",
    "batch_size": 20.0,
    ...
  }'
```

### Filter Recipes by Visibility

```bash
# Get only public recipes
curl http://localhost:8000/recipes?visibility=public

# Get recipes by a specific user
curl http://localhost:8000/recipes?user_id=1

# Combine filters
curl http://localhost:8000/recipes?visibility=public&user_id=1
```

## Recipe Ratings

Users can rate recipes on a scale of 1 to 5 stars and optionally leave a review.

### Create or Update a Rating

```bash
curl -X POST http://localhost:8000/recipes/42/ratings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "rating": 4.5,
    "review_text": "Excellent recipe! Very balanced hop profile."
  }'
```

**Response:**
```json
{
  "id": 1,
  "recipe_id": 42,
  "user_id": 1,
  "rating": 4.5,
  "review_text": "Excellent recipe! Very balanced hop profile.",
  "created_at": "2025-11-09T12:00:00Z",
  "updated_at": "2025-11-09T12:00:00Z"
}
```

### Get All Ratings for a Recipe

```bash
curl http://localhost:8000/recipes/42/ratings
```

**Response:**
```json
[
  {
    "id": 1,
    "recipe_id": 42,
    "user_id": 1,
    "rating": 4.5,
    "review_text": "Excellent recipe!",
    "created_at": "2025-11-09T12:00:00Z",
    "updated_at": "2025-11-09T12:00:00Z",
    "username": "john_brewer",
    "user_avatar": "https://example.com/avatar.jpg"
  }
]
```

### Delete Your Rating

```bash
curl -X DELETE http://localhost:8000/recipes/42/ratings \
  -H "Authorization: Bearer <token>"
```

## Recipe Comments

Create threaded discussions on recipes with nested comments and replies.

### Create a Comment

```bash
curl -X POST http://localhost:8000/recipes/42/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "comment_text": "Great recipe! I used Citra hops instead."
  }'
```

### Reply to a Comment

```bash
curl -X POST http://localhost:8000/recipes/42/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "comment_text": "How did the Citra hops work out?",
    "parent_id": 1
  }'
```

### Get All Comments for a Recipe

```bash
curl http://localhost:8000/recipes/42/comments
```

**Response:** Returns nested comment threads
```json
[
  {
    "id": 1,
    "recipe_id": 42,
    "user_id": 1,
    "parent_id": null,
    "comment_text": "Great recipe! I used Citra hops instead.",
    "created_at": "2025-11-09T12:00:00Z",
    "updated_at": "2025-11-09T12:00:00Z",
    "username": "john_brewer",
    "user_avatar": "https://example.com/avatar.jpg",
    "replies": [
      {
        "id": 2,
        "recipe_id": 42,
        "user_id": 2,
        "parent_id": 1,
        "comment_text": "How did the Citra hops work out?",
        "created_at": "2025-11-09T13:00:00Z",
        "updated_at": "2025-11-09T13:00:00Z",
        "username": "jane_brewer",
        "user_avatar": null,
        "replies": []
      }
    ]
  }
]
```

### Update a Comment

```bash
curl -X PUT http://localhost:8000/recipes/42/comments/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "comment_text": "Updated: Great recipe! I used Citra hops instead and it was amazing!"
  }'
```

### Delete a Comment

```bash
curl -X DELETE http://localhost:8000/recipes/42/comments/1 \
  -H "Authorization: Bearer <token>"
```

## Recipe Stars

Star or favorite recipes for quick access later.

### Star a Recipe

```bash
curl -X POST http://localhost:8000/recipes/42/star \
  -H "Authorization: Bearer <token>"
```

### Unstar a Recipe

```bash
curl -X DELETE http://localhost:8000/recipes/42/star \
  -H "Authorization: Bearer <token>"
```

### Get Your Starred Recipes

```bash
curl http://localhost:8000/users/me/starred \
  -H "Authorization: Bearer <token>"
```

**Response:** Returns array of recipe IDs
```json
[42, 57, 103]
```

## Recipe Statistics

Get aggregate statistics for a recipe including ratings, comments, stars, and forks.

```bash
curl http://localhost:8000/recipes/42/stats
```

**Response:**
```json
{
  "rating_average": 4.5,
  "rating_count": 12,
  "comment_count": 8,
  "star_count": 25,
  "fork_count": 3
}
```

## Recipe Forking

Fork public recipes to create your own version with proper attribution.

### Fork a Recipe

```bash
curl -X POST http://localhost:8000/recipes/42/fork \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "My Custom IPA Fork",
    "notes": "Increased hop amounts and changed yeast strain"
  }'
```

**Response:** Returns the new forked recipe
```json
{
  "id": 123,
  "name": "My Custom IPA Fork",
  "origin_recipe_id": 42,
  "user_id": 1,
  "visibility": "private",
  ...
}
```

**Note:** Only `public` recipes can be forked. The forked recipe will have:
- A new unique ID
- `origin_recipe_id` pointing to the original recipe
- Default `private` visibility
- A copy of all ingredients from the original

## User Profiles

Manage and view user profiles with activity statistics.

### Get a User Profile

```bash
curl http://localhost:8000/users/1/profile
```

**Response:**
```json
{
  "id": 1,
  "username": "john_brewer",
  "first_name": "John",
  "last_name": "Brewer",
  "bio": "Homebrewer from Portland. Love IPAs and sours!",
  "avatar_url": "https://example.com/avatar.jpg",
  "website": "https://johnbrews.com",
  "location": "Portland, OR",
  "created_at": "2025-01-01T00:00:00Z",
  "recipe_count": 15,
  "rating_count": 42,
  "comment_count": 28
}
```

### Update Your Profile

```bash
curl -X PUT http://localhost:8000/users/me/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "bio": "Passionate homebrewer and beer enthusiast",
    "website": "https://myblog.com",
    "location": "Seattle, WA",
    "avatar_url": "https://example.com/my-avatar.jpg"
  }'
```

## Complete Workflow Example

Here's a complete example of using the community features:

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret" | jq -r '.access_token')

# 2. Create a public recipe
RECIPE_ID=$(curl -X POST http://localhost:8000/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Johns West Coast IPA",
    "visibility": "public",
    "type": "IPA",
    "batch_size": 20.0,
    "hops": [...],
    "fermentables": [...],
    "yeasts": [...]
  }' | jq -r '.id')

# 3. Rate the recipe
curl -X POST http://localhost:8000/recipes/$RECIPE_ID/ratings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"rating": 5.0, "review_text": "Perfect!"}'

# 4. Add a comment
curl -X POST http://localhost:8000/recipes/$RECIPE_ID/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"comment_text": "This turned out amazing!"}'

# 5. Star the recipe
curl -X POST http://localhost:8000/recipes/$RECIPE_ID/star \
  -H "Authorization: Bearer $TOKEN"

# 6. Get recipe statistics
curl http://localhost:8000/recipes/$RECIPE_ID/stats

# 7. Fork the recipe (as another user)
curl -X POST http://localhost:8000/recipes/$RECIPE_ID/fork \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OTHER_TOKEN" \
  -d '{
    "name": "Modified West Coast IPA",
    "notes": "Added more late hops"
  }'

# 8. Update your profile
curl -X PUT http://localhost:8000/users/me/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "bio": "Homebrewer specializing in IPAs",
    "location": "San Diego, CA"
  }'
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200` - Success
- `201` - Created successfully
- `400` - Bad request (invalid data)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not found
- `500` - Server error

Error responses include a detail message:
```json
{
  "detail": "Recipe not found"
}
```

## Rate Limits

Currently, there are no rate limits enforced. This may change in production deployments.

## API Versioning

The community features are part of the main API (v1). Breaking changes will be communicated via release notes and migration guides.
