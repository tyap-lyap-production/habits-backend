from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from uuid import UUID
from app.schemas.habit import Habit, HabitUpdate, HabitBase
from app.schemas.goal import Goal, GoalBase, GoalUpdate
from app.schemas.user import User, UserBase, UserCreate

from app.models.habit import Habit as HabitModel
from app.models.goal import Goal as GoalModel
from app.models.user import User as UserModel

from app.db.base import get_db, engine

router = APIRouter()


# Create a new habit
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    is_exist = db.query(UserModel).filter(UserModel.email == user.email).first()
    if is_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User exist")
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Read all habits
@router.post("/login", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    is_exist = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .filter(UserModel.password == user.password)
        .first()
    )
    if not is_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return is_exist
