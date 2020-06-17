import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


# =============================================================================================================================


def get_user(db: Session, user_uuid: str):
    return db.query(models.User).filter(models.User.uuid == user_uuid).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    if len(user.phone) == 10:
        db_user = models.User(uuid=uuid.uuid4(), email=user.email, phone=user.phone, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return False


# =============================================================================================================================


def create_counter(db: Session, counter: schemas.CounterCreate):
    db_counter = models.Counter(type=counter.type, name=counter.name, description=counter.description)
    db.add(db_counter)
    db.commit()
    db.refresh(db_counter)
    return db_counter


def get_counter(db: Session, counter_id: int):
    return db.query(models.Counter).filter(models.Counter.id == counter_id).first()


def get_counters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Counter).order_by(models.Counter.id).offset(skip).limit(limit).all()


#def get_counter_detail(db: Session, counter_id: int):
#    db_counter = db.query(models.Counter).filter(models.Counter.id == counter_id).first()
#    db_registry = db.query(models.Registry).filter(models.Registry.counter_id == counter_id).order_by(models.Registry.id.desc()).first()
#    # НИЧЕГО НЕ ВОЗВРАЩАЕТ


def get_counters_by_type_id(db: Session, type_id: int):
    return db.query(models.Counter).filter(models.Counter.type == type_id).all()


def get_counter_by_name(db: Session, counter_name: str):
    return db.query(models.Counter).filter(models.Counter.name == counter_name).first()


# =============================================================================================================================


def append_registry(db: Session, registry: schemas.RegistryCreate):
    db_registry = models.Registry(counter_id=registry.counter_id, user_id=registry.user_id, create_dt=registry.create_dt, value=registry.value, comment=registry.comment)
    db.add(db_registry)
    db.commit()
    db.refresh(db_registry)
    return db_registry


def get_registry_on_date(db: Session, counter_id: int, date):
    if date:
        # есть дата - возвращаем значение на эту дату или раньше
        return db.query(models.Registry).filter(models.Registry.counter_id == counter_id, models.Registry.create_dt <= date).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).first()
    else:
        # нет даты - нужна последняя запись
        return db.query(models.Registry).filter(models.Registry.counter_id == counter_id).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).first()


def counter_list_reading(db: Session, counter_id: int, limit, date):
    if date:
        # есть дата - возвращаем значение на эту дату или раньше
        return db.query(models.Registry).filter(models.Registry.counter_id == counter_id, models.Registry.create_dt <= date).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(limit).all()
    else:
        # нет даты - нужна последняя запись
        return db.query(models.Registry).filter(models.Registry.counter_id == counter_id).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(limit).all()



def delete_registry_by_id(db: Session, registry_id: int):
    registry = db.query(models.Registry).get(registry_id)
    if registry:
        db.delete(registry)
        #models.Registry.query.filter_by(id=registry_id).delete()
        db.commit()
        return True
    else:
        return False


def average_consumtion(db: Session, counter_id: int, start, finish):
    # наличие показаний и их дат обязательно для расчета среднего расхода, поэтому они обязательны
    # при отсутствии даты окончания используем последнее доступное значение, при его отсутствии операция отменяется
    # при отсутствии даты начала используем самое раннее значение, при его отсутствии операция отменяется
    # анализ принятых дат на None
    if start == None:
        start = '1980-01-01'
    if finish == None:
        finish = '2099-12-31'
    counter = db.query(models.Counter).filter(models.Counter.id == counter_id).first()
    # получение разницы крайних значений, вычисление продолжительности времени между ними
    # расчет среднего потребления в час (finish - start) / time
    registry_start = db.query(models.Registry).filter(models.Registry.counter_id == counter_id, models.Registry.create_dt <= start).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(1).first()
    if registry_start == None:
        registry_start = db.query(models.Registry).filter(models.Registry.counter_id == counter_id).order_by(models.Registry.create_dt.asc(), models.Registry.id.asc()).limit(1).first()
    if registry_start:
        registry_finish = db.query(models.Registry).filter(models.Registry.counter_id == counter_id, models.Registry.create_dt <= finish).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(1).first()
        if registry_finish == None:
            registry_finish = db.query(models.Registry).filter(models.Registry.counter_id == counter_id).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(1).first()
    if registry_start == None or registry_finish == None:
        raise HTTPException(status_code=400, detail="Unable to complete operation.")
    # расчитываем промежуток премени
    hours = (registry_finish.create_dt - registry_start.create_dt).days * 24
    if hours == 0:
        average = 0
        diff = 0
    else:
        diff = registry_finish.value - registry_start.value
        average = round(diff / hours, 4)
    return {"counter": counter, "start": registry_start, "finish": registry_finish, "hours": hours, "difference": diff, "average": average}


def difference_in_readings(db: Session, counter_id: int, start, finish):
    # анализ принятых дат на None
    if start == None:
        start = '1980-01-01'
    if finish == None:
        finish = '2099-12-31'
    counter = db.query(models.Counter).filter(models.Counter.id == counter_id).first()
    # при отсутствии даты начала берется дата ранее, а при её отсутствии считаем что предыдущее показание равно 0
    # при отсутствии даты окончания берем последее доступное значение, а при его отсутствии считаем что нет ни одного значения
    registry_start = db.query(models.Registry).filter(models.Registry.counter_id == counter_id, models.Registry.create_dt <= start).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(1).first()
    registry_finish = db.query(models.Registry).filter(models.Registry.counter_id == counter_id, models.Registry.create_dt <= finish).order_by(models.Registry.create_dt.desc(), models.Registry.id.desc()).limit(1).first()
    if registry_start == None:
        if registry_finish == None:
            diff = 0
        else:
            diff = registry_finish.value
    else:
        if registry_finish == None:
            diff = registry_start.value
        else:
            diff = registry_finish.value - registry_start.value
    return {"counter": counter, "start": registry_start, "finish": registry_finish, "difference": diff}




# =============================================================================================================================


#def get_items(db: Session, skip: int = 0, limit: int = 100):
#    return db.query(models.Item).offset(skip).limit(limit).all()
#
#
#def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#    db_item = models.Item(**item.dict(), owner_id=user_id)
#    db.add(db_item)
#    db.commit()
#    db.refresh(db_item)
#    return db_item