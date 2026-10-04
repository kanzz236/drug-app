from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from database.database import get_db
from schemas.drug import MedicineResponse
from services.drug_service import get_all_medicines, get_medicine_by_id

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.get("/medicines")
def get_medicines(
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = Query(None, description="Nhập tên thuốc cần tìm kiếm"), 
    db = Depends(get_db)
):
    # Câu lệnh SQL linh hoạt: Nếu có truyền name thì dùng LIKE để lọc, không thì lấy tất cả
    if name:
        query = text("""
            SELECT m.id, m.name, m.sdk_code, m.strength, m.dosage_form, m.manufacturer, 
                   m.indication, m.contraindication, m.side_effect, m.warning,
                   a.name as active_ingredient
            FROM medicines m
            LEFT JOIN active_ingredients a ON m.active_ingredient_id = a.id
            WHERE m.name LIKE :search_name
            LIMIT :limit OFFSET :skip
        """)
        result = db.execute(query, {"search_name": f"%{name}%", "limit": limit, "skip": skip}).mappings().all()
    else:
        query = text("""
            SELECT m.id, m.name, m.sdk_code, m.strength, m.dosage_form, m.manufacturer, 
                   m.indication, m.contraindication, m.side_effect, m.warning,
                   a.name as active_ingredient
            FROM medicines m
            LEFT JOIN active_ingredients a ON m.active_ingredient_id = a.id
            LIMIT :limit OFFSET :skip
        """)
        result = db.execute(query, {"limit": limit, "skip": skip}).mappings().all()
        
    return [dict(row) for row in result]