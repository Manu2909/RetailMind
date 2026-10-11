from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, unique=True, index=True) # E.g., "FOOD_1_001"
    name = Column(String, nullable=False)
    category = Column(String)
    current_stock = Column(Integer, default=0)
    safety_stock_level = Column(Integer, default=10)
    price = Column(Float, default=0.0)

    # Relationship to sales
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date, nullable=False)
    quantity_sold = Column(Integer, nullable=False)

    # Relationship to product
    product = relationship("Product", back_populates="sales")