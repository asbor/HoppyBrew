"""
Tests for BeerXML import/export functionality
"""

import pytest
from modules.beerxml_parser import (
    parse_beerxml,
    validate_beerxml,
    BeerXMLParseError,
)


# Sample valid BeerXML data
VALID_BEERXML = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
<RECIPE>
 <NAME>Test IPA</NAME>
 <VERSION>1</VERSION>
 <TYPE>All Grain</TYPE>
 <BREWER>Test Brewer</BREWER>
 <BATCH_SIZE>20.0</BATCH_SIZE>
 <BOIL_SIZE>25.0</BOIL_SIZE>
 <BOIL_TIME>60</BOIL_TIME>
 <EFFICIENCY>75.0</EFFICIENCY>
 <HOPS>
  <HOP>
   <NAME>Cascade</NAME>
   <VERSION>1</VERSION>
   <ALPHA>5.5</ALPHA>
   <AMOUNT>0.0283</AMOUNT>
   <USE>Boil</USE>
   <TIME>60.0</TIME>
   <FORM>Pellet</FORM>
  </HOP>
 </HOPS>
 <FERMENTABLES>
  <FERMENTABLE>
   <NAME>Pale Malt</NAME>
   <VERSION>1</VERSION>
   <TYPE>Grain</TYPE>
   <AMOUNT>4.5</AMOUNT>
   <YIELD>80.0</YIELD>
   <COLOR>2.5</COLOR>
  </FERMENTABLE>
 </FERMENTABLES>
 <YEASTS>
  <YEAST>
   <NAME>US-05</NAME>
   <VERSION>1</VERSION>
   <TYPE>Ale</TYPE>
   <FORM>Dry</FORM>
   <ATTENUATION>75.0</ATTENUATION>
  </YEAST>
 </YEASTS>
 <MISCS>
  <MISC>
   <NAME>Irish Moss</NAME>
   <VERSION>1</VERSION>
   <TYPE>Fining</TYPE>
   <USE>Boil</USE>
   <TIME>10.0</TIME>
  </MISC>
 </MISCS>
 <NOTES>A test IPA recipe</NOTES>
 <OG>1.055</OG>
 <FG>1.012</FG>
 <IBU>45.0</IBU>
</RECIPE>
</RECIPES>
"""


INVALID_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
<RECIPE>
 <NAME>Broken Recipe
</RECIPE>
</RECIPES>
"""


EMPTY_RECIPES = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
</RECIPES>
"""


def test_parse_valid_beerxml():
    """Test parsing valid BeerXML content"""
    recipes = parse_beerxml(VALID_BEERXML)

    assert len(recipes) == 1
    recipe = recipes[0]

    # Check recipe fields
    assert recipe.name == "Test IPA"
    assert recipe.version == 1
    assert recipe.type == "All Grain"
    assert recipe.brewer == "Test Brewer"
    assert recipe.batch_size == 20.0
    assert recipe.boil_size == 25.0
    assert recipe.boil_time == 60
    assert recipe.efficiency == 75.0
    assert recipe.notes == "A test IPA recipe"
    assert recipe.og == 1.055
    assert recipe.fg == 1.012
    assert recipe.ibu == 45.0

    # Check hops
    assert len(recipe.hops) == 1
    hop = recipe.hops[0]
    assert hop.name == "Cascade"
    assert hop.alpha == 5.5
    assert hop.amount == 0.0283
    assert hop.use == "Boil"
    assert hop.time == 60.0
    assert hop.form == "Pellet"

    # Check fermentables
    assert len(recipe.fermentables) == 1
    ferm = recipe.fermentables[0]
    assert ferm.name == "Pale Malt"
    assert ferm.type == "Grain"
    assert ferm.amount == 4.5
    assert ferm.yield_ == 80.0
    assert ferm.color == 2.5

    # Check yeasts
    assert len(recipe.yeasts) == 1
    yeast = recipe.yeasts[0]
    assert yeast.name == "US-05"
    assert yeast.type == "Ale"
    assert yeast.form == "Dry"
    assert yeast.attenuation == 75.0

    # Check miscs
    assert len(recipe.miscs) == 1
    misc = recipe.miscs[0]
    assert misc.name == "Irish Moss"
    assert misc.type == "Fining"
    assert misc.use == "Boil"
    assert misc.time == 10.0


def test_parse_invalid_xml():
    """Test parsing invalid XML raises error"""
    with pytest.raises(BeerXMLParseError) as exc_info:
        parse_beerxml(INVALID_XML)

    assert "Invalid XML format" in str(exc_info.value)


def test_parse_empty_recipes():
    """Test parsing empty RECIPES element raises error"""
    with pytest.raises(BeerXMLParseError) as exc_info:
        parse_beerxml(EMPTY_RECIPES)

    assert "No valid recipes" in str(exc_info.value)


def test_validate_valid_beerxml():
    """Test validation of valid BeerXML"""
    result = validate_beerxml(VALID_BEERXML)

    assert result["valid"] is True
    assert result["recipe_count"] == 1
    assert len(result["errors"]) == 0


def test_validate_invalid_xml():
    """Test validation of invalid XML"""
    result = validate_beerxml(INVALID_XML)

    assert result["valid"] is False
    assert len(result["errors"]) > 0
    assert "Invalid XML format" in result["errors"][0]


def test_validate_empty_recipes():
    """Test validation of empty recipes"""
    result = validate_beerxml(EMPTY_RECIPES)

    assert result["valid"] is False
    assert "No RECIPE elements found" in result["errors"][0]


def test_parse_single_recipe_root():
    """Test parsing BeerXML with RECIPE as root element"""
    single_recipe_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPE>
 <NAME>Single Recipe</NAME>
 <VERSION>1</VERSION>
 <TYPE>Extract</TYPE>
 <BATCH_SIZE>19.0</BATCH_SIZE>
</RECIPE>
"""

    recipes = parse_beerxml(single_recipe_xml)

    assert len(recipes) == 1
    assert recipes[0].name == "Single Recipe"
    assert recipes[0].type == "Extract"


