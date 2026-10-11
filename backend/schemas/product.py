from pydantic import BaseModel


class ProductCreate(BaseModel):
    product_name: str
    available_stock: int
    reserved_stock: int = 0


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    available_stock: int
    reserved_stock: int

    class Config:
        from_attributes = True