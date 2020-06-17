from typing import List
from datetime import datetime

from pydantic import BaseModel


#class ItemBase(BaseModel):
#    title: str
#    description: str = None
#
#
#class ItemCreate(ItemBase):
#    pass
#
#
#class Item(ItemBase):
#    id: int
#    owner_id: int
#
#    class Config:
#        orm_mode = True

class UserBase(BaseModel):
    email: str
    phone: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: str
    is_active: bool
#    items: List[Item] = []

    class Config:
        orm_mode = True


class CounterBase(BaseModel):
    type: int
    name: str
    description: str


class CounterCreate(CounterBase):
    pass


class Counter(CounterBase):
    id: int
    
    class Config:
        orm_mode = True


class CounterDetail(Counter):
    last_date: int
    last_value: int


class RegistryBase(BaseModel):
    counter_id: int
    user_id: int
    create_dt: datetime
    value: int
    comment: str

class RegistryCreate(RegistryBase):
    pass


class Registry(RegistryBase):
   id: int
   
   class Config:
       orm_mode = True


class RegistryDetail(Registry):
    pass


class RegistryLast(Registry):
    pass


class RegistryAvg(BaseModel):
    counter: Counter
    start: Registry
    finish: Registry
    hours: int
    difference: int
    average: float


class RegistryDiff(BaseModel):
    counter: Counter
    start: Registry = None
    finish: Registry = None
    difference: int = 0