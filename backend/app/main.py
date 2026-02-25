from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import random
from datetime import datetime, timedelta

from app.database import engine, Base, get_db
from app.models import Request
from app.schemas import RequestCreate, RequestResponse, RequestUpdate

app = FastAPI(title="Support AI Assistant API")

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/api/requests", response_model=List[RequestResponse])
async def get_requests(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Request).order_by(Request.received_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()
@app.post("/api/requests", response_model=RequestResponse)
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    new_request = Request(
        **request.model_dump(),
        received_at=datetime.utcnow(),
        sentiment="Neutral",  
        issue_summary="Требуется анализ...",
        status="New"
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request

@app.patch("/api/requests/{request_id}", response_model=RequestResponse)
async def update_request(request_id: int, update_data: RequestUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Request).filter(Request.id == request_id))
    request = result.scalars().first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(request, key, value)

    await db.commit()
    await db.refresh(request)
    return request

@app.post("/api/debug/seed_data")
async def seed_data(db: AsyncSession = Depends(get_db)):
    sample_requests = [
        Request(
            sender_name="Иванов И.И.",
            company_name="ООО Ромашка",
            phone="+79161234567",
            email="ivanov@romashka.ru",
            full_text="Сломался прибор, номер 12345. Срочно почините!",
            serial_numbers="SN-12345",
            device_type="Датчик давления",
            sentiment="Negative",
            issue_summary="Поломка датчика, срочный ремонт",
            status="New",
            received_at=datetime.utcnow()
        ),
        Request(
            sender_name="Петров П.П.",
            company_name="Завод №1",
            phone="+79039876543",
            email="petrov@zavod1.ru",
            full_text="Добрый день. Высылаю отчет по эксплуатации.",
            serial_numbers="",
            device_type="",
            sentiment="Positive",
            issue_summary="Отчет по эксплуатации",
            status="Processed",
            received_at=datetime.utcnow() - timedelta(hours=2)
        )
    ]
    db.add_all(sample_requests)
    await db.commit()
    return {"message": "Test data created!"}
