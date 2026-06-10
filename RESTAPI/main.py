from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI()

# Temporary storage
users = {}


# User model
class User(BaseModel):
    id: int
    name: str
    age: int


# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to User API"}


# Create User
@app.post("/users")
def create_user(user: User):

    if user.id in users:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    users[user.id] = user

    return {
        "message": "User created successfully",
        "user": user
    }


# Get User
@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]


# Update User
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Ensure the ID in the path matches the ID in the body
    if user_id != user.id:
        raise HTTPException(
            status_code=400,
            detail="User ID in path and body do not match"
        )

    users[user_id] = user

    return {
        "message": "User updated successfully",
        "user": user
    }


# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    deleted_user = users.pop(user_id)

    return {
        "message": "User deleted successfully",
        "deleted_user": deleted_user
    }