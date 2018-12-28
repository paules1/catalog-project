#!/usr/bin/env python

import unittest
from services.dataservice import DataService


class TestDataMethods(unittest.TestCase):

    def test_user_create(self):
        ds = DataService()
        user_id = ds.get_user_id('paules@mercabyte.com')
        if user_id is None:
            user_id = ds.create_user({
                'username': 'Paul E Villacreces',
                'email': 'paules@mercabyte.com',
                'picture': 'None'
            })
        self.assertEquals(ds.get_user_info(user_id).email, 'paules@mercabyte.com')


if __name__ == '__main__':
    unittest.main()
