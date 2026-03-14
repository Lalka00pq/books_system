from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import verify_password
from app.core.exceptions import UnauthorizedError
from app.schemas.auth import LoginRequest


class AuthService:
    @staticmethod
    async def authenticate_user(db: AsyncSession, login_data: LoginRequest) -> User:
        stmt = select(User).where(User.email == login_data.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise UnauthorizedError("Incorrect email or password")

        if not verify_password(login_data.password, user.password_hash):
            raise UnauthorizedError("Incorrect email or password")

        return user
