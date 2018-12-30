#!/usr/bin/env python

from core.datahelper import DataHelper

if __name__ == '__main__':
    ds = DataHelper()
    ds.create_tables()
    ds.import_categories('imports/categories.txt')
    ds.import_brands('imports/brands.txt')
    # Add Default User
    user_id = ds.get_user_id('jd@domain.com')
    if user_id is None:
        user_id = ds.create_user({
            'username': 'John Doe',
            'email': 'jd@domain.com',
            'picture': ''
        })
    # Add Listings
    category_id = ds.get_category_id('Convertibles')
    brand_id = ds.get_brand_id('Porsche')
    user_id = ds.get_user_id('jd@domain.com')
    car_id = ds.get_car_id('Boxster', user_id)
    if car_id is None:
        car_id = ds.create_car({
            'model': 'Boxster',
            'price': '$25,000',
            'description': '2011 Porsche Boxster, Red, Manual Transmission',
            'category': category_id,
            'brand': brand_id,
            'user_id': user_id
        })
    car_id = ds.get_car_id('Boxster S', user_id)
    if car_id is None:
        car_id = ds.create_car({
            'model': 'Boxster S',
            'price': '$30,000',
            'description': '2011 Porsche Boxster S, Black, Automatic',
            'category': category_id,
            'brand': brand_id,
            'user_id': user_id
        })
