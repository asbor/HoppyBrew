"""
BeerXML Exporter Module

This module provides functionality to export brewing recipes to BeerXML format.
"""

import xml.etree.ElementTree as ET
from typing import List, Optional, Any
from xml.dom import minidom
import Database.Models as models


class BeerXMLExportError(Exception):
    """Custom exception for BeerXML export errors"""
    pass


def _add_element(parent: ET.Element, tag: str, text: Any, optional: bool = True) -> Optional[ET.Element]:
    """
    Add a child element with text content to a parent element.
    
    Args:
        parent: Parent XML element
        tag: Tag name for the new element
        text: Text content (will be converted to string)
        optional: If True, skip if text is None or empty
        
    Returns:
        The created element or None if skipped
    """
    if optional and (text is None or text == ''):
        return None
    
    elem = ET.SubElement(parent, tag)
    if text is not None:
        elem.text = str(text)
    return elem


def _export_hop(parent: ET.Element, hop: models.RecipeHop) -> None:
    """Export a hop to BeerXML format"""
    hop_elem = ET.SubElement(parent, 'HOP')
    
    _add_element(hop_elem, 'NAME', hop.name, optional=False)
    _add_element(hop_elem, 'VERSION', hop.version or 1)
    _add_element(hop_elem, 'ALPHA', hop.alpha)
    _add_element(hop_elem, 'AMOUNT', hop.amount)
    _add_element(hop_elem, 'USE', hop.use)
    _add_element(hop_elem, 'TIME', hop.time)
    _add_element(hop_elem, 'NOTES', hop.notes)
    _add_element(hop_elem, 'TYPE', hop.type)
    _add_element(hop_elem, 'FORM', hop.form)
    _add_element(hop_elem, 'BETA', hop.beta)
    _add_element(hop_elem, 'HSI', hop.hsi)
    _add_element(hop_elem, 'ORIGIN', hop.origin)
    _add_element(hop_elem, 'SUBSTITUTES', hop.substitutes)
    _add_element(hop_elem, 'HUMULENE', hop.humulene)
    _add_element(hop_elem, 'CARYOPHYLLENE', hop.caryophyllene)
    _add_element(hop_elem, 'COHUMULONE', hop.cohumulone)
    _add_element(hop_elem, 'MYRCENE', hop.myrcene)
    _add_element(hop_elem, 'DISPLAY_AMOUNT', hop.display_amount)
    _add_element(hop_elem, 'INVENTORY', hop.inventory)
    _add_element(hop_elem, 'DISPLAY_TIME', hop.display_time)


def _export_fermentable(parent: ET.Element, fermentable: models.RecipeFermentable) -> None:
    """Export a fermentable to BeerXML format"""
    ferm_elem = ET.SubElement(parent, 'FERMENTABLE')
    
    _add_element(ferm_elem, 'NAME', fermentable.name, optional=False)
    _add_element(ferm_elem, 'VERSION', fermentable.version or 1)
    _add_element(ferm_elem, 'TYPE', fermentable.type)
    _add_element(ferm_elem, 'AMOUNT', fermentable.amount)
    _add_element(ferm_elem, 'YIELD', fermentable.yield_)
    _add_element(ferm_elem, 'COLOR', fermentable.color)
    
    if fermentable.add_after_boil is not None:
        _add_element(ferm_elem, 'ADD_AFTER_BOIL', 'TRUE' if fermentable.add_after_boil else 'FALSE')
    
    _add_element(ferm_elem, 'ORIGIN', fermentable.origin)
    _add_element(ferm_elem, 'SUPPLIER', fermentable.supplier)
    _add_element(ferm_elem, 'NOTES', fermentable.notes)
    _add_element(ferm_elem, 'COARSE_FINE_DIFF', fermentable.coarse_fine_diff)
    _add_element(ferm_elem, 'MOISTURE', fermentable.moisture)
    _add_element(ferm_elem, 'DIASTATIC_POWER', fermentable.diastatic_power)
    _add_element(ferm_elem, 'PROTEIN', fermentable.protein)
    _add_element(ferm_elem, 'MAX_IN_BATCH', fermentable.max_in_batch)
    
    if fermentable.recommend_mash is not None:
        _add_element(ferm_elem, 'RECOMMEND_MASH', 'TRUE' if fermentable.recommend_mash else 'FALSE')
    
    _add_element(ferm_elem, 'IBU_GAL_PER_LB', fermentable.ibu_gal_per_lb)
    _add_element(ferm_elem, 'DISPLAY_AMOUNT', fermentable.display_amount)
    _add_element(ferm_elem, 'POTENTIAL', fermentable.potential)
    _add_element(ferm_elem, 'INVENTORY', fermentable.inventory)
    _add_element(ferm_elem, 'DISPLAY_COLOR', fermentable.display_color)


