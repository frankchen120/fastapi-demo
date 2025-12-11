from fastapi import FastAPI
from pydantic import BaseModel

from app.routers.discount import router as discount_router

# 一次引 不建議
#  from app.schemas import *
# 各別寫 多的時後麻煩
#  from app.schemas import Item, ItemResponse, Discount, DiscountResponse
# 引module, 用schemas.X
import app.schemas.schemas as schemas


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


# Day2: POST API
@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.Item):
    total_price = item.price * item.quantity
    return schemas.ItemResponse(
        name = item.name,
        total = total_price
    )


app.include_router(discount_router)
