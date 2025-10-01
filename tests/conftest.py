# tests/conftest.py
import asyncio
import types
import sys

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# --- If your code still imports the old path, keep this small shim. ---
# Remove this block if you've already fixed the import in your codebase.
try:
    from app.exceptions.exceptions import ServiceException as _SvcExc  # your actual exception
    mod = types.ModuleType("app.exceptions.exceptions")
    mod.ServiceException = _SvcExc
    sys.modules["app.exceptions.exceptions"] = mod
except Exception:
    pass

# Import your app bits
from app.endpoints.user_endpoints import router
from app.session import get_db
from app.models.base import Base
from app.models import user as _ensure_models_loaded  # ensure model metadata registers


# If you're on pytest-asyncio >= 0.23, set asyncio_mode=auto in pytest.ini,
# otherwise this explicit loop fixture is fine.
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    TestSessionLocal = sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def app(db_session):
    app = FastAPI()

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    app.include_router(router, prefix="/users")
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
