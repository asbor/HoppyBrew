# api/endpoints/quality_control_tests.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Optional
import logging
from datetime import datetime
import os
import shutil
from pathlib import Path

# For PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload directory
UPLOAD_DIR = Path("/app/data/qc_photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def calculate_bjcp_score(score_input: schemas.BJCPScoreInput) -> schemas.BJCPScoreResult:
    """
    Calculate total BJCP score and provide rating.
    BJCP Score Scale (0-50):
    - Outstanding (45-50)
    - Excellent (38-44)
    - Very Good (30-37)
    - Good (21-29)
    - Fair (14-20)
    - Problematic (6-13)
    - Flawed (0-5)
    """
    total = (
        score_input.aroma
        + score_input.appearance
        + score_input.flavor
        + score_input.mouthfeel
        + score_input.overall_impression
    )
    
    # Determine rating
    if total >= 45:
        rating = "Outstanding"
    elif total >= 38:
        rating = "Excellent"
    elif total >= 30:
        rating = "Very Good"
    elif total >= 21:
        rating = "Good"
    elif total >= 14:
        rating = "Fair"
    elif total >= 6:
        rating = "Problematic"
    else:
        rating = "Flawed"
    
    return schemas.BJCPScoreResult(
        total_score=total,
        aroma=score_input.aroma,
        appearance=score_input.appearance,
        flavor=score_input.flavor,
        mouthfeel=score_input.mouthfeel,
        overall_impression=score_input.overall_impression,
        rating=rating,
    )


@router.post("/bjcp-score", response_model=schemas.BJCPScoreResult)
async def calculate_bjcp(score_input: schemas.BJCPScoreInput):
    """Calculate BJCP score from individual component scores"""
    try:
        return calculate_bjcp_score(score_input)
    except Exception as e:
        logger.error(f"Error calculating BJCP score: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quality-control-tests", response_model=schemas.QualityControlTest)
async def create_quality_control_test(
    qc_test: schemas.QualityControlTestCreate,
    db: Session = Depends(get_db),
):
    """Create a new quality control test for a batch"""
    try:
        # Check if batch exists
        batch = db.query(models.Batches).filter(models.Batches.id == qc_test.batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        # Create QC test
        db_qc_test = models.QualityControlTest(**qc_test.model_dump())
        db.add(db_qc_test)
        db.commit()
        db.refresh(db_qc_test)
        
        logger.info(f"Created QC test {db_qc_test.id} for batch {qc_test.batch_id}")
        return db_qc_test
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating QC test: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quality-control-tests/{qc_test_id}", response_model=schemas.QualityControlTest)
async def get_quality_control_test(qc_test_id: int, db: Session = Depends(get_db)):
    """Get a specific quality control test by ID"""
    qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    if not qc_test:
        raise HTTPException(status_code=404, detail="Quality control test not found")
    return qc_test


@router.get("/batches/{batch_id}/quality-control-tests", response_model=List[schemas.QualityControlTest])
async def get_batch_quality_control_tests(batch_id: int, db: Session = Depends(get_db)):
    """Get all quality control tests for a specific batch"""
    # Check if batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    qc_tests = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.batch_id == batch_id)
        .order_by(models.QualityControlTest.test_date.desc())
        .all()
    )
    return qc_tests


@router.put("/quality-control-tests/{qc_test_id}", response_model=schemas.QualityControlTest)
async def update_quality_control_test(
    qc_test_id: int,
    qc_test_update: schemas.QualityControlTestUpdate,
    db: Session = Depends(get_db),
):
    """Update a quality control test"""
    db_qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    if not db_qc_test:
        raise HTTPException(status_code=404, detail="Quality control test not found")
    
    try:
        # Update only provided fields
        update_data = qc_test_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_qc_test, field, value)
        
        db_qc_test.updated_at = datetime.now()
        db.commit()
        db.refresh(db_qc_test)
        
        logger.info(f"Updated QC test {qc_test_id}")
        return db_qc_test
    except Exception as e:
        logger.error(f"Error updating QC test: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/quality-control-tests/{qc_test_id}")
