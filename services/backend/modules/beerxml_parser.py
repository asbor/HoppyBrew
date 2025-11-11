"""
BeerXML Parser Module

This module provides functionality to parse BeerXML format (version 1.0/2.0)
for importing and exporting brewing recipes.

BeerXML is an XML-based standard for exchanging brewing recipe data between
different brewing software applications.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ValidationError


class BeerXMLParseError(Exception):
    """Custom exception for BeerXML parsing errors"""
    pass


class BeerXMLHop(BaseModel):
    """Represents a hop in BeerXML format"""
    name: str
    version: Optional[int] = 1
    alpha: Optional[float] = None
    amount: Optional[float] = None
    use: Optional[str] = None
    time: Optional[float] = None
    notes: Optional[str] = None
    type: Optional[str] = None
    form: Optional[str] = None
    beta: Optional[float] = None
    hsi: Optional[float] = None
    origin: Optional[str] = None
    substitutes: Optional[str] = None
    humulene: Optional[float] = None
    caryophyllene: Optional[float] = None
    cohumulone: Optional[float] = None
    myrcene: Optional[float] = None
    display_amount: Optional[str] = None
    inventory: Optional[str] = None
    display_time: Optional[str] = None


class BeerXMLFermentable(BaseModel):
    """Represents a fermentable in BeerXML format"""
    name: str
    version: Optional[int] = 1
    type: Optional[str] = None
    amount: Optional[float] = None
    yield_: Optional[float] = Field(None, alias="yield")
    color: Optional[float] = None
    add_after_boil: Optional[bool] = False
    origin: Optional[str] = None
    supplier: Optional[str] = None
    notes: Optional[str] = None
    coarse_fine_diff: Optional[float] = None
    moisture: Optional[float] = None
    diastatic_power: Optional[float] = None
    protein: Optional[float] = None
    max_in_batch: Optional[float] = None
    recommend_mash: Optional[bool] = None
    ibu_gal_per_lb: Optional[float] = None
    display_amount: Optional[str] = None
    potential: Optional[float] = None
    inventory: Optional[str] = None
    display_color: Optional[str] = None


class BeerXMLYeast(BaseModel):
    """Represents a yeast in BeerXML format"""
    name: str
    version: Optional[int] = 1
    type: Optional[str] = None
    form: Optional[str] = None
    amount: Optional[float] = None
    amount_is_weight: Optional[bool] = False
    laboratory: Optional[str] = None
    product_id: Optional[str] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    flocculation: Optional[str] = None
    attenuation: Optional[float] = None
    notes: Optional[str] = None
    best_for: Optional[str] = None
    max_reuse: Optional[int] = None
    times_cultured: Optional[int] = None
    add_to_secondary: Optional[bool] = False
    display_amount: Optional[str] = None
    disp_min_temp: Optional[str] = None
    disp_max_temp: Optional[str] = None
    inventory: Optional[str] = None
    culture_date: Optional[str] = None


class BeerXMLMisc(BaseModel):
    """Represents a miscellaneous ingredient in BeerXML format"""
    name: str
    version: Optional[int] = 1
    type: Optional[str] = None
    use: Optional[str] = None
    amount: Optional[float] = None
    time: Optional[float] = None
    amount_is_weight: Optional[bool] = False
    use_for: Optional[str] = None
    notes: Optional[str] = None
    display_amount: Optional[str] = None
    inventory: Optional[str] = None
    display_time: Optional[str] = None
    batch_size: Optional[float] = None


class BeerXMLRecipe(BaseModel):
    """Represents a complete recipe in BeerXML format"""
    name: str
    version: Optional[int] = 1
    type: Optional[str] = None
    brewer: Optional[str] = None
    asst_brewer: Optional[str] = None
    batch_size: Optional[float] = None
    boil_size: Optional[float] = None
    boil_time: Optional[int] = None
    efficiency: Optional[float] = None
    hops: List[BeerXMLHop] = []
    fermentables: List[BeerXMLFermentable] = []
    yeasts: List[BeerXMLYeast] = []
    miscs: List[BeerXMLMisc] = []
    notes: Optional[str] = None
    taste_notes: Optional[str] = None
    taste_rating: Optional[int] = None
    og: Optional[float] = None
    fg: Optional[float] = None
    fermentation_stages: Optional[int] = None
    primary_age: Optional[int] = None
    primary_temp: Optional[float] = None
    secondary_age: Optional[int] = None
    secondary_temp: Optional[float] = None
    tertiary_age: Optional[int] = None
    tertiary_temp: Optional[float] = None
    age: Optional[int] = None
    age_temp: Optional[float] = None
    carbonation_used: Optional[str] = None
    est_og: Optional[float] = None
    est_fg: Optional[float] = None
    est_color: Optional[float] = None
    ibu: Optional[float] = None
    ibu_method: Optional[str] = None
    est_abv: Optional[float] = None
    abv: Optional[float] = None
    actual_efficiency: Optional[float] = None
    calories: Optional[float] = None
    display_batch_size: Optional[str] = None
    display_boil_size: Optional[str] = None
    display_og: Optional[str] = None
    display_fg: Optional[str] = None
    display_primary_temp: Optional[str] = None
    display_secondary_temp: Optional[str] = None
    display_tertiary_temp: Optional[str] = None
    display_age_temp: Optional[str] = None


def _get_text(element: ET.Element, tag: str, default: Any = None) -> Any:
    """
    Safely extract text content from an XML element.

    Args:
        element: Parent XML element
        tag: Tag name to find
        default: Default value if tag not found or empty

    Returns:
        Text content or default value
    """
    child = element.find(tag)
    if child is None or child.text is None:
        return default
    return child.text.strip()


def _get_float(element: ET.Element, tag: str, default: Optional[float] = None) -> Optional[float]:
    """Extract float value from XML element"""
    text = _get_text(element, tag)
    if text is None:
        return default
    try:
        return float(text)
    except (ValueError, TypeError):
        return default


def _get_int(element: ET.Element, tag: str, default: Optional[int] = None) -> Optional[int]:
    """Extract integer value from XML element"""
    text = _get_text(element, tag)
    if text is None:
        return default
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


def _get_bool(element: ET.Element, tag: str, default: bool = False) -> bool:
    """Extract boolean value from XML element"""
    text = _get_text(element, tag)
    if text is None:
        return default
    return text.upper() in ('TRUE', 'YES', '1')


def _parse_hop(hop_element: ET.Element) -> BeerXMLHop:
    """Parse a HOP element from BeerXML"""
    return BeerXMLHop(
        name=_get_text(hop_element, 'NAME', ''),
        version=_get_int(hop_element, 'VERSION', 1),
        alpha=_get_float(hop_element, 'ALPHA'),
        amount=_get_float(hop_element, 'AMOUNT'),
        use=_get_text(hop_element, 'USE'),
        time=_get_float(hop_element, 'TIME'),
        notes=_get_text(hop_element, 'NOTES'),
        type=_get_text(hop_element, 'TYPE'),
        form=_get_text(hop_element, 'FORM'),
        beta=_get_float(hop_element, 'BETA'),
        hsi=_get_float(hop_element, 'HSI'),
        origin=_get_text(hop_element, 'ORIGIN'),
        substitutes=_get_text(hop_element, 'SUBSTITUTES'),
        humulene=_get_float(hop_element, 'HUMULENE'),
        caryophyllene=_get_float(hop_element, 'CARYOPHYLLENE'),
        cohumulone=_get_float(hop_element, 'COHUMULONE'),
        myrcene=_get_float(hop_element, 'MYRCENE'),
        display_amount=_get_text(hop_element, 'DISPLAY_AMOUNT'),
        inventory=_get_text(hop_element, 'INVENTORY'),
        display_time=_get_text(hop_element, 'DISPLAY_TIME'),
    )


def _parse_fermentable(ferm_element: ET.Element) -> BeerXMLFermentable:
    """Parse a FERMENTABLE element from BeerXML"""
    return BeerXMLFermentable(
        name=_get_text(ferm_element, 'NAME', ''),
        version=_get_int(ferm_element, 'VERSION', 1),
        type=_get_text(ferm_element, 'TYPE'),
        amount=_get_float(ferm_element, 'AMOUNT'),
        yield_=_get_float(ferm_element, 'YIELD'),
        color=_get_float(ferm_element, 'COLOR'),
        add_after_boil=_get_bool(ferm_element, 'ADD_AFTER_BOIL'),
        origin=_get_text(ferm_element, 'ORIGIN'),
        supplier=_get_text(ferm_element, 'SUPPLIER'),
        notes=_get_text(ferm_element, 'NOTES'),
        coarse_fine_diff=_get_float(ferm_element, 'COARSE_FINE_DIFF'),
        moisture=_get_float(ferm_element, 'MOISTURE'),
        diastatic_power=_get_float(ferm_element, 'DIASTATIC_POWER'),
        protein=_get_float(ferm_element, 'PROTEIN'),
        max_in_batch=_get_float(ferm_element, 'MAX_IN_BATCH'),
        recommend_mash=(
            _get_bool(ferm_element, 'RECOMMEND_MASH')
            if ferm_element.find('RECOMMEND_MASH') is not None
            else None
        ),
        ibu_gal_per_lb=_get_float(ferm_element, 'IBU_GAL_PER_LB'),
        display_amount=_get_text(ferm_element, 'DISPLAY_AMOUNT'),
        potential=_get_float(ferm_element, 'POTENTIAL'),
        inventory=_get_text(ferm_element, 'INVENTORY'),
        display_color=_get_text(ferm_element, 'DISPLAY_COLOR'),
    )


def _parse_yeast(yeast_element: ET.Element) -> BeerXMLYeast:
    """Parse a YEAST element from BeerXML"""
    return BeerXMLYeast(
        name=_get_text(yeast_element, 'NAME', ''),
        version=_get_int(yeast_element, 'VERSION', 1),
        type=_get_text(yeast_element, 'TYPE'),
        form=_get_text(yeast_element, 'FORM'),
        amount=_get_float(yeast_element, 'AMOUNT'),
        amount_is_weight=_get_bool(yeast_element, 'AMOUNT_IS_WEIGHT'),
        laboratory=_get_text(yeast_element, 'LABORATORY'),
        product_id=_get_text(yeast_element, 'PRODUCT_ID'),
        min_temperature=_get_float(yeast_element, 'MIN_TEMPERATURE'),
        max_temperature=_get_float(yeast_element, 'MAX_TEMPERATURE'),
        flocculation=_get_text(yeast_element, 'FLOCCULATION'),
        attenuation=_get_float(yeast_element, 'ATTENUATION'),
        notes=_get_text(yeast_element, 'NOTES'),
        best_for=_get_text(yeast_element, 'BEST_FOR'),
        max_reuse=_get_int(yeast_element, 'MAX_REUSE'),
        times_cultured=_get_int(yeast_element, 'TIMES_CULTURED'),
        add_to_secondary=_get_bool(yeast_element, 'ADD_TO_SECONDARY'),
        display_amount=_get_text(yeast_element, 'DISPLAY_AMOUNT'),
        disp_min_temp=_get_text(yeast_element, 'DISP_MIN_TEMP'),
        disp_max_temp=_get_text(yeast_element, 'DISP_MAX_TEMP'),
        inventory=_get_text(yeast_element, 'INVENTORY'),
        culture_date=_get_text(yeast_element, 'CULTURE_DATE'),
    )


def _parse_misc(misc_element: ET.Element) -> BeerXMLMisc:
    """Parse a MISC element from BeerXML"""
    return BeerXMLMisc(
        name=_get_text(misc_element, 'NAME', ''),
        version=_get_int(misc_element, 'VERSION', 1),
        type=_get_text(misc_element, 'TYPE'),
        use=_get_text(misc_element, 'USE'),
        amount=_get_float(misc_element, 'AMOUNT'),
        time=_get_float(misc_element, 'TIME'),
        amount_is_weight=_get_bool(misc_element, 'AMOUNT_IS_WEIGHT'),
        use_for=_get_text(misc_element, 'USE_FOR'),
        notes=_get_text(misc_element, 'NOTES'),
        display_amount=_get_text(misc_element, 'DISPLAY_AMOUNT'),
        inventory=_get_text(misc_element, 'INVENTORY'),
        display_time=_get_text(misc_element, 'DISPLAY_TIME'),
        batch_size=_get_float(misc_element, 'BATCH_SIZE'),
    )


def _parse_recipe(recipe_element: ET.Element) -> BeerXMLRecipe:
    """Parse a RECIPE element from BeerXML"""

    # Parse hops
    hops = []
    hops_element = recipe_element.find('HOPS')
    if hops_element is not None:
        for hop_elem in hops_element.findall('HOP'):
            try:
                hops.append(_parse_hop(hop_elem))
            except (ValidationError, ValueError):
                # Skip malformed hops but continue parsing
                pass

    # Parse fermentables
    fermentables = []
    fermentables_element = recipe_element.find('FERMENTABLES')
    if fermentables_element is not None:
        for ferm_elem in fermentables_element.findall('FERMENTABLE'):
            try:
                fermentables.append(_parse_fermentable(ferm_elem))
            except (ValidationError, ValueError):
                # Skip malformed fermentables but continue parsing
                pass

    # Parse yeasts
    yeasts = []
    yeasts_element = recipe_element.find('YEASTS')
    if yeasts_element is not None:
        for yeast_elem in yeasts_element.findall('YEAST'):
            try:
                yeasts.append(_parse_yeast(yeast_elem))
            except (ValidationError, ValueError):
                # Skip malformed yeasts but continue parsing
                pass

    # Parse miscs
    miscs = []
    miscs_element = recipe_element.find('MISCS')
    if miscs_element is not None:
        for misc_elem in miscs_element.findall('MISC'):
            try:
                miscs.append(_parse_misc(misc_elem))
            except (ValidationError, ValueError):
                # Skip malformed miscs but continue parsing
                pass

    return BeerXMLRecipe(
        name=_get_text(recipe_element, 'NAME', ''),
        version=_get_int(recipe_element, 'VERSION', 1),
        type=_get_text(recipe_element, 'TYPE'),
        brewer=_get_text(recipe_element, 'BREWER'),
        asst_brewer=_get_text(recipe_element, 'ASST_BREWER'),
        batch_size=_get_float(recipe_element, 'BATCH_SIZE'),
        boil_size=_get_float(recipe_element, 'BOIL_SIZE'),
        boil_time=_get_int(recipe_element, 'BOIL_TIME'),
        efficiency=_get_float(recipe_element, 'EFFICIENCY'),
        hops=hops,
        fermentables=fermentables,
        yeasts=yeasts,
        miscs=miscs,
        notes=_get_text(recipe_element, 'NOTES'),
        taste_notes=_get_text(recipe_element, 'TASTE_NOTES'),
        taste_rating=_get_int(recipe_element, 'TASTE_RATING'),
        og=_get_float(recipe_element, 'OG'),
        fg=_get_float(recipe_element, 'FG'),
        fermentation_stages=_get_int(recipe_element, 'FERMENTATION_STAGES'),
        primary_age=_get_int(recipe_element, 'PRIMARY_AGE'),
        primary_temp=_get_float(recipe_element, 'PRIMARY_TEMP'),
        secondary_age=_get_int(recipe_element, 'SECONDARY_AGE'),
        secondary_temp=_get_float(recipe_element, 'SECONDARY_TEMP'),
        tertiary_age=_get_int(recipe_element, 'TERTIARY_AGE'),
        tertiary_temp=_get_float(recipe_element, 'TERTIARY_TEMP'),
        age=_get_int(recipe_element, 'AGE'),
        age_temp=_get_float(recipe_element, 'AGE_TEMP'),
        carbonation_used=_get_text(recipe_element, 'CARBONATION_USED'),
        est_og=_get_float(recipe_element, 'EST_OG'),
        est_fg=_get_float(recipe_element, 'EST_FG'),
        est_color=_get_float(recipe_element, 'EST_COLOR'),
        ibu=_get_float(recipe_element, 'IBU'),
        ibu_method=_get_text(recipe_element, 'IBU_METHOD'),
        est_abv=_get_float(recipe_element, 'EST_ABV'),
        abv=_get_float(recipe_element, 'ABV'),
        actual_efficiency=_get_float(recipe_element, 'ACTUAL_EFFICIENCY'),
        calories=_get_float(recipe_element, 'CALORIES'),
        display_batch_size=_get_text(recipe_element, 'DISPLAY_BATCH_SIZE'),
        display_boil_size=_get_text(recipe_element, 'DISPLAY_BOIL_SIZE'),
        display_og=_get_text(recipe_element, 'DISPLAY_OG'),
        display_fg=_get_text(recipe_element, 'DISPLAY_FG'),
        display_primary_temp=_get_text(recipe_element, 'DISPLAY_PRIMARY_TEMP'),
        display_secondary_temp=_get_text(recipe_element, 'DISPLAY_SECONDARY_TEMP'),
        display_tertiary_temp=_get_text(recipe_element, 'DISPLAY_TERTIARY_TEMP'),
        display_age_temp=_get_text(recipe_element, 'DISPLAY_AGE_TEMP'),
    )


def parse_beerxml(xml_content: bytes) -> List[BeerXMLRecipe]:
    """
    Parse BeerXML content and return a list of recipes.

    Args:
        xml_content: Raw XML content as bytes

    Returns:
        List of BeerXMLRecipe objects

    Raises:
        BeerXMLParseError: If XML is malformed or invalid
    """
    try:
        tree = ET.ElementTree(ET.fromstring(xml_content))
    except ET.ParseError as e:
        raise BeerXMLParseError(f"Invalid XML format: {str(e)}")

    root = tree.getroot()

    # Handle both RECIPES and RECIPE as root elements
    if root.tag == 'RECIPE':
        recipe_elements = [root]
    elif root.tag == 'RECIPES':
        recipe_elements = root.findall('RECIPE')
    else:
        raise BeerXMLParseError(
            f"Invalid root element: expected RECIPES or RECIPE, got {root.tag}"
        )

    if not recipe_elements:
        raise BeerXMLParseError("No RECIPE elements found in XML")

    recipes = []
    for recipe_elem in recipe_elements:
        try:
            recipe = _parse_recipe(recipe_elem)
            recipes.append(recipe)
        except ValidationError:
            # Skip recipes that fail validation
            pass

    if not recipes:
        raise BeerXMLParseError("No valid recipes could be parsed from XML")

    return recipes


def validate_beerxml(xml_content: bytes) -> Dict[str, Any]:
    """
    Validate BeerXML content without parsing into full objects.

    Args:
        xml_content: Raw XML content as bytes

    Returns:
        Dictionary with validation results:
        {
            "valid": bool,
            "recipe_count": int,
            "errors": List[str],
            "warnings": List[str]
        }
    """
    result = {
        "valid": True,
        "recipe_count": 0,
        "errors": [],
        "warnings": []
    }

    try:
        tree = ET.ElementTree(ET.fromstring(xml_content))
    except ET.ParseError as e:
        result["valid"] = False
        result["errors"].append(f"Invalid XML format: {str(e)}")
        return result

    root = tree.getroot()

    # Check root element
    if root.tag not in ('RECIPES', 'RECIPE'):
        result["valid"] = False
        result["errors"].append(
            f"Invalid root element: expected RECIPES or RECIPE, got {root.tag}"
        )
        return result

    # Get recipe elements
    if root.tag == 'RECIPE':
        recipe_elements = [root]
    else:
        recipe_elements = root.findall('RECIPE')

    if not recipe_elements:
        result["valid"] = False
        result["errors"].append("No RECIPE elements found in XML")
        return result

    result["recipe_count"] = len(recipe_elements)

    # Validate each recipe has required fields
    for i, recipe_elem in enumerate(recipe_elements, 1):
        name = _get_text(recipe_elem, 'NAME')
        if not name:
            result["warnings"].append(f"Recipe {i} missing NAME field")

        version = _get_text(recipe_elem, 'VERSION')
        if not version:
            result["warnings"].append(f"Recipe {i} ({name or 'unnamed'}) missing VERSION field")

    return result
