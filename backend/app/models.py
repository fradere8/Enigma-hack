from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    received_at = Column(DateTime, default=datetime.utcnow)

    sender_name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    phone = Column(String, nullable=True) 
    email = Column(String, index=True) 

    serial_numbers = Column(String, nullable=True) 
    device_type = Column(String, nullable=True)   

    sentiment = Column(String, default="Neutral") 
    issue_summary = Column(Text, nullable=True)  

    full_text = Column(Text)                      
    status = Column(String, default="New")         
    operator_comment = Column(Text, nullable=True)
