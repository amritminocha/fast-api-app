from app.exceptions.exceptions import ServiceException
from app.schemas.user_schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
import uuid
from app.locks.user_lock import get_email_lock

async def create_user(user: UserCreate, db: AsyncSession):
    lock = get_email_lock(user.email)
    async with lock:
        existing_user = await get_user_from_email(user.email, db)
        if existing_user:
            raise ServiceException(status_code=400, detail="User already exists")

        new_user = User(
            id=uuid.uuid4(),
            username=user.username,
            email=user.email,
            password=user.password
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user



async def get_user_from_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()