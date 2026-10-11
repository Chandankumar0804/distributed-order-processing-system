
def process_payment(order):
    """
    Demo payment processing function.
    """

    if order.quantity <= 0:
        return {
            "success": False,
            "message": "Invalid order quantity"
        }

    # Demo payment simulation
    return {
        "success": True,
        "message": "Payment processed successfully"
    }
