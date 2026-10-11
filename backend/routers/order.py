from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database.connection import get_db
from backend.models.order import Order
from backend.models.customer import Customer
from backend.models.product import Product
from backend.models.order_log import OrderLog

from backend.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate
)

from backend.services.order_validation import validate_order
from backend.services.discount_service import calculate_discount
from backend.services.fifo_service import process_fifo_orders
from backend.services.report_service import get_order_report


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# ---------------------------------
# 1. CREATE ORDER WITH VALIDATION
# ---------------------------------
@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    try:

        # ---------------------------------
        # Step 1: Validate order
        # ---------------------------------
        validation = validate_order(
            db=db,
            customer_id=order.customer_id,
            product_id=order.product_id,
            quantity=order.quantity,
            unit_price=order.unit_price
        )

        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=validation["reason"]
            )

        # ---------------------------------
        # Step 2: Check duplicate order ID
        # ---------------------------------
        if order.order_id is not None:

            existing_order = (
                db.query(Order)
                .filter(Order.order_id == order.order_id)
                .first()
            )

            if existing_order:
                raise HTTPException(
                    status_code=409,
                    detail=f"Order ID {order.order_id} already exists"
                )

        # ---------------------------------
        # Step 3: Lock product
        # ---------------------------------
        product = (
            db.query(Product)
            .filter(Product.product_id == order.product_id)
            .with_for_update()
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        # ---------------------------------
        # Step 4: Recheck stock
        # ---------------------------------
        if product.available_stock < order.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        # ---------------------------------
        # Step 5: Calculate amount
        # ---------------------------------
        subtotal = order.quantity * order.unit_price

        discount = calculate_discount(subtotal)

        subtotal = discount["subtotal"]
        discount_rate = discount["discount_rate"]
        discount_amount = discount["discount_amount"]
        final_amount = discount["final_amount"]

        # ---------------------------------
        # Step 6: Reserve stock
        # ---------------------------------
        product.available_stock -= order.quantity
        product.reserved_stock += order.quantity

        # ---------------------------------
        # Step 7: Create order
        # ---------------------------------
        new_order = Order(
            order_id=order.order_id,
            customer_id=order.customer_id,
            product_id=order.product_id,
            quantity=order.quantity,
            unit_price=order.unit_price,
            order_time=datetime.now(),
            payment_status=order.payment_status,
            payment_type=order.payment_type,
            source=order.source,

            subtotal=subtotal,
            discount_rate=discount_rate,
            discount_amount=discount_amount,
            final_amount=final_amount
        )

        db.add(new_order)
        db.flush()

        # ---------------------------------
        # Step 8: Create order log
        # ---------------------------------
        new_log = OrderLog(
            order_id=new_order.order_id,
            status=order.payment_status,
            reason="Order validated, discount calculated and stock reserved"
        )

        db.add(new_log)

        # ---------------------------------
        # Step 9: Commit
        # ---------------------------------
        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception:
        db.rollback()
        raise


# ---------------------------------
# 2. GET ALL ORDERS WITH FILTERS
# ---------------------------------
@router.get("/", response_model=list[OrderResponse])
def get_orders(
    payment_status: str | None = None,
    source: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Order)

    if payment_status:
        query = query.filter(
            Order.payment_status == payment_status
        )

    if source:
        query = query.filter(
            Order.source == source
        )

    orders = (
        query
        .order_by(Order.order_time.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return orders


# ---------------------------------
# 3. UPDATE ORDER STATUS
# ---------------------------------
@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    try:

        order = (
            db.query(Order)
            .filter(Order.order_id == order_id)
            .with_for_update()
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.payment_status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cannot update a cancelled order"
            )

        old_status = order.payment_status
        new_status = data.payment_status

        # ---------------------------------
        # PAYMENT FAILURE -> STOCK ROLLBACK
        # ---------------------------------
        if new_status == "Failed" and old_status != "Failed":

            product = (
                db.query(Product)
                .filter(Product.product_id == order.product_id)
                .with_for_update()
                .first()
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )

            # Release reserved stock
            product.available_stock += order.quantity
            product.reserved_stock -= order.quantity

            if product.reserved_stock < 0:
                product.reserved_stock = 0

            order.last_error = data.reason

        order.payment_status = new_status

        new_log = OrderLog(
            order_id=order_id,
            status=new_status,
            reason=data.reason
        )

        db.add(new_log)

        db.commit()

        return {
            "message": "Order status updated successfully",
            "order_id": order_id,
            "payment_status": new_status
        }

    except Exception:
        db.rollback()
        raise


# ---------------------------------
# 4. CANCEL ORDER
# ---------------------------------
@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    try:

        order = (
            db.query(Order)
            .filter(Order.order_id == order_id)
            .with_for_update()
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.payment_status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Order is already cancelled"
            )

        if order.payment_status != "Pending":
            raise HTTPException(
                status_code=400,
                detail="Only pending orders can be cancelled"
            )

        product = (
            db.query(Product)
            .filter(Product.product_id == order.product_id)
            .with_for_update()
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product.available_stock += order.quantity
        product.reserved_stock -= order.quantity

        if product.reserved_stock < 0:
            product.reserved_stock = 0

        order.payment_status = "Cancelled"

        new_log = OrderLog(
            order_id=order_id,
            status="Cancelled",
            reason="Order cancelled by user"
        )

        db.add(new_log)

        db.commit()

        return {
            "message": "Order cancelled successfully",
            "order_id": order_id,
            "payment_status": "Cancelled"
        }

    except Exception:
        db.rollback()
        raise


# ---------------------------------
# 5. RETRY FAILED ORDER
# ---------------------------------
@router.put("/{order_id}/retry")
def retry_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    try:

        order = (
            db.query(Order)
            .filter(Order.order_id == order_id)
            .with_for_update()
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.payment_status != "Failed":
            raise HTTPException(
                status_code=400,
                detail="Only failed orders can be retried"
            )

        if order.retry_count >= 3:
            raise HTTPException(
                status_code=400,
                detail="Maximum retry limit reached"
            )

        # ---------------------------------
        # Lock product
        # ---------------------------------
        product = (
            db.query(Product)
            .filter(Product.product_id == order.product_id)
            .with_for_update()
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        # ---------------------------------
        # Check stock
        # ---------------------------------
        if product.available_stock < order.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock for retry"
            )

        # ---------------------------------
        # Reserve stock again
        # ---------------------------------
        product.available_stock -= order.quantity
        product.reserved_stock += order.quantity

        # ---------------------------------
        # Update retry
        # ---------------------------------
        order.retry_count += 1
        order.last_error = None
        order.payment_status = "Pending"

        # ---------------------------------
        # Create retry log
        # ---------------------------------
        new_log = OrderLog(
            order_id=order_id,
            status="Retried",
            reason=f"Order retry initiated. Attempt {order.retry_count}"
        )

        db.add(new_log)

        retry_count = order.retry_count

        db.commit()

        return {
            "message": "Order retry initiated successfully",
            "order_id": order_id,
            "retry_count": retry_count,
            "payment_status": "Pending"
        }

    except Exception:
        db.rollback()
        raise


# ---------------------------------
# FIFO ORDER PROCESSING
# ---------------------------------
@router.post("/process-fifo")
def process_orders_fifo(
    db: Session = Depends(get_db)
):
    result = process_fifo_orders(db)

    return {
        "message": "Orders processed using FIFO",
        "processed_orders": result
    }


# ---------------------------------
# ORDER REPORT
# ---------------------------------
@router.get("/report")
def order_report(
    db: Session = Depends(get_db)
):
    return get_order_report(db)


# ---------------------------------
# 6. ORDER RECOVERY API
# ---------------------------------
@router.get("/recovery")
def get_recovery_orders(
    db: Session = Depends(get_db)
):
    orders = (
        db.query(Order)
        .filter(Order.payment_status == "Failed")
        .order_by(Order.retry_count.desc())
        .all()
    )

    recovery_data = []

    for order in orders:

        recovery_data.append({
            "order_id": order.order_id,
            "payment_status": order.payment_status,
            "retry_count": order.retry_count,
            "last_error": order.last_error,
            "recovery_status": (
                "Max retries reached"
                if order.retry_count >= 3
                else "Retry pending"
            )
        })

    return recovery_data


# ---------------------------------
# 7. GET ORDER BY ID
# ---------------------------------
@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order