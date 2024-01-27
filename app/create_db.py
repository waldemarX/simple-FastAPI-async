import asyncio

from models.models import Customer, Order, Product
from database.database import create_tables

models = [Customer, Product, Order]


async def main():
    await create_tables(models)


asyncio.run(main())
