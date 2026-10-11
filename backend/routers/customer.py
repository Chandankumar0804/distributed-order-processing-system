from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.customer import Customer
from backend.schemas.customer import CustomerCreate, CustomerResponse
from backend.models.order import Order


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# ---------------------------------
# CREATE CUSTOMER
# ---------------------------------
@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_customer = Customer(
        customer_name=customer.customer_name,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# ---------------------------------
# GET ALL CUSTOMERS
# ---------------------------------
@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


# ---------------------------------
# CUSTOMER-WISE REPORT
# ---------------------------------
@router.get("/report")
def customer_report(db: Session = Depends(get_db)):

    customers = db.query(Customer).order_by(
        Customer.customer_id.asc()
    ).all()

    report = []

    for customer in customers:

        orders = db.query(Order).filter(
            Order.customer_id == customer.customer_id
        ).all()

        total_orders = len(orders)

        pending_orders = sum(
            1 for order in orders
            if order.payment_status == "Pending"
        )

        processing_orders = sum(
            1 for order in orders
            if order.payment_status == "Processing"
        )

        failed_orders = sum(
            1 for order in orders
            if order.payment_status == "Failed"
        )

        cancelled_orders = sum(
            1 for order in orders
            if order.payment_status == "Cancelled"
        )

        total_spent = sum(
            order.final_amount or 0
            for order in orders
            if order.payment_status != "Cancelled"
        )

        report.append({
            "customer_id": customer.customer_id,
            "customer_name": customer.customer_name,
            "email": customer.email,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "processing_orders": processing_orders,
            "failed_orders": failed_orders,
            "cancelled_orders": cancelled_orders,
            "total_spent": total_spent
        })

    return report