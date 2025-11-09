# Recipe Community Features API Documentation

## Overview

HoppyBrew now includes comprehensive community features for recipe sharing, including public/private visibility, recipe forking, ratings, comments, and user profiles.

## Table of Contents

1. [Public Recipes](#public-recipes)
2. [Recipe Forking](#recipe-forking)
3. [Recipe Ratings](#recipe-ratings)
4. [Recipe Comments](#recipe-comments)
5. [User Profiles](#user-profiles)

---

## Public Recipes

### List Public Recipes

Get all recipes that have been marked as public by their authors.

```http
GET /recipes/public?skip=0&limit=50
```

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip for pagination (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 50, max: 100)

**Response:** Array of Recipe objects

**Example:**
```bash
curl -X GET "http://localhost:8000/recipes/public?limit=10"
```

### Toggle Recipe Visibility

Change a recipe's visibility between public and private.

```http
PATCH /recipes/{recipe_id}/visibility?is_public=true
```

**Path Parameters:**
- `recipe_id` (integer, required): ID of the recipe

**Query Parameters:**
- `is_public` (boolean, required): Set to `true` for public, `false` for private

**Response:**
```json
{
  "recipe_id": 123,
  "is_public": true,
  "message": "Recipe visibility set to public"
}
```

**Example:**
```bash
# Make recipe public
curl -X PATCH "http://localhost:8000/recipes/123/visibility?is_public=true"

# Make recipe private
curl -X PATCH "http://localhost:8000/recipes/123/visibility?is_public=false"
```

---

## Recipe Forking

### Fork a Recipe

Create a copy of an existing recipe with attribution to the original.

```http
POST /recipes/{recipe_id}/fork?user_id=1
```

**Path Parameters:**
- `recipe_id` (integer, required): ID of the recipe to fork

**Query Parameters:**
- `user_id` (integer, required): ID of the user creating the fork

**Request Body (optional):**
```json
{
  "new_name": "My Forked Recipe"
}
```

**Response:** Full Recipe object with `forked_from_id` set

**Example:**
```bash
curl -X POST "http://localhost:8000/recipes/123/fork?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"new_name": "My Custom IPA"}'
```

**Notes:**
- Forked recipes are private by default
- All ingredients are copied to the new recipe
- Original recipe attribution is added to notes
- `forked_from_id` references the original recipe

---

## Recipe Ratings

### Create or Update Rating

Add a rating to a recipe. If the user has already rated this recipe, it updates the existing rating.

```http
POST /recipes/{recipe_id}/ratings?user_id=1
```

**Path Parameters:**
- `recipe_id` (integer, required): ID of the recipe to rate

**Query Parameters:**
- `user_id` (integer, required): ID of the user creating the rating

**Request Body:**
```json
{
  "rating": 4.5,
  "review_text": "Great recipe! The hop profile is well balanced."
}
```

**Validation:**
- `rating`: Must be between 1.0 and 5.0
- `review_text`: Optional, max 2000 characters

**Response:** RecipeRating object

**Example:**
```bash
curl -X POST "http://localhost:8000/recipes/123/ratings?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4.5,
    "review_text": "Excellent IPA, perfect balance!"
  }'
```

### Get Recipe Ratings

Retrieve all ratings for a recipe with user information.

```http
GET /recipes/{recipe_id}/ratings?skip=0&limit=50
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "recipe_id": 123,
    "rating": 4.5,
    "review_text": "Great recipe!",
    "username": "brewer123",
    "user_full_name": "John Brewer",
    "created_at": "2025-11-09T12:00:00Z",
    "updated_at": "2025-11-09T12:00:00Z"
  }
]
```

### Get Rating Summary

Get aggregated statistics for a recipe's ratings.

```http
GET /recipes/{recipe_id}/ratings/summary
```

**Response:**
```json
{
  "recipe_id": 123,
  "average_rating": 4.2,
  "total_ratings": 15,
  "rating_distribution": {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 5,
    "5": 7
  }
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/recipes/123/ratings/summary"
```

---

## Recipe Comments

### Create Comment

Add a comment to a recipe. Supports threaded replies.

```http
POST /recipes/{recipe_id}/comments?user_id=1
```

**Path Parameters:**
- `recipe_id` (integer, required): ID of the recipe

**Query Parameters:**
- `user_id` (integer, required): ID of the user creating the comment

**Request Body:**
```json
{
  "comment_text": "Has anyone tried this with Cascade hops?",
  "parent_comment_id": null
}
```

**Notes:**
- `parent_comment_id` is `null` for top-level comments
- Set `parent_comment_id` to create a reply to another comment
- Max 2000 characters

**Example:**
```bash
# Top-level comment
curl -X POST "http://localhost:8000/recipes/123/comments?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "comment_text": "Great recipe! What temperature did you ferment at?",
    "parent_comment_id": null
  }'

# Reply to comment
curl -X POST "http://localhost:8000/recipes/123/comments?user_id=2" \
  -H "Content-Type: application/json" \
  -d '{
    "comment_text": "I fermented at 18°C for 2 weeks",
    "parent_comment_id": 456
  }'
```

### Get Recipe Comments

Retrieve all comments for a recipe with threading support.

```http
GET /recipes/{recipe_id}/comments?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "recipe_id": 123,
    "comment_text": "Great recipe!",
    "parent_comment_id": null,
    "username": "brewer123",
    "user_full_name": "John Brewer",
    "created_at": "2025-11-09T12:00:00Z",
    "updated_at": "2025-11-09T12:00:00Z",
    "replies": [
      {
        "id": 2,
        "user_id": 2,
        "recipe_id": 123,
        "comment_text": "I agree!",
        "parent_comment_id": 1,
        "username": "craftbeer",
        "user_full_name": "Jane Craft",
        "created_at": "2025-11-09T12:05:00Z",
        "updated_at": "2025-11-09T12:05:00Z",
        "replies": []
      }
    ]
  }
]
```

**Notes:**
- Returns top-level comments with nested replies
- Sorted by most recent first
- Replies are nested within their parent comments

### Update Comment

Update an existing comment.

```http
PUT /comments/{comment_id}?user_id=1
```

**Authorization:** Only the comment author can update their comment

**Request Body:**
```json
{
  "comment_text": "Updated comment text"
}
```

### Delete Comment

Delete a comment.

```http
DELETE /comments/{comment_id}?user_id=1
```

**Authorization:** Only the comment author can delete their comment

**Note:** Deleting a parent comment also deletes all replies (cascade)

---

## User Profiles

### Get User Profile

Retrieve full user profile information.

```http
GET /users/{user_id}/profile
```

**Response:**
```json
{
  "id": 1,
  "username": "brewer123",
  "email": "brewer@example.com",
  "first_name": "John",
  "last_name": "Brewer",
  "bio": "Homebrewer for 5 years, specializing in IPAs",
  "location": "Portland, OR",
  "avatar_url": "https://example.com/avatars/user123.jpg",
  "created_at": "2025-01-01T00:00:00Z",
  "is_active": true
}
```

### Get Public Profile

Retrieve public user profile with recipe statistics.

```http
GET /users/{user_id}/profile/public
```

**Response:**
```json
{
  "id": 1,
  "username": "brewer123",
  "first_name": "John",
  "last_name": "Brewer",
  "bio": "Homebrewer for 5 years",
  "location": "Portland, OR",
  "avatar_url": "https://example.com/avatars/user123.jpg",
  "recipe_count": 25,
  "public_recipe_count": 15
}
```

### Update User Profile

Update user profile information.

```http
PATCH /users/{user_id}/profile
```

**Authorization:** User should only update their own profile

**Request Body:**
```json
{
  "bio": "Updated biography",
  "location": "Seattle, WA",
  "first_name": "John",
  "last_name": "Smith",
  "avatar_url": "https://example.com/new-avatar.jpg"
}
```

**Note:** Only provided fields are updated

**Example:**
```bash
curl -X PATCH "http://localhost:8000/users/1/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Award-winning homebrewer specializing in Belgian styles",
    "location": "Denver, CO"
  }'
```

### Get User's Recipes

Retrieve all recipes created by a user.

```http
GET /users/{user_id}/recipes?include_private=false&skip=0&limit=50
```

**Query Parameters:**
- `include_private` (boolean, optional): Include private recipes (default: false)
- `skip` (integer, optional): Pagination offset
- `limit` (integer, optional): Max results (max: 100)

**Response:** Array of Recipe objects

**Example:**
```bash
# Get public recipes only
curl -X GET "http://localhost:8000/users/1/recipes"

# Get all recipes (requires authentication)
curl -X GET "http://localhost:8000/users/1/recipes?include_private=true"
```

---

## Data Models

### Recipe (with community fields)

```json
{
  "id": 123,
  "name": "Hoppy IPA",
  "user_id": 1,
  "is_public": true,
  "forked_from_id": null,
  "created_at": "2025-11-09T12:00:00Z",
  "updated_at": "2025-11-09T12:00:00Z",
  "...": "other recipe fields"
}
```

### RecipeRating

```json
{
  "id": 1,
  "user_id": 1,
  "recipe_id": 123,
  "rating": 4.5,
  "review_text": "Excellent recipe!",
  "created_at": "2025-11-09T12:00:00Z",
  "updated_at": "2025-11-09T12:00:00Z"
}
```

### RecipeComment

```json
{
  "id": 1,
  "user_id": 1,
  "recipe_id": 123,
  "comment_text": "Has anyone tried this recipe?",
  "parent_comment_id": null,
  "created_at": "2025-11-09T12:00:00Z",
  "updated_at": "2025-11-09T12:00:00Z"
}
```

---

## Security Considerations

1. **Authentication**: In production, all endpoints should verify user authentication before allowing modifications
2. **Authorization**: Users should only be able to:
   - Update/delete their own comments
   - Update/delete their own ratings
   - Update their own profile
   - Toggle visibility of their own recipes
3. **Validation**: 
   - Ratings must be 1.0-5.0
   - Text fields have maximum lengths
   - User-recipe rating combinations are unique
4. **Cascade Deletes**: 
   - Deleting a user deletes their ratings and comments
   - Deleting a recipe deletes its ratings and comments
   - Deleting a comment deletes all replies

---

## Integration Example

Here's a complete example workflow:

```bash
# 1. Create a public recipe
curl -X POST "http://localhost:8000/recipes" \
  -H "Content-Type: application/json" \
  -d '{"name": "Community IPA", "type": "IPA", "batch_size": 20, "is_public": true, ...}'

# 2. Rate the recipe
curl -X POST "http://localhost:8000/recipes/123/ratings?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5.0, "review_text": "Amazing!"}'

# 3. Comment on the recipe
curl -X POST "http://localhost:8000/recipes/123/comments?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"comment_text": "What hops did you use?", "parent_comment_id": null}'

# 4. Fork the recipe
curl -X POST "http://localhost:8000/recipes/123/fork?user_id=2" \
  -d '{"new_name": "My Custom IPA"}'

# 5. Get rating summary
curl -X GET "http://localhost:8000/recipes/123/ratings/summary"

# 6. Get all comments
curl -X GET "http://localhost:8000/recipes/123/comments"
```

---

## Migration Notes

To apply the database migration:

```bash
cd services/backend
alembic upgrade head
```

This will create the following tables:
- `recipe_ratings` (with unique user-recipe constraint)
- `recipe_comments` (with parent-child relationship)

And add columns to existing tables:
- `recipes`: user_id, is_public, forked_from_id, created_at, updated_at
- `user`: bio, location, avatar_url
