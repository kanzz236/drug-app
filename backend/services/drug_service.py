from sqlalchemy.orm import Session
from sqlalchemy import text
from database.models import Medicine, Symptom

def get_medicine_by_id(db: Session, medicine_id: int):
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()

def get_all_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()

def search_medicines_by_symptom(db: Session, symptom_name: str):
    return db.query(Medicine).join(Medicine.symptoms).filter(Symptom.name.ilike(f"%{symptom_name}%")).all()