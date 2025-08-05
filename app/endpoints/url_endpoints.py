from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from app.schemas.url_schemas import URLCreate, URLRead
from app.session import get_db
from app.services.url_services import create_short_url, get_url_by_short_id
from datetime import datetime

router = APIRouter()

@router.post("/shorten", response_model=URLRead)
async def shorten_url(data: URLCreate, db: AsyncSession = Depends(get_db)):
    return await create_short_url(data.original_url, db)

@router.get("/{short_id}")
async def redirect_to_url(short_id: str, db: AsyncSession = Depends(get_db)):
    url = await get_url_by_short_id(short_id, db)
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if url.expired_at and url.expired_at < datetime.now():
        raise HTTPException(status_code=410, detail="Short URL expired")

    return RedirectResponse(url.original_url)
