from collections.abc import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import your database elements, security config, and models
from backend.app.db.session import AsyncSessionLocal
from backend.app.core.security import SECRET_KEY, ALGORITHM
from backend.app.models.user import UserModel
from backend.app.schemas.user import TokenData

# Defines where FastAPI looks for the token (the React frontend will hit /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Database Session Yield Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user( token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db) ) -> UserModel:
    """
    Middleware dependency that extracts the JWT, verifies validity,
    and returns the authenticated user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Query the user from PostgreSQL asynchronously
    result = await db.execute(
        select(UserModel).where(UserModel.username == token_data.username)
    )
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
        
    return user
