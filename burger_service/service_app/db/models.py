from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
import service_app.db as db

Base = db.Base


class Burger(Base):
    __tablename__ = "burgers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    owner = Column(String)

    orders = relationship("Order", back_populates="burger")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    burger_id = Column(Integer, ForeignKey("burgers.id"))
    burger_name = Column(String)
    customer_name = Column(String)

    burger = relationship("Burger", back_populates="orders")
