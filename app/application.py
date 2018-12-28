#!/usr/bin/python

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for
from flask import session as login_session
from flask import make_response

import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import hmac
import hashlib
from core.datahelper import DataHelper

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True
app.static_folder = 'static'


@app.route('/', methods=['GET'])
def home():
    dh = DataHelper()
    categories = dh.get_categories()
    cars = dh.get_recent_listings()
    return render_template('public_home.html', categories=categories, cars=cars)


@app.route('/<int:car_id>/view')
def show_car(car_id):
    dh = DataHelper()
    car = dh.get_car_info(car_id)
    if car is None:
        return render_template('not_found.html')
    else:
        return render_template('public_car_view.html', car=car)


@app.route('/<string:category_name>/listings')
def by_category(category_name):
    dh = DataHelper()
    categories = dh.get_categories()
    category_id, cars = \
        dh.get_category_listings(
            string.capwords(category_name.replace('+', ' ')))
    return render_template('public_category_listings.html', categories=categories,
                           cars=cars, category_id=category_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
