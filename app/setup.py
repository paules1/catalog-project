#!/usr/bin/env python

from dataservice import DataService

if __name__ == '__main__':
    ds = DataService()
    ds.create_tables()
    ds.import_categories('imports/categories.txt')
    ds.import_brands('imports/brands.txt')
