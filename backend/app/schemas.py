from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Базовая схема (общие поля)
class RequestBase(BaseModel):
    sender_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    email: str
    full_text: str

# Для создания (симуляция прихода письма)
class RequestCreate(RequestBase):
    pass

# Для обновления (оператор правит поля или меняет статус)
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

# То, что отдаем на Фронтенд (строго по таблице)
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