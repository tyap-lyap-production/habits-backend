from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.habit import Habit, HabitCreate, HabitUpdate
from app.models.habit import Habit as HabitModel
from app.db.base import get_db

router = APIRouter()

# Create a new habit
@router.post("/", response_model=Habit, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = HabitModel(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

# Read all habits
@router.get("/", response_model=list[Habit])
def get_habits(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(HabitModel).offset(skip).limit(limit).all()

# Read a single habit by ID
@router.get("/{habit_id}", response_model=Habit)
def get_habit(habit_id: UUID, db: Session = Depends(get_db)):
    habit = db.query(HabitModel).filter(HabitModel.habit_id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return habit

# Update a habit
@router.put("/{habit_id}", response_model=Habit)
def update_habit(habit_id: UUID, habit_update: HabitUpdate, db: Session = Depends(get_db)):
    db_habit = db.query(HabitModel).filter(HabitModel.habit_id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    
    for key, value in habit_update.dict(exclude_unset=True).items():
        setattr(db_habit, key, value)
    
    db.commit()
    db.refresh(db_habit)
    return db_habit

# Delete a habit
@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: UUID, db: Session = Depends(get_db)):
    db_habit = db.query(HabitModel).filter(HabitModel.habit_id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    
    db.delete(db_habit)
    db.commit()
    return
