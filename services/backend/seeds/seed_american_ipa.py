"""
Seed file for American IPA (BJCP 21A) recipe.

This recipe is a classic American IPA with:
- Batch Size: 25L
- IBU: 55
- EBC: 14
- OG: 1.063
- FG: 1.014
- ABV: 6.4%

Based on the user's favorite recipe that they have brewed multiple times.
This is a base recipe that will be used as a template for actual brews,
which may have alterations specific to each batch.
"""

from sqlalchemy.orm import Session

from database import SessionLocal
import Database.Models as models
from logger_config import get_logger

logger = get_logger("SeedAmericanIPA")


def seed_american_ipa_recipe() -> int:
    """
    Create the American IPA (BJCP 21A) recipe in the database.
    
    Returns:
        int: The ID of the created recipe, or the existing recipe ID if it already exists.
    """
    session: Session = SessionLocal()
    
    try:
        # Check if the recipe already exists
        existing_recipe = (
            session.query(models.Recipes)
            .filter(models.Recipes.name == "American IPA (BJCP 21A)")
            .first()
        )
        
        if existing_recipe:
            logger.info("American IPA recipe already exists with ID: %d", existing_recipe.id)
            return existing_recipe.id
        
        # Create the main recipe
        recipe = models.Recipes(
            name="American IPA (BJCP 21A)",
            version=1,
            type="All Grain",
            brewer="HoppyBrew",
            batch_size=25.0,  # 25 liters
            boil_size=30.0,  # Estimated boil volume
            boil_time=60,
            efficiency=75.0,  # Standard homebrew efficiency
            og=1.063,
            fg=1.014,
            est_og=1.063,
            est_fg=1.014,
            ibu=55.0,
            ibu_method="Tinseth",
            est_color=14.0,  # EBC
            abv=6.4,
            est_abv=6.4,
            notes=(
                "American IPA is a pale, hoppy beer with intense hop bitterness (40-70 IBU according to BJCP) "
                "and New World hop aroma - citrus, fruity, floral. One of the best-selling craft beer styles. "
                "Key elements: well-stored new hop varieties, neutral yeast with low esters, and pale malts "
                "with some wheat and specialty malts to balance the bitterness.\n\n"
                "This is a base recipe for 25L wort. It can be scaled up (e.g., multiply by 2 for 50L, by 3 for 75L)."
            ),
            display_batch_size="25 L",
            display_boil_size="30 L",
            display_og="1.063",
            display_fg="1.014",
        )
        
        session.add(recipe)
        session.flush()  # Get the recipe ID
        
        # Add fermentables (malts)
        # For a 25L batch targeting OG 1.063, we need approximately 5.5-6 kg of base malt
        # with some specialty malts for balance
        fermentables = [
            models.RecipeFermentable(
                recipe_id=recipe.id,
                name="Pale Malt (2-Row)",
                type="Grain",
                amount=5.0,  # kg
                yield_=80.0,
                color=3,  # EBC (~1.5 Lovibond)
                origin="USA",
                notes="Base malt providing clean malt backbone",
            ),
            models.RecipeFermentable(
                recipe_id=recipe.id,
                name="Wheat Malt",
                type="Grain",
                amount=0.5,  # kg
                yield_=85.0,
                color=4,  # EBC (~2 Lovibond)
                origin="USA",
                notes="Adds body and head retention",
            ),
            models.RecipeFermentable(
                recipe_id=recipe.id,
                name="Crystal/Caramel 40L",
                type="Grain",
                amount=0.3,  # kg
                yield_=75.0,
                color=79,  # EBC (~40 Lovibond)
                origin="USA",
                notes="Adds caramel sweetness to balance hop bitterness",
            ),
            models.RecipeFermentable(
                recipe_id=recipe.id,
                name="Vienna Malt",
                type="Grain",
                amount=0.2,  # kg
                yield_=78.0,
                color=7,  # EBC (~3.5 Lovibond)
                origin="Germany",
                notes="Adds malt complexity and slight sweetness",
            ),
        ]
        
        for fermentable in fermentables:
            session.add(fermentable)
        
        # Add hops for American IPA character
        # Targeting 55 IBU with citrus/fruity New World hops
        hops = [
            models.RecipeHop(
                recipe_id=recipe.id,
                name="Cascade",
                origin="USA",
                alpha=5.5,
                type="Bittering/Aroma",
                form="Pellet",
                amount=25.0,  # grams
                use="Boil",
                time=60,  # minutes
                notes="Classic American hop - citrus and grapefruit character",
                display_amount="25 g",
                display_time="60 min",
            ),
            models.RecipeHop(
                recipe_id=recipe.id,
                name="Centennial",
                origin="USA",
                alpha=10.0,
                type="Bittering/Aroma",
                form="Pellet",
                amount=20.0,  # grams
                use="Boil",
                time=30,  # minutes
                notes="Strong citrus and floral aroma",
                display_amount="20 g",
                display_time="30 min",
            ),
            models.RecipeHop(
                recipe_id=recipe.id,
                name="Citra",
                origin="USA",
                alpha=12.0,
                type="Aroma",
                form="Pellet",
                amount=30.0,  # grams
                use="Boil",
                time=15,  # minutes
                notes="Intense citrus, tropical fruit, and passion fruit notes",
                display_amount="30 g",
                display_time="15 min",
            ),
            models.RecipeHop(
                recipe_id=recipe.id,
                name="Simcoe",
                origin="USA",
                alpha=13.0,
                type="Aroma",
                form="Pellet",
                amount=25.0,  # grams
                use="Aroma",
                time=0,  # Flameout/whirlpool
                notes="Citrus, pine, and earthy notes",
                display_amount="25 g",
                display_time="Flameout",
            ),
            models.RecipeHop(
                recipe_id=recipe.id,
                name="Amarillo",
                origin="USA",
                alpha=9.0,
                type="Aroma",
                form="Pellet",
                amount=50.0,  # grams
                use="Dry Hop",
                time=5,  # days
                notes="Orange, lemon, and tropical fruit aroma",
                display_amount="50 g",
                display_time="5 days",
            ),
        ]
        
        for hop in hops:
            session.add(hop)
        
        # Add yeast - clean American ale yeast with low esters
        yeast = models.RecipeYeast(
            recipe_id=recipe.id,
            name="SafAle US-05",
            type="Ale",
            form="Dry",
            amount=11.5,  # grams
            amount_is_weight=True,
            laboratory="Fermentis",
            product_id="US-05",
            min_temperature=18.0,  # Celsius
            max_temperature=28.0,  # Celsius
            flocculation="Medium",
            attenuation=78.0,
            notes="Clean fermenting American ale yeast with neutral profile, ideal for hop-forward beers",
            best_for="American Pale Ales, IPAs, and other hop-forward styles",
            max_reuse=5,
            add_to_secondary=False,
        )
        
        session.add(yeast)
        
        # Add optional misc ingredients for clarity
        miscs = [
            models.RecipeMisc(
                recipe_id=recipe.id,
                name="Irish Moss",
                type="Fining",
                use="Boil",
                amount=5,  # grams
                time=15,  # minutes
                notes="Helps with clarity by removing proteins",
            ),
            models.RecipeMisc(
                recipe_id=recipe.id,
                name="Yeast Nutrient",
                type="Other",
                use="Boil",
                amount=2,  # grams
                time=10,  # minutes
                notes="Supports healthy yeast fermentation",
            ),
        ]
        
        for misc in miscs:
            session.add(misc)
        
        session.commit()
        logger.info("Successfully created American IPA recipe with ID: %d", recipe.id)
        return recipe.id
        
    except Exception as e:
        session.rollback()
        logger.error("Failed to create American IPA recipe: %s", str(e))
        raise
    finally:
        session.close()


def main() -> None:
    """Main entry point for the seed script."""
    recipe_id = seed_american_ipa_recipe()
    logger.info("American IPA recipe seeded with ID: %d", recipe_id)


if __name__ == "__main__":
    main()
