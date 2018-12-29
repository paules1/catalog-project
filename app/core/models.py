from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import json

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
    cars = relationship('Car',
                        order_by="desc(Car.model)",
                        primaryjoin="Car.category_id==Category.id"
                        )

    @hybrid_property
    def car_count(self):
        return len(self.cars)

    @hybrid_property
    def cars_serialize(self):
        items = []
        for car in self.cars:
            items.append(car.serialize)
        return items

    @property
    def serialize(self):
        return {
            self.name: {
                'car_count': self.car_count,
                'car_list': self.cars_serialize
            }
        }


class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    model = Column(String(250), nullable=False)
    description = Column(String(1024), nullable=False)
    price = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship(Brand)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'model': self.model,
            'description': self.description,
            'price': self.price,
            'brand': self.brand.name,
            'contact': self.user.email
        }

