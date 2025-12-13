from pydantic import BaseModel, Field
from typing import Optional

class Discount(BaseModel):
    name: str
    price: int
    discount: float = Field(ge=0, lt=1) # 0 <= discount < 1
    
class DiscountResponse(BaseModel):
    id: int
    name: str
    final_price: float
           
class DiscountUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = Field(default=None, ge=0, lt=1)
    

            