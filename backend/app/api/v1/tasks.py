from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy import select 
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_user, get_db

from backend.app.models.user import UserModel
from backend.app.models.task import TaskModel
from backend.app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from backend.app.models.category import CategoryModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskResponse])
async def get_user_tasks(current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):


    result = await db.execute(select(TaskModel).where(TaskModel.user_id == current_user.id).options(selectinload(TaskModel.category)))  # Eager loading - When you go get the Tasks, fetch their Categories at the same time.
    return result.scalars().all()

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_user_task( task_in: TaskCreate , current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    if task_in.category_id and task_in.category_id != 0:
        category_check = await db.execute(select(CategoryModel).where( CategoryModel.id == task_in.category_id, CategoryModel.user_id == current_user.id) )
        
        if not category_check.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid category or unauthorized access"
            )


    new_task = TaskModel(
        title = task_in.title,
        description = task_in.description,
        category_id = task_in.category_id if task_in.category_id != 0 else None,
        user_id = current_user.id
    )

    db.add(new_task)
    await db.commit()

    result = await db.execute(select(TaskModel).where(TaskModel.id == new_task.id).options(selectinload(TaskModel.category)))
    return result.scalars().one()

@router.put("/{task_id}", response_model=TaskResponse)
async def update_user_task( task_id : int , task_in : TaskUpdate , current_user : UserModel = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    # Verify task exists and belongs to this user before updating
    query = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user.id)
    result = await db.execute(query)
    old_task = result.scalars().first()

    if not old_task:
        raise HTTPException(status_code=404 , detail="Task not found or unauthorized")

    merged_data = {
        "title": old_task.title,
        "description": old_task.description,
        "is_completed": old_task.is_completed,
        "category_id": old_task.category_id,
        "user_id": current_user.id
    }

    #Update field dynamically if they were provided by client
    update_data = task_in.model_dump(exclude_unset=True)
    

    if "category_id" in update_data:
        if update_data["category_id"] == 0 or update_data["category_id"] is None:
            update_data["category_id"] = None
        else:
            #  Verify the category belongs strictly to the logged-in user on updates
            category_check = await db.execute(
                select(CategoryModel).where(
                    CategoryModel.id == update_data["category_id"],
                    CategoryModel.user_id == current_user.id
                )
            )
            if not category_check.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Invalid category or unauthorized access"
                )
            

    merged_data.update(update_data)
    await db.delete(old_task)

    new_task = TaskModel(**merged_data)
    db.add(new_task)
    await db.commit()
    result = await db.execute( select(TaskModel) .where(TaskModel.id == new_task.id).options(selectinload(TaskModel.category)))
    return result.scalars().first()
    
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_task( task_id : int , current_user : UserModel = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    query = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user.id)
    result = await db.execute(query)
    db_task = result.scalars().first()

    if not db_task:
        raise HTTPException(status_code=404 , details="Task not found or unauthorized")

    await db.delete(db_task)
    await db.commit()
    return None


