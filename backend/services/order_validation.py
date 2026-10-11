
from decimal import Decimal

from sqlalchemy.orm import Session

from backend.models.customer import Customer
from backend.models.product import Product


def validate_order(
    db: Session,
    customer_id: int,
    product_id: int,
    quantity: int,
    unit_price: Decimal,
):
    """
    Validate order details before processing.
    """

    # 1. Validate quantity
    if quantity <= 0:
        return {
            "valid": False,
            "reason": "Quantity must be greater than zero."
        }

    # 2. Validate unit price
    if unit_price <= 0:
        return {
            "valid": False,
            "reason": "Unit price must be greater than zero."
        }

    # 3. Check customer
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        return {
            "valid": False,
            "reason": "Customer not found."
        }

    # 4. Check product
    product = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )

    if not product:
        return {
            "valid": False,
            "reason": "Product not found."
        }

    # 5. Check available stock
    if product.available_stock < quantity:
        return {
            "valid": False,
            "reason": "Insufficient inventory."
        }

    # 6. Validation successful
    return {
        "valid": True,
        "reason": "Order validation successful."
    }
