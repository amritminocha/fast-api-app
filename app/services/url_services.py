from sqlalchemy.ext.asyncio import AsyncSession
from app.models.url import URL
import random
import string
from sqlalchemy import select
from datetime import datetime, timedelta

def generate_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

async def create_short_url(original_url: str, db: AsyncSession):
    short_id = generate_short_id()
    while await get_url_by_short_id(short_id, db):
        short_id = generate_short_id()

    url = URL(original_url=original_url, short_id=short_id, expired_at=datetime.now() + timedelta(seconds=30))
    db.add(url)
    await db.commit()
    return url

async def get_url_by_short_id(short_id: str, db: AsyncSession):
    result = await db.execute(select(URL).where(URL.short_id == short_id))
    return result.scalar_one_or_none()
