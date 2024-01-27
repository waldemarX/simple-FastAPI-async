from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from models.models import Customer, Product, Order
from schemas.schemas import CustomerCreate, ProductCreate, OrderCreate


async def create_customer(db: AsyncSession, customer: CustomerCreate):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(Customer).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(Product).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(**order.model_dump())

    # Add the order to the session
    db.add(db_order)

    # Commit the changes to the database
    await db.commit()

    # Refresh the order instance to get the updated values from the database
    await db.refresh(db_order)

    # Explicitly load customer and product relationships using selectinload
    stmt = (
        select(Order)
        .where(Order.id == db_order.id)
        .options(selectinload(Order.customer), selectinload(Order.product))
    )

    # Execute the query and get the updated order instance with relationships loaded
    db_order = (await db.execute(stmt)).scalar()

    return db_order


async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = (
        select(Order)
        .options(selectinload(Order.customer), selectinload(Order.product))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()
