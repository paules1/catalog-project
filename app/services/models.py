from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Cars(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    model = Column(String(250), nullable=False)
    description = Column(String(1024), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship(Brand)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)