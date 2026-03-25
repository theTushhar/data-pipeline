from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

class CustomerBase(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    account_balance: Optional[Decimal] = None
    created_at: Optional[datetime] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    class Config:
        from_attributes = True

class PaginatedCustomerResponse(BaseModel):
    total: int
    page: int
    limit: int
    customers: List[CustomerResponse]
