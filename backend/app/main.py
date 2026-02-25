from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import engine, Base, get_db
from app.models import Request
from app.schemas import RequestCreate, RequestResponse, RequestUpdate

app = FastAPI(title="Support AI Assistant API")

# При старте создаем таблицы (для тестового задания миграции типа Alembic можно опустить)
@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- Эндпоинты ---

# 1. Получить список всех заявок (для таблицы на фронтенде)
@app.get("/api/requests", response_model=List[RequestResponse])
async def get_requests(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Request).offset(skip).limit(limit).order_by(Request.created_at.desc()))
    return result.scalars().all()

# 2. Создать новую заявку (имитация прихода письма)
@app.post("/api/requests", response_model=RequestResponse)
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    # Здесь в будущем будет вызов ML-модели для анализа текста
    # Пока ставим заглушки
    new_request = Request(
        **request.model_dump(),
        sentiment="Neutral",     # TODO: Replace with AI analysis
        issue_summary="Анализ...", 
        status="New"
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return new_request

# 3. Получить одну заявку по ID
@app.get("/api/requests/{request_id}", response_model=RequestResponse)
async def get_request(request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Request).filter(Request.id == request_id))
    request = result.scalars().first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

# 4. Обновить заявку (оператор правит данные или меняет статус)
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

# 5. Заглушка для AI-генерации ответа
@app.post("/api/ai/generate-answer")
async def generate_ai_answer(text: str):
    # TODO: Connect to LLM here
    return {"suggested_answer": f"Уважаемый клиент! Мы получили ваше сообщение: '{text[:20]}...'. Наши инженеры уже работают."}