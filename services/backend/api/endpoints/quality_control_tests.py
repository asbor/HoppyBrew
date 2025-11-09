# api/endpoints/quality_control_tests.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session, joinedload
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Optional
from pathlib import Path
from datetime import datetime
import logging
import shutil
import uuid
from config import settings

# PDF generation libraries (will be added to requirements)
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post(
    "/batches/{batch_id}/qc-tests",
    response_model=schemas.QualityControlTest,
    tags=["quality-control"],
    summary="Create a QC test for a batch",
    response_description="The created QC test",
)
async def create_qc_test(
    batch_id: int,
    qc_test: schemas.QualityControlTestCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new quality control test for a batch.
    
    Records test results, BJCP scores, and tasting notes.
    """
    # Verify batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Validate BJCP score if provided
    if qc_test.score is not None:
        if not (0 <= qc_test.score <= 50):
            raise HTTPException(status_code=400, detail="BJCP score must be between 0 and 50")
    
    # Calculate total score from individual scores if provided
    if all([
        qc_test.aroma_score is not None,
        qc_test.appearance_score is not None,
        qc_test.flavor_score is not None,
        qc_test.mouthfeel_score is not None,
        qc_test.overall_impression_score is not None,
    ]):
        calculated_score = (
            qc_test.aroma_score +
            qc_test.appearance_score +
            qc_test.flavor_score +
            qc_test.mouthfeel_score +
            qc_test.overall_impression_score
        )
        if qc_test.score is None:
            qc_test.score = calculated_score
    
    # Create the QC test
    db_qc_test = models.QualityControlTest(
        batch_id=batch_id,
        test_date=qc_test.test_date,
        final_gravity=qc_test.final_gravity,
        abv_actual=qc_test.abv_actual,
        color=qc_test.color,
        clarity=qc_test.clarity,
        taste_notes=qc_test.taste_notes,
        aroma_notes=qc_test.aroma_notes,
        appearance_notes=qc_test.appearance_notes,
        flavor_notes=qc_test.flavor_notes,
        mouthfeel_notes=qc_test.mouthfeel_notes,
        score=qc_test.score,
        aroma_score=qc_test.aroma_score,
        appearance_score=qc_test.appearance_score,
        flavor_score=qc_test.flavor_score,
        mouthfeel_score=qc_test.mouthfeel_score,
        overall_impression_score=qc_test.overall_impression_score,
        tester_name=qc_test.tester_name,
        notes=qc_test.notes,
    )
    
    db.add(db_qc_test)
    db.commit()
    db.refresh(db_qc_test)
    
    logger.info(f"Created QC test {db_qc_test.id} for batch {batch_id}")
    return db_qc_test


@router.get(
    "/batches/{batch_id}/qc-tests",
    response_model=List[schemas.QualityControlTest],
    tags=["quality-control"],
    summary="Get all QC tests for a batch",
    response_description="List of QC tests ordered by test date (newest first)",
)
async def get_batch_qc_tests(
    batch_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve all quality control tests for a specific batch.
    
    Returns tests in reverse chronological order (newest first).
    """
    # Verify batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Get QC tests ordered by test date (newest first)
    qc_tests = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.batch_id == batch_id)
        .order_by(models.QualityControlTest.test_date.desc())
        .all()
    )
    
    return qc_tests


