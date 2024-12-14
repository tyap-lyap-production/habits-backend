from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from uuid import UUID
from app.schemas.habit import Habit, HabitUpdate, HabitBase
from app.schemas.goal import Goal, GoalBase, GoalUpdate
from app.schemas.user import User, UserBase

from app.models.habit import Habit as HabitModel
from app.models.goal import Goal as GoalModel
from app.models.user import User as UserModel

from app.db.base import get_db, engine

router = APIRouter()


# Create a new habit
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_habit(user_id: UUID, habit: HabitBase, db: Session = Depends(get_db)):
    print(habit.goal.dict())
    db_goal = GoalModel(
        unit_type=habit.goal.unitType,
        value=habit.goal.value,
        periodicity=habit.goal.periodicity,
    )

    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    is_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not is_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_habit = HabitModel(
        user_id=user_id,
        name=habit.name,
        createDate=habit.createDate,
        goal_id=db_goal.id,
        status=int(habit.status),
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


# Read all habits


@router.get("/")
def get_habits(user_id: UUID, db: Session = Depends(get_db)):
    is_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    print(is_user)
    if not is_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    habits = (
        db.query(HabitModel, GoalModel)
        .filter(HabitModel.goal_id == GoalModel.id)
        .filter(HabitModel.user_id == user_id)
        .all()
    )
    print("habits", habits)

    # Convert to a serializable format
    results = [
        {"habit": habit.__dict__, "goal": goal.__dict__} for habit, goal in habits
    ]
    print("results", results)

    # Remove SQLAlchemy instance state keys (e.g., '_sa_instance_state')
    for result in results:
        result["habit"].pop("_sa_instance_state", None)
        result["goal"].pop("_sa_instance_state", None)

    return results


# Update a habit
@router.put("/{habit_id}")
def update_habit(
    habit_id: UUID, habit_update: HabitUpdate, db: Session = Depends(get_db)
):
    db_habit = db.query(HabitModel).filter(HabitModel.id == habit_id).first()
    if not db_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
        )

    db_goal = db.query(GoalModel).filter(GoalModel.id == db_habit.goal_id).first()

    if habit_update.goal:
        goal_update = habit_update.goal
        goal_update = goal_update.dict(exclude_unset=True)
        for key, value in goal_update.items():
            setattr(db_goal, key, value)
    habit_update = habit_update.dict(exclude_unset=True)

    habit_update.pop("goal", None)
    print(habit_update)
    for key, value in habit_update.items():
        setattr(db_habit, key, value)

    db.commit()
    db.refresh(db_goal)
    db.refresh(db_habit)

    return db_habit


# Delete a habit
@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: UUID, db: Session = Depends(get_db)):
    db_habit = db.query(HabitModel).filter(HabitModel.id == habit_id).first()
    if not db_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
        )

    db.delete(db_habit)
    db.commit()
    return
