#!/usr/bin/python
import random
import string
import httplib2
import json
import requests
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
from functools import wraps
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from core.datahelper import DataHelper

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True
app.static_folder = 'static'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'g_plus_id' not in login_session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def home():
    dh = DataHelper()
    user_id = None
    if 'email' in login_session:
        user_id = dh.get_user_id(login_session['email'])
    categories = dh.get_categories()
    cars = dh.get_recent_listings()
    return render_template('home.html', categories=categories, cars=cars, user=user_id)


@app.route('/<int:car_id>/view')
def show_car(car_id):
    dh = DataHelper()
    user_id = None
    if 'email' in login_session:
        user_id = dh.get_user_id(login_session['email'])
    car = dh.get_car_info(car_id)
    if car is None:
        flash('Resource not found.')
        return render_template('error.html')
    else:
        return render_template('view_car.html', car=car, user=user_id)


@app.route('/<string:category_name>/listings')
def by_category(category_name):
    dh = DataHelper()
    user_id = None
    if 'email' in login_session:
        user_id = dh.get_user_id(login_session['email'])
    categories = dh.get_categories()
    category_id, cars = \
        dh.get_category_listings(
            string.capwords(category_name.replace('+', ' ')))
    return render_template('category.html', categories=categories,
                           cars=cars, category_id=category_id, user=user_id)


@app.route('/car/add', methods=['GET', 'POST'])
@login_required
def add_car():
    dh = DataHelper()
    categories = dh.get_categories()
    brands = dh.get_brands()
    user_id = dh.get_user_id(login_session['email'])
    if request.method == 'GET':
        car = {
            'category': '',
            'brand': '',
            'model': '',
            'description': '',
            'price': ''
        }
        return render_template(
            'add_car.html', categories=categories, brands=brands, car=car, user=user_id)
    else:
        car = {
            'category': int(request.form['category']),
            'brand': int(request.form['brand']),
            'model': request.form['model'],
            'description': request.form['description'],
            'price': request.form['price'],
            'user_id': user_id
        }
        model = request.form['model']
        car_id = dh.get_car_id(model, user_id)
        if car_id is None:
            new_car_id = dh.create_car(car)
            flash('Listing successfully created.')
            return redirect(url_for('show_car', car_id=new_car_id))
        else:
            flash('Model already exists on your listings.')
            return render_template(
                'add_car.html', categories=categories, brands=brands, car=car)


@app.route('/car/<int:car_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_car(car_id):
    dh = DataHelper()
    user_id = dh.get_user_id(login_session['email'])
    car_info = dh.get_car_info(car_id)
    if car_info is None:
        flash('Resource not found')
        return render_template('error.html')
    if car_info.user_id != user_id:
        flash('Listing belongs to another user')
        return render_template('error.html')
    categories = dh.get_categories()
    brands = dh.get_brands()
    if request.method == 'GET':
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
        user_id = dh.get_user_id(login_session['email'])
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
@login_required
def delete_car(car_id):
    dh = DataHelper()
    user_id = dh.get_user_id(login_session['email'])
    car_info = dh.get_car_info(car_id)
    if car_info is None:
        flash('Resource not found')
        return render_template('error.html')
    if car_info.user_id != user_id:
        flash('Listing belongs to another user')
        return render_template('error.html')

    if request.method == 'GET':
        return render_template(
            'delete_car.html', car=car_info)
    else:
        model = car_info.model
        result = dh.delete_car(car_id, user_id)
        if result > 0:
            flash('Listing: %s was deleted.' % model)
            return render_template('message.html')
        else:
            flash('Listing: %s was not deleted.' % model)
            return render_template('error.html')


@app.route('/login')
def login():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', state=state, google_client_id=CLIENT_ID)


@app.route('/google/login', methods=['POST'])
def google_login():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='', )
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error'), 500))
        response.headers['Content-Type'] = 'application/json'
        return response
    g_plus_id = credentials.id_token['sub']
    if result['user_id'] != g_plus_id:
        response = make_response(json.dumps('Token\'s user ID doesn\'t match given user ID.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps('Token\'s client ID doesn\'t match given user ID.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_g_plus_id = login_session.get('g_plus_id')

    if stored_credentials is not None and g_plus_id == stored_g_plus_id:
        response = make_response(json.dumps('Current user already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['credentials'] = credentials.access_token
    login_session['g_plus_id'] = g_plus_id
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(user_info_url, params=params)
    print(answer.text)
    data = json.loads(answer.text)
    login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    dh = DataHelper()
    user_id = dh.get_user_id(login_session['email'])
    if not user_id:
        user_id = dh.create_user(login_session)
    login_session['user_id'] = user_id

    flash('You are now logged in as %s' % login_session['username'])
    output = 'Welcome %s' % login_session['username']
    response = make_response(json.dumps(output), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/logout')
def logout():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current User not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    print(access_token)
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['g_plus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully disconnected')
        return redirect(url_for('home'))
    else:
        response = make_response(json.dumps('Failed to revoke token'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog.json')
def full_catalog():
    dh = DataHelper()
    menu_items = dh.get_items(restaurant_id)
    return jsonify(menu_items=[item.serialize for item in menu_items])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
