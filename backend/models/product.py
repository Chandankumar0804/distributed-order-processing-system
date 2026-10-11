from sqlalchemy import Column, Integer, String

from backend.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_name = Column(
        String(150),
        nullable=False
    )

    available_stock = Column(
        Integer,
        nullable=False,
        default=0
    )

    reserved_stock = Column(
        Integer,
        nullable=False,
        default=0
    )