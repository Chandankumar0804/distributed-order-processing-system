from sqlalchemy.orm import Session

from backend.models.order import Order


def process_fifo_orders(db: Session):
    orders = (
        db.query(Order)
        .filter(Order.payment_status == "Pending")
        .order_by(Order.order_time.asc())
        .all()
    )

    processed_orders = []

    for order in orders:
        order.payment_status = "Processing"

        processed_orders.append({
            "order_id": order.order_id,
            "status": "Processing"
        })

    db.commit()

    return processed_orders