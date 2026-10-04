from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database import get_db
from services.ocr_service import process_prescription_image, identify_medicine_image_logic

router = APIRouter(prefix="/api/v1", tags=["OCR & AI Recognition"])

@router.post("/ocr/scan")
async def scan_prescription(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result_text = await process_prescription_image(temp_file_path)
        return {"success": True, "result": result_text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý OCR đơn thuốc: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.post("/medicines/identify-by-image")
async def identify_medicine_by_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File tải lên phải là hình ảnh!")
    
    try:
        image_bytes = await file.read()
        result = await identify_medicine_image_logic(image_bytes, file.content_type, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))