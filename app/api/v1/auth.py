from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)) -> Any:
    user = await AuthService.authenticate_user(db, login_data)
    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> dict:
    # Since we are using stateless JWT tokens, true logout relies on client-side deletion, 
    # but the assignment requires the endpoint to exist.
    return {"message": "Successfully logged out"}
