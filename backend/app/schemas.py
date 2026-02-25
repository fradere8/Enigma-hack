from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RequestBase(BaseModel):
    sender_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    email: str
    full_text: str

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    sender_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    serial_numbers: Optional[str] = None
    device_type: Optional[str] = None
    sentiment: Optional[str] = None
    issue_summary: Optional[str] = None
    status: Optional[str] = None
    operator_comment: Optional[str] = None

class RequestResponse(RequestBase):
    id: int
    received_at: datetime
    serial_numbers: Optional[str]
    device_type: Optional[str]
    sentiment: str
    issue_summary: Optional[str]
    status: str
    operator_comment: Optional[str]

    class Config:
        from_attributes = True
