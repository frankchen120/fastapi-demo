from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    quantity: int = 1
    
class ItemResponse(BaseModel):
    name: str
    total: float
    