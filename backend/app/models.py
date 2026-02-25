from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    
    # 1. Дата поступления
    received_at = Column(DateTime, default=datetime.utcnow)
    
    # 2. Данные заявителя
    sender_name = Column(String, nullable=True)  # ФИО
    company_name = Column(String, nullable=True) # Объект / Предприятие
    phone = Column(String, nullable=True)        # Телефон
    email = Column(String, index=True)           # Email
    
    # 3. Технические данные (извлекает AI)
    serial_numbers = Column(String, nullable=True) # Заводские номера (строкой через запятую)
    device_type = Column(String, nullable=True)    # Тип приборов
    
    # 4. Аналитика (AI)
    sentiment = Column(String, default="Neutral")  # Тональность: Positive, Neutral, Negative
    issue_summary = Column(Text, nullable=True)    # Суть вопроса (кратко)
    
    # 5. Обработка
    full_text = Column(Text)                       # Полный текст письма (для модального окна)
    status = Column(String, default="New")         # Статус: New, Processed
    operator_comment = Column(Text, nullable=True) # Ответ оператора / Черновик