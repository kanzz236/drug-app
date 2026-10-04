from pydantic import BaseModel
from typing import List, Optional

class OcrResultItem(BaseModel):
    drug_name: str
    dosage: Optional[str] = None
    quantity: Optional[str] = None
    instruction: Optional[str] = None

class OcrResponse(BaseModel):
    success: bool
    message: str
    data: List[OcrResultItem] = []