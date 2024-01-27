from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    email: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_price: float


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    created_at: str
    customer: Customer
    product: Product

    class Config:
        orm_mode = True
