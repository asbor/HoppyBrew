# tests/test_endpoints/test_community.py

import pytest
from copy import deepcopy
from datetime import datetime
import Database.Models as models
from Database.Models import RecipeVisibility


# Test data
BASE_RECIPE_PAYLOAD = {
    "name": "Community Test Recipe",
    "version": 1,
    "type": "IPA",
    "brewer": "Test Brewer",
    "batch_size": 20.0,
    "boil_size": 25.0,
    "boil_time": 60,
    "visibility": "public",
    "notes": "Test recipe for community features",
    "hops": [
        {
            "name": "Cascade",
            "use": "Boil",
            "time": 60,
            "amount": 1.5,
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
    "yeasts": [
        {
            "name": "Ale Yeast",
            "type": "Ale",
            "attenuation": 75.0,
        }
    ],
    "miscs": [],
}


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = models.Users(
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$test",
        is_active=True,
        role=models.UserRole.brewer,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user2(db_session):
    """Create a second test user"""
    user = models.Users(
        username="testuser2",
        email="test2@example.com",
        hashed_password="$2b$12$test2",
        is_active=True,
        role=models.UserRole.brewer,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def public_recipe(client, db_session, test_user):
    """Create a public recipe"""
    recipe = models.Recipes(
        name="Public Test Recipe",
        version=1,
        type="IPA",
        batch_size=20.0,
        boil_size=25.0,
        visibility=RecipeVisibility.public,
        user_id=test_user.id,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    return recipe


@pytest.fixture
def private_recipe(client, db_session, test_user):
    """Create a private recipe"""
    recipe = models.Recipes(
        name="Private Test Recipe",
        version=1,
        type="Stout",
        batch_size=20.0,
        boil_size=25.0,
        visibility=RecipeVisibility.private,
        user_id=test_user.id,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    return recipe


# Recipe Visibility Tests

def test_get_recipes_filters_by_visibility_public(client, public_recipe, private_recipe):
    """Test filtering recipes by public visibility"""
    response = client.get("/recipes?visibility=public")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["visibility"] == "public"


def test_get_recipes_filters_by_visibility_private(client, public_recipe, private_recipe):
    """Test filtering recipes by private visibility"""
    response = client.get("/recipes?visibility=private")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["visibility"] == "private"


def test_get_recipes_filters_by_user_id(client, db_session, test_user, test_user2):
    """Test filtering recipes by user_id"""
    # Create recipes for different users
    recipe1 = models.Recipes(
        name="User1 Recipe",
        version=1,
        type="IPA",
        batch_size=20.0,
        visibility=RecipeVisibility.public,
        user_id=test_user.id,
    )
    recipe2 = models.Recipes(
        name="User2 Recipe",
        version=1,
        type="Stout",
        batch_size=20.0,
        visibility=RecipeVisibility.public,
        user_id=test_user2.id,
    )
    db_session.add_all([recipe1, recipe2])
    db_session.commit()
    
    response = client.get(f"/recipes?user_id={test_user.id}")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["name"] == "User1 Recipe"


# Recipe Rating Tests

def test_create_recipe_rating(client, db_session, public_recipe, test_user):
    """Test creating a recipe rating"""
    rating_data = {
        "rating": 4.5,
        "review_text": "Great recipe!",
    }
    response = client.post(
        f"/recipes/{public_recipe.id}/ratings",
        json=rating_data,
    )
    assert response.status_code == 201
    rating = response.json()
    assert rating["rating"] == 4.5
    assert rating["review_text"] == "Great recipe!"
    assert rating["recipe_id"] == public_recipe.id


def test_update_recipe_rating(client, db_session, public_recipe, test_user):
    """Test updating an existing recipe rating"""
    # Create initial rating
    rating = models.RecipeRating(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        rating=3.0,
        review_text="Initial review",
    )
    db_session.add(rating)
    db_session.commit()
    
    # Update rating
    update_data = {
        "rating": 5.0,
        "review_text": "Updated review - even better!",
    }
    response = client.post(
        f"/recipes/{public_recipe.id}/ratings",
        json=update_data,
    )
    assert response.status_code == 201
    updated_rating = response.json()
    assert updated_rating["rating"] == 5.0
    assert updated_rating["review_text"] == "Updated review - even better!"


def test_get_recipe_ratings(client, db_session, public_recipe, test_user, test_user2):
    """Test getting all ratings for a recipe"""
    # Create ratings from different users
    rating1 = models.RecipeRating(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        rating=4.5,
        review_text="Excellent!",
    )
    rating2 = models.RecipeRating(
        recipe_id=public_recipe.id,
        user_id=test_user2.id,
        rating=4.0,
        review_text="Very good",
    )
    db_session.add_all([rating1, rating2])
    db_session.commit()
    
    response = client.get(f"/recipes/{public_recipe.id}/ratings")
    assert response.status_code == 200
    ratings = response.json()
    assert len(ratings) == 2


def test_delete_recipe_rating(client, db_session, public_recipe, test_user):
    """Test deleting a recipe rating"""
    # Create rating
    rating = models.RecipeRating(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        rating=4.0,
    )
    db_session.add(rating)
    db_session.commit()
    
    # Delete rating
    response = client.delete(f"/recipes/{public_recipe.id}/ratings")
    assert response.status_code == 200
    
    # Verify it's deleted
    deleted_rating = db_session.query(models.RecipeRating).filter(
        models.RecipeRating.id == rating.id
    ).first()
    assert deleted_rating is None


# Recipe Comment Tests

def test_create_recipe_comment(client, db_session, public_recipe, test_user):
    """Test creating a comment on a recipe"""
    comment_data = {
        "comment_text": "This is a great recipe!",
    }
    response = client.post(
        f"/recipes/{public_recipe.id}/comments",
        json=comment_data,
    )
    assert response.status_code == 201
    comment = response.json()
    assert comment["comment_text"] == "This is a great recipe!"
    assert comment["recipe_id"] == public_recipe.id


def test_create_comment_reply(client, db_session, public_recipe, test_user, test_user2):
    """Test creating a reply to a comment"""
    # Create parent comment
    parent_comment = models.RecipeComment(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        comment_text="Parent comment",
    )
    db_session.add(parent_comment)
    db_session.commit()
    db_session.refresh(parent_comment)
    
    # Create reply
    reply_data = {
        "comment_text": "This is a reply",
        "parent_id": parent_comment.id,
    }
    response = client.post(
        f"/recipes/{public_recipe.id}/comments",
        json=reply_data,
    )
    assert response.status_code == 201
    reply = response.json()
    assert reply["parent_id"] == parent_comment.id


def test_get_recipe_comments_with_replies(client, db_session, public_recipe, test_user, test_user2):
    """Test getting comments with nested replies"""
    # Create parent comment
    parent = models.RecipeComment(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        comment_text="Parent comment",
    )
    db_session.add(parent)
    db_session.commit()
    db_session.refresh(parent)
    
    # Create reply
    reply = models.RecipeComment(
        recipe_id=public_recipe.id,
        user_id=test_user2.id,
        parent_id=parent.id,
        comment_text="Reply to parent",
    )
    db_session.add(reply)
    db_session.commit()
    
    response = client.get(f"/recipes/{public_recipe.id}/comments")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 1
    assert len(comments[0]["replies"]) == 1
    assert comments[0]["replies"][0]["comment_text"] == "Reply to parent"


def test_update_recipe_comment(client, db_session, public_recipe, test_user):
    """Test updating a comment"""
    # Create comment
    comment = models.RecipeComment(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        comment_text="Original text",
    )
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    
    # Update comment
    update_data = {
        "comment_text": "Updated text",
    }
    response = client.put(
        f"/recipes/{public_recipe.id}/comments/{comment.id}",
        json=update_data,
    )
    assert response.status_code == 200
    updated_comment = response.json()
    assert updated_comment["comment_text"] == "Updated text"


def test_delete_recipe_comment(client, db_session, public_recipe, test_user):
    """Test deleting a comment"""
    # Create comment
    comment = models.RecipeComment(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        comment_text="Test comment",
    )
    db_session.add(comment)
    db_session.commit()
    
    # Delete comment
    response = client.delete(f"/recipes/{public_recipe.id}/comments/{comment.id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    deleted_comment = db_session.query(models.RecipeComment).filter(
        models.RecipeComment.id == comment.id
    ).first()
    assert deleted_comment is None


# Recipe Star Tests

def test_star_recipe(client, db_session, public_recipe, test_user):
    """Test starring a recipe"""
    response = client.post(f"/recipes/{public_recipe.id}/star")
    assert response.status_code == 201
    
    # Verify star was created
    star = db_session.query(models.RecipeStar).filter(
        models.RecipeStar.recipe_id == public_recipe.id,
        models.RecipeStar.user_id == test_user.id,
    ).first()
    assert star is not None


def test_star_recipe_twice(client, db_session, public_recipe, test_user):
    """Test starring a recipe that's already starred"""
    # Star once
    star = models.RecipeStar(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
    )
    db_session.add(star)
    db_session.commit()
    
    # Try to star again
    response = client.post(f"/recipes/{public_recipe.id}/star")
    assert response.status_code == 201
    assert "already starred" in response.json()["message"].lower()


def test_unstar_recipe(client, db_session, public_recipe, test_user):
    """Test unstarring a recipe"""
    # Star recipe
    star = models.RecipeStar(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
    )
    db_session.add(star)
    db_session.commit()
    
    # Unstar recipe
    response = client.delete(f"/recipes/{public_recipe.id}/star")
    assert response.status_code == 200
    
    # Verify star was deleted
    deleted_star = db_session.query(models.RecipeStar).filter(
        models.RecipeStar.recipe_id == public_recipe.id,
        models.RecipeStar.user_id == test_user.id,
    ).first()
    assert deleted_star is None


def test_get_starred_recipes(client, db_session, public_recipe, test_user):
    """Test getting list of starred recipes"""
    # Star recipe
    star = models.RecipeStar(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
    )
    db_session.add(star)
    db_session.commit()
    
    response = client.get("/users/me/starred")
    assert response.status_code == 200
    starred_ids = response.json()
    assert public_recipe.id in starred_ids


# Recipe Statistics Tests

def test_get_recipe_stats(client, db_session, public_recipe, test_user, test_user2):
    """Test getting recipe statistics"""
    # Create ratings
    rating1 = models.RecipeRating(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        rating=4.0,
    )
    rating2 = models.RecipeRating(
        recipe_id=public_recipe.id,
        user_id=test_user2.id,
        rating=5.0,
    )
    
    # Create comment
    comment = models.RecipeComment(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
        comment_text="Test comment",
    )
    
    # Create star
    star = models.RecipeStar(
        recipe_id=public_recipe.id,
        user_id=test_user.id,
    )
    
    db_session.add_all([rating1, rating2, comment, star])
    db_session.commit()
    
    response = client.get(f"/recipes/{public_recipe.id}/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["rating_average"] == 4.5
    assert stats["rating_count"] == 2
    assert stats["comment_count"] == 1
    assert stats["star_count"] == 1


# Recipe Fork Tests

def test_fork_recipe(client, db_session, public_recipe):
    """Test forking a public recipe"""
    response = client.post(f"/recipes/{public_recipe.id}/fork")
    assert response.status_code == 200
    forked_recipe = response.json()
    assert forked_recipe["origin_recipe_id"] == public_recipe.id
    assert "Fork of" in forked_recipe["name"]


def test_fork_recipe_with_custom_name(client, db_session, public_recipe):
    """Test forking a recipe with custom name and notes"""
    fork_data = {
        "name": "My Custom Fork",
        "notes": "I made some changes to the hops",
    }
    response = client.post(
        f"/recipes/{public_recipe.id}/fork",
        json=fork_data,
    )
    assert response.status_code == 200
    forked_recipe = response.json()
    assert forked_recipe["name"] == "My Custom Fork"
    assert "Fork Notes" in forked_recipe["notes"]


def test_cannot_fork_private_recipe(client, db_session, private_recipe):
    """Test that private recipes cannot be forked"""
    response = client.post(f"/recipes/{private_recipe.id}/fork")
    assert response.status_code == 403
    assert "public" in response.json()["detail"].lower()


# User Profile Tests

def test_get_user_profile(client, db_session, test_user):
    """Test getting a user profile"""
    # Add profile info
    test_user.bio = "Test bio"
    test_user.location = "Test City"
    db_session.commit()
    
    response = client.get(f"/users/{test_user.id}/profile")
    assert response.status_code == 200
    profile = response.json()
    assert profile["username"] == test_user.username
    assert profile["bio"] == "Test bio"
    assert profile["location"] == "Test City"


def test_update_user_profile(client, db_session, test_user):
    """Test updating user profile"""
    profile_update = {
        "bio": "New bio",
        "website": "https://example.com",
        "location": "New City",
        "avatar_url": "https://example.com/avatar.jpg",
    }
    response = client.put("/users/me/profile", json=profile_update)
    assert response.status_code == 200
    profile = response.json()
    assert profile["bio"] == "New bio"
    assert profile["website"] == "https://example.com"
    assert profile["location"] == "New City"
    assert profile["avatar_url"] == "https://example.com/avatar.jpg"


def test_user_profile_includes_stats(client, db_session, test_user, public_recipe):
    """Test that user profile includes activity statistics"""
    # Create a recipe
    recipe = models.Recipes(
        name="Test Recipe",
        version=1,
        type="IPA",
        batch_size=20.0,
        user_id=test_user.id,
        visibility=RecipeVisibility.public,
    )
    db_session.add(recipe)
    db_session.commit()
    
    response = client.get(f"/users/{test_user.id}/profile")
    assert response.status_code == 200
    profile = response.json()
    assert profile["recipe_count"] >= 1
