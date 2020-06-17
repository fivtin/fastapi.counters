from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Text, SmallInteger, Numeric, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(length=36), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String(length=10), unique=True)
    hashed_password = Column(String(length=60))
    is_active = Column(Boolean, default=True)

#    items = relationship("Item", back_populates="owner")


#class Item(Base):
#    __tablename__ = "items"
#
#    id = Column(Integer, primary_key=True, index=True)
#    title = Column(String, index=True)
#    description = Column(String, index=True)
#    owner_id = Column(Integer, ForeignKey("users.id"))
#
#    owner = relationship("User", back_populates="items")


class Counter(Base):
    __tablename__ = "counters"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(SmallInteger)
    name = Column(String(length=32), unique=True)
    description = Column(String(length=256))

    registry = relationship("Registry", back_populates="counter")

    # parent_id = Column(Integer, ForeignKey('parent.id'))
    # children = relationship("Child", back_populates="parent")
    # children = relationship("Child", backref="parent")



class Registry(Base):
    __tablename__ = "registry"

    id = Column(Integer, primary_key=True, index=True)
    counter_id = Column(Integer, ForeignKey("counters.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    create_dt = Column(DateTime)
    # datetime = Column(DateTime)
    # dt_create = Column(DateTime, server_default=func.now())
    value = Column(Numeric(precision=8, scale=2))
    comment = Column(String(length=256))

    counter = relationship("Counter", back_populates="registry")


#class Test(Base):
#    __tablename__ = "test"
#    id = Column(Integer, primary_key=True, index=True)
#    dt = Column(DateTime, server_default=func.now())