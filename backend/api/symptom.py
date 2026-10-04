from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database import get_db

router = APIRouter(prefix="/api/v1/symptoms", tags=["Symptoms"])

@router.get("/search")
def search_by_symptom(symptom_name: str = Query(..., description="Tên triệu chứng"), db: Session = Depends(get_db)):
    """
    Tra cứu danh sách thuốc dựa theo triệu chứng bệnh
    """
    sql = text("""
        SELECT m.id as medicine_id, m.name as medicine_name, m.strength, m.dosage_form, s.name as symptom_name
        FROM medicines m
        JOIN medicine_symptoms ms ON m.id = ms.medicine_id
        JOIN symptoms s ON ms.symptom_id = s.id
        WHERE LOWER(s.name) LIKE LOWER(:s)
    """)
    results = db.execute(sql, {"s": f"%{symptom_name}%"}).mappings().all()
    return list(results)