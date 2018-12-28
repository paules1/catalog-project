#!/usr/bin/env python

import unittest
from core.datahelper import DataHelper


class TestDataMethods(unittest.TestCase):

    def test_user_create(self):
        ds = DataHelper()
        user_id = ds.get_user_id('paules@mercabyte.com')
        if user_id is None:
            user_id = ds.create_user({
                'username': 'Paul E Villacreces',
                'email': 'paules@mercabyte.com',
                'picture': 'None'
            })
        self.assertEquals(ds.get_user_info(user_id).email, 'paules@mercabyte.com')

    def test_car_create(self):
        ds = DataHelper()
        car_id = ds.get_car_id('Boxster', 1)
        if car_id is None:
            car_id = ds.create_car({
                'model': 'Boxster',
                'price': '$25,000',
                'description': '2011 Porsche Boxster, Red, Manual Transmission',
                'category_id': 2,
                'brand_id': 29,
                'user_id': 1
            })
        self.assertEquals(ds.get_car_info(car_id).model, 'Boxster')

    def test_delete_car(self):
        ds = DataHelper()
        car_id = ds.get_car_id('Boxster', 1)
        result = ds.delete_car(car_id, 1)
        self.assertTrue(result > 0)

    def test_categories_list(self):
        ds = DataHelper()
        result = ds.get_categories()
        self.assertTrue(len(result) == 11)

    def test_brand_list(self):
        ds = DataHelper()
        result = ds.get_brands()
        self.assertTrue(len(result) == 37)


if __name__ == '__main__':
    unittest.main()
