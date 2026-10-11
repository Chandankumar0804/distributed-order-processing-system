from sqlalchemy import (
    Column, Integer, String, DateTime, DECIMAL, ForeignKey,Text
)

from backend.database.connection import Base


class Order(Base):
    __tablename__ = "orders"
   

    order_id = Column(
    Integer,
    primary_key=True,
    autoincrement=True
)
    retry_count = Column(Integer, default=0, nullable=False)
    last_error = Column(Text, nullable=True)
 
    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    payment_type = Column(
    String(30),
    nullable=False,
    default="CASH"
)

    quantity = Column(Integer, nullable=False)

    unit_price = Column(DECIMAL(10, 2), nullable=False)

    order_time = Column(DateTime, nullable=False)

    payment_status = Column(String(30), nullable=False)

    payment_type = Column(String(30), nullable=False, default="CASH")

    source = Column(String(30), nullable=False)

    subtotal = Column(DECIMAL(10, 2), nullable=False, default=0)

    discount_rate = Column(DECIMAL(5, 2), nullable=False, default=0)

    discount_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    
    final_amount = Column(DECIMAL(10, 2), nullable=False, default=0)