@router.get(
    "/qc-tests/{qc_test_id}",
    response_model=schemas.QualityControlTest,
    tags=["quality-control"],
    summary="Get a specific QC test",
    response_description="The QC test details",
)
async def get_qc_test(
    qc_test_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a specific quality control test by ID.
    """
    qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    
    if not qc_test:
        raise HTTPException(status_code=404, detail="QC test not found")
    
    return qc_test


@router.put(
    "/qc-tests/{qc_test_id}",
    response_model=schemas.QualityControlTest,
    tags=["quality-control"],
    summary="Update a QC test",
    response_description="The updated QC test",
)
async def update_qc_test(
    qc_test_id: int,
    qc_test_update: schemas.QualityControlTestUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing quality control test.
    """
    db_qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    
    if not db_qc_test:
        raise HTTPException(status_code=404, detail="QC test not found")
    
    # Update fields if provided
    update_data = qc_test_update.model_dump(exclude_unset=True)
    
    # Calculate total score if individual scores are updated
    if any(key in update_data for key in [
        "aroma_score", "appearance_score", "flavor_score", 
        "mouthfeel_score", "overall_impression_score"
    ]):
        # Get current or updated values
        aroma = update_data.get("aroma_score", db_qc_test.aroma_score)
        appearance = update_data.get("appearance_score", db_qc_test.appearance_score)
        flavor = update_data.get("flavor_score", db_qc_test.flavor_score)
        mouthfeel = update_data.get("mouthfeel_score", db_qc_test.mouthfeel_score)
        overall = update_data.get("overall_impression_score", db_qc_test.overall_impression_score)
        
        if all(v is not None for v in [aroma, appearance, flavor, mouthfeel, overall]):
            update_data["score"] = aroma + appearance + flavor + mouthfeel + overall
    
    for key, value in update_data.items():
        setattr(db_qc_test, key, value)
    
    db_qc_test.updated_at = datetime.now()
    db.commit()
    db.refresh(db_qc_test)
    
    logger.info(f"Updated QC test {qc_test_id}")
    return db_qc_test


@router.delete(
    "/qc-tests/{qc_test_id}",
    tags=["quality-control"],
    summary="Delete a QC test",
    response_description="Success message",
)
async def delete_qc_test(
    qc_test_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a quality control test.
    """
    db_qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    
    if not db_qc_test:
        raise HTTPException(status_code=404, detail="QC test not found")
    
    # Delete associated photo if exists
    if db_qc_test.photo_path:
        photo_file = Path(db_qc_test.photo_path)
        if photo_file.exists():
            photo_file.unlink()
    
    db.delete(db_qc_test)
    db.commit()
    
    logger.info(f"Deleted QC test {qc_test_id}")
    return {"message": "QC test deleted successfully"}


@router.post(
    "/qc-tests/{qc_test_id}/photo",
    response_model=schemas.QualityControlTest,
    tags=["quality-control"],
    summary="Upload photo for a QC test",
    response_description="The updated QC test with photo path",
)
async def upload_qc_test_photo(
    qc_test_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a photo for a quality control test (appearance documentation).
    
    Accepts image files (JPEG, PNG, WebP). Maximum size configured in settings.
    """
    # Verify QC test exists
    db_qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    
    if not db_qc_test:
        raise HTTPException(status_code=404, detail="QC test not found")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()  # Get position (size)
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"qc_test_{qc_test_id}_{uuid.uuid4()}{file_extension}"
    
    # Ensure upload directory exists
    upload_dir = Path(settings.UPLOAD_DIR) / "qc_photos"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = upload_dir / unique_filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")
    
    # Delete old photo if exists
    if db_qc_test.photo_path:
        old_photo = Path(db_qc_test.photo_path)
        if old_photo.exists():
            old_photo.unlink()
    
    # Update QC test with photo path
    db_qc_test.photo_path = str(file_path)
    db_qc_test.updated_at = datetime.now()
    db.commit()
    db.refresh(db_qc_test)
    
    logger.info(f"Uploaded photo for QC test {qc_test_id}")
    return db_qc_test


@router.post(
    "/qc-tests/{qc_test_id}/calculate-score",
    response_model=schemas.BJCPScoreCalculation,
    tags=["quality-control"],
    summary="Calculate BJCP score from individual components",
    response_description="The calculated total score and category",
)
async def calculate_bjcp_score(
    score_input: schemas.BJCPScoreCalculation,
):
    """
    Calculate total BJCP score from individual component scores.
    
    Returns the total score and the corresponding BJCP category.
    """
    return score_input


@router.get(
    "/qc-tests/templates/tasting-notes",
    tags=["quality-control"],
    summary="Get tasting note templates",
    response_description="Available tasting note templates",
)
async def get_tasting_note_templates():
    """
    Get available tasting note templates for structured tasting notes.
    """
    return schemas.TASTING_NOTE_TEMPLATES


@router.get(
    "/qc-tests/{qc_test_id}/export/pdf",
    tags=["quality-control"],
    summary="Export QC test as PDF",
    response_description="PDF file with tasting notes",
)
async def export_qc_test_pdf(
    qc_test_id: int,
    db: Session = Depends(get_db),
):
    """
    Export a quality control test as a PDF document.
    
    Creates a formatted PDF with BJCP score sheet and tasting notes.
    """
    if not REPORTLAB_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="PDF export not available. ReportLab library not installed."
        )
    
    # Get QC test with batch information
    qc_test = (
        db.query(models.QualityControlTest)
        .options(joinedload(models.QualityControlTest.batch))
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    
    if not qc_test:
        raise HTTPException(status_code=404, detail="QC test not found")
    
    # Generate PDF
    from fastapi.responses import FileResponse
    import tempfile
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_path = tmp_file.name
    
    try:
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(
            f"<b>Quality Control Test Report</b><br/>"
            f"Batch: {qc_test.batch.batch_name} (#{qc_test.batch.batch_number})",
            styles["Title"]
        )
        story.append(title)
        story.append(Spacer(1, 0.3 * inch))
        
        # Test Information
        test_info_data = [
            ["Test Date:", qc_test.test_date.strftime("%Y-%m-%d %H:%M")],
            ["Tester:", qc_test.tester_name or "N/A"],
            ["Final Gravity:", str(qc_test.final_gravity) if qc_test.final_gravity else "N/A"],
            ["ABV:", f"{qc_test.abv_actual}%" if qc_test.abv_actual else "N/A"],
            ["Color:", qc_test.color or "N/A"],
            ["Clarity:", qc_test.clarity or "N/A"],
        ]
        
        test_info_table = Table(test_info_data, colWidths=[2*inch, 4*inch])
        test_info_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(test_info_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # BJCP Scores
        if qc_test.score:
            score_category = "N/A"
            if qc_test.score >= 45:
                score_category = "Outstanding"
            elif qc_test.score >= 38:
                score_category = "Excellent"
            elif qc_test.score >= 30:
                score_category = "Very Good"
            elif qc_test.score >= 21:
                score_category = "Good"
            elif qc_test.score >= 14:
                score_category = "Fair"
            else:
                score_category = "Problematic"
            
            scores_title = Paragraph("<b>BJCP Scores</b>", styles["Heading2"])
            story.append(scores_title)
            
            scores_data = [
                ["Category", "Score", "Max"],
                ["Aroma", str(qc_test.aroma_score) if qc_test.aroma_score else "-", "12"],
                ["Appearance", str(qc_test.appearance_score) if qc_test.appearance_score else "-", "3"],
                ["Flavor", str(qc_test.flavor_score) if qc_test.flavor_score else "-", "20"],
                ["Mouthfeel", str(qc_test.mouthfeel_score) if qc_test.mouthfeel_score else "-", "5"],
                ["Overall", str(qc_test.overall_impression_score) if qc_test.overall_impression_score else "-", "10"],
                ["<b>TOTAL</b>", f"<b>{qc_test.score}</b>", "<b>50</b>"],
                ["<b>Category</b>", f"<b>{score_category}</b>", ""],
            ]
            
            scores_table = Table(scores_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            scores_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('BACKGROUND', (0, -2), (-1, -1), colors.lightblue),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ]))
            story.append(scores_table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Tasting Notes
        notes_title = Paragraph("<b>Tasting Notes</b>", styles["Heading2"])
        story.append(notes_title)
        
        if qc_test.aroma_notes:
            story.append(Paragraph("<b>Aroma:</b>", styles["Heading3"]))
            story.append(Paragraph(qc_test.aroma_notes, styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))
        
        if qc_test.appearance_notes:
            story.append(Paragraph("<b>Appearance:</b>", styles["Heading3"]))
            story.append(Paragraph(qc_test.appearance_notes, styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))
        
        if qc_test.flavor_notes:
            story.append(Paragraph("<b>Flavor:</b>", styles["Heading3"]))
            story.append(Paragraph(qc_test.flavor_notes, styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))
        
        if qc_test.mouthfeel_notes:
            story.append(Paragraph("<b>Mouthfeel:</b>", styles["Heading3"]))
            story.append(Paragraph(qc_test.mouthfeel_notes, styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))
        
        if qc_test.taste_notes:
            story.append(Paragraph("<b>Overall Impression:</b>", styles["Heading3"]))
            story.append(Paragraph(qc_test.taste_notes, styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))
        
        if qc_test.notes:
            story.append(Paragraph("<b>Additional Notes:</b>", styles["Heading3"]))
            story.append(Paragraph(qc_test.notes, styles["Normal"]))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF file
        filename = f"qc_test_{qc_test_id}_batch_{qc_test.batch_id}.pdf"
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename,
        )
    
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        # Clean up temporary file
        if Path(pdf_path).exists():
            Path(pdf_path).unlink()
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
