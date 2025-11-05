"""
Tests for the American IPA seed script.
"""
import pytest
from sqlalchemy.orm import Session
import Database.Models as models
from seeds.seed_american_ipa import seed_american_ipa_recipe


def test_seed_american_ipa_creates_recipe(db_session: Session):
    """Test that the seed script creates the American IPA recipe."""
    recipe_id = seed_american_ipa_recipe()
    
    assert recipe_id is not None
    assert recipe_id > 0
    
    recipe = db_session.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    assert recipe is not None
    assert recipe.name == "American IPA (BJCP 21A)"
    assert recipe.batch_size == 25.0
    assert recipe.og == 1.063
    assert recipe.fg == 1.014
    assert recipe.ibu == 55.0
    assert recipe.abv == 6.4
    assert recipe.est_color == 14.0


def test_seed_american_ipa_creates_fermentables(db_session: Session):
    """Test that the seed script creates the fermentables."""
    recipe_id = seed_american_ipa_recipe()
    
    fermentables = (
        db_session.query(models.RecipeFermentable)
        .filter(models.RecipeFermentable.recipe_id == recipe_id)
        .all()
    )
    
    assert len(fermentables) == 4
    
    fermentable_names = {f.name for f in fermentables}
    expected_names = {
        "Pale Malt (2-Row)",
        "Wheat Malt",
        "Crystal/Caramel 40L",
        "Vienna Malt",
    }
    assert fermentable_names == expected_names
    
    total_amount = sum(f.amount for f in fermentables)
    assert total_amount == 6.0


def test_seed_american_ipa_creates_hops(db_session: Session):
    """Test that the seed script creates the hops."""
    recipe_id = seed_american_ipa_recipe()
    
    hops = (
        db_session.query(models.RecipeHop)
        .filter(models.RecipeHop.recipe_id == recipe_id)
        .all()
    )
    
    assert len(hops) == 5
    
    hop_names = {h.name for h in hops}
    expected_names = {"Cascade", "Centennial", "Citra", "Simcoe", "Amarillo"}
    assert hop_names == expected_names
    
    total_hops = sum(h.amount for h in hops)
    assert total_hops == 150.0


def test_seed_american_ipa_creates_yeast(db_session: Session):
    """Test that the seed script creates the yeast."""
    recipe_id = seed_american_ipa_recipe()
    
    yeasts = (
        db_session.query(models.RecipeYeast)
        .filter(models.RecipeYeast.recipe_id == recipe_id)
        .all()
    )
    
    assert len(yeasts) == 1
    
    yeast = yeasts[0]
    assert yeast.name == "SafAle US-05"
    assert yeast.type == "Ale"
    assert yeast.amount == 11.5
    assert yeast.attenuation == 78.0


def test_seed_american_ipa_creates_miscs(db_session: Session):
    """Test that the seed script creates the misc ingredients."""
    recipe_id = seed_american_ipa_recipe()
    
    miscs = (
        db_session.query(models.RecipeMisc)
        .filter(models.RecipeMisc.recipe_id == recipe_id)
        .all()
    )
    
    assert len(miscs) == 2
    
    misc_names = {m.name for m in miscs}
    expected_names = {"Irish Moss", "Yeast Nutrient"}
    assert misc_names == expected_names


def test_seed_american_ipa_idempotent(db_session: Session):
    """Test that running the seed script multiple times doesn't create duplicates."""
    recipe_id_1 = seed_american_ipa_recipe()
    recipe_id_2 = seed_american_ipa_recipe()
    
    assert recipe_id_1 == recipe_id_2
    
    count = (
        db_session.query(models.Recipes)
        .filter(models.Recipes.name == "American IPA (BJCP 21A)")
        .count()
    )
    assert count == 1
