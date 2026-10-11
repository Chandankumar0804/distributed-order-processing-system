from decimal import Decimal


def calculate_discount(subtotal: Decimal):
    """
    Calculate discount based on order subtotal.
    """

    if subtotal < Decimal("1000"):
        discount_rate = Decimal("0")

    elif subtotal < Decimal("5000"):
        discount_rate = Decimal("0.05")

    elif subtotal < Decimal("10000"):
        discount_rate = Decimal("0.10")

    else:
        discount_rate = Decimal("0.15")

    discount_amount = subtotal * discount_rate
    final_amount = subtotal - discount_amount

    return {
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount_amount": discount_amount,
        "final_amount": final_amount
    }