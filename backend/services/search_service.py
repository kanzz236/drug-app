from sqlalchemy.orm import Session
from sqlalchemy import text
from database.models import Medicine

def global_search(db: Session, keyword: str):
    """
    Tìm kiếm tổng hợp theo tên thuốc, hoạt chất hoặc chỉ định
    """
    search_term = f"%{keyword}%"
    medicines = db.query(Medicine).filter(
        (Medicine.name.ilike(search_term)) | 
        (Medicine.indication.ilike(search_term))
    ).all()
    return medicines