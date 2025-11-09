"""
Tests for Recipe Community Features
Tests public recipes, forking, ratings, comments, and user profiles
"""

import pytest
from copy import deepcopy
import Database.Models as models


BASE_RECIPE_PAYLOAD = {
    "name": "Community Test Recipe",
    "version": 1,
    "type": "IPA",
    "brewer": "Test Brewer",
    "batch_size": 20.0,
    "boil_size": 25.0,
    "boil_time": 60,
    "is_public": False,
    "hops": [
        {
            "name": "Cascade",
            "use": "Boil",
            "time": 60,
            "amount": 1.5,
            "display_amount": "1.5 oz",
        }
    ],
    "fermentables": [
        {
            "name": "Pale Malt",
            "amount": 5.0,
            "yield_": 78.0,
            "type": "Grain",
        }
    ],
    "yeasts": [{"name": "US-05", "type": "Ale", "attenuation": 75.0}],
    "miscs": [{"name": "Irish Moss", "type": "Fining", "use": "Boil", "time": 15}],
}


def create_recipe(client, **overrides):
    """Helper function to create a recipe"""
    payload = deepcopy(BASE_RECIPE_PAYLOAD)
    for key, value in overrides.items():
        payload[key] = value
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def create_user(db_session, **overrides):
    """Helper function to create a user"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        **overrides
    }
    user = models.Users(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ============================================================================
# Public Recipe Tests
# ============================================================================

def test_get_public_recipes_returns_only_public(client, db_session):
    """Test that public recipes endpoint only returns public recipes"""
    # Create public recipe
    public_recipe = create_recipe(client, name="Public Recipe", is_public=True)
    
    # Create private recipe
    private_recipe = create_recipe(client, name="Private Recipe", is_public=False)
    
    # Get public recipes
    response = client.get("/recipes/public")
    assert response.status_code == 200
    recipes = response.json()
    
    # Should only include public recipe
    recipe_names = [r["name"] for r in recipes]
    assert "Public Recipe" in recipe_names
    assert "Private Recipe" not in recipe_names


def test_toggle_recipe_visibility(client, db_session):
    """Test toggling recipe visibility"""
    recipe = create_recipe(client, name="Toggle Test", is_public=False)
    recipe_id = recipe["id"]
    
    # Make public
    response = client.patch(f"/recipes/{recipe_id}/visibility?is_public=true")
    assert response.status_code == 200
    data = response.json()
    assert data["is_public"] is True
    
    # Verify it appears in public recipes
    response = client.get("/recipes/public")
    recipes = response.json()
    recipe_names = [r["name"] for r in recipes]
    assert "Toggle Test" in recipe_names
    
    # Make private again
    response = client.patch(f"/recipes/{recipe_id}/visibility?is_public=false")
    assert response.status_code == 200
    data = response.json()
    assert data["is_public"] is False
    
    # Verify it doesn't appear in public recipes
    response = client.get("/recipes/public")
    recipes = response.json()
    recipe_names = [r["name"] for r in recipes]
    assert "Toggle Test" not in recipe_names


def test_toggle_visibility_nonexistent_recipe_returns_404(client):
    """Test that toggling visibility for nonexistent recipe returns 404"""
    response = client.patch("/recipes/9999/visibility?is_public=true")
    assert response.status_code == 404


# ============================================================================
# Recipe Forking Tests
# ============================================================================

def test_fork_recipe_creates_copy_with_attribution(client, db_session):
    """Test that forking a recipe creates a copy with attribution"""
    user = create_user(db_session, username="forker", email="forker@example.com")
    
    # Create original recipe
    original = create_recipe(client, name="Original Recipe", is_public=True)
    original_id = original["id"]
    
    # Fork the recipe
    response = client.post(
        f"/recipes/{original_id}/fork?user_id={user.id}",
        json={"new_name": "Forked Recipe"}
    )
    assert response.status_code == 200
    forked = response.json()
    
    # Verify fork attributes
    assert forked["name"] == "Forked Recipe"
    assert forked["forked_from_id"] == original_id
    assert forked["user_id"] == user.id
    assert forked["is_public"] is False  # Forked recipes are private by default
    assert "Forked from: Original Recipe" in forked["notes"]
    
    # Verify ingredients were copied
    assert len(forked["hops"]) == len(original["hops"])
    assert len(forked["fermentables"]) == len(original["fermentables"])
    assert len(forked["yeasts"]) == len(original["yeasts"])
    assert len(forked["miscs"]) == len(original["miscs"])


def test_fork_recipe_without_new_name_uses_default(client, db_session):
    """Test that forking without specifying name creates default name"""
    user = create_user(db_session, username="forker2", email="forker2@example.com")
    
    original = create_recipe(client, name="Base Recipe")
    original_id = original["id"]
    
    # Fork without new name
    response = client.post(f"/recipes/{original_id}/fork?user_id={user.id}")
    assert response.status_code == 200
    forked = response.json()
    
    assert forked["name"] == "Base Recipe (Forked)"


def test_fork_nonexistent_recipe_returns_404(client, db_session):
    """Test that forking a nonexistent recipe returns 404"""
    user = create_user(db_session, username="forker3", email="forker3@example.com")
    
    response = client.post(f"/recipes/9999/fork?user_id={user.id}")
    assert response.status_code == 404


# ============================================================================
# Recipe Rating Tests
# ============================================================================

def test_create_recipe_rating(client, db_session):
    """Test creating a new recipe rating"""
    user = create_user(db_session, username="rater", email="rater@example.com")
    recipe = create_recipe(client, name="Rated Recipe")
    recipe_id = recipe["id"]
    
    # Create rating
    rating_data = {
        "rating": 4.5,
        "review_text": "Great recipe, very hoppy!"
    }
    response = client.post(
        f"/recipes/{recipe_id}/ratings?user_id={user.id}",
        json=rating_data
    )
    assert response.status_code == 200
    rating = response.json()
    
    assert rating["rating"] == 4.5
    assert rating["review_text"] == "Great recipe, very hoppy!"
    assert rating["user_id"] == user.id
    assert rating["recipe_id"] == recipe_id


def test_update_existing_rating(client, db_session):
    """Test that creating a rating for same user/recipe updates existing"""
    user = create_user(db_session, username="updater", email="updater@example.com")
    recipe = create_recipe(client, name="Update Rating Recipe")
    recipe_id = recipe["id"]
    
    # Create initial rating
    response = client.post(
        f"/recipes/{recipe_id}/ratings?user_id={user.id}",
        json={"rating": 3.0, "review_text": "It's okay"}
    )
    assert response.status_code == 200
    rating_id = response.json()["id"]
    
    # Update rating (same user/recipe)
    response = client.post(
        f"/recipes/{recipe_id}/ratings?user_id={user.id}",
        json={"rating": 5.0, "review_text": "Actually amazing!"}
    )
    assert response.status_code == 200
    updated = response.json()
    
    assert updated["id"] == rating_id  # Same rating object
    assert updated["rating"] == 5.0
    assert updated["review_text"] == "Actually amazing!"


def test_get_recipe_ratings(client, db_session):
    """Test getting all ratings for a recipe"""
    recipe = create_recipe(client, name="Popular Recipe")
    recipe_id = recipe["id"]
    
    # Create multiple users and ratings
    user1 = create_user(db_session, username="rater1", email="rater1@example.com")
    user2 = create_user(db_session, username="rater2", email="rater2@example.com")
    
    client.post(f"/recipes/{recipe_id}/ratings?user_id={user1.id}", 
                json={"rating": 4.0, "review_text": "Good"})
    client.post(f"/recipes/{recipe_id}/ratings?user_id={user2.id}",
                json={"rating": 5.0, "review_text": "Excellent"})
    
    # Get ratings
    response = client.get(f"/recipes/{recipe_id}/ratings")
    assert response.status_code == 200
    ratings = response.json()
    
    assert len(ratings) == 2
    # Verify user information is included
    assert all("username" in r for r in ratings)


def test_get_recipe_rating_summary(client, db_session):
    """Test getting aggregated rating statistics"""
    recipe = create_recipe(client, name="Summary Recipe")
    recipe_id = recipe["id"]
    
    # Create multiple ratings
    for i in range(5):
        user = create_user(
            db_session,
            username=f"user{i}",
            email=f"user{i}@example.com"
        )
        rating_value = (i % 5) + 1  # 1, 2, 3, 4, 5
        client.post(
            f"/recipes/{recipe_id}/ratings?user_id={user.id}",
            json={"rating": float(rating_value)}
        )
    
    # Get summary
    response = client.get(f"/recipes/{recipe_id}/ratings/summary")
    assert response.status_code == 200
    summary = response.json()
    
    assert summary["recipe_id"] == recipe_id
    assert summary["total_ratings"] == 5
    assert summary["average_rating"] == 3.0  # (1+2+3+4+5)/5
    assert "rating_distribution" in summary


def test_rating_validation(client, db_session):
    """Test that rating validation enforces 1-5 range"""
    user = create_user(db_session, username="validator", email="validator@example.com")
    recipe = create_recipe(client, name="Validation Recipe")
    
    # Try invalid rating (too high)
    response = client.post(
        f"/recipes/{recipe['id']}/ratings?user_id={user.id}",
        json={"rating": 6.0}
    )
    assert response.status_code == 422  # Validation error
    
    # Try invalid rating (too low)
    response = client.post(
        f"/recipes/{recipe['id']}/ratings?user_id={user.id}",
        json={"rating": 0.0}
    )
    assert response.status_code == 422


# ============================================================================
# Recipe Comment Tests
# ============================================================================

def test_create_comment(client, db_session):
    """Test creating a comment on a recipe"""
    user = create_user(db_session, username="commenter", email="commenter@example.com")
    recipe = create_recipe(client, name="Commented Recipe")
    recipe_id = recipe["id"]
    
    # Create comment
    comment_data = {
        "comment_text": "Has anyone tried this with Citra hops?",
        "parent_comment_id": None
    }
    response = client.post(
        f"/recipes/{recipe_id}/comments?user_id={user.id}",
        json=comment_data
    )
    assert response.status_code == 200
    comment = response.json()
    
    assert comment["comment_text"] == comment_data["comment_text"]
    assert comment["user_id"] == user.id
    assert comment["recipe_id"] == recipe_id
    assert comment["parent_comment_id"] is None


def test_create_threaded_comment_reply(client, db_session):
    """Test creating a reply to a comment (threading)"""
    user1 = create_user(db_session, username="commenter1", email="commenter1@example.com")
    user2 = create_user(db_session, username="commenter2", email="commenter2@example.com")
    recipe = create_recipe(client, name="Threaded Recipe")
    recipe_id = recipe["id"]
    
    # Create parent comment
    parent_response = client.post(
        f"/recipes/{recipe_id}/comments?user_id={user1.id}",
        json={"comment_text": "Great recipe!", "parent_comment_id": None}
    )
    parent_id = parent_response.json()["id"]
    
    # Create reply
    reply_response = client.post(
        f"/recipes/{recipe_id}/comments?user_id={user2.id}",
        json={"comment_text": "I agree!", "parent_comment_id": parent_id}
    )
    assert reply_response.status_code == 200
    reply = reply_response.json()
    
    assert reply["parent_comment_id"] == parent_id
    
    # Get comments with threading
    response = client.get(f"/recipes/{recipe_id}/comments")
    assert response.status_code == 200
    comments = response.json()
    
    # Should have one top-level comment with a reply
    assert len(comments) == 1
    assert len(comments[0]["replies"]) == 1
    assert comments[0]["replies"][0]["comment_text"] == "I agree!"


def test_get_recipe_comments_with_user_info(client, db_session):
    """Test that comments include user information"""
    user = create_user(
        db_session,
        username="infouser",
        email="info@example.com",
        first_name="Info",
        last_name="User"
    )
    recipe = create_recipe(client, name="User Info Recipe")
    
    client.post(
        f"/recipes/{recipe['id']}/comments?user_id={user.id}",
        json={"comment_text": "Test comment"}
    )
    
    response = client.get(f"/recipes/{recipe['id']}/comments")
    comments = response.json()
    
    assert len(comments) == 1
    assert comments[0]["username"] == "infouser"
    assert comments[0]["user_full_name"] == "Info User"


def test_update_comment(client, db_session):
    """Test updating a comment"""
    user = create_user(db_session, username="editor", email="editor@example.com")
    recipe = create_recipe(client, name="Edit Recipe")
    
    # Create comment
    response = client.post(
        f"/recipes/{recipe['id']}/comments?user_id={user.id}",
        json={"comment_text": "Original text"}
    )
    comment_id = response.json()["id"]
    
    # Update comment
    response = client.put(
        f"/comments/{comment_id}?user_id={user.id}",
        json={"comment_text": "Updated text"}
    )
    assert response.status_code == 200
    updated = response.json()
    
    assert updated["comment_text"] == "Updated text"


def test_update_comment_wrong_user_forbidden(client, db_session):
    """Test that users can only update their own comments"""
    user1 = create_user(db_session, username="user1", email="user1@example.com")
    user2 = create_user(db_session, username="user2", email="user2@example.com")
    recipe = create_recipe(client, name="Forbidden Recipe")
    
    # User1 creates comment
    response = client.post(
        f"/recipes/{recipe['id']}/comments?user_id={user1.id}",
        json={"comment_text": "User1's comment"}
    )
    comment_id = response.json()["id"]
    
    # User2 tries to update it
    response = client.put(
        f"/comments/{comment_id}?user_id={user2.id}",
        json={"comment_text": "Hacked!"}
    )
    assert response.status_code == 403


def test_delete_comment(client, db_session):
    """Test deleting a comment"""
    user = create_user(db_session, username="deleter", email="deleter@example.com")
    recipe = create_recipe(client, name="Delete Recipe")
    
    # Create comment
    response = client.post(
        f"/recipes/{recipe['id']}/comments?user_id={user.id}",
        json={"comment_text": "To be deleted"}
    )
    comment_id = response.json()["id"]
    
    # Delete comment
    response = client.delete(f"/comments/{comment_id}?user_id={user.id}")
    assert response.status_code == 200
    
    # Verify deletion
    comments_response = client.get(f"/recipes/{recipe['id']}/comments")
    comments = comments_response.json()
    assert len(comments) == 0


# ============================================================================
# User Profile Tests
# ============================================================================

def test_get_user_profile(client, db_session):
    """Test getting user profile"""
    user = create_user(
        db_session,
        username="profileuser",
        email="profile@example.com",
        first_name="Profile",
        last_name="User",
        bio="Homebrewer for 5 years"
    )
    
    response = client.get(f"/users/{user.id}/profile")
    assert response.status_code == 200
    profile = response.json()
    
    assert profile["username"] == "profileuser"
    assert profile["bio"] == "Homebrewer for 5 years"


def test_get_public_profile_with_recipe_count(client, db_session):
    """Test getting public profile includes recipe statistics"""
    user = create_user(db_session, username="counter", email="counter@example.com")
    
    # Create recipes for user
    recipe1 = create_recipe(client, name="Public Recipe 1", is_public=True)
    recipe2 = create_recipe(client, name="Public Recipe 2", is_public=True)
    recipe3 = create_recipe(client, name="Private Recipe", is_public=False)
    
    # Assign recipes to user
    db_session.query(models.Recipes).filter(
        models.Recipes.id.in_([recipe1["id"], recipe2["id"], recipe3["id"]])
    ).update({"user_id": user.id}, synchronize_session=False)
    db_session.commit()
    
    response = client.get(f"/users/{user.id}/profile/public")
    assert response.status_code == 200
    profile = response.json()
    
    assert profile["recipe_count"] == 3
    assert profile["public_recipe_count"] == 2


def test_update_user_profile(client, db_session):
    """Test updating user profile"""
    user = create_user(db_session, username="updatable", email="updatable@example.com")
    
    update_data = {
        "bio": "Updated bio",
        "location": "Portland, OR",
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    response = client.patch(f"/users/{user.id}/profile", json=update_data)
    assert response.status_code == 200
    updated = response.json()
    
    assert updated["bio"] == "Updated bio"
    assert updated["location"] == "Portland, OR"
    assert updated["first_name"] == "Updated"
    assert updated["last_name"] == "Name"


def test_get_user_recipes(client, db_session):
    """Test getting all recipes by a user"""
    user = create_user(db_session, username="recipeowner", email="owner@example.com")
    
    # Create recipes for user
    recipe1 = create_recipe(client, name="User Recipe 1", is_public=True)
    recipe2 = create_recipe(client, name="User Recipe 2", is_public=False)
    
    # Assign to user
    db_session.query(models.Recipes).filter(
        models.Recipes.id.in_([recipe1["id"], recipe2["id"]])
    ).update({"user_id": user.id}, synchronize_session=False)
    db_session.commit()
    
    # Get public recipes only (default)
    response = client.get(f"/users/{user.id}/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["name"] == "User Recipe 1"
    
    # Get all recipes including private
    response = client.get(f"/users/{user.id}/recipes?include_private=true")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 2


def test_get_nonexistent_user_profile_returns_404(client):
    """Test that getting nonexistent user profile returns 404"""
    response = client.get("/users/9999/profile")
    assert response.status_code == 404
