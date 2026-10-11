from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, ForeignKey, func
)
from backend.database.connection import Base


class OrderLog(Base):
    __tablename__ = "order_logs"

    log_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    status = Column(String(30), nullable=False)

    reason = Column(Text, nullable=True)

    timestamp = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )