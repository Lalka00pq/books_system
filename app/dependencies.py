from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.user import User
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    user_id_str = decode_access_token(token)
    
    stmt = select(User).where(User.id == user_id_str)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise UnauthorizedError("User not found")
        
    return user
