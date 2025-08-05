from fastapi import FastAPI
from app.endpoints.url_endpoints import router as url_router
from app.endpoints.user_endpoints import router as user_router
app = FastAPI()

app.include_router(url_router, prefix="/url", tags=["URL Shortener"])
app.include_router(user_router, prefix="/users", tags=["Users"])