import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.routers.discount import router as discount_router
from app.routers.auth import router as auth_router
from app.routers.order import router as order_router
from app.routers.report import router as report_router
from app.core.logging import setup_logging
# 一次引 不建議
#  from app.schemas import *
# 各別寫 多的時後麻煩
#  from app.schemas import Item, ItemResponse, Discount, DiscountResponse
# 引module, 用schemas.X
import app.schemas.schemas as schemas

setup_logging()

logger = logging.getLogger("api")


# 建立FastAPI物件
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"➡️{request.method} {request.url.path} - {response.status_code}")
    return response


# CORKS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", # 前端 dev server
    ],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["Authorization","Content-Type"],
)

#最簡單的GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FAstAPI"}

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
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(report_router)
