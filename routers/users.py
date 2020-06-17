from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import interaction, schemas
from db.database import get_db

router = APIRouter()


#@router.get("/")
#async def get_users_list():
#    return {"users_count": 0}


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = interaction.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    result = interaction.create_user(db=db, user=user)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="Phone number must contain 10 digit.")


@router.get("/", response_model=List[schemas.User])
def get_users_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = interaction.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_uuid}", response_model=schemas.User)
def get_user(user_uuid: str, db: Session = Depends(get_db)):
    db_user = interaction.get_user(db, user_uuid=user_uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
