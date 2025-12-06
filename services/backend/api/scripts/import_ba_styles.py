"""
Import Brewers Association Beer Style Guidelines (PDF) into the beer_styles tables.

This script downloads the latest BA guideline PDF, extracts style names and vitals,
and upserts them into:
  - style_guideline_sources (name: "BA 2025", abbreviation: "BA", year: 2025)
  - beer_styles (style_code left NULL, category left NULL for now)

Parsing is heuristic: we look for lines containing "-Style" to mark a style block,
and capture OG/FG/ABV/IBU/Color ranges from the text below it.
"""

import io
import re
import requests
import pdfplumber
from sqlalchemy.orm import Session

from database import SessionLocal
from Database.Models.beer_styles import BeerStyle
from Database.Models.style_guidlines import StyleGuidelineSource
from logger_config import get_logger

LOG = get_logger("import_ba_styles")

PDF_URL = "https://cdn.brewersassociation.org/wp-content/uploads/2025/06/20143326/2025_BA_Beer_Style_Guidelines.pdf"


def _ensure_guideline_source(db: Session) -> StyleGuidelineSource:
    src = (
        db.query(StyleGuidelineSource)
        .filter(StyleGuidelineSource.name == "BA 2025")
        .one_or_none()
    )
    if not src:
        src = StyleGuidelineSource(
            name="BA 2025",
            abbreviation="BA",
            year=2025,
            description="Brewers Association Beer Style Guidelines (2025)",
            is_active=True,
        )
        db.add(src)
        db.commit()
        db.refresh(src)
    return src


def _parse_range(pattern: str, text: str):
    m = re.search(pattern, text)
    if not m:
        return None, None
    try:
        return float(m.group(1)), float(m.group(2))
    except ValueError:
        return None, None


def _parse_style_block(name: str, block_text: str):
    og_min, og_max = _parse_range(r"Original Gravity.*?([0-9.]+)-([0-9.]+)", block_text)
    fg_min, fg_max = _parse_range(
        r"(Final Gravity|Apparent Extract/Final Gravity).*?([0-9.]+)-([0-9.]+)", block_text
    )
    abv_min, abv_max = _parse_range(
        r"Alcohol by Weight.*?([0-9.]+)%.*?([0-9.]+)%", block_text
    )
    ibu_min, ibu_max = _parse_range(r"Hop Bitterness.*?([0-9.]+)-([0-9.]+)", block_text)
    color_min, color_max = _parse_range(
        r"Color SRM.*?([0-9.]+)-([0-9.]+)", block_text
    )

    return {
        "name": name.strip(),
        "og_min": og_min,
        "og_max": og_max,
        "fg_min": fg_min,
        "fg_max": fg_max,
        "abv_min": abv_min,
        "abv_max": abv_max,
        "ibu_min": ibu_min if ibu_min is None else int(ibu_min),
        "ibu_max": ibu_max if ibu_max is None else int(ibu_max),
        "color_min_srm": color_min,
        "color_max_srm": color_max,
        "description": block_text.strip()[:5000],
    }


def _extract_styles(pdf_bytes: bytes):
    styles = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        current_name = None
        current_lines = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                line = line.strip()
                # Style header heuristic
                if "-Style" in line and len(line.split()) <= 6:
                    if current_name and current_lines:
                        styles.append((current_name, "\n".join(current_lines)))
                    current_name = line
                    current_lines = []
                elif current_name:
                    current_lines.append(line)
        if current_name and current_lines:
            styles.append((current_name, "\n".join(current_lines)))
    return styles


def import_ba_styles():
    LOG.info("Downloading BA guidelines PDF")
    resp = requests.get(PDF_URL, verify=False, timeout=60)
    resp.raise_for_status()
    styles_raw = _extract_styles(resp.content)
    LOG.info("Extracted %d style blocks (heuristic)", len(styles_raw))

    db = SessionLocal()
    try:
        source = _ensure_guideline_source(db)
        imported = 0
        for name, block in styles_raw:
            data = _parse_style_block(name, block)
            if not data["name"]:
                continue
            existing = (
                db.query(BeerStyle)
                .filter(
                    BeerStyle.guideline_source_id == source.id,
                    BeerStyle.name == data["name"],
                )
                .one_or_none()
            )
            if existing:
                for k, v in data.items():
                    setattr(existing, k, v)
                obj = existing
            else:
                obj = BeerStyle(**data, guideline_source_id=source.id, is_custom=False)
                db.add(obj)
            imported += 1
        db.commit()
        LOG.info("Imported/updated %d BA styles", imported)
    finally:
        db.close()


if __name__ == "__main__":
    import_ba_styles()