def _export_yeast(parent: ET.Element, yeast: models.RecipeYeast) -> None:
    """Export a yeast to BeerXML format"""
    yeast_elem = ET.SubElement(parent, 'YEAST')
    
    _add_element(yeast_elem, 'NAME', yeast.name, optional=False)
    _add_element(yeast_elem, 'VERSION', yeast.version or 1)
    _add_element(yeast_elem, 'TYPE', yeast.type)
    _add_element(yeast_elem, 'FORM', yeast.form)
    _add_element(yeast_elem, 'AMOUNT', yeast.amount)
    
    if yeast.amount_is_weight is not None:
        _add_element(yeast_elem, 'AMOUNT_IS_WEIGHT', 'TRUE' if yeast.amount_is_weight else 'FALSE')
    
    _add_element(yeast_elem, 'LABORATORY', yeast.laboratory)
    _add_element(yeast_elem, 'PRODUCT_ID', yeast.product_id)
    _add_element(yeast_elem, 'MIN_TEMPERATURE', yeast.min_temperature)
    _add_element(yeast_elem, 'MAX_TEMPERATURE', yeast.max_temperature)
    _add_element(yeast_elem, 'FLOCCULATION', yeast.flocculation)
    _add_element(yeast_elem, 'ATTENUATION', yeast.attenuation)
    _add_element(yeast_elem, 'NOTES', yeast.notes)
    _add_element(yeast_elem, 'BEST_FOR', yeast.best_for)
    _add_element(yeast_elem, 'MAX_REUSE', yeast.max_reuse)
    _add_element(yeast_elem, 'TIMES_CULTURED', yeast.times_cultured)
    
    if yeast.add_to_secondary is not None:
        _add_element(yeast_elem, 'ADD_TO_SECONDARY', 'TRUE' if yeast.add_to_secondary else 'FALSE')
    
    _add_element(yeast_elem, 'DISPLAY_AMOUNT', yeast.display_amount)
    _add_element(yeast_elem, 'DISP_MIN_TEMP', yeast.disp_min_temp)
    _add_element(yeast_elem, 'DISP_MAX_TEMP', yeast.disp_max_temp)
    _add_element(yeast_elem, 'INVENTORY', yeast.inventory)
    _add_element(yeast_elem, 'CULTURE_DATE', yeast.culture_date)


def _export_misc(parent: ET.Element, misc: models.RecipeMisc) -> None:
    """Export a miscellaneous ingredient to BeerXML format"""
    misc_elem = ET.SubElement(parent, 'MISC')
    
    _add_element(misc_elem, 'NAME', misc.name, optional=False)
    _add_element(misc_elem, 'VERSION', misc.version or 1)
    _add_element(misc_elem, 'TYPE', misc.type)
    _add_element(misc_elem, 'USE', misc.use)
    _add_element(misc_elem, 'AMOUNT', misc.amount)
    _add_element(misc_elem, 'TIME', misc.time)
    
    if misc.amount_is_weight is not None:
        _add_element(misc_elem, 'AMOUNT_IS_WEIGHT', 'TRUE' if misc.amount_is_weight else 'FALSE')
    
    _add_element(misc_elem, 'USE_FOR', misc.use_for)
    _add_element(misc_elem, 'NOTES', misc.notes)
    _add_element(misc_elem, 'DISPLAY_AMOUNT', misc.display_amount)
    _add_element(misc_elem, 'INVENTORY', misc.inventory)
    _add_element(misc_elem, 'DISPLAY_TIME', misc.display_time)
    _add_element(misc_elem, 'BATCH_SIZE', misc.batch_size)


