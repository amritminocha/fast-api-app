from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class ServiceException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


# def handle_service_exception(request: Request, exc: ServiceException):
#     return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
