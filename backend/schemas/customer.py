from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    customer_name: str
    email: EmailStr


class CustomerResponse(BaseModel):
    customer_id: int
    customer_name: str
    email: EmailStr

    class Config:
        from_attributes = True