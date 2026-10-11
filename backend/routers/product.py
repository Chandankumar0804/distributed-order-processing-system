from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.product import Product
from backend.schemas.product import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    
    
    existing_product = db.query(Product).filter(
        Product.product_name == product.product_name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists"
        )

    new_product = Product(
        product_name=product.product_name,
        available_stock=product.available_stock,
        reserved_stock=product.reserved_stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# ---------------------------------
# INVENTORY REPORT
# ---------------------------------
@router.get("/report")
def inventory_report(
    db: Session = Depends(get_db)
):
    products = (
        db.query(Product)
        .order_by(Product.product_id.asc())
        .all()
    )

    report = []

    for product in products:

        total_stock = (
            product.available_stock +
            product.reserved_stock
        )

        report.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "available_stock": product.available_stock,
            "reserved_stock": product.reserved_stock,
            "total_stock": total_stock
        })

    return report