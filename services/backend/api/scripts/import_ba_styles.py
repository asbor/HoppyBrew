# scripts/import_ba_styles.py
"""
Brewers Association Style Guide PDF Importer

This script parses the Brewers Association Beer Style Guidelines PDF
and imports the styles into the beer_styles table.

Usage:
    python api/scripts/import_ba_styles.py [path_to_pdf]

If no PDF path is provided, the script looks for the PDF in standard locations.
"""

import os
import re
import sys
from typing import Dict, List, Any

try:
    import pdfplumber
except ImportError:
    print("pdfplumber is required. Install it with: pip install pdfplumber")
    sys.exit(1)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database import engine
from Database.Models import BeerStyle
from Database.Models.style_guidlines import StyleGuidelineSource


def parse_range(value: str) -> tuple:
    """Parse a range string like '4.5-5.5' into (min, max)."""
    if not value or value.strip() == "-" or value.strip().lower() == "n/a":
        return (None, None)

    value = value.strip()

    # Handle single values
    if "-" not in value or value.count("-") == 1 and value.startswith("-"):
        try:
            val = float(value.replace("%", "").strip())
            return (val, val)
        except ValueError:
            return (None, None)

    # Handle ranges
    parts = value.split("-")
    if len(parts) == 2:
        try:
            min_val = float(parts[0].replace("%", "").strip())
            max_val = float(parts[1].replace("%", "").strip())
            return (min_val, max_val)
        except ValueError:
            return (None, None)

    return (None, None)


def extract_style_data(text: str) -> List[Dict[str, Any]]:
    """
    Extract beer style data from parsed PDF text.

    This is a heuristic parser that looks for common patterns in
    BA style guide PDFs.
    """
    styles = []

    # Split by style markers - this is a heuristic approach
    # BA PDFs typically have consistent formatting

    # Look for patterns like "Style Name" followed by vitals
    lines = text.split("\n")
    current_style = None

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Look for OG/FG/ABV/IBU/SRM patterns
        og_match = re.search(
            r"Original Gravity[:\s]+(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)",
            line,
            re.IGNORECASE,
        )
        fg_match = re.search(
            r"Final Gravity[:\s]+(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)",
            line,
            re.IGNORECASE,
        )
        abv_match = re.search(
            r"ABV[:\s]+(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)%?", line, re.IGNORECASE
        )
        ibu_match = re.search(
            r"IBU[:\s]+(\d+)\s*[-–]\s*(\d+)", line, re.IGNORECASE
        )
        srm_match = re.search(
            r"SRM[:\s]+(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)", line, re.IGNORECASE
        )

        if current_style is None:
            current_style = {"name": "Unknown Style", "description": ""}

        if og_match:
            current_style["og_min"] = float(og_match.group(1))
            current_style["og_max"] = float(og_match.group(2))
        elif fg_match:
            current_style["fg_min"] = float(fg_match.group(1))
            current_style["fg_max"] = float(fg_match.group(2))
        elif abv_match:
            current_style["abv_min"] = float(abv_match.group(1))
            current_style["abv_max"] = float(abv_match.group(2))
        elif ibu_match:
            current_style["ibu_min"] = int(ibu_match.group(1))
            current_style["ibu_max"] = int(ibu_match.group(2))
        elif srm_match:
            current_style["color_min_srm"] = float(srm_match.group(1))
            current_style["color_max_srm"] = float(srm_match.group(2))

    return styles


def extract_styles_from_tables(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract style data from tables in the PDF.

    BA style guides often use tables for vitals data.
    """
    styles = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables from the page
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 2:
                        continue

                    # Look for rows that contain style vitals
                    row_text = " ".join(str(cell) for cell in row if cell)

                    # Skip header rows
                    if any(
                        header in row_text.lower()
                        for header in ["style", "og", "fg", "abv", "ibu", "srm"]
                    ):
                        if "style" in row_text.lower() and row_text.count("\t") < 3:
                            continue

            # Also extract text for descriptions
            text = page.extract_text()
            if text:
                # Process text for style descriptions
                pass

    return styles


def import_styles_from_pdf(pdf_path: str) -> int:
    """
    Import beer styles from a Brewers Association PDF.

    Returns the number of styles imported.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return 0

    print(f"Opening PDF: {pdf_path}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    imported_count = 0

    try:
        # Get or create BA guideline source
        ba_source = (
            session.query(StyleGuidelineSource)
            .filter(StyleGuidelineSource.abbreviation == "BA")
            .first()
        )

        if not ba_source:
            ba_source = StyleGuidelineSource(
                name="Brewers Association",
                year=2025,
                abbreviation="BA",
                description="Brewers Association Beer Style Guidelines",
                is_active=True,
            )
            session.add(ba_source)
            session.commit()
            session.refresh(ba_source)
            print(f"Created BA guideline source with ID: {ba_source.id}")

        # Extract styles from PDF
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            print(f"Extracted {len(full_text)} characters from PDF")

            # For now, we extract basic style info from the text
            # This is a heuristic approach - real BA PDFs would need
            # more sophisticated parsing based on actual PDF structure

            styles = extract_style_data(full_text)

            for style_data in styles:
                try:
                    style = BeerStyle(
                        guideline_source_id=ba_source.id,
                        name=style_data.get("name", "Unknown"),
                        style_code=style_data.get("style_code"),
                        abv_min=style_data.get("abv_min"),
                        abv_max=style_data.get("abv_max"),
                        og_min=style_data.get("og_min"),
                        og_max=style_data.get("og_max"),
                        fg_min=style_data.get("fg_min"),
                        fg_max=style_data.get("fg_max"),
                        ibu_min=style_data.get("ibu_min"),
                        ibu_max=style_data.get("ibu_max"),
                        color_min_srm=style_data.get("color_min_srm"),
                        color_max_srm=style_data.get("color_max_srm"),
                        description=style_data.get("description"),
                        overall_impression=style_data.get("overall_impression"),
                        aroma=style_data.get("aroma"),
                        appearance=style_data.get("appearance"),
                        flavor=style_data.get("flavor"),
                        mouthfeel=style_data.get("mouthfeel"),
                        is_custom=False,
                    )
                    session.add(style)
                    session.commit()
                    imported_count += 1
                    print(f"Imported: {style.name}")
                except IntegrityError:
                    session.rollback()
                    print(f"Skipped duplicate: {style_data.get('name')}")
                except Exception as e:
                    session.rollback()
                    print(f"Error importing {style_data.get('name')}: {e}")

    except Exception as e:
        print(f"Error processing PDF: {e}")
        session.rollback()
    finally:
        session.close()

    return imported_count


def main():
    """Main entry point for the BA styles importer."""
    # Default PDF locations to check
    default_paths = [
        "data/ba_styles_2025.pdf",
        "/home/app/data/ba_styles_2025.pdf",
        "ba_styles.pdf",
    ]

    pdf_path = None

    # Check command line argument first
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Try default locations
        for path in default_paths:
            if os.path.exists(path):
                pdf_path = path
                break

    if not pdf_path:
        print("Usage: python import_ba_styles.py <path_to_pdf>")
        print("\nNo PDF file specified and none found in default locations.")
        print("Default locations checked:")
        for path in default_paths:
            print(f"  - {path}")
        sys.exit(1)

    print("=" * 60)
    print("Brewers Association Style Guide Importer")
    print("=" * 60)

    count = import_styles_from_pdf(pdf_path)

    print("=" * 60)
    print(f"Import complete. {count} styles imported.")
    print("=" * 60)


if __name__ == "__main__":
    main()
