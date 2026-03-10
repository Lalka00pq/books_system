from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=1, description="Password")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
