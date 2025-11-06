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


def export_references(xml_file, session=None):
    """
    Export references from the database to an XML file.
    
    Args:
        xml_file: Path to the output XML file
        session: Optional SQLAlchemy session (creates one if not provided)
    """
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True
    
    try:
        references = session.query(References).all()
        root = ET.Element("references")
        for reference in references:
            ref_element = ET.SubElement(root, "reference")
            ET.SubElement(ref_element, "id").text = str(reference.id)
            ET.SubElement(ref_element, "name").text = reference.name
            ET.SubElement(ref_element, "url").text = reference.url
            ET.SubElement(ref_element, "description").text = (
                reference.description or ""
            )
            ET.SubElement(ref_element, "category").text = reference.category or ""
            ET.SubElement(ref_element, "favicon_url").text = (
                reference.favicon_url or ""
            )
            ET.SubElement(ref_element, "created_at").text = (
                reference.created_at.isoformat()
            )
            ET.SubElement(ref_element, "updated_at").text = (
                reference.updated_at.isoformat() if reference.updated_at else ""
            )
        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
        print(f"Exported {len(references)} references to {xml_file}")
    finally:
        if close_session:
            session.close()


if __name__ == "__main__":
    export_references("references.xml")
