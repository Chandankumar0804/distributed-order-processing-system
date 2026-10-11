
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.order_log import OrderLog
from backend.schemas.order_log import OrderLogResponse


router = APIRouter(
    prefix="/order-logs",
    tags=["Order Logs"]
)


# Get all order logs with filter and pagination
@router.get("/", response_model=list[OrderLogResponse])
def get_order_logs(
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(OrderLog)

    # Filter by status
    if status:
        query = query.filter(
            OrderLog.status == status
        )

    # Pagination and sorting
    logs = (
        query.order_by(OrderLog.log_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return logs


# Get logs for a specific order
@router.get("/order/{order_id}", response_model=list[OrderLogResponse])
def get_logs_by_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    logs = (
        db.query(OrderLog)
        .filter(OrderLog.order_id == order_id)
        .order_by(OrderLog.log_id.desc())
        .all()
    )

    return logs
