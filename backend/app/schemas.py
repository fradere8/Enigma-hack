from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Данные отправителя
    sender_name = Column(String, nullable=True)  # ФИО
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)      # Объект/Предприятие
    
    # Технические данные (извлекаются AI)
    serial_numbers = Column(String, nullable=True) # Можно хранить через запятую
    device_type = Column(String, nullable=True)    # Тип прибора
    
    # Аналитика
    sentiment = Column(String, default="Neutral")  # Positive/Neutral/Negative
    issue_summary = Column(Text, nullable=True)    # Краткая суть проблемы
    
    # Полный текст и статус
    full_text = Column(Text)                       # Текст письма
    status = Column(String, default="New")         # New, In Progress, Closed
    admin_response = Column(Text, nullable=True)   # Черновик или финальный ответ