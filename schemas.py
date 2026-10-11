from pydantic import BaseModel
from typing import Optional
from datetime import date

# Base properties for a Product
class ProductBase(BaseModel):
    item_id: str
    name: str
    category: Optional[str] = "General"
    current_stock: int = 0
    safety_stock_level: int = 10
    price: float = 0.0

# Schema for creating a new product (inherits from Base)
class ProductCreate(ProductBase):
    pass

# Schema for returning a product (includes the database ID)
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True