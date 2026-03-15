from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.user import User
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedError

security = HTTPBearer(auto_error=False)


async def get_token_from_request(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    if credentials and credentials.credentials:
        return credentials.credentials

    token = request.cookies.get("access_token")
    if not token:
        raise UnauthorizedError("Not authenticated")

    if token.startswith("Bearer "):
        return token[len("Bearer "):]

    return token


async def get_current_user(
    token: str = Depends(get_token_from_request),
    db: AsyncSession = Depends(get_db)
) -> User:
    user_id_str = decode_access_token(token)

    stmt = select(User).where(User.id == user_id_str)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedError("User not found")

    return user
