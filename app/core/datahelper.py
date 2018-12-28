from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from models import Base
from models import Brand
from models import Car
from models import Category
from models import User


class DataHelper:

    def __init__(self):
        self.engine = create_engine('postgresql:///catalog')
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        return True

    def import_categories(self, file_name):
        for brand_name in open(file_name, 'r').readlines():
            if self.get_category_id(brand_name) is None:
                self.create_category({
                    'name': brand_name
                })

    def import_brands(self, file_name):
        for brand_name in open(file_name, 'r').readlines():
            if self.get_brand_id(brand_name) is None:
                self.create_brand({
                    'name': brand_name
                })

    def create_user(self, user_session):
        new_user = User(name=user_session['username'], email=user_session['email'],
                        picture=user_session['picture'])
        self.session.add(new_user)
        self.session.commit()
        user = self.session.query(User).filter_by(email=user_session['email']).one()
        self.session.close()
        return user.id

    def get_user_info(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).one()
        return user

    def get_user_id(self, user_email):
        try:
            user = self.session.query(User).filter_by(email=user_email).one()
            return user.id
        except SQLAlchemyError:
            return None

    def create_category(self, category_data):
        new_category = Category(
            name=category_data['name'],
        )
        self.session.add(new_category)
        self.session.commit()
        category = self.session.query(Category).filter_by(
            name=category_data['name'],
        ).one()
        self.session.close()
        return category.id

    def get_category_id(self, category_name):
        try:
            user = self.session.query(Category).filter_by(
                name=category_name
            ).one()
            return user.id
        except SQLAlchemyError:
            return None

    def create_brand(self, brand_data):
        new_brand = Brand(
            name=brand_data['name'],
        )
        self.session.add(new_brand)
        self.session.commit()
        brand = self.session.query(Brand).filter_by(
            name=brand_data['name'],
        ).one()
        self.session.close()
        return brand.id

    def get_brand_id(self, brand_name):
        try:
            user = self.session.query(Brand).filter_by(
                name=brand_name
            ).one()
            return user.id
        except SQLAlchemyError:
            return None

    def create_car(self, car_data):
        new_car = Car(
            model=car_data['model'],
            description=car_data['description'],
            price=car_data['price'],
            category_id=car_data['category_id'],
            brand_id=car_data['brand_id'],
            user_id=car_data['user_id'],
        )
        self.session.add(new_car)
        self.session.commit()
        car = self.session.query(Car).filter_by(
            model=car_data['model'],
            user_id=car_data['user_id'],
        ).one()
        self.session.close()
        return car.id

    def get_car_id(self, car_model, user_id):
        try:
            user = self.session.query(Car).filter_by(
                model=car_model,
                user_id=user_id
            ).one()
            self.session.close()
            return user.id
        except SQLAlchemyError:
            return None

    def get_car_info(self, car_id):
        car = self.session.query(Car).filter_by(id=car_id).one()
        return car

    def delete_car(self, car_id, user_id):
        try:
            car = self.session.query(Car).filter_by(
                id=car_id,
                user_id=user_id
            ).one()
            car_id = car.id
            if car_id > 0:
                self.session.delete(car)
                self.session.commit()
            self.session.close()
            return car_id
        except SQLAlchemyError:
            return None

    def get_categories(self):
        return self.session.query(Category).order_by('name').all()

    def get_brands(self):
        return self.session.query(Brand).order_by('name').all()
