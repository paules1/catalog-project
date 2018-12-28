#!/usr/bin/env python

from core.datahelper import DataHelper

if __name__ == '__main__':
    ds = DataHelper()
    ds.create_tables()
    ds.import_categories('imports/categories.txt')
    ds.import_brands('imports/brands.txt')
