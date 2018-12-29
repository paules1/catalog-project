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
        flash('Resource not found.')
        return render_template('error.html')
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


@app.route('/car/add', methods=['GET', 'POST'])
def add_car():
    dh = DataHelper()
    categories = dh.get_categories()
    brands = dh.get_brands()
    if request.method == 'GET':
        car = {
            'category': '',
            'brand': '',
            'model': '',
            'description': '',
            'price': ''
        }
        return render_template(
            'add_car.html', categories=categories, brands=brands, car=car)
    else:
        user_id = dh.get_user_id('jd@domain.com')
        car = {
            'category': int(request.form['category']),
            'brand': int(request.form['brand']),
            'model': request.form['model'],
            'description': request.form['description'],
            'price': request.form['price']
        }
        model = request.form['model']
        car_id = dh.get_car_id(model, user_id)
        if car_id is None:
            car['user_id'] = user_id
            new_car_id = dh.create_car(car)
            flash('Listing successfully created.')
            return redirect(url_for('show_car', car_id=new_car_id))
        else:
            flash('Model already exists on your listings.')
            return render_template(
                'add_car.html', categories=categories, brands=brands, car=car)


@app.route('/car/<int:car_id>/edit', methods=['GET', 'POST'])
def edit_car(car_id):
    dh = DataHelper()
    user_id = dh.get_user_id('jd@domain.com')
    categories = dh.get_categories()
    brands = dh.get_brands()
    if request.method == 'GET':
        car_info = dh.get_car_info(car_id)
        if car_info is None:
            flash('Resource not found')
            return render_template('error.html')
        else:
            car = {
                'category': car_info.category_id,
                'brand': car_info.brand_id,
                'model': car_info.model,
                'description': car_info.description,
                'price': car_info.price,
                'id': car_info.id
            }
            return render_template(
                'edit_car.html', categories=categories, brands=brands, car=car)
    else:
        user_id = dh.get_user_id('jd@domain.com')
        car = {
            'category': int(request.form['category']),
            'brand': int(request.form['brand']),
            'model': request.form['model'],
            'description': request.form['description'],
            'price': request.form['price'],
            'user_id': user_id,
            'id': car_id
        }
        result = dh.update_car(car)
        if result:
            flash('Listing successfully updated.')
            return redirect(url_for('show_car', car_id=car_id))
        else:
            return 'Error'


@app.route('/car/<int:car_id>/delete', methods=['GET', 'POST'])
def delete_car(car_id):
    dh = DataHelper()
    user_id = dh.get_user_id('jd@domain.com')
    if request.method == 'GET':
        car_info = dh.get_car_info(car_id)
        return render_template(
            'delete_car.html', car=car_info)
    else:
        car_info = dh.get_car_info(car_id)
        model = car_info.model
        result = dh.delete_car(car_id, user_id)
        if result > 0:
            flash('Listing: %s was deleted.' % model)
            return render_template('message.html')
        else:
            flash('Listing: %s was not deleted.' % model)
            return render_template('error.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
