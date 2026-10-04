from pydantic import BaseModel
from typing import List, Optional
from schemas.drug import MedicineResponse

class SymptomBase(BaseModel):
    name: str

class SymptomCreate(SymptomBase):
    pass

class SymptomResponse(SymptomBase):
    id: int
    medicines: List[MedicineResponse] = []

    class Config:
        from_attributes = True