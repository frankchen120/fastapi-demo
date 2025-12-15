from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItemResponse(BaseModel):
    product_name: str
    unit_price: float
    quantity: int
    
class OrderResponse(BaseModel):
    id: int
    created_at: datetime
