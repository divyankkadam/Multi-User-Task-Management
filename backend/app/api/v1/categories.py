from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db, get_current_user
from backend.app.models.user import UserModel
from backend.app.models.category import CategoryModel
from backend.app.schemas.category import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=list[CategoryResponse])
async def get_categories( db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user) ):
    result = await db.execute(select(CategoryModel).where(CategoryModel.user_id == current_user.id))
    return result.scalars().all()


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category( category_in: CategoryCreate, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user) ):
    
    # Prevent duplicate categories
    existing_category = await db.execute(select(CategoryModel).where(CategoryModel.name == category_in.name), CategoryModel.user_id == current_user.id)


    if existing_category.scalars().first():
        raise HTTPException(status_code=400, detail="Category already exists")

    
    new_category = CategoryModel(name=category_in.name, user_id=current_user.id)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


@router.delete("{/category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id : int , current_user : UserModel = Depends(get_current_user) ,  db : AsyncSession = Depends(get_db)):

    query = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.user_id == current_user.id)
    result = await db.execute(query)
    category  = result.scalars().first()

    if not category:
        raise HTTPException(status_code=404 , detail="Category not found or unauthorized ")

    await db.delete(category)
    await db.commit()
    return None