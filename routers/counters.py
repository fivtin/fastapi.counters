from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import interaction, schemas
from db.database import get_db

router = APIRouter()


@router.get("/type/{type_id}", response_model=List[schemas.Counter])
def get_counters_by_type_id(type_id: int, db: Session = Depends(get_db)):
    counters = interaction.get_counters_by_type_id(db, type_id=type_id)
    return counters


@router.get("/types")
def get_counter_types():
    return [
        {"id": 1, "name": "power", "title": "Электроэнергия"},
        {"id": 2, "name": "power2","title": "Электроэнергия (2ст.)"},
        {"id": 3, "name": "water_cold", "title": "Вода хол."},
        {"id": 4, "name": "water_hot", "title": "Вода гор."},
        {"id": 6, "name": "gas", "title": "Газ"}
    ]


@router.post("/", response_model=schemas.Counter)
def post_create_counter(counter: schemas.CounterCreate, db: Session = Depends(get_db)):
    db_counter = interaction.get_counter_by_name(db, counter_name=counter.name)
    if db_counter:
        raise HTTPException(status_code=400, detail="Counter name already registered.")
    result = interaction.create_counter(db=db, counter=counter)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="Counter don`t create.")


@router.get("/{counter_id}", response_model=schemas.Counter)
def get_counter(counter_id: int, db: Session = Depends(get_db)):
    db_counter = interaction.get_counter(db, counter_id=counter_id)
    if db_counter is None:
        raise HTTPException(status_code=404, detail="Counter not found.")
    return db_counter


@router.get("/", response_model=List[schemas.Counter])
def get_counters_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    counters = interaction.get_counters(db, skip=skip, limit=limit)
    return counters



#@router.get("/detail/{counter_id}", response_model=schemas.CounterDetail)
#def get_counter_detail(counter_id: int, db: Session = Depends(get_db))
#    db_counter = interaction.get_counter_detail(db, counter_id=counter_id)
#    if db_counter is None:
#        raise HTTPException(status_code=404, detail="Counter not found.")
#    return db_counter
