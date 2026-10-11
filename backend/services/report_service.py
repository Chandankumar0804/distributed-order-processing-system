from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.order import Order


def get_order_report(db: Session):

    total_orders = db.query(Order).count()

    pending_orders = (
        db.query(Order)
        .filter(Order.payment_status == "Pending")
        .count()
    )

    processing_orders = (
        db.query(Order)
        .filter(Order.payment_status == "Processing")
        .count()
    )

    failed_orders = (
        db.query(Order)
        .filter(Order.payment_status == "Failed")
        .count()
    )

    cancelled_orders = (
        db.query(Order)
        .filter(Order.payment_status == "Cancelled")
        .count()
    )

    total_revenue = (
        db.query(func.sum(Order.final_amount))
        .filter(Order.payment_status != "Cancelled")
        .scalar()
    )

    if total_revenue is None:
        total_revenue = 0

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "failed_orders": failed_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": total_revenue
    }