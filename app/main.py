from contextlib import asynccontextmanager
import logging
import time
import uuid
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from app.core.exceptions import AppError
from app.routers.discount import router as discount_router
from app.routers.auth import get_db, router as auth_router
from app.routers.order import router as order_router
from app.routers.report import router as report_router
from app.core.logging import setup_logging
from sqlalchemy.orm import Session


# 一次引 不建議
#  from app.schemas import *
# 各別寫 多的時後麻煩
#  from app.schemas import Item, ItemResponse, Discount, DiscountResponse
# 引module, 用schemas.X
from app.schemas.error import ErrorResponse
import app.schemas.schemas as schemas

setup_logging()
logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: app is starting")
    yield
    logger.info("shutdown: app is stopping")


# 建立FastAPI物件
app = FastAPI(lifespan=lifespan)

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
async def request_context_logging(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    start = time.perf_counter()
    has_auth = request.headers.get("authorization") is not None
    
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.perf_counter() - start) * 1000)
        
        # 考慮nginx client ip        
        xff = request.headers.get("x-forwarded-for")
        client_ip = (xff.split(",")[0].strip() if xff else (request.client.host if request.client else None))

        
        #status_code = getattr(locals().get("response", None), "status_code", 500)
        status_code = response.status_code if response else None
        
        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "client_ip": client_ip,
                "has_auth": has_auth,
            }
        )
        
        if response is not None:
            response.headers["X-Request-ID"] = request_id


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

@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ready"}

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