def test_parse_multiple_recipes():
    """Test parsing multiple recipes"""
    multi_recipe_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
<RECIPE>
 <NAME>Recipe 1</NAME>
 <VERSION>1</VERSION>
 <BATCH_SIZE>20.0</BATCH_SIZE>
</RECIPE>
<RECIPE>
 <NAME>Recipe 2</NAME>
 <VERSION>1</VERSION>
 <BATCH_SIZE>19.0</BATCH_SIZE>
</RECIPE>
</RECIPES>
"""

    recipes = parse_beerxml(multi_recipe_xml)

    assert len(recipes) == 2
    assert recipes[0].name == "Recipe 1"
    assert recipes[1].name == "Recipe 2"


def test_parse_recipe_with_optional_fields():
    """Test parsing recipe with many optional fields"""
    full_recipe_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPE>
 <NAME>Full Recipe</NAME>
 <VERSION>1</VERSION>
 <TYPE>All Grain</TYPE>
 <BREWER>Test Brewer</BREWER>
 <ASST_BREWER>Assistant</ASST_BREWER>
 <BATCH_SIZE>20.0</BATCH_SIZE>
 <BOIL_SIZE>25.0</BOIL_SIZE>
 <BOIL_TIME>60</BOIL_TIME>
 <EFFICIENCY>75.0</EFFICIENCY>
 <NOTES>Test notes</NOTES>
 <TASTE_NOTES>Hoppy and bitter</TASTE_NOTES>
 <TASTE_RATING>8</TASTE_RATING>
 <OG>1.055</OG>
 <FG>1.012</FG>
 <FERMENTATION_STAGES>2</FERMENTATION_STAGES>
 <PRIMARY_AGE>7</PRIMARY_AGE>
 <PRIMARY_TEMP>20.0</PRIMARY_TEMP>
 <SECONDARY_AGE>14</SECONDARY_AGE>
 <SECONDARY_TEMP>18.0</SECONDARY_TEMP>
 <TERTIARY_AGE>0</TERTIARY_AGE>
 <AGE>30</AGE>
 <AGE_TEMP>12.0</AGE_TEMP>
 <CARBONATION_USED>Bottle</CARBONATION_USED>
 <EST_OG>1.056</EST_OG>
 <EST_FG>1.013</EST_FG>
 <EST_COLOR>8.0</EST_COLOR>
 <IBU>45.0</IBU>
 <IBU_METHOD>Tinseth</IBU_METHOD>
 <EST_ABV>5.7</EST_ABV>
 <ABV>5.6</ABV>
 <ACTUAL_EFFICIENCY>73.0</ACTUAL_EFFICIENCY>
 <CALORIES>180.0</CALORIES>
 <DISPLAY_BATCH_SIZE>20 L</DISPLAY_BATCH_SIZE>
 <DISPLAY_BOIL_SIZE>25 L</DISPLAY_BOIL_SIZE>
 <DISPLAY_OG>1.055 SG</DISPLAY_OG>
 <DISPLAY_FG>1.012 SG</DISPLAY_FG>
</RECIPE>
"""

    recipes = parse_beerxml(full_recipe_xml)
    recipe = recipes[0]

    assert recipe.name == "Full Recipe"
    assert recipe.asst_brewer == "Assistant"
    assert recipe.taste_notes == "Hoppy and bitter"
    assert recipe.taste_rating == 8
    assert recipe.fermentation_stages == 2
    assert recipe.primary_age == 7
    assert recipe.primary_temp == 20.0
    assert recipe.secondary_age == 14
    assert recipe.secondary_temp == 18.0
    assert recipe.carbonation_used == "Bottle"
    assert recipe.ibu_method == "Tinseth"
    assert recipe.est_abv == 5.7
    assert recipe.abv == 5.6
    assert recipe.actual_efficiency == 73.0
    assert recipe.calories == 180.0


def test_parse_boolean_fields():
    """Test parsing boolean fields correctly"""
    bool_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPE>
 <NAME>Bool Test</NAME>
 <VERSION>1</VERSION>
 <FERMENTABLES>
  <FERMENTABLE>
   <NAME>Test Grain</NAME>
   <VERSION>1</VERSION>
   <ADD_AFTER_BOIL>TRUE</ADD_AFTER_BOIL>
   <RECOMMEND_MASH>FALSE</RECOMMEND_MASH>
  </FERMENTABLE>
 </FERMENTABLES>
</RECIPE>
"""

    recipes = parse_beerxml(bool_xml)
    ferm = recipes[0].fermentables[0]

    assert ferm.add_after_boil is True
    assert ferm.recommend_mash is False


def test_parse_recipe_with_missing_ingredients():
    """Test parsing recipe with no ingredients sections"""
    minimal_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPE>
 <NAME>Minimal Recipe</NAME>
 <VERSION>1</VERSION>
 <BATCH_SIZE>20.0</BATCH_SIZE>
</RECIPE>
"""

    recipes = parse_beerxml(minimal_xml)
    recipe = recipes[0]

    assert recipe.name == "Minimal Recipe"
    assert len(recipe.hops) == 0
    assert len(recipe.fermentables) == 0
    assert len(recipe.yeasts) == 0
    assert len(recipe.miscs) == 0
