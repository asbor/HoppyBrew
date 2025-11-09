# api/endpoints/community.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from database import get_db
import Database.Models as models
import Database.Schemas.community as community_schemas
from auth import get_current_active_user

router = APIRouter()


# Recipe Ratings Endpoints

@router.get("/recipes/{recipe_id}/ratings", response_model=List[community_schemas.RecipeRatingWithUser])
async def get_recipe_ratings(
    recipe_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """Get all ratings for a recipe"""
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Get ratings with user info
    ratings = (
        db.query(
            models.RecipeRating,
            models.Users.username,
            models.Users.avatar_url,
        )
        .join(models.Users, models.RecipeRating.user_id == models.Users.id)
        .filter(models.RecipeRating.recipe_id == recipe_id)
        .order_by(desc(models.RecipeRating.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return [
        community_schemas.RecipeRatingWithUser(
            id=rating.RecipeRating.id,
            recipe_id=rating.RecipeRating.recipe_id,
            user_id=rating.RecipeRating.user_id,
            rating=rating.RecipeRating.rating,
            review_text=rating.RecipeRating.review_text,
            created_at=rating.RecipeRating.created_at,
            updated_at=rating.RecipeRating.updated_at,
            username=rating.username,
            user_avatar=rating.avatar_url,
        )
        for rating in ratings
    ]


@router.post("/recipes/{recipe_id}/ratings", response_model=community_schemas.RecipeRating, status_code=status.HTTP_201_CREATED)
async def create_recipe_rating(
    recipe_id: int,
    rating: community_schemas.RecipeRatingCreate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Create or update a rating for a recipe"""
    # Check if recipe exists and is public
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if user already rated this recipe
    existing_rating = (
        db.query(models.RecipeRating)
        .filter(
            models.RecipeRating.recipe_id == recipe_id,
            models.RecipeRating.user_id == current_user.id,
        )
        .first()
    )
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating.rating
        existing_rating.review_text = rating.review_text
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    
    # Create new rating
    db_rating = models.RecipeRating(
        recipe_id=recipe_id,
        user_id=current_user.id,
        rating=rating.rating,
        review_text=rating.review_text,
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


@router.delete("/recipes/{recipe_id}/ratings")
async def delete_recipe_rating(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Delete user's rating for a recipe"""
    rating = (
        db.query(models.RecipeRating)
        .filter(
            models.RecipeRating.recipe_id == recipe_id,
            models.RecipeRating.user_id == current_user.id,
        )
        .first()
    )
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating)
    db.commit()
    return {"message": "Rating deleted successfully"}


# Recipe Comments Endpoints

@router.get("/recipes/{recipe_id}/comments", response_model=List[community_schemas.RecipeCommentWithUser])
async def get_recipe_comments(
    recipe_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """Get all top-level comments for a recipe with replies"""
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Get top-level comments (no parent) with user info and replies
    comments = (
        db.query(
            models.RecipeComment,
            models.Users.username,
            models.Users.avatar_url,
        )
        .join(models.Users, models.RecipeComment.user_id == models.Users.id)
        .filter(
            models.RecipeComment.recipe_id == recipe_id,
            models.RecipeComment.parent_id.is_(None),
        )
        .order_by(desc(models.RecipeComment.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    def build_comment_with_replies(comment_data):
        comment, username, avatar = comment_data
        # Get replies recursively
        replies_data = (
            db.query(
                models.RecipeComment,
                models.Users.username,
                models.Users.avatar_url,
            )
            .join(models.Users, models.RecipeComment.user_id == models.Users.id)
            .filter(models.RecipeComment.parent_id == comment.id)
            .order_by(models.RecipeComment.created_at)
            .all()
        )
        
        replies = [build_comment_with_replies(reply_data) for reply_data in replies_data]
        
        return community_schemas.RecipeCommentWithUser(
            id=comment.id,
            recipe_id=comment.recipe_id,
            user_id=comment.user_id,
            parent_id=comment.parent_id,
            comment_text=comment.comment_text,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            username=username,
            user_avatar=avatar,
            replies=replies,
        )
    
    return [build_comment_with_replies(comment_data) for comment_data in comments]


@router.post("/recipes/{recipe_id}/comments", response_model=community_schemas.RecipeComment, status_code=status.HTTP_201_CREATED)
async def create_recipe_comment(
    recipe_id: int,
    comment: community_schemas.RecipeCommentCreate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Create a comment on a recipe"""
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # If parent_id is provided, check if parent comment exists
    if comment.parent_id:
        parent = (
            db.query(models.RecipeComment)
            .filter(
                models.RecipeComment.id == comment.parent_id,
                models.RecipeComment.recipe_id == recipe_id,
            )
            .first()
        )
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")
    
    # Create comment
    db_comment = models.RecipeComment(
        recipe_id=recipe_id,
        user_id=current_user.id,
        parent_id=comment.parent_id,
        comment_text=comment.comment_text,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.put("/recipes/{recipe_id}/comments/{comment_id}", response_model=community_schemas.RecipeComment)
async def update_recipe_comment(
    recipe_id: int,
    comment_id: int,
    comment_update: community_schemas.RecipeCommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Update a comment (only by the comment author)"""
    comment = (
        db.query(models.RecipeComment)
        .filter(
            models.RecipeComment.id == comment_id,
            models.RecipeComment.recipe_id == recipe_id,
        )
        .first()
    )
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user is the comment author
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    
    comment.comment_text = comment_update.comment_text
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/recipes/{recipe_id}/comments/{comment_id}")
async def delete_recipe_comment(
    recipe_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Delete a comment (only by the comment author or admin)"""
    comment = (
        db.query(models.RecipeComment)
        .filter(
            models.RecipeComment.id == comment_id,
            models.RecipeComment.recipe_id == recipe_id,
        )
        .first()
    )
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user is the comment author or admin
    if comment.user_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}


# Recipe Stars Endpoints

@router.post("/recipes/{recipe_id}/star", status_code=status.HTTP_201_CREATED)
async def star_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Star/favorite a recipe"""
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if already starred
    existing_star = (
        db.query(models.RecipeStar)
        .filter(
            models.RecipeStar.recipe_id == recipe_id,
            models.RecipeStar.user_id == current_user.id,
        )
        .first()
    )
    
    if existing_star:
        return {"message": "Recipe already starred"}
    
    # Create star
    db_star = models.RecipeStar(
        recipe_id=recipe_id,
        user_id=current_user.id,
    )
    db.add(db_star)
    db.commit()
    return {"message": "Recipe starred successfully"}


@router.delete("/recipes/{recipe_id}/star")
async def unstar_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Unstar/unfavorite a recipe"""
    star = (
        db.query(models.RecipeStar)
        .filter(
            models.RecipeStar.recipe_id == recipe_id,
            models.RecipeStar.user_id == current_user.id,
        )
        .first()
    )
    
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    
    db.delete(star)
    db.commit()
    return {"message": "Recipe unstarred successfully"}


@router.get("/recipes/{recipe_id}/stats", response_model=community_schemas.RecipeStats)
async def get_recipe_stats(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    """Get statistics for a recipe"""
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Get rating stats
    rating_stats = (
        db.query(
            func.avg(models.RecipeRating.rating).label("avg"),
            func.count(models.RecipeRating.id).label("count"),
        )
        .filter(models.RecipeRating.recipe_id == recipe_id)
        .first()
    )
    
    # Get comment count
    comment_count = (
        db.query(func.count(models.RecipeComment.id))
        .filter(models.RecipeComment.recipe_id == recipe_id)
        .scalar()
    )
    
    # Get star count
    star_count = (
        db.query(func.count(models.RecipeStar.id))
        .filter(models.RecipeStar.recipe_id == recipe_id)
        .scalar()
    )
    
    # Get fork count (recipes with this as origin)
    fork_count = (
        db.query(func.count(models.Recipes.id))
        .filter(models.Recipes.origin_recipe_id == recipe_id)
        .scalar()
    )
    
    return community_schemas.RecipeStats(
        rating_average=float(rating_stats.avg) if rating_stats.avg else None,
        rating_count=rating_stats.count or 0,
        comment_count=comment_count or 0,
        star_count=star_count or 0,
        fork_count=fork_count or 0,
    )


# User Profile Endpoints

@router.get("/users/{user_id}/profile", response_model=community_schemas.UserProfile)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get public user profile"""
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user stats
    recipe_count = (
        db.query(func.count(models.Recipes.id))
        .filter(models.Recipes.user_id == user_id)
        .scalar()
    )
    
    rating_count = (
        db.query(func.count(models.RecipeRating.id))
        .filter(models.RecipeRating.user_id == user_id)
        .scalar()
    )
    
    comment_count = (
        db.query(func.count(models.RecipeComment.id))
        .filter(models.RecipeComment.user_id == user_id)
        .scalar()
    )
    
    return community_schemas.UserProfile(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        website=user.website,
        location=user.location,
        created_at=user.created_at,
        recipe_count=recipe_count or 0,
        rating_count=rating_count or 0,
        comment_count=comment_count or 0,
    )


@router.put("/users/me/profile", response_model=community_schemas.UserProfile)
async def update_user_profile(
    profile: community_schemas.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Update current user's profile"""
    current_user.bio = profile.bio
    current_user.avatar_url = profile.avatar_url
    current_user.website = profile.website
    current_user.location = profile.location
    
    db.commit()
    db.refresh(current_user)
    
    # Get user stats
    recipe_count = (
        db.query(func.count(models.Recipes.id))
        .filter(models.Recipes.user_id == current_user.id)
        .scalar()
    )
    
    rating_count = (
        db.query(func.count(models.RecipeRating.id))
        .filter(models.RecipeRating.user_id == current_user.id)
        .scalar()
    )
    
    comment_count = (
        db.query(func.count(models.RecipeComment.id))
        .filter(models.RecipeComment.user_id == current_user.id)
        .scalar()
    )
    
    return community_schemas.UserProfile(
        id=current_user.id,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        bio=current_user.bio,
        avatar_url=current_user.avatar_url,
        website=current_user.website,
        location=current_user.location,
        created_at=current_user.created_at,
        recipe_count=recipe_count or 0,
        rating_count=rating_count or 0,
        comment_count=comment_count or 0,
    )


@router.get("/users/me/starred", response_model=List[int])
async def get_starred_recipes(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_active_user),
):
    """Get list of recipe IDs starred by current user"""
    stars = (
        db.query(models.RecipeStar.recipe_id)
        .filter(models.RecipeStar.user_id == current_user.id)
        .all()
    )
    return [star.recipe_id for star in stars]