async def delete_quality_control_test(qc_test_id: int, db: Session = Depends(get_db)):
    """Delete a quality control test"""
    db_qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    if not db_qc_test:
        raise HTTPException(status_code=404, detail="Quality control test not found")
    
    try:
        # Delete associated photo if exists
        if db_qc_test.photo_url:
            # Extract filename from URL (e.g., "/qc_photos/filename.jpg" -> "filename.jpg")
            url_filename = Path(db_qc_test.photo_url).name
            # Only delete if it's a valid QC photo filename pattern
            # Expected pattern: qc_{id}_{timestamp}.{ext}
            if (url_filename and 
                url_filename.startswith('qc_') and 
                not any(bad in url_filename for bad in ['..', '/', '\\'])):
                photo_path = UPLOAD_DIR / url_filename
                # Ensure the file is within UPLOAD_DIR and exists
                try:
                    photo_resolved = photo_path.resolve()
                    upload_resolved = UPLOAD_DIR.resolve()
                    if (str(photo_resolved).startswith(str(upload_resolved)) and 
                        photo_path.exists()):
                        os.unlink(str(photo_path))
                except (ValueError, OSError) as e:
                    logger.warning(f"Could not delete photo file: {e}")
        
        db.delete(db_qc_test)
        db.commit()
        
        logger.info(f"Deleted QC test {qc_test_id}")
        return {"message": "Quality control test deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting QC test: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quality-control-tests/{qc_test_id}/upload-photo")
async def upload_qc_photo(
    qc_test_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a photo for a quality control test"""
    # Verify QC test exists
    db_qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    if not db_qc_test:
        raise HTTPException(status_code=404, detail="Quality control test not found")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate and sanitize file extension (prevent path injection)
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    original_extension = Path(file.filename).suffix.lower()
    if original_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Use a safe, validated extension from our whitelist
    # This ensures no user-provided data is used in the path
    safe_extension = original_extension if original_extension in ALLOWED_EXTENSIONS else '.jpg'
    
    try:
        # Generate unique filename with only safe, controlled values
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"qc_{qc_test_id}_{timestamp}{safe_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Double-check: Ensure the file_path is within UPLOAD_DIR (prevent path traversal)
        try:
            file_path_resolved = file_path.resolve()
            upload_dir_resolved = UPLOAD_DIR.resolve()
            if not str(file_path_resolved).startswith(str(upload_dir_resolved)):
                raise HTTPException(status_code=400, detail="Invalid file path")
        except (ValueError, OSError):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        # Save file
        with open(str(file_path), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update QC test with photo URL
        db_qc_test.photo_url = f"/qc_photos/{unique_filename}"
        db_qc_test.updated_at = datetime.now()
        db.commit()
        
        logger.info(f"Uploaded photo for QC test {qc_test_id}")
        return {"message": "Photo uploaded successfully", "photo_url": db_qc_test.photo_url}
    except Exception as e:
        logger.error(f"Error uploading photo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quality-control-tests/{qc_test_id}/export-pdf")
async def export_qc_test_pdf(qc_test_id: int, db: Session = Depends(get_db)):
    """Export quality control test as PDF"""
    # Get QC test
    qc_test = (
        db.query(models.QualityControlTest)
        .filter(models.QualityControlTest.id == qc_test_id)
        .first()
    )
    if not qc_test:
        raise HTTPException(status_code=404, detail="Quality control test not found")
    
    # Get batch info
    batch = db.query(models.Batches).filter(models.Batches.id == qc_test.batch_id).first()
    
    try:
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
        )
        story.append(Paragraph("Quality Control Test Report", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Batch Information
        story.append(Paragraph("<b>Batch Information</b>", styles['Heading2']))
        batch_data = [
            ["Batch Name:", batch.batch_name if batch else "N/A"],
            ["Batch Number:", str(batch.batch_number) if batch else "N/A"],
            ["Test Date:", qc_test.test_date.strftime("%Y-%m-%d %H:%M") if qc_test.test_date else "N/A"],
        ]
        batch_table = Table(batch_data, colWidths=[2 * inch, 4 * inch])
        batch_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(batch_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Measurements
        story.append(Paragraph("<b>Measurements</b>", styles['Heading2']))
        measurement_data = [
            ["Final Gravity:", f"{qc_test.final_gravity:.3f}" if qc_test.final_gravity else "N/A"],
            ["ABV (Actual):", f"{qc_test.abv_actual:.2f}%" if qc_test.abv_actual else "N/A"],
            ["Color:", qc_test.color or "N/A"],
            ["Clarity:", qc_test.clarity or "N/A"],
            ["BJCP Score:", f"{qc_test.score:.1f}/50" if qc_test.score else "N/A"],
        ]
        measurement_table = Table(measurement_data, colWidths=[2 * inch, 4 * inch])
        measurement_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(measurement_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Tasting Notes
        if qc_test.taste_notes:
            story.append(Paragraph("<b>Tasting Notes</b>", styles['Heading2']))
            story.append(Paragraph(qc_test.taste_notes, styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Return as streaming response
        filename = f"qc_test_{qc_test_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
