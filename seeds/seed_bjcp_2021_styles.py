"""
Seed script for BJCP 2021 Beer Styles
Populates the database with a sample of BJCP 2021 styles
"""

import sys
import os

# Add the services/backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'backend'))

from database import SessionLocal
from Database.Models import StyleGuidelineSource, StyleCategory, BeerStyle


def seed_bjcp_2021_styles():
    """Seed BJCP 2021 style guidelines and selected beer styles"""
    
    db = SessionLocal()
    
    try:
        # Check if BJCP 2021 already exists
        existing = db.query(StyleGuidelineSource).filter(
            StyleGuidelineSource.name == "BJCP 2021"
        ).first()
        
        if existing:
            print("BJCP 2021 guidelines already exist. Skipping seed.")
            return
        
        # Create BJCP 2021 guideline source
        print("Creating BJCP 2021 guideline source...")
        bjcp_2021 = StyleGuidelineSource(
            name="BJCP 2021",
            year=2021,
            abbreviation="BJCP",
            description="Beer Judge Certification Program 2021 Style Guidelines",
            is_active=True
        )
        db.add(bjcp_2021)
        db.flush()  # Flush to get the ID
        
        # Create categories
        print("Creating style categories...")
        
        # Category 21: IPA
        cat_ipa = StyleCategory(
            guideline_source_id=bjcp_2021.id,
            name="IPA",
            code="21",
            description="India Pale Ale"
        )
        db.add(cat_ipa)
        db.flush()
        
        # Category 18: Pale American Ale
        cat_pale_american = StyleCategory(
            guideline_source_id=bjcp_2021.id,
            name="Pale American Ale",
            code="18",
            description="American pale ales and related styles"
        )
        db.add(cat_pale_american)
        db.flush()
        
        # Category 10: German Lager
        cat_german_lager = StyleCategory(
            guideline_source_id=bjcp_2021.id,
            name="German Lager",
            code="10",
            description="German lager styles"
        )
        db.add(cat_german_lager)
        db.flush()
        
        # Create sample beer styles
        print("Creating beer styles...")
        
        # 21A: American IPA
        american_ipa = BeerStyle(
            guideline_source_id=bjcp_2021.id,
            category_id=cat_ipa.id,
            name="American IPA",
            style_code="21A",
            subcategory="American IPA",
            abv_min=5.5,
            abv_max=7.5,
            og_min=1.056,
            og_max=1.070,
            fg_min=1.008,
            fg_max=1.014,
            ibu_min=40,
            ibu_max=70,
            color_min_srm=6,
            color_max_srm=14,
            color_min_ebc=12,
            color_max_ebc=28,
            description="A decidedly hoppy and bitter, moderately strong American pale ale, showcasing modern American or New World hop varieties.",
            aroma="A prominent to intense hop aroma featuring one or more characteristics of American or New World hops, such as citrus, floral, pine, resinous, spicy, tropical fruit, stone fruit, berry, melon, etc.",
            appearance="Color ranges from medium gold to light reddish-amber. Should be clear, although unfiltered dry-hopped versions may be a bit hazy. Medium-sized, white to off-white head with good persistence.",
            flavor="Hop flavor is medium to very high, and should reflect an American or New World hop character, such as citrus, floral, pine, resinous, spicy, tropical fruit, stone fruit, berry, melon, etc.",
            mouthfeel="Medium-light to medium body, with a smooth texture. Medium to medium-high carbonation. No harsh hop-derived astringency.",
            overall_impression="A decidedly hoppy and bitter, moderately strong American pale ale, showcasing modern American or New World hop varieties. The balance is hop-forward, with a clean fermentation profile, dryish finish, and clean, supporting malt allowing a creative range of hop character to shine through.",
            comments="A modern American craft beer interpretation of the historical English style, brewed using American ingredients and attitude.",
            history="The first American craft beer adaptation of this British style is generally believed to be Anchor Liberty Ale, first brewed in 1975 and using whole Cascade hops.",
            ingredients="Pale ale or 2-row brewers malt as the base, American or New World hops, American or English yeast with a clean or slightly fruity profile.",
            comparison="Stronger and more highly hopped than American Pale Ale. Compared to English IPAs, has less of the 'English' character from malt, hops, and yeast.",
            examples="Bell's Two-Hearted Ale, Cigar City Jai Alai, Fat Head's Head Hunter IPA, Firestone Walker Union Jack, Russian River Blind Pig IPA, Stone IPA",
            is_custom=False
        )
        db.add(american_ipa)
        
        # 18B: American Pale Ale
        american_pale_ale = BeerStyle(
            guideline_source_id=bjcp_2021.id,
            category_id=cat_pale_american.id,
            name="American Pale Ale",
            style_code="18B",
            subcategory="American Pale Ale",
            abv_min=4.5,
            abv_max=6.2,
            og_min=1.045,
            og_max=1.060,
            fg_min=1.010,
            fg_max=1.015,
            ibu_min=30,
            ibu_max=50,
            color_min_srm=5,
            color_max_srm=10,
            color_min_ebc=10,
            color_max_ebc=20,
            description="An average-strength, hop-forward, pale American craft beer with sufficient supporting malt to make the beer balanced and drinkable.",
            aroma="Moderate to moderately-high hop aroma from American or New World hop varieties with a wide range of possible characteristics, including citrus, floral, pine, resinous, spicy, tropical fruit, stone fruit, berry, or melon.",
            appearance="Pale golden to deep amber. Moderately large white to off-white head with good retention. Generally quite clear.",
            flavor="Moderate to high hop flavor, typically showing an American or New World hop character. Low to moderate maltiness supports the hop presentation, and may show low amounts of specialty malt character.",
            mouthfeel="Medium-light to medium body. Moderate to high carbonation. Overall smooth finish without astringency and harshness.",
            overall_impression="An average-strength, hop-forward, pale American craft beer with sufficient supporting malt to make the beer balanced and drinkable. The clean fermentation profile allows creative hop character to shine through.",
            comments="New hop varieties and usage methods continue to be developed in this style.",
            history="A modern American craft beer era adaptation of English pale ale, reflecting indigenous ingredients.",
            ingredients="Pale ale malt, typically North American two-row. American or New World hops. American or English ale yeast.",
            comparison="Typically lighter in color, cleaner in fermentation by-products, and having less caramel flavors than English counterparts.",
            examples="Deschutes Mirror Pond Pale Ale, Half Acre Daisy Cutter Pale Ale, Great Lakes Burning River, Sierra Nevada Pale Ale, Stone Pale Ale 2.0",
            is_custom=False
        )
        db.add(american_pale_ale)
        
        # 10A: Helles
        helles = BeerStyle(
            guideline_source_id=bjcp_2021.id,
            category_id=cat_german_lager.id,
            name="Helles",
            style_code="10A",
            subcategory="Munich Helles",
            abv_min=4.7,
            abv_max=5.4,
            og_min=1.044,
            og_max=1.048,
            fg_min=1.006,
            fg_max=1.012,
            ibu_min=16,
            ibu_max=22,
            color_min_srm=3,
            color_max_srm=5,
            color_min_ebc=6,
            color_max_ebc=10,
            description="A gold-colored German lager with a smooth, malty flavor and a soft, dry finish. Subtle spicy, floral, or herbal hops and restrained bitterness help keep the balance malty but not sweet.",
            aroma="Moderate grainy-sweet malt aroma. Low to moderately-low spicy, floral, or herbal hop aroma. Pleasant, clean fermentation profile, with malt dominating the balance.",
            appearance="Medium yellow to pale gold. Clear. Persistent creamy white head.",
            flavor="Moderately malty start with the suggestion of sweetness, moderate grainy-sweet malt flavor with a soft, rounded palate impression, supported by a low to medium-low hop bitterness.",
            mouthfeel="Medium body. Medium carbonation. Smooth, well-lagered character.",
            overall_impression="A gold-colored German lager with a smooth, malty flavor and a soft, dry finish. Subtle spicy, floral, or herbal hops and restrained bitterness help keep the balance malty but not sweet, which helps make this beer a refreshing, everyday drink.",
            comments="A fully-attenuated Pils malt showcase, Helles is a malt-accentuated beer that is not overly sweet, but rather focuses on malt flavor with underlying hop bitterness in a supporting role.",
            history="Created in Munich in 1894 at the Spaten brewery to compete with pale Pilsner-type beers.",
            ingredients="Continental Pilsner malt, traditional German Saazer-type hop varieties, clean German lager yeast.",
            comparison="Similar in malt balance and bitterness to Munich Dunkel, but less malty-sweet in nature and pale rather than dark and rich.",
            examples="Augustiner Lagerbier Hell, Hacker-Pschorr Münchner Gold, Löwenbraü Original, Paulaner Münchner Lager, Spaten Premium Lager, Weihenstephaner Original",
            is_custom=False
        )
        db.add(helles)
        
        # Commit all changes
        db.commit()
        print("Successfully seeded BJCP 2021 styles!")
        print(f"  - Created guideline source: BJCP 2021")
        print(f"  - Created 3 categories")
        print(f"  - Created 3 beer styles")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting BJCP 2021 seed process...")
    seed_bjcp_2021_styles()
    print("Seed process complete!")
