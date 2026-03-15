from typing import Any
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import create_access_token, revoke_token
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> Any:
    user = await AuthService.authenticate_user(db, login_data)
    access_token = create_access_token(subject=user.id)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        max_age=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
        secure=False,
        path="/",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


security = HTTPBearer()


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
) -> dict:
    token = credentials.credentials
    revoke_token(token)

    return {"message": "Successfully logged out"}
