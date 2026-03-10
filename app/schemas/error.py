from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    code: int = Field(..., description="HTTP status code")
    type: str = Field(..., description="Error type constant")
    message: str = Field(..., description="Human-readable error message")

class ErrorResponse(BaseModel):
    error: ErrorDetail = Field(..., description="Error details container")
