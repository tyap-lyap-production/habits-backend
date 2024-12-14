import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import SessionLocal, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import date


# Fixture to set up the in-memory database for each test
@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session for each test
    db = SessionLocal()
    yield db  # This will be used in the test function
    
    # Rollback the transaction after the test is done
    db.rollback()
    db.close()

    # Drop the tables after the test is done
    Base.metadata.drop_all(bind=engine)
# Create TestClient instance with app
client = TestClient(app)

def test_create_user():
    user_data = {
        "email": f"testuser{str(uuid4())}@example.com",
        "password": "testpassword123"
    }
    response = client.post("/user/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]


def test_create_user_already_exists():
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    # Create the user first
    client.post("/user/", json=user_data)

    # Try to create the user again
    response = client.post("/user/", json=user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User exist"


def test_user_login():
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    # Ensure the user exists first
    client.post("/user/", json=user_data)

    # Log the user in
    response = client.post("/user/login", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]


def test_user_login_fail():
    user_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/user/login", json=user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

from app.schemas.habit import HabitBase, HabitUpdate
from app.schemas.goal import GoalBase
from app.schemas.status import HabitStatus


def test_create_habit():
    user_data = {
        "email": f"testuser{str(uuid4())}@example.com",
        "password": "testpassword123"
    }
    # Create user if it doesn't exist
    user = client.post("/user/", json=user_data).json()
    print(user)

    # Prepare habit data
    habit_data = {
        "name": "Test Habit",
        "createDate": "2024-12-14",
        "goal": {
            "value": 10,
            "unitType": "kg",
            "periodicity": "dayli"
        },
        "status": 0
    }

    # Create habit
    print(habit_data)
    response = client.post("/habits/", params={"user_id": user["user_id"]}, json=habit_data)
    print(response.text)
    assert response.status_code == 201
    habit = response.json()
    assert habit["name"] == habit_data["name"]
    assert habit["status"] == habit_data["status"]


def test_get_habits():
    # Ensure the user exists first
    user_data = {
        "email": f"testuser{str(uuid4())}@example.com",
        "password": "testpassword123"
    }
    user = client.post("/user/", json=user_data).json()

    # Create habit for the user
    habit_data = {
        "name": "Test Habit",
        "createDate": str(date.today()),
        "goal": {
            "value": 10,
            "unitType": "kg",
            "periodicity": "dayli"
        },
        "status": 0
    }

    # Create habit
    client.post("/habits/", params={"user_id": user["user_id"]}, json=habit_data)

    # Retrieve habits for the user
    response = client.get("/habits/", params={"user_id": user["user_id"]})
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) > 0


def test_update_habit():
    # Create a user and a habit
    user_data = {
        "email": f"testuser{str(uuid4())}@example.com",
        "password": "testpassword123"
    }
    user = client.post("/user/", json=user_data).json()

    # Create habit for the user
    habit_data = {
        "name": "Test Habit",
        "createDate": str(date.today()),
        "goal": {
            "value": 10,
            "unitType": "kg",
            "periodicity": "dayli"
        },
        "status": 0
    }

    # Create habit
    response = client.post("/habits/", params={"user_id": user["user_id"]}, json=habit_data).json()
    

    habit_id = response["id"]

    # Update the habit
    update_data = { 
        "name": "Updated Habit",
        "goal": {
            "value": 15,
            "unitType": "kg",
            "periodicity": "dayli"
        },
        "status": 1
    }
    response = client.put(f"/habits/{habit_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]
    assert response.json()["status"] == update_data["status"]


def test_delete_habit():
    # Create a user and a habit
    user_data = {
        "email": f"testuser{str(uuid4())}@example.com",
        "password": "testpassword123"
    }
    user = client.post("/user/", json=user_data).json()

    # Create habit for the user
    habit_data = {
        "name": "Test Habit",
        "createDate": str(date.today()),
        "goal": {
            "value": 10,
            "unitType": "kg",
            "periodicity": "dayli"
        },
        "status": 0
    }

    # Create habit
    response = client.post("/habits/", params={"user_id": user["user_id"]}, json=habit_data)
    habit_id = response.json()["id"]

    # Delete habit
    response = client.delete(f"/habits/{habit_id}")
    assert response.status_code == 204


    habit_data = {
        "name": "Test Habit",
        "createDate": str(date.today()),
        "goal": {
            "value": 10,
            "unitType": "kg",
            "periodicity": "dayli"
        },
        "status": 0
    }
    # Try to retrieve the deleted habit
    response = client.put(f"/habits/{habit_id}", json=habit_data)
    print(response.text)
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"