def _export_recipe(parent: ET.Element, recipe: models.Recipes) -> None:
    """Export a single recipe to BeerXML format"""
    recipe_elem = ET.SubElement(parent, 'RECIPE')
    
    # Required fields
    _add_element(recipe_elem, 'NAME', recipe.name or 'Untitled Recipe', optional=False)
    _add_element(recipe_elem, 'VERSION', recipe.version or 1)
    
    # Optional recipe fields
    _add_element(recipe_elem, 'TYPE', recipe.type)
    _add_element(recipe_elem, 'BREWER', recipe.brewer)
    _add_element(recipe_elem, 'ASST_BREWER', recipe.asst_brewer)
    _add_element(recipe_elem, 'BATCH_SIZE', recipe.batch_size)
    _add_element(recipe_elem, 'BOIL_SIZE', recipe.boil_size)
    _add_element(recipe_elem, 'BOIL_TIME', recipe.boil_time)
    _add_element(recipe_elem, 'EFFICIENCY', recipe.efficiency)
    
    # Hops
    if recipe.hops:
        hops_elem = ET.SubElement(recipe_elem, 'HOPS')
        for hop in recipe.hops:
            _export_hop(hops_elem, hop)
    
    # Fermentables
    if recipe.fermentables:
        fermentables_elem = ET.SubElement(recipe_elem, 'FERMENTABLES')
        for fermentable in recipe.fermentables:
            _export_fermentable(fermentables_elem, fermentable)
    
    # Yeasts
    if recipe.yeasts:
        yeasts_elem = ET.SubElement(recipe_elem, 'YEASTS')
        for yeast in recipe.yeasts:
            _export_yeast(yeasts_elem, yeast)
    
    # Miscs
    if recipe.miscs:
        miscs_elem = ET.SubElement(recipe_elem, 'MISCS')
        for misc in recipe.miscs:
            _export_misc(miscs_elem, misc)
    
    # Additional recipe fields
    _add_element(recipe_elem, 'NOTES', recipe.notes)
    _add_element(recipe_elem, 'TASTE_NOTES', recipe.taste_notes)
    _add_element(recipe_elem, 'TASTE_RATING', recipe.taste_rating)
    _add_element(recipe_elem, 'OG', recipe.og)
    _add_element(recipe_elem, 'FG', recipe.fg)
    _add_element(recipe_elem, 'FERMENTATION_STAGES', recipe.fermentation_stages)
    _add_element(recipe_elem, 'PRIMARY_AGE', recipe.primary_age)
    _add_element(recipe_elem, 'PRIMARY_TEMP', recipe.primary_temp)
    _add_element(recipe_elem, 'SECONDARY_AGE', recipe.secondary_age)
    _add_element(recipe_elem, 'SECONDARY_TEMP', recipe.secondary_temp)
    _add_element(recipe_elem, 'TERTIARY_AGE', recipe.tertiary_age)
    _add_element(recipe_elem, 'TERTIARY_TEMP', recipe.tertiary_temp)
    _add_element(recipe_elem, 'AGE', recipe.age)
    _add_element(recipe_elem, 'AGE_TEMP', recipe.age_temp)
    _add_element(recipe_elem, 'CARBONATION_USED', recipe.carbonation_used)
    _add_element(recipe_elem, 'EST_OG', recipe.est_og)
    _add_element(recipe_elem, 'EST_FG', recipe.est_fg)
    _add_element(recipe_elem, 'EST_COLOR', recipe.est_color)
    _add_element(recipe_elem, 'IBU', recipe.ibu)
    _add_element(recipe_elem, 'IBU_METHOD', recipe.ibu_method)
    _add_element(recipe_elem, 'EST_ABV', recipe.est_abv)
    _add_element(recipe_elem, 'ABV', recipe.abv)
    _add_element(recipe_elem, 'ACTUAL_EFFICIENCY', recipe.actual_efficiency)
    _add_element(recipe_elem, 'CALORIES', recipe.calories)
    _add_element(recipe_elem, 'DISPLAY_BATCH_SIZE', recipe.display_batch_size)
    _add_element(recipe_elem, 'DISPLAY_BOIL_SIZE', recipe.display_boil_size)
    _add_element(recipe_elem, 'DISPLAY_OG', recipe.display_og)
    _add_element(recipe_elem, 'DISPLAY_FG', recipe.display_fg)
    _add_element(recipe_elem, 'DISPLAY_PRIMARY_TEMP', recipe.display_primary_temp)
    _add_element(recipe_elem, 'DISPLAY_SECONDARY_TEMP', recipe.display_secondary_temp)
    _add_element(recipe_elem, 'DISPLAY_TERTIARY_TEMP', recipe.display_tertiary_temp)
    _add_element(recipe_elem, 'DISPLAY_AGE_TEMP', recipe.display_age_temp)


def export_to_beerxml(recipes: List[models.Recipes], pretty_print: bool = True) -> str:
    """
    Export one or more recipes to BeerXML format.
    
    Args:
        recipes: List of Recipe model objects to export
        pretty_print: If True, format XML with indentation
        
    Returns:
        BeerXML formatted string
        
    Raises:
        BeerXMLExportError: If export fails
    """
    if not recipes:
        raise BeerXMLExportError("No recipes provided for export")
    
    # Create root element
    root = ET.Element('RECIPES')
    
    # Export each recipe
    for recipe in recipes:
        try:
            _export_recipe(root, recipe)
        except Exception as e:
            raise BeerXMLExportError(f"Failed to export recipe '{recipe.name}': {str(e)}")
    
    # Convert to string
    if pretty_print:
        # Use minidom for pretty printing
        xml_str = ET.tostring(root, encoding='utf-8')
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
    else:
        # Return compact XML
        tree = ET.ElementTree(root)
        import io
        output = io.BytesIO()
        tree.write(output, encoding='utf-8', xml_declaration=True)
        return output.getvalue().decode('utf-8')


def export_recipe_to_beerxml(recipe: models.Recipes, pretty_print: bool = True) -> str:
    """
    Export a single recipe to BeerXML format.
    
    Args:
        recipe: Recipe model object to export
        pretty_print: If True, format XML with indentation
        
    Returns:
        BeerXML formatted string
    """
    return export_to_beerxml([recipe], pretty_print=pretty_print)
