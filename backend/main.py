from fastapi import FastAPI
from sqlalchemy import text

from backend.database.connection import engine
from backend.models import Customer, Product, Order, OrderLog, User
from backend.schemas import (
    CustomerCreate, CustomerResponse,
    ProductCreate, ProductResponse,
    OrderCreate, OrderResponse,
    OrderLogCreate, OrderLogResponse,
    UserCreate, UserResponse
)
from backend.routers.customer import router as customer_router
from backend.routers.product import router as product_router
from backend.routers.order import router as order_router
from backend.routers.order_log import router as order_log_router
from backend.routers.auth import router as auth_router

from backend.routers.admin import router as admin_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(order_log_router)
app.include_router(auth_router)
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Order Processing System"}


@app.get("/test-db")
def test_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "message": "Database connected successfully",
        "result": result.scalar()
    }