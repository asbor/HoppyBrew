import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directories to path to import models
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from Database.Models.references import References
from database import SessionLocal, SQLALCHEMY_DATABASE_URL


def import_references(xml_file, session=None):
    """
    Import references from an XML file to the database.
    
    Args:
        xml_file: Path to the input XML file
        session: Optional SQLAlchemy session (creates one if not provided)
    """
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        count = 0
        for ref_element in root.findall("reference"):
            reference = References(
                name=ref_element.find("name").text,
                url=ref_element.find("url").text,
                description=ref_element.find("description").text,
                category=ref_element.find("category").text,
                favicon_url=ref_element.find("favicon_url").text,
            )
            session.add(reference)
            count += 1
        session.commit()
        print(f"Imported {count} references from {xml_file}")
    finally:
        if close_session:
            session.close()


if __name__ == "__main__":
    import_references("references.xml")
