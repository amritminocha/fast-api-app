from fastapi import APIRouter
from app.schemas.user_schemas import UserCreate, UserRead
from app.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.services.user_services import create_user, get_user_from_email

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(user, db)


@router.get("/{email}", response_model=UserRead)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await get_user_from_email(email, db)