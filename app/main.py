import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.core.exceptions import AppError
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
from app.schemas.error import ErrorResponse
import app.schemas.schemas as schemas

setup_logging()
logger = logging.getLogger("api")

# 建立FastAPI物件
app = FastAPI()

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status_map = {
        "BAD_REQUEST": 400,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
        "TOO_MANY_REQUESTS": 429,
    }
    
    status_code = status_map.get(getattr(exc, "code", "APP_ERROR"), 400)
    
    payload = ErrorResponse(
        code = exc.code,
        message = exc.message,
        details = getattr(exc, "detail", None)
    ).model_dump()
    
    return JSONResponse(status_code=status_code, content=payload)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    auth = request.headers.get("authorization")
    logger.info(f"➡️{request.method} {request.url.path} auth={auth[:20] + '...' if auth else None}")
    response = await call_next(request)
    logger.info(f"➡️{request.method} {request.url.path} - {response.status_code}")
    return response


# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000", # 前端 dev server
    ],
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["Authorization","Content-Type"],
)

#最簡單的GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

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
