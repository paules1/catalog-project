#!/usr/bin/env python

import unittest
from core.datahelper import DataHelper


class TestDataMethods(unittest.TestCase):

    def test_user_create(self):
        ds = DataHelper()
        user_id = ds.get_user_id('jd@domain.com')
        if user_id is None:
            user_id = ds.create_user({
                'username': 'John Doe',
                'email': 'jd@domain.com',
                'picture': ''
            })
        self.assertEquals(ds.get_user_info(user_id).email, 'jd@domain.com')

    def test_car_create(self):
        ds = DataHelper()
        category_id = ds.get_category_id('Convertibles')
        brand_id = ds.get_brand_id('Porsche')
        user_id = ds.get_user_id('jd@domain.com')
        car_id = ds.get_car_id('Boxster Test', user_id)
        if car_id is None:
            car_id = ds.create_car({
                'model': 'Boxster Test',
                'price': '$25,000',
                'description': '2011 Porsche Boxster, Red, Manual Transmission',
                'category': category_id,
                'brand': brand_id,
                'user_id': user_id
            })
        self.assertEquals(ds.get_car_info(car_id).model, 'Boxster Test')

    def test_delete_car(self):
        ds = DataHelper()
        user_id = ds.get_user_id('jd@domain.com')
        car_id = ds.get_car_id('Boxster Test', user_id)
        result = ds.delete_car(car_id, user_id)
        self.assertTrue(result > 0)

    def test_categories_list(self):
        ds = DataHelper()
        result = ds.get_categories()
        self.assertTrue(len(result) == 11)

    def test_brand_list(self):
        ds = DataHelper()
        result = ds.get_brands()
        self.assertTrue(len(result) == 37)

    def test_car_update(self):
        ds = DataHelper()
        user_id = ds.get_user_id('jd@domain.com')
        car_id = ds.get_car_id('Boxster Test', user_id)
        car_info = ds.get_car_info(car_id)
        car = {
            'category': car_info.category_id,
            'brand': car_info.brand_id,
            'model': car_info.model,
            'description': car_info.description,
            'price': '$27,000',
            'id': car_info.id
        }
        result = ds.update_car(car)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
