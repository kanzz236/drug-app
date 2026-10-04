from pydantic import BaseModel
from typing import Optional, List

class ActiveIngredientBase(BaseModel):
    name: str
    description: Optional[str] = None

class ActiveIngredientResponse(ActiveIngredientBase):
    id: int

    class Config:
        from_attributes = True


class MedicineBase(BaseModel):
    name: str
    sdk_code: Optional[str] = None
    strength: Optional[str] = None
    dosage_form: Optional[str] = None
    manufacturer: Optional[str] = None
    indication: Optional[str] = None
    contraindication: Optional[str] = None
    side_effect: Optional[str] = None
    warning: Optional[str] = None
    active_ingredient_id: Optional[int] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int
    active_ingredient: Optional[ActiveIngredientResponse] = None

    class Config:
        from_attributes = True