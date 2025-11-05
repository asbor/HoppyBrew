from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from database import SessionLocal  # type: ignore
from Database.Models.styles import Styles  # type: ignore
from logger_config import get_logger

logger = get_logger("SeedBeerStyles")

# Map BeerXML fields to SQLAlchemy model attributes.
STYLE_FIELD_MAP: Dict[str, str] = OrderedDict(
    {
        "NAME": "name",
        "VERSION": "version",
        "CATEGORY": "category",
        "CATEGORY_NUMBER": "category_number",
        "STYLE_LETTER": "style_letter",
        "STYLE_GUIDE": "style_guide",
        "TYPE": "type",
        "OG_MIN": "og_min",
        "OG_MAX": "og_max",
        "FG_MIN": "fg_min",
        "FG_MAX": "fg_max",
        "IBU_MIN": "ibu_min",
        "IBU_MAX": "ibu_max",
        "COLOR_MIN": "color_min",
        "COLOR_MAX": "color_max",
        "CARB_MIN": "carb_min",
        "CARB_MAX": "carb_max",
        "ABV_MAX": "abv_max",
        "ABV_MIN": "abv_min",
        "NOTES": "notes",
        "PROFILE": "profile",
        "INGREDIENTS": "ingredients",
        "EXAMPLES": "examples",
        "DISPLAY_OG_MIN": "display_og_min",
        "DISPLAY_OG_MAX": "display_og_max",
        "DISPLAY_FG_MIN": "display_fg_min",
        "DISPLAY_FG_MAX": "display_fg_max",
        "DISPLAY_COLOR_MIN": "display_color_min",
        "DISPLAY_COLOR_MAX": "display_color_max",
        "OG_RANGE": "og_range",
        "FG_RANGE": "fg_range",
        "IBU_RANGE": "ibu_range",
        "CARB_RANGE": "carb_range",
        "COLOR_RANGE": "color_range",
        "ABV_RANGE": "abv_range",
    }
)

INT_FIELDS = {"version", "category_number"}


def _clean_value(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    cleaned = " ".join(value.split()).replace("\u00a0", " ").strip()
    if cleaned.endswith(">") and cleaned.count(">") == 1:
        cleaned = cleaned.rstrip(">")
    return cleaned or None


def _convert_value(field_name: str, value: Optional[str]) -> Optional[object]:
    cleaned = _clean_value(value)
    if cleaned is None:
        return None

    if field_name in INT_FIELDS:
        try:
            return int(float(cleaned))
        except ValueError:
            logger.warning("Could not convert %s=%s to int", field_name, cleaned)
            return None
    return cleaned


def _load_styles_from_xml(xml_path: Path) -> List[Dict[str, object]]:
    logger.info("Loading beer styles from %s", xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    deduped: Dict[Tuple[Optional[str], Optional[str], Optional[str]], Dict[str, object]] = {}

    for recipe in root.findall("RECIPE"):
        style = recipe.find("STYLE")
        if style is None:
            continue

        record: Dict[str, object] = {}
        for xml_key, model_field in STYLE_FIELD_MAP.items():
            element = style.find(xml_key)
            text = element.text if element is not None else None
            record[model_field] = _convert_value(model_field, text)

        name = record.get("name")
        if not name:
            logger.debug("Skipping style without a name: %s", record)
            continue

        key = (
            record.get("name"),
            record.get("category"),
            record.get("style_letter"),
        )
        existing = deduped.get(key)
        if existing:
            # Keep existing values, but fill gaps from the new record.
            for column, value in record.items():
                if value and not existing.get(column):
                    existing[column] = value
        else:
            deduped[key] = record

    logger.info("Parsed %d unique beer styles", len(deduped))
    return list(deduped.values())


def _upsert_style(session: Session, data: Dict[str, object]) -> None:
    query = {
        "name": data.get("name"),
        "category": data.get("category"),
        "style_letter": data.get("style_letter"),
    }
    existing = session.query(Styles).filter_by(**query).one_or_none()

    if existing:
        for key, value in data.items():
            if value is not None:
                setattr(existing, key, value)
    else:
        session.add(Styles(**data))


def seed_beer_styles(xml_filename: str = "recipes.xml") -> int:
    data_dir = Path(__file__).resolve().parents[3] / "data"
    xml_path = data_dir / xml_filename
    if not xml_path.exists():
        raise FileNotFoundError(f"BeerXML file not found: {xml_path}")

    styles = _load_styles_from_xml(xml_path)
    if not styles:
        logger.warning("No styles found to seed.")
        return 0

    session: Session = SessionLocal()
    try:
        for style in styles:
            _upsert_style(session, style)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    logger.info("Seeded %d beer styles", len(styles))
    return len(styles)


def main() -> None:
    count = seed_beer_styles()
    logger.info("Inserted or updated %d beer styles", count)


if __name__ == "__main__":
    main()
