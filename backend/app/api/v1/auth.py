from fastapi import APIRouter , Depends , HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db , get_current_user
from backend.app.core.security import get_password_hash, verify_password, create_access_token


from backend.app.models.user import UserModel
from backend.app.schemas.user import CreateUser, UserResponse, Token
from backend.app.schemas.task import TaskCreate, TaskResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: CreateUser , db: AsyncSession = Depends(get_db)):

    # Check if user already exists
    existing_user = await db.execute(select(UserModel).where((UserModel.username ==user_in.username ) | (UserModel.email == user_in.email)))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400 , detail="Username or Email already Registered")

    hashed_password = get_password_hash(user_in.password)
    
    new_user = UserModel(
        username = user_in.username,
        email = user_in.email,
        password = hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.username == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)

    access_token = create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}







