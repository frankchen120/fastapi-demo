from fastapi import FastAPI
from app.schemas import Item
from pydantic import BaseModel


# 建立FastAPI物件
app = FastAPI()

#最簡單的GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FAstAPI, Weel1 Day1!"}

#帶路徑參數的 endpoint
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"greeting": f"Hello, {name}"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/square")
def square(x: int):
    return {"x": x, "square": x*x}

class ItemResponse(BaseModel):
    name: str
    total: float
    
# Day2: POST API
@app.post("/items")
def create_item(item: Item, response_model=ItemResponse):
    total_price = item.price * item.quantity
    return {
        "name": item.name,
        "total": total_price
    }