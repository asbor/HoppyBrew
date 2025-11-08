# api/endpoints/references.py

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - fallback when bs4 is unavailable
    BeautifulSoup = None
from urllib.parse import urlparse, urljoin
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List
import xml.etree.ElementTree as ET
from fastapi.responses import StreamingResponse
import io
from pydantic import BaseModel, ConfigDict

try:
    import requests
except ImportError:  # pragma: no cover - fallback when requests is unavailable
    requests = None

router = APIRouter()

# References Endpoints


def _element_text(element, tag, default=None):
    child = element.find(tag)
    if child is None or child.text is None:
        return default
    return child.text


class ReferenceImportResponse(BaseModel):
    message: str
    imported_records: int
    skipped_records: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "References imported successfully",
                "imported_records": 12,
                "skipped_records": 2,
            }
        }
    )


@router.post(
    "/references/import",
    response_model=ReferenceImportResponse,
    summary="Import references from BeerXML",
    response_description="Outcome of the import operation summarising processed records.",
)
async def import_references(
    db: Session = Depends(get_db), file: UploadFile = File(...)
):
    contents = await file.read()
    try:
        tree = ET.ElementTree(ET.fromstring(contents))
    except ET.ParseError as parse_error:
        raise HTTPException(
            status_code=400,
            detail=f"Provided file is not valid XML: {parse_error}",
        ) from parse_error
    root = tree.getroot()
    imported_count = 0
    skipped_count = 0
    for ref_element in root.findall("reference"):
        name = _element_text(ref_element, "name")
        url = _element_text(ref_element, "url")
        if not name or not url:
            # Skip malformed records rather than failing the whole import
            skipped_count += 1
            continue
        description = _element_text(ref_element, "description", "")
        category = _element_text(ref_element, "category", "")
        favicon_url = fetch_favicon(url)
        reference = models.References(
            name=name,
            url=url,
            description=description,
            category=category,
            favicon_url=favicon_url,
        )
        db.add(reference)
        imported_count += 1
    db.commit()
    return ReferenceImportResponse(
        message="References imported successfully",
        imported_records=imported_count,
        skipped_records=skipped_count,
    )


@router.get("/references/export")
async def export_references(db: Session = Depends(get_db)):
    references = db.query(models.References).all()
    root = ET.Element("references")
    for reference in references:
        ref_element = ET.SubElement(root, "reference")
        ET.SubElement(ref_element, "id").text = str(reference.id)
        ET.SubElement(ref_element, "name").text = reference.name
        ET.SubElement(ref_element, "url").text = reference.url
        ET.SubElement(ref_element, "description").text = reference.description or ""
        ET.SubElement(ref_element, "category").text = reference.category or ""
        ET.SubElement(ref_element, "favicon_url").text = reference.favicon_url or ""
        ET.SubElement(ref_element, "created_at").text = reference.created_at.isoformat()
        ET.SubElement(ref_element, "updated_at").text = (
            reference.updated_at.isoformat() if reference.updated_at else ""
        )
    tree = ET.ElementTree(root)
    xml_io = io.BytesIO()
    tree.write(xml_io, encoding="utf-8", xml_declaration=True)
    xml_io.seek(0)
    return StreamingResponse(
        xml_io,
        media_type="application/xml",
        headers={"Content-Disposition": "attachment; filename=references.xml"},
    )


@router.get("/references", response_model=List[schemas.Reference])
async def get_all_references(db: Session = Depends(get_db)):
    references = db.query(models.References).all()
    return references


@router.get("/references/{reference_id}", response_model=schemas.Reference)
async def get_reference(reference_id: int, db: Session = Depends(get_db)):
    reference = (
        db.query(models.References).filter(models.References.id == reference_id).first()
    )
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    return reference


@router.post("/references", response_model=schemas.Reference)
async def create_reference(
    reference: schemas.ReferenceCreate, db: Session = Depends(get_db)
):
    favicon_url = fetch_favicon(reference.url)
    reference_data = reference.model_dump()
    reference_data["favicon_url"] = favicon_url
    db_reference = models.References(**reference_data)
    db.add(db_reference)
    db.commit()
    db.refresh(db_reference)
    return db_reference


@router.delete("/references/{reference_id}", response_model=schemas.Reference)
async def delete_reference(reference_id: int, db: Session = Depends(get_db)):
    reference = (
        db.query(models.References).filter(models.References.id == reference_id).first()
    )
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    db.delete(reference)
    db.commit()
    return reference


@router.put("/references/{reference_id}", response_model=schemas.Reference)
async def update_reference(
    reference_id: int,
    reference: schemas.ReferenceUpdate,
    db: Session = Depends(get_db),
):
    db_reference = (
        db.query(models.References).filter(models.References.id == reference_id).first()
    )
    if not db_reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    for key, value in reference.model_dump().items():
        setattr(db_reference, key, value)
    db.commit()
    db.refresh(db_reference)
    return db_reference


# Helper function to fetch favicon URL


def fetch_favicon(url: str) -> str:
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    google_favicon_url = (
        f"http://www.google.com/s2/favicons?domain={parsed_url.netloc}"
        if parsed_url.netloc
        else ""
    )
    if not parsed_url.scheme or not parsed_url.netloc or requests is None:
        return google_favicon_url

    # Try common paths

    common_paths = ["/favicon.ico", "/favicon.png", "/favicon.svg"]
    for path in common_paths:
        favicon_url = urljoin(base_url, path)
        try:
            response = requests.head(favicon_url, timeout=2)
            if response.status_code == 200:
                return favicon_url
        except Exception:
            continue
    # Try parsing the HTML for <link> tags

    if BeautifulSoup is None:
        return google_favicon_url

    try:
        response = requests.get(base_url, timeout=2)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        link_tags = soup.find_all(
            "link",
            rel=[
                "icon",
                "shortcut icon",
                "apple-touch-icon",
                "apple-touch-icon-precomposed",
            ],
        )
        for link in link_tags:
            href = link.get("href")
            if href:
                favicon_url = urljoin(base_url, href)
                try:
                    response = requests.head(favicon_url, timeout=2)
                    if response.status_code == 200:
                        return favicon_url
                except Exception:
                    continue
    except Exception as e:
        print(f"Error parsing HTML for {url}: {e}")
    # Fallback to Google's favicon service

    return google_favicon_url
