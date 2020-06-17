from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db import interaction, schemas
from db.database import get_db

router = APIRouter()


# добавляем запись в реестр показаний
@router.post("/", response_model=schemas.Registry)
def post_append_to_registry(registry: schemas.RegistryCreate, db: Session = Depends(get_db)):
    # проверяем входные данные (наличие счетчика с указанным ID)
    db_counter = interaction.get_counter(db, counter_id=registry.counter_id)
    if db_counter:
        # счетчик обнаружен - выполняем запись
        result = interaction.append_registry(db=db, registry=registry)
        if result:
            return result
        else:
            raise HTTPException(status_code=400, detail="Registry entry not added.")
    else:
        raise HTTPException(status_code=400, detail="In the data, the conter ID does not correspond to any known.")


# возращаем последнее показание счётчика или на указанную дату, переданную в Query
@router.get("/{counter_id}", response_model=schemas.RegistryLast)
def get_counter_last_reading(counter_id: int, date: str = Query(None, regex="^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"), db: Session = Depends(get_db)): # Warning!!! Query use add param "regex" for validate date value.
    registry = interaction.get_registry_on_date(db, counter_id=counter_id, date=date)
    print(registry)
    return registry



# возращаем список показаний счётчика (количество) или начиная с указанной даты, если она передана
@router.get("/reading/{counter_id}", response_model=List[schemas.Registry])
def get_counter_list_readings(counter_id: int, limit: int = 100, date: str = Query(None, regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"), db: Session = Depends(get_db)):
    results = interaction.counter_list_reading(db, counter_id, limit, date)
    return results


# удаляем запись из реестра по её ID
@router.delete("/{registry_id}")
def delete_registry(registry_id: int, db: Session = Depends(get_db)):
    if interaction.delete_registry_by_id(db, registry_id):
        return {"result": "delete", "id": registry_id}
    else:
        raise HTTPException(status_code=404, detail="Registry not found.")


# возвращаем среднне потребление за указанный период для счетчика, даты передаются в Query
@router.get("/average/{counter_id}", response_model=schemas.RegistryAvg)
def get_average_consumtion(counter_id: int, start: str = Query(None, regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"), finish: str = Query(None, regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"), db: Session = Depends(get_db)):
    return interaction.average_consumtion(db, counter_id, start, finish)


# возвращаем разницу показаний на указанный период для счетчика, даты передаются в Query
@router.get("/difference/{counter_id}", response_model=schemas.RegistryDiff)
def get_difference_in_readings(counter_id: int, start: str = Query(None, regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"), finish: str = Query(None, regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"), db: Session = Depends(get_db)):
    return interaction.difference_in_readings(db, counter_id, start, finish)





# возращаем 
#@router.get("/{id}", response_model=schemas.registry)
#def get_registry(id: int, db: Session = Depends(get_db)):
#    db_registry = interaction.get_registry(db, registry_id=id)
#    if db_registry is None:
#        raise HTTPException(status_code=404, detail="Registry not found.")
#    return db_registry
#
#
#@router.get("/detail/{id}", response_model=schemas.registryDetail)
#def get_registry_detail(id: str, db: Session = Depends(get_db)):
#    db_registry = interaction.get_registry_detail(db, registry_id=id)
#    if db_registry is None:
#        raise HTTPException(status_code=404, detail="Registry not found.")
#    return db_registry
