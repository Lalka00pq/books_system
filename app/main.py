from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.config import settings
from app.core.exceptions import AppException
from app.schemas.error import ErrorResponse, ErrorDetail

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Unified Error Format Handler
def create_error_response(code: int, type: str, message: str) -> JSONResponse:
    error_data = ErrorResponse(
        error=ErrorDetail(code=code, type=type, message=message)
    )
    return JSONResponse(
        status_code=code,
        content=error_data.model_dump()
    )

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return create_error_response(exc.code, exc.error_type, exc.message)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return create_error_response(
        exc.status_code, 
        "HTTP_ERROR", 
        str(exc.detail)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    message = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in errors])
    return create_error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY, 
        "VALIDATION_ERROR", 
        message
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the exception here in production
    return create_error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        "INTERNAL_SERVER_ERROR", 
        "An unexpected error occurred"
    )

# Include API Router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
