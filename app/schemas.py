from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    quantity: int = 1
    
class ItemResponse(BaseModel):
    name: str
    total: float

class Discount(BaseModel):
    name: str
    price: int
    discount: float
    
class DiscountResponse(BaseModel):
    name: str
    final_price: float
            