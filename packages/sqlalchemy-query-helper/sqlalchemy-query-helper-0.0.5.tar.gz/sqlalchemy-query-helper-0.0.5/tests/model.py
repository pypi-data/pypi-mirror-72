from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    fullname = Column(String(255))
    nickname = Column(String(255))
    timestamp = Column(DateTime)
    addresses = relationship("Adress")


class Adress(Base):
    __tablename__ = "adress"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    foos = relationship("Foo")


class Foo(Base):
    __tablename__ = "foo"
    id = Column(Integer, primary_key=True)
    foo = Column(String(255))
    adress_id = Column(Integer, ForeignKey("adress.id"))
    bars = relationship("Bar")


class Bar(Base):
    __tablename__ = "bar"
    id = Column(Integer, primary_key=True)
    bar = Column(String(255))
    foo_id = Column(Integer, ForeignKey("foo.id"))
