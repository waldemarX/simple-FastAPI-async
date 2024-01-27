from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import AsyncSessionLocal, create_tables
from crud.crud import (
    create_customer,
    get_customers,
    create_product,
    get_products,
    create_order,
    get_orders,
)
from schemas.schemas import (
    CustomerCreate,
    Customer,
    ProductCreate,
    Product,
    OrderCreate,
    Order,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_tables()


# CORS middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, change it based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the database session
async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.post("/customers/", response_model=Customer)
async def create_customer_api(
    customer: CustomerCreate, db: AsyncSession = Depends(get_db)
):
    return await create_customer(db, customer)


@app.get("/customers/", response_model=list[Customer])
async def read_customers(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await get_customers(db, skip=skip, limit=limit)


@app.post("/products/", response_model=Product)
async def create_product_api(
    product: ProductCreate, db: AsyncSession = Depends(get_db)
):
    return await create_product(db, product)


@app.get("/products/", response_model=list[Product])
async def read_products(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await get_products(db, skip=skip, limit=limit)


@app.post("/orders/", response_model=Order)
async def create_order_api(
    order: OrderCreate, db: AsyncSession = Depends(get_db)
):
    return await create_order(db, order)


@app.get("/orders/", response_model=list[Order])
async def read_orders(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await get_orders(db, skip=skip, limit=limit)
