from pydantic import BaseModel

class Discount(BaseModel):
    name: str
    price: int
    discount: float
    
class DiscountResponse(BaseModel):
    name: str
    final_price: float
            
            